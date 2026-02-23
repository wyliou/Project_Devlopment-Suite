"""Tests for transform.py — FR-018, FR-019, FR-020: Currency/country conversion and PO cleaning."""

import re
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from autoconvert.errors import ProcessingError, WarningCode
from autoconvert.models import AppConfig, InvoiceItem
from autoconvert.transform import clean_po_number, convert_country, convert_currency

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_item(
    currency: str = "USD",
    coo: str = "CN",
    po_no: str = "PO12345",
) -> InvoiceItem:
    """Create a minimal InvoiceItem for transform tests.

    Args:
        currency: Currency string field value.
        coo: Country of origin field value.
        po_no: Purchase order number field value.

    Returns:
        InvoiceItem with sensible defaults for all other required fields.
    """
    return InvoiceItem(
        part_no="PART-001",
        po_no=po_no,
        qty=Decimal("10"),
        price=Decimal("1.50000"),
        amount=Decimal("15.00"),
        currency=currency,
        coo=coo,
        cod="US",
        brand="BrandA",
        brand_type="TypeA",
        model_no="MOD-001",
        inv_no="INV-001",
        serial="",
    )


def _make_config(
    currency_lookup: dict[str, str] | None = None,
    country_lookup: dict[str, str] | None = None,
) -> AppConfig:
    """Create a minimal AppConfig with known lookup tables.

    Args:
        currency_lookup: Mapping of normalized currency keys to target codes.
        country_lookup: Mapping of normalized country keys to target codes.

    Returns:
        AppConfig instance suitable for transform tests.
    """
    # Reason: AppConfig requires many regex/Pattern fields that are not relevant
    # to transform tests. We provide valid empty-list defaults for those fields
    # and only populate the lookup tables under test.
    return AppConfig(
        invoice_sheet_patterns=[],
        packing_sheet_patterns=[],
        invoice_columns={},
        packing_columns={},
        inv_no_patterns=[],
        inv_no_label_patterns=[],
        inv_no_exclude_patterns=[],
        currency_lookup=currency_lookup or {},
        country_lookup=country_lookup or {},
        template_path=Path("template.xlsx"),
    )


# ---------------------------------------------------------------------------
# convert_currency() tests
# ---------------------------------------------------------------------------


class TestConvertCurrency:
    """Tests for convert_currency() (FR-018)."""

    def test_convert_currency_usd_matches_502(self) -> None:
        """Test convert_currency when currency='USD' matches lookup entry for '502'."""
        items = [_make_item(currency="USD")]
        config = _make_config(currency_lookup={"USD": "502"})

        result_items, warnings = convert_currency(items, config)

        assert result_items[0].currency == "502"
        assert warnings == []

    def test_convert_currency_chinese_meiyuan_matches_502(self) -> None:
        """Test convert_currency when currency='美元' also maps to '502'."""
        items = [_make_item(currency="美元")]
        config = _make_config(currency_lookup={"USD": "502", "美元": "502"})

        result_items, warnings = convert_currency(items, config)

        assert result_items[0].currency == "502"
        assert warnings == []

    def test_convert_currency_case_insensitive_normalization(self) -> None:
        """Test convert_currency normalizes 'usd' to 'USD' before lookup."""
        # The lookup table key is stored as "USD" (uppercase after normalization).
        # Input "usd" must be normalized to "USD" to find the match.
        items = [_make_item(currency="usd")]
        config = _make_config(currency_lookup={"USD": "502"})

        result_items, warnings = convert_currency(items, config)

        assert result_items[0].currency == "502"
        assert warnings == []

    def test_convert_currency_unmatched_returns_att003_warning(self) -> None:
        """Test convert_currency preserves unmatched currency and returns ATT_003 warning."""
        items = [_make_item(currency="EUR")]
        config = _make_config(currency_lookup={"USD": "502"})

        result_items, warnings = convert_currency(items, config)

        # Currency value preserved as-is (raw passthrough)
        assert result_items[0].currency == "EUR"
        # Exactly one ATT_003 warning
        assert len(warnings) == 1
        assert isinstance(warnings[0], ProcessingError)
        assert warnings[0].code == WarningCode.ATT_003

    def test_convert_currency_multiple_items_mixed_match(self) -> None:
        """Test convert_currency with two items: one matched (USD), one unmatched (GBP)."""
        items = [
            _make_item(currency="USD"),
            _make_item(currency="GBP"),
        ]
        config = _make_config(currency_lookup={"USD": "502"})

        result_items, warnings = convert_currency(items, config)

        # USD matched and converted
        assert result_items[0].currency == "502"
        # GBP not in lookup — preserved as-is
        assert result_items[1].currency == "GBP"
        # Exactly one warning for the unmatched GBP item
        assert len(warnings) == 1
        assert warnings[0].code == WarningCode.ATT_003


# ---------------------------------------------------------------------------
# convert_country() tests
# ---------------------------------------------------------------------------


class TestConvertCountry:
    """Tests for convert_country() (FR-019)."""

    def test_convert_country_taiwan_comma_china_normalization(self) -> None:
        """Test convert_country collapses ', ' to ',' for 'Taiwan, China' -> 'TAIWAN,CHINA'."""
        # normalize_lookup_key("Taiwan, China") -> "TAIWAN,CHINA"
        items = [_make_item(coo="Taiwan, China")]
        config = _make_config(country_lookup={"TAIWAN,CHINA": "158"})

        result_items, warnings = convert_country(items, config)

        assert result_items[0].coo == "158"
        assert warnings == []

    def test_convert_country_iso_code_cn(self) -> None:
        """Test convert_country matches ISO code 'CN' directly."""
        items = [_make_item(coo="CN")]
        config = _make_config(country_lookup={"CN": "156"})

        result_items, warnings = convert_country(items, config)

        assert result_items[0].coo == "156"
        assert warnings == []

    def test_convert_country_unmatched_returns_att004_warning(self) -> None:
        """Test convert_country preserves unmatched COO and returns ATT_004 warning."""
        items = [_make_item(coo="XYZ")]
        config = _make_config(country_lookup={"CN": "156"})

        result_items, warnings = convert_country(items, config)

        # COO value preserved as-is
        assert result_items[0].coo == "XYZ"
        # Exactly one ATT_004 warning
        assert len(warnings) == 1
        assert isinstance(warnings[0], ProcessingError)
        assert warnings[0].code == WarningCode.ATT_004

    def test_convert_country_empty_coo_preserved_as_empty(self) -> None:
        """Test convert_country with empty coo string: preserved as empty, ATT_004 issued."""
        # Empty coo is not in any lookup table — treat as unmatched per spec.
        items = [_make_item(coo="")]
        config = _make_config(country_lookup={"CN": "156"})

        result_items, warnings = convert_country(items, config)

        # Empty string preserved (not replaced with None or other value)
        assert result_items[0].coo == ""
        # One ATT_004 warning for the empty unmatched value
        assert len(warnings) == 1
        assert warnings[0].code == WarningCode.ATT_004

    def test_convert_country_mixed_int_str_target_code_normalized_by_config(self) -> None:
        """Test convert_country receives str target codes (config.py normalizes ints to str)."""
        # config.py normalizes Target_Code int values to str before storing.
        # transform.py receives str and stores it as str in item.coo.
        items = [_make_item(coo="US")]
        # Simulate config.py having converted int 840 to str "840"
        config = _make_config(country_lookup={"US": "840"})

        result_items, warnings = convert_country(items, config)

        assert result_items[0].coo == "840"
        assert isinstance(result_items[0].coo, str)
        assert warnings == []


# ---------------------------------------------------------------------------
# clean_po_number() tests
# ---------------------------------------------------------------------------


class TestCleanPoNumber:
    """Tests for clean_po_number() (FR-020)."""

    def test_clean_po_number_dash_delimiter(self) -> None:
        """Test clean_po_number strips from first '-' delimiter: '2250600556-2.1' -> '2250600556'."""
        items = [_make_item(po_no="2250600556-2.1")]

        result = clean_po_number(items)

        assert result[0].po_no == "2250600556"

    def test_clean_po_number_dot_delimiter(self) -> None:
        """Test clean_po_number strips from first '.' delimiter: 'PO32741.0' -> 'PO32741'."""
        items = [_make_item(po_no="PO32741.0")]

        result = clean_po_number(items)

        assert result[0].po_no == "PO32741"

    def test_clean_po_number_slash_delimiter(self) -> None:
        """Test clean_po_number strips from first delimiter in 'PO-001/A' (dash at idx 2) -> 'PO'."""
        # "PO-001/A": '-' at index 2, '/' at index 6 — minimum is 2.
        # Result: "PO-001/A"[:2] = "PO"
        items = [_make_item(po_no="PO-001/A")]

        result = clean_po_number(items)

        assert result[0].po_no == "PO"

    def test_clean_po_number_delimiter_at_position_0_preserved(self) -> None:
        """Test clean_po_number preserves po_no when delimiter is at position 0."""
        # "-PO12345": delimiter at index 0 -> return original unchanged.
        items = [_make_item(po_no="-PO12345")]

        result = clean_po_number(items)

        assert result[0].po_no == "-PO12345"

    def test_clean_po_number_no_delimiter(self) -> None:
        """Test clean_po_number returns po_no unchanged when no delimiter found."""
        items = [_make_item(po_no="PO12345")]

        result = clean_po_number(items)

        assert result[0].po_no == "PO12345"
