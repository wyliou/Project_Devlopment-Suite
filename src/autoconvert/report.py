"""report — FR-033: Batch summary reporting."""

import logging
from collections import defaultdict

from .errors import ProcessingError
from .models import BatchResult

logger = logging.getLogger(__name__)

_SEPARATOR = "=" * 75


def _condense_errors(errors: list[ProcessingError]) -> list[tuple[str, str, str]]:
    """Condense repeated error codes into single entries with occurrence count.

    Groups errors by their code value. If a code appears more than once,
    a single condensed entry is produced with "(N occurrences)" appended.
    The representative part_no is taken from the first occurrence's context.

    Args:
        errors (list[ProcessingError]): Raw list of errors from a FileResult.

    Returns:
        list[tuple[str, str, str]]: Each tuple is (code_value, message, suffix)
            where suffix is "" for single occurrences or " (N occurrences)" for
            repeated codes. part_no context is embedded in the message string
            only when relevant; callers format the output line themselves.
    """
    # Group errors by code value — order of first occurrence is preserved
    # because dict insertion order is guaranteed in Python 3.7+.
    groups: dict[str, list[ProcessingError]] = defaultdict(list)
    for error in errors:
        groups[error.code.value].append(error)

    condensed: list[tuple[str, str, str]] = []
    for code_value, group in groups.items():
        first = group[0]
        message = first.message
        if len(group) > 1:
            suffix = f" ({len(group)} occurrences)"
        else:
            suffix = ""
        condensed.append((code_value, message, suffix))
    return condensed


def _condense_warnings(warnings: list[ProcessingError]) -> list[tuple[str, str]]:
    """Condense warnings into (code_value, message) pairs.

    Warnings are not condensed by the spec (no occurrence count shown for
    attention items), so each warning is emitted as a separate entry.

    Args:
        warnings (list[ProcessingError]): Raw list of warnings from a FileResult.

    Returns:
        list[tuple[str, str]]: Each tuple is (code_value, message).
    """
    return [(w.code.value, w.message) for w in warnings]


def print_batch_summary(batch_result: BatchResult) -> None:
    """Format and print batch summary to console per FR-033 format.

    Produces the summary always, even if all files failed or total_files == 0.
    Summary header is logged at INFO level. Failed files section at ERROR level.
    Files needing attention section at WARNING level.

    The separator line is exactly 75 '=' characters.
    Processing time is formatted to exactly 2 decimal places.
    Error condensing: repeated error codes per file are shown as
    "{code}: {message} (N occurrences)" with representative part_no from first.

    Args:
        batch_result: Completed batch result with all file results, counts,
                      timing, and log path.

    Returns:
        None. Outputs to console via logger (INFO/ERROR/WARNING level).
    """
    # --- Summary header (INFO) ---
    logger.info(_SEPARATOR)
    logger.info("                   BATCH PROCESSING SUMMARY")
    logger.info(_SEPARATOR)
    logger.info("Total files:        %d", batch_result.total_files)
    logger.info("Successful:         %d", batch_result.success_count)
    logger.info("Attention:          %d", batch_result.attention_count)
    logger.info("Failed:             %d", batch_result.failed_count)
    logger.info("Processing time:    %.2f seconds", batch_result.processing_time)
    logger.info("Log file:           %s", batch_result.log_path)
    logger.info(_SEPARATOR)

    # --- Failed files section (ERROR) — omitted if no failed files ---
    failed_files = [fr for fr in batch_result.file_results if fr.status == "Failed"]
    if failed_files:
        logger.error("FAILED FILES:")
        for file_result in failed_files:
            logger.error("  %s:", file_result.filename)
            for code_value, message, suffix in _condense_errors(file_result.errors):
                logger.error("    %s: %s%s", code_value, message, suffix)

    # --- Attention files section (WARNING) — omitted if no attention files ---
    attention_files = [fr for fr in batch_result.file_results if fr.status == "Attention"]
    if attention_files:
        logger.warning("FILES NEEDING ATTENTION:")
        for file_result in attention_files:
            logger.warning("  %s:", file_result.filename)
            for code_value, message in _condense_warnings(file_result.warnings):
                logger.warning("    %s: %s", code_value, message)
