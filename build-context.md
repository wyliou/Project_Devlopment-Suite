# Build Context - AutoConvert

> Generated: 2026-02-20
> PRD: docs/PRD.md
> Architecture: docs/architecture.md

---

## Stack

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| Language | Python | 3.11+ | Type hints with `X | None` syntax, Decimal support |
| Excel (.xlsx) | openpyxl | 3.1.5 | `data_only=True` for formula values, merge handling |
| Excel (.xls) | xlrd | 2.0.2 | Legacy format, in-memory conversion, read-only |
| YAML | PyYAML | 6.0.3 | Config loading for field_patterns.yaml |
| Data models | pydantic | 2.12+ | Typed validation for all entities |
| Testing | pytest | 9.0+ | Fixture-based, conftest.py for shared fixtures |
| Linter/Formatter | ruff | 0.15+ | All-in-one: lint + black-compatible format |
| Type checker | pyright | 1.1+ | Strict mode for src/ |
| Packaging | PyInstaller | 6.19+ | Standalone Windows exe (<30 MB) |
| Package manager | uv | latest | Fast dependency resolution, venv management |

---

## Error Handling Strategy

### Two-Pattern Approach

1. **Raise Immediate (`ProcessingError`):** For single fatal errors that stop the current processing phase. The error contains: `code` (ErrorCode/WarningCode enum), `message` (human-readable with context), `context` (dict with filename, row, column, field_name, etc.).

2. **Collect-Then-Report:** For phases where all problems should be reported at once (e.g., column mapping reports all missing columns, not just the first). Return a result object that includes an `errors: list[ProcessingError]` or return a tuple `(result, list[ProcessingError])`.

### Orchestrator Convention (batch.py)

```python
# Every module call in batch.py follows this pattern:
try:
    result = module_function(args)
    # If result has errors/warnings, collect them
    if hasattr(result, 'errors'):
        file_errors.extend(result.errors)
except ProcessingError as e:
    file_errors.append(e)
    # Short-circuit: skip downstream phases
```

### Phase Short-Circuit Rules

When any ERR occurs in a phase, batch.py:
1. Collects all errors within the CURRENT phase (does not stop mid-phase for collect-then-report modules)
2. Skips ALL downstream phases
3. Jumps directly to status determination (FR-027)
4. This prevents cascading symptom errors while maximizing actionable info per run

Phase order: (1) Sheet Detection, (2) Column Mapping, (3) Extraction, (4) Weight Allocation, (5) Output.

### ConfigError vs ProcessingError

- `ConfigError`: Raised during startup config loading (FR-002). Fatal -- causes exit code 2. Never caught by per-file processing.
- `ProcessingError`: Raised during per-file processing. Caught by batch.py, recorded in FileResult, does not abort the batch.

### Warning Handling

Warnings (ATT_xxx) are `ProcessingError` instances with `WarningCode` instead of `ErrorCode`. They are collected alongside errors but do not trigger short-circuit. They cause "Attention" status only when no errors exist.

---

## Logging Pattern

### Dual-Output Configuration

| Target | Format | Levels | Handler |
|--------|--------|--------|---------|
| Console (stdout) | `[{LEVEL}] {message}` | INFO, WARNING, ERROR | StreamHandler |
| File (`process_log.txt`) | `[{HH:MM}] [{LEVEL}] {message}` | DEBUG, INFO, WARNING, ERROR | FileHandler |

### Logger Usage Convention

Every module uses:
```python
import logging
logger = logging.getLogger(__name__)
```

No module configures logging directly. Only `logger.py` calls `logging.basicConfig()` or creates handlers. All other modules just call `logger.info()`, `logger.warning()`, `logger.error()`, `logger.debug()`.

### Error/Warning Log Format

```python
# Errors: always include code and context
logger.error("[%s] %s: %s", error.code.value, error.code.name, error.message)

# Warnings: same format with WARNING level
logger.warning("[%s] %s: %s", warning.code.value, warning.code.name, warning.message)

# Debug: cell-level detail for diagnostic mode
logger.debug("Row %d, Col %d: raw='%s', parsed=%s", row, col, raw_value, parsed_value)
```

### Diagnostic Mode

`--diagnostic` sets console handler to DEBUG level. Single-file processing with maximum verbosity. Same log format, just more output to console.

---

## Conventions

### File & Naming

| Element | Convention | Example |
|---------|------------|---------|
| Source files | snake_case | `weight_alloc.py`, `extract_invoice.py` |
| Test files | `test_` prefix + source name | `test_weight_alloc.py` |
| Functions | snake_case | `detect_header_row()`, `allocate_weights()` |
| Classes/Models | PascalCase | `InvoiceItem`, `PackingTotals`, `MergeTracker` |
| Constants | UPPER_SNAKE_CASE | `MAX_SCAN_ROW`, `HEADER_KEYWORDS` |
| Config keys | snake_case | `invoice_sheet`, `part_no` |
| Error codes | ERR_NNN / ATT_NNN | `ERR_020`, `ATT_003` |
| Private functions | `_` prefix | `_extract_total_packets()`, `_detect_implicit_total()` |

### Code Style

- **PEP 8** compliance enforced by ruff
- **Type hints** on all function signatures using Python 3.11+ syntax (`X | None`, not `Optional[X]`)
- **Google-style docstrings** on every public function:
  ```python
  def detect_header_row(sheet: Worksheet, sheet_type: str, config: AppConfig) -> int:
      """Detect the header row position by scanning for non-empty cell density.

      Args:
          sheet: The worksheet to scan.
          sheet_type: Either "invoice" or "packing".
          config: Application configuration with field patterns.

      Returns:
          The 1-based row number of the detected header row.

      Raises:
          ProcessingError: ERR_014 if no row meets the threshold.
      """
  ```
- **Black-compatible formatting** via `ruff format`
- **Max file length:** 500 lines. If approaching, split into sub-modules.
- **Imports:** stdlib first, then third-party, then local. One import per line for local modules.

### Numeric Precision

- **All monetary/weight calculations use `Decimal`**, never `float`
- **Rounding method:** `ROUND_HALF_UP` everywhere (0.5 always rounds up)
- **Epsilon trick:** `round(value * 10^decimals + 1e-9) / 10^decimals` to handle floating-point representation issues (e.g., 2.28 stored as 2.2799999...)
- **Precision rules by field:**

| Field | Precision | Source |
|-------|-----------|--------|
| qty (invoice) | Cell display precision | FR-011 |
| price (invoice) | 5 decimals | FR-011 |
| amount (invoice) | 2 decimals | FR-011 |
| qty (packing) | Cell display precision | FR-012 |
| nw (packing per-item) | 5 decimals | FR-012 |
| total_nw | Cell format precision (min 2, max 5) | FR-015 |
| total_gw | Cell format precision | FR-016 |
| packing weight (allocated per-part) | total_nw precision N or N+1 | FR-023, FR-024 |
| invoice weight (allocated per-item) | packing precision + 1 | FR-025 |

### Pydantic Model Convention

- All data entities are pydantic `BaseModel` subclasses
- Use `model_config = ConfigDict(arbitrary_types_allowed=True)` if storing openpyxl objects
- Decimal fields use `Decimal` type directly (pydantic v2 supports it)
- Optional fields use `X | None = None` pattern
- Field names match PRD entity definitions exactly (except `model` which becomes `model_no` to avoid pydantic conflict)

### Import Rules

- Cross-module calls go through exported public interfaces only
- No circular imports (import graph is acyclic by design)
- `batch.py` is the only module that imports from all other modules
- No module imports from `batch.py` or `cli.py` (they are consumers, not providers)

### CLI Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All files processed as Success or Attention |
| 1 | One or more files Failed (any ERR_xxx) |
| 2 | Fatal startup error (config missing, permissions, bad arguments) |

---

## Side-Effect Rules

1. **Excel file reads:** Only `batch.py` opens workbooks via openpyxl/xlrd. All other modules receive `Worksheet` objects as parameters.
2. **Output file writes:** Only `output.py` writes to disk (via `write_template()`). `batch.py` constructs the output path and passes it in.
3. **Directory creation/deletion:** Only `batch.py` creates `data/` and `data/finished/` directories (FR-001) and clears `data/finished/` (FR-028).
4. **Console/file logging:** Only `logger.py` configures logging handlers. All other modules use `logging.getLogger(__name__)`.
5. **Config file reads:** Only `config.py` reads configuration files from disk. All other modules receive `AppConfig` as a parameter.
6. **No module writes to input files.** All input Excel files are read-only.
7. **No network access.** No HTTP calls, no telemetry, no update checks.

---

## Test Requirements

### Coverage Targets

- **3-5 test cases per public function** covering: happy path, edge case, error case
- **Minimum test structure per function:**
  1. Happy path: normal input produces expected output
  2. Edge case: boundary conditions, empty inputs, minimal valid inputs
  3. Error case: invalid input triggers expected error code
  4. (Optional) Edge case #2: unusual but valid input (e.g., Unicode, merged cells, maximum-length values)
  5. (Optional) Regression case: specific vendor file pattern that caused a previous bug

### Test Fixture Strategy

| Tier | Fixture Type | Source | Speed |
|------|-------------|--------|-------|
| Unit | In-memory workbooks via `make_workbook()` factory | Created in conftest.py | Fast |
| Component | Small purpose-built .xlsx files | `tests/fixtures/` | Medium |
| Integration | Full 41-file vendor corpus | `tests/fixtures/` (copied from `data/`) | Slow |

### conftest.py Required Fixtures

```python
@pytest.fixture
def app_config() -> AppConfig:
    """Load AppConfig from test config files."""

@pytest.fixture
def make_workbook() -> Callable:
    """Factory: create minimal in-memory workbooks with specified sheets, headers, data."""

@pytest.fixture
def tmp_output_dir(tmp_path: Path) -> Path:
    """Temporary output directory for write tests."""
```

### Test Naming Convention

```python
def test_<function_name>_<scenario>():
    """Test <function_name> when <scenario description>."""
```

Example:
```python
def test_detect_header_row_invoice_threshold_met()
def test_detect_header_row_no_qualifying_row()
def test_detect_header_row_tier0_beats_tier1()
```

### High-Risk Test Areas (minimum case counts)

| Module | Function | Min Cases | Key Scenarios |
|--------|----------|-----------|---------------|
| weight_alloc | `allocate_weights()` | 15 | Exact match at N, match at N+1, remainder adjustment, zero-check escalation, epsilon edges, single part, many parts, part not found |
| merge_tracker | `MergeTracker` | 10 | Horizontal merge, vertical merge, data-area vs header-area, weight first-row-only, string propagation, nested ranges |
| column_map | `detect_header_row()` | 8 | Tier-0 wins, tier-1 wins, tie-breaking by row, metadata row filtered, data-like row demoted, packing threshold vs invoice threshold |
| column_map | `map_columns()` | 8 | All required found, missing required, sub-header fallback, currency data-row fallback, two-currency-column shift |
| extract_packing | `extract_packing_items()` | 10 | Normal extraction, implicit continuation, ditto marks, merged part_no propagation, stop at keyword, stop at blank, stop at implicit total, merged NW first-row-only, header continuation skip |
| extract_invoice | `extract_invoice_items()` | 8 | Normal extraction, COO/COD fallback, stop at empty+qty0, stop at total keyword, stop at footer, header continuation filter, unit suffix stripping |

---

## Known Gotchas

### 1. openpyxl Merged Cell Behavior

After calling `sheet.unmerge_cells()`, openpyxl sets non-anchor cells to `None`. The `MergeTracker` must capture merge ranges BEFORE unmerging, then provide value propagation via `get_anchor_value()`. Without this, all non-anchor cells lose their data.

### 2. openpyxl `data_only=True` Limitation

When opening with `data_only=True`, openpyxl returns the cached formula result, not the formula itself. If the file was never opened in Excel (never calculated), formula cells return `None`. All test fixture files should have been opened/saved in Excel at least once.

### 3. xlrd vs openpyxl Interface Mismatch

xlrd's `Book`/`Sheet` objects have a completely different API from openpyxl's `Workbook`/`Worksheet`. Key differences:
- xlrd uses 0-based row/col indexing; openpyxl uses 1-based
- xlrd has no `merged_cells` ranges attribute in the same format
- xlrd cells have type codes (XL_CELL_EMPTY, XL_CELL_TEXT, etc.) instead of Python types
- **Solution needed:** Either create an adapter layer in `batch.py` that converts xlrd to openpyxl-compatible objects, or use openpyxl for both (converting .xls to .xlsx in memory via xlrd read + openpyxl write).

### 4. Floating-Point Artifacts in Excel

Values like `2.2800000000000002` are common in Excel files read by openpyxl. Always convert to `Decimal(str(value))` (not `Decimal(value)`) to avoid inheriting the float artifact. The `str()` conversion rounds to Python's default float repr, which is usually correct.

### 5. openpyxl `number_format` Parsing

Cell `number_format` can be complex: `'_($* #,##0.00_)'`, `'0.00000_'`, `'General'`, `'@'` (text). The precision detection function must handle all of these. Key patterns:
- Count digits after the decimal point in the format string
- `General` format: round to 5 decimals, strip trailing zeros
- `@` format (text): the value is stored as string, need special handling

### 6. Unicode in Cell Values

Chinese characters are common in headers, part numbers, and data values. All string comparisons must handle Unicode correctly:
- Sheet names may contain Chinese characters mixed with English
- Header cells may have Chinese column names
- Part numbers and brand names are often Chinese
- Ditto marks include Unicode characters (U+3003, U+201C, U+201D)

### 7. Third-Party Type-Stub Gaps

- **openpyxl:** No official type stubs. `pyright` may report errors on `Worksheet.cell()`, `merged_cells.ranges`, etc. Use `# type: ignore[attr-defined]` sparingly, or install `openpyxl-stubs` if available.
- **xlrd:** Limited type stubs. Similar `# type: ignore` may be needed.
- **PyYAML:** Has stubs but `yaml.safe_load()` returns `Any`. Explicit type narrowing needed after load.

### 8. Cross-Extraction Consistency

Functions extracting values that will be compared downstream must use identical precision and normalization:
- **part_no matching (invoice vs packing):** Both must strip whitespace identically before comparison in weight_alloc.py
- **Decimal precision:** All weight values must use the same rounding method (ROUND_HALF_UP with epsilon trick)
- **String normalization for lookup:** Currency and country values must be normalized identically in both extraction (raw value) and transformation (lookup key)

### 9. Windows Path Handling

- All file paths should use `pathlib.Path` for cross-platform compatibility
- The exe runs on Windows 10+ where paths may contain Chinese characters, spaces, and parentheses
- Config paths: `config/field_patterns.yaml` is relative to the executable location
- Use `Path(__file__).parent.parent.parent` or similar to find the project root from source modules

### 10. PyInstaller Executable Size

The 30 MB budget is tight. Exclude unused stdlib modules:
```python
excludes = ['tkinter', 'unittest', 'email', 'html', 'http', 'xml.etree',
            'pydoc', 'doctest', 'asyncio', 'multiprocessing', 'concurrent', 'xmlrpc']
```
Run an early size spike build after Batch 1 to validate.

### 11. Empty String vs None Distinction

In pydantic models, distinguish between "field not present" (`None`) and "field present but empty" (`""`). Convention:
- Optional fields use `str | None = None` (None = field not applicable/not found)
- Required fields use `str` (empty string = extracted but empty, triggers ERR_030)
- Numeric optional fields: `Decimal | None = None`

### 12. Row Number Off-by-One

openpyxl uses 1-based row/column indexing. All internal row references (header_row, last_data_row, total_row) are 1-based. When iterating with `sheet.iter_rows()`, the `min_row` and `max_row` parameters are inclusive and 1-based.

---

## Index Convention Table

| Data Structure | Index Base | Context | Conversion Pattern |
|---------------|-----------|---------|-------------------|
| openpyxl Worksheet rows | 1-based | `sheet.cell(row=r, column=c)` | Direct use -- no conversion needed |
| openpyxl Worksheet columns | 1-based | `sheet.cell(row=r, column=c)` | Direct use -- no conversion needed |
| ColumnMapping.field_map values | 1-based | Column index from openpyxl header scan | Direct use with `sheet.cell(row=r, column=col_idx)` |
| ColumnMapping.header_row | 1-based | Row number from openpyxl scan | Direct use |
| ColumnMapping.effective_header_row | 1-based | May be header_row or header_row+1 | Data starts at `effective_header_row + 1` |
| MergeRange (min_row, max_row, min_col, max_col) | 1-based | Stored from openpyxl `merged_cells.ranges` | Direct use with openpyxl cell access |
| `last_data_row` from extract_packing | 1-based | Row number of last extracted packing item | Total row search starts at `last_data_row + 1` |
| xlrd Sheet rows | 0-based | `sheet.cell_value(rowx, colx)` | `openpyxl_row = xlrd_row + 1`, `openpyxl_col = xlrd_col + 1` |
| xlrd Sheet columns | 0-based | `sheet.cell_value(rowx, colx)` | `openpyxl_col = xlrd_col + 1` |
| Python list indices (packing_items, invoice_items) | 0-based | Internal iteration | No conversion needed (not used as cell references) |
| Output template data start row | 1-based | Row 5 (rows 1-4 are template headers) | `output_sheet.cell(row=5 + item_index, column=col)` |

---

## Data Representation Consistency Table

This table documents every field/column that the PRD says can appear in an alternative representation. ALL readers of these fields must handle all listed representations, even if the alternative was documented in a different FR.

| Field | Primary Representation | Alternative Representation(s) | Documented In | Must Also Handle In |
|-------|----------------------|------------------------------|---------------|---------------------|
| NW (packing per-item) | Numeric cell value (float/int) | (a) Merged cell -- only anchor row has value, non-anchor = None after unmerge (FR-010); (b) Ditto mark characters: `"`, `〃`, `"`, `"` meaning "same carton as above" (FR-012); (c) Value with embedded unit suffix: "2.5 KGS" (FR-012); (d) Empty cell in implicit continuation rows (FR-012) | FR-010, FR-012 | extract_packing.py (extraction), weight_alloc.py (aggregation must not re-read cells) |
| QTY (packing) | Numeric cell value | (a) Merged cell -- non-anchor = None (FR-010, FR-012); (b) Empty in implicit continuation rows (FR-012); (c) Value with unit suffix: "100 PCS" (FR-012) | FR-010, FR-012 | extract_packing.py |
| NW (total row) | Numeric cell value | (a) Value with embedded unit suffix: "15.5 KG" (FR-015); (b) Cell with complex number_format: `0.00000_`, `#,##0.00` (FR-015); (c) General format with trailing float artifacts (FR-015) | FR-015 | extract_packing.py (extract_totals) |
| GW (total row) | Numeric cell value | (a) Same as total NW alternatives (FR-016); (b) Packaging weight addition: actual GW may be at total_row+2, not total_row (FR-016) | FR-016 | extract_packing.py (extract_totals) |
| part_no (packing) | String cell value | (a) Vertically merged across multiple rows -- non-anchor = None (FR-012); (b) May need propagation from merge anchor (FR-012) | FR-012 | extract_packing.py, weight_alloc.py (matching must use propagated values) |
| part_no (invoice) | String cell value | (a) May contain "part no" as header continuation row (FR-011) -- must be filtered, not extracted | FR-011 | extract_invoice.py |
| brand + brand_type (invoice) | Separate column values | (a) Horizontally merged across adjacent columns (e.g., L21:M21) -- non-anchor column = None after unmerge (FR-010); anchor value must propagate to both fields | FR-010 | extract_invoice.py |
| currency (invoice) | Dedicated currency column | (a) No column -- embedded in data cells of price/amount columns (FR-008 data-row fallback); when detected, price/amount column shifts +1 | FR-008 | column_map.py (fallback detection), extract_invoice.py (must use shifted column index) |
| COO (invoice) | Dedicated COO column value | (a) Empty -- use COD column value as fallback (FR-011) | FR-011 | extract_invoice.py |
| inv_no (invoice) | (a) Column in data table | (b) Header area rows 1-15 via pattern/label extraction (FR-009); (c) Value may have "INV#" or "NO." prefix that needs stripping | FR-008, FR-009, FR-011 | column_map.py (header extraction), extract_invoice.py (column extraction + cleaning), batch.py (orchestration) |
| Target_Code (country_rules) | Integer cell value | (a) String cell value -- 3 entries stored as string instead of int (Section 7) | FR-019, Section 7 | config.py (must normalize all to str), transform.py (lookup uses normalized keys) |
| Header cells | Single-row text | (a) Multi-line: embedded newlines `\n`, tabs `\t` (FR-008); (b) Two-row merged header spanning sub-columns (FR-008); (c) "Unnamed:" prefix from library artifacts (FR-007) | FR-007, FR-008 | column_map.py |
| Numeric values (general) | Python float from openpyxl | (a) Floating-point artifacts: 2.2800000000000002 (Section 7); (b) Integer stored as float: 91600.0 from .xls (Section 7); (c) String with unit suffix: "15 KG" | FR-011, FR-012, FR-015 | All extraction modules, utils.py (safe_decimal, strip_unit_suffix) |
| po_no (invoice) | Raw string from cell | (a) Contains suffix after `-`, `.`, `/` that must be stripped (FR-020); (b) Delimiter at position 0 (e.g., "-PO12345") -- preserve original | FR-020 | transform.py (cleaning), extract_invoice.py (raw extraction only) |

---

## Platform-Specific Considerations

### Windows 10+ Target

- **File paths:** Chinese characters, spaces, and parentheses in filenames are common (e.g., `中磊(蘇州)AVT251216A-074.xlsx`). Use `pathlib.Path` everywhere.
- **Console encoding:** Windows console may not display Chinese characters correctly by default. Use `sys.stdout.reconfigure(encoding='utf-8')` or `chcp 65001` equivalent.
- **File locking:** Windows locks files opened by other processes. `openpyxl.load_workbook()` will raise `PermissionError` or similar. Detect at scan time (FR-003).
- **Temp files:** Excel creates `~$filename.xlsx` temp files when a file is open. These must be excluded (FR-003).
- **Hidden files:** Files with the hidden attribute must be excluded. Check via `os.stat()` and `stat.FILE_ATTRIBUTE_HIDDEN` on Windows.
- **Line endings:** Output log files use platform-native line endings (CRLF on Windows).
- **Executable path:** PyInstaller `sys._MEIPASS` for bundled resources; `Path(sys.executable).parent` for config directory resolution.

---

## Subagent Constraints

These universal implementation rules apply to all subagents building modules from spec files.

### No Stubs Rule
- Every function body must be fully implemented. No `raise NotImplementedError`, no `pass` as function body, no `TODO:IMPLEMENT` placeholders.
- If a function cannot be fully implemented due to missing dependencies from a different batch, it should not exist yet. Batch ordering ensures all dependencies are available.

### No Type Redefinition
- Never redefine types, classes, or enums that already exist in `models.py` or `errors.py`. Import them.
- Never create local dataclasses or TypedDicts that duplicate pydantic models.
- If you need a new type, check models.py first. If it should exist there, add it to models.py, not to your module.

### No New Dependencies
- Do not add any package not listed in the Build Config or architecture technology stack.
- stdlib modules are always allowed.
- If you think a new dependency is needed, flag it as an ambiguity -- do not install it.

### No Cross-Module Mocking
- Unit tests mock only the current module's dependencies, never internal functions of the module under test.
- Use `unittest.mock.patch` targeting the import path in the module under test (e.g., `patch('autoconvert.transform.logger')` not `patch('autoconvert.logger.setup_logging')`).
- For integration tests, use real objects (real AppConfig, real workbooks).

### Fixture Scoping
- `conftest.py` fixtures at `session` scope: `app_config` (expensive to load, immutable).
- `conftest.py` fixtures at `function` scope: `make_workbook`, `tmp_output_dir` (mutable, must be fresh per test).
- Never use `module` scope for fixtures that create mutable state.

### Singleton Teardown
- If any module uses module-level singletons (e.g., compiled regex cache, logging handlers), tests must reset them in fixtures or teardown.
- The `logger.py` module configures global logging handlers. Tests should use `caplog` fixture instead of checking stdout directly.

### Dictionary Key Lookups
- Dictionary key lookups must use exact casing from the definition source.
- Config keys from `field_patterns.yaml` are lowercase snake_case (e.g., `invoice_columns`, `part_no`).
- Lookup table keys (`currency_lookup`, `country_lookup`) are normalized via `normalize_lookup_key()` -- always uppercase after normalization.
- Error code enum values match PRD exactly (e.g., `ERR_001`, not `err_001`).

### Parse/Conversion Error Wrapping
- Wrap ALL parse/conversion calls for user-supplied data in try/except.
- Cell values from Excel can be: None, str, int, float, datetime, bool. Never assume a specific type.
- Numeric parsing: `try: Decimal(str(value)) except (InvalidOperation, TypeError, ValueError)` -> raise ProcessingError with ERR_031.
- String parsing: `try: str(value).strip() except (TypeError, AttributeError)` -> treat as empty string.
- Fields with optional or polymorphic content (e.g., total_packets which can be int, float-as-int, or string) may contain unexpected types. Always validate before use.

### Test Output Assertions
- Test assertions must compare against concrete expected values, not just "is not None" or "len > 0".
- Decimal comparisons use `==` with exact Decimal values (e.g., `assert result == Decimal('2.28')`, not `assert abs(result - 2.28) < 0.01`).
- Error code assertions check the specific code: `assert error.code == ErrorCode.ERR_020`, not just `assert isinstance(error, ProcessingError)`.

### No Silent Failures
- Every function that can fail must either raise an exception or return an error indicator that the caller checks.
- Never use bare `except:` or `except Exception:` without re-raising or recording the error.
- If a non-critical operation fails (e.g., logging), log at WARNING level and continue -- but never silently swallow the error.

### Import Discipline
- Only import from modules in earlier batches or the same batch (if no dependency between them).
- Never import from `batch.py` or `cli.py` in any other module.
- Use relative imports within the `autoconvert` package: `from .models import InvoiceItem`, not `from autoconvert.models import InvoiceItem`.
