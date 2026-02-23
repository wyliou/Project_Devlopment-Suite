"""tests/test_validate.py — Tests for validate.determine_file_status()."""

import pytest

from autoconvert.errors import ErrorCode
from autoconvert.errors import ProcessingError
from autoconvert.errors import WarningCode
from autoconvert.validate import determine_file_status


class TestDetermineFileStatus:
    """Test suite for determine_file_status function."""

    def test_determine_file_status_success_no_errors_no_warnings(self) -> None:
        """Test determine_file_status when no errors and no warnings; returns "Success"."""
        errors: list[ProcessingError] = []
        warnings: list[ProcessingError] = []

        status = determine_file_status(errors, warnings)

        assert status == "Success"

    def test_determine_file_status_failed_on_any_err(self) -> None:
        """Test determine_file_status when one ERR_020 ProcessingError; returns "Failed" regardless of warnings."""
        err = ProcessingError(
            code=ErrorCode.ERR_020,
            message="Header row not found",
            context={"filename": "test.xlsx"},
        )
        errors = [err]
        warnings: list[ProcessingError] = []

        status = determine_file_status(errors, warnings)

        assert status == "Failed"

    def test_determine_file_status_failed_with_multiple_errors(self) -> None:
        """Test determine_file_status with multiple errors returns "Failed"."""
        err1 = ProcessingError(
            code=ErrorCode.ERR_020,
            message="Header row not found",
            context={"filename": "test.xlsx"},
        )
        err2 = ProcessingError(
            code=ErrorCode.ERR_030,
            message="Missing required field",
            context={"filename": "test.xlsx", "field": "part_no"},
        )
        errors = [err1, err2]
        warnings: list[ProcessingError] = []

        status = determine_file_status(errors, warnings)

        assert status == "Failed"

    def test_determine_file_status_attention_att_only(self) -> None:
        """Test determine_file_status when no ERR, one ATT_003 warning; returns "Attention"."""
        errors: list[ProcessingError] = []
        warn = ProcessingError(
            code=WarningCode.ATT_003,
            message="Ambiguous currency",
            context={"filename": "test.xlsx"},
        )
        warnings = [warn]

        status = determine_file_status(errors, warnings)

        assert status == "Attention"

    def test_determine_file_status_attention_with_multiple_warnings(self) -> None:
        """Test determine_file_status with multiple warnings (no errors) returns "Attention"."""
        errors: list[ProcessingError] = []
        warn1 = ProcessingError(
            code=WarningCode.ATT_003,
            message="Ambiguous currency",
            context={"filename": "test.xlsx"},
        )
        warn2 = ProcessingError(
            code=WarningCode.ATT_002,
            message="Inferred sheet type",
            context={"filename": "test.xlsx"},
        )
        warnings = [warn1, warn2]

        status = determine_file_status(errors, warnings)

        assert status == "Attention"

    def test_determine_file_status_failed_takes_precedence_over_att(self) -> None:
        """Test determine_file_status when one ERR_030 and one ATT_003; returns "Failed" (ERR wins)."""
        err = ProcessingError(
            code=ErrorCode.ERR_030,
            message="Missing required field",
            context={"filename": "test.xlsx", "field": "qty"},
        )
        errors = [err]
        warn = ProcessingError(
            code=WarningCode.ATT_003,
            message="Ambiguous currency",
            context={"filename": "test.xlsx"},
        )
        warnings = [warn]

        status = determine_file_status(errors, warnings)

        assert status == "Failed"

    def test_determine_file_status_distinguishes_errorcode_vs_warningcode(self) -> None:
        """Test that determine_file_status uses isinstance(error.code, ErrorCode) to distinguish ERR from ATT."""
        # Create a ProcessingError with ErrorCode and one with WarningCode
        err = ProcessingError(
            code=ErrorCode.ERR_031,
            message="Invalid decimal value",
            context={"filename": "test.xlsx", "row": 10, "column": "C"},
        )
        warn = ProcessingError(
            code=WarningCode.ATT_004,
            message="Unusual format detected",
            context={"filename": "test.xlsx", "row": 15},
        )

        # Verify isinstance checks work correctly
        assert isinstance(err.code, ErrorCode)
        assert not isinstance(err.code, WarningCode)
        assert isinstance(warn.code, WarningCode)
        assert not isinstance(warn.code, ErrorCode)

        # Test with error only
        status = determine_file_status([err], [])
        assert status == "Failed"

        # Test with warning only
        status = determine_file_status([], [warn])
        assert status == "Attention"

    def test_determine_file_status_err_020_specific(self) -> None:
        """Test with ERR_020 specifically (from spec test case 2)."""
        err = ProcessingError(
            code=ErrorCode.ERR_020,
            message="Header row not found",
            context={"filename": "test.xlsx"},
        )
        errors = [err]
        warnings: list[ProcessingError] = []

        status = determine_file_status(errors, warnings)

        assert status == "Failed"

    def test_determine_file_status_att_003_specific(self) -> None:
        """Test with ATT_003 specifically (from spec test case 3)."""
        warn = ProcessingError(
            code=WarningCode.ATT_003,
            message="Ambiguous currency detected",
            context={"filename": "test.xlsx"},
        )
        errors: list[ProcessingError] = []
        warnings = [warn]

        status = determine_file_status(errors, warnings)

        assert status == "Attention"

    def test_determine_file_status_err_030_and_att_003(self) -> None:
        """Test with ERR_030 and ATT_003 together (from spec test case 4)."""
        err = ProcessingError(
            code=ErrorCode.ERR_030,
            message="Missing required field",
            context={"filename": "test.xlsx", "field": "part_no"},
        )
        warn = ProcessingError(
            code=WarningCode.ATT_003,
            message="Ambiguous currency",
            context={"filename": "test.xlsx"},
        )
        errors = [err]
        warnings = [warn]

        status = determine_file_status(errors, warnings)

        assert status == "Failed"

    def test_determine_file_status_att_002_specific(self) -> None:
        """Test with ATT_002 warning code."""
        warn = ProcessingError(
            code=WarningCode.ATT_002,
            message="Inferred sheet type",
            context={"filename": "test.xlsx", "inferred_type": "packing"},
        )
        errors: list[ProcessingError] = []
        warnings = [warn]

        status = determine_file_status(errors, warnings)

        assert status == "Attention"

    def test_determine_file_status_att_004_specific(self) -> None:
        """Test with ATT_004 warning code."""
        warn = ProcessingError(
            code=WarningCode.ATT_004,
            message="Unusual value format detected",
            context={"filename": "test.xlsx", "row": 5, "column": "E"},
        )
        errors: list[ProcessingError] = []
        warnings = [warn]

        status = determine_file_status(errors, warnings)

        assert status == "Attention"

    def test_determine_file_status_with_all_error_codes(self) -> None:
        """Test that all ErrorCode values correctly return "Failed"."""
        error_codes = [
            ErrorCode.ERR_001,
            ErrorCode.ERR_002,
            ErrorCode.ERR_003,
            ErrorCode.ERR_004,
            ErrorCode.ERR_005,
            ErrorCode.ERR_010,
            ErrorCode.ERR_011,
            ErrorCode.ERR_012,
            ErrorCode.ERR_013,
            ErrorCode.ERR_014,
            ErrorCode.ERR_020,
            ErrorCode.ERR_021,
            ErrorCode.ERR_030,
            ErrorCode.ERR_031,
            ErrorCode.ERR_032,
            ErrorCode.ERR_033,
            ErrorCode.ERR_034,
            ErrorCode.ERR_040,
            ErrorCode.ERR_041,
            ErrorCode.ERR_042,
            ErrorCode.ERR_043,
            ErrorCode.ERR_044,
            ErrorCode.ERR_045,
            ErrorCode.ERR_046,
            ErrorCode.ERR_047,
            ErrorCode.ERR_048,
            ErrorCode.ERR_051,
            ErrorCode.ERR_052,
        ]

        for code in error_codes:
            err = ProcessingError(
                code=code,
                message=f"Error {code.value}",
                context={"filename": "test.xlsx"},
            )
            status = determine_file_status([err], [])
            assert status == "Failed", f"ErrorCode {code.value} should return Failed"

    def test_determine_file_status_with_all_warning_codes(self) -> None:
        """Test that all WarningCode values correctly return "Attention"."""
        warning_codes = [
            WarningCode.ATT_002,
            WarningCode.ATT_003,
            WarningCode.ATT_004,
        ]

        for code in warning_codes:
            warn = ProcessingError(
                code=code,
                message=f"Warning {code.value}",
                context={"filename": "test.xlsx"},
            )
            status = determine_file_status([], [warn])
            assert status == "Attention", f"WarningCode {code.value} should return Attention"

    def test_determine_file_status_error_with_rich_context(self) -> None:
        """Test that error with rich context data still returns "Failed"."""
        err = ProcessingError(
            code=ErrorCode.ERR_033,
            message="Decimal conversion failed for price field",
            context={
                "filename": "invoice_2026.xlsx",
                "sheet": "Invoice",
                "row": 42,
                "column": "F",
                "field_name": "price",
                "raw_value": "2.28x",
            },
        )
        status = determine_file_status([err], [])
        assert status == "Failed"

    def test_determine_file_status_warning_with_rich_context(self) -> None:
        """Test that warning with rich context data still returns "Attention"."""
        warn = ProcessingError(
            code=WarningCode.ATT_003,
            message="Ambiguous currency: multiple columns detected",
            context={
                "filename": "packing_2026.xlsx",
                "sheet": "Packing",
                "currency_columns": [5, 7, 9],
                "selected": 5,
            },
        )
        status = determine_file_status([], [warn])
        assert status == "Attention"
