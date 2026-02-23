"""models — Pydantic data models for all entities (InvoiceItem, PackingItem, etc.)."""

import re
from decimal import Decimal
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from .errors import ProcessingError


class InvoiceItem(BaseModel):
    """A single line item extracted from an invoice sheet (FR-011).

    Note: The field name is ``model_no`` (not ``model``) to avoid collision with
    pydantic's reserved ``model`` class method (Ambiguity #8). All downstream
    modules must reference ``item.model_no``.

    Fields:
        part_no: Part number string.
        po_no: Purchase order number string.
        qty: Quantity as Decimal (cell display precision).
        price: Unit price as Decimal (5 decimals).
        amount: Line amount as Decimal (2 decimals).
        currency: Currency code string (e.g. "USD").
        coo: Country of origin code. May be empty string if column absent.
        cod: Country of destination code. May be empty string if column absent.
        brand: Brand name string.
        brand_type: Brand type string.
        model_no: Model number string (PRD entity name: ``model``).
        inv_no: Invoice number string. May be empty string if column absent.
        serial: Serial number string. May be empty string if column absent.
        allocated_weight: Net weight allocated to this item; None until
            weight_alloc.py populates it.
    """

    part_no: str
    po_no: str
    qty: Decimal
    price: Decimal
    amount: Decimal
    currency: str
    coo: str
    cod: str
    brand: str
    brand_type: str
    model_no: str
    inv_no: str
    serial: str
    allocated_weight: Decimal | None = None


class PackingItem(BaseModel):
    """A single line item extracted from a packing sheet (FR-012).

    Fields:
        part_no: Part number string.
        qty: Quantity as Decimal (cell display precision).
        nw: Net weight as Decimal (5 decimals).
        is_first_row_of_merge: True for normal single-row items and merge anchor
            rows; False for non-anchor merge continuation rows, ditto-mark rows,
            and implicit continuation rows. Used by weight_alloc.py to determine
            which rows contribute weight.
    """

    part_no: str
    qty: Decimal
    nw: Decimal
    is_first_row_of_merge: bool


class PackingTotals(BaseModel):
    """Totals extracted from the packing sheet totals row (FR-015/FR-016/FR-017).

    Fields:
        total_nw: Total net weight as Decimal.
        total_nw_precision: Detected format precision for total_nw (min 2, max 5).
            Used by weight_alloc.py to round allocated weights consistently.
        total_gw: Total gross weight as Decimal.
        total_gw_precision: Detected format precision for total_gw (min 2, max 5).
        total_packets: Number of shipping packets; optional per FR-017.
    """

    total_nw: Decimal
    total_nw_precision: int
    total_gw: Decimal
    total_gw_precision: int
    total_packets: int | None = None


class ColumnMapping(BaseModel):
    """Result of column detection for one sheet (FR-007/FR-008).

    Fields:
        sheet_type: Either ``"invoice"`` or ``"packing"``.
        field_map: Maps field name (e.g. ``"part_no"``) to 1-based column index
            (openpyxl convention). Consumers use ``sheet.cell(row=r, column=col_idx)``.
        header_row: 1-based row number of the detected header row.
        effective_header_row: Equals ``header_row`` unless a sub-header scan
            advanced it to ``header_row + 1``. Data extraction starts at
            ``effective_header_row + 1``.
    """

    sheet_type: str
    field_map: dict[str, int]
    header_row: int
    effective_header_row: int


class MergeRange(BaseModel):
    """Represents a merged cell range captured before unmerging (FR-010).

    All indices are 1-based (openpyxl convention).
    ``value`` is the anchor cell's value at time of capture; may be None, str,
    int, float, or datetime.

    Fields:
        min_row: First row of the merge range (1-based).
        max_row: Last row of the merge range (1-based).
        min_col: First column of the merge range (1-based).
        max_col: Last column of the merge range (1-based).
        value: The anchor cell's value (Any type — not constrained).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    min_row: int
    max_row: int
    min_col: int
    max_col: int
    value: Any


class FieldPattern(BaseModel):
    """Pattern configuration for a single field used during column detection (FR-002).

    Fields:
        patterns: Raw regex strings (not compiled) for matching column headers.
        type: One of ``"string"``, ``"numeric"``, or ``"currency"``.
        required: Whether the field is required for extraction to proceed.
    """

    patterns: list[str]
    type: str
    required: bool


class AppConfig(BaseModel):
    """Application configuration loaded from field_patterns.yaml (FR-002).

    Stores compiled ``re.Pattern`` objects for sheet and field detection.
    ``arbitrary_types_allowed=True`` is required for ``re.Pattern`` and ``Path``.

    Fields:
        invoice_sheet_patterns: Compiled regex patterns for invoice sheet name detection.
        packing_sheet_patterns: Compiled regex patterns for packing sheet name detection.
        invoice_columns: Mapping of field name to FieldPattern for invoice columns.
        packing_columns: Mapping of field name to FieldPattern for packing columns.
        inv_no_patterns: Compiled regex patterns for invoice number value extraction.
        inv_no_label_patterns: Compiled regex patterns for invoice number label detection.
        inv_no_exclude_patterns: Compiled regex patterns for excluding false positives.
        currency_lookup: Maps normalized currency keys (uppercase) to output codes.
        country_lookup: Maps normalized country keys (uppercase) to output codes.
        template_path: Path to the Excel output template file.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    invoice_sheet_patterns: list[re.Pattern]  # type: ignore[type-arg]
    packing_sheet_patterns: list[re.Pattern]  # type: ignore[type-arg]
    invoice_columns: dict[str, FieldPattern]
    packing_columns: dict[str, FieldPattern]
    inv_no_patterns: list[re.Pattern]  # type: ignore[type-arg]
    inv_no_label_patterns: list[re.Pattern]  # type: ignore[type-arg]
    inv_no_exclude_patterns: list[re.Pattern]  # type: ignore[type-arg]
    currency_lookup: dict[str, str]
    country_lookup: dict[str, str]
    template_path: Path


class FileResult(BaseModel):
    """Processing result for a single Excel file (FR-027/FR-033).

    ``arbitrary_types_allowed=True`` is required because ``ProcessingError``
    is an Exception subclass, not a pydantic model.

    Fields:
        filename: The input file name (not full path).
        status: One of ``"Pending"``, ``"Success"``, ``"Attention"``, ``"Failed"``.
        errors: List of hard errors collected during processing.
        warnings: List of warnings (ATT_xxx) collected during processing.
        invoice_items: Extracted invoice line items.
        packing_items: Extracted packing line items.
        packing_totals: Extracted packing totals; None if extraction failed.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    filename: str
    status: str
    errors: list[ProcessingError]
    warnings: list[ProcessingError]
    invoice_items: list[InvoiceItem]
    packing_items: list[PackingItem]
    packing_totals: PackingTotals | None = None


class BatchResult(BaseModel):
    """Aggregate result for the entire batch run (FR-027).

    Fields:
        total_files: Total number of files processed.
        success_count: Number of files with ``"Success"`` status.
        attention_count: Number of files with ``"Attention"`` status.
        failed_count: Number of files with ``"Failed"`` status.
        processing_time: Total processing time in seconds.
        file_results: Per-file results in processing order.
        log_path: Absolute path string of the generated log file.
    """

    total_files: int
    success_count: int
    attention_count: int
    failed_count: int
    processing_time: float
    file_results: list[FileResult]
    log_path: str
