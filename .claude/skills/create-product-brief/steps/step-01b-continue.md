---
name: 'step-01b-continue'
description: 'Resume interrupted project charter workflow from last completed step'
outputFile: '{project_root}/docs/project-charter.md'
---

# Step 1B: Workflow Continuation

**Goal:** Resume project charter workflow from where it was left off.

---

## Instructions

### 1. Validate Frontmatter

Check the existing document's frontmatter:

| Field | Requirement |
|-------|-------------|
| `stepsCompleted` | Array, not empty |
| `workflowType` | Must equal `'project-charter'` |

**If validation fails:** Offer to reset or fix manually.

---

### 2. Restore Context

Reload all documents listed in `inputDocuments` array.

---

### 3. Determine Next Step

**Step Mapping:**

| Last Completed | Next Step File |
|----------------|----------------|
| `step-01-init` | `./step-02-discovery.md` |
| `step-02-discovery` | `./step-03-scope.md` |
| `step-03-scope` | `./step-04-complete.md` |

1. Get last element from `stepsCompleted` array
2. Use mapping to determine next step

---

### 4. Check Completion

**If `step-04-complete` in `stepsCompleted`:**

"Project charter is already complete.

Options:
- Review the completed charter
- Run /prd-create to generate PRD
- Start a new charter"

---

### 5. Report & Proceed

**If workflow not complete:**

"Resuming project charter workflow.

Last completed: {last step}
Next step: {next step name}
Context documents: {count} loaded

[C] Continue → {next step name}"

**On [C]:** Load and execute the next step file.
