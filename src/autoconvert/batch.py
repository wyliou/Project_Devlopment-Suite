"""batch -- FR-001, FR-003, FR-028: Batch orchestration, file scanning, and directory management.

Orchestrates the full per-file pipeline: open workbook, detect sheets,
map columns, extract data, transform, allocate weights, validate, and
write output.  ``run_batch()`` manages directory setup, file scanning,
clearing ``data/finished/``, and collecting results.
"""

import logging
import os
import stat
import time
from pathlib import Path

import openpyxl

from .column_map import detect_header_row, extract_inv_no_from_header, map_columns
from .errors import ErrorCode, ProcessingError, WarningCode
from .extract_invoice import extract_invoice_items
from .extract_packing import extract_packing_items, validate_merged_weights
from .extract_totals import detect_total_row, extract_totals
from .merge_tracker import MergeTracker
from .models import AppConfig, BatchResult, FileResult, InvoiceItem, PackingTotals
from .output import write_template
from .report import print_batch_summary
from .sheet_detect import detect_sheets
from .transform import clean_po_number, convert_country, convert_currency
from .validate import determine_file_status
from .weight_alloc import allocate_weights
from .xls_adapter import convert_xls_to_xlsx

logger = logging.getLogger(__name__)

_DATA_DIR = Path("data")
_FINISHED_DIR = Path("data") / "finished"
_SEPARATOR = "-" * 65


def run_batch(config: AppConfig) -> BatchResult:
    """Orchestrate full batch: setup dirs, clear finished, scan, process, collect.

    Args:
        config: Application configuration (pre-loaded, pre-validated by config.py).

    Returns:
        BatchResult with counts, timing, and per-file FileResult list.
    """
    _ensure_directories()
    file_list = _scan_files()

    if not file_list:
        logger.info("No processable files found in %s", _DATA_DIR)
        return BatchResult(
            total_files=0,
            success_count=0,
            attention_count=0,
            failed_count=0,
            processing_time=0.0,
            file_results=[],
            log_path=str((_DATA_DIR / "process_log.txt").resolve()),
        )

    _clear_finished_dir()
    start_time = time.monotonic()

    total = len(file_list)
    results: list[FileResult] = []
    for idx, filepath in enumerate(file_list, start=1):
        logger.info(_SEPARATOR)
        logger.info("[%d/%d] Processing: %s ...", idx, total, filepath.name)
        results.append(process_file(filepath, config))

    processing_time = time.monotonic() - start_time
    batch_result = BatchResult(
        total_files=total,
        success_count=sum(1 for r in results if r.status == "Success"),
        attention_count=sum(1 for r in results if r.status == "Attention"),
        failed_count=sum(1 for r in results if r.status == "Failed"),
        processing_time=processing_time,
        file_results=results,
        log_path=str((_DATA_DIR / "process_log.txt").resolve()),
    )
    print_batch_summary(batch_result)
    return batch_result


def process_file(filepath: Path, config: AppConfig) -> FileResult:
    """Per-file pipeline: open workbook, detect sheets, map columns,
    extract, transform, allocate, validate, output.

    Args:
        filepath: Absolute path to the input Excel file.
        config: Application configuration.

    Returns:
        FileResult with status, errors, warnings, invoice_items,
        packing_items, packing_totals.
    """
    errs: list[ProcessingError] = []
    warns: list[ProcessingError] = []
    inv_items: list[InvoiceItem] = []
    pack_items: list = []
    pack_totals: PackingTotals | None = None

    # Phase 1: Open Workbook
    workbook = None
    try:
        workbook = _open_workbook(filepath)
    except PermissionError:
        _record_err(
            errs, ErrorCode.ERR_010, f"File is locked or inaccessible: {filepath.name}", {"filename": filepath.name}
        )
    except Exception as exc:
        _record_err(
            errs,
            ErrorCode.ERR_011,
            f"File is corrupted or unreadable: {filepath.name} ({exc})",
            {"filename": filepath.name},
        )

    if errs or workbook is None:
        return _make_result(filepath, errs, warns)

    # Phase 2: Sheet Detection
    try:
        invoice_sheet, packing_sheet = detect_sheets(workbook, config)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    # Phase 3a: Invoice Column Mapping
    # Reason: MergeTracker MUST be initialized BEFORE detect_header_row / map_columns
    inv_mt = MergeTracker(invoice_sheet)
    try:
        inv_hdr = detect_header_row(invoice_sheet, "invoice", config)
    except ProcessingError as e:
        _collect(errs, e)
        # Still init packing MergeTracker before returning (for consistency)
        MergeTracker(packing_sheet)
        return _make_result(filepath, errs, warns)

    try:
        inv_cmap = map_columns(invoice_sheet, inv_hdr, "invoice", config)
    except ProcessingError as e:
        _collect(errs, e)
        MergeTracker(packing_sheet)
        return _make_result(filepath, errs, warns)

    # Phase 3b: Packing Column Mapping
    pack_mt = MergeTracker(packing_sheet)
    try:
        pack_hdr = detect_header_row(packing_sheet, "packing", config)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    try:
        pack_cmap = map_columns(packing_sheet, pack_hdr, "packing", config)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    # Phase 3c: Invoice Number Fallback
    inv_no_from_col = "inv_no" in inv_cmap.field_map
    inv_no_param: str | None = None
    if not inv_no_from_col:
        inv_no_param = extract_inv_no_from_header(invoice_sheet, config)

    # Phase 4: Data Extraction
    try:
        inv_items = extract_invoice_items(invoice_sheet, inv_cmap, inv_mt, inv_no_param)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    # [10b] ERR_021: verify inv_no is populated
    if inv_no_from_col:
        inv_no_val = inv_items[0].inv_no if inv_items else None
    else:
        inv_no_val = inv_no_param
    if not inv_no_val:
        _record_err(
            errs,
            ErrorCode.ERR_021,
            "Invoice number not found: neither column extraction nor header fallback produced a value.",
            {"filename": filepath.name},
        )
        return _make_result(filepath, errs, warns)

    try:
        pack_items, last_data_row = extract_packing_items(packing_sheet, pack_cmap, pack_mt)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    try:
        validate_merged_weights(pack_items, pack_mt, pack_cmap)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    try:
        total_row = detect_total_row(packing_sheet, last_data_row, pack_cmap, pack_mt)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    try:
        pack_totals = extract_totals(packing_sheet, total_row, pack_cmap)
    except ProcessingError as e:
        _collect(errs, e)

    # ATT_002 if total_packets is None
    if pack_totals is not None and pack_totals.total_packets is None:
        w = ProcessingError(
            code=WarningCode.ATT_002,
            message="Total packets not found in packing sheet.",
            context={"filename": filepath.name},
        )
        logger.warning("[%s] %s: %s", w.code.value, w.code.name, w.message)
        warns.append(w)

    if errs:
        return _make_result(filepath, errs, warns)
    assert pack_totals is not None

    # Phase 5: Transformation (warnings only, no short-circuit)
    inv_items, cur_w = convert_currency(inv_items, config)
    warns.extend(cur_w)
    inv_items, coo_w = convert_country(inv_items, config)
    warns.extend(coo_w)
    inv_items = clean_po_number(inv_items)

    # Phase 6: Weight Allocation
    try:
        inv_items = allocate_weights(inv_items, pack_items, pack_totals)
    except ProcessingError as e:
        _collect(errs, e)
        return _make_result(filepath, errs, warns)

    # Phase 7: Validation
    status = determine_file_status(errs, warns)

    # Phase 8: Output (only for Success or Attention)
    if status in ("Success", "Attention"):
        output_path = _FINISHED_DIR / f"{filepath.stem}_template.xlsx"
        try:
            write_template(inv_items, pack_totals, config, output_path)
        except ProcessingError as e:
            _collect(errs, e)
            status = determine_file_status(errs, warns)

    _log_file_status(status)
    return FileResult(
        filename=filepath.name,
        status=status,
        errors=errs,
        warnings=warns,
        invoice_items=inv_items,
        packing_items=pack_items,
        packing_totals=pack_totals,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _record_err(
    errs: list[ProcessingError],
    code: ErrorCode,
    message: str,
    context: dict,
) -> None:
    """Create a ProcessingError, log it, and append to the error list."""
    err = ProcessingError(code=code, message=message, context=context)
    logger.error("[%s] %s: %s", err.code.value, err.code.name, err.message)
    errs.append(err)


def _collect(errs: list[ProcessingError], e: ProcessingError) -> None:
    """Log and collect a caught ProcessingError."""
    logger.error("[%s] %s: %s", e.code.value, e.code.name, e.message)
    errs.append(e)


def _make_result(
    filepath: Path,
    errs: list[ProcessingError],
    warns: list[ProcessingError],
) -> FileResult:
    """Build a failed FileResult, log status, and return it."""
    status = determine_file_status(errs, warns)
    _log_file_status(status)
    return FileResult(
        filename=filepath.name,
        status=status,
        errors=errs,
        warnings=warns,
        invoice_items=[],
        packing_items=[],
        packing_totals=None,
    )


def _ensure_directories() -> None:
    """Create data/ and data/finished/ if they don't exist.

    Raises:
        PermissionError: If directory creation fails due to permissions.
    """
    for dir_path in (_DATA_DIR, _FINISHED_DIR):
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logger.error("Cannot create directory: %s", dir_path.resolve())
            raise


def _scan_files() -> list[Path]:
    """Scan data/ for .xlsx/.xls files, excluding temp and hidden files.

    Returns:
        Sorted list of Path objects for processable files.
    """
    files: list[Path] = []
    if not _DATA_DIR.exists():
        return files
    for entry in sorted(_DATA_DIR.iterdir()):
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in (".xlsx", ".xls"):
            continue
        if entry.name.startswith("~$"):
            logger.debug("Excluding temp file: %s", entry.name)
            continue
        if _is_hidden(entry):
            logger.debug("Excluding hidden file: %s", entry.name)
            continue
        files.append(entry)
    return files


def _is_hidden(filepath: Path) -> bool:
    """Check if a file has the Windows hidden attribute.

    Args:
        filepath: Path to the file to check.

    Returns:
        True if the file has the hidden attribute set.
    """
    try:
        file_stat = os.stat(filepath)
        # Reason: stat.FILE_ATTRIBUTE_HIDDEN is 2 on Windows. st_file_attributes
        # only exists on Windows; on other platforms this will be 0 via getattr.
        attrs = getattr(file_stat, "st_file_attributes", 0)
        return bool(attrs & stat.FILE_ATTRIBUTE_HIDDEN)
    except OSError:
        return False


def _clear_finished_dir() -> None:
    """Remove all existing files in data/finished/ before processing.

    Raises:
        PermissionError: If a file cannot be deleted.
    """
    if not _FINISHED_DIR.exists():
        return
    for entry in _FINISHED_DIR.iterdir():
        if entry.is_file():
            try:
                entry.unlink()
            except PermissionError:
                logger.error("Cannot delete file: %s", entry.resolve())
                raise


def _open_workbook(filepath: Path) -> openpyxl.Workbook:
    """Open an Excel file as an openpyxl Workbook.

    Args:
        filepath: Path to the Excel file.

    Returns:
        openpyxl Workbook object.

    Raises:
        PermissionError: If the file is locked (ERR_010).
        Exception: If the file is corrupted or unreadable (ERR_011).
    """
    if filepath.suffix.lower() == ".xls":
        return convert_xls_to_xlsx(filepath)
    return openpyxl.load_workbook(filepath, data_only=True)


def _log_file_status(status: str) -> None:
    """Log the final file processing status with appropriate level.

    Args:
        status: One of "Success", "Attention", "Failed".
    """
    if status == "Success":
        logger.info("SUCCESS")
    elif status == "Attention":
        logger.warning("ATTENTION")
    else:
        logger.error("FAILED")
