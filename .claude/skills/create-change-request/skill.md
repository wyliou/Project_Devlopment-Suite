---
name: create-change-request
description: Create CAB documentation for deployment approval
---

# Create Change Request Workflow

**Goal:** Create a change request document for CAB (Change Advisory Board) approval before deployment.

**Your Role:** Change manager documenting the deployment plan, impact, and rollback procedures.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Gather** | Collect change details, impact, plan |
| 2 | **Generate** | Create change request document |

---

## OUTPUT FORMAT

```markdown
# Change Request: CR-{number}

## Summary
| Field | Value |
|-------|-------|
| System | {system name} |
| Type | Standard / Normal / Emergency |
| Priority | Low / Medium / High / Critical |
| Requested Date | {date} |
| Requestor | {name} |

## Description
{What is being changed}

## Business Justification
{Why this change is needed, link to approved project}

## Impact Assessment
- **Users Affected:** {number/groups}
- **Downtime Required:** {duration or "None"}
- **Systems Affected:** {list}
- **Data Impact:** {any data changes/migrations}

## Implementation Plan
1. {Pre-deployment step}
2. {Deployment step}
3. {Verification step}
4. {Post-deployment step}

## Rollback Plan
1. {Rollback trigger criteria}
2. {Rollback step}
3. {Verification step}

## Testing Summary
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] UAT sign-off obtained
- [ ] Performance tested

## Communication Plan
| Audience | Method | Timing |
|----------|--------|--------|

## Approvals
| Role | Name | Date |
|------|------|------|
| Business Owner | | |
| IT Security | | |
| CAB | | |
```

---

## CHANGE TYPES

| Type | Definition | Approval |
|------|------------|----------|
| **Standard** | Pre-approved, low-risk, routine | Auto-approved |
| **Normal** | Planned, follows normal process | CAB review |
| **Emergency** | Urgent fix, expedited process | Emergency CAB |

---

## Execution

Load and execute `./steps/step-01-gather.md` to begin.
