---
name: 'step-01-analyze'
description: 'Discover PRD and architecture, extract modules, build dependency graph, create execution plan'
nextStepFile: '{skill_base}/steps/step-02-scaffold.md'
continueStepFile: '{skill_base}/steps/step-01b-continue.md'
stateFile: '{project_root}/build-state.json'
stateTemplate: '{skill_base}/build-state-template.json'
---

# Step 1: Analyze

**Progress:** Step 1 of 4 - Next: Scaffold

**Goal:** Discover input documents, extract modules, build dependency graph, and create execution plan.

---

## Execution Rules

- **Autonomous step** - no user prompts
- You are a Build Orchestrator preparing for autonomous execution
- HALT only for critical errors (missing inputs, circular deps)
- Auto-proceed to next step on success

---

## Sequence (Follow Exactly)

### 1. Check for Existing State

Check if `{stateFile}` exists.

**If exists and status is not "complete":**
- Load `{continueStepFile}` immediately (auto-resume)
- Do not proceed further in this file

**If exists and status is "complete":**
- Output: "Previous build completed. Starting fresh build..."
- Delete existing state file
- Continue with step 2

**If not exists:**
- Continue with step 2

---

### 2. Discover Input Documents

Search for required documents:

| Document | Search Locations | Pattern |
|----------|------------------|---------|
| PRD | `docs/`, `{planning_artifacts}/` | `*prd*.md`, `prd.md` |
| Architecture | `docs/`, `{planning_artifacts}/` | `*architecture*.md`, `architecture.md` |

**HALT Conditions:**

If PRD not found:
```
HALT: Build requires PRD document.
Searched: docs/, {planning_artifacts}/
Pattern: *prd*.md, prd.md

Run /prd-create first or provide path.
```

If Architecture not found:
```
HALT: Build requires architecture document.
Searched: docs/, {planning_artifacts}/
Pattern: *architecture*.md, architecture.md

Run /create-architecture first or provide path.
```

---

### 3. Detect Build Mode

Scan project for existing source code:

| Pattern | Check |
|---------|-------|
| `src/**/*.py` | Python source |
| `src/**/*.js` | JavaScript source |
| `src/**/*.ts` | TypeScript source |
| `app/**/*` | App directory |
| `lib/**/*` | Library directory |

**Mode Detection:**
- Source files found with implementation → **Brownfield**
- No source files or only stubs → **Greenfield**

Output: "Build mode: [Greenfield/Brownfield]"

---

### 4. Load and Parse Documents

Read both documents completely:

**From PRD extract:**
- Project name (Section 1)
- Functional Requirements list (Section 3)
- Data Entities (Section 5)

**From Architecture extract:**
- Technology Stack (Section 1)
- Project Structure (Section 2)
- Module Boundaries (Section 4)
- API Contracts (Section 5)
- Database Schema (Section 6)
- Environment Config (Section 7)

---

### 5. Extract Modules and Dependencies

From Architecture Section 4 (Module Boundaries), extract:

| Field | Source |
|-------|--------|
| Module name | Module header |
| Location | Path in project structure |
| FRs | Functional requirements handled |
| Dependencies | Other modules this depends on |

Build dependency map:
```
{
  "module_name": {
    "location": "src/modules/auth",
    "frs": ["FR-001", "FR-002"],
    "depends_on": ["database", "config"]
  }
}
```

---

### 6. Build Dependency Graph and Layers

**Detect Circular Dependencies:**

Run topological sort on dependency graph. If cycle detected:
```
HALT: Circular dependency detected.
Cycle: [module_a] -> [module_b] -> [module_c] -> [module_a]

Fix architecture.md Module Boundaries section and re-run.
```

**Build Layers:**

Sort modules into layers by dependency level:
- **Layer 0:** Modules with no dependencies (or only external deps)
- **Layer 1:** Modules depending only on Layer 0
- **Layer 2:** Modules depending on Layer 0 and/or Layer 1
- Continue until all modules assigned

Output:
```
Dependency Analysis:
- Layer 0: [module_a, module_b] (no deps)
- Layer 1: [module_c] (depends on L0)
- Layer 2: [module_d, module_e] (depends on L0, L1)
Total: [N] modules in [M] layers
```

---

### 7. Initialize Build State

Copy `{stateTemplate}` content and populate:

```json
{
  "status": "in-progress",
  "current_step": 1,
  "mode": "[greenfield/brownfield]",
  "prd_path": "[discovered path]",
  "prd_checksum": "[first 8 chars of sha256 of PRD content]",
  "architecture_path": "[discovered path]",
  "architecture_checksum": "[first 8 chars of sha256 of architecture content]",
  "layers": [
    {
      "level": 0,
      "modules": ["module_a", "module_b"],
      "status": "pending"
    },
    {
      "level": 1,
      "modules": ["module_c"],
      "status": "pending"
    }
  ],
  "completed_modules": [],
  "failed_modules": [],
  "retry_counts": {},
  "scaffold_complete": false,
  "started_at": "[ISO timestamp]"
}
```

Write to `{stateFile}`.

---

### 8. Output Analysis Summary

```
Build Analysis Complete
=======================
Project: [name]
Mode: [Greenfield/Brownfield]
PRD: [path]
Architecture: [path]

Modules: [N] total
Layers: [M]
  - Layer 0: [count] modules
  - Layer 1: [count] modules
  ...

Proceeding to scaffold...
```

---

### 9. Auto-Proceed

Update state: `current_step: 2`

Load and execute `{nextStepFile}`.

---

## Success Criteria

- PRD and architecture documents discovered and loaded
- Build mode detected correctly
- All modules extracted with dependencies
- No circular dependencies
- Layers computed via topological sort
- build-state.json initialized
- Auto-proceeded to step-02-scaffold.md
