---
name: 'step-01-init'
description: 'Initialize PRD workflow - detect state, discover inputs, setup document, handle continuation'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-02-discovery.md'
outputFile: '{project_root}/docs/prd.md'
prdTemplate: '{skills_root}/_prd-data/prd-template.md'
prdPurpose: '{skills_root}/_prd-data/prd-purpose.md'

# Resume step mapping
step02File: '{skill_base}/steps-create-prd/step-02-discovery.md'
step03File: '{skill_base}/steps-create-prd/step-03-requirements.md'
step04File: '{skill_base}/steps-create-prd/step-04-specifications.md'
step05File: '{skill_base}/steps-create-prd/step-05-complete.md'
---

# Step 1: Init

**Progress: Step 1 of 5** - Next: Discovery

## STEP GOAL

Detect workflow state, discover input documents, setup PRD document, and handle continuation of interrupted workflows.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a PRD Creator - a product-focused facilitator
- Focus on setup - no content creation yet
- Continuation is handled inline (no separate step file)

## SEQUENCE (Follow Exactly)

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` + missing `step-05-complete` | → Continuation Branch (Section 2 below) |
| File exists + NO `stepsCompleted` (unmanaged) | → Safeguard Protocol (Section 3) |
| File not exists | → Fresh Setup (Section 4) |

### 2. Continuation Branch (Inline — replaces step-01b)

If existing file has `stepsCompleted` array but workflow is incomplete:

#### A. Validate Frontmatter

| Field | Requirement |
|-------|-------------|
| `stepsCompleted` | Array, not empty (at least `step-01-init`) |
| `inputDocuments` | Array (can be empty) |
| `workflowType` | Should equal `'prd'` |

**If validation fails:**
"Frontmatter validation failed: {specific errors}

Options:
- [R] Reset - Backup current file and start fresh
- [M] Manual fix - Show what needs correction
- [A] Abort - Stop for manual investigation"

Wait for user choice.

#### B. Restore Context

1. Reload all documents listed in `inputDocuments` array (no new discovery needed).
2. Load `{prdPurpose}` for quality standards context (normally loaded in step-02, but skipped on continuation).

#### C. Determine Resume Point

**5-step workflow mapping:**

| Last Completed | Resume At | File |
|----------------|-----------|------|
| `step-01-init` | Step 2: Discovery | `{step02File}` |
| `step-02-discovery` | Step 3: Requirements | `{step03File}` |
| `step-03-requirements` | Step 4: Specifications | `{step04File}` |
| `step-04-specifications` | Step 5: Complete | `{step05File}` |

**Backward compatibility (old 4-step workflows):**

| Last Completed | Condition | Resume At | File |
|----------------|-----------|-----------|------|
| `step-04-complete` | — | Workflow already complete | → Already Complete options |
| `step-03-requirements` | Section 4 has NFR content AND Section 5 has entity content | Step 5: Complete | `{step05File}` |
| `step-03-requirements` | Section 4 or Section 5 is empty/placeholder | Step 4: Specifications | `{step04File}` |

#### D. Check if Already Complete

**If `step-05-complete` or `step-04-complete` in `stepsCompleted`:**

"Workflow already complete.

Options:
- [V] Validate - Run /prd-validate
- [A] Architecture - Run /create-architecture
- [E] Edit - Run /prd-edit
- [X] Exit"

#### E. Report & Menu

"**Resuming PRD Workflow**

**Document:** {outputFile}
**Progress:** {count}/5 steps completed

**Completed:**
{list completed steps}

**Next:** {next step name}

**Context:** {count} input documents loaded

Ready to continue?"

**[C] Continue** - Resume from next step
**[R] Restart** - Start over from step 2 (keeps document)
**[X] Exit** - Stop workflow

**C (Continue):** Load and execute the appropriate step file based on resume point.

**R (Restart):** Reset frontmatter: `stepsCompleted: ['step-01-init']`, load and execute `{step02File}`

**X (Exit):** Exit workflow

### 3. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing PRD at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `prd_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 4. Fresh Setup

#### A. Discover Input Documents

Search locations: `{product_knowledge}/**`, `docs/**`

| Type | Pattern |
|------|---------|
| Product Brief | `*brief*.md` or `*brief*/index.md` |
| Research | `*research*.md` or `*research*/index.md` |
| Project Docs | Other `.md` files in search locations |

**Detect Project Type:**
- Scan for source code (`src/**/*.py`, `**/*.js`, etc.)
- Source found → **Brownfield**
- No source → **Greenfield**

**Report discoveries to user and ask for confirmation before loading.**

#### B. Validate & Load Files

Before loading:
1. Verify each confirmed file exists
2. If missing files, present options: [S]kip / [P]rovide path / [A]bort
3. Verify `{prdTemplate}` exists
4. Load all confirmed files completely (no offset/limit)

#### C. Create Document

- Copy `{prdTemplate}` to `{outputFile}`
- Initialize frontmatter with `inputDocuments` array and `stepsCompleted: []`

### 5. Report & Menu

**Report:**
- Document created/migrated
- Input documents loaded (with counts by type)
- Project type (Brownfield/Greenfield)

**Menu:**

**[C] Continue** - Proceed to Discovery (Step 2)
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-init']`), then load and execute `{nextStepFile}`.

---

## SUCCESS CRITERIA

- Workflow state detected correctly (fresh, continuation, or unmanaged)
- Continuation handled inline with correct resume point mapping
- Input documents discovered and loaded
- PRD document created or migrated
- User confirmed setup before proceeding
