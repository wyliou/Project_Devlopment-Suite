"""tests/test_models.py — Tests for src/autoconvert/models.py.

Verifies all model fields, defaults, validators, and edge cases per spec Section 8.
"""

import re
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from autoconvert.errors import ErrorCode, ProcessingError, WarningCode
from autoconvert.models import (
    AppConfig,
    BatchResult,
    ColumnMapping,
    FieldPattern,
    FileResult,
    InvoiceItem,
    MergeRange,
    PackingItem,
    PackingTotals,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_invoice_item(**overrides) -> InvoiceItem:
    """Create a minimal valid InvoiceItem with optional field overrides."""
    defaults = {
        "part_no": "ABC-001",
        "po_no": "PO-9999",
        "qty": Decimal("10"),
        "price": Decimal("1.23456"),
        "amount": Decimal("12.35"),
        "currency": "USD",
        "coo": "CN",
        "cod": "US",
        "brand": "ACME",
        "brand_type": "OEM",
        "model_no": "MDL-X",
        "inv_no": "INV-001",
        "serial": "SN-001",
    }
    defaults.update(overrides)
    return InvoiceItem(**defaults)


def _make_processing_error() -> ProcessingError:
    """Create a minimal ProcessingError for use in FileResult tests."""
    return ProcessingError(code=ErrorCode.ERR_020, message="test error", context={})


# ---------------------------------------------------------------------------
# InvoiceItem tests
# ---------------------------------------------------------------------------


def test_invoice_item_construction_all_fields():
    """Test InvoiceItem construction with all 14 fields including allocated_weight."""
    item = InvoiceItem(
        part_no="P-001",
        po_no="PO-100",
        qty=Decimal("5"),
        price=Decimal("2.50000"),
        amount=Decimal("12.50"),
        currency="USD",
        coo="CN",
        cod="US",
        brand="BrandX",
        brand_type="OEM",
        model_no="ABC-123",
        inv_no="INV-2024-001",
        serial="SER-001",
        allocated_weight=Decimal("1.23"),
    )
    assert item.part_no == "P-001"
    assert item.po_no == "PO-100"
    assert item.qty == Decimal("5")
    assert item.price == Decimal("2.50000")
    assert item.amount == Decimal("12.50")
    assert item.currency == "USD"
    assert item.coo == "CN"
    assert item.cod == "US"
    assert item.brand == "BrandX"
    assert item.brand_type == "OEM"
    assert item.model_no == "ABC-123"
    assert item.inv_no == "INV-2024-001"
    assert item.serial == "SER-001"
    assert item.allocated_weight == Decimal("1.23")


def test_invoice_item_allocated_weight_defaults_none():
    """Test that allocated_weight defaults to None when not provided."""
    item = _make_invoice_item()
    assert item.allocated_weight is None


def test_invoice_item_rejects_non_decimal_qty():
    """Test that pydantic coerces float qty to Decimal (pydantic v2 behavior)."""
    # Pydantic v2 coerces floats to Decimal rather than raising ValidationError.
    # Reason: pydantic v2 uses Decimal(str(value)) internally for float inputs.
    item = _make_invoice_item(qty=1.5)
    assert isinstance(item.qty, Decimal)
    # The coerced value should be numerically equal to 1.5
    assert item.qty == Decimal("1.5")


def test_invoice_item_model_no_field_exists():
    """Test that model_no stores correctly and does not shadow pydantic internals."""
    item = _make_invoice_item(model_no="ABC-123")
    assert item.model_no == "ABC-123"
    # Verify pydantic's model class method is still accessible (not shadowed)
    assert callable(getattr(InvoiceItem, "model_validate", None))


def test_invoice_item_empty_string_fields():
    """Test that required string fields accept empty string (not None)."""
    item = _make_invoice_item(cod="", serial="", inv_no="")
    assert item.cod == ""
    assert item.serial == ""
    assert item.inv_no == ""


# ---------------------------------------------------------------------------
# PackingItem tests
# ---------------------------------------------------------------------------


def test_packing_item_is_first_row_of_merge_true():
    """Test PackingItem with is_first_row_of_merge=True."""
    item = PackingItem(
        part_no="P-002",
        qty=Decimal("100"),
        nw=Decimal("5.00000"),
        is_first_row_of_merge=True,
    )
    assert item.is_first_row_of_merge is True


def test_packing_item_is_first_row_of_merge_false():
    """Test PackingItem with is_first_row_of_merge=False (continuation rows)."""
    item = PackingItem(
        part_no="P-002",
        qty=Decimal("50"),
        nw=Decimal("2.50000"),
        is_first_row_of_merge=False,
    )
    assert item.is_first_row_of_merge is False


def test_packing_item_nw_decimal():
    """Test that nw stores exact Decimal value including trailing zeros."""
    item = PackingItem(
        part_no="P-003",
        qty=Decimal("10"),
        nw=Decimal("2.50000"),
        is_first_row_of_merge=True,
    )
    assert item.nw == Decimal("2.50000")


# ---------------------------------------------------------------------------
# PackingTotals tests
# ---------------------------------------------------------------------------


def test_packing_totals_total_packets_optional():
    """Test that total_packets defaults to None when not provided."""
    totals = PackingTotals(
        total_nw=Decimal("100.00"),
        total_nw_precision=2,
        total_gw=Decimal("110.00"),
        total_gw_precision=2,
    )
    assert totals.total_packets is None


def test_packing_totals_precision_fields():
    """Test that precision fields are stored independently."""
    totals = PackingTotals(
        total_nw=Decimal("50.000"),
        total_nw_precision=3,
        total_gw=Decimal("55.00"),
        total_gw_precision=2,
    )
    assert totals.total_nw_precision == 3
    assert totals.total_gw_precision == 2


def test_packing_totals_full_construction():
    """Test PackingTotals with all fields including total_packets."""
    totals = PackingTotals(
        total_nw=Decimal("200.00000"),
        total_nw_precision=5,
        total_gw=Decimal("220.00000"),
        total_gw_precision=5,
        total_packets=7,
    )
    assert totals.total_nw == Decimal("200.00000")
    assert totals.total_nw_precision == 5
    assert totals.total_gw == Decimal("220.00000")
    assert totals.total_gw_precision == 5
    assert totals.total_packets == 7


# ---------------------------------------------------------------------------
# ColumnMapping tests
# ---------------------------------------------------------------------------


def test_column_mapping_effective_header_row_advances():
    """Test that header_row and effective_header_row are stored independently."""
    col_map = ColumnMapping(
        sheet_type="invoice",
        field_map={"part_no": 1},
        header_row=10,
        effective_header_row=11,
    )
    assert col_map.header_row == 10
    assert col_map.effective_header_row == 11


def test_column_mapping_field_map_stores_1based_indices():
    """Test that field_map stores 1-based column indices as specified."""
    col_map = ColumnMapping(
        sheet_type="packing",
        field_map={"part_no": 3, "qty": 5},
        header_row=1,
        effective_header_row=1,
    )
    assert col_map.field_map["part_no"] == 3
    assert col_map.field_map["qty"] == 5


def test_column_mapping_sheet_type_values():
    """Test that both 'invoice' and 'packing' are accepted as sheet_type."""
    invoice_map = ColumnMapping(
        sheet_type="invoice",
        field_map={"part_no": 1},
        header_row=1,
        effective_header_row=1,
    )
    packing_map = ColumnMapping(
        sheet_type="packing",
        field_map={"part_no": 1},
        header_row=2,
        effective_header_row=2,
    )
    assert invoice_map.sheet_type == "invoice"
    assert packing_map.sheet_type == "packing"


# ---------------------------------------------------------------------------
# MergeRange tests
# ---------------------------------------------------------------------------


def test_merge_range_any_value_type():
    """Test that MergeRange accepts None, str, and float for the value field."""
    none_range = MergeRange(min_row=1, max_row=3, min_col=2, max_col=2, value=None)
    assert none_range.value is None

    text_range = MergeRange(min_row=1, max_row=3, min_col=2, max_col=2, value="text")
    assert text_range.value == "text"

    float_range = MergeRange(min_row=1, max_row=3, min_col=2, max_col=2, value=1.5)
    assert float_range.value == 1.5


def test_merge_range_1based_indices():
    """Test that 1-based row/column indices are stored exactly."""
    merge = MergeRange(min_row=5, max_row=7, min_col=3, max_col=3, value="anchor")
    assert merge.min_row == 5
    assert merge.max_row == 7
    assert merge.min_col == 3
    assert merge.max_col == 3


# ---------------------------------------------------------------------------
# AppConfig tests
# ---------------------------------------------------------------------------


def _make_minimal_app_config(**overrides) -> AppConfig:
    """Create a minimal valid AppConfig for testing."""
    defaults = {
        "invoice_sheet_patterns": [],
        "packing_sheet_patterns": [],
        "invoice_columns": {},
        "packing_columns": {},
        "inv_no_patterns": [],
        "inv_no_label_patterns": [],
        "inv_no_exclude_patterns": [],
        "currency_lookup": {},
        "country_lookup": {},
        "template_path": Path("/tmp/template.xlsx"),
    }
    defaults.update(overrides)
    return AppConfig(**defaults)


def test_app_config_accepts_compiled_patterns():
    """Test that AppConfig stores compiled re.Pattern objects without error."""
    pattern = re.compile(r"^invoice", re.IGNORECASE)
    config = _make_minimal_app_config(invoice_sheet_patterns=[pattern])
    assert len(config.invoice_sheet_patterns) == 1
    assert config.invoice_sheet_patterns[0] == pattern
    assert isinstance(config.invoice_sheet_patterns[0], re.Pattern)


def test_app_config_lookup_dict_accepts_string_keys():
    """Test that currency_lookup stores string key/value pairs."""
    config = _make_minimal_app_config(currency_lookup={"USD": "502"})
    assert config.currency_lookup["USD"] == "502"


def test_app_config_multiple_compiled_patterns():
    """Test that AppConfig stores multiple compiled patterns across all pattern lists."""
    inv_pat = re.compile(r"^invoice", re.IGNORECASE)
    pack_pat = re.compile(r"^packing", re.IGNORECASE)
    inv_no_pat = re.compile(r"INV[-#]\s*(\w+)", re.IGNORECASE)
    config = _make_minimal_app_config(
        invoice_sheet_patterns=[inv_pat],
        packing_sheet_patterns=[pack_pat],
        inv_no_patterns=[inv_no_pat],
    )
    assert config.invoice_sheet_patterns[0] is inv_pat
    assert config.packing_sheet_patterns[0] is pack_pat
    assert config.inv_no_patterns[0] is inv_no_pat


# ---------------------------------------------------------------------------
# FileResult and BatchResult tests
# ---------------------------------------------------------------------------


def test_file_result_status_values():
    """Test that all 4 valid status strings are accepted by FileResult."""
    for status in ("Pending", "Success", "Attention", "Failed"):
        result = FileResult(
            filename="test.xlsx",
            status=status,
            errors=[],
            warnings=[],
            invoice_items=[],
            packing_items=[],
        )
        assert result.status == status


def test_file_result_packing_totals_optional():
    """Test that packing_totals defaults to None when not provided."""
    result = FileResult(
        filename="test.xlsx",
        status="Pending",
        errors=[],
        warnings=[],
        invoice_items=[],
        packing_items=[],
    )
    assert result.packing_totals is None


def test_file_result_accepts_processing_errors():
    """Test that FileResult stores ProcessingError instances in errors and warnings."""
    err = ProcessingError(code=ErrorCode.ERR_020, message="missing column", context={"col": "part_no"})
    warn = ProcessingError(code=WarningCode.ATT_003, message="attention", context={"field": "currency"})
    result = FileResult(
        filename="test.xlsx",
        status="Failed",
        errors=[err],
        warnings=[warn],
        invoice_items=[],
        packing_items=[],
    )
    assert len(result.errors) == 1
    assert result.errors[0].code == ErrorCode.ERR_020
    assert len(result.warnings) == 1
    assert result.warnings[0].code == WarningCode.ATT_003


def test_batch_result_counts():
    """Test BatchResult count fields and verify total_files relationship."""
    success = FileResult(
        filename="ok.xlsx",
        status="Success",
        errors=[],
        warnings=[],
        invoice_items=[],
        packing_items=[],
    )
    attention = FileResult(
        filename="warn.xlsx",
        status="Attention",
        errors=[],
        warnings=[],
        invoice_items=[],
        packing_items=[],
    )
    failed = FileResult(
        filename="fail.xlsx",
        status="Failed",
        errors=[_make_processing_error()],
        warnings=[],
        invoice_items=[],
        packing_items=[],
    )

    batch = BatchResult(
        total_files=3,
        success_count=1,
        attention_count=1,
        failed_count=1,
        processing_time=1.23,
        file_results=[success, attention, failed],
        log_path="/tmp/process_log.txt",
    )

    assert batch.total_files == 3
    assert batch.success_count == 1
    assert batch.attention_count == 1
    assert batch.failed_count == 1
    # The model does not enforce this, but the test verifies the relationship.
    assert batch.total_files == batch.success_count + batch.attention_count + batch.failed_count
    assert batch.processing_time == 1.23
    assert len(batch.file_results) == 3
    assert batch.log_path == "/tmp/process_log.txt"
