"""Tests for errors module — ErrorCode, WarningCode, ProcessingError, ConfigError."""

from autoconvert.errors import ConfigError, ErrorCode, ProcessingError, WarningCode


class TestErrorCodeValues:
    """Test ErrorCode enum values match PRD catalog."""

    def test_error_code_values_match_prd(self) -> None:
        """Test all ErrorCode members have string values exactly matching their name."""
        # Test a sample of error codes
        assert ErrorCode.ERR_001.value == "ERR_001"
        assert ErrorCode.ERR_002.value == "ERR_002"
        assert ErrorCode.ERR_003.value == "ERR_003"
        assert ErrorCode.ERR_005.value == "ERR_005"
        assert ErrorCode.ERR_010.value == "ERR_010"
        assert ErrorCode.ERR_014.value == "ERR_014"
        assert ErrorCode.ERR_020.value == "ERR_020"
        assert ErrorCode.ERR_021.value == "ERR_021"
        assert ErrorCode.ERR_030.value == "ERR_030"
        assert ErrorCode.ERR_031.value == "ERR_031"
        assert ErrorCode.ERR_040.value == "ERR_040"
        assert ErrorCode.ERR_046.value == "ERR_046"
        assert ErrorCode.ERR_047.value == "ERR_047"
        assert ErrorCode.ERR_051.value == "ERR_051"
        assert ErrorCode.ERR_052.value == "ERR_052"

        # Verify all members follow the pattern: name == value
        for member in ErrorCode:
            assert member.value == member.name

        # Verify we have exactly 28 error codes
        assert len(ErrorCode) == 28


class TestWarningCodeValues:
    """Test WarningCode enum values match PRD catalog."""

    def test_warning_code_values_match_prd(self) -> None:
        """Test all WarningCode members have string values matching their name."""
        assert WarningCode.ATT_002.value == "ATT_002"
        assert WarningCode.ATT_003.value == "ATT_003"
        assert WarningCode.ATT_004.value == "ATT_004"

        # Verify all members follow the pattern: name == value
        for member in WarningCode:
            assert member.value == member.name

        # Verify we have exactly 3 warning codes
        assert len(WarningCode) == 3


class TestProcessingError:
    """Test ProcessingError exception class."""

    def test_processing_error_is_exception(self) -> None:
        """Test ProcessingError is an instance of Exception."""
        error = ProcessingError(code=ErrorCode.ERR_020, message="missing", context={})
        assert isinstance(error, Exception)
        assert hasattr(error, "code")
        assert hasattr(error, "message")
        assert hasattr(error, "context")

    def test_processing_error_attributes(self) -> None:
        """Test ProcessingError attributes are accessible and correct."""
        context = {"filename": "test.xlsx", "row": 5}
        error = ProcessingError(code=ErrorCode.ERR_020, message="test message", context=context)

        assert error.code == ErrorCode.ERR_020
        assert error.message == "test message"
        assert error.context == context

    def test_processing_error_accepts_warning_code(self) -> None:
        """Test ProcessingError accepts WarningCode for the code parameter."""
        context = {"field": "currency"}
        error = ProcessingError(code=WarningCode.ATT_003, message="warn", context=context)

        assert isinstance(error, Exception)
        assert error.code == WarningCode.ATT_003
        assert error.message == "warn"
        assert error.context == context

    def test_processing_error_string_representation(self) -> None:
        """Test ProcessingError string representation includes message."""
        message = "Required column missing"
        error = ProcessingError(code=ErrorCode.ERR_020, message=message, context={})
        # The Exception's string representation should be the message
        assert str(error) == message


class TestConfigError:
    """Test ConfigError exception class."""

    def test_config_error_is_exception(self) -> None:
        """Test ConfigError is an instance of Exception."""
        error = ConfigError(
            code=ErrorCode.ERR_001,
            message="not found",
            path="/config/x.yaml",
        )
        assert isinstance(error, Exception)
        assert hasattr(error, "code")
        assert hasattr(error, "message")
        assert hasattr(error, "path")

    def test_config_error_attributes(self) -> None:
        """Test ConfigError attributes are accessible and correct."""
        path = "/config/field_patterns.yaml"
        error = ConfigError(
            code=ErrorCode.ERR_001,
            message="configuration file not found",
            path=path,
        )

        assert error.code == ErrorCode.ERR_001
        assert error.message == "configuration file not found"
        assert error.path == path

    def test_config_error_string_representation(self) -> None:
        """Test ConfigError string representation includes message."""
        message = "Config not found"
        error = ConfigError(code=ErrorCode.ERR_001, message=message, path="/config/test.yaml")
        # The Exception's string representation should be the message
        assert str(error) == message


class TestErrorCodeCatalog:
    """Test ErrorCode catalog completeness per PRD Section 7."""

    def test_error_code_catalog_001_to_005(self) -> None:
        """Test config/startup error codes exist (001-005)."""
        assert hasattr(ErrorCode, "ERR_001")
        assert hasattr(ErrorCode, "ERR_002")
        assert hasattr(ErrorCode, "ERR_003")
        assert hasattr(ErrorCode, "ERR_004")
        assert hasattr(ErrorCode, "ERR_005")

    def test_error_code_catalog_010_to_014(self) -> None:
        """Test file processing error codes exist (010-014)."""
        assert hasattr(ErrorCode, "ERR_010")
        assert hasattr(ErrorCode, "ERR_011")
        assert hasattr(ErrorCode, "ERR_012")
        assert hasattr(ErrorCode, "ERR_013")
        assert hasattr(ErrorCode, "ERR_014")

    def test_error_code_catalog_020_to_021(self) -> None:
        """Test column mapping error codes exist (020-021)."""
        assert hasattr(ErrorCode, "ERR_020")
        assert hasattr(ErrorCode, "ERR_021")

    def test_error_code_catalog_030_to_034(self) -> None:
        """Test data extraction error codes exist (030-034)."""
        assert hasattr(ErrorCode, "ERR_030")
        assert hasattr(ErrorCode, "ERR_031")
        assert hasattr(ErrorCode, "ERR_032")
        assert hasattr(ErrorCode, "ERR_033")
        assert hasattr(ErrorCode, "ERR_034")

    def test_error_code_catalog_040_to_048(self) -> None:
        """Test weight allocation error codes exist (040-048)."""
        assert hasattr(ErrorCode, "ERR_040")
        assert hasattr(ErrorCode, "ERR_041")
        assert hasattr(ErrorCode, "ERR_042")
        assert hasattr(ErrorCode, "ERR_043")
        assert hasattr(ErrorCode, "ERR_044")
        assert hasattr(ErrorCode, "ERR_045")
        assert hasattr(ErrorCode, "ERR_046")
        assert hasattr(ErrorCode, "ERR_047")
        assert hasattr(ErrorCode, "ERR_048")

    def test_error_code_catalog_051_to_052(self) -> None:
        """Test output error codes exist (051-052)."""
        assert hasattr(ErrorCode, "ERR_051")
        assert hasattr(ErrorCode, "ERR_052")

    def test_error_code_no_gaps_filled(self) -> None:
        """Test ErrorCode does not have members for gaps (006-009, 015-019, etc.)."""
        # Verify gap ranges don't have members
        gap_codes = [
            "ERR_006",
            "ERR_007",
            "ERR_008",
            "ERR_009",
            "ERR_015",
            "ERR_016",
            "ERR_017",
            "ERR_018",
            "ERR_019",
            "ERR_022",
            "ERR_023",
            "ERR_035",
            "ERR_049",
            "ERR_050",
            "ERR_053",
        ]
        for code_str in gap_codes:
            assert not hasattr(ErrorCode, code_str)
