# Spec: weight_alloc.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/weight_alloc.py`
- **Tests:** `tests/test_weight_alloc.py`
- **FRs:** FR-021, FR-022, FR-023, FR-024, FR-025, FR-026

---

## 2. Functional Requirements

### FR-021 — Weight Aggregation by Part_No

Sum NW values from `packing_items` grouped by `part_no` (whitespace-stripped exact string match).

For merged NW cells and implicit continuation rows: only rows where `PackingItem.is_first_row_of_merge == True` and `nw > 0` contribute weight. Continuation rows (nw=0.0) are already zeroed by extract_packing.py — the aggregation simply sums; no re-reading of cells occurs.

**Validate all aggregated weights:**
- Aggregated weight == 0 for any part_no → **ERR_042** (PACKING_PART_ZERO_NW).
- Part's total qty == 0 for any part_no (sum of qty across all rows for the part) → **ERR_045** (ZERO_QUANTITY_FOR_PART).

### FR-022 — Pre-Allocation Validation (sum vs total_nw)

Compare sum of all aggregated packing weights against `packing_totals.total_nw`.

**Threshold:** `abs(sum - total_nw) ≤ 0.1`

**Fires before any rounding or precision adjustment.** Catches data issues (missing packing rows, wrong total row).

**Error:** ERR_047 (AGGREGATE_DISAGREE_TOTAL) if difference > 0.1.

### FR-023 — Optimal Precision Determination

**Base precision N:** determined from `total_nw` value — minimum 2, maximum 5 decimals.

**Step 1 — Sum matching (try N then N+1):**
1. Round all aggregated part weights to precision N using ROUND_HALF_UP with epsilon trick.
2. If rounded sum equals `total_nw` → use N.
3. Else try N+1: if rounded sum equals `total_nw` → use N+1.
4. Else use N+1 with remainder correction (FR-024) — never escalate to N+2 for sum matching.

**Step 2 — Zero check (independent, runs after Step 1):**
- If any weight rounds to zero at chosen precision:
  - Escalate by +1, try again. Repeat up to max precision 5.
  - Stop at first precision where no weights round to zero.
  - **Max escalation is 5 decimal places.** If still zero at 5 → ERR_044.

**Error:** ERR_044 (WEIGHT_ROUNDS_TO_ZERO) if zero weight persists at max precision 5.

### FR-024 — Rounding and Remainder Correction

Round ALL part weights to the determined packing precision using ROUND_HALF_UP with epsilon trick.

**Remainder correction:** sum all rounded weights → compute remainder = `total_nw - sum`. Add remainder to the **last part's** rounded weight so that the sum equals `total_nw` exactly.

**Error:** ERR_041 (WEIGHT_ALLOCATION_MISMATCH) if adjustment fails (sum still does not equal `total_nw` after correction — should not happen in practice; guard for defensive programming).

### FR-025 — Proportional Allocation to Invoice Items

Match invoice items to packing parts by `part_no` (exact match after whitespace strip).

**For each distinct `part_no` in packing:**
1. Find all matching `InvoiceItem` objects by part_no.
2. If no matching invoice items → ERR_043 (PACKING_PART_NOT_IN_INVOICE).
3. Compute total qty for the part across all matching invoice items.
4. For each invoice item: `allocated = part_weight × (item.qty / total_qty)`.
5. Round to **packing precision + 1** using ROUND_HALF_UP.
6. Apply remainder to the **last invoice item** in the group so that the group sum equals `part_weight` (at packing precision+1).

**For each distinct `part_no` in invoice:**
1. Find matching part in packing aggregation.
2. If no match → ERR_040 (PART_NOT_IN_PACKING).

**Precision cascade:**
- `total_nw` precision = N
- Packing weights precision = N or N+1 (from FR-023)
- Invoice item allocated_weight precision = packing precision + 1

**Matching:** whitespace strip only, exact string match. No case-folding, no fuzzy matching.

**Error:** ERR_040 (PART_NOT_IN_PACKING); ERR_043 (PACKING_PART_NOT_IN_INVOICE).

### FR-026 — Final Weight Validation

Verify that `sum(item.allocated_weight for item in invoice_items) == total_nw` (exact Decimal equality after all rounding and remainder corrections).

**Error:** ERR_048 (WEIGHT_FINAL_VALIDATION_FAILED) if sum does not equal `total_nw`.

---

## 3. Exports

```python
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
```

---

## 4. Imports

```python
from .models import InvoiceItem, PackingItem, PackingTotals
from .errors import ProcessingError, ErrorCode
from .utils import safe_decimal, round_half_up
from decimal import Decimal
import logging
```

Functions used:
- `safe_decimal(value, decimals)` — used when converting intermediate float results to Decimal during proportional allocation.
- `round_half_up(value, decimals)` — primary rounding function; called for all weight rounding (part weights and invoice item weights).

**NOTE:** `weight_alloc.py` does NOT re-read cell values. It operates on `PackingItem.nw` values already extracted and zeroed by extract_packing.py. The aggregation simply sums the `nw` field values from the list.

---

## 5. Side-Effect Rules

- **No file I/O.** Operates on model objects only.
- **No cell reading.** Does not import or use openpyxl or MergeTracker.
- **Logging:** Use `logging.getLogger(__name__)`. Log INFO for precision determination steps (FR-031 verbatim format). Log ERROR for each ERR_04x raised.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_030 (EMPTY_REQUIRED_FIELD) — owned by extract_invoice.py and extract_packing.py.
- DO NOT validate/log ERR_031 (INVALID_NUMERIC) — owned by extract_invoice.py and extract_packing.py.
- DO NOT validate/log ERR_032 (TOTAL_ROW_NOT_FOUND) — owned by extract_totals.py.
- DO NOT validate/log ERR_033 (INVALID_TOTAL_NW) — owned by extract_totals.py.
- DO NOT validate/log ERR_034 (INVALID_TOTAL_GW) — owned by extract_totals.py.
- DO NOT validate/log ERR_046 (DIFFERENT_PARTS_SHARE_MERGED_WEIGHT) — owned by extract_packing.py.

---

## 7. Gotchas

1. **NW aggregation sums `PackingItem.nw` directly from the list.** Continuation rows have `nw=Decimal('0.00000')` — they contribute zero to the sum without any re-reading. Do not apply `is_first_row_of_merge` as a filter here; extract_packing.py already zeroed non-contributing rows.
2. **part_no matching uses whitespace strip only.** Apply `.strip()` to both sides before comparison. No `.lower()`, no punctuation removal. Zero False Positive policy requires exact match.
3. **Precision zero check is INDEPENDENT from sum matching.** Even if sum matched at N, if any part weight rounds to zero at N, escalate. The escalation may force N+1 even when N worked for sum matching.
4. **Remainder correction on last part** (FR-024) is by sorted order of part_no in the aggregation dict. The "last" part is the last key in insertion order (Python 3.7+ dict ordering). Define this deterministically.
5. **Remainder correction on last invoice item** (FR-025) is the last item in the invoice_items list matching the given part_no. Ordering matters for reproducibility.
6. **Patterned examples from PRD (generalization rules):** The PRD lists specific precision examples:
   - `212.5` with General format → precision 2 (not 1). Generalize: General format minimum precision is 2.
   - N → N+1 → N+1+adjustment: never try N+2 for sum matching. Test both "match at N" and "match at N+1" cases.
   - Zero check: escalate N+1, N+2... up to 5. Test zero-at-N+1-but-ok-at-N+2 case.
7. **ERR_044 fires per-part, not once.** If two parts both round to zero at max precision 5, raise ERR_044 with both part_no values in context (collect-then-report is acceptable here; fail fast after collecting all zero-weight offenders).
8. **Decimal arithmetic only.** Never use float for any weight calculation. The epsilon trick is applied inside `round_half_up()` — call that function rather than reimplementing rounding.
9. **Proportional allocation formula:** `allocated = part_weight × (item_qty / total_part_qty)`. All operands must be Decimal; use `Decimal` division (not float).
10. **ERR_041 is a defensive guard.** If the arithmetic is correct, remainder correction should always work. Still implement the check with ERR_041 so any future regression is caught.

---

## 8. Verbatim Outputs

Console log format (FR-031):
```
[INFO] Trying precision: {N}
[INFO] Expecting rounded part sum: {val}, Target: {val}
[INFO] Perfect match at {N} decimals
[INFO] Weight allocation complete: {val}
```

---

## 9. Test Requirements (minimum 15 cases for `allocate_weights()`)

### Aggregation (FR-021)
1. **test_allocate_weights_aggregation_sums_by_part_no** — Two parts, each with one packing row; aggregated weights correct.
2. **test_allocate_weights_aggregation_continuation_rows_contribute_zero** — Part P1 has three rows: nw=[2.5, 0.0, 0.0]; aggregated weight = 2.5.
3. **test_allocate_weights_err042_zero_aggregated_weight** — Part P1 all nw=0.0; raises ERR_042.
4. **test_allocate_weights_err045_zero_qty** — Part P1 has qty=0; raises ERR_045.

### Pre-allocation validation (FR-022)
5. **test_allocate_weights_err047_sum_exceeds_threshold** — Packing sum differs from total_nw by 0.15; raises ERR_047.
6. **test_allocate_weights_sum_within_threshold_ok** — Packing sum differs from total_nw by 0.05 (within 0.1); no ERR_047.

### Precision determination (FR-023)
7. **test_allocate_weights_precision_match_at_n** — total_nw at precision 2; rounded sum matches at N=2; uses N=2.
8. **test_allocate_weights_precision_match_at_n_plus_1** — total_nw at precision 2; rounded sum at N=2 doesn't match; matches at N+1=3; uses N+1=3.
9. **test_allocate_weights_precision_uses_n_plus_1_with_remainder** — Neither N nor N+1 match exactly; uses N+1 with remainder correction.
10. **test_allocate_weights_zero_check_escalates_precision** — Part weight rounds to zero at N=2; escalated to N+1=3 where weight is non-zero.
11. **test_allocate_weights_err044_weight_rounds_to_zero_at_max_5** — Part weight so small it rounds to zero at all precisions up to 5; raises ERR_044.

### Allocation (FR-025)
12. **test_allocate_weights_proportional_single_part_multiple_items** — Part P1, weight=10.00, two items with qty=3 and qty=7; allocated weights are 3.000 and 7.000 (sum = 10.000).
13. **test_allocate_weights_remainder_applied_to_last_item** — Proportional split is uneven; last item gets the remainder so group sums to part_weight exactly.
14. **test_allocate_weights_err040_invoice_part_not_in_packing** — Invoice has part_no "P9" not in packing; raises ERR_040.
15. **test_allocate_weights_err043_packing_part_not_in_invoice** — Packing has part_no "P9" not in invoice; raises ERR_043.

### Final validation (FR-026)
16. **test_allocate_weights_err048_final_sum_mismatch** — Inject a scenario where final sum doesn't match total_nw (mock remainder correction failure); raises ERR_048.
17. **test_allocate_weights_epsilon_edge_2_28_stored_as_2_2799** — Part weight is 2.28 stored as float 2.2799999...; after epsilon rounding, allocated_weight = Decimal('2.28') exactly; no ERR_048.
