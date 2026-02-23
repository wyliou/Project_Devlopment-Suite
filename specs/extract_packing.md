# Spec: extract_packing.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/extract_packing.py`
- **Tests:** `tests/test_extract_packing.py`
- **FRs:** FR-012, FR-013

---

## 2. Functional Requirements

### FR-012 — Packing Item Extraction

Extract **3 fields** per item: `part_no`, `qty`, `nw`.

**Numeric precision:**
- `qty` = cell display precision (via `detect_cell_precision(cell)`)
- `nw` = **5 decimals** (high precision for weight allocation)

**Unit suffix stripping:** strip KG, KGS, G, LB, LBS, PCS, EA, 件, 个 before parsing via `strip_unit_suffix()`.

**Data starts at `effective_header_row + 1`** (not `header_row + 1`).

#### Merged NW Handling

Only the first row of a merged NW range retains its weight. Subsequent rows return 0.0.
- Use `MergeTracker.get_weight_value(row, nw_col, header_row)` — returns Decimal(0.0) for non-anchor rows.
- `is_first_row_of_merge` is set to `True` only for the merge anchor row.

#### Merged QTY Handling

Apply the same merged-cell and implicit-continuation logic to QTY as to NW:
- When QTY is empty AND (non-anchor merge row OR current part_no matches previous item's part_no): set QTY=0.
- Combined with NW=0.0, the `qty=0 AND nw=0` skip filter correctly removes these PO-reference rows.

#### Implicit Continuation Handling

Some vendors group multiple PO lines under one carton without merged cells (NW appears only on first row):
1. **NW continuation** — Detection: NW cell is empty AND current part_no matches previous extracted item's part_no. Treatment: set NW=0.0, `is_first_row_of_merge=False`.
2. **QTY continuation** — Detection: QTY cell is empty AND (non-anchor merge row OR current part_no matches previous item's part_no). Treatment: set QTY=Decimal(0).
3. Do NOT raise ERR_030 for continuation rows — empty fields are intentional.

Examples:
- `加高電子股份有限公司.xlsx` — CTNS=1 row has NW, continuation rows (same part, different PO) have empty NW.
- `登壹企業股份有限公司.xlsx` — rows 25–26 merged across CTNS/QTY/NW/GW; row 26 is PO-reference with only PO No. and Part No. after unmerging.

#### Merged Part_No Propagation

When `part_no` is empty AND cell is a non-anchor row of a vertical merge (check via `MergeTracker.is_in_merge()` and `MergeTracker.is_merge_anchor()`):
- Propagate anchor value via `MergeTracker.get_string_value()` so the row is processed as a data continuation with its own qty/nw.
- CRITICAL: stop condition 3 (implicit total row) must exclude these rows — a row with empty part_no due to vertical merge is a data continuation, not a total row.

Example: `12.8 发票箱单模版-苏州.xlsx` — Part No. merged vertically C23:C25; rows 24–25 have empty part_no but own NW/GW values.

#### Ditto Mark Handling

Recognized ditto characters from `DITTO_MARKS`: `"` (U+0022), `〃` (U+3003), `"` (U+201C), `"` (U+201D).

When detected in NW column:
- Set NW=0.0.
- Set `is_first_row_of_merge=False`.
- Do NOT propagate previous row's NW — prevents weight inflation in FR-021 aggregation.

#### Row Filtering (skip but don't stop)

- Skip leading blank rows before first data row.
- Skip rows where part_no contains "part no" (header continuation — case-insensitive).
- Skip pallet summary rows where part_no or row text contains "plt.", "pallet" (case-insensitive).
- Skip empty part_no rows (after propagation; only true non-merge-continuation empty rows).
- Skip rows where `qty=0 AND nw=0` (PO-reference rows after merge/continuation handling).

**DO NOT raise ERR_030 for rows skipped by these filters.**

#### Stop Conditions — Processing Order

**CRITICAL (differs from invoice):** Check stop conditions BEFORE blank check.

1. Any cell in columns A–J contains "total/合计/总计/小计" (case-insensitive via `is_stop_keyword()`).
2. Truly blank row (all key columns empty: part_no, qty, nw) after first data row.
3. Implicit total row: empty part_no + numeric NW > 0 AND GW > 0 — **exclude rows where part_no is empty due to vertical merge continuations** (use `MergeTracker.is_in_merge(row, part_no_col)` to detect continuation rows).

**Returns:** `tuple[list[PackingItem], int]` where the int is `last_data_row` (1-based row number of last extracted PackingItem).

### FR-013 — Merged Weight Cell Validation

Run immediately after `extract_packing_items()`, BEFORE weight allocation.

Check only data-area merges (rows after `header_row`):
- For each NW-column merge range in the data area: collect all distinct `part_no` values in rows covered by the merge range.
- If more than one distinct part_no shares a single NW merged cell: raise **ERR_046** (DIFFERENT_PARTS_SHARE_MERGED_WEIGHT).
- Same part_no sharing a merged NW cell: allowed.

This provides a clear root cause error instead of the downstream ERR_042 symptom.

---

## 3. Exports

```python
def extract_packing_items(
    sheet: Worksheet,
    column_map: ColumnMapping,
    merge_tracker: MergeTracker,
) -> tuple[list[PackingItem], int]:
    """Extract packing items (part_no, qty, nw) from the packing sheet.

    Args:
        sheet: Packing worksheet (already unmerged by MergeTracker).
        column_map: Column index mapping with header_row and effective_header_row.
        merge_tracker: Pre-initialized MergeTracker for merged cell propagation.

    Returns:
        Tuple of (list of PackingItem, last_data_row). last_data_row is the 1-based
        row number of the last extracted item, used by extract_totals.detect_total_row().

    Raises:
        ProcessingError: ERR_030 for empty required field (non-continuation rows);
                         ERR_031 for invalid numeric value.
    """

def validate_merged_weights(
    packing_items: list[PackingItem],
    merge_tracker: MergeTracker,
    column_map: ColumnMapping,
) -> None:
    """Validate that no different part_nos share a merged NW cell.

    Args:
        packing_items: Extracted packing items from extract_packing_items().
        merge_tracker: MergeTracker with merge range metadata.
        column_map: Column mapping to locate the NW column index.

    Returns:
        None if all merged weight cells are valid.

    Raises:
        ProcessingError: ERR_046 if different part_nos share a merged NW cell.
    """
```

---

## 4. Imports

```python
from .models import PackingItem, ColumnMapping
from .errors import ProcessingError, ErrorCode
from .merge_tracker import MergeTracker
from .utils import (
    strip_unit_suffix,
    safe_decimal,
    detect_cell_precision,
    is_stop_keyword,
    DITTO_MARKS,
)
from openpyxl.worksheet.worksheet import Worksheet
import logging
```

Functions used:
- `strip_unit_suffix(value)` — called on qty and nw cell raw values before Decimal parsing.
- `safe_decimal(value, decimals)` — `qty` (detected precision), `nw` (5 decimals).
- `detect_cell_precision(cell)` — called on qty cell for display precision.
- `is_stop_keyword(value)` — called on each cell A–J for stop condition 1.
- `DITTO_MARKS` — checked for ditto mark detection on nw cell value.
- `MergeTracker.get_weight_value(row, col, header_row)` — for nw column.
- `MergeTracker.get_string_value(row, col, header_row)` — for part_no (propagation).
- `MergeTracker.is_merge_anchor(row, col)` — to detect first row of merge.
- `MergeTracker.is_in_merge(row, col)` — to detect non-anchor continuation rows.
- `MergeTracker.get_merge_range(row, col)` — in validate_merged_weights for range iteration.
- `MergeTracker.is_data_area_merge(row, col, header_row)` — for validate_merged_weights scope check.

---

## 5. Side-Effect Rules

- **No file I/O.** Receives `Worksheet` object.
- **No config loading.** All configuration arrives via `ColumnMapping`.
- **Logging:** Use `logging.getLogger(__name__)`. Debug-log each row's raw values, continuation detection decisions, and ditto mark detections.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_014 (HEADER_ROW_NOT_FOUND) — owned by column_map.py.
- DO NOT validate/log ERR_020 (REQUIRED_COLUMN_MISSING) — owned by column_map.py.
- DO NOT validate/log ERR_032 (TOTAL_ROW_NOT_FOUND) — owned by extract_totals.py.
- DO NOT validate/log ERR_033 (INVALID_TOTAL_NW) — owned by extract_totals.py.
- DO NOT validate/log ERR_034 (INVALID_TOTAL_GW) — owned by extract_totals.py.
- DO NOT validate/log ERR_040 (PART_NOT_IN_PACKING) — owned by weight_alloc.py.
- DO NOT validate/log ERR_042 (PACKING_PART_ZERO_NW) — owned by weight_alloc.py.
- DO NOT validate/log ERR_043 (PACKING_PART_NOT_IN_INVOICE) — owned by weight_alloc.py.
- DO NOT validate/log ERR_045 (ZERO_QUANTITY_FOR_PART) — owned by weight_alloc.py.
- DO NOT validate/log ERR_047 (AGGREGATE_DISAGREE_TOTAL) — owned by weight_alloc.py.
- ATT_002 (MISSING_TOTAL_PACKETS) — owned by extract_totals.py (not this module).

---

## 7. Gotchas

1. **Stop condition ORDER differs from invoice extraction.** In packing: check stop conditions FIRST (before blank check). In invoice: check blank first (skip), then stop conditions. Reversing this causes premature stops or missed implicit total rows.
2. **Implicit total row detection must exclude merge continuations.** A row with empty part_no due to vertical merge (C23:C25 example) would falsely trigger stop condition 3 if merge awareness is missing. Use `MergeTracker.is_in_merge(row, part_no_col)` as guard.
3. **Ditto marks are in the NW column, not part_no.** Check the NW cell value against `DITTO_MARKS` before attempting numeric parsing. The four recognized characters are: `"` (U+0022), `〃` (U+3003), `"` (U+201C), `"` (U+201D).
4. **NW precision is always 5 decimals** regardless of cell format (FR-012). Cell format precision is used only for qty and for total_nw/total_gw in extract_totals.
5. **`last_data_row` is 1-based row number**, not a list index. extract_totals.detect_total_row() uses `last_data_row + 1` as its search start.
6. **Patterned format examples from PRD (generalization rules):** The PRD lists ditto marks `"`, `〃`, `"`, `"` as individual characters — each must have its own test case. Use `DITTO_MARKS` frozenset which includes all four.
7. **ERR_046 identifies the NW column merge, not the part_no merge.** validate_merged_weights checks NW/qty column merges, not part_no column merges. Part_no merges are intentional (propagation); NW merges across different parts are errors.
8. **`is_first_row_of_merge` field in PackingItem:** Set `True` for the anchor row of any weight-relevant merge (or for a row that genuinely has NW > 0 with no merge context). Set `False` for continuation rows (merged non-anchor, implicit continuation, or ditto mark rows).
9. **Unit suffix stripping before numeric parsing** applies to NW column even in packing. "2.5 KGS" → strip → "2.5" → `safe_decimal("2.5", 5)`.
10. **KGS sub-header row** (present in virtually every packing sheet) contains "KGS|KGS" as a text row immediately after the header. It is handled by the header continuation filter ("part no" check) and the blank row skip — it typically has an empty part_no column, so it falls under the empty-part_no skip rule.

---

## 8. Verbatim Outputs

Errors reference (build-plan.md Section 7):
- ERR_046: "DIFFERENT_PARTS_SHARE_MERGED_WEIGHT" — different parts share same merged weight cell.
- ERR_030: "EMPTY_REQUIRED_FIELD" — required field empty with row details.
- ERR_031: "INVALID_NUMERIC" — non-numeric value in numeric field with row/column.

---

## 9. Test Requirements

### `extract_packing_items()`

1. **test_extract_packing_items_normal_extraction** — Three rows with distinct part_no, qty, nw; verify list length 3, correct Decimal values (nw at 5 decimals), last_data_row = row number of third item.
2. **test_extract_packing_items_implicit_continuation_nw_zero** — Row 1: part_no="P1", qty=10, nw=2.5; Row 2: part_no="P1", qty=5, nw=empty (no merge); Row 2 extracted as PackingItem(nw=Decimal('0.00000'), is_first_row_of_merge=False).
3. **test_extract_packing_items_ditto_mark_sets_nw_zero** — NW cell contains `"` (U+0022); extracted as nw=Decimal('0.00000'), is_first_row_of_merge=False; no ERR_031 raised.
4. **test_extract_packing_items_ditto_mark_unicode_3003** — NW cell contains `〃` (U+3003); same result as above (separate test per distinct character).
5. **test_extract_packing_items_ditto_mark_unicode_201c** — NW cell contains `"` (U+201C); same result.
6. **test_extract_packing_items_ditto_mark_unicode_201d** — NW cell contains `"` (U+201D); same result.
7. **test_extract_packing_items_merged_part_no_propagated** — Part_no merged vertically across rows 23–25; rows 24–25 extracted with propagated part_no; stop condition 3 does NOT trigger on rows 24–25 even though part_no is empty before propagation.
8. **test_extract_packing_items_stop_at_total_keyword** — Row contains "TOTAL" in column B (within A–J); extraction stops; items before that row returned.
9. **test_extract_packing_items_stop_at_blank_row** — Truly blank row (all key columns empty) after first data row; extraction stops.
10. **test_extract_packing_items_stop_check_before_blank_check** — Row has "合计" in col A AND is also blank; stop fires on keyword (not blank) — confirms ordering.
11. **test_extract_packing_items_pallet_summary_row_skipped** — Row with part_no "PLT." skipped; extraction continues to next row.
12. **test_extract_packing_items_merged_nw_anchor_retains_weight** — Rows 5–7 share merged NW cell; Row 5 is anchor (nw=3.0); rows 6–7 extracted as nw=Decimal('0.00000').
13. **test_extract_packing_items_unit_suffix_stripped_from_nw** — NW cell "2.5 KGS"; extracted nw=Decimal('2.50000').
14. **test_extract_packing_items_err030_raised_for_non_continuation_empty_required** — Row with genuinely empty part_no (not a merge continuation, not a skip pattern); raises ERR_030.

### `validate_merged_weights()`

1. **test_validate_merged_weights_same_part_no_ok** — Rows 5–6 share merged NW cell; both have part_no="P1"; no error raised.
2. **test_validate_merged_weights_different_part_no_raises_err046** — Rows 5–6 share merged NW cell; row 5 part_no="P1", row 6 part_no="P2"; raises ProcessingError with code ERR_046.
3. **test_validate_merged_weights_header_area_merge_ignored** — Merge in header area (row ≤ header_row); not checked; no error raised.
4. **test_validate_merged_weights_no_merges_no_error** — Sheet with no merged cells; function returns None without error.
