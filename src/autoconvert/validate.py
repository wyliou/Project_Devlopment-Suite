"""validate — FR-027: File status determination (Success/Attention/Failed)."""

from .errors import ErrorCode, ProcessingError


def determine_file_status(errors: list[ProcessingError], warnings: list[ProcessingError]) -> str:
    """Determine file status based on accumulated errors and warnings.

    Implements FR-027: Returns "Failed" if any ERR_xxx error exists,
    "Attention" if any ATT_xxx warning exists (and no errors),
    otherwise "Success".

    Status determination is purely based on code type (ErrorCode vs WarningCode),
    not the string prefix. Uses isinstance() checks on error.code.

    Args:
        errors: List of ProcessingError instances with ErrorCode.
        warnings: List of ProcessingError instances with WarningCode.

    Returns:
        "Failed" if any error, "Attention" if any warning (no errors),
        "Success" otherwise.
    """
    # Check for any errors (ErrorCode instances)
    for error in errors:
        if isinstance(error.code, ErrorCode):
            return "Failed"

    # Check for any warnings (WarningCode instances)
    for warning in warnings:
        if not isinstance(warning.code, ErrorCode):
            return "Attention"

    # No errors and no warnings
    return "Success"
