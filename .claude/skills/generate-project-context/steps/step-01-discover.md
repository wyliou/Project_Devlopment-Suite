---
name: 'step-01-discover'
description: 'Discover project context, technology stack, and initialize output document'
nextStepFile: './step-02-generate.md'
outputFile: '{project_root}/docs/project-context.md'
templateFile: '{installed_path}/project-context-template.md'
---

# Step 1: Discovery & Initialization

**Progress:** Step 1 of 3 → Next: Generate Rules

**Goal:** Analyze existing project files to discover technology stack, patterns, and critical rules. Initialize the project context document.

---

## Instructions

### 1. Check for Existing Context

Search for existing project context at `{outputFile}`.

**If found with `status: in-progress`:**
- Load `step-01b-continue.md` to resume

**If found with `status: complete`:**
- Ask user: "Found existing project context. Update existing or create fresh?"
- If update: Load existing, prepare for additions
- If fresh: Backup and start new

**If not found:** Proceed with fresh discovery.

---

### 2. Discover Technology Stack

Analyze project files to identify technologies:

**Architecture Document:**
- Look for `{project_root}/docs/architecture.md` or `{project_root}/planning/architecture.md`
- Extract technology choices with versions

**Package Files:**
- `package.json` → Node.js dependencies
- `requirements.txt` / `pyproject.toml` → Python dependencies
- `Cargo.toml` → Rust dependencies
- `go.mod` → Go dependencies

**Configuration Files:**
- Language configs: `tsconfig.json`, `.python-version`
- Build tools: `vite.config.*`, `next.config.*`, `webpack.config.*`
- Linting: `.eslintrc.*`, `.prettierrc.*`, `ruff.toml`
- Testing: `jest.config.*`, `vitest.config.*`, `pytest.ini`

---

### 3. Identify Existing Patterns

Search codebase for established patterns:

**Naming Conventions:**
- File naming (PascalCase, kebab-case, snake_case)
- Function/method naming
- Variable naming
- Test file naming

**Code Organization:**
- Directory structure
- Component/module organization
- Service layer patterns
- Utility placement

**Documentation:**
- Comment styles
- Docstring patterns
- README conventions

---

### 4. Extract Critical Rules

Identify rules AI agents might miss:

| Category | Look For |
|----------|----------|
| Language | Strict mode, import conventions, error handling |
| Framework | Hook patterns, routing, state management |
| Testing | Test structure, mocks, coverage requirements |
| Workflow | Branch naming, commit format, PR process |

---

### 5. Initialize Document

1. Copy `{templateFile}` to `{outputFile}`
2. Fill frontmatter:
   ```yaml
   ---
   status: in-progress
   current_step: 1
   project_name: [from package.json or directory]
   created_at: [today]
   categories_completed: []
   ---
   ```
3. Fill Technology Stack section with discovered versions

---

### 6. Present Discovery Summary

Show user:
- Technology stack with versions
- Patterns discovered (count by category)
- Key areas needing rules

**Example:**
```
Discovered project context for [project_name]:

Technology Stack:
- Framework: Next.js 14.1.0
- Language: TypeScript 5.3.3
- Database: PostgreSQL (Prisma 5.8.0)
- Testing: Vitest 1.2.0

Patterns Found:
- 12 naming conventions
- 8 code organization patterns
- 5 testing patterns

Key Areas for Rules:
- TypeScript strict mode configuration
- React hooks usage patterns
- API error handling conventions

Ready to generate project context rules.
```

---

### 7. Checkpoint

**Menu:**
- **[C] Continue** - Proceed to Step 2: Generate Rules
- **[R] Revise** - Adjust discovery or add sources
- **[X] Exit** - Save progress and stop

**On Continue:** Update frontmatter `current_step: 2`, load `{nextStepFile}`
