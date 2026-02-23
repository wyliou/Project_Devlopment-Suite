# Spec: column_map.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/column_map.py`
- **Tests:** `tests/test_column_map.py`
- **FRs:** FR-007, FR-008, FR-009

---

## 2. Functional Requirements

### FR-007 — Header Row Detection

Scan rows **7–30**, first **13** columns. For each row, count non-empty cells after filtering (exclude cells with "Unnamed:" prefix). Apply thresholds: **Invoice ≥ 7** non-empty cells, **Packing ≥ 4** non-empty cells.

**Three-tier priority classification** (apply only to rows meeting the threshold):

- **Tier 0 (highest):** Row contains at least one HEADER_KEYWORDS match AND fewer than 2 numeric/data-like cells.
- **Tier 1:** All other qualifying rows (no keywords, not metadata/data-like).
- **Tier 2 (lowest):** Metadata markers present (Tel:, Fax:, Cust ID:, Contact:, Address:) OR data-like rows (3+ cells with pure numbers, decimals, or alphanumeric codes).

Select the row with the lowest tier number; on tie, select the **earliest row number**.

Error: **ERR_014** (HEADER_ROW_NOT_FOUND) if no row meets the threshold.

### FR-008 — Column Mapping via Regex

Normalize headers before matching: collapse newlines, tabs, multiple spaces → single space; strip leading/trailing whitespace. Match each header cell against each field's regex synonym list (case-insensitive). First match per field wins.

**Invoice fields (14 total):**
- **Required (10):** part_no, po_no, qty, price, amount, currency, coo, brand, brand_type, model
- **Optional (4):** cod, weight, inv_no, serial

**Packing fields (6 total):**
- **Required (4):** part_no, qty, nw, gw
- **Optional (2):** po_no, pack

Missing any required field → **ERR_020** (REQUIRED_COLUMN_MISSING); list ALL missing fields in a single error (collect-then-report).

**Two-row merged header fallback (sub-header scan):**
1. After primary header row scan, if any required fields remain unmapped, scan `header_row+1` (all columns).
2. Guard: verify sub-header row is not data-like (fewer than 3 numeric/code cells) before advancing.
3. If ≥1 field matched and row is not data-like, advance `effective_header_row` to `header_row+1`.
4. Data extraction begins at `effective_header_row + 1`.

**Currency data-row fallback (invoice only):**
1. After header scan, if currency column absent from field_map:
2. Scan rows `header_row+1` through `header_row+4`, all columns.
3. If a cell matches a currency pattern (e.g., "USD", "CNY") AND its column is already mapped to price or amount, shift that field's mapping to `col+1` (actual numeric value is one column right).
4. Record the currency column index in field_map. The fallback must shift ALL affected numeric fields, not just the first match (handles vendors with two currency columns).

### FR-009 — Invoice Number Header-Area Fallback

Used when no `inv_no` column detected in data table. Scan invoice sheet rows **1–15** using patterns from `config.inv_no_patterns` (capture-group) and `config.inv_no_label_patterns` (label+adjacent).

**Adjacent cell search for label patterns:**
- Right: up to +3 columns from label cell.
- Below: row+1 AND row+2 (to handle date at row+1 with actual inv_no at row+2).

**False positive filtering:** exclude matches against `config.inv_no_exclude_patterns` (dates, label text captured as values).

**Cleaning:** remove "INV#" and "NO." prefixes from extracted value.

Returns `str | None`. Returns `None` (does **not** raise ERR_021) — ERR_021 is raised by batch.py only after both column and header extraction both fail.

---

## 3. Exports

Must match build-plan.md exactly:

```python
def detect_header_row(sheet: Worksheet, sheet_type: str, config: AppConfig) -> int:
    """Detect the header row by scanning rows 7-30 with three-tier priority.

    Args:
        sheet: Worksheet to scan (already unmerged).
        sheet_type: "invoice" or "packing".
        config: Application configuration.

    Returns:
        1-based row number of the detected header row.

    Raises:
        ProcessingError: ERR_014 if no row meets the cell-count threshold.
    """

def map_columns(sheet: Worksheet, header_row: int, sheet_type: str, config: AppConfig) -> ColumnMapping:
    """Map columns via regex with sub-header and currency fallback.

    Args:
        sheet: Worksheet (already unmerged).
        header_row: 1-based header row from detect_header_row().
        sheet_type: "invoice" or "packing".
        config: Application configuration.

    Returns:
        ColumnMapping with field_map, header_row, effective_header_row.

    Raises:
        ProcessingError: ERR_020 listing all missing required column names.
    """

def extract_inv_no_from_header(sheet: Worksheet, config: AppConfig) -> str | None:
    """Scan invoice sheet rows 1-15 for invoice number via capture/label patterns.

    Args:
        sheet: Invoice worksheet (already unmerged).
        config: Application configuration with inv_no patterns.

    Returns:
        Cleaned invoice number string, or None if not found.
        Does NOT raise ERR_021 — caller (batch.py) decides if error applies.
    """
```

---

## 4. Imports

```python
from .models import AppConfig, ColumnMapping, FieldPattern
from .errors import ProcessingError, ErrorCode
from .utils import normalize_header, HEADER_KEYWORDS
from openpyxl.worksheet.worksheet import Worksheet
import re
import logging
```

Functions used:
- `normalize_header(value)` — called on every header cell before regex matching.
- `HEADER_KEYWORDS` — used in Tier 0 classification.
- `ProcessingError(code, message, context)` — raised for ERR_014 and ERR_020.
- `ErrorCode.ERR_014`, `ErrorCode.ERR_020`, `ErrorCode.ERR_021` — **ERR_021 is NOT raised here; only batch.py raises it after this returns None.**

---

## 5. Side-Effect Rules

- **No file I/O.** Receives `Worksheet` object as parameter; does not open workbooks.
- **No config loading.** Receives `AppConfig` as parameter; does not read files.
- **Logging:** Use `logging.getLogger(__name__)`. Debug-log each regex match attempt, tier classification, and sub-header scan result.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_002 (INVALID_REGEX) — owned by config.py. Patterns arrive pre-compiled.
- DO NOT validate/log ERR_012 (INVOICE_SHEET_NOT_FOUND) — owned by sheet_detect.py.
- DO NOT validate/log ERR_013 (PACKING_SHEET_NOT_FOUND) — owned by sheet_detect.py.
- DO NOT validate/log ERR_021 (INVOICE_NUMBER_NOT_FOUND) — owned by batch.py (orchestration). `extract_inv_no_from_header()` returns `None`; batch.py decides whether to raise ERR_021.

---

## 7. Gotchas

1. **Scan range is rows 7–30, columns 1–13** (1-based openpyxl indexing). The upper column bound of 13 prevents false positives from phantom 256-column sheets (e.g., `上海健三電子有限公司.xlsx`).
2. **Tier classification applies only after threshold is met.** A row with 1 keyword but only 2 non-empty cells (below invoice threshold of 7) is not classified — it's simply skipped.
3. **Earliest row tie-breaking** applies within the same tier, not across tiers. Tier 0 always beats Tier 1 even if Tier 1 is earlier.
4. **Sub-header guard is mandatory.** Without the data-like check, a numeric data row immediately below the header would be incorrectly advanced as `effective_header_row`, corrupting data extraction start position.
5. **Currency fallback shifts ALL affected fields.** If a vendor embeds currency in both the price column and the amount column, both columns shift +1. Missing the second shift causes price/amount to be extracted from the currency column.
6. **Header normalization before matching:** `"N.W.\n(KGS)"` → `"N.W. (KGS)"` via `normalize_header()`. Regex patterns in config expect the normalized form.
7. **`effective_header_row` vs `header_row`:** `ColumnMapping.header_row` = detected row; `ColumnMapping.effective_header_row` = last row used for column mapping (may be header_row or header_row+1). Data extraction ALWAYS starts at `effective_header_row + 1`.
8. **`extract_inv_no_from_header` must check row+1 AND row+2** below a label cell — some vendors place a date at row+1 and the actual invoice number at row+2.
9. **ERR_020 collect-then-report pattern:** collect all missing required fields, then raise a single ProcessingError listing all of them. Do not stop at the first missing field.
10. **Packing `gw` is required in packing_columns** (for total row detection column index), even though per-item GW is never extracted. Map it but do not use it for per-item extraction — this is by design (see build-plan.md Ambiguity #5).

---

## 8. Verbatim Outputs

Console log format (FR-031):
- `[INFO] Inv_No extracted ({method}): {value} at '{cell}'` — method is "column" or "header_area"

---

## 9. Test Requirements

### `detect_header_row()`

1. **test_detect_header_row_invoice_tier0_wins** — Row 10 has 8 cells including "qty", "part no", "price" (Tier 0). Row 8 has 7 cells with no keywords (Tier 1). Row 10 selected despite being later.
2. **test_detect_header_row_tie_earliest_row** — Two rows both qualify as Tier 0 with same keyword count; earlier row (row 9) is selected over row 11.
3. **test_detect_header_row_metadata_row_demoted** — Row 12 has 8 cells including "Tel:" (Tier 2). Row 14 has 7 cells with keywords (Tier 0). Row 14 wins.
4. **test_detect_header_row_packing_threshold_4** — Packing sheet row with exactly 4 non-empty cells qualifies; invoice threshold of 7 would reject it.
5. **test_detect_header_row_no_qualifying_row_raises_err014** — All rows 7–30 have ≤3 non-empty cells; raises ProcessingError with code ERR_014.
6. **test_detect_header_row_unnamed_prefix_excluded** — Cells with "Unnamed:0", "Unnamed:1" prefix not counted toward density.
7. **test_detect_header_row_data_like_row_is_tier2** — Row with 5+ pure numeric cells is Tier 2 even with many non-empty cells.
8. **test_detect_header_row_scan_range_7_to_30** — Header in row 6 is not found (below scan start); header in row 31 is not found (above scan end).

### `map_columns()`

1. **test_map_columns_all_required_invoice_found** — 10 required invoice columns present; ColumnMapping field_map contains all 10 with correct 1-based column indices.
2. **test_map_columns_missing_required_raises_err020_with_all_names** — currency and coo columns absent; single ERR_020 error lists both field names.
3. **test_map_columns_sub_header_fallback_advances_effective_row** — Primary header has "WEIGHT(KGS)" spanning two rows; sub-header has "N.W.(KGS)" and "G.M.(KGS)"; effective_header_row advanced to header_row+1.
4. **test_map_columns_sub_header_guard_rejected_if_data_like** — Row header_row+1 has 4 numeric cells; sub-header scan rejected; effective_header_row stays at header_row.
5. **test_map_columns_currency_data_row_fallback_shifts_price** — No currency column in header; "USD" found at column 5 in data row; price field was at column 5, shifts to column 6.
6. **test_map_columns_currency_fallback_shifts_both_price_and_amount** — Two currency columns embedded; both price and amount shift +1.
7. **test_map_columns_case_insensitive_regex_match** — Header "N.W. (KGS)" matched by pattern `n\.w\.` (case-insensitive).
8. **test_map_columns_packing_optional_fields_absent_no_error** — po_no and pack absent from packing sheet; no ERR_020 raised; field_map lacks those keys.

### `extract_inv_no_from_header()`

1. **test_extract_inv_no_capture_group_pattern** — Cell contains "INVOICE NO.: INV2025-001"; capture pattern extracts "INV2025-001" with "INV" prefix stripped → "2025-001".
2. **test_extract_inv_no_label_right_adjacent** — Cell "Invoice No." at row 3, col 2; value "INV-001" at col 4 (within +3 range); returns "INV-001".
3. **test_extract_inv_no_label_two_rows_below** — Cell "Invoice No." at row 3, col 1; row+1 has a date (filtered by exclude pattern); row+2 has "INV-2025-009"; returns "INV-2025-009".
4. **test_extract_inv_no_not_found_returns_none** — No inv_no pattern matches rows 1–15; returns None (no exception raised).
5. **test_extract_inv_no_exclude_pattern_filters_date** — Captured value "2025-01-15" matches exclude date pattern; filtered; None returned.
