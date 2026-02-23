Module: src/autoconvert/cli.py | Tests: tests/test_diagnostic.py | FRs: FR-034

Exports:
  main() -> None
    Entry point: parse args, load config, setup logging, call run_batch or diagnostic; sys.exit with code 0/1/2.
  parse_args() -> argparse.Namespace
    Parse CLI args: optional --diagnostic <filename>.

Imports:
  .batch: run_batch, process_file
  .config: load_config
  .logger: setup_logging, setup_diagnostic_logging
  argparse, sys, pathlib.Path

Tests:
  1. test_parse_args_no_args — sys.argv has no --diagnostic; parse_args() returns namespace with diagnostic=None
  2. test_parse_args_diagnostic_flag — sys.argv has ["--diagnostic", "file.xlsx"]; parse_args().diagnostic == "file.xlsx"
  3. test_main_exit_code_0_on_all_success — run_batch returns BatchResult with failed_count=0; sys.exit called with 0
  4. test_main_exit_code_1_on_any_failed — run_batch returns BatchResult with failed_count=1; sys.exit called with 1
  5. test_main_exit_code_2_on_config_error — load_config raises ConfigError; sys.exit called with 2

Gotchas:
  - DO NOT validate/log ERR_001 (CONFIG_NOT_FOUND) — owned by config.py. cli.py catches ConfigError and calls sys.exit(2).
  - Exit code 0: all files Success or Attention. Exit code 1: any Failed file. Exit code 2: fatal startup error (ConfigError, bad args, permission error on dirs).
  - Diagnostic mode: call setup_diagnostic_logging() (DEBUG level to console) instead of setup_logging(). Then call process_file() on the single specified file, not run_batch().
  - cli.py must NOT import from batch.py at module level in a way that prevents testing parse_args() in isolation.
  - sys.exit() must be the last statement of main() to allow testing with pytest-raises or monkeypatch.
