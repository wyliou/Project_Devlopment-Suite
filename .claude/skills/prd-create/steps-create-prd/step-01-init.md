---
name: 'step-01-init'
description: 'Initialize PRD workflow - detect state, discover inputs, determine output path, setup document, handle continuation'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-02-discovery.md'
defaultOutputFile: '{project_root}/docs/prd.md'
prdTemplate: '{skills_root}/_prd-data/prd-template.md'
prdPurpose: '{skills_root}/_prd-data/prd-purpose.md'
projectTypesCSV: '{skills_root}/_prd-data/project-types.csv'

# Resume step mapping
step02File: '{skill_base}/steps-create-prd/step-02-discovery.md'
step03File: '{skill_base}/steps-create-prd/step-03-journeys.md'
step04File: '{skill_base}/steps-create-prd/step-04-requirements.md'
step05File: '{skill_base}/steps-create-prd/step-05-specifications.md'
step06File: '{skill_base}/steps-create-prd/step-06-complete.md'
---

# Step 1: Init

**Progress: Step 1 of 6** - Next: Discovery

## STEP GOAL

Detect workflow state, determine output path, discover input documents, setup PRD document, and handle continuation of interrupted workflows.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a PRD Creator - a product-focused facilitator
- Focus on setup - no content creation yet
- Continuation is handled inline (no separate step file)

## SEQUENCE (Follow Exactly)

### 1A. Determine Output Path

Ask the user where to save the PRD:

"Where should the PRD be saved? Default: `{defaultOutputFile}`"

If user provides a path, use it. Otherwise use `{defaultOutputFile}`. Store this as `outputPath` for all subsequent steps.

### 1B. Multi-PRD Discovery

Search for existing PRD files: `docs/*prd*.md`, `docs/*PRD*.md`

**If multiple PRD files found:**

"Found existing PRDs:
1. `{path_1}` — {first line or title}
2. `{path_2}` — {first line or title}
...

Which would you like to work with?
- [1-N] Select an existing PRD
- [New] Create a new PRD at `{outputPath}`"

Wait for user choice. If an existing PRD is selected, update `outputPath` to that file.

### 1C. Check Workflow State

Check if the file at `outputPath` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` + missing `step-06-complete` | → Continuation Branch (Section 2 below) |
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
| `capabilityAreas` | Array (can be empty) |

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

**6-step workflow mapping:**

| Last Completed | Resume At | File |
|----------------|-----------|------|
| `step-01-init` | Step 2: Discovery | `{step02File}` |
| `step-02-discovery` | Step 3: Journeys & Mapping | `{step03File}` |
| `step-03-journeys` | Step 4: Requirements | `{step04File}` |
| `step-04-requirements` | Step 5: Specifications | `{step05File}` |
| `step-05-specifications` | Step 6: Complete | `{step06File}` |

**Backward compatibility (PRDs created under old 4-step or 5-step workflows — these step names may exist in their frontmatter):**

| Last Completed | Condition | Resume At | File |
|----------------|-----------|-----------|------|
| `step-04-complete` | — | Workflow already complete | → Already Complete options |
| `step-05-complete` | — | Workflow already complete | → Already Complete options |
| `step-03-requirements` | Contains `**NFR-` pattern AND >3 non-empty lines in Section 4 | Step 6: Complete | `{step06File}` |
| `step-03-requirements` | Section 4 or Section 5 is empty/placeholder | Step 5: Specifications | `{step05File}` |

#### D. Check if Already Complete

**If `step-06-complete` or `step-05-complete` or `step-04-complete` in `stepsCompleted`:**

"Workflow already complete.

Options:
- [V] Validate - Run /prd-validate
- [A] Architecture - Run /create-architecture
- [E] Edit - Run /prd-edit
- [X] Exit"

#### E. Report & Menu

"**Resuming PRD Workflow**

**Document:** {outputPath}
**Progress:** {count}/6 steps completed

**Completed:**
{list completed steps}

**Next:** {next step name}

**Context:** {count} input documents loaded

Ready to continue?"

**[C] Continue** - Resume from next step
**[R] Restart** - Start over from step 2 (keeps document)
**[X] Exit** - Stop workflow

**C (Continue):** Load and execute the appropriate step file based on resume point.

**R (Restart):** Reset frontmatter: `stepsCompleted: ['step-01-init']`, and begin Discovery again. Note: existing document content will be overwritten as each step is re-run. Load and execute `{step02File}`.

**X (Exit):** Exit workflow

### 3. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing PRD at `{outputPath}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `prd_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 4. Fresh Setup

#### A. Discover Input Documents

Search for product knowledge documents in common locations:

**Search paths (check each, skip if not found):**
- `docs/`
- `product_knowledge/` (if exists)
- Project root `.md` files

| Type | Pattern |
|------|---------|
| Product Brief | `*brief*.md` or `*brief*/index.md` |
| Research | `*research*.md` or `*research*/index.md` |
| Project Docs | Other `.md` files in search locations |

**If no documents found or user confirms none are relevant:**
"Proceeding without input documents. We'll gather all context through our conversation."
Store `inputDocuments: []` in frontmatter and continue to Fresh Setup section 4C.

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

#### B2. Template Fallback

**If `{prdTemplate}` not found:** Display warning and generate minimal inline skeleton:

"Warning: PRD template not found at `{prdTemplate}`. Using minimal inline skeleton."

Generate a document with complete frontmatter and 8 section headers:

```yaml
---
stepsCompleted: []
inputDocuments: []
workflowType: 'prd'
completedAt: ''
documentChecksum: ''
capabilityAreas: []
outputPath: '{outputPath}'
---
```

Then add 8 section headers (`## 1. Overview` through `## 8. Implementation Reference`) with placeholder content.

#### C. Create Document

- Copy `{prdTemplate}` to `{outputPath}`
- Initialize frontmatter with:
  - `stepsCompleted: []`
  - `inputDocuments: [...]` (list of loaded docs)
  - `workflowType: 'prd'`
  - `completedAt: ''`
  - `documentChecksum: ''`
  - `capabilityAreas: []`
  - `outputPath: '{outputPath}'`

Subsequent steps read `outputPath` from frontmatter rather than using a hardcoded value.

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
- Output path determined and stored in frontmatter
- Multi-PRD discovery handled if multiple PRDs exist
- Continuation handled inline with correct resume point mapping
- Input documents discovered and loaded
- PRD document created or migrated with `capabilityAreas` and `outputPath` in frontmatter
- User confirmed setup before proceeding
