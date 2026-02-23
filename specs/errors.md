Module: `src/autoconvert/errors.py` | Tests: `tests/test_errors.py` | FRs: FR-002 (error catalog), FR-027 (status determination inputs)

Exports:
- `ErrorCode` — enum with string values matching PRD catalog exactly. Members: ERR_001 through ERR_052 (non-contiguous; see catalog below). Each member value is the code string, e.g. `ERR_001 = "ERR_001"`.
  Full member list: ERR_001, ERR_002, ERR_003, ERR_004, ERR_005, ERR_010, ERR_011, ERR_012, ERR_013, ERR_014, ERR_020, ERR_021, ERR_030, ERR_031, ERR_032, ERR_033, ERR_034, ERR_040, ERR_041, ERR_042, ERR_043, ERR_044, ERR_045, ERR_046, ERR_047, ERR_048, ERR_051, ERR_052.
- `WarningCode` — enum with string values. Members: ATT_002 = "ATT_002", ATT_003 = "ATT_003", ATT_004 = "ATT_004".
- `ProcessingError` — `class(Exception)`: fields `code: ErrorCode | WarningCode`, `message: str`, `context: dict[str, Any]`. Used for per-file processing errors and warnings. Caught by batch.py; does NOT abort the batch.
- `ConfigError` — `class(Exception)`: fields `code: ErrorCode`, `message: str`, `path: str`. Raised during startup config loading (FR-002). Fatal — causes exit code 2. Never caught by per-file processing.

Imports:
- `enum`: `Enum`
- `typing`: `Any`

Tests:
1. `test_error_code_values_match_prd` — all 28 ErrorCode members have string values exactly matching their name (e.g., `ErrorCode.ERR_001.value == "ERR_001"`).
2. `test_warning_code_values_match_prd` — all 3 WarningCode members have string values matching their name.
3. `test_processing_error_is_exception` — `ProcessingError(code=ErrorCode.ERR_020, message="missing", context={})` is an instance of `Exception`; `.code`, `.message`, `.context` accessible.
4. `test_config_error_is_exception` — `ConfigError(code=ErrorCode.ERR_001, message="not found", path="/config/x.yaml")` is an instance of `Exception`; `.path` accessible.
5. `test_processing_error_accepts_warning_code` — `ProcessingError(code=WarningCode.ATT_003, message="warn", context={"field": "currency"})` created without error; `.code` is `WarningCode.ATT_003`.

Gotchas:
- ERR codes are non-contiguous (gaps at 006-009, 015-019, 022-029, 035-039, 049-050, 053+). Define only the codes listed in the PRD Section 7 catalog — do not fill gaps.
- `ProcessingError` accepts BOTH `ErrorCode` and `WarningCode` for its `code` field (warnings are ProcessingError instances with WarningCode). Type annotation must be `ErrorCode | WarningCode`.
- `ConfigError` accepts only `ErrorCode` (config errors are always hard failures, never warnings).
- Do not add any validation logic, lookup behavior, or logging in this module. It is a pure data-definition module.
