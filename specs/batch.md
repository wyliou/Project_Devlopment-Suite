# Spec: batch.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/batch.py`
- **Tests:** `tests/test_batch.py`
- **FRs:** FR-001, FR-003, FR-028

---

## 2. Functional Requirements

### FR-001 — Directory Setup

On startup (`run_batch()` entry), auto-create `data/` and `data/finished/` directories if missing.

- `config/` must pre-exist (validated by config.py, not batch.py).
- If directory creation fails (PermissionError) → log error with exact path, raise to caller (cli.py handles sys.exit(2)).

### FR-003 — File Scanning and Queuing

Scan `data/` folder for `.xlsx` and `.xls` files.

**Exclusion rules:**
- Exclude temp files: filenames starting with `~$` (Excel temp files).
- Exclude hidden files: check `os.stat()` and `stat.FILE_ATTRIBUTE_HIDDEN` on Windows.

**Per-file handling:**
- `.xls` files: convert in-memory via `xls_adapter.convert_xls_to_xlsx()` — no temp file, original untouched.
- `.xlsx` files: open with `openpyxl.load_workbook(filepath, data_only=True)`.
- File locked: catch `PermissionError` → record ERR_010, skip file.
- File corrupted: catch `Exception` from openpyxl/xlrd → record ERR_011, skip file.
- Process each file independently — one file's failure does not abort the batch.
- No processable files found → log info, return empty BatchResult.

### FR-028 — Clear Output Directory

Before processing any files, remove all existing files in `data/finished/`.

**Timing:** after directory setup (FR-001) and after file scanning (FR-003), but before processing any individual file.

**Error:** PermissionError on delete → log error, raise to caller.

---

## 3. Exports

```python
def run_batch(config: AppConfig) -> BatchResult:
    """Orchestrate full batch: setup dirs (FR-001), clear finished (FR-028),
    scan files (FR-003), process each, collect results.

    Args:
        config: Application configuration (pre-loaded, pre-validated by config.py).

    Returns:
        BatchResult with counts, timing, and per-file FileResult list.
    """

def process_file(filepath: Path, config: AppConfig) -> FileResult:
    """Per-file pipeline: open workbook, detect sheets, map columns,
    extract, transform, allocate, validate, output.

    Args:
        filepath: Absolute path to the input Excel file.
        config: Application configuration.

    Returns:
        FileResult with status, errors, warnings, invoice_items, packing_items,
        packing_totals.
    """
```

---

## 4. Imports

```python
from .models import AppConfig, FileResult, BatchResult, InvoiceItem
from .errors import ProcessingError, ErrorCode, WarningCode
from .logger import setup_logging, setup_diagnostic_logging
from .config import load_config
from .sheet_detect import detect_sheets
from .column_map import detect_header_row, map_columns, extract_inv_no_from_header
from .merge_tracker import MergeTracker
from .extract_invoice import extract_invoice_items
from .extract_packing import extract_packing_items, validate_merged_weights
from .extract_totals import detect_total_row, extract_totals
from .transform import convert_currency, convert_country, clean_po_number
from .weight_alloc import allocate_weights
from .validate import determine_file_status
from .output import write_template
from .report import print_batch_summary
from .xls_adapter import convert_xls_to_xlsx
import openpyxl
from pathlib import Path
import os
import stat
import time
import logging
```

---

## 5. Required Call Order (Field Population Map Compliance)

The following call order is MANDATORY. Each step is annotated with the Field Population Map constraint it satisfies.

### `process_file()` — Required Call Sequence

```
Phase 1: Open Workbook
  [1] Open file: openpyxl.load_workbook() or xls_adapter.convert_xls_to_xlsx()
      ERR_010 (FILE_LOCKED) or ERR_011 (FILE_CORRUPTED) → short-circuit to status

Phase 2: Sheet Detection  (short-circuits on ANY ERR in this phase)
  [2] detect_sheets(workbook, config)
      → (invoice_sheet, packing_sheet)
      ERR_012 or ERR_013 → short-circuit

Phase 3a: Invoice Column Mapping  (short-circuits on ANY ERR)
  [3] MergeTracker(invoice_sheet)  ← captures merges BEFORE unmerge
  [4] detect_header_row(invoice_sheet, "invoice", config)
      ERR_014 → short-circuit
  [5] map_columns(invoice_sheet, header_row, "invoice", config)
      ERR_020 → short-circuit
      → invoice_column_map (includes effective_header_row, possibly currency column shift)

  [6] inv_no POPULATION STEP A: Check if inv_no in invoice_column_map.field_map
      (If present, extraction in step [11] will read it per-row)

Phase 3b: Packing Column Mapping  (short-circuits on ANY ERR)
  [7] MergeTracker(packing_sheet)  ← captures merges BEFORE unmerge
  [8] detect_header_row(packing_sheet, "packing", config)
      ERR_014 → short-circuit
  [9] map_columns(packing_sheet, header_row, "packing", config)
      ERR_020 → short-circuit
      → packing_column_map

  RATIONALE: Both column maps must complete before extraction begins.
  ERR_020 in either sheet aborts extraction for that sheet.

Phase 3c: Invoice Number Fallback  (Detection-Fallback Map constraint)
  [10] IF inv_no NOT in invoice_column_map.field_map:
         inv_no = extract_inv_no_from_header(invoice_sheet, config)
         (returns str | None — does NOT raise ERR_021)
       ELSE:
         inv_no = None  ← extraction step [11] will populate per-row

  [10b] AFTER extraction step [11] completes:
         IF inv_no column was in field_map: inv_no = invoice_items[0].inv_no if items else None
         IF inv_no is still None (neither column nor header found any value):
           Raise ERR_021 (INVOICE_NUMBER_NOT_FOUND)

  RATIONALE: ERR_021 fires ONLY after BOTH column extraction AND header fallback fail.
  Primary (column) must attempt before fallback (header scan). Neither raises ERR_021 alone.

Phase 4: Data Extraction  (short-circuits on ANY ERR in this phase)

  [11] extract_invoice_items(invoice_sheet, invoice_column_map, invoice_merge_tracker, inv_no_param)
       ERR_030, ERR_031 → short-circuit
       → invoice_items
       (inv_no_param is the value from step [10] if header fallback was used, else None)

  [12] extract_packing_items(packing_sheet, packing_column_map, packing_merge_tracker)
       ERR_030, ERR_031 → short-circuit
       → (packing_items, last_data_row)

  [13] validate_merged_weights(packing_items, packing_merge_tracker, packing_column_map)
       ERR_046 → short-circuit

  RATIONALE (Detection-Fallback Map — coo field):
  extract_invoice_items handles COO/COD fallback internally per row.
  ERR_030 for COO fires inside extract_invoice_items only after COD fallback fails.
  batch.py does not need to orchestrate coo fallback.

  [14] detect_total_row(packing_sheet, last_data_row, packing_column_map, packing_merge_tracker)
       Strategy 1 → None → Strategy 2 → None → ERR_032 → short-circuit
       → total_row

  RATIONALE (Detection-Fallback Map — total_row):
  Strategy 1 (keyword) runs first, returns None if not found.
  Strategy 2 (implicit) runs only when Strategy 1 fails.
  ERR_032 fires only after both strategies fail.
  This is handled internally by detect_total_row(); batch.py does not need to sequence them.

  [15] extract_totals(packing_sheet, total_row, packing_column_map)
       ERR_033, ERR_034 → short-circuit
       ATT_002 (total_packets=None) → collect as warning
       → packing_totals

  FIELD POPULATION MAP CHECK — all required fields now populated or failed:
  - inv_no: from column extraction [11] or header fallback [10]; ERR_021 checked at [10b]
  - currency: from column extraction [11] (possibly with column shift from [5])
  - coo: from column extraction [11] (with COD fallback inside extract_invoice_items)
  - po_no: from column extraction [11]
  - nw (packing): from extract_packing_items [12]
  - total_nw: from extract_totals [15]
  - total_gw: from extract_totals [15]
  - total_packets: from extract_totals [15] (None → ATT_002)
  - part_no (packing): from extract_packing_items [12] (with merge propagation inside)

Phase 5: Transformation  (warnings only — no short-circuit for ATT_xxx)
  [16] invoice_items, currency_warnings = convert_currency(invoice_items, config)
       ATT_003 → collect warnings, continue

  [17] invoice_items, country_warnings = convert_country(invoice_items, config)
       ATT_004 → collect warnings, continue

  [18] invoice_items = clean_po_number(invoice_items)
       No errors/warnings

  FIELD POPULATION MAP CHECK:
  - currency: now converted (or raw if ATT_003)
  - coo: now converted (or raw if ATT_004)
  - po_no: now cleaned

Phase 6: Weight Allocation  (short-circuits on ANY ERR)
  [19] invoice_items = allocate_weights(invoice_items, packing_items, packing_totals)
       ERR_040, ERR_041, ERR_042, ERR_043, ERR_044, ERR_045, ERR_047, ERR_048 → short-circuit

  FIELD POPULATION MAP CHECK:
  - allocated_weight: all invoice_items now have allocated_weight populated (FR-026 validated)

Phase 7: Validation
  [20] status = determine_file_status(all_errors, all_warnings)

Phase 8: Output  (only for Success or Attention)
  [21] IF status in ("Success", "Attention"):
         output_path = config.finished_dir / f"{filepath.stem}_template.xlsx"
         write_template(invoice_items, packing_totals, config, output_path)
         ERR_051, ERR_052 → collect error (status becomes Failed if ERR occurs)
```

### `run_batch()` — Required Call Sequence

```
[1] Auto-create data/ and data/finished/ (FR-001)
[2] Scan data/ for .xlsx/.xls files, excluding ~$ and hidden (FR-003)
[3] IF no processable files: log info, return empty BatchResult
[4] Clear data/finished/ of all existing files (FR-028)
    RATIONALE: FR-028 requires clearing BEFORE processing, not before scanning.
               Scanning first ensures files exist before destructive clear.
[5] start_time = time.monotonic()
[6] FOR each filepath in file_list:
      log [N/M] Processing: {filename} ... header
      file_result = process_file(filepath, config)
      collect file_result into results list
[7] processing_time = time.monotonic() - start_time
[8] batch_result = BatchResult(total_files=..., success_count=..., ...)
[9] print_batch_summary(batch_result)
[10] return batch_result
```

---

## 6. Side-Effect Ownership

- **Excel file reads:** ONLY batch.py opens workbooks via openpyxl/xlrd. All other modules receive Worksheet objects.
- **Directory creation (`data/`, `data/finished/`):** ONLY batch.py.
- **Directory clearing (`data/finished/`):** ONLY batch.py.
- **Output file paths:** batch.py constructs `output_path = config.finished_dir / f"{filepath.stem}_template.xlsx"` and passes it to `write_template()`.
- **Config loading:** ONLY config.py (via cli.py before batch.py is called). batch.py receives pre-loaded AppConfig.

---

## 7. Phase Short-Circuit Rules (from build-context.md)

When any ERR occurs in a phase:
1. Collect all errors within the CURRENT phase (do not stop mid-phase for collect-then-report modules like column_map.py).
2. Skip ALL downstream phases.
3. Jump directly to status determination (step [20]).
4. Record status as "Failed".

**ATT_xxx warnings do NOT trigger short-circuit.** Collection continues; no phase is skipped.

**Phase order:** (1) Sheet Detection, (2) Column Mapping, (3) Extraction, (4) Weight Allocation, (5) Output.

---

## 8. Ownership Exclusions

- DO NOT validate/log ERR_001 (CONFIG_NOT_FOUND) — owned by config.py.
- DO NOT validate/log ERR_002 (INVALID_REGEX) — owned by config.py.
- DO NOT validate/log ERR_003 (DUPLICATE_LOOKUP) — owned by config.py.
- DO NOT validate/log ERR_004 (MALFORMED_CONFIG) — owned by config.py.
- DO NOT validate/log ERR_005 (TEMPLATE_INVALID) — owned by config.py.
- DO NOT validate/log ERR_012 (INVOICE_SHEET_NOT_FOUND) — owned by sheet_detect.py.
- DO NOT validate/log ERR_013 (PACKING_SHEET_NOT_FOUND) — owned by sheet_detect.py.
- DO NOT validate/log ERR_014 (HEADER_ROW_NOT_FOUND) — owned by column_map.py.
- DO NOT validate/log ERR_020 (REQUIRED_COLUMN_MISSING) — owned by column_map.py.
- DO NOT validate/log ERR_052 (OUTPUT_WRITE_FAILED) — owned by output.py (batch.py catches and records, but does not raise it itself).
- ERR_021 (INVOICE_NUMBER_NOT_FOUND): batch.py is the ORCHESTRATOR that raises ERR_021 after both column extraction and header fallback both fail. batch.py raises this error but does so only after consulting column_map.extract_inv_no_from_header().

---

## 9. Gotchas

1. **MergeTracker must be initialized BEFORE any other operation on the sheet.** MergeTracker captures merge ranges and calls `sheet.unmerge_cells()` internally. If detect_header_row or map_columns run on an unmerged sheet, they see None cells instead of merged values. Order: `MergeTracker(sheet)` → then detect_header_row → map_columns → extraction.
2. **Invoice and packing MergeTrackers are separate instances** on their respective sheets. Do not share a MergeTracker between sheets.
3. **inv_no resolution follows Detection-Fallback Map exactly:**
   - If inv_no column IS in field_map: pass `inv_no_param=None` to `extract_invoice_items()`; items will populate per-row.
   - If inv_no column IS NOT in field_map: call `extract_inv_no_from_header()` first; pass result as `inv_no_param`.
   - After extraction: if items have inv_no populated (either column or param), proceed; else raise ERR_021.
   - ERR_021 is raised by batch.py — do not raise it in column_map.py or extract_invoice.py.
4. **`xls_adapter.convert_xls_to_xlsx()` returns an in-memory `Workbook`** — not a path. Pass the returned Workbook object to MergeTracker and sheet_detect.
5. **File scan must exclude `~$` prefix AND hidden files.** On Windows, use `os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN` (value 2) to detect hidden files. This requires `import stat` from stdlib.
6. **`data/finished/` must be cleared BEFORE processing any file**, not before each file. Clearing happens once per batch at the batch start. Order: scan files → then clear → then process.
7. **`[N/M] Processing: {filename}...` header** must be logged at INFO level before calling process_file() — it is a per-file milestone log per FR-031 format.
8. **Diagnostic mode uses a separate code path in cli.py** (via `--diagnostic <filename>`). batch.py's `process_file()` is reused by diagnostic mode, but `run_batch()` is not called in diagnostic mode.
9. **`BatchResult.log_path`** should be set to the absolute path of `process_log.txt`. This value is printed in the batch summary report.
10. **Phase isolation for collect-then-report errors:** If `map_columns()` raises with a list of missing columns (ERR_020), batch.py catches the single `ProcessingError` (which contains all missing field names in the message/context). It does NOT call map_columns multiple times.

---

## 10. Verbatim Outputs

Console log format (FR-031):
```
[INFO] -----------------------------------------------------------------
[INFO] [N/M] Processing: {filename} ...
[INFO] Inv_No extracted ({method}): {value} at '{cell}'
[INFO] Invoice sheet extracted {N} items (rows {start}-{end})
[INFO] Packing total row at row {N}, NW= {val}, GW= {val}, Packets= {val}
[INFO] Packing sheet extracted {N} items (rows {start}-{end})
[INFO] Trying precision: {N}
[INFO] Expecting rounded part sum: {val}, Target: {val}
[INFO] Perfect match at {N} decimals
[INFO] Weight allocation complete: {val}
[INFO] Output successfully written to: {filename}_template.xlsx
[INFO] ✅ SUCCESS
```

Errors: `[ERROR] [ERR_xxx] {message}` → `[ERROR] ❌ FAILED`
Warnings: `[WARNING] [ATT_xxx] {message}` → `[WARNING] ⚠️ ATTENTION`

---

## 11. Test Requirements

### `run_batch()`

1. **test_run_batch_creates_directories** — data/ and data/finished/ don't exist; after run_batch(), both exist.
2. **test_run_batch_clears_finished_before_processing** — data/finished/ has stale files before batch; after run_batch(), stale files gone and new outputs present.
3. **test_run_batch_empty_folder_returns_empty_result** — data/ has no .xlsx/.xls files; BatchResult.total_files == 0; no crash.
4. **test_run_batch_excludes_temp_files** — data/ has "~$temp.xlsx"; excluded from processing; BatchResult.total_files == 0.
5. **test_run_batch_one_file_processed** — data/ has one valid file; BatchResult.total_files == 1; success_count or failed_count == 1.

### `process_file()`

1. **test_process_file_full_pipeline_success** — Valid file with all sheets, columns, data; returns FileResult with status="Success", non-empty invoice_items with allocated_weight, output file created.
2. **test_process_file_short_circuit_on_err012** — File where detect_sheets raises ERR_012; FileResult.status="Failed"; column mapping, extraction, allocation NOT called; no output file.
3. **test_process_file_short_circuit_on_err020** — File where map_columns raises ERR_020; FileResult.status="Failed"; extraction NOT called.
4. **test_process_file_inv_no_header_fallback** — File with no inv_no column; header area has "INVOICE NO.: INV-001"; FileResult.invoice_items[0].inv_no == "INV-001".
5. **test_process_file_err021_when_both_inv_no_sources_fail** — No inv_no column AND header scan returns None; FileResult has ERR_021 error.
6. **test_process_file_att003_produces_attention_status** — ATT_003 from currency conversion; no ERR; FileResult.status="Attention".
7. **test_process_file_xls_file_processed** — Input is .xls file; convert_xls_to_xlsx called; processing succeeds same as .xlsx.
