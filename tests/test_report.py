"""tests/test_report.py — Tests for report.print_batch_summary() per FR-033."""

import logging

import pytest

from autoconvert.errors import ErrorCode, ProcessingError, WarningCode
from autoconvert.models import BatchResult, FileResult
from autoconvert.report import print_batch_summary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_file_result(
    filename: str,
    status: str,
    errors: list[ProcessingError] | None = None,
    warnings: list[ProcessingError] | None = None,
) -> FileResult:
    """Build a minimal FileResult for use in tests.

    Args:
        filename (str): The input file name.
        status (str): Processing status string.
        errors (list[ProcessingError] | None): Hard errors; defaults to empty.
        warnings (list[ProcessingError] | None): Warnings; defaults to empty.

    Returns:
        FileResult: A populated FileResult with empty item lists.
    """
    return FileResult(
        filename=filename,
        status=status,
        errors=errors or [],
        warnings=warnings or [],
        invoice_items=[],
        packing_items=[],
        packing_totals=None,
    )


def _make_batch_result(
    file_results: list[FileResult],
    processing_time: float = 1.0,
    log_path: str = "/logs/process_log.txt",
) -> BatchResult:
    """Build a BatchResult from a list of FileResults with counts derived automatically.

    Args:
        file_results (list[FileResult]): Per-file results.
        processing_time (float): Total processing time in seconds.
        log_path (str): Path to the log file.

    Returns:
        BatchResult: A fully populated BatchResult.
    """
    success_count = sum(1 for fr in file_results if fr.status == "Success")
    attention_count = sum(1 for fr in file_results if fr.status == "Attention")
    failed_count = sum(1 for fr in file_results if fr.status == "Failed")
    return BatchResult(
        total_files=len(file_results),
        success_count=success_count,
        attention_count=attention_count,
        failed_count=failed_count,
        processing_time=processing_time,
        file_results=file_results,
        log_path=log_path,
    )


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


class TestPrintBatchSummary:
    """Test suite for print_batch_summary function."""

    def test_print_batch_summary_all_success(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test print_batch_summary when all 3 files succeed.

        Verifies separator lines, summary header, and correct counts appear in
        log output at INFO level. Confirms no FAILED or ATTENTION sections emitted.
        """
        file_results = [
            _make_file_result("file1.xlsx", "Success"),
            _make_file_result("file2.xlsx", "Success"),
            _make_file_result("file3.xlsx", "Success"),
        ]
        batch_result = _make_batch_result(file_results, processing_time=2.5)

        with caplog.at_level(logging.INFO, logger="autoconvert.report"):
            print_batch_summary(batch_result)

        log_text = caplog.text

        # Separator must appear (75 '=' characters)
        assert "=" * 75 in log_text
        # Summary header
        assert "BATCH PROCESSING SUMMARY" in log_text
        # Counts
        assert "Total files:        3" in log_text
        assert "Successful:         3" in log_text
        assert "Attention:          0" in log_text
        assert "Failed:             0" in log_text
        # No failed or attention sections
        assert "FAILED FILES:" not in log_text
        assert "FILES NEEDING ATTENTION:" not in log_text

    def test_print_batch_summary_failed_files_section(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test print_batch_summary emits FAILED FILES section for a failed file with ERR_020.

        Verifies the ERROR-level FAILED FILES header and the specific error code
        appear in the captured log output.
        """
        err = ProcessingError(
            code=ErrorCode.ERR_020,
            message="Column mapping failed: part_no not found",
            context={"filename": "bad_file.xlsx", "part_no": "P001"},
        )
        failed = _make_file_result("bad_file.xlsx", "Failed", errors=[err])
        batch_result = _make_batch_result([failed])

        with caplog.at_level(logging.DEBUG, logger="autoconvert.report"):
            print_batch_summary(batch_result)

        log_text = caplog.text

        assert "FAILED FILES:" in log_text
        assert "bad_file.xlsx:" in log_text
        assert "ERR_020" in log_text
        assert "Column mapping failed: part_no not found" in log_text
        # Attention section must NOT appear since there are no attention files
        assert "FILES NEEDING ATTENTION:" not in log_text

    def test_print_batch_summary_error_condensing(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test print_batch_summary condenses 3 ERR_030 errors into a single line with count.

        Three separate ERR_030 errors on different rows must be condensed to
        "ERR_030: ... (3 occurrences)" — not listed as 3 separate lines.
        """
        errors = [
            ProcessingError(
                code=ErrorCode.ERR_030,
                message="Missing required field: part_no",
                context={"filename": "multi.xlsx", "row": 5, "part_no": "A100"},
            ),
            ProcessingError(
                code=ErrorCode.ERR_030,
                message="Missing required field: part_no",
                context={"filename": "multi.xlsx", "row": 6, "part_no": "A101"},
            ),
            ProcessingError(
                code=ErrorCode.ERR_030,
                message="Missing required field: part_no",
                context={"filename": "multi.xlsx", "row": 7, "part_no": "A102"},
            ),
        ]
        failed = _make_file_result("multi.xlsx", "Failed", errors=errors)
        batch_result = _make_batch_result([failed])

        with caplog.at_level(logging.DEBUG, logger="autoconvert.report"):
            print_batch_summary(batch_result)

        log_text = caplog.text

        assert "ERR_030" in log_text
        assert "(3 occurrences)" in log_text
        # Must not appear as 3 separate ERR_030 lines — count exact occurrences
        # of the code in the log to confirm condensing
        err_030_count = log_text.count("ERR_030")
        assert err_030_count == 1, f"Expected 1 condensed ERR_030 line, got {err_030_count}"

    def test_print_batch_summary_attention_files_section(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test print_batch_summary emits FILES NEEDING ATTENTION section for ATT_003 warning.

        Verifies the WARNING-level attention header and the ATT_003 code appear in
        the captured log output when a file has Attention status.
        """
        warn = ProcessingError(
            code=WarningCode.ATT_003,
            message="Unstandardized currency: RMB",
            context={"filename": "attention.xlsx"},
        )
        attention = _make_file_result("attention.xlsx", "Attention", warnings=[warn])
        batch_result = _make_batch_result([attention])

        with caplog.at_level(logging.DEBUG, logger="autoconvert.report"):
            print_batch_summary(batch_result)

        log_text = caplog.text

        assert "FILES NEEDING ATTENTION:" in log_text
        assert "attention.xlsx:" in log_text
        assert "ATT_003" in log_text
        assert "Unstandardized currency: RMB" in log_text
        # No failed section since the file is Attention, not Failed
        assert "FAILED FILES:" not in log_text

    def test_print_batch_summary_processing_time_two_decimal_format(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test print_batch_summary formats processing_time=12.3456 as "12.35 seconds".

        The format must be exactly 2 decimal places; 12.3456 rounds to 12.35.
        """
        batch_result = _make_batch_result([], processing_time=12.3456)

        with caplog.at_level(logging.INFO, logger="autoconvert.report"):
            print_batch_summary(batch_result)

        log_text = caplog.text

        assert "12.35 seconds" in log_text
        # Ensure the un-rounded value does NOT appear
        assert "12.3456" not in log_text
