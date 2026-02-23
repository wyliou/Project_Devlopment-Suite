Module: src/autoconvert/validate.py | Tests: tests/test_validate.py | FRs: FR-027

Exports:
  determine_file_status(errors: list[ProcessingError], warnings: list[ProcessingError]) -> str
    Any ERR_xxx -> "Failed", any ATT_xxx (no ERR_xxx) -> "Attention", else -> "Success".

Imports:
  .models: (none needed beyond ProcessingError)
  .errors: ProcessingError, ErrorCode, WarningCode

Tests:
  1. test_determine_file_status_success_no_errors_no_warnings — empty errors and warnings lists; returns "Success"
  2. test_determine_file_status_failed_on_any_err — one ERR_020 ProcessingError; returns "Failed" regardless of warnings
  3. test_determine_file_status_attention_att_only — no ERR, one ATT_003 warning; returns "Attention"
  4. test_determine_file_status_failed_takes_precedence_over_att — one ERR_030 and one ATT_003; returns "Failed" (ERR wins)
  5. test_determine_file_status_distinguishes_errorcode_vs_warningcode — verifies type check uses isinstance(error.code, ErrorCode) for ERR detection and isinstance(error.code, WarningCode) for ATT detection

Gotchas:
  - Status determination is purely based on the code type (ErrorCode vs WarningCode), not the string prefix. Use isinstance checks on error.code.
  - This module does NOT accumulate errors. It only inspects already-accumulated lists passed by batch.py.
  - "Failed" status is returned even when the errors list contains only ATT-prefixed codes IF they were mistakenly constructed with ErrorCode — but this should not happen; validate.py only inspects, does not produce errors.
