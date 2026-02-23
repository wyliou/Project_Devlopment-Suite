# Spec: merge_tracker.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/merge_tracker.py`
- **Tests:** `tests/test_merge_tracker.py`

## 2. FRs

### FR-010: Resolve Merged Cells Before Data Extraction

**Input:** Sheet with merged cell ranges.

**Rules:**
1. Capture all merged cell ranges BEFORE unmerging. Each range records `min_row`, `max_row`, `min_col`, `max_col`, and the anchor cell value at capture time.
2. Unmerge all cells in the sheet. After `sheet.unmerge_cells()`, non-anchor cells become `None` in openpyxl.
3. **String fields** (part_no, po_no, brand, brand_type, etc.): propagate anchor cell value to all cells in the merge range — covers both vertical merges (same column, multiple rows) and horizontal merges (same row, multiple columns, e.g., brand+brand_type merged into one cell, FR-010 note on horizontal).
4. **Weight fields** (NW, QTY in packing): only first row (anchor) retains value; subsequent rows in the merge return `Decimal('0.0')`. This prevents double-counting in FR-021 aggregation.
5. **Header-area vs data-area distinction:** Only data-area merges (starting AFTER the header row) are processed for data propagation. Header-area merges are formatting only and must not influence data extraction.
6. The `MergeTracker` class is instantiated ONCE per sheet, BEFORE any extraction begins. It performs the capture-and-unmerge in `__init__`.

**Key methods:**
- `is_merge_anchor(row, col)`: True if `(row, col)` is the top-left cell of any merge range.
- `is_in_merge(row, col)`: True if `(row, col)` falls inside any merge range (including anchor).
- `get_merge_range(row, col)`: Returns the `MergeRange` that contains this cell, or `None`.
- `get_anchor_value(row, col)`: Returns the anchor cell's value for a merged cell (from pre-unmerge capture). Works for both anchor and non-anchor cells within the range.
- `is_data_area_merge(row, col, header_row)`: True if the merge range for this cell starts at a row AFTER `header_row` (i.e., `merge_range.min_row > header_row`).
- `get_string_value(row, col, header_row)`: For data-area merges, return the anchor value (string propagation). For non-data-area or non-merged cells, return the sheet cell value directly.
- `get_weight_value(row, col, header_row)`: For data-area merges: anchor row returns the captured numeric value; non-anchor rows return `Decimal('0.0')`. For non-merged cells in data area, return the sheet cell value as-is for callers to parse. Returns `Decimal('0.0')` for non-data-area merges.

## 3. Exports

| Symbol | Signature | Return | Docstring Summary |
|--------|-----------|--------|-------------------|
| `MergeTracker` | `class` | — | Captures merged cell ranges before unmerging, provides value propagation for string and weight fields per FR-010. |
| `MergeTracker.__init__` | `(self, sheet: Worksheet) -> None` | None | Capture all merge ranges (with anchor values), then unmerge all cells in the sheet. |
| `MergeTracker.is_merge_anchor` | `(self, row: int, col: int) -> bool` | bool | Return True if (row, col) is the top-left anchor of any merge range. |
| `MergeTracker.is_in_merge` | `(self, row: int, col: int) -> bool` | bool | Return True if (row, col) falls within any merge range (anchor or non-anchor). |
| `MergeTracker.get_merge_range` | `(self, row: int, col: int) -> MergeRange \| None` | `MergeRange \| None` | Return the MergeRange containing this cell, or None if not merged. |
| `MergeTracker.get_anchor_value` | `(self, row: int, col: int) -> Any` | Any | Return the anchor cell's value for a cell in a merge range (pre-unmerge). Works for both anchor and non-anchor cells. Returns None if cell is not in any merge range. |
| `MergeTracker.is_data_area_merge` | `(self, row: int, col: int, header_row: int) -> bool` | bool | Return True if the merge range for this cell starts after header_row (data-area merge). |
| `MergeTracker.get_string_value` | `(self, row: int, col: int, header_row: int) -> Any` | Any | For data-area merges: return anchor value. For all other cells: return current sheet cell value. |
| `MergeTracker.get_weight_value` | `(self, row: int, col: int, header_row: int) -> Decimal` | Decimal | For data-area merges: anchor row returns captured numeric value as Decimal; non-anchor rows return Decimal('0.0'). For non-merged data cells: return sheet cell value (raw, not parsed to Decimal). |

## 4. Imports

| Module | Symbols | Purpose |
|--------|---------|---------|
| `decimal` (stdlib) | `Decimal` | Return type for weight values |
| `typing` (stdlib) | `Any` | Anchor value type (cell values can be any type) |
| `openpyxl.worksheet.worksheet` | `Worksheet` | Sheet parameter type annotation |
| `.models` | `MergeRange` | Merge range data structure |

No call order required — the public methods are independent queries on the pre-built internal state.

## 5. Side-Effect Rules

- **Sheet mutation:** `MergeTracker.__init__` IS the one place that modifies the sheet by calling `sheet.unmerge_cells()` for each merged range. This is an intentional and documented side effect — the sheet is unmerged in-place.
- **No file I/O.**
- **No logging configuration.** Uses `logging.getLogger(__name__)` for debug-level messages only (e.g., logging captured merge ranges).
- **One instance per sheet:** Each sheet (invoice and packing) gets its own `MergeTracker` instance. batch.py creates these before passing sheets to extraction modules.

## 6. Gotchas

- **Capture BEFORE unmerge:** `MergeTracker.__init__` must iterate `sheet.merged_cells.ranges` and capture each range's `min_row`, `max_row`, `min_col`, `max_col`, and the anchor cell value (`sheet.cell(row=min_row, column=min_col).value`) BEFORE calling any `unmerge_cells()`. After unmerging, the anchor cell retains its value but non-anchor cells become `None` in openpyxl.
- **openpyxl `merged_cells.ranges` modification during iteration:** Do NOT iterate and modify `merged_cells.ranges` simultaneously. Collect all merge range objects into a list first, then unmerge.
- **`get_weight_value` return contract for non-merged cells:** For non-merged cells, this method returns the raw sheet cell value (not coerced to Decimal). The caller (extract_packing.py) is responsible for parsing it. This avoids double-parsing and keeps the method focused on merge semantics. However, when the cell IS a non-anchor merge row, the method returns exactly `Decimal('0.0')` (already a Decimal).
- **Horizontal merge propagation:** A horizontal merge (e.g., `L21:M21` spanning brand + brand_type columns) must propagate the anchor value to all cells in the same row. `get_string_value` for column M in a row where L-M are merged returns the value from column L (the anchor). This is the same mechanism as vertical merges — the anchor is `(min_row, min_col)`.
- **All row/column indices are 1-based** (openpyxl convention). MergeRange stores 1-based indices. All method parameters are 1-based.
- **`is_data_area_merge` logic:** A merge is a data-area merge if `merge_range.min_row > header_row`. If a merge starts at `header_row` or before, it is a header-area merge (formatting only). Note: a merge could SPAN the header row (start before, end after) — this case is treated as header-area (non-data) because the anchor is in the header.
- **`get_string_value` for header-area merges:** Returns the current sheet cell value directly (not the captured anchor value). For header cells, openpyxl retains the anchor value after unmerging, so this usually returns the correct header text. The distinction matters only for non-anchor header cells which become `None` after unmerging — these are not typically read during data extraction.
- **`get_anchor_value` for non-merged cells:** Returns `None` (cell is not in any merge range). Callers should use `is_in_merge()` to check first, or handle `None` returns appropriately.
- **Patterned examples in PRD (Generalization Gotcha):** FR-010 describes propagation for both vertical merges (part_no across rows) and horizontal merges (brand+brand_type). The generalization rule is: ANY merge range (regardless of orientation) propagates the anchor value for string fields via `get_string_value`. The `is_data_area_merge` check applies identically to both orientations.
- **openpyxl type stubs:** `Worksheet.merged_cells.ranges` may require `# type: ignore[attr-defined]`. The return type of `sheet.cell().value` is `Any`. Use explicit type annotations on the stored capture structures.

## 7. Ownership Exclusions

merge_tracker.py does not own any error codes.
- DO NOT validate/log ERR_046 (DIFFERENT_PARTS_SHARE_MERGED_WEIGHT) — owned by extract_packing.py. merge_tracker.py provides the data (is_in_merge, get_merge_range) that extract_packing.py uses to make the ERR_046 determination.
- DO NOT validate/log ERR_030 (EMPTY_REQUIRED_FIELD) — owned by extract_invoice.py and extract_packing.py.
- DO NOT validate/log ERR_031 (INVALID_NUMERIC) — owned by extract_invoice.py and extract_packing.py.

## 8. Test Requirements

### `MergeTracker.__init__` (construction and unmerge)
1. `test_merge_tracker_captures_ranges_before_unmerge` — create workbook with a vertical merge (e.g., A5:A7 = "PartA"); construct `MergeTracker(sheet)`; verify the tracker has captured 1 merge range with `min_row=5, max_row=7, min_col=1, max_col=1, value="PartA"`; verify the sheet is now unmerged (no ranges in `sheet.merged_cells.ranges`).
2. `test_merge_tracker_non_anchor_cell_is_none_after_unmerge` — after construction with A5:A7 merge, verify `sheet.cell(row=6, column=1).value is None` (openpyxl sets non-anchor to None after unmerge).
3. `test_merge_tracker_horizontal_merge_captured` — create workbook with horizontal merge B3:C3 = "Brand"; construct `MergeTracker(sheet)`; verify captured range has `min_col=2, max_col=3`.
4. `test_merge_tracker_no_merges` — sheet with no merge ranges; construct `MergeTracker(sheet)`; verify no exception; `is_in_merge(5, 2)` returns `False`.

### `is_merge_anchor` and `is_in_merge`
5. `test_is_merge_anchor_true_for_top_left` — vertical merge A5:A7; `is_merge_anchor(5, 1)` → `True`.
6. `test_is_merge_anchor_false_for_non_anchor` — `is_merge_anchor(6, 1)` → `False` (row 6 is inside merge but not anchor).
7. `test_is_in_merge_true_for_all_cells` — vertical merge A5:A7; `is_in_merge(5, 1)` → `True`; `is_in_merge(6, 1)` → `True`; `is_in_merge(7, 1)` → `True`.
8. `test_is_in_merge_false_outside_range` — `is_in_merge(8, 1)` → `False` (row 8 not in merge).

### `get_merge_range` and `get_anchor_value`
9. `test_get_merge_range_returns_correct_range` — vertical merge A5:A7; `get_merge_range(6, 1)` returns `MergeRange(min_row=5, max_row=7, min_col=1, max_col=1, value="PartA")`.
10. `test_get_merge_range_returns_none_outside` — `get_merge_range(8, 1)` returns `None`.
11. `test_get_anchor_value_from_non_anchor_row` — vertical merge A5:A7 = "PartA"; `get_anchor_value(6, 1)` → `"PartA"` (anchor's value even when querying non-anchor row).
12. `test_get_anchor_value_from_anchor_row` — `get_anchor_value(5, 1)` → `"PartA"`.

### `is_data_area_merge` and `get_string_value`
13. `test_is_data_area_merge_true_when_starts_after_header` — merge A10:A12 (data area), `header_row=5`; `is_data_area_merge(11, 1, header_row=5)` → `True`.
14. `test_is_data_area_merge_false_for_header_area` — merge A3:A5 (spans header), `header_row=5`; `is_data_area_merge(4, 1, header_row=5)` → `False`.
15. `test_get_string_value_data_area_returns_anchor` — data-area vertical merge A10:A12 = "PartX", `header_row=5`; `get_string_value(11, 1, header_row=5)` → `"PartX"`.
16. `test_get_string_value_non_merged_returns_cell` — non-merged cell B8 = "USD"; `get_string_value(8, 2, header_row=5)` → `"USD"`.

### `get_weight_value`
17. `test_get_weight_value_anchor_returns_value` — data-area merge A10:A12 with captured value `2.5`; `get_weight_value(10, 1, header_row=5)` → the captured value (raw, as returned from sheet).
18. `test_get_weight_value_non_anchor_returns_zero` — data-area merge A10:A12 = 2.5; `get_weight_value(11, 1, header_row=5)` → `Decimal('0.0')`.
19. `test_get_weight_value_non_anchor_returns_zero_for_third_row` — `get_weight_value(12, 1, header_row=5)` → `Decimal('0.0')`.
20. `test_get_weight_value_header_area_merge_returns_zero` — merge A3:A5 = 100 (header area), `header_row=5`; `get_weight_value(4, 1, header_row=5)` → `Decimal('0.0')`.
