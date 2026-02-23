# Spec: config.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/config.py`
- **Tests:** `tests/test_config.py`

## 2. FRs

### FR-002: Load and Validate All Configuration Files

**Input:** `config/field_patterns.yaml`, `config/output_template.xlsx`, `config/currency_rules.xlsx`, `config/country_rules.xlsx`

**Rules (all must be enforced before any data file processing):**
1. Load `field_patterns.yaml` via PyYAML `yaml.safe_load()`. Raise ERR_001 if missing; ERR_004 if malformed (missing required keys).
2. Validate required YAML keys present: `invoice_sheet.patterns`, `packing_sheet.patterns`, `invoice_columns` (with subkeys for 14 fields), `packing_columns` (with subkeys for 6 fields), `inv_no_cell.patterns`, `inv_no_cell.label_patterns`, `inv_no_cell.exclude_patterns`. Raise ERR_004 if any required key is absent.
3. Compile all regex patterns from `invoice_sheet.patterns`, `packing_sheet.patterns`, `invoice_columns[*].patterns`, `packing_columns[*].patterns`, `inv_no_cell.patterns`, `inv_no_cell.label_patterns`, `inv_no_cell.exclude_patterns`. Raise ERR_002 with pattern name and compilation error message if any pattern fails to compile.
4. Load `currency_rules.xlsx` sheet `Currency_Rules`, columns `Source_Value` / `Target_Code`. Raise ERR_001 if file missing; ERR_004 if sheet or columns missing. Check for duplicate `Source_Value` entries; raise ERR_003 with the duplicate value. Normalize all keys via `normalize_lookup_key()` (uppercase, strip, collapse `, ` → `,`). Cast all `Target_Code` values to `str` (handles mixed int/str cells).
5. Load `country_rules.xlsx` sheet `Country_Rules`, columns `Source_Value` / `Target_Code`. Same rules as currency: ERR_001 if missing, ERR_004 if malformed, ERR_003 if duplicate `Source_Value`. Normalize keys. **Special requirement:** 3 entries have `Target_Code` stored as string instead of int — normalize ALL `Target_Code` values to `str` regardless of Excel cell type.
6. Load `output_template.xlsx` and validate: sheet `工作表1` must exist; must have ≥ 40 columns (A-AN); rows 1-4 must be present (template headers). Raise ERR_005 if validation fails. Store only the `Path` to the template in `AppConfig.template_path` — do NOT keep the workbook open (output.py loads it at write time).
7. All errors (ERR_001 through ERR_005) are raised as `ConfigError` (not `ProcessingError`) — they are fatal startup errors. Caller (cli.py / batch.py) exits with code 2 on `ConfigError`.
8. Return `AppConfig` with all compiled patterns, lookup dicts, `FieldPattern` objects, and `template_path`.

**Field definitions (for FieldPattern construction):**
- Invoice columns (14): `part_no`, `po_no`, `qty`, `price`, `amount`, `currency`, `coo`, `brand`, `brand_type`, `model`, `cod` (optional), `weight` (optional), `inv_no` (optional), `serial` (optional).
- Packing columns (6): `part_no`, `po_no` (optional), `qty`, `nw`, `gw`, `pack` (optional).

## 3. Exports

| Symbol | Signature | Return | Docstring Summary |
|--------|-----------|--------|-------------------|
| `load_config(config_dir: Path) -> AppConfig` | Load YAML + 3 Excel configs, compile all regex patterns, build normalized lookup tables, validate template structure. Raises ConfigError on any failure. | `AppConfig` | Load and validate all configuration files from config_dir; compile regex; build lookup tables; validate template. |

## 4. Imports

| Module | Symbols | Purpose |
|--------|---------|---------|
| `pathlib` (stdlib) | `Path` | File path resolution |
| `re` (stdlib) | `re.compile`, `re.IGNORECASE`, `re.error` | Regex compilation |
| `typing` (stdlib) | `Any` | YAML safe_load return type annotation |
| `yaml` (PyYAML) | `yaml.safe_load` | Load field_patterns.yaml |
| `openpyxl` | `load_workbook` | Load Excel config files |
| `.models` | `AppConfig`, `FieldPattern` | Return type and field definition container |
| `.errors` | `ConfigError`, `ErrorCode` | Fatal error reporting |
| `.utils` | `normalize_lookup_key` | Lookup table key normalization |

**Required call order within `load_config`:**
1. Load and validate `field_patterns.yaml` (ERR_001, ERR_004)
2. Compile all regex patterns from YAML (ERR_002)
3. Build `FieldPattern` objects for invoice and packing columns
4. Load and validate `currency_rules.xlsx` — build `currency_lookup` dict (ERR_001, ERR_003, ERR_004)
5. Load and validate `country_rules.xlsx` — build `country_lookup` dict (ERR_001, ERR_003, ERR_004)
6. Load and validate `output_template.xlsx` structure — store `template_path` (ERR_001, ERR_005)
7. Construct and return `AppConfig`

**Rationale:** Steps 1-2 must precede all others (YAML patterns are referenced by steps 3+). Steps 4-5 are independent of each other but must follow step 3. Step 6 is independent and can follow step 5. Step 7 assembles the final object.

## 5. Side-Effect Rules

- **File reads:** config.py is the ONLY module that reads config files from disk. All other modules receive `AppConfig` as a parameter.
- **No output writes.** config.py does not create or write any files.
- **No logging configuration.** config.py may call `logger.debug()` for config load milestones but does not configure handlers.
- **No workbook kept open.** The `output_template.xlsx` workbook is opened for validation only, then closed. Only `template_path: Path` is stored in `AppConfig`.

## 6. Verbatim Outputs (Error Context)

These error messages / context keys must be produced verbatim as specified:
- ERR_001 context: `{"path": str(missing_path)}` — exact path as string.
- ERR_002 context: `{"pattern_name": "<field_name>.<pattern_index>", "error": str(re.error)}`.
- ERR_003 context: `{"duplicate_value": "<Source_Value>", "file": str(rules_xlsx_path)}`.
- ERR_004 context: `{"key": "<missing_yaml_key>"}` or `{"sheet": "<missing_sheet_name>", "file": str(path)}`.
- ERR_005 context: `{"reason": "<description of validation failure>", "file": str(template_path)}`.

## 7. Gotchas

- **ERR_005 vs ERR_051 distinction:** config.py validates the TEMPLATE STRUCTURE (sheet exists, 40 columns, rows 1-4 present) and raises ERR_005. output.py validates that the template can be LOADED AT WRITE TIME and raises ERR_051. These are separate validations at separate times. config.py must NOT raise ERR_051.
- **`Target_Code` normalization (country_rules.xlsx):** Cast ALL `Target_Code` values to `str` unconditionally, regardless of whether the cell contains an int, float, or string. PRD Section 7 notes "3 Target_Code values stored as string instead of int." A `float` cell (e.g., `502.0`) should become `"502"` not `"502.0"` — cast via `str(int(float(value)))` if the value is numeric to avoid the trailing `.0`.
- **Duplicate `Source_Value` detection:** Compare after normalization via `normalize_lookup_key()`. Two entries are duplicates if their normalized keys are equal, even if their raw cell values differ by case or whitespace.
- **Regex compile flags:** All patterns compiled with `re.IGNORECASE`. Pattern compilation failures must capture the field name + pattern index for the ERR_002 context. Example pattern name: `"invoice_columns.part_no.pattern[0]"`.
- **YAML `safe_load` returns `Any`:** Explicit type narrowing required. After loading, verify the top-level result is a `dict`; then verify expected keys. Do not assume types of nested values.
- **Config files are relative to `config_dir`:** The caller (cli.py) passes the config directory path. All file paths are `config_dir / filename`. Never hardcode absolute paths.
- **`invoice_columns` YAML field names vs `model_no`:** The YAML uses `model` as a field key (matching the PRD). config.py reads this as `FieldPattern` objects keyed by `"model"` in `AppConfig.invoice_columns`. The rename to `model_no` only applies to the `InvoiceItem` pydantic field — the config dict key remains `"model"`. column_map.py uses `"model"` as the dict key when mapping columns.
- **Template validation — 40 columns:** Count the max column used in row 1 (or use `worksheet.max_column`). Must be ≥ 40. Column AN is column 40 (A=1, B=2, ..., AN=40).
- **`weight` column in invoice_columns:** The `weight` field is listed as optional in the YAML config (`required: false`). config.py stores its `FieldPattern` in `AppConfig.invoice_columns["weight"]`. Downstream modules map it but do not extract its values (Ambiguity #7 resolution).
- **Patterned examples in PRD (Generalization Gotcha):** FR-004 lists example patterns `^invoice`, `^inv$`, `^commercial` and FR-005 lists `^packing`, `^pack`, `^pak$`, `^dn&pl$`. These are YAML config values, not hardcoded in config.py. config.py compiles whatever patterns are in the YAML — it does not hardcode any sheet name patterns.

## 8. Ownership Exclusions

config.py owns ERR_001, ERR_002, ERR_003, ERR_004, ERR_005.

- DO NOT validate/log ERR_012 or ERR_013 (INVOICE/PACKING_SHEET_NOT_FOUND) — owned by sheet_detect.py.
- DO NOT validate/log ERR_014 (HEADER_ROW_NOT_FOUND) — owned by column_map.py.
- DO NOT validate/log ERR_020 (REQUIRED_COLUMN_MISSING) — owned by column_map.py.
- DO NOT validate/log ERR_051 (TEMPLATE_LOAD_FAILED) — owned by output.py. config.py validates STRUCTURE (ERR_005), output.py validates LOAD (ERR_051).

## 9. Test Requirements

### `load_config` — Happy Path
1. `test_load_config_success` — create a minimal valid config dir with all 4 config files; call `load_config(config_dir)`; verify returned `AppConfig` has `invoice_sheet_patterns` (list of compiled re.Pattern), `currency_lookup` (dict with normalized uppercase keys), `template_path` (Path).
2. `test_load_config_currency_lookup_normalized` — currency_rules.xlsx has `Source_Value="美元"`, `Target_Code=502` (int); verify `app_config.currency_lookup["美元"] == "502"` (string, normalized key).
3. `test_load_config_country_lookup_target_code_str` — country_rules.xlsx has 3 entries with string Target_Code and 1 with int; verify ALL values in `country_lookup` are `str` type.
4. `test_load_config_country_lookup_comma_space_key` — country_rules.xlsx has `Source_Value="Taiwan, China"`; verify key in `country_lookup` is `"TAIWAN,CHINA"` (normalized).
5. `test_load_config_field_patterns_compiled` — YAML has regex patterns for `invoice_columns.part_no`; verify `app_config.invoice_columns["part_no"].patterns` is a `list[str]` and `app_config.invoice_sheet_patterns` is a `list[re.Pattern]`.

### `load_config` — ERR_001
6. `test_load_config_missing_yaml_raises_err001` — remove `field_patterns.yaml`; verify `ConfigError` raised with `code == ErrorCode.ERR_001` and `path` pointing to the YAML file.
7. `test_load_config_missing_currency_xlsx_raises_err001` — remove `currency_rules.xlsx`; verify `ConfigError` with ERR_001.
8. `test_load_config_missing_country_xlsx_raises_err001` — remove `country_rules.xlsx`; verify `ConfigError` with ERR_001.
9. `test_load_config_missing_template_raises_err001` — remove `output_template.xlsx`; verify `ConfigError` with ERR_001.

### `load_config` — ERR_002
10. `test_load_config_invalid_regex_raises_err002` — YAML contains `invoice_columns.part_no.patterns: ["[invalid"]`; verify `ConfigError` with `code == ErrorCode.ERR_002`; context includes `pattern_name` and `error`.

### `load_config` — ERR_003
11. `test_load_config_duplicate_source_value_raises_err003` — currency_rules.xlsx has two rows with same `Source_Value` (e.g., "USD" twice); verify `ConfigError` with `code == ErrorCode.ERR_003`; context includes `duplicate_value`.
12. `test_load_config_duplicate_source_value_case_insensitive` — country_rules.xlsx has "china" and "CHINA" as Source_Value entries; verify ERR_003 (same after normalization).

### `load_config` — ERR_004
13. `test_load_config_malformed_yaml_missing_key_raises_err004` — YAML missing `invoice_sheet` key; verify `ConfigError` with `code == ErrorCode.ERR_004`.
14. `test_load_config_malformed_currency_sheet_raises_err004` — currency_rules.xlsx missing `Currency_Rules` sheet; verify `ConfigError` with ERR_004.

### `load_config` — ERR_005
15. `test_load_config_template_missing_sheet_raises_err005` — output_template.xlsx missing `工作表1` sheet; verify `ConfigError` with `code == ErrorCode.ERR_005`.
16. `test_load_config_template_insufficient_columns_raises_err005` — output_template.xlsx has only 30 columns; verify `ConfigError` with ERR_005.
