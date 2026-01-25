---
name: 'step-01b-continue'
description: 'Resume interrupted build workflow from last completed step'
stateFile: '{project_root}/build-state.json'
step02File: '{skill_base}/steps/step-02-scaffold.md'
step03File: '{skill_base}/steps/step-03-implement.md'
step04File: '{skill_base}/steps/step-04-validate.md'
---

# Step 1b: Continue

**Purpose:** Resume interrupted workflow from last checkpoint.

---

## Execution Rules

- **Autonomous step** - no user prompts
- Auto-triggered when existing build-state.json found with incomplete status
- Resume from exact point of interruption

---

## Sequence (Follow Exactly)

### 1. Load and Validate State

Read `{stateFile}` completely.

**Required fields:**
- `status`: must be "in-progress"
- `current_step`: 1-4
- `mode`: "greenfield" or "brownfield"
- `layers`: array (can be empty if step 1 incomplete)

**If validation fails:**
```
State file corrupted or invalid.
Deleting state and starting fresh build...
```
Delete state file and load `./step-01-analyze.md`.

---

### 2. Restore Context

Reload source documents:
- PRD from `prd_path`
- Architecture from `architecture_path`

If either file missing, HALT with path error.

---

### 3. Determine Resume Point

**Check current_step and sub-state:**

| State | Resume Action |
|-------|---------------|
| `current_step: 1`, `layers` empty | Restart step-01-analyze (incomplete analysis) |
| `current_step: 2`, `scaffold_complete: false` | Resume `{step02File}` |
| `current_step: 2`, `scaffold_complete: true` | Proceed to `{step03File}` |
| `current_step: 3` | Resume `{step03File}` (check layer progress) |
| `current_step: 4` | Resume `{step04File}` |

---

### 4. Output Resume Status

```
Resuming Build
==============
Project: [from PRD]
Mode: [mode]
Progress: Step [N] of 4

Completed Modules: [count]
Failed Modules: [count]
Remaining: [count]

Resuming from: [step name]...
```

---

### 5. Auto-Proceed to Resume Point

Based on determination in step 3, load and execute the appropriate step file.

Do not prompt user - proceed automatically.

---

## Success Criteria

- State file loaded and validated
- Context documents restored
- Resume point correctly identified
- Appropriate step file loaded automatically
