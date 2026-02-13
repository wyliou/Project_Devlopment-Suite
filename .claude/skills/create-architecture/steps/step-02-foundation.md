---
name: 'step-02-foundation'
description: 'Select technology stack, define build commands, project structure, and coding patterns'
nextStepFile: '{skill_base}/steps/step-03-modules.md'
outputFile: '{planning_artifacts}/architecture.md'
---

# Step 2: Technology & Foundation

**Progress:** Step 2 of 4 → Next: Modules & Contracts

**Goal:** Select the complete technology stack, define build commands, project structure, and coding patterns.

---

## Instructions

### 1. Select Technology Stack

**For each "Open" decision in PRD Section 6:**

1. Match product category to recommendations:
   - Load `{data_files_path}/project-types.csv` for options by category
   - Use web search: "[technology] latest stable version 2026"

2. Select technology that aligns with:
   - PRD constraints (Section 6 Decided items are locked)
   - NFR requirements (Section 4)
   - Ecosystem compatibility

3. Document rationale briefly

**Categories (fill all that apply):**

| Category | Selection Inputs |
|----------|------------------|
| Framework | Product category + PRD hints |
| Database | Data complexity (Section 5) + scale (Section 4) |
| ORM | Framework ecosystem |
| Auth | Security requirements (Section 4) |
| Styling | Frontend needs (if applicable) |
| Testing | Framework ecosystem |

**Decision Rule:** If PRD clearly implies one choice, select it. Only ask user if multiple equally valid options exist—then present top 2 with your recommendation.

Fill Section 1 Technology Stack table in `{outputFile}`.

---

### 2. Define Build Commands

Derive Install/Test/Lint/Type Check/Format/Build commands from the selected stack. These directly feed build-from-prd's Build Config table.

| Command | Value |
|---------|-------|
| Install | e.g., `npm install`, `uv sync`, `go mod download` |
| Test | e.g., `npm test`, `uv run pytest tests/ --tb=short`, `go test ./...` |
| Lint | e.g., `npm run lint`, `uv run ruff check src/ --fix`, `golangci-lint run` |
| Type Check | e.g., `npx tsc --noEmit`, `uv run pyright src/`, leave empty for dynamic langs |
| Format | e.g., `npx prettier --write src/`, `uv run ruff format src/`, leave empty if lint handles it |
| Build | e.g., `npm run build`, `uv run python -m build`, `go build ./cmd/app` |

Fill Section 1 Build Commands table in `{outputFile}`.

---

### 3. Define Project Structure

Generate directory tree following framework conventions.

**Structure must include:**
- Source code organization (framework-specific)
- Test file locations (mirroring source structure)
- Configuration files
- Database/schema files
- Static assets (if applicable)

**Derive from:**
- Framework conventions (e.g., Next.js app router, NestJS modules)
- PRD functional areas (Section 3 capability area headers → corresponding directories)
- Module count from FRs

**Add `src_dir` and `test_dir` markers as HTML comments:**
```markdown
<!-- src_dir: src/ -->
<!-- test_dir: tests/ -->
```

These markers are extracted by build-from-prd for automated tooling.

Fill Section 2 in `{outputFile}`.

---

### 4. Define Coding Patterns

#### A. Naming Conventions (7 rows)

| Element | Convention | Example |
|---------|------------|---------|
| Component files | Framework standard | (derive from framework) |
| Utility files | kebab-case | `user-service.ts` |
| Functions | camelCase | `getUserById` |
| DB Tables | snake_case | `user_accounts` |
| API Routes | kebab-case | `/api/user-profile` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Types/Interfaces | PascalCase | `UserProfile` |

#### B. API Response Format (Adapted per project type)

**Web App / API Service:**
```typescript
// Success: { data: T, error: null }
// Error: { data: null, error: { code: string, message: string } }
```

**CLI Tool:**
```
Exit codes: 0 (success), 1 (runtime error), 2 (usage error)
Stdout: structured output (JSON/table/plain per command)
Stderr: error messages and diagnostics
```

**Library/SDK:**
```
Returns: typed values
Errors: typed exceptions/errors with code property
```

#### C. Error Code Taxonomy

Standard prefixes:
| Prefix | Category | HTTP Status |
|--------|----------|-------------|
| AUTH_ | Authentication | 401/403 |
| VAL_ | Validation | 400 |
| RES_ | Resource | 404/409 |
| SYS_ | System | 500 |

Add domain-specific prefixes from PRD Section 3 capability areas (e.g., "Order Management" section → ORDER_).

#### D. Logging Pattern

Define:
- **Format:** e.g., `[{timestamp}] {level} [{module}] {message}`
- **Levels:** ERROR (failures), WARN (degraded), INFO (state changes), DEBUG (dev only)
- **What gets logged:** State transitions, external calls, errors. NOT: routine reads, internal calculations.
- **Structured fields:** If applicable, define required fields per log entry.

Derive from PRD Section 8 (if present) and FR Log fields.

#### E. Side-Effect Ownership

Define which modules own which side effects:

| Side Effect | Owner Module | Non-owners Must |
|-------------|-------------|-----------------|
| File writes | {module} | Call {module}.write() |
| HTTP calls | {module} | Call {module}.request() |
| DB writes | {module} | Go through {module} service |
| Logging | Each module | Use shared logger config |

Derive from FR capability areas — modules that handle FILE, API, DATA areas typically own corresponding side effects.

Fill Section 3 in `{outputFile}`.

---

### 5. Checkpoint

Present to user:
- Technology stack table (versions + rationale)
- Build commands
- Project structure (collapsed view)
- Coding patterns summary

**Menu:**
- **[C] Continue** - Proceed to Step 3: Modules & Contracts
- **[R] Revise** - Adjust technology selections, structure, or patterns
- **[P] Party Mode** - Discuss stack decisions with architect/dev agents
- **[D] Deep Dive** - Analyze decisions with advanced elicitation methods
- **[X] Exit** - Save progress and stop

**On [P] Party Mode:**
Invoke `_party-mode` skill with:
- `topic`: "Technology stack decisions for [project name]"
- `content`: Technology stack table + PRD constraints summary
- `focus_agents`: `architect`, `dev`

After party mode completes, return to this checkpoint with insights applied.

**On [D] Deep Dive:**
Invoke `_deep-dive` skill with:
- `content`: Technology stack table + rationale
- `focus_area`: "Technology stack validation"
- `content_type`: "architecture"

Recommended method categories: `technical`, `risk`, `competitive`

After deep dive completes, return to this checkpoint with enhancements applied.

**On Continue:** Update frontmatter `current_step: 3`, load `{nextStepFile}`
