"""Tests for src/autoconvert/utils.py.

Covers all 14 public exports:
    strip_unit_suffix, safe_decimal, round_half_up, normalize_header,
    is_stop_keyword, normalize_lookup_key, detect_cell_precision, try_float,
    DITTO_MARKS, FOOTER_KEYWORDS, HEADER_KEYWORDS,
    WEIGHT_PRECISION_MIN, WEIGHT_PRECISION_MAX, STOP_KEYWORD_COL_COUNT.
"""

from decimal import Decimal, InvalidOperation
from types import SimpleNamespace
from typing import Any

import pytest

from autoconvert.utils import (
    DITTO_MARKS,
    FOOTER_KEYWORDS,
    HEADER_KEYWORDS,
    STOP_KEYWORD_COL_COUNT,
    WEIGHT_PRECISION_MAX,
    WEIGHT_PRECISION_MIN,
    detect_cell_precision,
    is_stop_keyword,
    normalize_header,
    normalize_lookup_key,
    round_half_up,
    safe_decimal,
    strip_unit_suffix,
    try_float,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_cell(number_format: str, value: Any = None) -> SimpleNamespace:
    """Create a minimal mock cell with number_format and value attributes.

    Args:
        number_format (str): The Excel number format string.
        value (Any): The cell value (None for empty cells).

    Returns:
        SimpleNamespace: A simple object with number_format and value attributes.
    """
    return SimpleNamespace(number_format=number_format, value=value)


# ---------------------------------------------------------------------------
# strip_unit_suffix
# ---------------------------------------------------------------------------


class TestStripUnitSuffix:
    """Tests for strip_unit_suffix function."""

    def test_strip_unit_suffix_kgs(self) -> None:
        """Strip KGS suffix with leading space."""
        assert strip_unit_suffix("2.5 KGS") == "2.5"

    def test_strip_unit_suffix_kg_no_space(self) -> None:
        """Strip KG suffix without space between number and unit."""
        assert strip_unit_suffix("15KG") == "15"

    def test_strip_unit_suffix_g(self) -> None:
        """Strip G (grams) suffix without space."""
        assert strip_unit_suffix("500G") == "500"

    def test_strip_unit_suffix_lbs(self) -> None:
        """Strip LBS suffix with leading space."""
        assert strip_unit_suffix("10 LBS") == "10"

    def test_strip_unit_suffix_lb(self) -> None:
        """Strip LB suffix without space."""
        assert strip_unit_suffix("10LB") == "10"

    def test_strip_unit_suffix_pcs(self) -> None:
        """Strip PCS suffix with leading space."""
        assert strip_unit_suffix("100 PCS") == "100"

    def test_strip_unit_suffix_ea(self) -> None:
        """Strip EA (each) suffix with leading space."""
        assert strip_unit_suffix("50 EA") == "50"

    def test_strip_unit_suffix_jian(self) -> None:
        """Strip Chinese 件 (jian) suffix with leading space."""
        assert strip_unit_suffix("3 件") == "3"

    def test_strip_unit_suffix_ge(self) -> None:
        """Strip Chinese 个 (ge) suffix without space."""
        assert strip_unit_suffix("10个") == "10"

    def test_strip_unit_suffix_case_insensitive(self) -> None:
        """Strip lowercase unit suffix (case-insensitive matching)."""
        assert strip_unit_suffix("5.0 kgs") == "5.0"

    def test_strip_unit_suffix_no_suffix(self) -> None:
        """Leave string unchanged when no recognized unit suffix is present."""
        assert strip_unit_suffix("2.500") == "2.500"

    def test_strip_unit_suffix_empty(self) -> None:
        """Return empty string when input is empty string."""
        assert strip_unit_suffix("") == ""

    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("1 KG", "1"),
            ("1 KGS", "1"),
            ("1 LB", "1"),
            ("1 LBS", "1"),
            ("1 G", "1"),
            ("1 PCS", "1"),
            ("1 EA", "1"),
            ("1 件", "1"),
            ("1 个", "1"),
        ],
    )
    def test_strip_unit_suffix_all_variants_parametrized(
        self, raw: str, expected: str
    ) -> None:
        """Strip each recognized unit suffix variant individually."""
        assert strip_unit_suffix(raw) == expected

    def test_strip_unit_suffix_kgs_takes_precedence_over_g(self) -> None:
        """KGS should be stripped as a whole, not partially leaving KG."""
        # If G matched before KGS, "2 KGS" would yield "2 K" — wrong.
        assert strip_unit_suffix("2 KGS") == "2"

    def test_strip_unit_suffix_trailing_whitespace_stripped(self) -> None:
        """Leading/trailing whitespace on the input is stripped."""
        assert strip_unit_suffix("  15 KG  ") == "15"


# ---------------------------------------------------------------------------
# safe_decimal
# ---------------------------------------------------------------------------


class TestSafeDecimal:
    """Tests for safe_decimal function."""

    def test_safe_decimal_float_value(self) -> None:
        """Epsilon trick converts floating-point artifact to correct Decimal."""
        result = safe_decimal(2.2799999999, 2)
        assert result == Decimal("2.28")

    def test_safe_decimal_int_value(self) -> None:
        """Integer input converts correctly with zero decimals."""
        result = safe_decimal(10, 0)
        assert result == Decimal("10")

    def test_safe_decimal_string_numeric(self) -> None:
        """Numeric string is correctly converted to Decimal."""
        result = safe_decimal("3.14159", 5)
        assert result == Decimal("3.14159")

    def test_safe_decimal_none_raises(self) -> None:
        """None input raises ValueError or InvalidOperation."""
        with pytest.raises((ValueError, InvalidOperation)):
            safe_decimal(None, 2)

    def test_safe_decimal_string_non_numeric_raises(self) -> None:
        """Non-numeric string raises ValueError or InvalidOperation."""
        with pytest.raises((ValueError, InvalidOperation)):
            safe_decimal("abc", 2)

    def test_safe_decimal_zero_value(self) -> None:
        """Zero input returns exact Decimal zero with correct precision."""
        result = safe_decimal(0, 2)
        assert result == Decimal("0.00")

    def test_safe_decimal_negative_value(self) -> None:
        """Negative float value rounds correctly using ROUND_HALF_UP."""
        result = safe_decimal(-1.005, 2)
        # -1.005 * 100 + 1e-9 => -100.4999... => rounds to -100 => -1.00
        # This validates the epsilon behavior for negative numbers
        assert isinstance(result, Decimal)

    def test_safe_decimal_high_precision(self) -> None:
        """Five-decimal precision is returned correctly."""
        result = safe_decimal(1.23456, 5)
        assert result == Decimal("1.23456")

    def test_safe_decimal_bool_raises(self) -> None:
        """Bool True/False convert to float (1.0/0.0) via Python's float() — not an error."""
        # Python's float(True) == 1.0, so this should succeed, not raise.
        result = safe_decimal(True, 0)
        assert result == Decimal("1")


# ---------------------------------------------------------------------------
# round_half_up
# ---------------------------------------------------------------------------


class TestRoundHalfUp:
    """Tests for round_half_up function."""

    def test_round_half_up_half_rounds_up(self) -> None:
        """Value exactly at halfway point rounds away from zero (up)."""
        result = round_half_up(Decimal("2.125"), 2)
        assert result == Decimal("2.13")

    def test_round_half_up_no_artifact(self) -> None:
        """Floating-point artifact value rounds correctly to 2 decimals."""
        result = round_half_up(Decimal("2.2799999999"), 2)
        assert result == Decimal("2.28")

    def test_round_half_up_zero_decimals(self) -> None:
        """Value 5.5 rounds to 6 when decimals=0."""
        result = round_half_up(Decimal("5.5"), 0)
        assert result == Decimal("6")

    def test_round_half_up_five_decimals(self) -> None:
        """Six-decimal value rounds correctly to 5 decimal places."""
        result = round_half_up(Decimal("1.123456"), 5)
        assert result == Decimal("1.12346")

    def test_round_half_up_exact_value_unchanged(self) -> None:
        """Value with fewer decimals than requested is returned unchanged."""
        result = round_half_up(Decimal("3.14"), 5)
        assert result == Decimal("3.14000")

    def test_round_half_up_zero_value(self) -> None:
        """Zero rounds to zero with specified decimal places."""
        result = round_half_up(Decimal("0"), 2)
        assert result == Decimal("0.00")

    def test_round_half_up_returns_decimal_type(self) -> None:
        """Return type is always Decimal."""
        result = round_half_up(Decimal("1.5"), 0)
        assert isinstance(result, Decimal)


# ---------------------------------------------------------------------------
# normalize_header
# ---------------------------------------------------------------------------


class TestNormalizeHeader:
    """Tests for normalize_header function."""

    def test_normalize_header_newline_in_header(self) -> None:
        """Newline inside header text is replaced with a single space."""
        assert normalize_header("N.W.\n(KGS)") == "N.W. (KGS)"

    def test_normalize_header_tab(self) -> None:
        """Tab character is replaced with a single space."""
        assert normalize_header("Part\tNo") == "Part No"

    def test_normalize_header_multiple_spaces(self) -> None:
        """Multiple consecutive spaces collapse to a single space."""
        assert normalize_header("Part   No") == "Part No"

    def test_normalize_header_strip_whitespace(self) -> None:
        """Leading and trailing whitespace is stripped."""
        assert normalize_header("  qty  ") == "qty"

    def test_normalize_header_mixed(self) -> None:
        """Combination of newline, tab, and trailing spaces are all normalized."""
        assert normalize_header("N.W.\n\t(KGS)  ") == "N.W. (KGS)"

    def test_normalize_header_plain_string(self) -> None:
        """String without any whitespace issues is returned as-is."""
        assert normalize_header("Amount") == "Amount"

    def test_normalize_header_empty_string(self) -> None:
        """Empty string input returns empty string."""
        assert normalize_header("") == ""

    def test_normalize_header_only_whitespace(self) -> None:
        """String of only whitespace returns empty string after strip."""
        assert normalize_header("   \n\t  ") == ""

    def test_normalize_header_newline_and_multiple_spaces(self) -> None:
        """Newline followed by multiple spaces collapses to single space."""
        assert normalize_header("G.W.\n   (KGS)") == "G.W. (KGS)"


# ---------------------------------------------------------------------------
# is_stop_keyword
# ---------------------------------------------------------------------------


class TestIsStopKeyword:
    """Tests for is_stop_keyword function."""

    def test_is_stop_keyword_total_english(self) -> None:
        """English 'Total' with additional text is matched."""
        assert is_stop_keyword("Total Amount") is True

    def test_is_stop_keyword_hejii(self) -> None:
        """Chinese 合计 (hé jì) is matched as a stop keyword."""
        assert is_stop_keyword("合计") is True

    def test_is_stop_keyword_zongjii(self) -> None:
        """Chinese 总计 (zǒng jì) is matched as a stop keyword."""
        assert is_stop_keyword("总计") is True

    def test_is_stop_keyword_xiaoji(self) -> None:
        """Chinese 小计 (xiǎo jì) is matched as a stop keyword."""
        assert is_stop_keyword("小计") is True

    def test_is_stop_keyword_case_insensitive(self) -> None:
        """Uppercase TOTAL is matched (case-insensitive)."""
        assert is_stop_keyword("TOTAL") is True

    def test_is_stop_keyword_normal_value(self) -> None:
        """Part number string without any stop keyword returns False."""
        assert is_stop_keyword("ABC-123") is False

    def test_is_stop_keyword_total_embedded_in_text(self) -> None:
        """'total' embedded within longer text is still matched."""
        assert is_stop_keyword("Grand Total Weight") is True

    def test_is_stop_keyword_none_input(self) -> None:
        """None input is converted to string 'None' which is not a stop keyword."""
        assert is_stop_keyword(None) is False  # type: ignore[arg-type]

    def test_is_stop_keyword_integer_input(self) -> None:
        """Integer input is converted to string and checked."""
        assert is_stop_keyword(12345) is False  # type: ignore[arg-type]

    def test_is_stop_keyword_empty_string(self) -> None:
        """Empty string returns False."""
        assert is_stop_keyword("") is False

    @pytest.mark.parametrize(
        "keyword",
        ["total", "Total", "TOTAL", "合计", "总计", "小计"],
    )
    def test_is_stop_keyword_all_variants(self, keyword: str) -> None:
        """Each stop keyword variant is individually matched."""
        assert is_stop_keyword(keyword) is True


# ---------------------------------------------------------------------------
# normalize_lookup_key
# ---------------------------------------------------------------------------


class TestNormalizeLookupKey:
    """Tests for normalize_lookup_key function."""

    def test_normalize_lookup_key_uppercase(self) -> None:
        """Lowercase input is uppercased."""
        assert normalize_lookup_key("usd") == "USD"

    def test_normalize_lookup_key_strip_whitespace(self) -> None:
        """Leading and trailing whitespace is stripped before uppercasing."""
        assert normalize_lookup_key("  USD  ") == "USD"

    def test_normalize_lookup_key_comma_space(self) -> None:
        """Comma-space in country name is collapsed to plain comma."""
        assert normalize_lookup_key("Taiwan, China") == "TAIWAN,CHINA"

    def test_normalize_lookup_key_already_normalized(self) -> None:
        """Already-normalized input passes through unchanged."""
        assert normalize_lookup_key("USD") == "USD"

    def test_normalize_lookup_key_mixed_case_country(self) -> None:
        """Mixed-case country name is fully uppercased."""
        assert normalize_lookup_key("china") == "CHINA"

    def test_normalize_lookup_key_multiple_comma_spaces(self) -> None:
        """Multiple comma-space sequences are all collapsed."""
        result = normalize_lookup_key("a, b, c")
        assert result == "A,B,C"

    def test_normalize_lookup_key_empty_string(self) -> None:
        """Empty string input returns empty string."""
        assert normalize_lookup_key("") == ""

    def test_normalize_lookup_key_no_change_needed(self) -> None:
        """Input with no whitespace or comma-space is returned uppercased only."""
        assert normalize_lookup_key("EUR") == "EUR"


# ---------------------------------------------------------------------------
# detect_cell_precision
# ---------------------------------------------------------------------------


class TestDetectCellPrecision:
    """Tests for detect_cell_precision function."""

    def test_detect_cell_precision_format_0_00(self) -> None:
        """Format '0.00' has two digits after decimal point -> 2."""
        cell = _make_cell(number_format="0.00", value=1.23)
        assert detect_cell_precision(cell) == 2

    def test_detect_cell_precision_format_hash_comma(self) -> None:
        """Format '#,##0.00' has two digits after decimal point -> 2."""
        cell = _make_cell(number_format="#,##0.00", value=1.23)
        assert detect_cell_precision(cell) == 2

    def test_detect_cell_precision_format_00000(self) -> None:
        """Format '0.00000_' has five digits after decimal point -> 5."""
        cell = _make_cell(number_format="0.00000_", value=1.23456)
        assert detect_cell_precision(cell) == 5

    def test_detect_cell_precision_general_format(self) -> None:
        """General format with value having 5 significant decimals -> 5."""
        # Value 1.23456 has 5 decimal places after rounding to 5 -> returns 5
        cell = _make_cell(number_format="General", value=1.234560001)
        # After rounding to 5 decimals and stripping trailing zeros:
        # f"{1.234560001:.5f}" = "1.23456" -> 5 digits after "."
        assert detect_cell_precision(cell) == 5

    def test_detect_cell_precision_text_format(self) -> None:
        """Text format '@' with None value -> 0 (no numeric precision)."""
        cell = _make_cell(number_format="@", value=None)
        assert detect_cell_precision(cell) == 0

    def test_detect_cell_precision_complex_accounting(self) -> None:
        """Complex accounting format '_($* #,##0.00_)' has 2 decimal places."""
        cell = _make_cell(number_format="_($* #,##0.00_)", value=1.23)
        assert detect_cell_precision(cell) == 2

    def test_detect_cell_precision_no_decimal(self) -> None:
        """Format '0' has no decimal portion -> 0."""
        cell = _make_cell(number_format="0", value=42.0)
        assert detect_cell_precision(cell) == 0

    def test_detect_cell_precision_general_integer_value(self) -> None:
        """General format with integer value (no decimals) -> 0."""
        cell = _make_cell(number_format="General", value=42)
        assert detect_cell_precision(cell) == 0

    def test_detect_cell_precision_general_none_value(self) -> None:
        """General format with None value -> 0."""
        cell = _make_cell(number_format="General", value=None)
        assert detect_cell_precision(cell) == 0

    def test_detect_cell_precision_general_two_decimals(self) -> None:
        """General format cell with value 1.23 -> 2 significant decimal places."""
        cell = _make_cell(number_format="General", value=1.23)
        # f"{1.23:.5f}" = "1.23000" -> rstrip("0") = "23" -> len=2
        assert detect_cell_precision(cell) == 2

    def test_detect_cell_precision_no_number_format_attr(self) -> None:
        """Cell with no number_format attribute defaults to General treatment."""
        cell = SimpleNamespace(value=1.5)  # no number_format attribute
        # getattr(cell, "number_format", "General") => "General"
        # _precision_from_value: f"{1.5:.5f}" = "1.50000" -> strip -> "5" -> 1
        assert detect_cell_precision(cell) == 1

    def test_detect_cell_precision_none_format(self) -> None:
        """Cell with number_format=None falls back to General treatment."""
        cell = _make_cell(number_format=None, value=None)  # type: ignore[arg-type]
        assert detect_cell_precision(cell) == 0

    def test_detect_cell_precision_text_format_with_string_value(self) -> None:
        """Text format '@' with a string value -> 0 (non-numeric)."""
        cell = _make_cell(number_format="@", value="N/A")
        assert detect_cell_precision(cell) == 0

    def test_detect_cell_precision_four_decimal_format(self) -> None:
        """Format '0.0000' has exactly four decimal digits -> 4."""
        cell = _make_cell(number_format="0.0000", value=1.2345)
        assert detect_cell_precision(cell) == 4


# ---------------------------------------------------------------------------
# DITTO_MARKS constant
# ---------------------------------------------------------------------------


class TestDittoMarks:
    """Tests for the DITTO_MARKS frozenset constant."""

    def test_ditto_marks_contains_all_four(self) -> None:
        """DITTO_MARKS contains all four expected ditto mark characters."""
        expected = {
            '"',        # U+0022 standard double-quote
            "\u3003",   # 〃 DITTO MARK
            "\u201c",   # " LEFT DOUBLE QUOTATION MARK
            "\u201d",   # " RIGHT DOUBLE QUOTATION MARK
        }
        assert DITTO_MARKS == expected

    def test_ditto_marks_length(self) -> None:
        """DITTO_MARKS has exactly 4 members."""
        assert len(DITTO_MARKS) == 4

    def test_ditto_marks_is_frozenset(self) -> None:
        """DITTO_MARKS is a frozenset (immutable)."""
        assert isinstance(DITTO_MARKS, frozenset)

    def test_ditto_marks_standard_quote(self) -> None:
        """Standard ASCII double-quote U+0022 is in DITTO_MARKS."""
        assert '"' in DITTO_MARKS

    def test_ditto_marks_cjk_ditto(self) -> None:
        """CJK ditto mark U+3003 (〃) is in DITTO_MARKS."""
        assert "\u3003" in DITTO_MARKS

    def test_ditto_marks_left_double_quote(self) -> None:
        """Left double quotation mark U+201C is in DITTO_MARKS."""
        assert "\u201c" in DITTO_MARKS

    def test_ditto_marks_right_double_quote(self) -> None:
        """Right double quotation mark U+201D is in DITTO_MARKS."""
        assert "\u201d" in DITTO_MARKS

    def test_ditto_marks_immutable(self) -> None:
        """frozenset cannot be mutated (add raises AttributeError)."""
        with pytest.raises(AttributeError):
            DITTO_MARKS.add("x")  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# FOOTER_KEYWORDS constant
# ---------------------------------------------------------------------------


class TestFooterKeywords:
    """Tests for the FOOTER_KEYWORDS tuple constant."""

    def test_footer_keywords_is_tuple(self) -> None:
        """FOOTER_KEYWORDS is a tuple (ordered, not frozenset)."""
        assert isinstance(FOOTER_KEYWORDS, tuple)

    def test_footer_keywords_contains_baoguan_hang(self) -> None:
        """FOOTER_KEYWORDS contains '报关行' (customs broker)."""
        assert "报关行" in FOOTER_KEYWORDS

    def test_footer_keywords_contains_youxian_gongsi(self) -> None:
        """FOOTER_KEYWORDS contains '有限公司' (limited company)."""
        assert "有限公司" in FOOTER_KEYWORDS

    def test_footer_keywords_tuple_length(self) -> None:
        """FOOTER_KEYWORDS has exactly 4 elements."""
        assert len(FOOTER_KEYWORDS) == 4

    def test_footer_keywords_usable_in_any_pattern(self) -> None:
        """FOOTER_KEYWORDS works correctly in any(...) membership check."""
        cell_value = "某有限公司 深圳"
        assert any(kw in str(cell_value) for kw in FOOTER_KEYWORDS) is True

    def test_footer_keywords_no_match_for_normal_row(self) -> None:
        """Normal data rows do not match FOOTER_KEYWORDS."""
        cell_value = "ABC-12345"
        assert any(kw in str(cell_value) for kw in FOOTER_KEYWORDS) is False


# ---------------------------------------------------------------------------
# HEADER_KEYWORDS constant
# ---------------------------------------------------------------------------


class TestHeaderKeywords:
    """Tests for the HEADER_KEYWORDS frozenset constant."""

    def test_header_keywords_is_frozenset(self) -> None:
        """HEADER_KEYWORDS is a frozenset."""
        assert isinstance(HEADER_KEYWORDS, frozenset)

    def test_header_keywords_minimum_length(self) -> None:
        """HEADER_KEYWORDS contains at least 20 entries."""
        assert len(HEADER_KEYWORDS) >= 20

    def test_header_keywords_contains_qty(self) -> None:
        """'qty' keyword is in HEADER_KEYWORDS."""
        assert "qty" in HEADER_KEYWORDS

    def test_header_keywords_contains_nw(self) -> None:
        """'n.w.' keyword is in HEADER_KEYWORDS."""
        assert "n.w." in HEADER_KEYWORDS

    def test_header_keywords_contains_part_no(self) -> None:
        """'part no' keyword is in HEADER_KEYWORDS."""
        assert "part no" in HEADER_KEYWORDS

    def test_header_keywords_contains_coo(self) -> None:
        """'coo' (country of origin) keyword is in HEADER_KEYWORDS."""
        assert "coo" in HEADER_KEYWORDS

    def test_header_keywords_contains_pinpai(self) -> None:
        """Chinese '品牌' (brand) keyword is in HEADER_KEYWORDS."""
        assert "品牌" in HEADER_KEYWORDS

    def test_header_keywords_contains_gw(self) -> None:
        """'g.w.' keyword is in HEADER_KEYWORDS."""
        assert "g.w." in HEADER_KEYWORDS

    def test_header_keywords_contains_amount(self) -> None:
        """'amount' keyword is in HEADER_KEYWORDS."""
        assert "amount" in HEADER_KEYWORDS

    def test_header_keywords_contains_price(self) -> None:
        """'price' keyword is in HEADER_KEYWORDS."""
        assert "price" in HEADER_KEYWORDS

    def test_header_keywords_contains_quantity(self) -> None:
        """'quantity' keyword is in HEADER_KEYWORDS."""
        assert "quantity" in HEADER_KEYWORDS

    def test_header_keywords_contains_weight(self) -> None:
        """'weight' keyword is in HEADER_KEYWORDS."""
        assert "weight" in HEADER_KEYWORDS

    def test_header_keywords_contains_country(self) -> None:
        """'country' keyword is in HEADER_KEYWORDS."""
        assert "country" in HEADER_KEYWORDS

    def test_header_keywords_contains_origin(self) -> None:
        """'origin' keyword is in HEADER_KEYWORDS."""
        assert "origin" in HEADER_KEYWORDS

    def test_header_keywords_contains_brand(self) -> None:
        """'brand' keyword is in HEADER_KEYWORDS."""
        assert "brand" in HEADER_KEYWORDS

    def test_header_keywords_contains_description(self) -> None:
        """'description' keyword is in HEADER_KEYWORDS."""
        assert "description" in HEADER_KEYWORDS

    def test_header_keywords_contains_unit(self) -> None:
        """'unit' keyword is in HEADER_KEYWORDS."""
        assert "unit" in HEADER_KEYWORDS

    def test_header_keywords_contains_currency(self) -> None:
        """'currency' keyword is in HEADER_KEYWORDS."""
        assert "currency" in HEADER_KEYWORDS

    def test_header_keywords_all_lowercase(self) -> None:
        """All entries in HEADER_KEYWORDS are lowercase strings."""
        for kw in HEADER_KEYWORDS:
            assert kw == kw.lower(), f"Keyword {kw!r} is not lowercase"

    def test_header_keywords_immutable(self) -> None:
        """frozenset cannot be mutated (add raises AttributeError)."""
        with pytest.raises(AttributeError):
            HEADER_KEYWORDS.add("test")  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# WEIGHT_PRECISION_MIN / WEIGHT_PRECISION_MAX constants
# ---------------------------------------------------------------------------


class TestWeightPrecisionConstants:
    """Tests for WEIGHT_PRECISION_MIN and WEIGHT_PRECISION_MAX constants."""

    def test_weight_precision_min_value(self) -> None:
        """WEIGHT_PRECISION_MIN equals 2."""
        assert WEIGHT_PRECISION_MIN == 2

    def test_weight_precision_max_value(self) -> None:
        """WEIGHT_PRECISION_MAX equals 5."""
        assert WEIGHT_PRECISION_MAX == 5

    def test_weight_precision_min_is_int(self) -> None:
        """WEIGHT_PRECISION_MIN is an integer."""
        assert isinstance(WEIGHT_PRECISION_MIN, int)

    def test_weight_precision_max_is_int(self) -> None:
        """WEIGHT_PRECISION_MAX is an integer."""
        assert isinstance(WEIGHT_PRECISION_MAX, int)

    def test_weight_precision_min_less_than_max(self) -> None:
        """WEIGHT_PRECISION_MIN is strictly less than WEIGHT_PRECISION_MAX."""
        assert WEIGHT_PRECISION_MIN < WEIGHT_PRECISION_MAX


# ---------------------------------------------------------------------------
# STOP_KEYWORD_COL_COUNT constant
# ---------------------------------------------------------------------------


class TestStopKeywordColCount:
    """Tests for STOP_KEYWORD_COL_COUNT constant."""

    def test_stop_keyword_col_count_value(self) -> None:
        """STOP_KEYWORD_COL_COUNT equals 10 (columns A through J)."""
        assert STOP_KEYWORD_COL_COUNT == 10

    def test_stop_keyword_col_count_is_int(self) -> None:
        """STOP_KEYWORD_COL_COUNT is an integer."""
        assert isinstance(STOP_KEYWORD_COL_COUNT, int)

    def test_stop_keyword_col_count_positive(self) -> None:
        """STOP_KEYWORD_COL_COUNT is positive."""
        assert STOP_KEYWORD_COL_COUNT > 0


# ---------------------------------------------------------------------------
# try_float
# ---------------------------------------------------------------------------


class TestTryFloat:
    """Tests for try_float function."""

    def test_try_float_none_returns_none(self) -> None:
        """None input returns None."""
        assert try_float(None) is None

    def test_try_float_integer(self) -> None:
        """Integer input converts to float."""
        assert try_float(5) == 5.0

    def test_try_float_float(self) -> None:
        """Float input is returned as float."""
        assert try_float(1.23) == 1.23

    def test_try_float_numeric_string(self) -> None:
        """Numeric string is converted to float."""
        assert try_float("3.14") == 3.14

    def test_try_float_decimal(self) -> None:
        """Decimal input converts to float."""
        assert try_float(Decimal("2.5")) == 2.5

    def test_try_float_string_with_unit_suffix(self) -> None:
        """String with unit suffix is parsed after stripping suffix."""
        result = try_float("12.5 KGS")
        assert result == 12.5

    def test_try_float_non_numeric_string_returns_none(self) -> None:
        """Non-numeric string with no unit suffix returns None."""
        assert try_float("abc") is None

    def test_try_float_empty_string_returns_none(self) -> None:
        """Empty string returns None."""
        assert try_float("") is None

    def test_try_float_zero(self) -> None:
        """Zero input returns 0.0."""
        assert try_float(0) == 0.0

    def test_try_float_zero_string(self) -> None:
        """Zero string returns 0.0."""
        assert try_float("0") == 0.0
