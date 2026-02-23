# Spec: report.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/report.py`
- **Tests:** `tests/test_report.py`
- **FRs:** FR-033

---

## 2. Functional Requirements

### FR-033 — Batch Summary Report

Produce a batch summary report to console after all files are processed. Always produces the summary even if all files failed.

**Display order:**
1. Summary header with totals and metadata.
2. Failed files section with per-file error details.
3. Files Needing Attention section with per-file warning details.

**Error condensing rule:** For each file, if multiple errors share the same error code, condense them as: `{code}: {message} (N occurrences)` with a representative `part_no` from the first occurrence's context. Do not list individual rows for repeated codes.

**Verbatim output format (copy character-for-character from PRD Section 7):**

```
[INFO] ===========================================================================
[INFO]                    BATCH PROCESSING SUMMARY
[INFO] ===========================================================================
[INFO] Total files:        {N}
[INFO] Successful:         {N}
[INFO] Attention:          {N}
[INFO] Failed:             {N}
[INFO] Processing time:    {N.NN} seconds
[INFO] Log file:           {path}/process_log.txt
[INFO] ===========================================================================
```

Failed section:
```
[ERROR] FAILED FILES:
[ERROR]   {filename}:
[ERROR]     {ERR_CODE}: {message} (N occurrences)
```

Attention section:
```
[WARNING] FILES NEEDING ATTENTION:
[WARNING]   {filename}:
[WARNING]     {ATT_CODE}: {message}
```

The report is printed using the logger (`logging.getLogger(__name__)`), not `print()`.

---

## 3. Exports

```python
def print_batch_summary(batch_result: BatchResult) -> None:
    """Format and print batch summary to console per FR-033 format.

    Args:
        batch_result: Completed batch result with all file results, counts,
                      timing, and log path.

    Returns:
        None. Outputs to console via logger (INFO/ERROR/WARNING level).
    """
```

---

## 4. Imports

```python
from .models import BatchResult, FileResult
from .errors import ProcessingError, ErrorCode, WarningCode
import logging
```

No imports from batch.py, cli.py, output.py, or weight_alloc.py.

---

## 5. Side-Effect Rules

- **No file I/O.** Logging to console only (via existing logger handlers configured by logger.py).
- **No output file writes.** output.py is the sole writer to disk.
- **Logging:** Use `logging.getLogger(__name__)`. Summary header at INFO. Failed files at ERROR. Attention files at WARNING.

---

## 6. Ownership Exclusions

- DO NOT validate/log ATT_002 (MISSING_TOTAL_PACKETS) as a new event — only report it if present in `FileResult.warnings`. ATT_002 is owned by extract_totals.py.
- DO NOT validate/log ATT_003 (UNSTANDARDIZED_CURRENCY) — owned by transform.py.
- DO NOT validate/log ATT_004 (UNSTANDARDIZED_COO) — owned by transform.py.
- This module is a pure reporting module. It reads pre-populated `BatchResult` data and formats it. It does NOT make any processing decisions.

---

## 7. Gotchas

1. **Summary always produced** even if `batch_result.total_files == 0` or all files failed.
2. **Processing time format:** `{N.NN} seconds` — exactly 2 decimal places. Use `f"{batch_result.processing_time:.2f} seconds"`.
3. **Log file path format:** `{path}/process_log.txt` where `{path}` is the directory of the log file. Use `batch_result.log_path` directly as specified in `BatchResult`.
4. **Separator line is exactly 75 `=` characters** (count the characters in the verbatim format). Verify: `"="*75`.
5. **Error condensing:** Group errors by `error.code.value` per file. For each group: if count > 1, append `"(N occurrences)"`. Representative part_no from `error.context.get('part_no', '')` of the first occurrence.
6. **Failed section omitted if no failed files.** Attention section omitted if no attention files.
7. **The indentation in the verbatim format is significant.** Use exactly two spaces before filename, four spaces before error/warning codes.

---

## 8. Verbatim Outputs

All strings must match PRD Section 7 character-for-character:

```
[INFO] ===========================================================================
[INFO]                    BATCH PROCESSING SUMMARY
[INFO] ===========================================================================
[INFO] Total files:        {N}
[INFO] Successful:         {N}
[INFO] Attention:          {N}
[INFO] Failed:             {N}
[INFO] Processing time:    {N.NN} seconds
[INFO] Log file:           {path}/process_log.txt
[INFO] ===========================================================================
```

Failed section header: `[ERROR] FAILED FILES:`
Attention section header: `[WARNING] FILES NEEDING ATTENTION:`

---

## 9. Test Requirements

### `print_batch_summary()`

1. **test_print_batch_summary_all_success** — BatchResult with 3 files all Success; verify logger.info called with separator, summary lines, counts; no FAILED section; no ATTENTION section. Use `caplog` fixture to capture log output.
2. **test_print_batch_summary_failed_files_section** — BatchResult with 1 failed file and ERR_020 error; verify `[ERROR] FAILED FILES:` and error code appear in log output.
3. **test_print_batch_summary_error_condensing** — Failed file with 3 ERR_030 errors for different rows; condensed as "ERR_030: ... (3 occurrences)" in output; not listed as 3 separate lines.
4. **test_print_batch_summary_attention_files_section** — BatchResult with 1 attention file and ATT_003 warning; verify `[WARNING] FILES NEEDING ATTENTION:` and ATT_003 appear.
5. **test_print_batch_summary_processing_time_two_decimal_format** — BatchResult.processing_time=12.3456; output contains "12.35 seconds".
