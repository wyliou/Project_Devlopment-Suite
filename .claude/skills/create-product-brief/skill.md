---
name: create-project-charter
description: Create project charters optimized for PRD generation
---

# Create Project Charter Workflow

**Goal:** Create concise project charters that feed directly into the prd-create workflow.

**Your Role:** Project-focused facilitator collaborating with an expert peer.

---

## WORKFLOW OVERVIEW (4 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Init** | Setup, discover docs, detect continuation |
| 1b | **Continue** | Resume interrupted workflow (auto-triggered) |
| 2 | **Discovery** | Vision, problem, solution, users |
| 3 | **Scope** | Success metric, MVP scope, constraints |
| 4 | **Complete** | Validation and handoff to PRD |

---

## OUTPUT FORMAT (Optimized for prd-create)

The project charter provides input for PRD generation:

```markdown
# Project Charter: {project_name}

## 1. Vision
### Problem Statement
{2-3 sentences describing the core problem}

### Solution Overview
{2-3 sentences describing how we solve it}

### Key Differentiators
- {differentiator 1}
- {differentiator 2}

## 2. Users
| User Type | Primary Goal | Pain Points |
|-----------|--------------|-------------|
| {type} | {goal} | {pain} |

## 3. Success
### Key Success Metric
{THE ONE metric that defines success}

### Supporting Indicators
- {indicator 1}
- {indicator 2}

## 4. MVP Scope
**In Scope:**
- {core capability 1}
- {core capability 2}

**Out of Scope:**
- {deferred 1}
- {deferred 2}

## 5. Context
### Technology Preferences
{Any decided tech or "No preferences"}

### Timeline
{Target timeline or "Flexible"}

### Domain Notes
{Relevant domain context}
```

---

## HOW BRIEF FEEDS PRD

| Brief Section | PRD Section |
|---------------|-------------|
| Vision | PRD 1. Overview → Vision |
| Users table | PRD 1. Overview → Users table |
| Key Success Metric | PRD 1. Overview → Key Success Metric |
| MVP Scope | PRD 1. Overview → MVP Scope |
| Technology Preferences | PRD 6. Technology Constraints |

---

## CONVERSATION APPROACH

- **Extract, don't lecture** - user is the domain expert
- **Ask focused questions** - 2-3 at a time, not lengthy lists
- **Be concise** - brief is meant to be brief
- **Challenge assumptions** - push for specificity
- **Aim for 2-4 exchanges per step** - not exhaustive interviews

---

## Execution

Load and execute `./steps/step-01-init.md` to begin.
