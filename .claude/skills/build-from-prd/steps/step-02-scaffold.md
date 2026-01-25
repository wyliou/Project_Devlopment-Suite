---
name: 'step-02-scaffold'
description: 'Create project structure, install dependencies, setup database, configure environment'
nextStepFile: '{skill_base}/steps/step-03-implement.md'
stateFile: '{project_root}/build-state.json'
---

# Step 2: Scaffold

**Progress:** Step 2 of 4 - Next: Implement

**Goal:** Create project foundation - directories, dependencies, database, environment.

---

## Execution Rules

- **Autonomous step** - no user prompts
- Auto-retry failed operations up to 3 times
- Log errors but continue on non-critical failures
- Auto-proceed to next step on completion

---

## Sequence (Follow Exactly)

### 1. Load Context

Read `{stateFile}` for paths and mode.

Load architecture document sections needed:
- Section 1: Technology Stack
- Section 2: Project Structure
- Section 6: Database Schema
- Section 7: Environment Variables

---

### 2. Create Directory Structure

From Architecture Section 2, create all directories.

**Example structure parsing:**
```
src/
  modules/
    auth/
    users/
  shared/
tests/
docs/
```

Create each directory. Output: "Created [N] directories"

**On failure:** Log error, continue (non-critical).

---

### 3. Initialize Project

Based on Technology Stack (Section 1):

**Python:**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install [packages from stack]
```

**Node.js:**
```bash
npm init -y
npm install [packages from stack]
```

**On failure:**
- Retry up to 3 times with error context
- Log final error if still failing
- Continue (mark in state as `deps_install_failed: true`)

Output: "Dependencies installed: [package list]"

---

### 4. Setup Database

From Architecture Section 6 (Database Schema):

**If using SQLite:**
- Create database file at specified path
- Run initial schema creation

**If using PostgreSQL/MySQL:**
- Verify connection (from env config)
- Run migrations if migration tool specified

**If using ORM (SQLAlchemy, Prisma, etc.):**
- Generate models from schema
- Run migration command

**On failure:**
- Retry up to 3 times
- Log error if still failing
- Continue (mark in state as `db_setup_failed: true`)

Output: "Database setup: [status]"

---

### 5. Create Environment Configuration

From Architecture Section 7 (Environment Variables):

Create `.env` file with:
- All variables from architecture
- Placeholder values marked with `# TODO: Set actual value`
- Database connection string
- Any API keys as placeholders

Also create `.env.example` (same content, no sensitive values).

Output: "Environment configured: .env created"

---

### 6. Setup Testing Framework

Based on Technology Stack:

**Python (pytest):**
```bash
pip install pytest pytest-cov
```
Create `pytest.ini` or `pyproject.toml` test config.

**Node.js (jest/vitest):**
```bash
npm install --save-dev jest  # or vitest
```
Create `jest.config.js` or `vitest.config.js`.

Create initial test directory structure matching modules.

Output: "Testing framework configured: [framework]"

---

### 7. Create Base Files

Create foundational files based on architecture patterns:

| File | Purpose |
|------|---------|
| `src/__init__.py` (Python) | Package init |
| `src/index.ts` (TS) | Entry point |
| `src/config.py` or `config.ts` | Configuration loader |
| `src/shared/errors.py` or `errors.ts` | Error handling patterns |

Use patterns from Architecture Section 3 (Coding Patterns) if specified.

---

### 8. Validation Checks

Verify scaffold completion:

| Check | Validation |
|-------|------------|
| Directories | All from Section 2 exist |
| Dependencies | Package manager lock file exists |
| Database | Connection successful or file exists |
| Environment | `.env` file exists |
| Tests | Test config file exists |

**On validation failure:**
- Log specific failures
- Continue to next step (non-blocking)
- Failures will be noted in final report

---

### 9. Update State

Update `{stateFile}`:

```json
{
  "current_step": 2,
  "scaffold_complete": true,
  "scaffold_status": {
    "directories": true,
    "dependencies": true,
    "database": true,
    "environment": true,
    "testing": true
  }
}
```

Mark any failed items as `false`.

---

### 10. Output Summary

```
Scaffold Complete
=================
Directories: [N] created
Dependencies: [installed/failed]
Database: [configured/failed]
Environment: .env created
Testing: [framework] configured

Proceeding to implementation...
```

---

### 11. Auto-Proceed

Update state: `current_step: 3`

Load and execute `{nextStepFile}`.

---

## Success Criteria

- Directory structure created
- Dependencies installed (or failure logged)
- Database initialized (or failure logged)
- Environment files created
- Testing framework configured
- Scaffold status recorded in state
- Auto-proceeded to step-03-implement.md
