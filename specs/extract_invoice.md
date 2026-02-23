# Spec: extract_invoice.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/extract_invoice.py`
- **Tests:** `tests/test_extract_invoice.py`
- **FRs:** FR-011

---

## 2. Functional Requirements

### FR-011 — Per-Item Extraction from Invoice Sheet

Extract **13 fields** per item from the invoice sheet. `weight` is NOT extracted (calculated by weight allocation in FR-025).

**Fields extracted:**

| Field | Type | Required | Precision |
|-------|------|----------|-----------|
| part_no | str | yes | strip whitespace |
| po_no | str | yes | strip whitespace |
| qty | Decimal | yes | cell display precision |
| price | Decimal | yes | 5 decimals |
| amount | Decimal | yes | 2 decimals |
| currency | str | yes | strip whitespace |
| coo | str | yes | strip whitespace (COO/COD fallback applies) |
| brand | str | yes | strip whitespace |
| brand_type | str | yes | strip whitespace |
| model | str | yes | strip whitespace (field name `model_no` in pydantic — avoid pydantic conflict) |
| cod | str | optional | strip whitespace |
| inv_no | str | optional column | strip, clean prefix |
| serial | str | optional column | strip whitespace |

**Numeric precision (ROUND_HALF_UP with epsilon trick):**
- `qty` = cell display precision (via `detect_cell_precision(cell)`)
- `price` = 5 decimals fixed
- `amount` = 2 decimals fixed

**Unit suffix stripping:** strip KG, KGS, G, LB, LBS, PCS, EA, 件, 个 from numeric values before parsing via `strip_unit_suffix()`.

**String field handling:**
- Strip leading/trailing whitespace.
- Propagate merged cell values via `MergeTracker.get_string_value()`.

**Invoice number cleaning (if inv_no column mapped):**
- Remove "INV#" prefix (case-insensitive).
- Remove "NO." prefix (case-insensitive).

**COO/COD fallback (per row):**
- If COO column value is empty (after whitespace strip) AND `cod` field has a value, use `cod` value as COO.
- ERR_030 for COO fires ONLY after COD fallback is attempted.

**Header continuation filtering:**
- Skip rows where `part_no` cell value contains "part no" (case-insensitive). These are sub-header rows that repeat the column label.

**Currency column shift handling:**
- When column_map currency fallback shifted price/amount columns, extract from the shifted indices as stored in `ColumnMapping.field_map`. No special logic needed here — use field_map as given.

**Leading blank rows:**
- Skip blank rows between `effective_header_row + 1` and the first data row before applying stop conditions.
- A "blank" row for this purpose: part_no empty AND qty cell empty.

**Horizontal merge propagation (brand + brand_type):**
- Some vendors merge brand and brand_type columns horizontally per row (e.g., `L21:M21`). After unmerging, the non-anchor column is None. Use `MergeTracker.get_string_value()` for both brand and brand_type columns.

**Stop conditions — processing order per row:**
1. Check if blank → skip and continue (do NOT stop).
2. Check stop conditions → stop if matched.
3. Process data row.

**Stop conditions (ANY condition stops iteration):**
1. `part_no` is empty AND `qty = 0` (after first data row has been found).
2. `part_no` contains "total" (case-insensitive).
3. `part_no` contains any value from `FOOTER_KEYWORDS` (报关行, 有限公司).
4. Any cell in columns A–J contains "total", "合计", "总计", "小计" (case-insensitive).

**Errors:**
- **ERR_030** (EMPTY_REQUIRED_FIELD): Required field empty after extraction and fallbacks, with row and field name in context.
- **ERR_031** (INVALID_NUMERIC): Non-numeric value in numeric field after unit suffix stripping, with row and column in context.

---

## 3. Exports

```python
def extract_invoice_items(
    sheet: Worksheet,
    column_map: ColumnMapping,
    merge_tracker: MergeTracker,
    inv_no: str | None,
) -> list[InvoiceItem]:
    """Extract 13 per-item fields from the invoice sheet.

    Args:
        sheet: Invoice worksheet (already unmerged by MergeTracker).
        column_map: Column index mapping with header_row and effective_header_row.
        merge_tracker: Pre-initialized MergeTracker for merged cell propagation.
        inv_no: Invoice number from batch orchestration (column or header fallback);
                used to populate inv_no field when inv_no column is absent from field_map.

    Returns:
        List of InvoiceItem records in extraction order.

    Raises:
        ProcessingError: ERR_030 for empty required field; ERR_031 for invalid numeric.
    """
```

---

## 4. Imports

```python
from .models import InvoiceItem, ColumnMapping
from .errors import ProcessingError, ErrorCode
from .merge_tracker import MergeTracker
from .utils import (
    strip_unit_suffix,
    safe_decimal,
    detect_cell_precision,
    is_stop_keyword,
    FOOTER_KEYWORDS,
)
from openpyxl.worksheet.worksheet import Worksheet
import logging
```

Functions used:
- `strip_unit_suffix(value)` — called on qty, price, amount cell raw string before Decimal parsing.
- `safe_decimal(value, decimals)` — called for qty (detected precision), price (5), amount (2).
- `detect_cell_precision(cell)` — called on qty cell to determine display precision.
- `is_stop_keyword(value)` — called on part_no and on each cell A–J for stop condition 4.
- `FOOTER_KEYWORDS` — checked against part_no for stop condition 3.
- `MergeTracker.get_string_value(row, col, header_row)` — for all string fields.
- `MergeTracker.get_weight_value(row, col, header_row)` — NOT used here; weight extraction belongs to extract_packing.

---

## 5. Side-Effect Rules

- **No file I/O.** Receives `Worksheet` object as parameter.
- **No config loading.** All patterns arrive via `ColumnMapping` and `MergeTracker`.
- **Logging:** Use `logging.getLogger(__name__)`. Debug-log each row's extracted raw values and parsed Decimal results.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_014 (HEADER_ROW_NOT_FOUND) — owned by column_map.py.
- DO NOT validate/log ERR_020 (REQUIRED_COLUMN_MISSING) — owned by column_map.py.
- DO NOT validate/log ERR_021 (INVOICE_NUMBER_NOT_FOUND) — owned by batch.py.
- DO NOT validate/log ERR_040 (PART_NOT_IN_PACKING) — owned by weight_alloc.py.
- DO NOT validate/log ERR_043 (PACKING_PART_NOT_IN_INVOICE) — owned by weight_alloc.py.

---

## 7. Gotchas

1. **Data starts at `effective_header_row + 1`**, not `header_row + 1`. These differ when sub-header scanning advanced the effective row.
2. **Stop condition ordering for invoice differs from packing:** invoice checks blank first (skip), then stop conditions. Packing checks stop conditions first.
3. **COO/COD fallback is per-row**, not a global setting. Some rows may have COO filled; others may rely on COD. Evaluate each row independently.
4. **`part_no` "header continuation" filter** targets rows where the part_no cell literally contains the column header label (e.g., "PART NO."). These appear when a two-row header format repeats column labels below the primary header row.
5. **`inv_no` parameter vs column:** If `inv_no` column IS in field_map, extract it per row and clean prefixes. If NOT in field_map, use the `inv_no` parameter (from batch.py's orchestration of header fallback) for ALL rows.
6. **`model` field stored as `model_no` in InvoiceItem** (pydantic conflict avoidance — see build-plan.md Ambiguity #8).
7. **Do NOT raise ERR_030 for COO when COD fallback succeeds.** ERR_030 for COO only fires if both COO column and COD fallback both produce empty.
8. **Float artifacts** from openpyxl: always convert via `str(float_value)` then `Decimal(str(...))`, not `Decimal(float_value)`. Use `safe_decimal()` which handles this.
9. **Part_no consistency for downstream comparison with packing:** strip whitespace identically. Do not apply any other normalization (no case-folding, no punctuation removal). Exact match is required in weight_alloc.py.
10. **Patterned example from PRD — generalization rule:** The PRD lists footer keywords `(报关行, 有限公司)` as examples. These are **exact entries** from `FOOTER_KEYWORDS` constant in utils.py. Do not extend the list — use `FOOTER_KEYWORDS` as defined.

---

## 8. Test Requirements

### `extract_invoice_items()`

1. **test_extract_invoice_items_happy_path_13_fields** — Row with all 13 fields populated; verify InvoiceItem has correct values for part_no, qty (Decimal with cell precision), price (5 decimals), amount (2 decimals), currency, coo, brand, brand_type, model_no, cod, inv_no, serial; allocated_weight is None.
2. **test_extract_invoice_items_coo_cod_fallback** — COO column empty for a row, COD column has "CN"; extracted InvoiceItem.coo == "CN"; no ERR_030 raised.
3. **test_extract_invoice_items_stop_at_empty_part_no_qty_zero** — After first data row, row has empty part_no and qty=0; extraction stops; only rows before stop included.
4. **test_extract_invoice_items_stop_at_total_keyword_in_part_no** — Row where part_no cell contains "TOTAL"; extraction stops before that row.
5. **test_extract_invoice_items_stop_at_footer_keyword** — Row where part_no contains "有限公司"; extraction stops.
6. **test_extract_invoice_items_stop_at_any_cell_aj_total** — Row where column F contains "合计"; extraction stops.
7. **test_extract_invoice_items_header_continuation_skipped** — Row where part_no == "PART NO." skipped; next data row extracted normally.
8. **test_extract_invoice_items_unit_suffix_stripped** — Qty cell value "100 PCS"; parsed as Decimal('100') with cell precision; no ERR_031.
9. **test_extract_invoice_items_err030_on_missing_required_field** — Row with empty brand field; raises ProcessingError ERR_030 with field "brand" and row number in context.
10. **test_extract_invoice_items_err031_on_non_numeric_qty** — Row with "N/A" in qty column; raises ProcessingError ERR_031 with row and column in context.
11. **test_extract_invoice_items_horizontal_merge_brand_brand_type** — brand and brand_type columns are horizontally merged (anchor at brand col, brand_type col = None after unmerge); MergeTracker propagates "无品牌" to both fields.
12. **test_extract_invoice_items_inv_no_param_used_when_no_column** — No inv_no column in field_map; all extracted items have inv_no == parameter value "INV-2025-001".
