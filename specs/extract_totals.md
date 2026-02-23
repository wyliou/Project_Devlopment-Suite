# Spec: extract_totals.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/extract_totals.py`
- **Tests:** `tests/test_extract_totals.py`
- **FRs:** FR-014, FR-015, FR-016, FR-017

---

## 2. Functional Requirements

### FR-014 — Total Row Detection (Two-Strategy)

**Strategy 1 (Keyword):** Search rows `last_data_row + 1` through `last_data_row + 15`, columns A–J, for "total/合计/总计/小计" (case-insensitive via `is_stop_keyword()`). First row with a match is the total row.

**Strategy 2 (Implicit):** If Strategy 1 returns no result, search the same range for rows satisfying ALL of:
- Mapped `part_no` column is empty.
- Mapped NW column contains a numeric value > 0.
- Mapped GW column contains a numeric value > 0.
- Row is NOT a merged cell continuation (use `MergeTracker.is_in_merge(row, part_no_col)` to exclude continuation rows).

**Sequencing constraint:** Strategy 1 returns `None` (not found) — does NOT raise ERR_032. Strategy 2 runs only when Strategy 1 returns None. ERR_032 fires after BOTH strategies fail.

Use actual mapped column indices from `ColumnMapping.field_map`, not hardcoded positions.

SUM formula detection not needed — `data_only=True` resolves formulas to values.

**Error:** ERR_032 (TOTAL_ROW_NOT_FOUND) after both strategies fail.

### FR-015 — Total NW Extraction

Read NW value from total row (mapped NW column index).

**Unit suffix stripping:** strip KG, KGS, G, LB, LBS via `strip_unit_suffix()` before parsing.

**Cell format precision detection:**
1. Read `cell.number_format` via `detect_cell_precision(cell)`.
2. For `General` or empty format: round to 5 decimals first to clean floating-point artifacts, then normalize trailing zeros (remove trailing zeros after decimal point, minimum 2 decimals).
3. For explicit format (e.g., `0.00`, `#,##0.00`, `0.00000_`): extract decimal place count from format string.
4. Strip embedded unit BEFORE counting decimal places when format is General and value is a string.

Store result as `Decimal` with detected precision. Store precision in `PackingTotals.total_nw_precision`.

**Precision bounds:** minimum 2, maximum 5 decimals.

**Error:** ERR_033 (INVALID_TOTAL_NW) if cell value is non-numeric or missing.

### FR-016 — Total GW Extraction

Extract GW from total row (mapped GW column index). Same unit stripping and precision rules as FR-015.

**Packaging weight addition check:**
1. Read GW cell at total_row.
2. Check GW column at `total_row + 1`: if numeric, continue.
3. Check GW column at `total_row + 2`: if both `+1` and `+2` are numeric, use `+2` as final `total_gw` (handles pallet weight addition: row+1 = pallet weight, row+2 = final total).
4. If only `+1` is numeric (but not `+2`), use total_row value.
5. Precision derived from the final selected cell's number_format.

**Error:** ERR_034 (INVALID_TOTAL_GW) if cell value is non-numeric or missing.

### FR-017 — Total Packets Multi-Priority Search

**Column search range:** columns A to (NW column index + 2), minimum 11 columns.

**Priority 1 (件数/件數 label):**
- Search rows `total_row + 1` through `total_row + 3`.
- Look for "件数" or "件數" label in any cell within the column range.
- Extract value from: adjacent right (up to +3 columns from label) OR embedded in label cell itself.
- Adjacent cell values must be stripped of unit suffixes before numeric parsing.

**Priority 2 (PLT.G indicator):**
- Search rows `total_row - 1` and `total_row - 2`.
- Two formats:
  - Number-before-PLT: cell contains a number followed by "PLT" — extract the number.
  - PLT-before-number: cell contains "PLT" — check the cell immediately to the right for the number.

**Priority 3 (Below-total patterns, searched in order):**
Search rows `total_row + 1` through `total_row + 3`:
1. **Total-with-breakdown pattern** — e.g., `"348（256胶框+92纸箱）"` → extract leading number before `（` or `(`. Verbatim pattern example: leading numeric before CJK parenthesis.
2. **Unit-suffix patterns** — e.g., `"7托"`, `"30箱"`, `"55 CTNS"` → extract numeric before 托/箱/件/CTNS.
3. **Embedded Chinese pattern** — e.g., `"共7托"` → extract numeric after 共 and before 托.
4. **Pallet range pattern** — e.g., `"PLT#1(1~34)"` → extract trailing number after `~` (this is the highest pallet index, representing pallet count).

**Pallet vs box priority:** When both pallet and box counts appear (e.g., `"共7托（172件）"`), extract the pallet count (7), not the box count (172).

**Validation:** Result must be a positive integer in range **1–1000**. Values outside this range → treated as not found (continue to next priority).

**Field classification:** Optional. ATT_002 fires only after ALL 3 priorities fail.

**Detection-Fallback Map constraint:** ATT_002 fires only after all 3 priorities fail. No hard-fail until all attempted.

**Error:** ATT_002 (MISSING_TOTAL_PACKETS) — warning (not failure); returned as ProcessingError with WarningCode.ATT_002 in `extract_totals()` return value.

---

## 3. Exports

```python
def detect_total_row(
    sheet: Worksheet,
    last_data_row: int,
    column_map: ColumnMapping,
    merge_tracker: MergeTracker,
) -> int:
    """Detect total row using two-strategy approach.

    Args:
        sheet: Packing worksheet (already unmerged).
        last_data_row: 1-based row number of last extracted packing item.
        column_map: Column index mapping including nw, gw, part_no indices.
        merge_tracker: For excluding merged continuation rows in Strategy 2.

    Returns:
        1-based row number of the detected total row.

    Raises:
        ProcessingError: ERR_032 if both strategies fail to find a total row.
    """

def extract_totals(
    sheet: Worksheet,
    total_row: int,
    column_map: ColumnMapping,
) -> PackingTotals:
    """Extract total_nw (FR-015), total_gw (FR-016), total_packets (FR-017).

    Args:
        sheet: Packing worksheet (already unmerged).
        total_row: 1-based row number of the total row from detect_total_row().
        column_map: Column index mapping.

    Returns:
        PackingTotals with total_nw, total_nw_precision, total_gw, total_gw_precision,
        total_packets (None if not found). ATT_002 warning is logged via logger if
        total_packets not found; caller (batch.py) may also collect it as a warning
        via returned PackingTotals with total_packets=None.

    Raises:
        ProcessingError: ERR_033 if total_nw is non-numeric or missing;
                         ERR_034 if total_gw is non-numeric or missing.
    """
```

Note: ATT_002 is issued as a warning log inside `extract_totals()`. The `PackingTotals.total_packets` field being `None` is the signal to batch.py that the warning should be recorded in the file's warning list.

---

## 4. Imports

```python
from .models import PackingTotals, ColumnMapping
from .errors import ProcessingError, ErrorCode, WarningCode
from .merge_tracker import MergeTracker
from .utils import (
    strip_unit_suffix,
    safe_decimal,
    detect_cell_precision,
    is_stop_keyword,
)
from openpyxl.worksheet.worksheet import Worksheet
import re
import logging
```

Functions used:
- `strip_unit_suffix(value)` — called on nw and gw raw cell values before parsing.
- `safe_decimal(value, decimals)` — called with detected precision for total_nw and total_gw.
- `detect_cell_precision(cell)` — called on total_nw and total_gw cells; also called on final GW cell selected in packaging weight check.
- `is_stop_keyword(value)` — called in Strategy 1 keyword search.
- `MergeTracker.is_in_merge(row, col)` — used in Strategy 2 to exclude continuation rows.

---

## 5. Side-Effect Rules

- **No file I/O.** Receives `Worksheet` and `int`.
- **No config loading.** All configuration arrives via `ColumnMapping`.
- **Logging:** Use `logging.getLogger(__name__)`. Log ATT_002 warning when total_packets not found. Log INFO for detected total row, total_nw, total_gw, total_packets per FR-031 format.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_030 (EMPTY_REQUIRED_FIELD) — per-item field validation owned by extract_packing.py.
- DO NOT validate/log ERR_031 (INVALID_NUMERIC) — per-item field validation owned by extract_packing.py.
- DO NOT validate/log ERR_040 through ERR_048 — owned by weight_alloc.py.
- DO NOT validate/log ERR_046 (DIFFERENT_PARTS_SHARE_MERGED_WEIGHT) — owned by extract_packing.py.

---

## 7. Gotchas

1. **Strategy 1 returns None — does NOT raise ERR_032.** Only after Strategy 2 also fails does ERR_032 fire. Do not add a guard after Strategy 1 that raises before attempting Strategy 2.
2. **Column search range for FR-017 is A to max(NW_col + 2, 11)** — minimum 11 columns. Compute: `max_col = max(column_map.field_map['nw'] + 2, 11)`.
3. **Packaging weight addition rule (FR-016):** Only use `+2` row when BOTH `+1` AND `+2` are numeric. If only `+1` is numeric, stick with the total_row GW value.
4. **Precision for GW when `+2` row selected:** read precision from the `+2` row cell's number_format, not from the total_row cell.
5. **total_nw precision bounds:** minimum 2, maximum 5 decimals. Even if cell format shows 1 decimal (e.g., "212.5"), store with precision 2.
6. **General format precision:** `detect_cell_precision()` returns 5 for General format — caller must then normalize trailing zeros (strip to minimum 2). This normalization happens in extract_totals, not in utils.
7. **Patterned examples from PRD (generalization rule):** The PRD lists specific example strings for Priority 3 patterns:
   - `"348（256胶框+92纸箱）"` → extracts 348 (generalize: extract leading number before `（` or `(`).
   - `"7托"`, `"30箱"`, `"55 CTNS"` → each of 托, 箱, 件, CTNS is a distinct suffix (each must have its own test case).
   - `"共7托"` → generalize: pattern `共(\d+)托`.
   - `"PLT#1(1~34)"` → generalize: pattern `PLT#\d+\(\d+~(\d+)\)`, extract trailing number.
8. **ATT_002 is a warning, not an error.** Do not raise `ProcessingError` with an `ErrorCode` for ATT_002. Use `WarningCode.ATT_002`. The warning is logged by this module and also signaled to batch.py via `PackingTotals.total_packets == None`.
9. **Consistency with extract_packing.py on total_nw/total_gw extraction rules:** Both this module and the cross-validation expectations use `strip_unit_suffix` then `safe_decimal(value, detected_precision)`. The precision detection is identical to what extract_packing uses for per-item qty — but for totals, cell format precision is the authoritative source.
10. **`data_only=True` resolves SUM formulas** — no need to detect SUM formulas. The resolved numeric value is read directly.

---

## 8. Verbatim Outputs

Console log format (FR-031):
```
[INFO] Packing total row at row {N}, NW= {val}, GW= {val}, Packets= {val}
```

---

## 9. Test Requirements

### `detect_total_row()`

1. **test_detect_total_row_strategy1_keyword_total** — Row `last_data_row + 3` has "TOTAL" in column A; detected as total row; Strategy 2 not needed.
2. **test_detect_total_row_strategy1_keyword_chinese_合计** — Row has "合计" in column F; detected correctly.
3. **test_detect_total_row_strategy2_implicit_when_strategy1_fails** — No keyword rows; row `last_data_row + 2` has empty part_no, NW=15.5, GW=18.0; detected via Strategy 2.
4. **test_detect_total_row_strategy2_excludes_merge_continuation** — Row with empty part_no due to vertical merge (MergeTracker shows it is in merge); NOT detected as total row; Strategy 2 continues search.
5. **test_detect_total_row_both_strategies_fail_raises_err032** — No keyword rows and no implicit-pattern rows in range; raises ProcessingError with code ERR_032.

### `extract_totals()`

#### FR-015 — total_nw
1. **test_extract_totals_nw_explicit_format_precision** — NW cell format "0.00000_"; value 15.5; total_nw = Decimal('15.50000'), total_nw_precision = 5.
2. **test_extract_totals_nw_general_format_trailing_zero_normalization** — NW cell format "General"; value 15.5000000000001 (float artifact); total_nw = Decimal('15.50'), total_nw_precision = 2 (General normalized).
3. **test_extract_totals_nw_with_unit_suffix** — NW cell value "15.5 KG"; unit stripped; total_nw = Decimal('15.50'), precision = 2.
4. **test_extract_totals_nw_invalid_raises_err033** — NW cell is empty; raises ProcessingError ERR_033.

#### FR-016 — total_gw
5. **test_extract_totals_gw_packaging_weight_addition** — total_row GW = 18.0; total_row+1 GW = 2.5 (pallet); total_row+2 GW = 20.5 (final); total_gw = Decimal('20.50'), precision from +2 cell.
6. **test_extract_totals_gw_no_additional_rows** — total_row+1 GW is empty; use total_row GW value directly.
7. **test_extract_totals_gw_invalid_raises_err034** — GW cell is empty or non-numeric; raises ProcessingError ERR_034.

#### FR-017 — total_packets
8. **test_extract_totals_packets_priority1_件数_label** — Row total_row+1 has "件数" label; adjacent right cell has "55 件"; total_packets = 55.
9. **test_extract_totals_packets_priority2_plt_g_number_before** — Row total_row-1 has cell "7PLT.G"; total_packets = 7.
10. **test_extract_totals_packets_priority3a_total_with_breakdown** — Row total_row+1 has "348（256胶框+92纸箱）"; total_packets = 348.
11. **test_extract_totals_packets_priority3b_unit_suffix_托** — Row total_row+1 has "7托"; total_packets = 7.
12. **test_extract_totals_packets_priority3b_unit_suffix_ctns** — Row total_row+1 has "55 CTNS"; total_packets = 55.
13. **test_extract_totals_packets_priority3c_embedded_chinese_共n托** — Row total_row+2 has "共7托"; total_packets = 7.
14. **test_extract_totals_packets_priority3d_pallet_range** — Row total_row+1 has "PLT#1(1~34)"; total_packets = 34.
15. **test_extract_totals_packets_pallet_vs_box_priority** — Row has "共7托（172件）"; extracts pallet count 7, not box count 172.
16. **test_extract_totals_packets_not_found_att002_warning** — No priority pattern matches; total_packets = None; ATT_002 warning logged.
17. **test_extract_totals_packets_out_of_range_treated_as_not_found** — Pattern matches value 1500 (> 1000); treated as not found; continues to next priority.
