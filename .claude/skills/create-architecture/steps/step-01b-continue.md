---
name: 'step-01b-continue'
description: 'Resume interrupted architecture workflow'
outputFile: '{planning_artifacts}/architecture.md'
---

# Step 1b: Continue Architecture Workflow

**Purpose:** Resume an interrupted architecture workflow from where it left off.

---

## Instructions

### 1. Detect Existing Architecture

Search for in-progress architecture: `{planning_artifacts}/architecture.md`, `{output_folder}/architecture.md`

**If not found:** "No in-progress architecture found. Starting fresh." → Load `step-01-discovery.md`

**If found:** Read and check frontmatter for `status: in-progress`

---

### 2. Determine Resume Point

Read frontmatter `current_step` value:

| Step Value | Resume Action |
|------------|---------------|
| 1 | Load `step-01-discovery.md` (restart step 1) |
| 2 | Load `step-02-structure.md` |
| 3 | Load `step-03-specifications.md` |

---

### 3. Load PRD Context

From frontmatter `prd_source`, reload the PRD document to restore context.

**If PRD not found at stored path:** Ask user for new path.

---

### 4. Present Resume Summary

Show user:
- Architecture document path
- PRD source path
- Current progress (step X of 3)
- What's already completed (check filled sections)

**Example:**
```
Resuming architecture workflow:
- Document: planning/architecture.md
- PRD: planning/prd.md
- Progress: Step 2 of 3 (Structure)
- Completed: Technology Stack ✓

Continue from Step 2: Structure & Patterns?
```

**Menu:**
- **[C] Continue** - Resume from detected step
- **[R] Restart** - Begin fresh (will overwrite)
- **[X] Exit** - Stop without changes

---

### 5. Resume

On Continue: Load the appropriate step file based on `current_step` value.
