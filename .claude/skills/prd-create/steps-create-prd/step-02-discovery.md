---
name: 'step-02-discovery'
description: 'Gather vision, users, success criteria, scope, user journeys, and capability-area preview'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-03-requirements.md'
outputFile: '{project_root}/docs/prd.md'
prdPurpose: '{skills_root}/_prd-data/prd-purpose.md'
---

# Step 2: Discovery

**Progress: Step 2 of 5** - Next: Requirements

## STEP GOAL

Extract essential context for AI implementation - vision, users, success metric, scope, user journeys, and preview capability areas for FR generation.

## EXECUTION RULES

- **Interactive step** - requires user collaboration
- You are a PRD Creator - a product-focused facilitator
- User is the domain expert - extract, don't lecture

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{prdPurpose}` to understand PRD quality standards. This is the single load point for prd-purpose across the entire workflow.

### 2. Discovery Conversation

Have a **single focused conversation** to gather all discovery information. Ask questions naturally, covering these areas:

#### A. Vision & Classification
- What problem does this product solve?
- Who is it for? (Primary user types)
- What makes this different from alternatives?
- Project type: Greenfield or Brownfield?
- Product category: CLI Tool / Web App / API Service / Desktop App / Mobile App / Library?
- Context: Enterprise / Consumer / Internal / B2B?

#### A2. Brownfield Context (If Brownfield)
If user indicates brownfield, gather additional context:
- What existing systems are being replaced or integrated with?
- Is there legacy data that needs to be migrated? (Volume, complexity)
- Are there existing users whose workflows will change?
- What technical constraints come from the legacy systems?
- What's the coexistence strategy? (Parallel run, phased cutover, big bang)

#### B. Success & Scope
- What's the ONE metric that defines success?
- What's in MVP scope? (Core capabilities)
- What's explicitly out of scope? (Deferred to later phases)

#### C. User Journeys
For each user type identified:
- What's their primary journey? (3-5 steps, not detailed narratives)
- What's their goal/outcome?

**Conversation Approach:**
- Use input documents to inform your questions (don't ask what's already documented)
- Keep it conversational, not interrogative
- Aim for 2-4 exchanges maximum

### 3. Update Document

After gathering information, update `{outputFile}` Section 1 (Overview) and Section 2 (User Journeys):

**Section 1: Overview**
```markdown
## 1. Overview

### Vision
{2-3 sentences from conversation}

### Classification
| Attribute | Value |
|-----------|-------|
| Project Type | {Greenfield / Brownfield} |
| Product Category | {category} |
| Primary Context | {context} |

### Brownfield Context (If Applicable)
| Existing System | Disposition | Integration Type |
|-----------------|-------------|------------------|
| {system} | Replace / Integrate / Migrate From | API / DB / File |

**Legacy Data:** {description of data to migrate, or "N/A"}
**Coexistence Strategy:** {Parallel Run / Phased Cutover / Big Bang / N/A}

### Users
| User Type | Primary Goal |
|-----------|--------------|
| {user_type} | {goal} |

### Key Success Metric
{The single metric}

### MVP Scope

**In Scope:**
- {capability 1}
- {capability 2}

**Out of Scope:**
- {deferred 1}
- {deferred 2}
```

**Section 2: User Journeys (Adapted by Product Category)**

Adapt Section 2 format to product category:

| Product Category | Section 2 Format |
|-----------------|------------------|
| Web App / Mobile / Desktop | **User Journeys** — 3-5 step flows per user type |
| API Service | **API Consumer Journeys** — request/response flows, briefer |
| CLI Tool | **Command Workflows** — command sequences with expected outputs |
| Library/SDK | **Integration Scenarios** — code usage patterns showing typical integration |
| Prototype/MVP | **User Journeys** — simplified, 2-3 steps |

```markdown
## 2. User Journeys

### {User Type}: {Journey Name}
1. {Step 1} → {Step 2} → {Step 3} → {Outcome}
```

### 4. Validation

Before proceeding, verify:

| Check | Requirement |
|-------|-------------|
| Vision | 2-3 sentences, clear value proposition |
| Users | At least 1 user type with goal |
| Success Metric | Single, measurable metric |
| Scope | At least 2 in-scope, 1 out-of-scope items |
| Journeys | At least 1 journey per user type, 3-5 steps each |

**If validation fails:** Ask targeted questions to fill gaps.

### 5. Capability Area Preview

Before presenting the menu, build a preview of capability areas that will drive FR generation in step 3:

**Map scope items + journey steps to capability areas:**

| Capability Area | Source (Scope Items / Journey Steps) |
|----------------|--------------------------------------|
| {descriptive area name} | {matching scope items and journey steps} |
| {descriptive area name} | {matching scope items and journey steps} |

Use natural, descriptive names for areas (e.g., "Authentication", "User Management", "Data Processing") — these become the `### Section Headers` in step 3.

**Present to user:**
"These are the capability areas I'll generate Functional Requirements for in the next step. Missing any areas?"

**After user confirms**, persist the areas as an HTML comment in `{outputFile}` after Section 2:
```markdown
<!-- CAPABILITY_AREAS: {comma-separated list of confirmed capability area names} -->
```
This enables step-03 to reference the approved list even across sessions, and avoids rebuilding the mapping from scratch.

### 6. Report & Menu

**Report:**
- Summary of what was captured
- Capability areas identified
- Any gaps or areas needing clarification

**Menu:**

**[C] Continue** - Proceed to Requirements (Step 3)
**[R] Revise** - Discuss changes to Overview, Journeys, or capability areas
**[P] Party Mode** - Multi-agent review of scope, journeys, and capability areas
**[D] Deep Dive** - Apply advanced elicitation on vision, users, or scope
**[X] Exit** - Save progress and stop

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-02-discovery'`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss specific changes, update document, return to menu.

**On [P]:** Invoke `/_party-mode` skill with topic "Scope and journey review for [project name]", content = Sections 1-2 + capability areas, focus_agents = `pm`, `architect`, `qa`. After discussion, apply insights and return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore a specific area more thoroughly (vision, users, success metric, scope, or journeys). After deep dive, update document with insights and return to menu.

**On [X]:** Update frontmatter (`stepsCompleted` add `'step-02-discovery'`), exit workflow.

---

## SUCCESS CRITERIA

- Vision and classification captured
- Users identified with goals
- Success metric defined (single, measurable)
- MVP scope defined (in/out)
- User journeys documented (3-5 steps each)
- Capability areas previewed and confirmed by user
- User confirmed discovery before proceeding
