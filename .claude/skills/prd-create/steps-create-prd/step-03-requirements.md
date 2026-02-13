---
name: 'step-03-requirements'
description: 'Generate Functional Requirements with systematic capability mapping'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-04-specifications.md'
outputFile: '{project_root}/docs/prd.md'
---

# Step 3: Requirements

**Progress: Step 3 of 5** - Next: Specifications

## STEP GOAL

Generate comprehensive, AI-implementation-ready Functional Requirements through systematic capability mapping. This step handles FRs ONLY — NFRs, Data Entities, and Tech Constraints are handled in step 4.

## EXECUTION RULES

- **Interactive step** - requires user feedback on requirements
- You are a PRD Creator - generating AI-optimized requirements
- Apply quality checks during generation, not as separate step
- This step is FR-only — do NOT generate NFRs, Data Entities, or Tech Constraints here

## SEQUENCE (Follow Exactly)

### 1. Analyze Context

Review the PRD document sections 1-2 (Overview, User Journeys) to understand:
- User types and their goals
- MVP scope items
- User journey steps → these imply capabilities
- Capability areas confirmed in step-02 preview

### 2. Systematic Capability Mapping

Before writing any FRs, check for the persisted capability areas from step-02:

1. **Look for `<!-- CAPABILITY_AREAS: ... -->` comment** in `{outputFile}` after Section 2
   - If found: use as starting point (already user-approved)
   - If not found: derive from scope items + journey steps (same as step-02 preview)

2. **Build coverage map** to verify completeness:

```markdown
| Scope Item | Capability Area | Capabilities | Journey References |
|------------|----------------|--------------|-------------------|
| {scope item 1} | {area name} | {what the system must do} | {journey step refs} |
| {scope item 2} | {area name} | {what the system must do} | {journey step refs} |
```

3. **Cross-reference:** Flag scope items without a capability area, and capability areas with no scope items.

4. **Present to user for confirmation** — only if changes were made or areas were derived fresh. If using the persisted list unchanged, briefly confirm and proceed.

### 3. Generate Functional Requirements

For each capability area identified in the mapping:

#### FR Format
```markdown
### {Capability Area Name}

**FR-001**: [Actor] [capability]
- **Input:** field1 (type, format constraint, validation rule), field2 (type, constraints)
- **Rules:** IF condition THEN action; ELSE alternative. Express as business logic, not implementation.
- **Output:** Observable result. What changes in system state? What does the user see?
- **Error:** trigger condition → handling; second condition → handling. Be exhaustive.
- **Depends:** FR-xxx (if any)
```

FRs are grouped under `### Capability Area Name` section headers. The header carries the domain context — IDs are sequential (`FR-001`, `FR-002`, ...).

**For large projects (15+ FRs):** Area-based IDs (`FR-AUTH-001`) are acceptable if the user prefers them. The capability area is still in the section header regardless of ID format.

#### Expanded Field-Level Guidance

| Field | Guidance |
|-------|----------|
| **Input** | List every field with type, format constraint, and validation rule. E.g., `email (string, RFC 5322, required, unique)` |
| **Rules** | Express as IF/THEN/ELSE business logic. Avoid implementation language (no "database", "API call"). Focus on what, not how. |
| **Output** | Describe observable result. What changes in system state? What does the user see/receive? Must be testable. |
| **Error** | List each error case with `trigger condition → handling`. Be exhaustive — cover validation errors, authorization failures, state conflicts, resource limits. |
| **Depends** | Reference other FRs this requires. Only include if there's a true dependency. |

#### FR Depth Adaptation

Adapt detail level to project scale while keeping the same format:

| Project Scale | Depth Guidance |
|--------------|----------------|
| Production (5+ FRs) | Full detail — exhaustive input constraints, comprehensive error cases, precise validation rules |
| Small / Prototype (< 5 FRs) | Essential detail — key constraints and primary error cases. Skip edge-case errors and granular validation rules. |

The Input/Rules/Output/Error **format** is always used (downstream tools depend on it). What changes is the **depth** within each field.

#### Quality Checks (Apply During Generation)
- Actor is explicit (User, System, Admin)
- Input has constraints (types, formats, limits)
- Rules capture business logic, not implementation
- Output is specific and testable
- Error handling is explicit (exhaustive for production; primary cases for prototypes)
- Dependencies are noted

### 4. FR Completeness Verification

After generating all FRs, build a coverage matrix:

```markdown
| Scope Item | FRs | Coverage |
|------------|-----|----------|
| {scope item 1} | FR-xxx, FR-xxx | Complete / Partial / Missing |

| Journey Step | FRs | Coverage |
|--------------|-----|----------|
| {user type}: {step} | FR-xxx | Complete / Partial / Missing |
```

**Every scope item must map to at least 1 FR.** Every journey step must map to at least 1 FR.

**If gaps found:** Generate additional FRs to fill coverage gaps before proceeding.

### 5. Present to User

Show the user:
1. Summary: "Generated X FRs across Y capability areas"
2. Coverage matrix summary
3. Key dependencies identified
4. Any assumptions made

Ask for feedback on:
- Missing capabilities?
- FR precision (are inputs/rules/outputs clear enough?)
- Additional error cases?

### 6. Report & Menu

**Menu:**

**[C] Continue** - Proceed to Specifications (Step 4)
**[R] Revise** - Modify requirements, add missing capabilities
**[P] Party Mode** - Multi-agent review of requirements completeness and quality
**[D] Deep Dive** - Apply advanced elicitation on complex requirements
**[X] Exit** - Save progress and stop

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-03-requirements'`), then load and execute `{nextStepFile}`.

**On [R]:** Make specific changes, re-verify coverage, return to menu.

**On [P]:** Invoke `/_party-mode` skill with topic "Requirements review for [project name]", content = Section 3 FRs + coverage matrix, focus_agents = `pm`, `architect`, `dev`, `qa`. After discussion, apply insights and return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore complex requirements, edge cases, or business rules more thoroughly. After deep dive, update requirements with insights and return to menu.

**On [X]:** Update frontmatter (`stepsCompleted` add `'step-03-requirements'`), exit workflow.

---

## SUCCESS CRITERIA

- Capability mapping built and confirmed by user before FR generation
- FRs generated with Input/Rules/Output/Error format
- Every scope item maps to at least 1 FR
- Every journey step maps to at least 1 FR
- FR quality checks pass (explicit actors, constrained inputs, testable outputs, exhaustive errors)
- User confirmed requirements before proceeding
