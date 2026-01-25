---
name: 'step-01b-continue'
description: 'Resume interrupted project context workflow'
outputFile: '{project_root}/docs/project-context.md'
---

# Step 1b: Continue Project Context Workflow

**Purpose:** Resume an interrupted project context workflow from where it left off.

---

## Instructions

### 1. Detect Existing Context

Search for in-progress context: `{project_root}/docs/project-context.md`

**If not found:** "No in-progress context found. Starting fresh." → Load `step-01-discover.md`

**If found:** Read and check frontmatter for `status: in-progress`

---

### 2. Determine Resume Point

Read frontmatter `current_step` value:

| Step Value | Resume Action |
|------------|---------------|
| 1 | Load `step-01-discover.md` (restart discovery) |
| 2 | Load `step-02-generate.md` |
| 3 | Load `step-03-complete.md` |

---

### 3. Restore Context

From frontmatter, restore:
- `project_name` - Project identifier
- `categories_completed` - Which rule categories are done
- Technology stack section content

**If architecture.md exists:** Reload to restore technology context.

---

### 4. Present Resume Summary

Show user:
- Project context document path
- Current progress (step X of 3)
- Categories already completed
- What remains to be done

**Example:**
```
Resuming project context workflow:
- Document: docs/project-context.md
- Project: my-project
- Progress: Step 2 of 3 (Generate Rules)
- Completed: Technology Stack, Language Rules, Framework Rules
- Remaining: Testing, Code Quality, Workflow, Don't-Miss

Continue from where you left off?
```

**Menu:**
- **[C] Continue** - Resume from detected step
- **[R] Restart** - Begin fresh (will overwrite)
- **[X] Exit** - Stop without changes

---

### 5. Resume

On Continue: Load the appropriate step file based on `current_step` value.

If resuming Step 2, also restore `categories_completed` to skip already-done categories.
