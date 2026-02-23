# Spec: utils.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/utils.py`
- **Tests:** `tests/test_utils.py`

## 2. FRs

- FR-011 (unit suffix stripping for invoice extraction, COO/COD, precision)
- FR-012 (unit suffix stripping for packing extraction, ditto mark detection)
- FR-015/FR-016 (cell format precision detection for total_nw/total_gw)
- FR-007 (header keyword detection for tier classification)
- FR-008 (header normalization)
- FR-018/FR-019 (lookup key normalization for currency/country transforms)

Key rules:
- `strip_unit_suffix`: Strip `KG`, `KGS`, `G`, `LB`, `LBS`, `PCS`, `EA`, `件`, `个` suffixes from numeric strings. Regex: `re.sub(r'\s*(KGS?|LBS?|G|PCS|EA|件|个)\s*$', '', value.strip(), flags=re.IGNORECASE)`. Case-insensitive.
- `safe_decimal`: Convert cell value to `Decimal` with specified precision using ROUND_HALF_UP + epsilon. Implementation: `Decimal(str(float(value) * 10**decimals + 1e-9)).to_integral_value() / Decimal(10**decimals)`. Wrap in try/except for non-numeric.
- `round_half_up`: ROUND_HALF_UP with epsilon trick. Apply epsilon then `quantize(Decimal(10) ** -decimals, rounding=ROUND_HALF_UP)`.
- `normalize_header`: Collapse `\n`, `\t`, multiple spaces → single space, strip. Two-step: `re.sub(r'[\n\t]+', ' ', value).strip()` then `re.sub(r'\s+', ' ', result)`.
- `is_stop_keyword`: `re.search(r'(?i)(total|合计|总计|小计)', str(value)) is not None`.
- `normalize_lookup_key`: `value.strip().upper().replace(', ', ',')` — collapse `, ` (comma-space) to `,` so "Taiwan, China" matches key "TAIWAN,CHINA".
- `detect_cell_precision`: Read `cell.number_format`, count `0` or `#` digits after `.`. `General`/empty format: return 5 then normalize trailing zeros (per FR-015 "General format: round to 5 decimals"). Format `@` (text): return 0. Complex formats like `_($* #,##0.00_)` → count `00` after `.` → 2.
- `DITTO_MARKS`: `frozenset({'"', '\u3003', '\u201C', '\u201D'})` — double-quote (U+0022), 〃 (U+3003), " (U+201C), " (U+201D).
- `FOOTER_KEYWORDS`: `('报关行', '有限公司')` — tuple, used by extract_invoice.py stop conditions.
- `HEADER_KEYWORDS`: `frozenset({'qty', 'n.w.', 'g.w.', 'part no', 'amount', 'price', 'quantity', 'weight', '品牌', '料号', '数量', '单价', '金额', '净重', '毛重', '原产', 'country', 'origin', 'brand', 'model', 'description', 'unit', 'currency', 'coo'})`.

## 3. Exports

| Symbol | Type/Signature | Return | Docstring Summary |
|--------|---------------|--------|--------------------|
| `strip_unit_suffix(value: str) -> str` | function | str | Remove KG/KGS/G/LB/LBS/PCS/EA/件/个 suffixes from numeric strings before parsing. Case-insensitive. |
| `safe_decimal(value: Any, decimals: int) -> Decimal` | function | Decimal | Convert cell value (any type) to Decimal with specified decimal places using ROUND_HALF_UP + epsilon trick. Raises ValueError on non-numeric. |
| `round_half_up(value: Decimal, decimals: int) -> Decimal` | function | Decimal | Round a Decimal value to `decimals` places using ROUND_HALF_UP with epsilon trick. |
| `normalize_header(value: str) -> str` | function | str | Normalize header cell text: collapse newlines/tabs/multiple spaces to single space, strip leading/trailing whitespace. |
| `is_stop_keyword(value: str) -> bool` | function | bool | Return True if value contains total/合计/总计/小计 (case-insensitive). |
| `normalize_lookup_key(value: str) -> str` | function | str | Normalize for lookup table: strip, uppercase, collapse comma-space to comma. |
| `detect_cell_precision(cell: Any) -> int` | function | int | Read openpyxl cell number_format and return the number of decimal places (0-5). |
| `DITTO_MARKS` | `frozenset[str]` | frozenset | Set of recognized ditto mark characters: `"`, `〃`, `"`, `"`. |
| `FOOTER_KEYWORDS` | `tuple[str, ...]` | tuple | Footer keywords indicating end of invoice data: `('报关行', '有限公司')`. |
| `HEADER_KEYWORDS` | `frozenset[str]` | frozenset | Keywords indicating a true header row for Tier-0 classification in header detection. |

## 4. Imports

| Module | Symbols |
|--------|---------|
| `re` (stdlib) | `re.sub`, `re.search`, `re.IGNORECASE` |
| `decimal` (stdlib) | `Decimal`, `ROUND_HALF_UP`, `InvalidOperation` |
| `typing` (stdlib) | `Any` |

No internal autoconvert imports — this is a foundation module with no local dependencies.

No call order required among the functions in this module — each is independent.

## 5. Side-Effect Rules

- No file I/O.
- No logging.
- No state mutation (all functions are pure/stateless).
- `DITTO_MARKS`, `FOOTER_KEYWORDS`, `HEADER_KEYWORDS` are module-level constants (computed once at import time, immutable).

## 6. Gotchas

- **`strip_unit_suffix` unit order:** The regex `KGS?` must come before `G` to avoid `G` matching inside `KGS`. The regex as written (`KGS?|LBS?|G|PCS|EA|件|个`) handles this via alternation precedence (leftmost match wins in `re.sub`).
- **`safe_decimal` epsilon trick:** The epsilon `1e-9` is added to handle floating-point storage artifacts (e.g., `2.2799999...` rounds correctly to `2.28`). The implementation must use `str(float(value) * 10**decimals + 1e-9)` — NOT `Decimal(value)` directly (inherits float error). Non-numeric input (None, str, bool) must raise `ValueError` or `InvalidOperation` so callers can catch and raise ERR_031.
- **`safe_decimal` vs `round_half_up`:** `safe_decimal` is for converting raw cell values (any type) to Decimal. `round_half_up` is for re-rounding already-Decimal values. They use the same underlying technique but different input contracts.
- **`detect_cell_precision` for `General` format:** Return 5. Callers (FR-015) then apply `round_half_up(value, 5)` and normalize trailing zeros. Do NOT return 0 for General — 0 would lose all decimal information.
- **`detect_cell_precision` for `@` format:** Return 0. Text-formatted cells are not numeric; the caller handles this case.
- **`detect_cell_precision` for complex formats:** Examples to handle correctly:
  - `"0.00000_"` → 5
  - `"#,##0.00"` → 2
  - `"_($* #,##0.00_)"` → 2
  - `"0"` → 0
  - `"General"` → 5
  - `"@"` → 0
  Parse by finding `.` in the format string, then counting `0` or `#` characters after it until a non-digit-format character (e.g., `_`, `)`, space).
- **`normalize_lookup_key` collapse rule:** Replace `, ` (comma THEN space) with `,` (comma only). This ensures "Taiwan, China" normalizes to "TAIWAN,CHINA" matching the config entry. The collapse happens AFTER `.upper()` and `.strip()` — actually the order is: strip → upper → replace. The replace `', '` → `','` operates on the already-uppercased string (comma-space is the same in any case).
- **`is_stop_keyword` input type:** The function receives `str(value)` — it must handle `None`, `int`, and other types by calling `str(value)` internally before the regex search. The signature takes `str` but callers may pass any type; the implementation should guard with `str(value)`.
- **`FOOTER_KEYWORDS` as tuple not frozenset:** The order matters for documentation clarity (tuple is the correct type) and matches the build-plan.md spec exactly. Used in `any(kw in str(value) for kw in FOOTER_KEYWORDS)` patterns.
- **Patterned examples in PRD (Generalization Gotcha):** FR-012 lists ditto mark characters `"` (U+0022), `〃` (U+3003), `"` (U+201C), `"` (U+201D) individually. These are NOT a pattern to generalize further — only these 4 exact characters are in `DITTO_MARKS`. If a new ditto character is discovered, it must be added explicitly.

## 7. Ownership Exclusions

utils.py does not own any error codes. It provides utilities used by owning modules:
- DO NOT validate/log ERR_030 (EMPTY_REQUIRED_FIELD) — owned by extract_invoice.py and extract_packing.py.
- DO NOT validate/log ERR_031 (INVALID_NUMERIC) — owned by extract_invoice.py and extract_packing.py. `safe_decimal` raises `ValueError`/`InvalidOperation` which callers convert to ERR_031.
- DO NOT validate/log ERR_002 (INVALID_REGEX) — owned by config.py.

## 8. Test Requirements

### `strip_unit_suffix`
1. `test_strip_unit_suffix_kgs` — `strip_unit_suffix("2.5 KGS")` → `"2.5"`.
2. `test_strip_unit_suffix_kg_no_space` — `strip_unit_suffix("15KG")` → `"15"`.
3. `test_strip_unit_suffix_g` — `strip_unit_suffix("500G")` → `"500"`.
4. `test_strip_unit_suffix_lbs` — `strip_unit_suffix("10 LBS")` → `"10"`.
5. `test_strip_unit_suffix_pcs` — `strip_unit_suffix("100 PCS")` → `"100"`.
6. `test_strip_unit_suffix_ea` — `strip_unit_suffix("50 EA")` → `"50"`.
7. `test_strip_unit_suffix_jian` — `strip_unit_suffix("3 件")` → `"3"`.
8. `test_strip_unit_suffix_ge` — `strip_unit_suffix("10个")` → `"10"`.
9. `test_strip_unit_suffix_case_insensitive` — `strip_unit_suffix("5.0 kgs")` → `"5.0"`.
10. `test_strip_unit_suffix_no_suffix` — `strip_unit_suffix("2.500")` → `"2.500"` (unchanged).
11. `test_strip_unit_suffix_empty` — `strip_unit_suffix("")` → `""`.

### `safe_decimal`
1. `test_safe_decimal_float_value` — `safe_decimal(2.2799999999, 2)` → `Decimal('2.28')` (epsilon handles artifact).
2. `test_safe_decimal_int_value` — `safe_decimal(10, 0)` → `Decimal('10')`.
3. `test_safe_decimal_string_numeric` — `safe_decimal("3.14159", 5)` → `Decimal('3.14159')`.
4. `test_safe_decimal_none_raises` — `safe_decimal(None, 2)` raises `ValueError` or `InvalidOperation`.
5. `test_safe_decimal_string_non_numeric_raises` — `safe_decimal("abc", 2)` raises `ValueError` or `InvalidOperation`.

### `round_half_up`
1. `test_round_half_up_half_rounds_up` — `round_half_up(Decimal('2.125'), 2)` → `Decimal('2.13')` (not 2.12).
2. `test_round_half_up_no_artifact` — `round_half_up(Decimal('2.2799999999'), 2)` → `Decimal('2.28')`.
3. `test_round_half_up_zero_decimals` — `round_half_up(Decimal('5.5'), 0)` → `Decimal('6')`.
4. `test_round_half_up_five_decimals` — `round_half_up(Decimal('1.123456'), 5)` → `Decimal('1.12346')`.

### `normalize_header`
1. `test_normalize_header_newline_in_header` — `normalize_header("N.W.\n(KGS)")` → `"N.W. (KGS)"`.
2. `test_normalize_header_tab` — `normalize_header("Part\tNo")` → `"Part No"`.
3. `test_normalize_header_multiple_spaces` — `normalize_header("Part   No")` → `"Part No"`.
4. `test_normalize_header_strip_whitespace` — `normalize_header("  qty  ")` → `"qty"`.
5. `test_normalize_header_mixed` — `normalize_header("N.W.\n\t(KGS)  ")` → `"N.W. (KGS)"`.

### `is_stop_keyword`
1. `test_is_stop_keyword_total_english` — `is_stop_keyword("Total Amount")` → `True`.
2. `test_is_stop_keyword_hejii` — `is_stop_keyword("合计")` → `True`.
3. `test_is_stop_keyword_zongjii` — `is_stop_keyword("总计")` → `True`.
4. `test_is_stop_keyword_xiaoji` — `is_stop_keyword("小计")` → `True`.
5. `test_is_stop_keyword_case_insensitive` — `is_stop_keyword("TOTAL")` → `True`.
6. `test_is_stop_keyword_normal_value` — `is_stop_keyword("ABC-123")` → `False`.

### `normalize_lookup_key`
1. `test_normalize_lookup_key_uppercase` — `normalize_lookup_key("usd")` → `"USD"`.
2. `test_normalize_lookup_key_strip_whitespace` — `normalize_lookup_key("  USD  ")` → `"USD"`.
3. `test_normalize_lookup_key_comma_space` — `normalize_lookup_key("Taiwan, China")` → `"TAIWAN,CHINA"`.
4. `test_normalize_lookup_key_already_normalized` — `normalize_lookup_key("USD")` → `"USD"`.

### `detect_cell_precision`
1. `test_detect_cell_precision_format_0_00` — cell with `number_format="0.00"` → `2`.
2. `test_detect_cell_precision_format_hash_comma` — cell with `number_format="#,##0.00"` → `2`.
3. `test_detect_cell_precision_format_00000` — cell with `number_format="0.00000_"` → `5`.
4. `test_detect_cell_precision_general_format` — cell with `number_format="General"` → `5`.
5. `test_detect_cell_precision_text_format` — cell with `number_format="@"` → `0`.
6. `test_detect_cell_precision_complex_accounting` — cell with `number_format="_($* #,##0.00_)"` → `2`.
7. `test_detect_cell_precision_no_decimal` — cell with `number_format="0"` → `0`.

### Constants
1. `test_ditto_marks_contains_all_four` — verify `DITTO_MARKS` contains exactly: `'"'` (U+0022), `'〃'` (U+3003), `'\u201C'`, `'\u201D'`. Length is 4.
2. `test_footer_keywords_tuple` — verify `FOOTER_KEYWORDS` is a `tuple` containing `'报关行'` and `'有限公司'`. Length is 2.
3. `test_header_keywords_frozenset` — verify `HEADER_KEYWORDS` is a `frozenset` containing `'qty'`, `'n.w.'`, `'part no'`, `'coo'`, `'品牌'`. Minimum length check ≥ 20.
