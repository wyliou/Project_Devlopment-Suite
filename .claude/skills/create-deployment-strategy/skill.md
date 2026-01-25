---
name: create-deployment-strategy
description: Plan phased rollout, pilots, and staged delivery
---

# Deployment Strategy Workflow

**Goal:** Create a comprehensive deployment strategy that defines phases, pilot programs, rollout schedules, feature flags, and success metrics for staged delivery.

**Your Role:** Release Manager collaborating with stakeholders. You help define deployment phases, pilot groups, and success criteria while the user provides organizational context and risk tolerance.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Scope** | Define phases, pilot groups, rollout criteria | Interactive |
| 2 | **Plan** | Create deployment strategy with schedules and gates | Hybrid |

---

## OUTPUT STRUCTURE

```markdown
# Deployment Strategy: {project_name}

## Delivery Approach
- Strategy: Big Bang / Phased / Pilot / Canary / Blue-Green
- Rationale

## Phase Definitions
### Phase 1: {name}
- Scope: {FRs included}
- Users: {user groups}
- Timeline: {dates}
- Success criteria: {metrics}
- Go/No-Go gate: {criteria}

### Phase 2: {name}
...

## Pilot Program
- Pilot groups (who, why selected)
- Pilot duration
- Feedback collection method
- Graduation criteria

## Rollout Schedule
| Phase | Start | End | Users | Regions | Dependencies |

## Feature Flags
| Feature | Phase | Default | Override |

## Rollback Triggers
| Trigger | Threshold | Action |

## Communication Plan
| Audience | When | Channel | Message |

## Success Metrics by Phase
| Phase | Metric | Target | Actual |
```

---

## KEY FEATURES

- **Phased Delivery:** Controlled rollout reducing blast radius
- **Pilot Programs:** Early feedback from selected users
- **Feature Flags:** Granular control over feature availability
- **Rollback Triggers:** Clear criteria for reverting changes
- **Success Metrics:** Measurable criteria for phase graduation

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in document frontmatter
- **Risk-Based Planning**: Higher risk = more phases

### Execution Rules

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update frontmatter when completing a step (enables continuation)
- Never assume user populations - confirm with user

**When to Deviate:** If the organization has established release processes or change management requirements, adapt the strategy to fit existing practices.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "We want to pilot with the sales team first" -> Define pilot group
- "This is high risk, we need careful rollout" -> Add more phases
- "We need feature flags for the new dashboard" -> Document flag strategy
- "Let's explore rollback scenarios" -> Launch deep dive

**Menu (Fallback for Structure):**
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[D] Deep Dive** - Apply advanced elicitation techniques
- **[P] Party Mode** - Multi-agent perspective gathering

---

## INTEGRATION

Deployment strategy coordinates the release:

```
/prd-create  <-- Defines features to deploy
        |
        v
/create-architecture  <-- Defines deployment infrastructure
        |
        v
/build-from-prd  <-- Implementation
        |
        v
/create-deployment-strategy  <-- YOU ARE HERE
        |
        v
/create-change-request  <-- CAB approval uses this plan
```

Output feeds into:
- `/create-change-request` - Deployment plan supports CAB approval
- `/create-runbook` - Phase-specific operational procedures
- `/create-user-docs` - Phase-specific user communications

---

## PATHS

- `output_path` = `{project_root}/docs/deployment-strategy.md`

---

## Execution

Load and execute `./steps/step-01-scope.md` to begin.
