---
name: write-tests
description: Write tests for existing implementation
---

# Write Tests

Discover the codebase, plan coverage by risk, build fixtures, write and run tests. Fully autonomous.

---

## 1. Discover

**Auto-detect everything — do NOT ask the user.**

- **Spec docs:** Read PRD, architecture, or requirements from `docs/` or project root. These define edge cases, error codes, algorithms, and behavioral contracts that must be tested.
- **Source tree:** Scan `src/`, `lib/`, `app/`, or project root for all source modules. Build a list of modules with their exported functions and classes.
- **Existing tests:** Check `tests/`, `test/`, `__tests__/`, or co-located `*_test.*` / `test_*.*` files. Note the framework, directory layout, naming conventions, and shared fixtures. Extend what exists rather than rewrite.
- **Test runner:** Determine the run command from `pyproject.toml` (`[tool.pytest]`), `package.json` (`scripts.test`), `Makefile`, `Cargo.toml`, or architecture docs. If nothing is configured, infer from the framework (e.g., `uv run pytest tests/` for Python with pytest).
- **Test data:** Note any fixture files in `tests/fixtures/`, `data/`, or `samples/` available for integration tests.
- **Virtual environment:** If Python, use the project's virtual environment for all commands.

---

## 2. Plan by Risk

Create a task list mapping source modules to test files, ordered by risk:

**High risk (test first):**
- Complex logic with many branches or state transitions
- Numerical precision (rounding, floating-point, decimal arithmetic)
- Parsing and extraction (regex, data formats, stop conditions)
- Orchestrators that coordinate multiple modules

**Low risk (test last):**
- Thin wrappers and pass-through functions
- Pure data models with no logic
- Simple formatting and string operations

For each module, inventory what needs coverage:
- Every public function and class method
- Every error/exception the module can raise
- Every branching condition, fallback path, and edge case
- Every algorithm step, stop condition, and priority rule from the spec

---

## 3. Build Shared Fixtures

Create or update `conftest.py` / test helpers before writing individual test files.

- **Prefer factories over static fixtures** — a function that builds minimal test inputs with overridable defaults is more flexible than a hardcoded fixture
- **Unit test fixtures:** Lightweight, in-memory, no I/O. Create minimal objects with just enough data for the test.
- **Integration test fixtures:** May use real data files from `tests/fixtures/` if available
- **Follow existing conventions** — if the project already has a `conftest.py` or fixture pattern, extend it

---

## 4. Write Tests (High-Risk First)

For each module, write tests in four categories:

| Category | What to Test |
|----------|-------------|
| **Happy path** | Normal inputs → correct outputs with concrete value assertions |
| **Edge cases** | Boundary values, empty inputs, single-element, max-size, off-by-one, precision limits, special characters |
| **Error paths** | Every distinct error the module can produce — verify both error type and message/code |
| **Behavioral contracts** | Spec says "X takes priority over Y" or "A happens before B" → prove it with a test |

**After each module's tests:**
- Run that module's tests immediately — don't batch
- Fix failures before moving on
- If a test reveals a genuine source bug, fix the source code, not the test

---

## 5. Keep Tests Fast and Isolated

- Unit tests complete in seconds — no network, no disk I/O, no sleep
- Each test is independent — no shared mutable state, no ordering dependencies
- Mock sparingly and only at module boundaries (external services, file I/O) — never mock the code under test
- If the project has test tiers (unit / component / integration), respect the structure and make tiers runnable independently

---

## 6. Final Validation

Run the full test suite end-to-end and confirm all tests pass.

Report:
```
Test suite: {runner command}
Total: N tests
Passed: N
Failed: N
Skipped: N (with reasons)

Coverage by module:
- module_a.py → test_module_a.py (N tests)
- module_b.py → test_module_b.py (N tests)
- module_c.py → (no tests)  ← flag uncovered modules

Issues:
- Flaky tests: (list any, or "none")
- Source bugs found and fixed: (list any, or "none")
```
