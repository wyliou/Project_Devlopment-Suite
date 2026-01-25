---
stepsCompleted: []
workflowType: 'change-request'
crNumber: ''
---

# Change Request: {{cr_number}}

**Created:** {{date}}
**Requestor:** {{requestor}}

---

## Summary

| Field | Value |
|-------|-------|
| **System** | {{system_name}} |
| **Type** | {{Standard / Normal / Emergency}} |
| **Priority** | {{Low / Medium / High / Critical}} |
| **Requested Date** | {{deployment_date}} |
| **Environment** | {{Production / Staging / etc.}} |

---

## Description

{{Clear description of what is being changed}}

---

## Business Justification

{{Why this change is needed}}

**Related Documents:**
- Business Case: {{link or N/A}}
- PRD: {{link or N/A}}
- Project Charter: {{link or N/A}}

---

## Impact Assessment

| Impact Area | Details |
|-------------|---------|
| **Users Affected** | {{number and/or user groups}} |
| **Downtime Required** | {{duration or "None - zero downtime deployment"}} |
| **Systems Affected** | {{list of systems}} |
| **Data Impact** | {{migrations, schema changes, or "None"}} |
| **Integration Impact** | {{affected integrations or "None"}} |

---

## Implementation Plan

**Deployment Window:** {{date/time}} to {{date/time}}

| Step | Action | Owner | Duration |
|------|--------|-------|----------|
| 1 | {{Pre-deployment action}} | {{who}} | {{time}} |
| 2 | {{Deployment action}} | {{who}} | {{time}} |
| 3 | {{Verification action}} | {{who}} | {{time}} |
| 4 | {{Post-deployment action}} | {{who}} | {{time}} |

---

## Rollback Plan

**Rollback Trigger:** {{criteria for initiating rollback}}

**Rollback Window:** {{how long rollback remains possible}}

| Step | Action | Owner | Duration |
|------|--------|-------|----------|
| 1 | {{Rollback action}} | {{who}} | {{time}} |
| 2 | {{Verification action}} | {{who}} | {{time}} |

---

## Testing Summary

| Test Type | Status | Evidence |
|-----------|--------|----------|
| Unit Tests | {{Pass/Fail/N/A}} | {{link or description}} |
| Integration Tests | {{Pass/Fail/N/A}} | {{link or description}} |
| UAT | {{Pass/Fail/N/A}} | {{sign-off from}} |
| Performance | {{Pass/Fail/N/A}} | {{link or description}} |
| Security Scan | {{Pass/Fail/N/A}} | {{link or description}} |

---

## Communication Plan

| Audience | Method | Timing | Message |
|----------|--------|--------|---------|
| {{End users}} | {{Email/Slack/etc.}} | {{Before/During/After}} | {{key message}} |
| {{Support team}} | {{Meeting/Doc}} | {{Before}} | {{what they need to know}} |
| {{Stakeholders}} | {{Email}} | {{After}} | {{completion notice}} |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {{risk}} | {{L/M/H}} | {{L/M/H}} | {{mitigation}} |

---

## Approvals

| Role | Name | Status | Date |
|------|------|--------|------|
| Requestor | {{name}} | Submitted | {{date}} |
| Business Owner | | Pending | |
| IT Security | | Pending | |
| CAB | | Pending | |

---

## Post-Implementation Review

*To be completed after deployment*

| Item | Status |
|------|--------|
| Deployment successful | |
| Rollback required | |
| Issues encountered | |
| Lessons learned | |
