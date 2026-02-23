# Spec: models.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/models.py`
- **Tests:** `tests/test_models.py`

## 2. FRs

This module defines data entities used by all other modules. It has no FR of its own but must faithfully represent the entities defined in FR-011 (InvoiceItem), FR-012 (PackingItem), FR-015/FR-016/FR-017 (PackingTotals), FR-007/FR-008 (ColumnMapping), FR-010 (MergeRange), FR-002 (FieldPattern, AppConfig), and FR-027/FR-033 (FileResult, BatchResult).

Key rules captured in the models:
- All monetary/weight values use `Decimal` (not float).
- Optional pydantic fields use `X | None = None` syntax (Python 3.11+ style).
- `model_no` is used instead of `model` to avoid collision with pydantic internals (Ambiguity #8).
- `AppConfig` stores compiled `re.Pattern` objects; requires `model_config = ConfigDict(arbitrary_types_allowed=True)`.
- `allocated_weight: Decimal | None = None` on `InvoiceItem` — `None` before weight allocation, `Decimal` after.
- `total_packets: int | None = None` on `PackingTotals` — optional per FR-017.

## 3. Exports

All exports match the build-plan.md Batch 1 Exports Table exactly.

| Class | Signature / Fields | Notes |
|-------|--------------------|-------|
| `InvoiceItem` | `part_no: str, po_no: str, qty: Decimal, price: Decimal, amount: Decimal, currency: str, coo: str, cod: str, brand: str, brand_type: str, model_no: str, inv_no: str, serial: str, allocated_weight: Decimal \| None = None` | Pydantic BaseModel. `cod` and `serial` are required str fields (may be empty string when column absent). `allocated_weight` is None until weight_alloc.py populates it. |
| `PackingItem` | `part_no: str, qty: Decimal, nw: Decimal, is_first_row_of_merge: bool` | Pydantic BaseModel. `is_first_row_of_merge=True` for merged-cell anchor rows and normal single rows; `False` for non-anchor continuation rows and ditto-mark rows. |
| `PackingTotals` | `total_nw: Decimal, total_nw_precision: int, total_gw: Decimal, total_gw_precision: int, total_packets: int \| None = None` | Pydantic BaseModel. Precision fields store the detected format precision (min 2, max 5) for use by weight_alloc.py. |
| `ColumnMapping` | `sheet_type: str, field_map: dict[str, int], header_row: int, effective_header_row: int` | Pydantic BaseModel. `sheet_type` is `"invoice"` or `"packing"`. `field_map` maps field name (e.g. `"part_no"`) to 1-based column index. `effective_header_row` equals `header_row` unless sub-header scan advanced it to `header_row+1`. |
| `MergeRange` | `min_row: int, max_row: int, min_col: int, max_col: int, value: Any` | Pydantic BaseModel. All indices 1-based (openpyxl convention). `value` is the anchor cell's value at time of capture (before unmerging). Requires `model_config = ConfigDict(arbitrary_types_allowed=True)` for `Any`. |
| `FieldPattern` | `patterns: list[str], type: str, required: bool` | Pydantic BaseModel. `type` is one of `"string"`, `"numeric"`, `"currency"`. `patterns` are raw regex strings (not compiled). |
| `AppConfig` | `invoice_sheet_patterns: list[re.Pattern], packing_sheet_patterns: list[re.Pattern], invoice_columns: dict[str, FieldPattern], packing_columns: dict[str, FieldPattern], inv_no_patterns: list[re.Pattern], inv_no_label_patterns: list[re.Pattern], inv_no_exclude_patterns: list[re.Pattern], currency_lookup: dict[str, str], country_lookup: dict[str, str], template_path: Path` | Pydantic BaseModel. `model_config = ConfigDict(arbitrary_types_allowed=True)` required for `re.Pattern` and `Path`. Lookup dict keys are normalized via `normalize_lookup_key()` (uppercase). |
| `FileResult` | `filename: str, status: str, errors: list[ProcessingError], warnings: list[ProcessingError], invoice_items: list[InvoiceItem], packing_items: list[PackingItem], packing_totals: PackingTotals \| None = None` | Pydantic BaseModel. `status` is one of `"Success"`, `"Attention"`, `"Failed"`, `"Pending"`. `model_config = ConfigDict(arbitrary_types_allowed=True)` for `ProcessingError`. |
| `BatchResult` | `total_files: int, success_count: int, attention_count: int, failed_count: int, processing_time: float, file_results: list[FileResult], log_path: str` | Pydantic BaseModel. |

## 4. Imports

| Module | Symbols |
|--------|---------|
| `decimal` (stdlib) | `Decimal` |
| `re` (stdlib) | `Pattern` (for type annotations) |
| `pathlib` (stdlib) | `Path` |
| `typing` (stdlib) | `Any` |
| `pydantic` | `BaseModel`, `ConfigDict` |
| `.errors` | `ProcessingError` |

No call order required — this module is pure model definitions with no function calls between models.

## 5. Side-Effect Rules

- No file I/O.
- No logging.
- No regex compilation (patterns stored as `list[str]` in `FieldPattern`; compiled patterns stored as `list[re.Pattern]` in `AppConfig` after config.py compiles them).
- No validation beyond pydantic field type coercion.

## 6. Gotchas

- **`model_no` vs `model`:** The PRD entity name is `model` (型号), but this module uses `model_no` to avoid collision with pydantic's `model` class method. All downstream modules (extract_invoice.py, output.py) must reference `item.model_no`. Document this in the field's `Field(alias="model")` or simply in the docstring — do NOT use pydantic alias unless the downstream serialization requires it. Prefer simple rename with docstring note.
- **`AppConfig` compiled patterns:** `re.Pattern` objects are stored (not raw strings). `arbitrary_types_allowed=True` is required. config.py compiles the regex before constructing `AppConfig`.
- **`FileResult` status values:** Exactly `"Pending"`, `"Success"`, `"Attention"`, `"Failed"` — match these strings exactly (validate.py produces these verbatim).
- **`ColumnMapping.field_map` 1-based:** Column indices in `field_map` are 1-based (openpyxl convention). Consumers use `sheet.cell(row=r, column=col_idx)` directly.
- **`MergeRange` value is Any:** The anchor value can be `None`, `str`, `int`, `float`, `datetime`. Do not constrain the type.
- **`PackingItem.is_first_row_of_merge`:** Set to `True` for: (a) normal single-row items, (b) merge anchor rows. Set to `False` for: (a) non-anchor merge continuation rows, (b) ditto-mark rows, (c) implicit continuation rows (same part_no, empty NW). This flag is used by weight_alloc.py to determine which rows contribute weight.
- **`ProcessingError` in `FileResult`:** Requires `arbitrary_types_allowed=True` since `ProcessingError` is an `Exception` subclass, not a pydantic model.
- **Empty string vs None on `InvoiceItem`:** Required string fields (`cod`, `serial`, `inv_no`) use `str` with default `""` (not `None`) when the column is absent or the value is truly empty. This enables ERR_030 detection by extract_invoice.py when a truly-required field is empty.

## 7. Ownership Exclusions

models.py defines data structures only. It does not perform any validation, raise any errors, or log any messages. It has no error code ownership.

## 8. Test Requirements

### `InvoiceItem`
1. `test_invoice_item_construction_all_fields` — construct with all 14 fields + `allocated_weight=Decimal('1.23')`; verify each attribute.
2. `test_invoice_item_allocated_weight_defaults_none` — construct without `allocated_weight`; verify `item.allocated_weight is None`.
3. `test_invoice_item_rejects_non_decimal_qty` — construct with `qty=1.5` (float); verify pydantic coerces it to `Decimal('1.5')` or raises `ValidationError` (pydantic v2 coerces floats to Decimal).
4. `test_invoice_item_model_no_field_exists` — construct with `model_no="ABC-123"`; verify `item.model_no == "ABC-123"` and attribute `model` does not shadow pydantic internals.

### `PackingItem`
1. `test_packing_item_is_first_row_of_merge_true` — construct with `is_first_row_of_merge=True`; verify attribute.
2. `test_packing_item_is_first_row_of_merge_false` — construct with `is_first_row_of_merge=False`; verify attribute.
3. `test_packing_item_nw_decimal` — construct with `nw=Decimal('2.50000')`; verify exact Decimal equality.

### `PackingTotals`
1. `test_packing_totals_total_packets_optional` — construct without `total_packets`; verify `packing_totals.total_packets is None`.
2. `test_packing_totals_precision_fields` — construct with `total_nw_precision=3, total_gw_precision=2`; verify both stored.
3. `test_packing_totals_full_construction` — construct all fields including `total_packets=7`; verify all values.

### `ColumnMapping`
1. `test_column_mapping_effective_header_row_advances` — construct with `header_row=10, effective_header_row=11`; verify both stored independently.
2. `test_column_mapping_field_map_stores_1based_indices` — `field_map={"part_no": 3, "qty": 5}`; verify `col_map.field_map["part_no"] == 3`.
3. `test_column_mapping_sheet_type_values` — construct with `sheet_type="invoice"` and separately `sheet_type="packing"`; both accepted.

### `MergeRange`
1. `test_merge_range_any_value_type` — construct with `value=None`, then with `value="text"`, then with `value=1.5`; all accepted.
2. `test_merge_range_1based_indices` — construct with `min_row=5, max_row=7, min_col=3, max_col=3`; verify exact storage.

### `AppConfig`
1. `test_app_config_accepts_compiled_patterns` — construct with `invoice_sheet_patterns=[re.compile(r'^invoice', re.IGNORECASE)]`; verify stored.
2. `test_app_config_lookup_dict_accepts_string_keys` — construct with `currency_lookup={"USD": "502"}`; verify `config.currency_lookup["USD"] == "502"`.

### `FileResult` and `BatchResult`
1. `test_file_result_status_values` — construct with `status="Failed"`; verify attribute; repeat for all 4 valid status strings.
2. `test_batch_result_counts` — construct with all count fields; verify `total_files == success_count + attention_count + failed_count` (not enforced by model but verified by test logic).
