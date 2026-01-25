---
name: 'step-01-analyze'
description: 'Analyze PRD and extract test scenarios'
nextStepFile: './step-02-generate.md'
outputFile: '{project_root}/docs/test-plan.md'
template: '../test-plan.template.md'
---

# Step 1: Analyze

**Progress:** Step 1 of 2 → Next: Generate

**Goal:** Extract test scenarios from PRD functional requirements.

---

## Instructions

### 1. Load PRD

Look for PRD document:
- `docs/prd.md`

**If not found:** Ask user to provide PRD location or run `/prd-create` first.

**If found:** Load and analyze.

---

### 2. Extract Functional Requirements

From PRD Section 3 (Functional Requirements), extract:

| FR ID | Summary | Input | Rules | Output | Error |
|-------|---------|-------|-------|--------|-------|

---

### 3. Derive Test Cases

For each FR, create test cases:

**From Input:**
- Valid input → Positive test
- Invalid input → Negative test
- Boundary values → Boundary test
- Missing required → Error test

**From Rules:**
- Each rule condition → Scenario
- IF/THEN → Verify THEN occurs
- Business logic → Validate logic

**From Output:**
- Success → Verify output
- State changes → Verify state

**From Error:**
- Each error condition → Negative test
- Error message → Verify message

---

### 4. Prioritize

Assign priority based on PRD Quick Reference:

| PRD Priority | Test Priority |
|--------------|---------------|
| P0-Critical | P0 - Must pass for release |
| P1-High | P1 - Should pass |
| P2-Medium | P2 - Nice to verify |
| P3-Low | P2 or skip |

---

### 5. Non-Functional Tests

From PRD Section 4 (NFRs), extract:

- Performance criteria → Performance tests
- Security requirements → Security tests
- Any accessibility requirements → Accessibility tests

---

### 6. Confirm Coverage

**Present to user:**
"Analyzed PRD and identified test scenarios:

| Area | FRs | Test Cases |
|------|-----|------------|
{coverage table}

**Priority breakdown:**
- P0 (Critical): {count}
- P1 (High): {count}
- P2 (Medium): {count}

**NFR Tests:**
- Performance: {count}
- Security: {count}

Any additional scenarios to include?"

---

### 7. Test Environment

"What's the test environment?

- UAT URL?
- How do testers get access?
- Any test accounts needed?
- Specific browsers/devices to test?"

---

### 8. Proceed

**Menu:**
```
[C] Continue → Generate test plan
[R] Revise → Adjust scenarios
```

**On [C]:** Update frontmatter, load and execute `{nextStepFile}`.
