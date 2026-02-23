# Spec: xls_adapter.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/xls_adapter.py`
- **Tests:** `tests/test_xls_adapter.py`

## 2. FRs

### FR-003 (partial): Convert `.xls` files to in-memory openpyxl Workbook

**Input:** Path to a `.xls` file.

**Rules:**
1. Read the `.xls` file using `xlrd.open_workbook(filepath, formatting_info=True)`. Do NOT create temp files — all conversion is in-memory. The original `.xls` file is never modified.
2. For each sheet in the xlrd workbook, create a corresponding openpyxl worksheet with the same name.
3. Transfer all cell values from xlrd to openpyxl. Preserve Python types: text → str, number → float or int (xlrd stores all numbers as float), date (xlrd `XL_CELL_DATE`) → convert using `xlrd.xldate_as_datetime(value, datemode)` → store as Python `datetime`.
4. Convert xlrd 0-based row/column indices to openpyxl 1-based indices when writing to openpyxl cells: `openpyxl_row = xlrd_row + 1`, `openpyxl_col = xlrd_col + 1`.
5. Preserve merged cell ranges: xlrd `sheet.merged_cells` provides a list of `(rlo, rhi, clo, chi)` tuples (0-based, rhi/chi exclusive). Convert to openpyxl merge range and call `openpyxl_sheet.merge_cells(start_row=rlo+1, start_column=clo+1, end_row=rhi, end_column=chi)`. Set the anchor cell value from xlrd before merging.
6. Return the constructed in-memory `openpyxl.Workbook`. The returned workbook is used identically to one opened from a `.xlsx` file — all downstream modules receive an openpyxl `Workbook` and are unaware of the source format.
7. `formatting_info=True` is required in `xlrd.open_workbook()` to access merged cell information in `.xls` files.

**Note on xlrd 2.0.2 limitation:** xlrd 2.0.2 only supports `.xls` format (not `.xlsx`). It does NOT support `formatting_info=True` for number format strings in the same way as older versions. Number formats are not required to be preserved (downstream uses `data_only=True` semantics — openpyxl will read the literal cell values, not formats). The number_format of converted cells will be `"General"` — `detect_cell_precision` returns 5 for General format, which is the correct fallback per FR-015.

## 3. Exports

| Symbol | Signature | Return | Docstring Summary |
|--------|-----------|--------|-------------------|
| `convert_xls_to_xlsx(filepath: Path) -> Workbook` | Read `.xls` via xlrd, create in-memory openpyxl Workbook with all sheets, cells, and merge ranges preserved. Original file is never modified. | `openpyxl.Workbook` | Convert a legacy .xls file to an in-memory openpyxl Workbook preserving all sheets, cell values, and merge ranges. |

## 4. Imports

| Module | Symbols | Purpose |
|--------|---------|---------|
| `pathlib` (stdlib) | `Path` | Function parameter type |
| `datetime` (stdlib) | `datetime` | xlrd date conversion |
| `xlrd` | `open_workbook`, `xldate_as_datetime`, `XL_CELL_EMPTY`, `XL_CELL_TEXT`, `XL_CELL_NUMBER`, `XL_CELL_DATE`, `XL_CELL_BOOLEAN`, `XL_CELL_ERROR` | Read .xls files |
| `openpyxl` | `Workbook` | Create in-memory workbook |

No internal autoconvert imports — xls_adapter.py depends only on external libraries and stdlib. It does not import from models, errors, or utils.

No call order required — single public function.

## 5. Side-Effect Rules

- **No file writes.** The returned `Workbook` is in-memory only. Never call `workbook.save()` within this module.
- **No temp files.** All conversion happens in RAM.
- **Source file is read-only.** Never modify the xlrd `Book` object or the original `.xls` file.
- **No logging configuration.** Uses `logging.getLogger(__name__)` for debug output only (e.g., number of sheets converted, merge ranges processed).

## 6. Gotchas

- **xlrd vs openpyxl index bases:** xlrd uses 0-based row/col; openpyxl uses 1-based. Conversion: `openpyxl_row = xlrd_row + 1`, `openpyxl_col = xlrd_col + 1`. The `merged_cells` tuples are `(rlo, rhi, clo, chi)` where `rlo` and `clo` are 0-based inclusive, `rhi` and `chi` are 0-based exclusive. To openpyxl: `start_row=rlo+1, end_row=rhi, start_column=clo+1, end_column=chi`. Verify this conversion carefully — off-by-one errors here cause phantom shifted merges.
- **xlrd `XL_CELL_DATE` conversion:** `xlrd.xldate_as_datetime(cell.value, book.datemode)` returns a `datetime` object. Store it in the openpyxl cell as-is. The `datemode` attribute must come from the xlrd `Book` object (`book.datemode`), not hardcoded.
- **xlrd `XL_CELL_BOOLEAN`:** xlrd returns 0 or 1 for boolean cells. Store as Python `bool` (`True`/`False`) in openpyxl.
- **xlrd `XL_CELL_ERROR`:** Error cells (e.g., `#DIV/0!`) should be stored as `None` in openpyxl (treat as empty, same as `data_only=True` behavior for error cells).
- **xlrd `XL_CELL_EMPTY`:** Store as `None`.
- **Number format not preserved:** xlrd 2.0.2 does not reliably expose number format strings. All converted cells have `number_format="General"` in the resulting openpyxl workbook. This is acceptable because `detect_cell_precision("General")` returns 5, and integer values from `.xls` (e.g., `91600.0` stored as float) are handled by precision rounding. Implementors must NOT attempt to read `cell.xf_index` or format strings — this is unreliable in xlrd 2.0.2 without `formatting_info=True` in full format mode.
- **`.xls` merged cells — `formatting_info=True` required:** Without `formatting_info=True` in `xlrd.open_workbook()`, `sheet.merged_cells` returns an empty list in xlrd 2.0.2. Always pass `formatting_info=True`.
- **Anchor cell value before merging:** When merging cells in the openpyxl sheet, write the anchor cell value BEFORE calling `merge_cells()`. openpyxl's `merge_cells()` clears non-anchor cells but preserves the anchor.
- **xlrd `XL_CELL_NUMBER` float vs int:** xlrd returns all numeric values as Python `float` (e.g., `91600.0` for what was an int in Excel). This is expected behavior. Downstream `safe_decimal` and `round_half_up` handle float-to-Decimal conversion. Do NOT attempt to convert floats to ints in this adapter.
- **xlrd sheet name encoding:** xlrd returns sheet names as Python `str` (Unicode). No conversion needed.
- **`formatting_info=True` and xlrd 2.0.2:** The `formatting_info` parameter is supported but has known limitations in xlrd 2.0.2 for some `.xls` variants (BIFF5 vs BIFF8). If `open_workbook` raises an exception with `formatting_info=True`, callers (batch.py) handle it as ERR_011 (FILE_CORRUPTED). Do NOT catch exceptions inside `convert_xls_to_xlsx` — let them propagate so batch.py owns the ERR_011 determination.

## 7. Ownership Exclusions

xls_adapter.py does not own any error codes. Exceptions propagate to batch.py which owns:
- DO NOT raise/log ERR_010 (FILE_LOCKED) — owned by batch.py.
- DO NOT raise/log ERR_011 (FILE_CORRUPTED) — owned by batch.py. If xlrd raises an exception, let it propagate.
- DO NOT raise/log ERR_001 through ERR_005 — owned by config.py.

## 8. Test Requirements

### `convert_xls_to_xlsx` — Happy Path
1. `test_convert_xls_basic_cell_values` — create a simple in-memory `.xls` file (via xlwt or use the corpus `茂綸股份有限公司.xls`); call `convert_xls_to_xlsx(path)`; verify the returned object is an `openpyxl.Workbook`; verify sheet names are preserved; verify a known cell value (e.g., sheet name "Invoice" or a specific text cell) is present in the converted workbook.
2. `test_convert_xls_index_conversion_1based` — verify that xlrd row 0, col 0 maps to openpyxl row 1, col 1; check a cell at `workbook.active.cell(row=1, column=1).value` equals the xlrd value at `sheet.cell_value(0, 0)`.
3. `test_convert_xls_multiple_sheets_preserved` — `.xls` with 2+ sheets; verify the converted `Workbook` has the same number of sheets with identical names.
4. `test_convert_xls_merge_ranges_preserved` — `.xls` with a merged cell range (e.g., A5:A7); verify the converted openpyxl workbook has a corresponding merge range (check `workbook.active.merged_cells.ranges`); verify the anchor cell retains its value.
5. `test_convert_xls_numeric_values_as_float` — `.xls` cell with integer value `91600`; verify the converted openpyxl cell value is `91600.0` (float, not int — xlrd's standard behavior); verify `float` type.
6. `test_convert_xls_text_cells` — `.xls` with text cells containing Chinese characters (e.g., part numbers, brand names); verify the converted openpyxl cells have identical `str` values.
7. `test_convert_xls_empty_cells_are_none` — `.xls` with intentionally empty cells (XL_CELL_EMPTY); verify converted openpyxl cells have `value is None`.
