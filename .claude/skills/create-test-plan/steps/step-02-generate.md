---
name: 'step-02-generate'
description: 'Generate test plan document'
outputFile: '{project_root}/docs/test-plan.md'
template: '{skill_base}/test-plan.template.md'
---

# Step 2: Generate

**Progress:** Step 2 of 2 → Final Step

**Goal:** Generate the complete test plan document.

---

## Instructions

### 1. Create Document

Copy `{template}` to `{outputFile}` and populate all sections.

---

### 2. Test Case Format

Each test case should include:

```markdown
#### TC-{NNN}: {Descriptive Name}

| Field | Value |
|-------|-------|
| **Requirement** | FR-xxx |
| **Priority** | P0/P1/P2 |
| **Type** | Positive / Negative / Boundary |

**Preconditions:**
- {What must be true before test}

**Test Steps:**
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | {Specific action} | {Specific expected outcome} |

**Status:** ⬜ Not Started
```

---

### 3. Naming Convention

Test Case IDs: `TC-{Area}{Number}`

Examples:
- TC-AUTH-001 (Authentication test 1)
- TC-ORD-001 (Order test 1)
- TC-USR-001 (User test 1)

---

### 4. Build Traceability Matrix

Map every FR to at least one test case:

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| FR-xxx | TC-001, TC-002 | ✅ |
| FR-xxx | - | ⚠️ Gap |

Flag gaps for user attention.

---

### 5. Validate Completeness

| Check | Required |
|-------|----------|
| All P0 FRs have tests | Yes |
| All P1 FRs have tests | Yes |
| Positive + Negative for key flows | Yes |
| Error handling tested | Yes |
| NFR tests defined | If NFRs exist |
| Test environment documented | Yes |

---

### 6. Present Document

"**Test Plan Generated**

**System:** {name}

**Coverage:**
- Total test cases: {count}
- P0 (Critical): {count}
- P1 (High): {count}
- Traceability: {x}% FRs covered

**Gaps identified:** {count or "None"}

Review the document. Any adjustments needed?"

---

### 7. Finalize

**Menu:**
```
[V] View → Display full document
[R] Revise → Make changes
[X] Exit → Complete
```

**On [X]:**

Update frontmatter:
```yaml
stepsCompleted: ['step-01-analyze', 'step-02-generate']
completedAt: '{timestamp}'
prdSource: '{prd_path}'
```

**Completion Message:**
"Test plan saved to `{outputFile}`.

**UAT checklist:**
- [ ] Review with business stakeholders
- [ ] Prepare test environment
- [ ] Create test accounts
- [ ] Prepare test data
- [ ] Schedule UAT sessions
- [ ] Execute tests and log results
- [ ] Get sign-off

**Next steps:**
- Execute UAT before deployment
- Run `/create-change-request` when UAT passes"
