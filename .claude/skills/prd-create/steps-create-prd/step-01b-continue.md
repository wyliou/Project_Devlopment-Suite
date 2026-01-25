---
name: 'step-01b-continue'
description: 'Resume interrupted PRD workflow from last completed step'

# File references
outputFile: '{project_root}/docs/prd.md'
step02File: '{skill_base}/steps-create-prd/step-02-discovery.md'
step03File: '{skill_base}/steps-create-prd/step-03-requirements.md'
step04File: '{skill_base}/steps-create-prd/step-04-complete.md'
---

# Step 1b: Continue

**Purpose:** Resume interrupted workflow from last completed step.

## STEP GOAL

Detect where the workflow was interrupted and resume from the correct step.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- Auto-triggered when existing PRD has incomplete `stepsCompleted`
- You are a PRD Creator resuming previous work

## SEQUENCE (Follow Exactly)

### 1. Validate Frontmatter

Check the existing document's frontmatter:

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

### 2. Restore Context

Reload all documents listed in `inputDocuments` array (no new discovery needed).

### 3. Determine Resume Point

**Check last completed step:**

| Last Completed | Resume At | File |
|----------------|-----------|------|
| `step-01-init` | Step 2: Discovery | `{step02File}` |
| `step-02-discovery` | Step 3: Requirements | `{step03File}` |
| `step-03-requirements` | Step 4: Complete | `{step04File}` |

### 4. Check if Already Complete

**If `step-04-complete` in `stepsCompleted`:**

"Workflow already complete.

Options:
- [V] Validate - Run /prd-validate
- [A] Architecture - Run /create-architecture
- [E] Edit - Run /prd-edit
- [X] Exit"

### 5. Report State

"**Resuming PRD Workflow**

**Document:** {outputFile}
**Progress:** {count}/4 steps completed

**Completed:**
{list completed steps}

**Next:** {next step name}

**Context:** {count} input documents loaded

Ready to continue?"

### 6. Menu

**[C] Continue** - Resume from next step
**[R] Restart** - Start over from step 2 (keeps document)
**[X] Exit** - Stop workflow

#### Menu Logic:

**C (Continue):**
Load and execute the appropriate step file based on resume point.

**R (Restart):**
- Reset frontmatter: `stepsCompleted: ['step-01-init']`
- Load and execute `{step02File}`

**X (Exit):**
Exit workflow

---

## SUCCESS CRITERIA

- Workflow state correctly detected
- Resume point accurately identified
- Context documents restored
- User confirmed continuation
- Correct step file loaded
