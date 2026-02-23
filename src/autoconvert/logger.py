"""logger — FR-031, FR-032: Dual-output logging configuration (console + file)."""

import io
import logging
import sys
from pathlib import Path


def _make_console_handler(level: int) -> logging.StreamHandler:
    """Create a console handler with UTF-8 encoding to handle CJK characters on Windows.

    Args:
        level: Logging level for the handler.

    Returns:
        Configured StreamHandler with UTF-8 output.
    """
    # Reason: Windows console defaults to cp950/cp936 which can't encode all CJK chars.
    # Wrap stdout in a UTF-8 stream with error replacement to prevent UnicodeEncodeError.
    utf8_stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    handler = logging.StreamHandler(utf8_stream)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    return handler


def setup_logging(log_path: Path) -> None:
    """Configure root logger with console (INFO) and file (DEBUG) handlers.

    Args:
        log_path: Directory where process_log.txt will be created.
    """
    root_logger = logging.getLogger()

    # Clear existing handlers to prevent accumulation
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = _make_console_handler(logging.INFO)

    # File handler: DEBUG level, format [HH:MM] [LEVEL] message
    log_file = log_path / "process_log.txt"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M")
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)


def setup_diagnostic_logging(log_path: Path) -> None:
    """Configure root logger with console (DEBUG) and file (DEBUG) handlers.

    Used by --diagnostic flag for maximum verbosity.

    Args:
        log_path: Directory where process_log.txt will be created.
    """
    root_logger = logging.getLogger()

    # Clear existing handlers to prevent accumulation
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = _make_console_handler(logging.DEBUG)

    # File handler: DEBUG level, format [HH:MM] [LEVEL] message
    log_file = log_path / "process_log.txt"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M")
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)
