# Spec: transform.py

## 1. Module Path and Test Path

- **Module:** `src/autoconvert/transform.py`
- **Tests:** `tests/test_transform.py`
- **FRs:** FR-018, FR-019, FR-020

---

## 2. Functional Requirements

### FR-018 — Currency Conversion

Look up each `InvoiceItem.currency` value in `config.currency_lookup` (built from `currency_rules.xlsx`).

**Normalization:** Apply `normalize_lookup_key(value)` before lookup — case-fold to uppercase, strip whitespace, collapse `, ` to `,`.

**Many-to-one mapping:** e.g., "USD" and "美元" both map to "502".

**On match:** replace `item.currency` with the Target_Code string.
**On no match:** preserve original value as-is; append ProcessingError with WarningCode.ATT_003 to the warnings list.

Returns `tuple[list[InvoiceItem], list[ProcessingError]]` — warnings list contains ATT_003 entries for unmatched currencies.

**Error:** ATT_003 (UNSTANDARDIZED_CURRENCY) — warning, not failure.

### FR-019 — Country Code Conversion

Look up each `InvoiceItem.coo` value in `config.country_lookup` (built from `country_rules.xlsx`).

**Normalization:** Apply `normalize_lookup_key(value)` — same as FR-018 (uppercase, strip, collapse `, ` → `,`).

Examples matching behavior: "Taiwan, China" normalized to "TAIWAN,CHINA" before lookup.

**Mixed int/str Target_Code:** config.py normalizes all to string; transform.py receives string values from `country_lookup`.

**On match:** replace `item.coo` with Target_Code string.
**On no match:** preserve original value as-is; append ProcessingError with WarningCode.ATT_004.

Returns `tuple[list[InvoiceItem], list[ProcessingError]]`.

**Error:** ATT_004 (UNSTANDARDIZED_COO) — warning, not failure.

### FR-020 — PO Number Cleaning

Strip everything from the first occurrence of `-`, `.`, or `/` onwards.

**Rules:**
- Find the first occurrence of any of `-`, `.`, `/` in the string.
- If found and the delimiter is NOT at position 0: return the substring before it.
- If the delimiter is at position 0 (e.g., "-PO12345"): return the original value unchanged.
- If no delimiter found: return original value unchanged.
- Applied as a transformation step — not at extraction time.

**Examples (verbatim from PRD):**
- `2250600556-2.1` → `2250600556`
- `PO32741.0` → `PO32741`
- `-PO12345` → `-PO12345` (preserved — delimiter at position 0)

Modifies `InvoiceItem.po_no` in place (returns new list of modified items).

**Error:** None (cleaning is best-effort; no error or warning raised).

---

## 3. Exports

```python
def convert_currency(
    items: list[InvoiceItem],
    config: AppConfig,
) -> tuple[list[InvoiceItem], list[ProcessingError]]:
    """Lookup currency -> numeric code; return warnings ATT_003 for unmatched.

    Args:
        items: Invoice items with raw currency values from extraction.
        config: Application configuration with compiled currency_lookup table.

    Returns:
        Tuple of (updated items list, list of ATT_003 warnings for unmatched values).
        Matched items have currency replaced with Target_Code string.
        Unmatched items preserve original currency value.
    """

def convert_country(
    items: list[InvoiceItem],
    config: AppConfig,
) -> tuple[list[InvoiceItem], list[ProcessingError]]:
    """Lookup COO -> numeric code; return warnings ATT_004 for unmatched.

    Args:
        items: Invoice items with raw coo values from extraction.
        config: Application configuration with compiled country_lookup table.

    Returns:
        Tuple of (updated items list, list of ATT_004 warnings for unmatched values).
        Matched items have coo replaced with Target_Code string.
        Unmatched items preserve original coo value.
    """

def clean_po_number(
    items: list[InvoiceItem],
) -> list[InvoiceItem]:
    """Strip suffix after first '-', '.', '/' delimiter; preserve if empty result.

    Args:
        items: Invoice items with raw po_no values.

    Returns:
        List of items with po_no cleaned. Items with po_no already empty or
        with delimiter at position 0 are unchanged.
    """
```

---

## 4. Imports

```python
from .models import InvoiceItem, AppConfig
from .errors import ProcessingError, WarningCode
from .utils import normalize_lookup_key
import logging
```

Functions used:
- `normalize_lookup_key(value)` — called on each currency and coo value before dictionary lookup.
- `ProcessingError(code, message, context)` — instantiated with `WarningCode.ATT_003` or `WarningCode.ATT_004`.

---

## 5. Side-Effect Rules

- **No file I/O.** Receives `AppConfig` (already loaded lookup tables).
- **No openpyxl usage.** Operates on model objects only.
- **Logging:** Use `logging.getLogger(__name__)`. Log WARNING for each ATT_003/ATT_004 occurrence; debug-log each lookup attempt and normalized key.

---

## 6. Ownership Exclusions

- DO NOT validate/log ERR_003 (DUPLICATE_LOOKUP) — owned by config.py. Lookup tables arrive deduplicated.
- DO NOT validate/log ERR_030 (EMPTY_REQUIRED_FIELD) — owned by extract_invoice.py and extract_packing.py.

---

## 7. Gotchas

1. **`normalize_lookup_key` must be applied identically in both transform.py and config.py** when building/using lookup tables. Both use `value.strip().upper().replace(', ', ',')`. A mismatch causes false ATT_003/ATT_004 warnings.
2. **ATT_003/ATT_004 are warnings (WarningCode), not errors (ErrorCode).** Constructing them as `ProcessingError(ErrorCode.ATT_003, ...)` would be incorrect — use `WarningCode.ATT_003`.
3. **Unmatched values are preserved as-is** (raw vendor string passthrough). output.py then writes this raw string to column D (currency) or H (coo). Do not replace with None or empty string.
4. **Po_no delimiter at position 0 must be preserved.** The check is: `if idx == 0: return original`. Without this guard, "-PO12345" becomes "" (empty string), triggering downstream ERR_030.
5. **All three delimiters are checked simultaneously**: find the minimum index among `-`, `.`, `/` positions. Use `min(filter(lambda i: i != -1, [s.find('-'), s.find('.'), s.find('/')]))` pattern or similar.
6. **Empty po_no:** If `po_no` is empty string, return it unchanged (no delimiter search needed).
7. **Patterned example from PRD:** The examples `2250600556-2.1 → 2250600556`, `PO32741.0 → PO32741`, `-PO12345 → -PO12345` are verbatim. Each must have its own test case.
8. **`convert_currency` and `convert_country` return new item lists** — do not mutate items in-place (functional style). However, the items list may contain the same InvoiceItem objects with updated fields (pydantic model_copy or direct field assignment) — avoid breaking reference equality if downstream code relies on it.

---

## 8. Test Requirements

### `convert_currency()`

1. **test_convert_currency_usd_matches_502** — Item with currency="USD"; after conversion, currency="502"; no warnings.
2. **test_convert_currency_chinese_美元_matches_502** — Item with currency="美元"; normalized to "美元" (already upper in this case but strip applied); maps to "502".
3. **test_convert_currency_case_insensitive_normalization** — Item with currency="usd"; normalized to "USD"; matches "502".
4. **test_convert_currency_unmatched_returns_att003_warning** — Item with currency="EUR" (not in lookup); currency preserved as "EUR"; warning list contains one ATT_003 ProcessingError.
5. **test_convert_currency_multiple_items_mixed_match** — Two items: one USD (matched), one GBP (unmatched); currency list has one ATT_003; matched item updated.

### `convert_country()`

1. **test_convert_country_taiwan_comma_china_normalization** — Item with coo="Taiwan, China"; normalized to "TAIWAN,CHINA" (collapse `, ` → `,`); matches lookup; replaced with code.
2. **test_convert_country_iso_code_cn** — Item with coo="CN"; matches lookup; replaced with code.
3. **test_convert_country_unmatched_returns_att004_warning** — Item with coo="XYZ"; preserved as "XYZ"; warning list contains ATT_004.
4. **test_convert_country_empty_coo_preserved_as_empty** — Item with coo=""; empty string not in lookup; preserved as ""; ATT_004 warning for empty (or no warning depending on whether empty string is treated as "not applicable" — treat as unmatched for correctness: empty coo was already a potential ERR_030 from extract_invoice.py; if it reached transform it was not an error, so produce ATT_004).
5. **test_convert_country_mixed_int_str_target_code_normalized_by_config** — Target_Code stored as int in config file is normalized to str by config.py; transform.py receives str and stores it as str in item.coo.

### `clean_po_number()`

1. **test_clean_po_number_dash_delimiter** — po_no="2250600556-2.1"; cleaned to "2250600556".
2. **test_clean_po_number_dot_delimiter** — po_no="PO32741.0"; cleaned to "PO32741".
3. **test_clean_po_number_slash_delimiter** — po_no="PO-001/A"; cleaned to "PO-001" (first delimiter `-` at index 6 — actually this is `-` at index 2: "PO-001" — corrected: `PO-001/A` → first delimiter is `-` at index 2 → `PO`... Wait: delimiter search finds minimum index among `-`=2, `.`=-1, `/`=6 → minimum is 2 → result is "PO"). Actually: "PO-001/A" has `-` at index 2, result = "PO". Verify with actual string: p=0, O=1, -=2 → "PO". Test should assert cleaned == "PO".
4. **test_clean_po_number_delimiter_at_position_0_preserved** — po_no="-PO12345"; preserved as "-PO12345" unchanged.
5. **test_clean_po_number_no_delimiter** — po_no="PO12345"; no delimiter; returned unchanged as "PO12345".
