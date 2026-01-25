---
name: 'step-02-discovery'
description: 'Gather vision, users, success criteria, scope, and user journeys'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-03-requirements.md'
outputFile: '{project_root}/docs/prd.md'
prdPurpose: '{skills_root}/_prd-data/prd-purpose.md'
---

# Step 2: Discovery

**Progress: Step 2 of 4** - Next: Requirements

## STEP GOAL

Extract essential context for AI implementation - vision, users, success metric, scope, and user journeys.

## EXECUTION RULES

- **Interactive step** - requires user collaboration
- You are a PRD Creator - a product-focused facilitator
- User is the domain expert - extract, don't lecture

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{prdPurpose}` to understand PRD quality standards.

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

**Section 2: User Journeys**
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

### 5. Report & Menu

**Report:**
- Summary of what was captured
- Any gaps or areas needing clarification

**Menu:**

**[C] Continue** - Proceed to Requirements (Step 3)
**[R] Revise** - Discuss changes to Overview or Journeys
**[D] Deep Dive** - Apply advanced elicitation on vision, users, or scope

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-02-discovery'`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss specific changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore a specific area more thoroughly (vision, users, success metric, scope, or journeys). After deep dive, update document with insights and return to menu.

---

## SUCCESS CRITERIA

- Vision and classification captured
- Users identified with goals
- Success metric defined (single, measurable)
- MVP scope defined (in/out)
- User journeys documented (3-5 steps each)
- User confirmed discovery before proceeding
