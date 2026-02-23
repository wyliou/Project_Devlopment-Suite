"""errors — ErrorCode/WarningCode enums, ProcessingError, and ConfigError exceptions."""

from enum import Enum
from typing import Any


class ErrorCode(Enum):
    """Error codes matching PRD Section 7 catalog exactly.

    Values are string representations of the code name.
    Members are non-contiguous per the PRD catalog.
    """

    ERR_001 = "ERR_001"
    ERR_002 = "ERR_002"
    ERR_003 = "ERR_003"
    ERR_004 = "ERR_004"
    ERR_005 = "ERR_005"
    ERR_010 = "ERR_010"
    ERR_011 = "ERR_011"
    ERR_012 = "ERR_012"
    ERR_013 = "ERR_013"
    ERR_014 = "ERR_014"
    ERR_020 = "ERR_020"
    ERR_021 = "ERR_021"
    ERR_030 = "ERR_030"
    ERR_031 = "ERR_031"
    ERR_032 = "ERR_032"
    ERR_033 = "ERR_033"
    ERR_034 = "ERR_034"
    ERR_040 = "ERR_040"
    ERR_041 = "ERR_041"
    ERR_042 = "ERR_042"
    ERR_043 = "ERR_043"
    ERR_044 = "ERR_044"
    ERR_045 = "ERR_045"
    ERR_046 = "ERR_046"
    ERR_047 = "ERR_047"
    ERR_048 = "ERR_048"
    ERR_051 = "ERR_051"
    ERR_052 = "ERR_052"


class WarningCode(Enum):
    """Warning codes matching PRD Section 7 catalog exactly.

    Values are string representations of the code name.
    Warnings cause "Attention" status but do not abort processing.
    """

    ATT_002 = "ATT_002"
    ATT_003 = "ATT_003"
    ATT_004 = "ATT_004"


class ProcessingError(Exception):
    """Per-file processing error or warning.

    Used for errors and warnings that occur during per-file processing.
    Caught by batch.py; does NOT abort the batch.
    Accepts both ErrorCode (hard errors) and WarningCode (warnings) for the code field.

    Args:
        code: The error or warning code (ErrorCode or WarningCode).
        message: Human-readable description with context.
        context: Additional context dict (filename, row, column, field_name, etc.).
    """

    def __init__(self, code: ErrorCode | WarningCode, message: str, context: dict[str, Any]) -> None:
        """Initialize ProcessingError.

        Args:
            code (ErrorCode | WarningCode): The error or warning code.
            message (str): Human-readable description with context.
            context (dict[str, Any]): Additional context (filename, row, column, etc.).
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.context = context


class ConfigError(Exception):
    """Fatal configuration error raised during startup config loading (FR-002).

    Fatal — causes exit code 2. Never caught by per-file processing.
    Only accepts ErrorCode (config errors are always hard failures, never warnings).

    Args:
        code: The error code (ErrorCode only).
        message: Human-readable description of the config problem.
        path: File system path where the error occurred.
    """

    def __init__(self, code: ErrorCode, message: str, path: str) -> None:
        """Initialize ConfigError.

        Args:
            code (ErrorCode): The error code.
            message (str): Human-readable description of the config problem.
            path (str): File system path where the error occurred.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path
