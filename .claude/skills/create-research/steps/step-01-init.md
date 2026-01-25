---
name: 'step-01-init'
description: 'Initialize stakeholder research workflow - detect state, gather project concept, setup document'

# File references
nextStepFile: './step-02-discovery.md'
continueStepFile: './step-01b-continue.md'
outputFile: '{planning_artifacts}/stakeholder-research-{{project_name}}.md'
researchTemplate: '../stakeholder-research.template.md'
---

# Step 1: Init

**Progress: Step 1 of 3** - Next: Discovery

## STEP GOAL

Detect workflow state, gather project concept, and setup research document.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a Research Analyst - gather context, don't conduct research yet
- Focus on understanding what to research

## SEQUENCE (Follow Exactly)

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` array | → Load `{continueStepFile}` (auto-proceed) |
| File exists + NO `stepsCompleted` | → Safeguard Protocol |
| File not exists | → Fresh Setup |

### 2. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing research at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `research_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 3. Fresh Setup

#### A. Gather Project Concept

**Opening:**
"Welcome! I'm your Research Analyst, ready to help map stakeholders and systems.

Before I begin researching, I need to understand what we're investigating:

- What problem does this project solve?
- Who are the key stakeholders (sponsors, users, impacted teams)?
- What existing systems might be affected or integrated?
- Any known organizational constraints (compliance, budget, timeline)?"

#### B. Confirm Research Scope

After user provides concept, confirm understanding:

**Summary:**
"Let me confirm the research scope:

**Project Concept:** [summarize]
**Problem Space:** [identify]
**Target Category:** [identify]
**Known Stakeholders:** [list or 'To be discovered']
**Known Systems:** [list or 'To be discovered']

**Research Coverage:**
1. **Stakeholders** - Key players, influence, RACI
2. **Systems** - Existing landscape, integration points, dependencies
3. **Organization** - Processes, compliance, constraints

Any areas to prioritize or skip?"

#### C. Create Document

- Copy `{researchTemplate}` to `{outputFile}`
- Update frontmatter with project concept summary
- Initialize `stepsCompleted: []`

### 4. Report & Menu

**Report:**
- Document created at `{outputFile}`
- Research scope confirmed
- Ready to begin research discovery

**Menu:**

**[C] Continue** - Proceed to Discovery (Step 2)
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-init']`), then load and execute `{nextStepFile}`.

---

## SUCCESS CRITERIA

- Workflow state detected correctly
- Project concept gathered and confirmed
- Research document created with proper frontmatter
- User confirmed scope before proceeding
