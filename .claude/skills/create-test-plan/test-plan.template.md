---
stepsCompleted: []
workflowType: 'test-plan'
prdSource: ''
---

# Test Plan: {{system_name}}

**Version:** {{version}}
**Date:** {{date}}
**Author:** {{author}}

---

## Overview

### Objective
{{Purpose of this test plan}}

### Scope
**In Scope:**
- {{Feature/area to be tested}}

**Out of Scope:**
- {{What won't be tested and why}}

### Approach
{{Testing approach - manual UAT, automated, exploratory, etc.}}

### Success Criteria
- All P0 test cases pass
- All P1 test cases pass
- No critical defects open
- Business sign-off obtained

---

## Test Environment

| Item | Details |
|------|---------|
| **Environment** | {{UAT / Staging URL}} |
| **Access** | {{How testers get access}} |
| **Test Data** | {{Where test data comes from}} |
| **Browser/Device** | {{Supported platforms}} |

### Test Accounts
| Role | Username | Password |
|------|----------|----------|
| {{role}} | {{user}} | {{See secure storage}} |

---

## Test Cases

### {{Capability Area 1}}

#### TC-001: {{Test Case Name}}

| Field | Value |
|-------|-------|
| **Requirement** | FR-xxx |
| **Priority** | {{P0/P1/P2}} |
| **Type** | {{Positive / Negative / Boundary}} |

**Preconditions:**
- {{Setup required before test}}

**Test Steps:**
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | {{action}} | {{expected}} |
| 2 | {{action}} | {{expected}} |
| 3 | {{action}} | {{expected}} |

**Actual Result:** {{To be filled during testing}}

**Status:** ⬜ Not Started / ✅ Pass / ❌ Fail

**Notes:** {{Any observations}}

---

#### TC-002: {{Test Case Name}}

| Field | Value |
|-------|-------|
| **Requirement** | FR-xxx |
| **Priority** | {{P0/P1/P2}} |
| **Type** | {{Positive / Negative / Boundary}} |

**Preconditions:**
- {{Setup required}}

**Test Steps:**
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | {{action}} | {{expected}} |
| 2 | {{action}} | {{expected}} |

**Status:** ⬜ Not Started

---

### {{Capability Area 2}}

#### TC-003: {{Test Case Name}}

| Field | Value |
|-------|-------|
| **Requirement** | FR-xxx |
| **Priority** | {{P0/P1/P2}} |

**Preconditions:**
- {{Setup required}}

**Test Steps:**
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | {{action}} | {{expected}} |

**Status:** ⬜ Not Started

---

## Non-Functional Tests

### Performance
| Test | Criteria | Status |
|------|----------|--------|
| Page load time | < {{x}} seconds | ⬜ |
| API response | < {{x}} ms | ⬜ |

### Security
| Test | Criteria | Status |
|------|----------|--------|
| Authentication required | All protected routes | ⬜ |
| Authorization enforced | Role-based access | ⬜ |

### Accessibility
| Test | Criteria | Status |
|------|----------|--------|
| Keyboard navigation | All functions accessible | ⬜ |
| Screen reader | Labels present | ⬜ |

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| FR-xxx | TC-001, TC-002 | ✅ |
| FR-xxx | TC-003 | ✅ |
| FR-xxx | - | ⚠️ Missing |

---

## Defect Log

| ID | Test Case | Severity | Description | Status |
|----|-----------|----------|-------------|--------|
| | | | | |

---

## Test Summary

### Execution Summary
| Priority | Total | Passed | Failed | Blocked | Not Run |
|----------|-------|--------|--------|---------|---------|
| P0 | | | | | |
| P1 | | | | | |
| P2 | | | | | |

### Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| QA Lead | | | |
| Business Owner | | | |
| Project Manager | | | |

---

## Appendix

### Test Data Requirements
{{Details on test data needed}}

### Known Issues
{{Issues known before testing}}
