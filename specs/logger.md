Module: `src/autoconvert/logger.py` | Tests: none (logging configuration; tested via integration) | FRs: FR-031, FR-032

Exports:
- `setup_logging(log_path: Path) -> None` — Configures root logger with two handlers: (1) StreamHandler to stdout at INFO level, format `[{LEVEL}] {message}`; (2) FileHandler to `log_path / "process_log.txt"` at DEBUG level, format `[{HH:MM}] [{LEVEL}] {message}`. Normal batch mode.
- `setup_diagnostic_logging(log_path: Path) -> None` — Same as `setup_logging` but StreamHandler is set to DEBUG level for maximum verbosity to console. Used by `--diagnostic` flag (FR-034).

Imports:
- `logging` (stdlib)
- `pathlib`: `Path`

Tests:
1. `test_setup_logging_creates_process_log` — call `setup_logging(tmp_path)`, log a DEBUG message, verify `process_log.txt` exists in `tmp_path` and contains the message; verify console handler does NOT emit DEBUG messages (level is INFO).
2. `test_setup_logging_console_format` — after `setup_logging`, emit `logger.info("test message")`, capture with `caplog`; verify record appears at INFO level.
3. `test_setup_diagnostic_logging_console_debug` — call `setup_diagnostic_logging(tmp_path)`, emit `logger.debug("detail")`, verify the message appears in console handler output (DEBUG level active).
4. `test_file_handler_timestamp_format` — after `setup_logging`, emit a message, read `process_log.txt`; verify the line matches `[HH:MM] [LEVEL] ...` format (regex: `^\[\d{2}:\d{2}\] \[`).
5. `test_repeated_setup_clears_handlers` — call `setup_logging` twice; verify the root logger does not accumulate duplicate handlers (handler count stays at 2).

Gotchas:
- Only this module configures logging handlers. All other modules use `logging.getLogger(__name__)` only — they never call `basicConfig`, add handlers, or set levels.
- Log file format uses `[HH:MM]` (hours and minutes only, no seconds) per FR-032: `[HH:MM] [LEVEL]`.
- Console format uses `[{LEVEL}]` not `[%(levelname)s]` brackets — must match PRD Section 7 Console Output Format verbatim: `[INFO]`, `[ERROR]`, `[WARNING]`.
- `setup_logging`/`setup_diagnostic_logging` must remove any existing handlers from the root logger before adding new ones (prevents handler accumulation on repeated calls in tests).
- The log file path is `log_path / "process_log.txt"` where `log_path` is the project root directory (passed in by cli.py/batch.py). The filename is always `process_log.txt`.
