"""weight_alloc — FR-021 through FR-026: Weight aggregation, rounding, allocation, and validation."""

import logging
from decimal import Decimal

from .errors import ErrorCode, ProcessingError
from .models import InvoiceItem, PackingItem, PackingTotals
from .utils import WEIGHT_PRECISION_MAX, WEIGHT_PRECISION_MIN, round_half_up

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_AGGREGATE_THRESHOLD = Decimal("0.1")
_ZERO = Decimal("0")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _aggregate_weights(
    packing_items: list[PackingItem],
) -> tuple[dict[str, Decimal], dict[str, Decimal]]:
    """Aggregate NW and QTY by part_no from packing items (FR-021).

    Sums PackingItem.nw directly — continuation rows already have nw=0.0
    from extract_packing.py, so no filtering by is_first_row_of_merge is needed.

    Args:
        packing_items: Extracted packing items.

    Returns:
        Tuple of (weight_by_part, qty_by_part) dicts keyed by stripped part_no.

    Raises:
        ProcessingError: ERR_042 if aggregated weight is zero for any part.
        ProcessingError: ERR_045 if aggregated qty is zero for any part.
    """
    weight_by_part: dict[str, Decimal] = {}
    qty_by_part: dict[str, Decimal] = {}

    for item in packing_items:
        key = item.part_no.strip()
        weight_by_part[key] = weight_by_part.get(key, _ZERO) + item.nw
        qty_by_part[key] = qty_by_part.get(key, _ZERO) + item.qty

    # Validate all aggregated weights are non-zero
    for part_no, weight in weight_by_part.items():
        if weight == _ZERO:
            msg = f"Aggregated NW is zero for part_no '{part_no}'"
            logger.error(
                "[%s] %s: %s",
                ErrorCode.ERR_042.value,
                ErrorCode.ERR_042.name,
                msg,
            )
            raise ProcessingError(
                code=ErrorCode.ERR_042,
                message=msg,
                context={"part_no": part_no},
            )

    # Validate all aggregated qtys are non-zero
    for part_no, qty in qty_by_part.items():
        if qty == _ZERO:
            msg = f"Total qty is zero for part_no '{part_no}'"
            logger.error(
                "[%s] %s: %s",
                ErrorCode.ERR_045.value,
                ErrorCode.ERR_045.name,
                msg,
            )
            raise ProcessingError(
                code=ErrorCode.ERR_045,
                message=msg,
                context={"part_no": part_no},
            )

    return weight_by_part, qty_by_part


def _validate_aggregate_vs_total(
    weight_by_part: dict[str, Decimal],
    total_nw: Decimal,
) -> None:
    """Validate packing sum vs total_nw within threshold (FR-022).

    Args:
        weight_by_part: Aggregated weights by part_no.
        total_nw: Total NW from packing totals.

    Raises:
        ProcessingError: ERR_047 if difference exceeds 0.1.
    """
    packing_sum = sum(weight_by_part.values(), _ZERO)
    diff = abs(packing_sum - total_nw)

    if diff > _AGGREGATE_THRESHOLD:
        msg = (
            f"Aggregated packing sum {packing_sum} differs from "
            f"total_nw {total_nw} by {diff} (threshold: {_AGGREGATE_THRESHOLD})"
        )
        logger.error(
            "[%s] %s: %s",
            ErrorCode.ERR_047.value,
            ErrorCode.ERR_047.name,
            msg,
        )
        raise ProcessingError(
            code=ErrorCode.ERR_047,
            message=msg,
            context={
                "packing_sum": str(packing_sum),
                "total_nw": str(total_nw),
                "difference": str(diff),
            },
        )


def _determine_precision(
    weight_by_part: dict[str, Decimal],
    total_nw: Decimal,
    base_precision: int,
) -> int:
    """Determine optimal packing precision via sum matching + zero check (FR-023).

    Step 1 — Sum matching (try N then N+1):
      1. Round all aggregated part weights to precision N.
      2. If rounded sum equals total_nw -> use N.
      3. Else try N+1: if match -> use N+1.
      4. Else use N+1 with remainder correction.

    Step 2 — Zero check (independent, runs after Step 1):
      If any weight rounds to zero at chosen precision, escalate +1
      up to max 5. If still zero at 5 -> ERR_044.

    Args:
        weight_by_part: Aggregated weights by part_no.
        total_nw: Total NW from packing totals.
        base_precision: Base precision N derived from total_nw_precision.

    Returns:
        The chosen packing precision.

    Raises:
        ProcessingError: ERR_044 if any weight rounds to zero at max precision 5.
    """
    weights = list(weight_by_part.values())

    # Step 1: Sum matching
    precision = base_precision
    logger.info("Trying precision: %d", precision)

    rounded_at_n = [round_half_up(w, precision) for w in weights]
    rounded_sum_n = sum(rounded_at_n, _ZERO)
    logger.info("Expecting rounded part sum: %s, Target: %s", rounded_sum_n, total_nw)

    if rounded_sum_n == total_nw:
        logger.info("Perfect match at %d decimals", precision)
    else:
        # Try N+1
        precision_n1 = min(base_precision + 1, WEIGHT_PRECISION_MAX)
        logger.info("Trying precision: %d", precision_n1)

        rounded_at_n1 = [round_half_up(w, precision_n1) for w in weights]
        rounded_sum_n1 = sum(rounded_at_n1, _ZERO)
        logger.info(
            "Expecting rounded part sum: %s, Target: %s",
            rounded_sum_n1,
            total_nw,
        )

        if rounded_sum_n1 == total_nw:
            logger.info("Perfect match at %d decimals", precision_n1)
            precision = precision_n1
        else:
            # Use N+1 with remainder correction (FR-024 will handle it)
            precision = precision_n1

    # Step 2: Zero check (independent — may escalate further)
    current = precision
    while current <= WEIGHT_PRECISION_MAX:
        rounded = [round_half_up(w, current) for w in weights]
        if all(r != _ZERO for r in rounded):
            break
        if current == WEIGHT_PRECISION_MAX:
            # Collect all offending parts
            zero_parts = [pn for pn, w in weight_by_part.items() if round_half_up(w, WEIGHT_PRECISION_MAX) == _ZERO]
            max_prec = WEIGHT_PRECISION_MAX
            msg = f"Weight rounds to zero at max precision {max_prec} for part_no(s): {', '.join(zero_parts)}"
            logger.error(
                "[%s] %s: %s",
                ErrorCode.ERR_044.value,
                ErrorCode.ERR_044.name,
                msg,
            )
            raise ProcessingError(
                code=ErrorCode.ERR_044,
                message=msg,
                context={"part_nos": zero_parts, "precision": WEIGHT_PRECISION_MAX},
            )
        current += 1

    # Reason: The zero check may have escalated precision beyond the sum-matching
    # result. We use the escalated value so no parts round to zero.
    if current > precision:
        precision = current

    return precision


def _round_with_remainder(
    weight_by_part: dict[str, Decimal],
    precision: int,
    total_nw: Decimal,
) -> dict[str, Decimal]:
    """Round all part weights and apply remainder correction to last part (FR-024).

    Args:
        weight_by_part: Aggregated weights by part_no.
        precision: The determined packing precision.
        total_nw: Total NW from packing totals.

    Returns:
        Dict of part_no -> rounded weight, summing exactly to total_nw.

    Raises:
        ProcessingError: ERR_041 if sum still does not equal total_nw after correction.
    """
    rounded: dict[str, Decimal] = {}
    for part_no, weight in weight_by_part.items():
        rounded[part_no] = round_half_up(weight, precision)

    # Remainder correction on the last part (dict insertion order)
    rounded_sum = sum(rounded.values(), _ZERO)
    remainder = total_nw - rounded_sum

    if remainder != _ZERO:
        last_key = list(rounded.keys())[-1]
        rounded[last_key] = rounded[last_key] + remainder

    # Defensive guard: verify sum == total_nw
    final_sum = sum(rounded.values(), _ZERO)
    if final_sum != total_nw:
        msg = f"Weight allocation mismatch after remainder correction: sum={final_sum}, total_nw={total_nw}"
        logger.error(
            "[%s] %s: %s",
            ErrorCode.ERR_041.value,
            ErrorCode.ERR_041.name,
            msg,
        )
        raise ProcessingError(
            code=ErrorCode.ERR_041,
            message=msg,
            context={"sum": str(final_sum), "total_nw": str(total_nw)},
        )

    return rounded


def _allocate_to_invoice_items(
    invoice_items: list[InvoiceItem],
    rounded_weights: dict[str, Decimal],
    packing_precision: int,
) -> list[InvoiceItem]:
    """Proportionally allocate part weights to invoice items (FR-025).

    Matches by part_no (exact match after whitespace strip).
    For each part: allocate weight proportionally by qty ratio.
    Round to packing_precision + 1. Apply remainder to last item in group.

    Args:
        invoice_items: Invoice items to populate with allocated_weight.
        rounded_weights: Rounded part weights from FR-024.
        packing_precision: The packing precision level.

    Returns:
        Invoice items with allocated_weight populated.

    Raises:
        ProcessingError: ERR_040 if invoice part_no not found in packing.
        ProcessingError: ERR_043 if packing part_no not found in invoice.
    """
    line_precision = packing_precision + 1

    # Build index: part_no -> list of indices in invoice_items
    invoice_parts: dict[str, list[int]] = {}
    for idx, item in enumerate(invoice_items):
        key = item.part_no.strip()
        invoice_parts.setdefault(key, []).append(idx)

    # Validate: every invoice part_no must exist in packing
    for part_no in invoice_parts:
        if part_no not in rounded_weights:
            msg = f"Invoice part_no '{part_no}' not found in packing"
            logger.error(
                "[%s] %s: %s",
                ErrorCode.ERR_040.value,
                ErrorCode.ERR_040.name,
                msg,
            )
            raise ProcessingError(
                code=ErrorCode.ERR_040,
                message=msg,
                context={"part_no": part_no},
            )

    # Validate: every packing part_no must exist in invoice
    for part_no in rounded_weights:
        if part_no not in invoice_parts:
            msg = f"Packing part_no '{part_no}' not found in invoice"
            logger.error(
                "[%s] %s: %s",
                ErrorCode.ERR_043.value,
                ErrorCode.ERR_043.name,
                msg,
            )
            raise ProcessingError(
                code=ErrorCode.ERR_043,
                message=msg,
                context={"part_no": part_no},
            )

    # Allocate proportionally for each part
    for part_no, part_weight in rounded_weights.items():
        indices = invoice_parts[part_no]
        total_qty = sum(invoice_items[i].qty for i in indices)

        allocated_sum = _ZERO
        for i, idx in enumerate(indices):
            item = invoice_items[idx]
            # Reason: Proportional allocation formula uses Decimal division
            # to avoid float precision loss.
            raw = part_weight * (item.qty / total_qty)
            rounded_val = round_half_up(raw, line_precision)

            if i < len(indices) - 1:
                invoice_items[idx] = item.model_copy(update={"allocated_weight": rounded_val})
                allocated_sum += rounded_val
            else:
                # Last item gets the remainder
                last_val = part_weight - allocated_sum
                invoice_items[idx] = item.model_copy(update={"allocated_weight": last_val})

    return invoice_items


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def allocate_weights(
    invoice_items: list[InvoiceItem],
    packing_items: list[PackingItem],
    packing_totals: PackingTotals,
) -> list[InvoiceItem]:
    """Full weight allocation pipeline (FR-021 through FR-026).

    Pipeline steps:
      1. Aggregate packing NW by part_no (FR-021)
      2. Validate aggregated weights are non-zero (FR-021)
      3. Validate packing sum vs total_nw within 0.1 (FR-022)
      4. Determine optimal rounding precision (FR-023)
      5. Round part weights with remainder correction (FR-024)
      6. Proportionally allocate to invoice items (FR-025)
      7. Final validation: allocated sum == total_nw (FR-026)

    Args:
        invoice_items: Extracted and transformed invoice items (FR-011, FR-018-FR-020).
        packing_items: Extracted packing items (FR-012, FR-013 validated).
        packing_totals: Total NW, GW, packets from packing sheet (FR-015-FR-017).

    Returns:
        Invoice items with allocated_weight field populated.

    Raises:
        ProcessingError: ERR_040, ERR_041, ERR_042, ERR_043, ERR_044,
                         ERR_045, ERR_047, ERR_048 at appropriate pipeline steps.
    """
    total_nw = packing_totals.total_nw
    base_precision = max(WEIGHT_PRECISION_MIN, min(packing_totals.total_nw_precision, WEIGHT_PRECISION_MAX))

    # Step 1 & 2: Aggregate and validate (FR-021)
    weight_by_part, _qty_by_part = _aggregate_weights(packing_items)

    # Step 3: Pre-allocation validation (FR-022)
    _validate_aggregate_vs_total(weight_by_part, total_nw)

    # Step 4: Determine optimal precision (FR-023)
    packing_precision = _determine_precision(weight_by_part, total_nw, base_precision)

    # Step 5: Round with remainder correction (FR-024)
    rounded_weights = _round_with_remainder(weight_by_part, packing_precision, total_nw)

    # Step 6: Proportional allocation to invoice items (FR-025)
    result = _allocate_to_invoice_items(invoice_items, rounded_weights, packing_precision)

    # Step 7: Final validation (FR-026)
    final_sum = sum(
        (item.allocated_weight for item in result if item.allocated_weight is not None),
        _ZERO,
    )

    if final_sum != total_nw:
        msg = f"Final weight validation failed: allocated sum {final_sum} != total_nw {total_nw}"
        logger.error(
            "[%s] %s: %s",
            ErrorCode.ERR_048.value,
            ErrorCode.ERR_048.name,
            msg,
        )
        raise ProcessingError(
            code=ErrorCode.ERR_048,
            message=msg,
            context={
                "allocated_sum": str(final_sum),
                "total_nw": str(total_nw),
            },
        )

    logger.info("Weight allocation complete: %s", total_nw)

    return result
