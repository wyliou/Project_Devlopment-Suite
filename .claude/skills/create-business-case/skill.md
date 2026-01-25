---
name: create-business-case
description: Create business case with ROI and budget justification for project approval
---

# Create Business Case Workflow

**Goal:** Create a concise business case document for project approval and budget justification.

**Your Role:** Business analyst helping articulate project value and costs.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Discovery** | Gather problem, solution, benefits, costs |
| 2 | **Generate** | Create business case document |

---

## OUTPUT FORMAT

```markdown
# Business Case: {project_name}

**Date:** {date}
**Sponsor:** {sponsor}
**Business Unit:** {department}

---

## Problem Statement
{2-3 sentences on business problem and its impact}

## Proposed Solution
{Brief description of what will be built}

## Benefits

| Benefit | Metric | Current | Target |
|---------|--------|---------|--------|
| {benefit} | {how measured} | {baseline} | {expected} |

## Costs

| Item | One-time | Recurring (Annual) |
|------|----------|-------------------|
| Development | {cost} | - |
| Infrastructure | {cost} | {cost} |
| Licenses | {cost} | {cost} |
| Support | - | {cost} |
| **Total** | {sum} | {sum} |

## ROI Summary
- **Total Investment:** {one-time + year 1 recurring}
- **Annual Value:** {quantified benefit}
- **Payback Period:** {months}
- **3-Year ROI:** {percentage}

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {risk} | Low/Med/High | Low/Med/High | {mitigation} |

## Recommendation
{Go / No-Go / Conditional with rationale}

## Approvals

| Role | Name | Date |
|------|------|------|
| Sponsor | | |
| Finance | | |
| IT | | |
```

---

## CONVERSATION APPROACH

- **Focus on value** - quantify benefits where possible
- **Be realistic on costs** - include hidden costs (training, support)
- **Acknowledge risks** - shows thorough analysis
- **Keep it brief** - 1-2 pages maximum

---

## Execution

Load and execute `./steps/step-01-discovery.md` to begin.
