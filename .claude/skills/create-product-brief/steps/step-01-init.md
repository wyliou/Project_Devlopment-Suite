---
name: 'step-01-init'
description: 'Initialize project charter workflow - detect state, discover docs, setup document'
nextStepFile: '{skill_base}/steps/step-02-discovery.md'
continueStepFile: '{skill_base}/steps/step-01b-continue.md'
outputFile: '{project_root}/docs/project-charter.md'
briefTemplate: '{skill_base}/project-charter.template.md'
---

# Step 1: Workflow Initialization

**Progress:** Step 1 of 4 → Next: Discovery

**Goal:** Detect workflow state, discover input documents, and setup project charter document.

---

## Instructions

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` + not complete | → Load `{continueStepFile}` |
| File exists + NO `stepsCompleted` | → Ask: Migrate or Backup? |
| File not exists | → Fresh Setup |

---

### 2. Fresh Setup

#### A. Discover Input Documents

Search locations: `docs/**`, `{product_knowledge}/**`

| Type | Pattern |
|------|---------|
| Research | `*research*.md` |
| Brainstorming | `*brainstorm*.md` |
| Project Context | `*context*.md` |

**Report discoveries to user:**
"Found these documents:
- Research: {count}
- Brainstorming: {count}
- Project Context: {count}

Should I load these? Any others to include?"

Wait for confirmation before loading.

#### B. Load Confirmed Documents

- Load all confirmed files completely
- Track in frontmatter `inputDocuments` array

#### C. Create Document

- Copy `{briefTemplate}` to `{outputFile}`
- Initialize frontmatter with `stepsCompleted: []` and `inputDocuments`

---

### 3. Report & Proceed

**Report to user:**
"Project charter initialized at `{outputFile}`.

Loaded {count} input document(s).

Ready to begin discovery."

**Menu:**
```
[C] Continue → Discovery (Step 2)
```

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-init']`), then load and execute `{nextStepFile}`.
