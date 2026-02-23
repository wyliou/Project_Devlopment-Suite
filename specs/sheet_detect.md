Module: src/autoconvert/sheet_detect.py | Tests: tests/test_sheet_detect.py | FRs: FR-004, FR-005, FR-006

Exports:
  detect_sheets(workbook: Workbook, config: AppConfig) -> tuple[Worksheet, Worksheet]
    Identify Invoice + Packing sheets by regex; raises ProcessingError ERR_012/013.

Imports:
  .models: AppConfig
  .errors: ProcessingError, ErrorCode
  openpyxl.workbook.workbook: Workbook
  openpyxl.worksheet.worksheet: Worksheet

Tests:
  1. test_detect_sheets_invoice_matched_by_pattern — sheet name "INVOICE" matches ^invoice pattern (case-insensitive), returns correct pair
  2. test_detect_sheets_packing_matched_by_dn_pl — sheet name "DN&PL" matches ^dn&pl$ pattern, returns correct packing sheet
  3. test_detect_sheets_invoice_not_found_raises_err012 — workbook with only "Packing" sheet raises ProcessingError with code ERR_012
  4. test_detect_sheets_packing_not_found_raises_err013 — workbook with only "Invoice" sheet raises ProcessingError with code ERR_013
  5. test_detect_sheets_ignores_unrecognized_sheets — workbook with extra "Purchase Contract" and "Lookup" sheets ignored; correct pair still returned

Gotchas:
  - Strip whitespace from sheet names before pattern matching (FR-004, FR-005).
  - Pattern matching is case-insensitive (re.IGNORECASE).
  - First matching sheet wins for each type.
  - ERR_012 and ERR_013 are both raised by this module — DO NOT raise ERR_012 or ERR_013 in batch.py or column_map.py.
  - DO NOT validate/log ERR_002 (INVALID_REGEX) — owned by config.py. Patterns arrive already compiled in AppConfig.
