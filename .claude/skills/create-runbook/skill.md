---
name: create-runbook
description: Create operational runbook for support team handoff
---

# Create Runbook Workflow

**Goal:** Create operational documentation for support teams to deploy, monitor, and troubleshoot the system.

**Your Role:** Operations specialist documenting procedures for support handoff.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Discovery** | Gather operational details, procedures, contacts |
| 2 | **Generate** | Create runbook document |

---

## OUTPUT FORMAT

```markdown
# Runbook: {system_name}

## Quick Reference
- Support Tier: L1 / L2 / L3
- On-call: {contact}
- Escalation: {path}

## System Overview
- Purpose, architecture diagram, dependencies

## Health Checks
- How to verify system is healthy
- Key metrics and thresholds

## Common Procedures
- Start/stop/restart
- Log access
- Config changes

## Troubleshooting
- Common issues and resolutions
- Decision trees

## Alerts & Monitoring
- What alerts exist
- Response procedures

## Contacts & Escalation
- Who to call when
```

---

## Execution

Load and execute `./steps/step-01-discovery.md` to begin.
