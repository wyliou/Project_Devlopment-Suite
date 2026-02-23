# Build Plan - AutoConvert

> Generated: 2026-02-20
> PRD: docs/PRD.md
> Architecture: docs/architecture.md

---

## PRD Format Notes

- **FR identifier scheme:** `FR-NNN` (zero-padded 3-digit, e.g., FR-001 through FR-034)
- **FR fields:** Input, Rules, Output, Error; optional Depends field present on ~60% of FRs
- **Grouping:** FRs grouped under capability headings: Batch Processing, Sheet Detection, Column Mapping, Data Extraction, Data Transformation, Weight Allocation, Validation, Output Generation, Logging & Reporting, Diagnostics
- **Priority information:** No explicit Must/Should/Could per FR; MVP scope lists 11 capability areas in priority order; success metrics provide implicit ranking (Fail-Safe Trust = primary)
- **Warning/Error codes:** ERR_xxx (Failed status) and ATT_xxx (Attention status) with full catalog in Section 7

---

## 1. Build Config

| Key | Value |
|-----|-------|
| language | python |
| package_manager | uv |
| test_command | `uv run pytest tests/ --tb=short` |
| lint_command | `uv run ruff check src/ --fix` |
| lint_tool | ruff |
| type_check_command | `uv run pyright src/` |
| type_check_tool | pyright |
| run_command | `uv run python -m autoconvert` |
| stub_detection_pattern | `raise NotImplementedError` |
| src_dir | `src/autoconvert/` |
| test_dir | `tests/` |
| format_command | `uv run ruff format src/` |
| format_tool | _(omit — ruff handles both linting and formatting)_ |

---

## 2. Gate Configuration

| Gate | Active | Reason if disabled |
|------|--------|--------------------|
| stub_detection | yes | |
| lint | yes | |
| type_check | yes | pyright configured for Python 3.11+ |
| format | yes | ruff format (separate from lint) |
| integration_tests | yes | 41-file vendor corpus in `data/` |
| simplification | yes | 5 batches — simplification pass worthwhile |
| validation | yes | 41 vendor Excel files available in `data/` for real-data validation |

---

## 3. Project Summary

| Item | Detail |
|------|--------|
| PRD path | `docs/PRD.md` |
| Architecture path | `docs/architecture.md` |
| Config dir | `config/` (field_patterns.yaml, output_template.xlsx, currency_rules.xlsx, country_rules.xlsx) |
| Source dir | `src/autoconvert/` (does not exist yet — greenfield) |
| Test dir | `tests/` (does not exist yet — greenfield) |
| Test corpus | `data/` — 41 vendor Excel files (40 .xlsx + 1 .xls) |
| Golden outputs | `data/finished/` — existing template outputs (potential golden files for NFR-REL-001) |
| Stack | Python 3.11+, openpyxl 3.1.5, xlrd 2.0.2, PyYAML 6.0.3, pydantic 2.12+, ruff, pyright, pytest, PyInstaller |
| Product type | CLI tool, standalone Windows executable (<30 MB) |
| Existing code | None — fully greenfield. No pyproject.toml, no src/, no tests/ |
| Conventions | See build-context.md |

---

## 4. FR to Subsystem Map

### Batch Processing
- **FR-001**: batch.py — `data/` and `data/finished/` directories exist and are writable after startup
- **FR-002**: config.py — all config files loaded, regex compiled, lookup tables parsed, template validated with no ERR_001-005
- **FR-003**: batch.py — ordered list of `.xlsx`/`.xls` files queued; temp/hidden/locked files excluded; each file independent

### Sheet Detection
- **FR-004**: sheet_detect.py — invoice sheet identified by regex match on sheet name
- **FR-005**: sheet_detect.py — packing sheet identified by regex match on sheet name
- **FR-006**: sheet_detect.py — both Invoice and Packing sheets confirmed present before proceeding

### Column Mapping
- **FR-007**: column_map.py — header row number detected via non-empty cell density with three-tier priority
- **FR-008**: column_map.py — all required columns mapped by regex; sub-header fallback and currency data-row fallback applied
- **FR-009**: column_map.py — invoice number extracted from header area rows 1-15 as fallback

### Data Extraction
- **FR-010**: merge_tracker.py — all merged cells captured, unmerged, and values propagated per field-type rules
- **FR-011**: extract_invoice.py — 13 per-item fields extracted with correct precision, stop conditions, and COO/COD fallback
- **FR-012**: extract_packing.py — packing items extracted with implicit continuation, ditto marks, merged part_no propagation
- **FR-013**: extract_packing.py — merged weight cells validated (same part_no OK, different part_no = ERR_046)
- **FR-014**: extract_totals.py — total row detected via keyword or implicit strategy
- **FR-015**: extract_totals.py — total_nw extracted with visible precision from cell format
- **FR-016**: extract_totals.py — total_gw extracted with packaging weight addition check (+1/+2 rows)
- **FR-017**: extract_totals.py — total_packets extracted via multi-priority search (optional field)

### Data Transformation
- **FR-018**: transform.py — currency codes converted to numeric customs codes via lookup
- **FR-019**: transform.py — country codes/names converted to numeric customs codes via lookup
- **FR-020**: transform.py — PO numbers cleaned by stripping suffixes after `-`, `.`, `/`

### Weight Allocation
- **FR-021**: weight_alloc.py — packing weights aggregated by part_no; all non-zero validated
- **FR-022**: weight_alloc.py — packing weight sum vs total_nw within 0.1 threshold
- **FR-023**: weight_alloc.py — optimal rounding precision determined (N to N+1, zero-check escalation)
- **FR-024**: weight_alloc.py — part weights rounded with remainder correction for exact sum
- **FR-025**: weight_alloc.py — weights proportionally allocated to invoice items by qty ratio
- **FR-026**: weight_alloc.py — final validation: allocated sum equals total_nw

### Validation
- **FR-027**: validate.py — file status determined: any ERR = Failed, any ATT (no ERR) = Attention, else Success

### Output Generation
- **FR-028**: batch.py — `data/finished/` cleared before batch processing
- **FR-029**: output.py — 40-column template populated per column mapping (A-AN); only for Success/Attention files
- **FR-030**: output.py — output file saved as `{input_filename}_template.xlsx`

### Logging & Reporting
- **FR-031**: logger.py — real-time per-file console output with milestones, errors, warnings, final status
- **FR-032**: logger.py — detailed `process_log.txt` with `[HH:MM] [LEVEL]` format including DEBUG
- **FR-033**: report.py — batch summary: total/success/attention/failed counts, failed file details, attention file details

### Diagnostics
- **FR-034**: cli.py + batch.py — `--diagnostic <filename>` processes single file with DEBUG-level console output

---

## 5. Side-Effect & Validation Ownership

### Side-Effect Ownership

| Side Effect | Owner Module | Non-owners Must |
|-------------|-------------|-----------------|
| Excel file reads (openpyxl/xlrd) | batch.py | Receive workbook/sheet object as parameter |
| Output file writes | output.py | Call `output.write_template()` |
| Directory creation (`data/`, `data/finished/`) | batch.py | Not create directories |
| Directory clearing (`data/finished/`) | batch.py | Not delete files |
| Console logging | logger.py | Use `logging.getLogger(__name__)` |
| File logging (`process_log.txt`) | logger.py | Use `logging.getLogger(__name__)` |
| Config file reads | config.py | Call `config.load_config()` |

### Validation Ownership

Each validation rule is owned by exactly one module. Non-owners must NOT duplicate these checks.

| Validation | Error Code | Owning Module | Non-Owner Exclusion List |
|------------|-----------|---------------|--------------------------|
| Config file existence | ERR_001 | config.py | batch.py, cli.py |
| Regex compilation | ERR_002 | config.py | column_map.py, sheet_detect.py |
| Duplicate lookup Source_Value | ERR_003 | config.py | transform.py |
| Config structure validity | ERR_004 | config.py | batch.py |
| Template structure validity | ERR_005 | config.py | output.py |
| File locked detection | ERR_010 | batch.py | — |
| File corruption detection | ERR_011 | batch.py | — |
| Invoice sheet presence | ERR_012 | sheet_detect.py | batch.py, column_map.py |
| Packing sheet presence | ERR_013 | sheet_detect.py | batch.py, column_map.py |
| Header row detection | ERR_014 | column_map.py | extract_invoice.py, extract_packing.py |
| Required column presence | ERR_020 | column_map.py | extract_invoice.py, extract_packing.py |
| Invoice number existence | ERR_021 | column_map.py (fallback) + batch.py (orchestration) | extract_invoice.py |
| Required field empty in data row | ERR_030 | extract_invoice.py, extract_packing.py (each owns its sheet) | weight_alloc.py, transform.py |
| Invalid numeric value | ERR_031 | extract_invoice.py, extract_packing.py (each owns its sheet) | weight_alloc.py |
| Total row detection | ERR_032 | extract_packing.py | weight_alloc.py |
| Total NW validity | ERR_033 | extract_packing.py | weight_alloc.py |
| Total GW validity | ERR_034 | extract_packing.py | weight_alloc.py |
| Invoice part not in packing | ERR_040 | weight_alloc.py | extract_invoice.py, extract_packing.py |
| Weight allocation sum mismatch | ERR_041 | weight_alloc.py | output.py |
| Packing part zero NW | ERR_042 | weight_alloc.py | extract_packing.py |
| Packing part not in invoice | ERR_043 | weight_alloc.py | extract_invoice.py |
| Weight rounds to zero | ERR_044 | weight_alloc.py | — |
| Zero quantity for part | ERR_045 | weight_alloc.py | extract_packing.py |
| Different parts share merged weight | ERR_046 | extract_packing.py | weight_alloc.py, merge_tracker.py |
| Aggregate disagrees with total | ERR_047 | weight_alloc.py | extract_packing.py |
| Final weight validation failed | ERR_048 | weight_alloc.py | output.py |
| Template load failure | ERR_051 | output.py | config.py (config validates structure, output validates load at write time) |
| Output write failure | ERR_052 | output.py | batch.py |
| Missing total packets | ATT_002 | extract_packing.py | output.py, report.py |
| Unstandardized currency | ATT_003 | transform.py | output.py (passes raw value through) |
| Unstandardized COO | ATT_004 | transform.py | output.py (passes raw value through) |

### Field Population Map (for batch.py orchestrator)

This maps every validated required field to ALL sources that can populate or modify it, and the pipeline step where population occurs.

| Field | Population Source(s) | Pipeline Step | Validation After |
|-------|---------------------|---------------|------------------|
| inv_no | (1) Column extraction from invoice data table (FR-011) | Step 3: Extraction | After extraction |
| | (2) Header area fallback extraction rows 1-15 (FR-009) | Step 2b: Column Mapping fallback | After extraction |
| | (3) Prefix cleaning: strip "INV#", "NO." (FR-009, FR-011) | Step 3: Extraction | After extraction |
| currency | (1) Column extraction from invoice (FR-011) | Step 3: Extraction | After transformation |
| | (2) Data-row fallback scan if no currency column (FR-008) | Step 2: Column Mapping | After transformation |
| | (3) Lookup conversion to numeric code (FR-018) | Step 4: Transformation | After transformation (ATT_003 if no match) |
| coo | (1) Column extraction from invoice (FR-011) | Step 3: Extraction | After transformation |
| | (2) COD fallback when COO is empty (FR-011) | Step 3: Extraction | After transformation |
| | (3) Lookup conversion to numeric code (FR-019) | Step 4: Transformation | After transformation (ATT_004 if no match) |
| po_no | (1) Column extraction from invoice (FR-011) | Step 3: Extraction | After transformation |
| | (2) Suffix cleaning: strip after `-`, `.`, `/` (FR-020) | Step 4: Transformation | After transformation |
| allocated_weight | (1) Packing NW aggregation by part_no (FR-021) | Step 5: Weight Allocation | After allocation (FR-026) |
| | (2) Precision determination and rounding (FR-023, FR-024) | Step 5: Weight Allocation | After allocation |
| | (3) Proportional allocation by qty ratio (FR-025) | Step 5: Weight Allocation | After allocation |
| | (4) Remainder correction on last item (FR-025) | Step 5: Weight Allocation | After final validation (FR-026) |
| total_gw | (1) Total row GW cell (FR-016) | Step 3: Extraction | After extraction |
| | (2) Packaging weight addition: +2 row override when +1 and +2 both numeric (FR-016) | Step 3: Extraction | After extraction |
| total_packets | (1) Priority 1: 件数/件數 label search (FR-017) | Step 3: Extraction | After extraction (ATT_002 if not found) |
| | (2) Priority 2: PLT.G indicator (FR-017) | Step 3: Extraction | After extraction |
| | (3) Priority 3: Below-total patterns (FR-017) | Step 3: Extraction | After extraction |
| part_no (packing) | (1) Column extraction (FR-012) | Step 3: Extraction | After extraction |
| | (2) Vertical merge propagation when empty (FR-012) | Step 3: Extraction | After extraction |
| nw (packing) | (1) Column extraction (FR-012) | Step 3: Extraction | After merged weight validation (FR-013) |
| | (2) Merged NW: first row only, others = 0.0 (FR-010, FR-012) | Step 3: Extraction | After merged weight validation |
| | (3) Implicit continuation: same part_no = 0.0 (FR-012) | Step 3: Extraction | After merged weight validation |
| | (4) Ditto mark detection: set to 0.0 (FR-012) | Step 3: Extraction | After merged weight validation |

### Detection-Fallback Map

| Field | Primary Detection | Fallback Detection | Sequencing Constraint |
|-------|-------------------|--------------------|-----------------------|
| inv_no | Column mapping via header row regex (FR-008) | Header area rows 1-15 scan with capture/label patterns (FR-009) | Primary returns `None` (not found), does NOT raise ERR_021. ERR_021 fires only after fallback also fails. batch.py orchestrates: try column first, if absent try header fallback, then determine if ERR_021. |
| currency column | Header row regex scan (FR-008) | Data-row scan rows header+1 to header+4 for currency values in data cells (FR-008) | Primary returns incomplete mapping (currency absent). Fallback augments the mapping. ERR_020 for currency fires only after both header and data-row scans complete. column_map.py handles both internally. |
| coo value | COO column extraction (FR-011) | COD column value when COO is empty (FR-011) | Primary returns empty string for the row. Fallback reads COD value for that same row. extract_invoice.py handles both internally per row. ERR_030 for COO fires only after COD fallback attempted. |
| total_row | Strategy 1: keyword search in rows after last_data_row (FR-014) | Strategy 2: implicit total detection (empty part_no + numeric NW>0 + GW>0) (FR-014) | Strategy 1 returns `None`. Strategy 2 runs only when Strategy 1 fails. ERR_032 fires after both strategies fail. extract_packing.py handles both internally. |
| total_packets | Priority 1: 件数 label → Priority 2: PLT.G → Priority 3: below-total patterns (FR-017) | Each priority is a fallback for the previous | ATT_002 fires only after all 3 priorities fail. extract_packing.py handles all internally. No hard-fail until all attempted. |
| header_row | Three-tier priority scan rows 7-30 (FR-007) | Sub-header scanning of header_row+1 for unmapped required fields (FR-008) | Primary returns a header row number (never fails to select one if threshold met). Sub-header augments the column mapping, does not replace the header row. ERR_014 fires only if no row meets threshold. |

---

## 6. Shared Utilities

### 1. `strip_unit_suffix(value: str) -> str`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** extract_invoice.py, extract_packing.py, extract_packing.py (totals)
- **Purpose:** Strip KG, KGS, G, LB, LBS, PCS, EA, 件, 个 suffixes from numeric strings before parsing
- **Implementation:** Regex `re.sub(r'\s*(KGS?|LBS?|G|PCS|EA|件|个)\s*$', '', value.strip(), flags=re.IGNORECASE)`

### 2. `safe_decimal(value: Any, decimals: int, rounding: str = ROUND_HALF_UP) -> Decimal`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** extract_invoice.py, extract_packing.py, weight_alloc.py
- **Purpose:** Convert cell value to Decimal with specified precision using ROUND_HALF_UP with epsilon trick
- **Implementation:** `Decimal(str(float(value) * 10**decimals + 1e-9)).to_integral_value() / Decimal(10**decimals)` — wrap in try/except for non-numeric values

### 3. `round_half_up(value: Decimal, decimals: int) -> Decimal`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** weight_alloc.py, extract_packing.py (totals), extract_invoice.py
- **Purpose:** ROUND_HALF_UP rounding with epsilon trick to handle floating-point representation
- **Implementation:** Apply epsilon trick then quantize to `Decimal(10) ** -decimals` with ROUND_HALF_UP

### 4. `normalize_header(value: str) -> str`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** column_map.py (primary header scan, sub-header scan)
- **Purpose:** Normalize header cell text: collapse newlines/tabs/multiple spaces to single space, strip whitespace
- **Implementation:** `re.sub(r'[\n\t]+', ' ', value).strip(); re.sub(r'\s+', ' ', result)`

### 5. `is_stop_keyword(value: str) -> bool`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** extract_invoice.py, extract_packing.py
- **Purpose:** Check if a cell value contains total/合计/总计/小计 (case-insensitive)
- **Implementation:** `re.search(r'(?i)(total|合计|总计|小计)', str(value)) is not None`

### 6. `normalize_lookup_key(value: str) -> str`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** transform.py (currency conversion, country conversion), config.py (lookup table loading)
- **Purpose:** Normalize lookup keys: case-fold, strip whitespace, collapse `, ` to `,`
- **Implementation:** `value.strip().upper().replace(', ', ',')`

### 7. `detect_cell_precision(cell) -> int`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** extract_packing.py (FR-015, FR-016 — total_nw/total_gw precision), extract_invoice.py (FR-011 — qty display precision)
- **Purpose:** Read openpyxl cell's `number_format` and extract decimal place count; handle `General`, `0.00`, `#,##0.00`, `_($* #,##0.00_)` etc.
- **Implementation:** Parse format string for `.` then count `0` or `#` chars after it; General format defaults to 5-decimal clean then normalize trailing zeros

### 8. `DITTO_MARKS: frozenset[str]`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** extract_packing.py (FR-012 ditto mark detection)
- **Purpose:** Set of recognized ditto mark characters
- **Implementation:** `frozenset({'"', '\u3003', '\u201C', '\u201D'})`

### 9. `FOOTER_KEYWORDS: tuple[str, ...]`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** extract_invoice.py (FR-011 stop conditions)
- **Purpose:** Footer keywords that indicate end of invoice data
- **Implementation:** `('报关行', '有限公司')`

### 10. `HEADER_KEYWORDS: frozenset[str]`

- **Placement:** `src/autoconvert/utils.py`
- **Consumers:** column_map.py (FR-007 header row detection tier classification)
- **Purpose:** Keywords that indicate a row is a true header row for tier-0 classification
- **Implementation:** `frozenset({'qty', 'n.w.', 'g.w.', 'part no', 'amount', 'price', 'quantity', 'weight', '品牌', '料号', '数量', '单价', '金额', '净重', '毛重', '原产', 'country', 'origin', 'brand', 'model', 'description', 'unit', 'currency', 'coo'})`

---

## 7. Batch Plan

**Total modules:** 18 (models, errors, logger, utils, config, merge_tracker, xls_adapter, sheet_detect, column_map, extract_invoice, extract_packing, extract_totals, transform, weight_alloc, validate, output, report, batch+cli+__main__)
**Target batches:** ceil(18 / 6) = 3 batches minimum. Using 5 batches for dependency ordering.

### Batch 1: Foundation (no dependencies)

| Module | Path | Test Path | FRs | Complexity | Imports |
|--------|------|-----------|-----|------------|---------|
| models | `src/autoconvert/models.py` | `tests/test_models.py` | — | moderate | pydantic |
| errors | `src/autoconvert/errors.py` | `tests/test_errors.py` | — | simple | — |
| logger | `src/autoconvert/logger.py` | — | FR-031, FR-032 | simple | logging (stdlib) |
| utils | `src/autoconvert/utils.py` | `tests/test_utils.py` | — | moderate | re, decimal (stdlib) |

**Exports Table:**

| Module | Function/Class | Signature | Return Type |
|--------|---------------|-----------|-------------|
| models | `InvoiceItem` | pydantic model: part_no: str, po_no: str, qty: Decimal, price: Decimal, amount: Decimal, currency: str, coo: str, cod: str, brand: str, brand_type: str, model_no: str, inv_no: str, serial: str, allocated_weight: Decimal \| None | InvoiceItem |
| models | `PackingItem` | pydantic model: part_no: str, qty: Decimal, nw: Decimal, is_first_row_of_merge: bool | PackingItem |
| models | `PackingTotals` | pydantic model: total_nw: Decimal, total_nw_precision: int, total_gw: Decimal, total_gw_precision: int, total_packets: int \| None | PackingTotals |
| models | `ColumnMapping` | pydantic model: sheet_type: str, field_map: dict[str, int], header_row: int, effective_header_row: int | ColumnMapping |
| models | `MergeRange` | pydantic model: min_row: int, max_row: int, min_col: int, max_col: int, value: Any | MergeRange |
| models | `FieldPattern` | pydantic model: patterns: list[str], type: str, required: bool | FieldPattern |
| models | `AppConfig` | pydantic model: invoice_sheet_patterns: list[re.Pattern], packing_sheet_patterns: list[re.Pattern], invoice_columns: dict[str, FieldPattern], packing_columns: dict[str, FieldPattern], inv_no_patterns: list[re.Pattern], inv_no_label_patterns: list[re.Pattern], inv_no_exclude_patterns: list[re.Pattern], currency_lookup: dict[str, str], country_lookup: dict[str, str], template_path: Path | AppConfig |
| models | `FileResult` | pydantic model: filename: str, status: str, errors: list[ProcessingError], warnings: list[ProcessingError], invoice_items: list[InvoiceItem], packing_items: list[PackingItem], packing_totals: PackingTotals \| None | FileResult |
| models | `BatchResult` | pydantic model: total_files: int, success_count: int, attention_count: int, failed_count: int, processing_time: float, file_results: list[FileResult], log_path: str | BatchResult |
| errors | `ErrorCode` | enum: ERR_001 through ERR_052 (string values matching PRD catalog) | ErrorCode |
| errors | `WarningCode` | enum: ATT_002, ATT_003, ATT_004 | WarningCode |
| errors | `ProcessingError` | class(Exception): code: ErrorCode \| WarningCode, message: str, context: dict[str, Any] | ProcessingError |
| errors | `ConfigError` | class(Exception): code: ErrorCode, message: str, path: str | ConfigError |
| logger | `setup_logging(log_path: Path) -> None` | Configures root logger with console (INFO) + file (DEBUG) handlers | None |
| logger | `setup_diagnostic_logging(log_path: Path) -> None` | Configures root logger with console (DEBUG) + file (DEBUG) handlers | None |
| utils | `strip_unit_suffix(value: str) -> str` | Remove KG/KGS/G/LB/LBS/PCS/EA/件/个 suffixes | str |
| utils | `safe_decimal(value: Any, decimals: int) -> Decimal` | Convert to Decimal with precision, ROUND_HALF_UP + epsilon | Decimal |
| utils | `round_half_up(value: Decimal, decimals: int) -> Decimal` | ROUND_HALF_UP with epsilon trick | Decimal |
| utils | `normalize_header(value: str) -> str` | Normalize header: collapse whitespace, strip | str |
| utils | `is_stop_keyword(value: str) -> bool` | Check for total/合计/总计/小计 | bool |
| utils | `normalize_lookup_key(value: str) -> str` | Normalize for lookup: upper, strip, collapse comma-space | str |
| utils | `detect_cell_precision(cell: Any) -> int` | Read cell number_format, extract decimal places | int |
| utils | `DITTO_MARKS` | `frozenset[str]` | frozenset |
| utils | `FOOTER_KEYWORDS` | `tuple[str, ...]` | tuple |
| utils | `HEADER_KEYWORDS` | `frozenset[str]` | frozenset |

---

### Batch 2: Config + Merge Infrastructure + XLS Adapter

| Module | Path | Test Path | FRs | Complexity | Imports |
|--------|------|-----------|-----|------------|---------|
| config | `src/autoconvert/config.py` | `tests/test_config.py` | FR-002 | complex | models, errors, utils, PyYAML, openpyxl, pathlib |
| merge_tracker | `src/autoconvert/merge_tracker.py` | `tests/test_merge_tracker.py` | FR-010 | complex | models |
| xls_adapter | `src/autoconvert/xls_adapter.py` | `tests/test_xls_adapter.py` | FR-003 (partial) | moderate | xlrd, openpyxl |

**Exports Table:**

| Module | Function/Class | Signature | Return Type |
|--------|---------------|-----------|-------------|
| config | `load_config(config_dir: Path) -> AppConfig` | Load YAML + 3 Excel configs, compile regex, build lookup tables, validate template | AppConfig |
| merge_tracker | `MergeTracker` | class: `__init__(self, sheet: Worksheet) -> None` — captures merges, unmerges sheet | MergeTracker |
| merge_tracker | `MergeTracker.is_merge_anchor(self, row: int, col: int) -> bool` | Check if cell is top-left of a merge range | bool |
| merge_tracker | `MergeTracker.is_in_merge(self, row: int, col: int) -> bool` | Check if cell is in any merge range | bool |
| merge_tracker | `MergeTracker.get_merge_range(self, row: int, col: int) -> MergeRange \| None` | Get the merge range containing this cell | MergeRange \| None |
| merge_tracker | `MergeTracker.get_anchor_value(self, row: int, col: int) -> Any` | Get the anchor cell's value for a merged cell | Any |
| merge_tracker | `MergeTracker.is_data_area_merge(self, row: int, col: int, header_row: int) -> bool` | Check if merge is in data area (after header) | bool |
| merge_tracker | `MergeTracker.get_string_value(self, row: int, col: int, header_row: int) -> Any` | Get propagated string value for data-area merges | Any |
| merge_tracker | `MergeTracker.get_weight_value(self, row: int, col: int, header_row: int) -> Decimal` | Get weight value: anchor row retains, others = 0.0 | Decimal |
| xls_adapter | `convert_xls_to_xlsx(filepath: Path) -> Workbook` | Read .xls via xlrd, create in-memory openpyxl Workbook with all sheets, cells, and merge ranges preserved | Workbook |

---

### Batch 3: Detection + Extraction + Transformation

These modules are independent of each other (sheet_detect and column_map both depend on config; extract_* both depend on merge_tracker; transform depends on config). None depend on each other. Note: extract_packing split into two modules per ambiguity resolution #4.

| Module | Path | Test Path | FRs | Complexity | Imports |
|--------|------|-----------|-----|------------|---------|
| sheet_detect | `src/autoconvert/sheet_detect.py` | `tests/test_sheet_detect.py` | FR-004, FR-005, FR-006 | simple | models, errors, config |
| column_map | `src/autoconvert/column_map.py` | `tests/test_column_map.py` | FR-007, FR-008, FR-009 | complex | models, errors, config, utils |
| extract_invoice | `src/autoconvert/extract_invoice.py` | `tests/test_extract_invoice.py` | FR-011 | complex | models, errors, merge_tracker, utils |
| extract_packing | `src/autoconvert/extract_packing.py` | `tests/test_extract_packing.py` | FR-012, FR-013 | complex | models, errors, merge_tracker, utils |
| extract_totals | `src/autoconvert/extract_totals.py` | `tests/test_extract_totals.py` | FR-014, FR-015, FR-016, FR-017 | complex | models, errors, merge_tracker, utils |
| transform | `src/autoconvert/transform.py` | `tests/test_transform.py` | FR-018, FR-019, FR-020 | moderate | models, errors, config, utils |
| weight_alloc | `src/autoconvert/weight_alloc.py` | `tests/test_weight_alloc.py` | FR-021-FR-026 | complex | models, errors, utils |

**Exports Table:**

| Module | Function/Class | Signature | Return Type |
|--------|---------------|-----------|-------------|
| sheet_detect | `detect_sheets(workbook: Workbook, config: AppConfig) -> tuple[Worksheet, Worksheet]` | Identify Invoice + Packing sheets by regex; raises ProcessingError ERR_012/013 | tuple[Worksheet, Worksheet] |
| column_map | `detect_header_row(sheet: Worksheet, sheet_type: str, config: AppConfig) -> int` | Scan rows 7-30 with three-tier priority; raises ProcessingError ERR_014 | int |
| column_map | `map_columns(sheet: Worksheet, header_row: int, sheet_type: str, config: AppConfig) -> ColumnMapping` | Map columns via regex with sub-header + currency fallback; raises ProcessingError ERR_020 | ColumnMapping |
| column_map | `extract_inv_no_from_header(sheet: Worksheet, config: AppConfig) -> str \| None` | Scan rows 1-15 for invoice number; returns None if not found (ERR_021 raised by batch.py) | str \| None |
| extract_invoice | `extract_invoice_items(sheet: Worksheet, column_map: ColumnMapping, merge_tracker: MergeTracker, inv_no: str \| None) -> list[InvoiceItem]` | Extract 13 fields per item with stop conditions, precision, COO/COD fallback | list[InvoiceItem] |
| extract_packing | `extract_packing_items(sheet: Worksheet, column_map: ColumnMapping, merge_tracker: MergeTracker) -> tuple[list[PackingItem], int]` | Extract packing items + last_data_row; handles implicit continuation, ditto marks, merged part_no | tuple[list[PackingItem], int] |
| extract_packing | `validate_merged_weights(packing_items: list[PackingItem], merge_tracker: MergeTracker, column_map: ColumnMapping) -> None` | Validate no different part_nos share merged NW cell; raises ProcessingError ERR_046 | None |
| extract_totals | `detect_total_row(sheet: Worksheet, last_data_row: int, column_map: ColumnMapping, merge_tracker: MergeTracker) -> int` | Two-strategy total row detection; raises ProcessingError ERR_032 | int |
| extract_totals | `extract_totals(sheet: Worksheet, total_row: int, column_map: ColumnMapping) -> PackingTotals` | Extract total_nw (FR-015), total_gw (FR-016), total_packets (FR-017); raises ERR_033/034, warns ATT_002 | PackingTotals |
| transform | `convert_currency(items: list[InvoiceItem], config: AppConfig) -> tuple[list[InvoiceItem], list[ProcessingError]]` | Lookup currency -> numeric code; returns warnings ATT_003 for unmatched | tuple[list[InvoiceItem], list[ProcessingError]] |
| transform | `convert_country(items: list[InvoiceItem], config: AppConfig) -> tuple[list[InvoiceItem], list[ProcessingError]]` | Lookup COO -> numeric code; returns warnings ATT_004 for unmatched | tuple[list[InvoiceItem], list[ProcessingError]] |
| transform | `clean_po_number(items: list[InvoiceItem]) -> list[InvoiceItem]` | Strip suffix after first `-`, `.`, `/`; preserve if empty result | list[InvoiceItem] |
| weight_alloc | `allocate_weights(invoice_items: list[InvoiceItem], packing_items: list[PackingItem], packing_totals: PackingTotals) -> list[InvoiceItem]` | Full pipeline: aggregate (FR-021), validate sum (FR-022), precision (FR-023), round (FR-024), allocate (FR-025), final validate (FR-026); raises ERR_040-048 | list[InvoiceItem] |

---

### Batch 4: Validation + Output + Report

| Module | Path | Test Path | FRs | Complexity | Imports |
|--------|------|-----------|-----|------------|---------|
| validate | `src/autoconvert/validate.py` | `tests/test_validate.py` | FR-027 | simple | models, errors |
| output | `src/autoconvert/output.py` | `tests/test_output.py` | FR-029, FR-030 | moderate | models, errors, config, openpyxl |
| report | `src/autoconvert/report.py` | `tests/test_report.py` | FR-033 | moderate | models, logging |

**Exports Table:**

| Module | Function/Class | Signature | Return Type |
|--------|---------------|-----------|-------------|
| validate | `determine_file_status(errors: list[ProcessingError], warnings: list[ProcessingError]) -> str` | Any ERR -> "Failed", any ATT -> "Attention", else "Success" | str |
| output | `write_template(invoice_items: list[InvoiceItem], packing_totals: PackingTotals, config: AppConfig, output_path: Path) -> None` | Populate 40-column template, write to output_path; raises ERR_051/052 | None |
| report | `print_batch_summary(batch_result: BatchResult) -> None` | Format and print batch summary to console per FR-033 format | None |

---

### Batch 5: Orchestrator + Entry Point

| Module | Path | Test Path | FRs | Complexity | Imports |
|--------|------|-----------|-----|------------|---------|
| batch | `src/autoconvert/batch.py` | `tests/test_batch.py` | FR-001, FR-003, FR-028 | complex | models, errors, config, sheet_detect, column_map, merge_tracker, extract_invoice, extract_packing, extract_totals, transform, weight_alloc, validate, output, logger, report, xls_adapter |
| cli | `src/autoconvert/cli.py` | `tests/test_diagnostic.py` | FR-034 | simple | batch, config, logger |
| __main__ | `src/autoconvert/__main__.py` | — | — | simple | cli |

**Exports Table:**

| Module | Function/Class | Signature | Return Type |
|--------|---------------|-----------|-------------|
| batch | `run_batch(config: AppConfig) -> BatchResult` | Orchestrate full batch: setup dirs (FR-001), clear finished (FR-028), scan files (FR-003), process each, collect results | BatchResult |
| batch | `process_file(filepath: Path, config: AppConfig) -> FileResult` | Per-file pipeline: open workbook, detect sheets, map columns, extract, transform, allocate, validate, output | FileResult |
| cli | `main() -> None` | Entry point: parse args, load config, setup logging, call run_batch or diagnostic; sys.exit with code 0/1/2 | None |
| cli | `parse_args() -> argparse.Namespace` | Parse CLI args: optional `--diagnostic <filename>` | argparse.Namespace |

---

## 8. Ambiguities

1. **Golden output files location:** ~~RESOLVED~~ — Skip golden ref testing. `data/finished/` files are not validated as correct output.

2. **Test corpus location:** ~~RESOLVED~~ — Integration tests point to `data/` directly. No copying to `tests/fixtures/`.

3. **ERR_021 ownership split:** The PRD says inv_no extraction is a fallback (FR-009) handled by `column_map.py`, but the ERR_021 decision (both column and header failed) requires knowledge from both column mapping and header extraction phases. The architecture assigns orchestration to `batch.py`. This means batch.py must check: (1) was inv_no in column_map? (2) if not, did `extract_inv_no_from_header()` return a value? (3) if neither, raise ERR_021. The error is logically batch.py's responsibility but the code is `column_map.py`'s domain.

4. **extract_packing.py size risk:** ~~RESOLVED~~ — Proactively split: `extract_packing.py` (FR-012, FR-013) + `extract_totals.py` (FR-014, FR-015, FR-016, FR-017).

5. **Packing GW column mapping:** GW is listed as `required: true` in `packing_columns` config, but the PRD only extracts GW from the total row (FR-016), not from per-item rows. The GW column index is needed for total row detection (FR-014 implicit strategy) and total_gw extraction, but is never used for per-item data. Mapping it as "required" is correct for the column_map phase even though it is not extracted per-item.

6. **`.xls` adapter:** ~~RESOLVED~~ — Build `xls_adapter.py` module in Batch 2. Converts xlrd Book to in-memory openpyxl Workbook with all sheets, cells, and merge ranges.

7. **Invoice `weight` field mapping but no extraction:** FR-008 lists `weight` as an optional invoice column to map, but FR-011 explicitly says "weight is NOT extracted (calculated by weight allocation)." The column is mapped but ignored during extraction. This is by design (the mapping confirms the column exists for diagnostic purposes) but could confuse implementers.

8. **`model` field name collision:** The PRD uses `model` as an invoice field name (型号), but Python's `model` is a common attribute name in pydantic. The data model field should be named `model_no` or similar to avoid collision with pydantic internals. Architecture does not specify the escape name.

9. **Total packets validation range:** FR-017 says "positive integer 1-1000" but some vendors may have very large shipments. The 1000 upper bound is a heuristic. If a legitimate vendor has >1000 cartons, this will produce a false ATT_002 warning.

10. **Config `country_rules.xlsx` mixed types:** PRD Section 7 notes "3 Target_Code values stored as string instead of int." The `config.py` module must normalize all Target_Code to consistent string type. The exact entries are not specified — must handle any cell type.
