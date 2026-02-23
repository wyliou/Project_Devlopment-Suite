# Spec: output.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/output.py`
- **Tests:** `tests/test_output.py`
- **FRs:** FR-029, FR-030

---

## 2. Functional Requirements

### FR-029 — Template Population

Load `config/output_template.xlsx` (sheet `工作表1`). Preserve rows 1–4 (headers, data types, required/optional rules, fill instructions). Write one row per `InvoiceItem` starting at row 5.

**Column mapping (A=1 through AN=40):**

| Col | Letter | Field | Source | Notes |
|-----|--------|-------|--------|-------|
| 1 | A | 企业料号 (part_no) | InvoiceItem.part_no | Required |
| 2 | B | 采购订单号 (po_no) | InvoiceItem.po_no | Cleaned per FR-020 |
| 3 | C | 征免方式 | Fixed "3" | All rows, every item |
| 4 | D | 币制 (currency) | InvoiceItem.currency | Numeric code via FR-018; raw string if ATT_003 |
| 5 | E | 申报数量 (qty) | InvoiceItem.qty | |
| 6 | F | 申报单价 (price) | InvoiceItem.price | |
| 7 | G | 申报总价 (amount) | InvoiceItem.amount | |
| 8 | H | 原产国 (coo) | InvoiceItem.coo | Numeric code via FR-019; raw string if ATT_004 |
| 9–11 | I–K | Reserved | N/A | Empty (leave blank) |
| 12 | L | 报关单商品序号 (serial) | InvoiceItem.serial | |
| 13 | M | 净重 (weight) | InvoiceItem.allocated_weight | Weight from FR-025 |
| 14 | N | 发票号码 (inv_no) | InvoiceItem.inv_no | |
| 15 | O | Reserved | N/A | Empty |
| 16 | P | 毛重 (total_gw) | packing_totals.total_gw | **Row 5 ONLY** |
| 17 | Q | Reserved | N/A | Empty |
| 18 | R | 境内目的地代码 | Fixed "32052" | All rows |
| 19 | S | 行政区划代码 | Fixed "320506" | All rows |
| 20 | T | 最终目的国 | Fixed "142" | All rows |
| 21–36 | U–AJ | Reserved | N/A | Empty (16 columns) |
| 37 | AK | 件数 (total_packets) | packing_totals.total_packets | **Row 5 ONLY** |
| 38 | AL | 品牌 (brand) | InvoiceItem.brand | |
| 39 | AM | 品牌类型 (brand_type) | InvoiceItem.brand_type | |
| 40 | AN | 型号 (model) | InvoiceItem.model_no | |

**Attention file passthrough:** For files with ATT_003 or ATT_004, the raw vendor string for currency/coo is passed through to columns D/H as-is (because `convert_currency`/`convert_country` preserved the original value on no match). No special logic needed — just write `InvoiceItem.currency` and `InvoiceItem.coo` as stored.

**Only generate output for files with "Success" or "Attention" status.** Files with "Failed" status do not call `write_template()`.

**Template number format:** columns L and M use `0.00000_` (5 decimals); all others use `@` (text format). The template file already has these formats set in rows 1–4; data rows inherit the format from the template structure or are written as values only.

### FR-030 — Output File Naming and Save

Save as `{input_filename}_template.xlsx` in `data/finished/` directory.

- `input_filename` is the stem of the input file (without extension, without path).
- Example: `ACME_INV_001.xlsx` → `ACME_INV_001_template.xlsx`.

**Error:** ERR_052 (OUTPUT_WRITE_FAILED) if write fails (permission, disk space).

---

## 3. Exports

```python
def write_template(
    invoice_items: list[InvoiceItem],
    packing_totals: PackingTotals,
    config: AppConfig,
    output_path: Path,
) -> None:
    """Populate 40-column template and write to output_path.

    Args:
        invoice_items: Fully processed invoice items with allocated_weight populated.
        packing_totals: Packing totals for total_gw (col P, row 5) and
                        total_packets (col AK, row 5).
        config: Application configuration with template_path.
        output_path: Full path to write output file (data/finished/{stem}_template.xlsx).

    Returns:
        None.

    Raises:
        ProcessingError: ERR_051 if template cannot be loaded at write time;
                         ERR_052 if the output file cannot be written.
    """
```

---

## 4. Imports

```python
from .models import InvoiceItem, PackingTotals, AppConfig
from .errors import ProcessingError, ErrorCode
import openpyxl
from openpyxl import load_workbook
from pathlib import Path
import logging
```

No imports from weight_alloc.py, validate.py, or report.py. output.py receives fully processed data as parameters.

---

## 5. Side-Effect Rules

- **Output file writes are the sole purpose of this module.** Only `output.py` writes to `data/finished/`. batch.py constructs `output_path` and passes it in.
- **No directory creation.** batch.py ensures `data/finished/` exists before calling `write_template()`.
- **Template loading:** Load template from `config.template_path` at call time inside `write_template()`. If load fails → ERR_051.
- **Logging:** Use `logging.getLogger(__name__)`. Log INFO: `Output successfully written to: {filename}_template.xlsx` per FR-031 format.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_005 (TEMPLATE_INVALID) — owned by config.py (structure validation at startup). output.py validates that the template can be loaded at write time (ERR_051), which is separate from structure validation (ERR_005).
- DO NOT validate/log ERR_041 (WEIGHT_ALLOCATION_MISMATCH) — owned by weight_alloc.py.
- DO NOT validate/log ERR_048 (WEIGHT_FINAL_VALIDATION_FAILED) — owned by weight_alloc.py.
- ATT_002 (MISSING_TOTAL_PACKETS) — owned by extract_totals.py. output.py handles total_packets=None gracefully (writes empty cell at AK row 5).
- ATT_003 (UNSTANDARDIZED_CURRENCY) — owned by transform.py. output.py simply passes raw currency value through to column D.
- ATT_004 (UNSTANDARDIZED_COO) — owned by transform.py. output.py simply passes raw coo value through to column H.

---

## 7. Gotchas

1. **Row 5 is the first data row** (rows 1–4 are template metadata). Item index 0 → row 5, item index N → row `5 + N`. Use `output_sheet.cell(row=5 + item_index, column=col_num)`.
2. **total_gw and total_packets are written ONLY at row 5** (the first data row). All other rows leave columns P and AK empty.
3. **Fixed values written to every data row:** column C="3", column R="32052", column S="320506", column T="142". These are strings — write as string literals.
4. **Columns I, J, K, O, Q, U–AJ are empty.** Write nothing (leave cell value as None/unset). Do not write empty strings — they may affect downstream format validation.
5. **`total_packets` may be None** (ATT_002 case). If None, write nothing to column AK row 5.
6. **Template sheet name is `工作表1`** — must access exactly this sheet name, including the Chinese characters.
7. **ERR_051 is raised by output.py** at template load time (not at startup). config.py validates the template structure at startup (ERR_005); output.py validates that it can be loaded during the output step (ERR_051). These are separate concerns.
8. **`allocated_weight` goes into column M (净重).** This is the per-item weight from FR-025, not the total NW. The template format for column M is `0.00000_` — write as Decimal value; openpyxl will apply the cell format.
9. **Column AN uses `model_no` from InvoiceItem.** The PRD field is "型号 (model)" but the Python attribute is `model_no` (pydantic conflict avoidance). Access `item.model_no`.
10. **Template is loaded fresh for each file** (inside `write_template()`), not cached, to avoid state contamination between files in a batch.

---

## 8. Verbatim Outputs

Console log format (FR-031):
```
[INFO] Output successfully written to: {filename}_template.xlsx
```

---

## 9. Test Requirements

### `write_template()`

1. **test_write_template_creates_output_file** — Call with 2 invoice items; verify output file exists at `output_path`; verify file can be opened with openpyxl.
2. **test_write_template_rows_1_to_4_preserved** — Template rows 1–4 content unchanged after write; row 5 has first item's data.
3. **test_write_template_column_mapping_correct** — Item with known field values; assert row 5 col A = part_no, col C = "3", col D = currency, col E = qty, col M = allocated_weight, col P = total_gw (only row 5), col R = "32052", col S = "320506", col T = "142", col AN = model_no.
4. **test_write_template_total_gw_and_packets_row5_only** — Two invoice items; total_gw written at row 5 col P only; row 6 col P is empty; total_packets written at row 5 col AK only; row 6 col AK is empty.
5. **test_write_template_total_packets_none_writes_empty** — packing_totals.total_packets is None; row 5 col AK is empty (no error raised).
6. **test_write_template_err051_on_bad_template_path** — config.template_path points to non-existent file; raises ProcessingError ERR_051.
7. **test_write_template_err052_on_unwritable_path** — output_path is in a read-only directory; raises ProcessingError ERR_052.
