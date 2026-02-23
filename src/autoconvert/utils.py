"""utils — Shared utility functions and constants used across multiple modules."""

import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DITTO_MARKS: frozenset[str] = frozenset({'"', "\u3003", "\u201c", "\u201d"})
"""Recognized ditto mark characters for packing extraction (FR-012)."""

FOOTER_KEYWORDS: tuple[str, ...] = ("报关行", "有限公司", "口岸关别", "进境口岸")
"""Footer keywords that indicate end of invoice data (FR-011)."""

WEIGHT_PRECISION_MIN: int = 2
"""Minimum decimal precision for weight values (used in extract_totals and weight_alloc)."""

WEIGHT_PRECISION_MAX: int = 5
"""Maximum decimal precision for weight values (used in extract_totals and weight_alloc)."""

STOP_KEYWORD_COL_COUNT: int = 10
"""Number of columns (A through J, 1-based) scanned for stop keywords (used in
extract_invoice, extract_packing, and extract_totals)."""

HEADER_KEYWORDS: frozenset[str] = frozenset(
    {
        "qty",
        "n.w.",
        "g.w.",
        "part no",
        "amount",
        "price",
        "quantity",
        "weight",
        "品牌",
        "料号",
        "数量",
        "单价",
        "金额",
        "净重",
        "毛重",
        "原产",
        "country",
        "origin",
        "brand",
        "model",
        "description",
        "unit",
        "currency",
        "coo",
    }
)
"""Keywords indicating a true header row for tier-0 classification (FR-007)."""

# Compiled regex patterns (module-level for performance)
_UNIT_SUFFIX_RE = re.compile(r"\s*(KGS?|LBS?|G|PCS|EA|件|个)\s*$", re.IGNORECASE)
_STOP_KEYWORD_RE = re.compile(r"(?i)(total|合计|总计|小计)")
_NEWLINE_TAB_RE = re.compile(r"[\n\t]+")
_MULTI_SPACE_RE = re.compile(r"\s+")
_FORMAT_DECIMAL_RE = re.compile(r"\.([0#]+)")


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def strip_unit_suffix(value: str) -> str:
    """Strip unit suffixes (KG, KGS, G, LB, LBS, PCS, EA, etc.) from numeric strings.

    Args:
        value: Raw string value potentially containing a unit suffix.

    Returns:
        The string with trailing unit suffix removed and whitespace stripped.
    """
    return _UNIT_SUFFIX_RE.sub("", value.strip())


def safe_decimal(value: Any, decimals: int) -> Decimal:
    """Convert a cell value to Decimal with specified precision using ROUND_HALF_UP.

    Uses the epsilon trick to handle floating-point representation issues
    (e.g., 2.28 stored as 2.2799999...).

    Args:
        value: The cell value to convert (int, float, str, etc.).
        decimals: Number of decimal places for the result.

    Returns:
        Decimal value rounded to the specified precision.

    Raises:
        ValueError: If the value cannot be converted to a numeric type.
    """
    try:
        float_val = float(value)
    except (TypeError, ValueError, InvalidOperation) as exc:
        raise ValueError(f"Cannot convert {value!r} to Decimal") from exc

    # Reason: The epsilon trick (adding 1e-9 before rounding) corrects for
    # floating-point artifacts like 2.2799999... which should round to 2.28.
    scaled = float_val * 10**decimals + 1e-9
    integral = Decimal(str(scaled)).to_integral_value(rounding=ROUND_HALF_UP)
    return integral / Decimal(10**decimals)


def round_half_up(value: Decimal, decimals: int) -> Decimal:
    """Round a Decimal value using ROUND_HALF_UP with the epsilon trick.

    Args:
        value: The Decimal value to round.
        decimals: Number of decimal places for the result.

    Returns:
        Decimal value rounded to the specified precision.
    """
    # Reason: Convert through float to apply the epsilon trick, ensuring
    # values like Decimal('2.285') round correctly to 2.29 at 2 decimals.
    float_val = float(value)
    scaled = float_val * 10**decimals + 1e-9
    integral = Decimal(str(scaled)).to_integral_value(rounding=ROUND_HALF_UP)
    return integral / Decimal(10**decimals)


def normalize_header(value: str) -> str:
    """Normalize header cell text by collapsing whitespace and stripping.

    Collapses newlines and tabs to single spaces, then collapses multiple
    spaces to a single space, then strips leading/trailing whitespace.

    Args:
        value: Raw header cell text.

    Returns:
        Normalized header string.
    """
    result = _NEWLINE_TAB_RE.sub(" ", value).strip()
    return _MULTI_SPACE_RE.sub(" ", result)


def is_stop_keyword(value: str) -> bool:
    """Check if a cell value contains a total/summary keyword.

    Matches: total, 合计, 总计, 小计 (case-insensitive).

    Args:
        value: The cell value to check (converted to string).

    Returns:
        True if the value contains a stop keyword, False otherwise.
    """
    return _STOP_KEYWORD_RE.search(str(value)) is not None


def normalize_lookup_key(value: str) -> str:
    """Normalize a lookup key for currency/country table matching.

    Applies: strip whitespace, uppercase, collapse comma-space to comma.

    Args:
        value: Raw lookup key string.

    Returns:
        Normalized lookup key.
    """
    return value.strip().upper().replace(", ", ",")


def detect_cell_precision(cell: Any) -> int:
    """Detect the number of decimal places from an openpyxl cell's number_format.

    Handles formats like 'General', '0.00', '#,##0.00', '_($* #,##0.00_)', '@'.
    For 'General' format, examines the cell value directly: rounds to 5 decimals
    then strips trailing zeros.

    Args:
        cell: An openpyxl cell object with `number_format` and `value` attributes.

    Returns:
        The number of decimal places (0 if no decimal portion detected).
    """
    fmt = getattr(cell, "number_format", "General")
    if fmt is None:
        fmt = "General"

    # Reason: 'General' and '@' (text) formats don't specify precision,
    # so we infer from the actual cell value instead.
    if fmt in ("General", "@"):
        return _precision_from_value(cell)

    # Parse the format string for decimal places
    match = _FORMAT_DECIMAL_RE.search(fmt)
    if match:
        return len(match.group(1))

    return 0


def try_float(value: Any) -> float | None:
    """Try to convert a value to float; strip unit suffixes from strings if needed.

    Used internally by extract_packing, extract_totals, and similar modules for
    numeric stop-condition checks where a hard parse failure should return None
    rather than raise.

    Args:
        value: Raw cell value (int, float, str, Decimal, or None).

    Returns:
        Float representation of the value, or None if conversion fails.
    """
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        # Reason: String cells may include unit suffixes (e.g. "12.5 KGS").
        # Strip the suffix and retry before giving up.
        if isinstance(value, str):
            stripped = strip_unit_suffix(value)
            try:
                return float(stripped)
            except (ValueError, TypeError):
                return None
        return None


def _precision_from_value(cell: Any) -> int:
    """Infer decimal precision from a cell's actual value for General format.

    Rounds the value to 5 decimal places and counts significant trailing digits.

    Args:
        cell: An openpyxl cell object with a `value` attribute.

    Returns:
        The detected number of decimal places (0-5).
    """
    value = getattr(cell, "value", None)
    if value is None:
        return 0

    try:
        float_val = float(value)
    except (TypeError, ValueError):
        return 0

    # Reason: Round to 5 decimals first to clean floating-point artifacts,
    # then strip trailing zeros to find the actual display precision.
    rounded = f"{float_val:.5f}"
    _, decimal_part = rounded.split(".")
    stripped = decimal_part.rstrip("0")
    return len(stripped)
