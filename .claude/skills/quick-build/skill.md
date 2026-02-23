---
name: quick-build
description: Implement from PRD + architecture quickly
---

# Quick Build

Implement a project from spec docs. Fully autonomous — discover specs, plan, build, verify, audit.

---

## 1. Discover Project State

**Auto-detect — do NOT ask the user.**

- **Find specs:** Scan `docs/` for PRD/requirements and architecture/design docs (any naming: `prd.md`, `PRD.md`, `requirements.md`, `architecture.md`, `design.md`, etc.). Also check project root. If no spec docs exist, stop and tell the user — building without specs produces guesswork.
- **Find existing code:** Scan the source tree (`src/`, `lib/`, `app/`, or project root). If code already exists, read it to understand what's built vs what's missing. Only build what's incomplete.
- **Find config:** Read `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, or equivalent for project name, dependencies, and build/test commands.
- **Find conventions:** Read `CLAUDE.md` at project root or in `.claude/` for coding conventions. Read linter/formatter config if present.
- **Find test data:** Note any `data/`, `samples/`, `fixtures/`, or `tests/fixtures/` directories for later verification.

**Output of this step:** Mental model of what exists, what's missing, and what conventions to follow.

---

## 2. Read Specs Thoroughly

Read the full PRD and architecture docs. Pay special attention to:
- **Error/warning codes** — every one must be implemented
- **Edge cases and algorithm details** — these are where bugs hide
- **Module boundaries and dependencies** — build order follows this
- **Config-driven behavior** — flags like `required: true` must be enforced in code, not just loaded
- **Data flow contracts** — inputs/outputs between modules

---

## 3. Plan the Build

Create a task list ordered by dependency (foundations first):
- Group into batches per the architecture's dependency graph (if specified)
- Leaf modules (models, errors, utils) first → core logic → orchestrator → entry point last
- Each task = one module or one cohesive unit of work
- Mark dependencies between tasks where relevant

---

## 4. Build

Build every module directly — do NOT delegate to subagents. Summarizing specs for subagents loses edge-case nuance and produces plausible-but-wrong code that costs more time to debug than it saves.

**Per module:**
- Follow conventions from `CLAUDE.md` and project config
- No file over 500 lines — split into sub-modules if approaching the limit
- Implement ALL error paths defined in the spec, not just the happy path
- Use the exact error/warning codes from the spec

---

## 5. Verify Incrementally

After each batch of related modules:
- Run imports or a minimal smoke test to catch syntax errors and broken references
- Fix before moving on — don't accumulate tech debt across batches

After the full pipeline is built:
- Run end-to-end against real data if available in `data/` or `tests/fixtures/`
- Run the test suite if one exists (auto-detect runner from project config)

---

## 6. Audit Against Spec

This is the most important step. A "working" build that misses spec requirements is not done.

| Check | How |
|-------|-----|
| **Error codes** | Grep codebase for every error/warning code defined in the spec. If a code is defined but never raised → missing validation — implement it. |
| **Placeholder code** | Search for `pass`, `TODO`, `FIXME`, `...` (Ellipsis) in built source. Each one is unfinished — complete or remove it. |
| **Config-driven flags** | If the spec defines config flags that control behavior (e.g., `required: true`), verify the code actually reads and enforces them. |
| **FR error outputs** | For every functional requirement that lists an error/warning as output, trace the code path and confirm it can actually be triggered. |
| **Algorithm fidelity** | For each algorithm described in the spec (especially multi-step ones), walk the code and verify every step/condition/priority is implemented. |

---

## 7. Wrap Up

- Create or update `README.md` with setup steps, usage, and project structure
- Report build summary: modules built, total lines, any known gaps
- Recommend `/real-data-validation` as the next step if test data exists
