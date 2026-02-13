---
name: 'step-03-modules'
description: 'Define module boundaries, inter-module interfaces, and project-type-adaptive contracts'
nextStepFile: '{skill_base}/steps/step-04-finalize.md'
outputFile: '{planning_artifacts}/architecture.md'
---

# Step 3: Modules & Contracts

**Progress:** Step 3 of 4 → Next: Schema & Finalize

**Goal:** Define module boundaries with paths/exports/dependencies, inter-module interfaces, and project-type-adaptive contracts.

---

## Instructions

### 1. Extract Capability Areas

From PRD Section 3:
- `### Capability Area` section headers → each becomes a potential module
- FRs grouped under each header → define module responsibilities
- Quick Reference dependencies → inform module dependency graph
- User Journeys → inform flow between modules

### 2. Define Module Boundaries

Create the enhanced module table with all columns build-from-prd needs:

| Module | Path | Test Path | Responsibility | Implements | Exports | Depends On |
|--------|------|-----------|----------------|------------|---------|------------|
| {area} | `src/{path}/` | `tests/{path}/` | {what it does} | FR-001, FR-002, ... | {exported functions/classes} | {other modules} |

**Deriving each column:**
- **Path:** From directory structure defined in Step 2. Follow framework conventions.
- **Test Path:** Mirror source path under test directory.
- **Responsibility:** One-line summary of what the module does.
- **Implements:** List all FR IDs this module handles (from the matching capability area section).
- **Exports:** List the public functions/classes/types this module exposes. Derive from FR outputs — what other modules need to call.
- **Depends On:** List other modules this one imports from. Derive from FR dependency chains and data flow between areas.

### 3. Define Inter-Module Interfaces

For each dependency edge in the module table, document the interface:

```markdown
### {Consumer Module} → {Provider Module}
- **Provider function:** {function name from exports}
- **Data flow:** {what data passes between them}
- **Error propagation:** {how errors from provider surface in consumer}
```

This ensures subagents in build-from-prd know exactly how to wire modules together.

### 4. Generate Contracts (Project-Type-Adaptive)

Read `product_category` from architecture frontmatter to determine contract format.

#### Web App / API Service: REST Endpoints

Group by resource. Use RESTful design (plural nouns, standard HTTP methods, nested resources).

```markdown
### METHOD /api/[route]
- **FR:** FR-###
- **Module:** {owning module from Section 4}
- **Request:** `{ field: type, ... }`
- **Response 200:** `{ data: { ... } }`
- **Response 4xx:** `{ error: { code: "...", message: "..." } }`
```

**Notes:**
- Derive route from FR subject (e.g., "Create Order" → POST /api/orders)
- Use error codes from Section 3 taxonomy
- Include path params where appropriate (`/api/orders/:id`)

#### CLI Tool: Command Specifications

```markdown
### command-name
- **FR:** FR-###
- **Module:** {owning module from Section 4}
- **Args:** `<required-arg> [optional-arg]`
- **Flags:** `--flag description (default: value)`
- **Stdin:** {accepted input format, or "N/A"}
- **Stdout:** {output format description}
- **Stderr:** {error/diagnostic output}
- **Exit Codes:** `0: success, 1: {error type}, 2: usage error`
```

#### Library/SDK: Public API Surface

```markdown
### functionName(params): ReturnType
- **FR:** FR-###
- **Module:** {owning module from Section 4}
- **Parameters:** `param1: Type - description`, `param2: Type - description`
- **Returns:** `Type - description`
- **Throws:** `ErrorType - when condition`
```

**Every contract entry MUST include `Module:` mapping it to Section 4.**

### 5. Complete Error Taxonomy

After contract generation, revisit Section 3 error taxonomy:

1. Review all error responses from contracts
2. Add domain-specific error codes for every error case
3. Cross-reference PRD Section 8.3 (Error Code Catalog) if present
4. Ensure every error code used in contracts exists in the taxonomy

Update Section 3 error taxonomy in `{outputFile}`.

### 6. Update Document

Fill Sections 4 (Module Boundaries) and 5 (Contracts) in `{outputFile}`.

Include the Import Graph in Section 4:
```markdown
### Import Graph
module-a → module-b (uses: functionX, functionY)
module-b → module-c (uses: functionZ)
```

Verify graph is acyclic. If cycles found, restructure modules (extract shared code into a common module).

### 7. Validation

Before checkpoint, verify:

| Check | Requirement |
|-------|-------------|
| FR Coverage | Every FR has at least one contract |
| Contract Mapping | Every contract maps to exactly one module |
| Module Graph | Acyclic — no circular dependencies |
| Path Consistency | Module paths match directory structure from Section 2 |
| Export Completeness | Every module has at least one export |
| Dependency Validity | Every "Depends On" entry references an existing module |

**If gaps found:** Fix before presenting checkpoint.

### 8. Checkpoint

Present to user:
- Module boundaries table
- Import graph
- Contract summary (count by type)
- Coverage: FRs without contracts (should be 0)

**Menu:**
- **[C] Continue** - Proceed to Step 4: Schema & Finalize
- **[R] Revise** - Adjust modules, interfaces, or contracts
- **[X] Exit** - Save progress and stop

**On Continue:** Update frontmatter `current_step: 4`, load `{nextStepFile}`
