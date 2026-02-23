"""Tests for column_map.py — FR-007, FR-008, FR-009."""

import re
from pathlib import Path

import pytest
from openpyxl import Workbook

from autoconvert.column_map import (
    detect_header_row,
    extract_inv_no_from_header,
    map_columns,
)
from autoconvert.errors import ErrorCode, ProcessingError
from autoconvert.models import AppConfig, FieldPattern

# ---------------------------------------------------------------------------
# Helpers — create minimal AppConfig for tests
# ---------------------------------------------------------------------------


def _make_config(
    *,
    invoice_columns: dict[str, FieldPattern] | None = None,
    packing_columns: dict[str, FieldPattern] | None = None,
    inv_no_patterns: list[re.Pattern[str]] | None = None,
    inv_no_label_patterns: list[re.Pattern[str]] | None = None,
    inv_no_exclude_patterns: list[re.Pattern[str]] | None = None,
) -> AppConfig:
    """Build a minimal AppConfig for testing column_map functions.

    Returns:
        AppConfig with sensible defaults for unspecified fields.
    """
    if invoice_columns is None:
        invoice_columns = _default_invoice_columns()
    if packing_columns is None:
        packing_columns = _default_packing_columns()
    if inv_no_patterns is None:
        inv_no_patterns = [
            re.compile(r"INVOICE\s*NO\.?\s*[:：]\s*(\S+)", re.IGNORECASE),
            re.compile(r"INV\.?\s*NO\.?\s*[:：]\s*(\S+)", re.IGNORECASE),
        ]
    if inv_no_label_patterns is None:
        inv_no_label_patterns = [
            re.compile(r"^INV\.?\s*NO\.?\s*[:：]?$", re.IGNORECASE),
            re.compile(r"(?i)^invoice\s*no\.?\s*[:：]?$", re.IGNORECASE),
        ]
    if inv_no_exclude_patterns is None:
        inv_no_exclude_patterns = [
            re.compile(r"(?i)^invoice\s*no\.?[:：]?"),
            re.compile(r"^\d{4}-\d{2}-\d{2}"),
            re.compile(r"\d{4}/\d{1,2}/\d{1,2}"),
        ]

    return AppConfig(
        invoice_sheet_patterns=[re.compile(r"^invoice", re.IGNORECASE)],
        packing_sheet_patterns=[re.compile(r"^packing", re.IGNORECASE)],
        invoice_columns=invoice_columns,
        packing_columns=packing_columns,
        inv_no_patterns=inv_no_patterns,
        inv_no_label_patterns=inv_no_label_patterns,
        inv_no_exclude_patterns=inv_no_exclude_patterns,
        currency_lookup={},
        country_lookup={},
        template_path=Path("dummy_template.xlsx"),
    )


def _default_invoice_columns() -> dict[str, FieldPattern]:
    """Build default invoice column patterns matching real config."""
    return {
        "part_no": FieldPattern(patterns=[r"(?i)^part\s*no"], type="string", required=True),
        "po_no": FieldPattern(patterns=[r"(?i)^p\.?o\.?\s*no"], type="string", required=True),
        "qty": FieldPattern(patterns=[r"(?i)^qty", r"(?i)^quantity"], type="numeric", required=True),
        "price": FieldPattern(patterns=[r"(?i)^unit\s*price", r"(?i)^price"], type="numeric", required=True),
        "amount": FieldPattern(patterns=[r"(?i)^amount"], type="currency", required=True),
        "currency": FieldPattern(
            patterns=[r"(?i)^currency", r"^USD$", r"^CNY$", r"^EUR$"],
            type="string",
            required=True,
        ),
        "coo": FieldPattern(patterns=[r"(?i)^c\.?o\.?o\.?$", r"(?i)country.*origin"], type="string", required=True),
        "brand": FieldPattern(patterns=[r"(?i)^brand$"], type="string", required=True),
        "brand_type": FieldPattern(patterns=[r"(?i)品牌类型"], type="string", required=True),
        "model": FieldPattern(patterns=[r"(?i)^model", r"(?i)型号"], type="string", required=True),
        "cod": FieldPattern(patterns=[r"(?i)^c\.?o\.?d\.?$"], type="string", required=False),
        "weight": FieldPattern(patterns=[r"(?i)^n\.?w\.?"], type="numeric", required=False),
        "inv_no": FieldPattern(patterns=[r"(?i)^inv\.?\s*no"], type="string", required=False),
        "serial": FieldPattern(patterns=[r"(?i)项号"], type="string", required=False),
    }


def _default_packing_columns() -> dict[str, FieldPattern]:
    """Build default packing column patterns matching real config."""
    return {
        "part_no": FieldPattern(patterns=[r"(?i)^part\s*no"], type="string", required=True),
        "po_no": FieldPattern(patterns=[r"(?i)^p\.?o\.?\s*no"], type="string", required=False),
        "qty": FieldPattern(patterns=[r"(?i)^qty"], type="numeric", required=True),
        "nw": FieldPattern(
            patterns=[r"(?i)^n\.?w\.?$", r"(?i)n\.?w\.?.*kg", r"(?i)^n\.?w\.?\s*\(kg"],
            type="numeric",
            required=True,
        ),
        "gw": FieldPattern(
            patterns=[r"(?i)^g\.?w\.?", r"(?i)^g\.?m\.?", r"(?i)^g\.?m\.?\s*\(kg"],
            type="numeric",
            required=True,
        ),
        "pack": FieldPattern(patterns=[r"(?i)^cartons?$"], type="numeric", required=False),
    }


def _make_sheet(row_data: dict[int, list[object]]) -> Workbook:
    """Create an in-memory workbook with a single sheet populated from row_data.

    Args:
        row_data: Dict mapping 1-based row number -> list of cell values.
            Values are placed starting at column 1.

    Returns:
        Workbook (use wb.active to get the Worksheet).
    """
    wb = Workbook()
    ws = wb.active
    for row_idx, values in row_data.items():
        for col_idx, value in enumerate(values, start=1):
            ws.cell(row=row_idx, column=col_idx, value=value)
    return wb


# ===========================================================================
# detect_header_row() Tests
# ===========================================================================


class TestDetectHeaderRow:
    """Tests for detect_header_row (FR-007)."""

    def test_detect_header_row_invoice_tier0_wins(self) -> None:
        """Row 10 has 8 cells including keywords (Tier 0) and beats row 8 (Tier 1)."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            # Row 8: 7 non-empty cells, no keywords -> Tier 1
            8: ["A", "B", "C", "D", "E", "F", "G"],
            # Row 10: 8 cells including "qty", "part no", "price" -> Tier 0
            10: ["qty", "part no", "price", "amount", "brand", "model", "coo", "po no"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        result = detect_header_row(ws, "invoice", config)

        assert result == 10

    def test_detect_header_row_tie_earliest_row(self) -> None:
        """Two Tier 0 rows; earlier row (row 9) selected over row 11."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            9: ["qty", "part no", "price", "amount", "brand", "model", "coo", "po no"],
            11: ["qty", "part no", "price", "amount", "brand", "model", "coo", "po no"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        result = detect_header_row(ws, "invoice", config)

        assert result == 9

    def test_detect_header_row_metadata_row_demoted(self) -> None:
        """Row 12 has 8 cells including 'Tel:' (Tier 2). Row 14 has keywords (Tier 0). Row 14 wins."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            # Row 12: 8 cells with Tel: marker -> Tier 2
            12: ["Company", "Tel: 123", "Fax:", "Address", "City", "State", "Zip", "Country"],
            # Row 14: 7 cells with keywords -> Tier 0
            14: ["qty", "part no", "price", "amount", "brand", "model", "coo"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        result = detect_header_row(ws, "invoice", config)

        assert result == 14

    def test_detect_header_row_packing_threshold_4(self) -> None:
        """Packing sheet: row with exactly 4 non-empty cells qualifies."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            10: ["Part No", "Qty", "N.W.", "G.W."],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        result = detect_header_row(ws, "packing", config)

        assert result == 10

    def test_detect_header_row_no_qualifying_row_raises_err014(self) -> None:
        """All rows have <= 3 non-empty cells; raises ERR_014."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            10: ["A", "B", "C"],
            15: ["X", "Y"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        with pytest.raises(ProcessingError) as exc_info:
            detect_header_row(ws, "invoice", config)

        assert exc_info.value.code == ErrorCode.ERR_014

    def test_detect_header_row_unnamed_prefix_excluded(self) -> None:
        """Cells with 'Unnamed:' prefix are not counted toward density."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            # 3 real cells + 5 "Unnamed:" = 8 total but only 3 count
            10: [
                "qty",
                "part no",
                "price",
                "Unnamed:0",
                "Unnamed:1",
                "Unnamed:2",
                "Unnamed:3",
                "Unnamed:4",
            ],
            # Row 15 has 7 genuine cells with keywords
            15: ["qty", "part no", "price", "amount", "brand", "model", "coo"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        result = detect_header_row(ws, "invoice", config)

        # Row 10 doesn't meet threshold (3 < 7), row 15 does
        assert result == 15

    def test_detect_header_row_data_like_row_is_tier2(self) -> None:
        """Row with 5+ pure numeric cells is Tier 2 even with many non-empty cells."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            # Row 10: 8 cells, 5 are pure numbers -> Tier 2 (data-like)
            10: ["12345", "67890", "111", "222", "333", "some text", "more text", "extra"],
            # Row 14: 7 cells with keywords -> Tier 0
            14: ["qty", "part no", "price", "amount", "brand", "model", "coo"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        result = detect_header_row(ws, "invoice", config)

        assert result == 14

    def test_detect_header_row_scan_range_7_to_30(self) -> None:
        """Header in row 6 (below start) and row 31 (above end) are not found."""
        config = _make_config()
        row_data: dict[int, list[object]] = {
            # Row 6 is out of scan range (below start)
            6: ["qty", "part no", "price", "amount", "brand", "model", "coo"],
            # Row 31 is out of scan range (above end)
            31: ["qty", "part no", "price", "amount", "brand", "model", "coo"],
        }
        wb = _make_sheet(row_data)
        ws = wb.active

        with pytest.raises(ProcessingError) as exc_info:
            detect_header_row(ws, "invoice", config)

        assert exc_info.value.code == ErrorCode.ERR_014


# ===========================================================================
# map_columns() Tests
# ===========================================================================


class TestMapColumns:
    """Tests for map_columns (FR-008)."""

    def test_map_columns_all_required_invoice_found(self) -> None:
        """10 required invoice columns present; ColumnMapping contains all with correct indices."""
        config = _make_config()
        # Build a header row with all 10 required fields
        headers = [
            "Part No",  # col 1 -> part_no
            "PO No",  # col 2 -> po_no
            "Qty",  # col 3 -> qty
            "Unit Price",  # col 4 -> price
            "Amount",  # col 5 -> amount
            "Currency",  # col 6 -> currency
            "COO",  # col 7 -> coo
            "Brand",  # col 8 -> brand
            "品牌类型",  # col 9 -> brand_type
            "Model",  # col 10 -> model
        ]
        wb = _make_sheet({10: headers})
        ws = wb.active

        result = map_columns(ws, 10, "invoice", config)

        assert result.sheet_type == "invoice"
        assert result.header_row == 10
        assert result.effective_header_row == 10
        assert result.field_map["part_no"] == 1
        assert result.field_map["po_no"] == 2
        assert result.field_map["qty"] == 3
        assert result.field_map["price"] == 4
        assert result.field_map["amount"] == 5
        assert result.field_map["currency"] == 6
        assert result.field_map["coo"] == 7
        assert result.field_map["brand"] == 8
        assert result.field_map["brand_type"] == 9
        assert result.field_map["model"] == 10

    def test_map_columns_missing_required_raises_err020_with_all_names(self) -> None:
        """Currency and coo absent; single ERR_020 lists both field names."""
        config = _make_config()
        # 8 of 10 required fields (missing currency and coo)
        headers = [
            "Part No",
            "PO No",
            "Qty",
            "Unit Price",
            "Amount",
            "Brand",
            "品牌类型",
            "Model",
        ]
        wb = _make_sheet({10: headers})
        ws = wb.active

        with pytest.raises(ProcessingError) as exc_info:
            map_columns(ws, 10, "invoice", config)

        err = exc_info.value
        assert err.code == ErrorCode.ERR_020
        assert "coo" in err.message
        assert "currency" in err.message
        assert "coo" in err.context["missing_fields"]
        assert "currency" in err.context["missing_fields"]

    def test_map_columns_sub_header_fallback_advances_effective_row(self) -> None:
        """Primary header has partial match; sub-header has N.W. and G.W.; effective row advances."""
        config = _make_config()
        # Primary header row 10: has part_no and qty but missing nw and gw
        primary_headers = ["Part No", "Qty", None, None]
        # Sub-header row 11: has N.W.(KGS) and G.M.(KGS) for nw and gw
        sub_headers = [None, None, "N.W.(KGS)", "G.M.(KGS)"]
        wb = _make_sheet({10: primary_headers, 11: sub_headers})
        ws = wb.active

        result = map_columns(ws, 10, "packing", config)

        assert result.effective_header_row == 11
        assert result.field_map["nw"] == 3
        assert result.field_map["gw"] == 4

    def test_map_columns_sub_header_guard_rejected_if_data_like(self) -> None:
        """Row header_row+1 has 4 numeric cells; sub-header scan rejected."""
        config = _make_config()
        # Primary: has part_no and qty but missing nw, gw
        primary_headers = ["Part No", "Qty", None, None, None, None]
        # Sub-header row: data-like (4 numeric cells)
        sub_row = [None, None, "1234", "5678", "9012", "3456"]
        wb = _make_sheet({10: primary_headers, 11: sub_row})
        ws = wb.active

        with pytest.raises(ProcessingError) as exc_info:
            map_columns(ws, 10, "packing", config)

        # nw and gw are still missing because sub-header was rejected
        err = exc_info.value
        assert err.code == ErrorCode.ERR_020
        assert "nw" in err.context["missing_fields"]
        assert "gw" in err.context["missing_fields"]

    def test_map_columns_currency_data_row_fallback_shifts_price(self) -> None:
        """No currency column; 'USD' found at col 5 in data row; price shifts from 5 to 6."""
        config = _make_config()
        # Header without currency column; price maps to col 5 initially
        headers = [
            "Part No",  # col 1
            "PO No",  # col 2
            "Qty",  # col 3
            "Amount",  # col 4
            "Price",  # col 5 (but actual data has USD here, price at col 6)
            None,  # col 6
            "COO",  # col 7
            "Brand",  # col 8
            "品牌类型",  # col 9
            "Model",  # col 10
        ]
        # Data row: col 5 has "USD", col 6 has the actual price
        data_row = ["ABC-001", "PO-100", 100, 500.00, "USD", 5.00, "TW", "BrandX", "境内", "M-1"]
        wb = _make_sheet({10: headers, 11: data_row})
        ws = wb.active

        result = map_columns(ws, 10, "invoice", config)

        # Price should have shifted from col 5 to col 6
        assert result.field_map["price"] == 6
        # Currency should be detected at col 5
        assert result.field_map["currency"] == 5

    def test_map_columns_currency_fallback_shifts_both_price_and_amount(self) -> None:
        """Two currency columns embedded; both price and amount shift +1."""
        config = _make_config()
        # Header: price at col 4, amount at col 6 — both will be where USD sits
        headers = [
            "Part No",  # col 1
            "PO No",  # col 2
            "Qty",  # col 3
            "Price",  # col 4 (currency will be here)
            None,  # col 5 (actual price)
            "Amount",  # col 6 (currency will be here too)
            None,  # col 7 (actual amount)
            "COO",  # col 8
            "Brand",  # col 9
            "品牌类型",  # col 10
            "Model",  # col 11
        ]
        # Data row: "USD" at col 4 and col 6
        data_row = [
            "ABC-001",
            "PO-100",
            100,
            "USD",
            5.00,  # price col 4 has USD, col 5 has actual price
            "USD",
            500.00,  # amount col 6 has USD, col 7 has actual amount
            "TW",
            "BrandX",
            "境内",
            "M-1",
        ]
        wb = _make_sheet({10: headers, 11: data_row})
        ws = wb.active

        result = map_columns(ws, 10, "invoice", config)

        # Both should shift +1
        assert result.field_map["price"] == 5
        assert result.field_map["amount"] == 7
        # Currency detected
        assert "currency" in result.field_map

    def test_map_columns_case_insensitive_regex_match(self) -> None:
        """Header 'N.W. (KGS)' matched by pattern n\\.w\\. (case-insensitive)."""
        config = _make_config()
        headers = ["Part No", "Qty", "N.W. (KGS)", "G.W."]
        wb = _make_sheet({10: headers})
        ws = wb.active

        result = map_columns(ws, 10, "packing", config)

        assert result.field_map["nw"] == 3

    def test_map_columns_packing_optional_fields_absent_no_error(self) -> None:
        """po_no and pack absent from packing sheet; no ERR_020 raised."""
        config = _make_config()
        # Only the 4 required packing fields
        headers = ["Part No", "Qty", "N.W.", "G.W."]
        wb = _make_sheet({10: headers})
        ws = wb.active

        result = map_columns(ws, 10, "packing", config)

        assert "po_no" not in result.field_map
        assert "pack" not in result.field_map
        assert result.field_map["part_no"] == 1
        assert result.field_map["qty"] == 2
        assert result.field_map["nw"] == 3
        assert result.field_map["gw"] == 4


# ===========================================================================
# extract_inv_no_from_header() Tests
# ===========================================================================


class TestExtractInvNoFromHeader:
    """Tests for extract_inv_no_from_header (FR-009)."""

    def test_extract_inv_no_capture_group_pattern(self) -> None:
        """Cell has 'INVOICE NO.: INV2025-001'; capture extracts and cleans to '2025-001'."""
        config = _make_config()
        wb = _make_sheet({3: [None, "INVOICE NO.: INV2025-001"]})
        ws = wb.active

        result = extract_inv_no_from_header(ws, config)

        assert result == "2025-001"

    def test_extract_inv_no_label_right_adjacent(self) -> None:
        """Label 'Invoice No.' at row 3, col 2; value 'INV-001' at col 4 (within +3)."""
        config = _make_config()
        wb = _make_sheet(
            {
                3: [None, "Invoice No.", None, "INV-001"],
            }
        )
        ws = wb.active

        result = extract_inv_no_from_header(ws, config)

        assert result == "INV-001"

    def test_extract_inv_no_label_two_rows_below(self) -> None:
        """Label at row 3 col 1; row+1 has date (excluded); row+2 has 'INV-2025-009'."""
        config = _make_config()
        wb = _make_sheet(
            {
                3: ["Invoice No."],
                4: ["2025-01-15"],  # Date - excluded by exclude pattern
                5: ["INV-2025-009"],
            }
        )
        ws = wb.active

        result = extract_inv_no_from_header(ws, config)

        assert result == "INV-2025-009"

    def test_extract_inv_no_not_found_returns_none(self) -> None:
        """No inv_no pattern matches rows 1-15; returns None (no exception)."""
        config = _make_config()
        wb = _make_sheet(
            {
                1: ["Company Name"],
                2: ["Some other info"],
                3: ["Date: 2025-01-01"],
            }
        )
        ws = wb.active

        result = extract_inv_no_from_header(ws, config)

        assert result is None

    def test_extract_inv_no_exclude_pattern_filters_date(self) -> None:
        """Captured value '2025-01-15' matches exclude date pattern; returns None."""
        config = _make_config(
            inv_no_patterns=[
                # A very loose capture pattern that would match a date
                re.compile(r"NO\.?\s*[:：]\s*(\S+)", re.IGNORECASE),
            ],
            inv_no_exclude_patterns=[
                re.compile(r"^\d{4}-\d{2}-\d{2}"),
            ],
        )
        wb = _make_sheet(
            {
                3: ["No.: 2025-01-15"],
            }
        )
        ws = wb.active

        result = extract_inv_no_from_header(ws, config)

        assert result is None
