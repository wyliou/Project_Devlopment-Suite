---
name: create-test-plan
description: Create UAT test plan and test cases from PRD
---

# Create Test Plan Workflow

**Goal:** Create a test plan with UAT test cases derived from PRD functional requirements.

**Your Role:** QA analyst creating comprehensive test scenarios for user acceptance testing.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Analyze** | Extract test scenarios from PRD |
| 2 | **Generate** | Create test plan document |

---

## OUTPUT FORMAT

```markdown
# Test Plan: {system_name}

## Overview
- Scope, objectives, approach

## Test Environment
- Environment details, test data

## Test Cases

### TC-001: {Test Case Name}
- **Requirement:** FR-xxx
- **Priority:** P0/P1/P2
- **Preconditions:** {setup needed}
- **Steps:**
  1. {action}
  2. {action}
- **Expected Result:** {outcome}
- **Status:** Not Started / Pass / Fail

## Test Summary
- Coverage matrix
- Sign-off section
```

---

## TEST CASE DERIVATION

From PRD Functional Requirements:

| FR Element | Becomes |
|------------|---------|
| Input | Test data / preconditions |
| Rules | Test scenarios (positive + negative) |
| Output | Expected results |
| Error | Negative test cases |

---

## Execution

Load and execute `./steps/step-01-analyze.md` to begin.
