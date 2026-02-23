"""cli — FR-034: Command-line interface and diagnostic mode entry point."""

import argparse
import sys
from pathlib import Path

from . import batch as _batch
from .config import load_config
from .errors import ConfigError
from .logger import setup_diagnostic_logging, setup_logging
from .report import print_batch_summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for autoconvert.

    Supports an optional --diagnostic <filename> flag that processes a single
    file with DEBUG-level console output.

    Returns:
        argparse.Namespace: Parsed arguments with attribute ``diagnostic``
            set to the filename string if provided, or ``None`` otherwise.
    """
    parser = argparse.ArgumentParser(
        prog="autoconvert",
        description="AutoConvert: batch Excel invoice/packing converter.",
    )
    parser.add_argument(
        "--diagnostic",
        metavar="FILENAME",
        default=None,
        help="Process a single file with DEBUG-level console output (FR-034).",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: parse args, load config, setup logging, run batch or diagnostic.

    Exit codes:
        0 — All files processed as Success or Attention.
        1 — One or more files Failed (any ERR_xxx).
        2 — Fatal startup error (ConfigError, bad arguments, permission error).

    Returns:
        None. Calls sys.exit() with the appropriate exit code.
    """
    args = parse_args()

    # Resolve project root and config/data directories relative to this file.
    project_root = Path(__file__).parent.parent.parent
    config_dir = project_root / "config"
    data_dir = project_root / "data"

    # --- Load configuration (exit 2 on any ConfigError) ---
    try:
        config = load_config(config_dir)
    except ConfigError as exc:
        # Print to stderr before logging is configured so the message is visible.
        print(
            f"[ERROR] Configuration error ({exc.code.value}): {exc.message}",
            file=sys.stderr,
        )
        sys.exit(2)

    # --- Diagnostic mode (FR-034): single-file with DEBUG console output ---
    if args.diagnostic is not None:
        setup_diagnostic_logging(data_dir)
        file_path = Path(args.diagnostic)
        file_result = _batch.process_file(file_path, config)
        exit_code = 1 if file_result.status == "Failed" else 0
        sys.exit(exit_code)

    # --- Normal batch mode ---
    setup_logging(data_dir)
    batch_result = _batch.run_batch(config)
    print_batch_summary(batch_result)

    exit_code = 1 if batch_result.failed_count > 0 else 0
    sys.exit(exit_code)
