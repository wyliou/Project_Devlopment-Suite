---
name: 'step-01b-continue'
description: 'Handle continuation of an interrupted research workflow'

# File references
step02File: './step-02-discovery.md'
step03File: './step-03-complete.md'
outputFile: '{planning_artifacts}/research-{{project_name}}.md'
---

# Step 1b: Research Workflow Continuation

## STEP GOAL

Handle continuation of an interrupted research workflow by detecting progress and resuming from the correct step.

## EXECUTION RULES

- **Auto-triggered** when existing workflow detected
- Focus on state detection and seamless continuation
- Preserve all existing work in the document

## SEQUENCE (Follow Exactly)

### 1. Analyze Existing Document

Read the existing document at `{outputFile}` and extract:

- `stepsCompleted` array from frontmatter
- Existing content sections
- Product concept from frontmatter

### 2. Determine Next Step

**Step Routing Logic:**

| stepsCompleted | Next Step | Action |
|----------------|-----------|--------|
| `['step-01-init']` | step-02-discovery | Research discovery |
| `['step-01-init', 'step-02-discovery']` | step-03-complete | Finalization |
| `['step-01-init', 'step-02-discovery', 'step-03-complete']` | Complete | Workflow finished |

### 3. Report Continuation Status

**Continuation Report:**
"Welcome back! I found your existing research for {{project_name}}.

**Progress Detected:**
- Steps completed: [list by name]
- Document: `{outputFile}`

**Existing Research:**
[Brief summary of what's in the document]

**Next Step:** [Name]

Ready to continue?"

### 4. Route to Correct Step

Based on `stepsCompleted`:

- If next is discovery: load and execute `{step02File}`
- If next is complete: load and execute `{step03File}`
- If already complete: Inform user and offer to start fresh

---

## SUCCESS CRITERIA

- Correctly detected workflow state
- Accurate summary of existing progress
- Proper routing to correct next step
- Preserved all existing content
