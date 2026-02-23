"""tests/test_diagnostic.py — Tests for cli.parse_args() and cli.main() exit codes."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from autoconvert import batch as _batch_module
from autoconvert.cli import main, parse_args
from autoconvert.errors import ConfigError, ErrorCode
from autoconvert.models import BatchResult, FileResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_file_result(status: str) -> FileResult:
    """Build a minimal FileResult with the given status.

    Args:
        status (str): One of "Success", "Attention", "Failed".

    Returns:
        FileResult: A minimal FileResult with empty item lists.
    """
    return FileResult(
        filename="test.xlsx",
        status=status,
        errors=[],
        warnings=[],
        invoice_items=[],
        packing_items=[],
        packing_totals=None,
    )


def _make_batch_result(failed_count: int) -> BatchResult:
    """Build a BatchResult with the given failed_count and one file result.

    Args:
        failed_count (int): Number of failed files (0 or 1).

    Returns:
        BatchResult: A minimal BatchResult for testing exit code logic.
    """
    if failed_count > 0:
        file_results = [_make_file_result("Failed")]
        success_count = 0
        attention_count = 0
    else:
        file_results = [_make_file_result("Success")]
        success_count = 1
        attention_count = 0
    return BatchResult(
        total_files=1,
        success_count=success_count,
        attention_count=attention_count,
        failed_count=failed_count,
        processing_time=0.1,
        file_results=file_results,
        log_path="/tmp/process_log.txt",
    )


# ---------------------------------------------------------------------------
# parse_args tests
# ---------------------------------------------------------------------------


class TestParseArgs:
    """Tests for parse_args() argument parsing."""

    def test_parse_args_no_args(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test parse_args returns diagnostic=None when no --diagnostic flag given.

        sys.argv contains only the program name (no extra flags).
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert"])
        namespace = parse_args()
        assert namespace.diagnostic is None

    def test_parse_args_diagnostic_flag(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test parse_args returns diagnostic='file.xlsx' when --diagnostic file.xlsx given.

        The diagnostic attribute must equal the string exactly as passed.
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert", "--diagnostic", "file.xlsx"])
        namespace = parse_args()
        assert namespace.diagnostic == "file.xlsx"


# ---------------------------------------------------------------------------
# main() exit code tests
# ---------------------------------------------------------------------------


class TestMainExitCodes:
    """Tests for main() exit codes via monkeypatching."""

    def test_main_exit_code_0_on_all_success(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Test main exits with code 0 when run_batch returns BatchResult with failed_count=0.

        Monkeypatches: sys.argv (normal mode), load_config, setup_logging,
        run_batch, and print_batch_summary.
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert"])

        # Patch load_config to return a mock config without touching the filesystem
        mock_config = MagicMock()
        monkeypatch.setattr("autoconvert.cli.load_config", lambda _: mock_config)

        # Patch setup_logging to avoid creating log files
        monkeypatch.setattr("autoconvert.cli.setup_logging", lambda _: None)

        # Patch run_batch to return a success BatchResult
        batch_result = _make_batch_result(failed_count=0)
        monkeypatch.setattr(_batch_module, "run_batch", lambda config: batch_result)

        # Patch print_batch_summary to avoid output side effects
        monkeypatch.setattr("autoconvert.cli.print_batch_summary", lambda _: None)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

    def test_main_exit_code_1_on_any_failed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Test main exits with code 1 when run_batch returns BatchResult with failed_count=1.

        Monkeypatches: sys.argv (normal mode), load_config, setup_logging,
        run_batch, and print_batch_summary.
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert"])

        mock_config = MagicMock()
        monkeypatch.setattr("autoconvert.cli.load_config", lambda _: mock_config)
        monkeypatch.setattr("autoconvert.cli.setup_logging", lambda _: None)

        batch_result = _make_batch_result(failed_count=1)
        monkeypatch.setattr(_batch_module, "run_batch", lambda config: batch_result)

        monkeypatch.setattr("autoconvert.cli.print_batch_summary", lambda _: None)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    def test_main_exit_code_2_on_config_error(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
    ) -> None:
        """Test main exits with code 2 when load_config raises ConfigError.

        Monkeypatches: sys.argv (normal mode), load_config to raise ConfigError.
        No batch or logging calls should occur.
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert"])

        config_error = ConfigError(
            code=ErrorCode.ERR_001,
            message="Required configuration file not found: field_patterns.yaml",
            path="/config/field_patterns.yaml",
        )
        monkeypatch.setattr("autoconvert.cli.load_config", lambda _: (_ for _ in ()).throw(config_error))

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 2

    def test_main_diagnostic_exit_code_0_on_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test main exits with code 0 in diagnostic mode when file status is Success.

        Monkeypatches: sys.argv (--diagnostic mode), load_config,
        setup_diagnostic_logging, and process_file.
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert", "--diagnostic", "invoice.xlsx"])

        mock_config = MagicMock()
        monkeypatch.setattr("autoconvert.cli.load_config", lambda _: mock_config)
        monkeypatch.setattr("autoconvert.cli.setup_diagnostic_logging", lambda _: None)

        success_result = _make_file_result("Success")
        monkeypatch.setattr(_batch_module, "process_file", lambda path, config: success_result)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

    def test_main_diagnostic_exit_code_1_on_failed(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test main exits with code 1 in diagnostic mode when file status is Failed.

        Monkeypatches: sys.argv (--diagnostic mode), load_config,
        setup_diagnostic_logging, and process_file.
        """
        monkeypatch.setattr(sys, "argv", ["autoconvert", "--diagnostic", "bad_file.xlsx"])

        mock_config = MagicMock()
        monkeypatch.setattr("autoconvert.cli.load_config", lambda _: mock_config)
        monkeypatch.setattr("autoconvert.cli.setup_diagnostic_logging", lambda _: None)

        failed_result = _make_file_result("Failed")
        monkeypatch.setattr(_batch_module, "process_file", lambda path, config: failed_result)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
