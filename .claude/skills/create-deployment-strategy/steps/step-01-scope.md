---
name: 'step-01-scope'
description: 'Define phases, pilot groups, and rollout criteria'

# File references
nextStepFile: './step-02-plan.md'
outputFile: '{project_root}/docs/deployment-strategy.md'
---

# Step 1: Scope

**Progress: Step 1 of 2** - Next: Plan

## STEP GOAL

Define deployment scope including delivery approach, phase definitions, pilot groups, and success criteria for each phase.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a Release Manager - gather requirements, don't create schedule yet
- Focus on understanding risk tolerance and rollout constraints

## SEQUENCE (Follow Exactly)

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` array | -> Resume workflow |
| File exists + NO `stepsCompleted` | -> Safeguard Protocol |
| File not exists | -> Fresh Setup |

### 2. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing deployment strategy at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `deployment-strategy_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 3. Fresh Setup

#### A. Gather Deployment Context

**Opening:**
"Welcome! I'm your Release Manager, ready to help plan your deployment strategy.

Let's start by understanding your deployment context:

**Project Scope:**
- What is being deployed (new application, major update, migration)?
- How many features/functional requirements in this release?
- What's the overall project risk level (high/medium/low)?

**User Base:**
- How many total users will be affected?
- Are there distinct user groups (internal/external, regions, departments)?
- Any users who should get early access (power users, champions)?

**Organizational Constraints:**
- Any blackout periods (fiscal close, holidays, peak seasons)?
- Change approval board (CAB) requirements?
- Existing release cadence or deployment windows?"

#### B. Gather Risk and Strategy Preferences

After initial responses, probe for strategy:

"Now let's discuss your deployment strategy preferences:

**Strategy Options:**

| Strategy | Description | Best For |
|----------|-------------|----------|
| Big Bang | All users at once | Low risk, small user base |
| Phased | Groups of users over time | Medium risk, manageable groups |
| Pilot | Small test group first | High risk, need validation |
| Canary | Tiny % first, gradually increase | Technical risk, need monitoring |
| Blue-Green | Parallel environments, instant switch | Zero downtime required |

**Questions:**
- Which strategy resonates with your risk tolerance?
- Can you run old and new systems in parallel?
- How important is zero-downtime deployment?
- Do you have infrastructure for blue-green or canary?"

#### C. Gather Phase and Pilot Details

"Let's define phases and pilots:

**If Phased/Pilot:**
- What user groups would make good pilot candidates?
- Why would they be good early adopters (tech-savvy, low risk, champions)?
- How long should a pilot run before broader rollout?
- What feedback would you need before expanding?

**Feature Considerations:**
- Should all features deploy together, or can some be held back?
- Any features that are higher risk and need controlled rollout?
- Dependencies between features?"

#### D. Gather Success Criteria

"Let's define success criteria:

**Metrics to Track:**
- What technical metrics matter (uptime, response time, error rate)?
- What business metrics matter (adoption, transactions, user satisfaction)?
- What thresholds would indicate problems?

**Go/No-Go Criteria:**
- What would cause you to pause the rollout?
- Who has authority to make go/no-go decisions?
- What's the minimum success criteria for each phase?"

#### E. Confirm Deployment Scope

After user provides context, confirm understanding:

**Summary:**
"Let me confirm the deployment scope:

**Deployment Overview:**
- Project: {project_name}
- Risk Level: {High/Medium/Low}
- Strategy: {Chosen strategy}
- Total Users: {Number}

**Phase Structure:**
| Phase | Name | Users | Purpose |
|-------|------|-------|---------|
| 1 | Pilot | {Group} | Validate in production |
| 2 | Early Adopters | {Group} | Gather feedback |
| 3 | General Availability | All | Full rollout |

**Pilot Program:**
- Pilot group: {Who and why}
- Duration: {Time}
- Success criteria: {Criteria}

**Key Constraints:**
- Blackout periods: {Dates}
- CAB requirements: {Yes/No}

Anything to add or adjust?"

#### F. Create Document

Create `{outputFile}` with initial structure:

```markdown
---
stepsCompleted: []
strategy: {chosen}
riskLevel: {level}
totalUsers: {number}
---

# Deployment Strategy: {project_name}

## Document Control
- **Status:** Draft
- **Created:** {date}
- **Last Updated:** {date}

## Delivery Approach

### Strategy
- **Selected:** {Big Bang/Phased/Pilot/Canary/Blue-Green}
- **Rationale:** {Why this strategy fits}

### Risk Assessment
- **Risk Level:** {High/Medium/Low}
- **Key Risks:** {List}
- **Mitigations:** {List}

### Constraints
- **Blackout Periods:** {List}
- **CAB Requirements:** {Details}
- **Parallel Operation:** {Yes/No}

---
*Sections below to be completed in Step 2: Plan*
---

## Phase Definitions
*Pending*

## Pilot Program
*Pending*

## Rollout Schedule
*Pending*

## Feature Flags
*Pending*

## Rollback Triggers
*Pending*

## Communication Plan
*Pending*

## Success Metrics by Phase
*Pending*
```

### 4. Report & Menu

**Report:**
- Document created at `{outputFile}`
- Deployment strategy selected
- Phase structure outlined
- Ready to create detailed plan

**Menu:**

**[C] Continue** - Proceed to Plan (Step 2)
**[R] Revise** - Discuss changes to scope
**[D] Deep Dive** - Explore risk assessment deeper
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-scope']`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on deployment risks or strategy comparison. Update document, return to menu.

---

## SUCCESS CRITERIA

- Deployment strategy selected with rationale
- Risk level assessed
- Phase structure defined
- Pilot group identified (if applicable)
- Success criteria outlined
- Constraints documented
- Document created with proper frontmatter
- User confirmed scope before proceeding
