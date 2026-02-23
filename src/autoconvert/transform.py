"""transform — FR-018, FR-019, FR-020: Currency/country conversion and PO number cleaning."""

import logging

from .errors import ProcessingError, WarningCode
from .models import AppConfig, InvoiceItem
from .utils import normalize_lookup_key

logger = logging.getLogger(__name__)


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
    warnings: list[ProcessingError] = []

    for item in items:
        raw = item.currency
        normalized = normalize_lookup_key(raw)
        logger.debug("currency lookup: raw=%r normalized=%r", raw, normalized)

        if normalized in config.currency_lookup:
            target = config.currency_lookup[normalized]
            logger.debug("currency matched: %r -> %r", raw, target)
            item.currency = target
        else:
            msg = f"Currency value {raw!r} (normalized: {normalized!r}) not found in currency_lookup"
            logger.warning("[ATT_003] UNSTANDARDIZED_CURRENCY: %s", msg)
            warning = ProcessingError(
                code=WarningCode.ATT_003,
                message=msg,
                context={"raw_value": raw, "normalized_key": normalized},
            )
            warnings.append(warning)

    return items, warnings


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
    warnings: list[ProcessingError] = []

    for item in items:
        raw = item.coo
        normalized = normalize_lookup_key(raw)
        logger.debug("country lookup: raw=%r normalized=%r", raw, normalized)

        if normalized in config.country_lookup:
            target = config.country_lookup[normalized]
            logger.debug("country matched: %r -> %r", raw, target)
            item.coo = target
        else:
            msg = f"COO value {raw!r} (normalized: {normalized!r}) not found in country_lookup"
            logger.warning("[ATT_004] UNSTANDARDIZED_COO: %s", msg)
            warning = ProcessingError(
                code=WarningCode.ATT_004,
                message=msg,
                context={"raw_value": raw, "normalized_key": normalized},
            )
            warnings.append(warning)

    return items, warnings


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
    for item in items:
        item.po_no = _clean_po(item.po_no)
    return items


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _clean_po(po_no: str) -> str:
    """Clean a single PO number by stripping after the first delimiter.

    Finds the minimum index of '-', '.', '/' in the string and strips from
    that position onward. If the delimiter is at position 0, returns the
    original string unchanged (to avoid producing an empty PO number).

    Args:
        po_no: Raw purchase order number string.

    Returns:
        Cleaned PO number string.
    """
    if not po_no:
        return po_no

    # Collect positions of each delimiter; -1 means not found
    positions = [po_no.find(ch) for ch in ("-", ".", "/")]
    # Reason: Filter out -1 (not found) before finding minimum to avoid
    # treating "not found" as position -1 which would appear before position 0.
    found = [p for p in positions if p != -1]

    if not found:
        # No delimiter present — return unchanged
        return po_no

    idx = min(found)

    if idx == 0:
        # Reason: Delimiter at position 0 (e.g., "-PO12345") would produce an
        # empty prefix, which triggers downstream ERR_030. Preserve original.
        return po_no

    return po_no[:idx]
