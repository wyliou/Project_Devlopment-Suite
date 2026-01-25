---
name: 'step-04-complete'
description: 'Finalize project charter with validation and handoff to PRD'
outputFile: '{project_root}/docs/project-charter.md'
---

# Step 4: Complete

**Progress:** Step 4 of 4 → Workflow Complete

**Goal:** Finalize the project charter and prepare for PRD generation.

---

## Instructions

### 1. Final Validation

Verify the brief has all required sections:

| Section | Check |
|---------|-------|
| 1. Vision | Problem + Solution + Differentiators |
| 2. Users | At least 1 user with goal and pain |
| 3. Success | ONE key metric + supporting indicators |
| 4. MVP Scope | In scope + Out of scope lists |
| 5. Context | Technology + Timeline + Domain notes |
| 6. Enterprise Context | (Optional) Sponsor + Systems + Compliance |

**If any section incomplete:** Flag and ask user to complete.

---

### 2. PRD Readiness Check

Verify brief can feed into PRD:

| Brief Element | Maps to PRD |
|---------------|-------------|
| Problem + Solution | PRD Overview Vision |
| Users table | PRD Overview Users table |
| Key Success Metric | PRD Key Success Metric |
| MVP In Scope | PRD MVP Scope |
| Technology Preferences | PRD Technology Constraints |

**All elements should be present and specific.**

---

### 3. Update Frontmatter

```yaml
---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-scope', 'step-04-complete']
completedAt: '{timestamp}'
workflowType: 'project-charter'
---
```

---

### 4. Completion Report

"**Project Charter Complete**

**Document:** `{outputFile}`

**Summary:**
- Problem: {1-sentence}
- Solution: {1-sentence}
- Users: {count} user types
- Success Metric: {metric}
- MVP Scope: {in_count} in / {out_count} out
- Enterprise Context: {present/not present}

**Next Step:**
Run `/prd-create` to generate a full PRD from this charter.

The PRD workflow will:
1. Load this charter automatically
2. Expand vision into detailed Overview
3. Generate User Journeys from Users table
4. Create Functional Requirements from MVP scope
5. Define Data Entities and Quick Reference
6. Import Integration Points and Compliance Notes (if present)

Ready to create PRD?"

---

### 5. Menu

```
[P] PRD → Run /prd-create workflow
[V] View → Display the complete brief
[X] Exit → Finish
```

**On [P]:** Suggest running `/prd-create` to continue.

**On [V]:** Display the full brief document.

**On [X]:** End workflow.

---

## Workflow Complete

The project charter is now complete and optimized for PRD generation.

**Document Chain:**
```
Project Charter → PRD → Architecture → Implementation
      ↓             ↓         ↓              ↓
   Vision       Details   API/Schema      Code
   Users        FRs/NFRs  Patterns
   Scope        Entities  Structure
   Enterprise   Integration
```
