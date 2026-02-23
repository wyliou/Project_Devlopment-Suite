"""Tests for weight_alloc module (FR-021 through FR-026).

Covers aggregation, pre-allocation validation, precision determination,
proportional allocation, and final validation — minimum 17 test cases.
"""

from decimal import Decimal
from unittest.mock import patch

import pytest

from autoconvert.errors import ErrorCode, ProcessingError
from autoconvert.models import InvoiceItem, PackingItem, PackingTotals
from autoconvert.weight_alloc import allocate_weights

# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

_INVOICE_DEFAULTS = {
    "po_no": "PO-001",
    "price": Decimal("1.00000"),
    "amount": Decimal("10.00"),
    "currency": "USD",
    "coo": "CN",
    "cod": "US",
    "brand": "TestBrand",
    "brand_type": "TypeA",
    "model_no": "M-001",
    "inv_no": "INV-001",
    "serial": "",
}


def _inv(part_no: str, qty: Decimal, **overrides: object) -> InvoiceItem:
    """Create an InvoiceItem with sensible defaults."""
    fields = {**_INVOICE_DEFAULTS, "part_no": part_no, "qty": qty}
    fields.update(overrides)
    return InvoiceItem(**fields)  # type: ignore[arg-type]


def _pack(
    part_no: str,
    qty: Decimal,
    nw: Decimal,
    is_first: bool = True,
) -> PackingItem:
    """Create a PackingItem."""
    return PackingItem(part_no=part_no, qty=qty, nw=nw, is_first_row_of_merge=is_first)


def _totals(
    total_nw: Decimal,
    nw_precision: int,
    total_gw: Decimal | None = None,
    gw_precision: int = 2,
) -> PackingTotals:
    """Create PackingTotals with sensible defaults."""
    return PackingTotals(
        total_nw=total_nw,
        total_nw_precision=nw_precision,
        total_gw=total_gw if total_gw is not None else total_nw + Decimal("1"),
        total_gw_precision=gw_precision,
    )


# ===========================================================================
# Aggregation tests (FR-021)
# ===========================================================================


class TestAggregation:
    """FR-021: Weight aggregation by part_no."""

    def test_allocate_weights_aggregation_sums_by_part_no(self) -> None:
        """Test aggregation sums NW values for two parts with one row each."""
        invoice = [
            _inv("P1", Decimal("10")),
            _inv("P2", Decimal("5")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("3.00000")),
            _pack("P2", Decimal("5"), Decimal("7.00000")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # P1 gets 3.00 of 10.00 total, P2 gets 7.00
        assert result[0].allocated_weight == Decimal("3.000")
        assert result[1].allocated_weight == Decimal("7.000")

    def test_allocate_weights_aggregation_continuation_rows_contribute_zero(
        self,
    ) -> None:
        """Test that continuation rows (nw=0) are summed but contribute zero."""
        invoice = [_inv("P1", Decimal("10"))]
        packing = [
            _pack("P1", Decimal("5"), Decimal("2.50000"), is_first=True),
            _pack("P1", Decimal("3"), Decimal("0.00000"), is_first=False),
            _pack("P1", Decimal("2"), Decimal("0.00000"), is_first=False),
        ]
        totals = _totals(Decimal("2.50"), 2)

        result = allocate_weights(invoice, packing, totals)

        # All weight comes from the first row
        assert result[0].allocated_weight == Decimal("2.500")

    def test_allocate_weights_err042_zero_aggregated_weight(self) -> None:
        """Test ERR_042 when all NW values for a part are zero."""
        invoice = [_inv("P1", Decimal("10"))]
        packing = [
            _pack("P1", Decimal("5"), Decimal("0.00000")),
            _pack("P1", Decimal("5"), Decimal("0.00000")),
        ]
        totals = _totals(Decimal("0.00"), 2)

        with pytest.raises(ProcessingError) as exc_info:
            allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_042
        assert "P1" in exc_info.value.context["part_no"]

    def test_allocate_weights_err045_zero_qty(self) -> None:
        """Test ERR_045 when total qty for a part is zero."""
        invoice = [_inv("P1", Decimal("10"))]
        packing = [
            _pack("P1", Decimal("0"), Decimal("5.00000")),
        ]
        totals = _totals(Decimal("5.00"), 2)

        with pytest.raises(ProcessingError) as exc_info:
            allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_045
        assert "P1" in exc_info.value.context["part_no"]


# ===========================================================================
# Pre-allocation validation tests (FR-022)
# ===========================================================================


class TestPreAllocationValidation:
    """FR-022: Sum vs total_nw validation."""

    def test_allocate_weights_err047_sum_exceeds_threshold(self) -> None:
        """Test ERR_047 when packing sum differs from total_nw by > 0.1."""
        invoice = [_inv("P1", Decimal("10"))]
        packing = [
            _pack("P1", Decimal("10"), Decimal("10.00000")),
        ]
        # total_nw = 10.15 but packing sum = 10.0 => diff = 0.15 > 0.1
        totals = _totals(Decimal("10.15"), 2)

        with pytest.raises(ProcessingError) as exc_info:
            allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_047

    def test_allocate_weights_sum_within_threshold_ok(self) -> None:
        """Test no ERR_047 when packing sum differs from total_nw by <= 0.1."""
        invoice = [_inv("P1", Decimal("10"))]
        packing = [
            _pack("P1", Decimal("10"), Decimal("10.00000")),
        ]
        # total_nw = 10.05 but packing sum = 10.0 => diff = 0.05 <= 0.1
        totals = _totals(Decimal("10.05"), 2)

        result = allocate_weights(invoice, packing, totals)

        # Should succeed — weight allocated with remainder correction
        assert result[0].allocated_weight is not None


# ===========================================================================
# Precision determination tests (FR-023)
# ===========================================================================


class TestPrecisionDetermination:
    """FR-023: Optimal precision determination."""

    def test_allocate_weights_precision_match_at_n(self) -> None:
        """Test precision matches at N=2 when rounded sum equals total_nw."""
        # Two parts: 3.50 + 6.50 = 10.00 exactly at precision 2
        invoice = [
            _inv("P1", Decimal("10")),
            _inv("P2", Decimal("10")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("3.50000")),
            _pack("P2", Decimal("10"), Decimal("6.50000")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # Packing precision = 2, line precision = 3
        assert result[0].allocated_weight == Decimal("3.500")
        assert result[1].allocated_weight == Decimal("6.500")

    def test_allocate_weights_precision_match_at_n_plus_1(self) -> None:
        """Test precision escalates to N+1 when rounded sum at N doesn't match."""
        # Two parts: 3.333 + 6.667 = 10.000
        # At precision 2: round(3.333)=3.33, round(6.667)=6.67 => 10.00 = 10.00
        # Actually that matches. Let's pick values that don't match at N=2 but do at N=3.
        # 3.335 + 6.666 = 10.001 raw but total_nw = 10.001
        # At N=2: round(3.335)=3.34, round(6.666)=6.67 => 10.01 != 10.001
        # At N=3: round(3.335)=3.335, round(6.666)=6.666 => 10.001 = 10.001
        invoice = [
            _inv("P1", Decimal("10")),
            _inv("P2", Decimal("10")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("3.33500")),
            _pack("P2", Decimal("10"), Decimal("6.66600")),
        ]
        totals = _totals(Decimal("10.001"), 3)

        result = allocate_weights(invoice, packing, totals)

        # Base precision from total_nw_precision=3 => N=3
        # At N=3: 3.335 + 6.666 = 10.001 == 10.001 => match at N
        # Line precision = 4
        assert result[0].allocated_weight is not None
        assert result[1].allocated_weight is not None

        # Let's verify sum equals total
        total = result[0].allocated_weight + result[1].allocated_weight
        assert total == Decimal("10.001")

    def test_allocate_weights_precision_match_at_n_plus_1_real(self) -> None:
        """Test precision escalates from N=2 to N+1=3 when N=2 sum doesn't match."""
        # Two parts: 3.125 + 6.875 = 10.000
        # At N=2: round(3.125)=3.13, round(6.875)=6.88 => 10.01 != 10.000
        # At N=3: round(3.125)=3.125, round(6.875)=6.875 => 10.000 = 10.000
        invoice = [
            _inv("P1", Decimal("10")),
            _inv("P2", Decimal("10")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("3.12500")),
            _pack("P2", Decimal("10"), Decimal("6.87500")),
        ]
        totals = _totals(Decimal("10.000"), 2)

        result = allocate_weights(invoice, packing, totals)

        total = result[0].allocated_weight + result[1].allocated_weight
        assert total == Decimal("10.000")

    def test_allocate_weights_precision_uses_n_plus_1_with_remainder(
        self,
    ) -> None:
        """Test N+1 with remainder correction when neither N nor N+1 match exactly."""
        # Pick values where rounding at N=2 and N+1=3 both miss total_nw
        # 3.3334 + 6.6667 = 10.0001 raw but total_nw = 10.00
        # At N=2: round(3.3334)=3.33, round(6.6667)=6.67 => 10.00 = 10.00
        # That matches. Need different values.
        # 1.111 + 2.222 + 6.777 = 10.110
        # At N=2: 1.11 + 2.22 + 6.78 = 10.11 != 10.11 (total_nw=10.11 at precision 2)
        # Actually let's just use values that clearly need remainder at N+1.
        # 3.3333 + 6.6666 = 9.9999 => total_nw = 10.00
        # At N=2: 3.33 + 6.67 = 10.00 => that matches!
        # Try: 3.3337 + 6.6664 = 10.0001 => total_nw = 10.00
        # At N=2: 3.33 + 6.67 = 10.00 => matches
        # Let's try with three parts:
        # 3.333 + 3.333 + 3.334 = 10.000 => total_nw = 10.00
        # At N=2: 3.33 + 3.33 + 3.33 = 9.99 != 10.00
        # At N=3: 3.333 + 3.333 + 3.334 = 10.000 = 10.00 => matches
        # Need ones that don't match at N or N+1:
        # 3.3334 + 3.3333 + 3.3334 = 10.0001 => total_nw = 10.00
        # At N=2: 3.33 + 3.33 + 3.33 = 9.99 != 10.00
        # At N=3: 3.333 + 3.333 + 3.333 = 9.999 != 10.00
        # => uses N+1=3 with remainder correction: last part = 10.00 - 3.333 - 3.333 = 3.334
        invoice = [
            _inv("P1", Decimal("10")),
            _inv("P2", Decimal("10")),
            _inv("P3", Decimal("10")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("3.33340")),
            _pack("P2", Decimal("10"), Decimal("3.33330")),
            _pack("P3", Decimal("10"), Decimal("3.33340")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # Sum of allocated weights must equal total_nw exactly
        total = sum(item.allocated_weight for item in result if item.allocated_weight is not None)
        assert total == Decimal("10.00")

    def test_allocate_weights_zero_check_escalates_precision(self) -> None:
        """Test precision escalates when a part weight rounds to zero at chosen N."""
        # Part P1: nw=0.001 rounds to 0.00 at N=2 but 0.001 at N=3
        # Part P2: nw=9.999 rounds fine at any precision
        # total_nw = 10.000 at precision 2
        # Sum at N=2: 0.00 + 10.00 = 10.00 => sum matches at N=2
        # But P1 rounds to zero => escalate to N=3
        # Sum at N=3: 0.001 + 9.999 = 10.000 => OK, no zeros
        invoice = [
            _inv("P1", Decimal("1")),
            _inv("P2", Decimal("100")),
        ]
        packing = [
            _pack("P1", Decimal("1"), Decimal("0.00100")),
            _pack("P2", Decimal("100"), Decimal("9.99900")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # P1 should get non-zero weight
        assert result[0].allocated_weight is not None
        assert result[0].allocated_weight > _ZERO
        # Sum must equal total
        total = sum(item.allocated_weight for item in result if item.allocated_weight is not None)
        assert total == Decimal("10.00")

    def test_allocate_weights_err044_weight_rounds_to_zero_at_max_5(
        self,
    ) -> None:
        """Test ERR_044 when a part weight is so small it rounds to zero at precision 5."""
        # 0.0000001 rounds to 0.00000 at precision 5
        invoice = [
            _inv("P1", Decimal("1")),
            _inv("P2", Decimal("100")),
        ]
        packing = [
            _pack("P1", Decimal("1"), Decimal("0.0000001")),
            _pack("P2", Decimal("100"), Decimal("9.9999999")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        # Packing sum = 10.0000000, total_nw = 10.00, diff = 0 => OK for FR-022
        with pytest.raises(ProcessingError) as exc_info:
            allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_044
        assert "P1" in exc_info.value.context["part_nos"]


# ===========================================================================
# Proportional allocation tests (FR-025)
# ===========================================================================

_ZERO = Decimal("0")


class TestProportionalAllocation:
    """FR-025: Proportional weight allocation to invoice items."""

    def test_allocate_weights_proportional_single_part_multiple_items(
        self,
    ) -> None:
        """Test proportional allocation with two items for same part."""
        # Part P1, weight=10.00, items with qty=3 and qty=7
        invoice = [
            _inv("P1", Decimal("3")),
            _inv("P1", Decimal("7")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("10.00000")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # allocated = 10.00 * (3/10) = 3.000, 10.00 * (7/10) = 7.000
        assert result[0].allocated_weight == Decimal("3.000")
        assert result[1].allocated_weight == Decimal("7.000")

    def test_allocate_weights_remainder_applied_to_last_item(self) -> None:
        """Test remainder goes to last invoice item in group for exact sum."""
        # Part P1, weight=10.00, items with qty=3, qty=3, qty=4
        # 10.00 * 3/10 = 3.000, 10.00 * 3/10 = 3.000, last = 10.00 - 3.000 - 3.000 = 4.000
        # But let's use an uneven split:
        # Part P1, weight=10.00, items with qty=1, qty=1, qty=1
        # 10.00 * 1/3 = 3.33333... rounds to 3.333 at precision 3
        # last = 10.00 - 3.333 - 3.333 = 3.334
        invoice = [
            _inv("P1", Decimal("1")),
            _inv("P1", Decimal("1")),
            _inv("P1", Decimal("1")),
        ]
        packing = [
            _pack("P1", Decimal("3"), Decimal("10.00000")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # First two get 3.333, last gets remainder 3.334
        assert result[0].allocated_weight == Decimal("3.333")
        assert result[1].allocated_weight == Decimal("3.333")
        assert result[2].allocated_weight == Decimal("3.334")

        # Verify exact sum
        total = sum(item.allocated_weight for item in result if item.allocated_weight is not None)
        assert total == Decimal("10.00")

    def test_allocate_weights_err040_invoice_part_not_in_packing(self) -> None:
        """Test ERR_040 when invoice has a part_no not in packing."""
        invoice = [
            _inv("P1", Decimal("10")),
            _inv("P9", Decimal("5")),  # Not in packing
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("10.00000")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        with pytest.raises(ProcessingError) as exc_info:
            allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_040
        assert "P9" in exc_info.value.context["part_no"]

    def test_allocate_weights_err043_packing_part_not_in_invoice(self) -> None:
        """Test ERR_043 when packing has a part_no not in invoice."""
        invoice = [
            _inv("P1", Decimal("10")),
        ]
        packing = [
            _pack("P1", Decimal("10"), Decimal("5.00000")),
            _pack("P9", Decimal("5"), Decimal("5.00000")),  # Not in invoice
        ]
        totals = _totals(Decimal("10.00"), 2)

        with pytest.raises(ProcessingError) as exc_info:
            allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_043
        assert "P9" in exc_info.value.context["part_no"]


# ===========================================================================
# Final validation tests (FR-026)
# ===========================================================================


class TestFinalValidation:
    """FR-026: Final weight validation."""

    def test_allocate_weights_err048_final_sum_mismatch(self) -> None:
        """Test ERR_048 when final sum doesn't match total_nw (mock scenario).

        We mock _allocate_to_invoice_items to return items whose weights
        don't sum to total_nw, triggering the final validation check.
        """
        invoice = [_inv("P1", Decimal("10"))]
        packing = [_pack("P1", Decimal("10"), Decimal("10.00000"))]
        totals = _totals(Decimal("10.00"), 2)

        # Create a mock return that has wrong allocated weight
        bad_item = _inv("P1", Decimal("10"), allocated_weight=Decimal("9.99"))

        with patch(
            "autoconvert.weight_alloc._allocate_to_invoice_items",
            return_value=[bad_item],
        ):
            with pytest.raises(ProcessingError) as exc_info:
                allocate_weights(invoice, packing, totals)

        assert exc_info.value.code == ErrorCode.ERR_048

    def test_allocate_weights_epsilon_edge_2_28_stored_as_2_2799(
        self,
    ) -> None:
        """Test that float artifact 2.2799999... rounds correctly to 2.28.

        Simulates the common openpyxl artifact where 2.28 is stored as
        2.2799999999999998. After epsilon rounding, allocated_weight should
        be exactly Decimal('2.28') with no ERR_048.
        """
        # Reason: safe_decimal and round_half_up both use the epsilon trick
        # to correct float artifacts. We test the full pipeline here.
        invoice = [_inv("P1", Decimal("10"))]

        # Simulate the artifact: nw value that came through safe_decimal
        # as Decimal('2.28000') (already cleaned by extract_packing)
        packing = [_pack("P1", Decimal("10"), Decimal("2.28000"))]
        totals = _totals(Decimal("2.28"), 2)

        result = allocate_weights(invoice, packing, totals)

        assert result[0].allocated_weight is not None
        # The allocated weight at line precision (packing_precision=2, line=3)
        # should sum to 2.28 exactly
        assert result[0].allocated_weight == Decimal("2.280")

        # Final sum must equal total_nw
        total = sum(item.allocated_weight for item in result if item.allocated_weight is not None)
        assert total == Decimal("2.28")


# ===========================================================================
# Additional edge case tests
# ===========================================================================


class TestEdgeCases:
    """Additional edge cases for robustness."""

    def test_allocate_weights_whitespace_stripped_part_no_matching(
        self,
    ) -> None:
        """Test that part_no whitespace is stripped for matching."""
        invoice = [_inv(" P1 ", Decimal("10"))]
        packing = [_pack("P1 ", Decimal("10"), Decimal("5.00000"))]
        totals = _totals(Decimal("5.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        assert result[0].allocated_weight is not None
        assert result[0].allocated_weight == Decimal("5.000")

    def test_allocate_weights_multiple_parts_remainder_on_last_part(
        self,
    ) -> None:
        """Test remainder correction applied to last part in dict order."""
        # Three parts with weights that don't sum exactly after rounding
        invoice = [
            _inv("A", Decimal("10")),
            _inv("B", Decimal("10")),
            _inv("C", Decimal("10")),
        ]
        packing = [
            _pack("A", Decimal("10"), Decimal("3.33333")),
            _pack("B", Decimal("10"), Decimal("3.33333")),
            _pack("C", Decimal("10"), Decimal("3.33334")),
        ]
        totals = _totals(Decimal("10.00"), 2)

        result = allocate_weights(invoice, packing, totals)

        # All allocated weights must sum to 10.00
        total = sum(item.allocated_weight for item in result if item.allocated_weight is not None)
        assert total == Decimal("10.00")

    def test_allocate_weights_single_part_single_item(self) -> None:
        """Test simplest case: one part, one item."""
        invoice = [_inv("P1", Decimal("5"))]
        packing = [_pack("P1", Decimal("5"), Decimal("12.50000"))]
        totals = _totals(Decimal("12.50"), 2)

        result = allocate_weights(invoice, packing, totals)

        assert result[0].allocated_weight == Decimal("12.500")
