---
name: 'step-02-discovery'
description: 'Gather vision, classification, actors, success metrics, and scope'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-03-journeys.md'
prdPurpose: '{skills_root}/_prd-data/prd-purpose.md'
projectTypesCSV: '{skills_root}/_prd-data/project-types.csv'
---

# Step 2: Discovery

**Progress: Step 2 of 6** - Next: Journeys & Mapping

## STEP GOAL

Extract essential context for AI implementation — vision, classification, actors, success metrics, and scope. Journeys/workflows and capability areas are handled in step 3.

## EXECUTION RULES

- **Interactive step** — requires user collaboration
- You are a PRD Creator — a product-focused facilitator
- User is the domain expert — extract, don't lecture
- **One question at a time:** Ask a single focused question, wait for the answer, then ask the next. Never batch multiple questions into one message. This produces higher-quality, more detailed answers. Let the user's response guide your next question naturally.
- Adapt conversation depth to project complexity — simple projects need fewer exchanges, complex ones deserve thorough exploration
- **Compose-then-write principle:** Gather all discovery information before writing to the document. Do not write partial sections during conversation.

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{prdPurpose}` to understand PRD quality standards. This is the single load point for prd-purpose across the entire workflow.

Load `{projectTypesCSV}` for project-type-specific discovery questions. After product category is identified, use the matching CSV row's `key_questions` to ask category-specific questions.

### 2. Discovery Conversation

Gather all discovery information following the one-question-at-a-time principle. Cover these areas in natural order:

#### A. Vision & Classification
Topics to cover:
- What problem does this product solve?
- Who is it for? (Primary actor types — users, operators, admins, systems)
- What makes this different from alternatives?
- Project type: Greenfield or Brownfield?
- Product category? Options:
  - CLI Tool (`cli_tool`)
  - Web App (`web_app`)
  - API Service (`api_backend`)
  - Desktop App (`desktop_app`)
  - Mobile App (`mobile_app`)
  - Library / SDK (`developer_tool`)
  - Data Pipeline (`data_pipeline`)
  - ML Model/Service (`ml_service`)
  - Infrastructure/IaC (`infrastructure`)
  - Microservices System (`microservices`)
  - Plugin/Extension (`plugin_extension`)
  - Full Stack App (`full_stack`)
  - SaaS / B2B Platform (`saas_b2b`)
  - IoT / Embedded (`iot_embedded`)
  - Prototype / MVP (use closest type with simplified depth)
  - Other (describe and we'll adapt)
- Context: Enterprise / Consumer / Internal / B2B?

**After product category identified:** Load matching CSV row (use the `project_type` value in parentheses above) and use `key_questions` for category-specific discovery. Ask these one at a time too.

#### A2. Brownfield Context (If Brownfield)
If user indicates brownfield, gather additional context:
- What existing systems are being replaced or integrated with?
- Is there legacy data that needs to be migrated? (Volume, complexity)
- Are there existing users whose workflows will change?
- What technical constraints come from the legacy systems?
- What's the coexistence strategy? (Parallel run, phased cutover, big bang)

**Store brownfield context explicitly for step 3 (migration journeys, brownfield-specific capability areas) and step 4 (tech constraints from legacy systems).**

#### B. Success & Scope
Topics to cover:
- What are the key metrics that define success? (1-3 metrics; designate one as primary)
- What's in MVP scope? (Core capabilities)
- What's explicitly out of scope? (Deferred to later phases)

**Conversation Approach:**
- **Smart defaults from input documents:** Before asking each question, check loaded input documents for relevant information. If found, propose it: "Based on your brief, the problem is: {extracted}. Correct or would you refine?" This accelerates discovery for well-documented projects.
- Keep it conversational, not interrogative
- If the user provides a rich answer that covers multiple topics, acknowledge what was covered and move to the next uncovered topic

### 3. Update Document

After gathering information, read `outputPath` from the PRD document's frontmatter to determine the target file. Update Section 1 (Overview) only:

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

### Actors
| Actor Type | Primary Goal |
|------------|--------------|
| {actor_type} | {goal} |

### Success Metrics
| Metric | Target | Primary |
|--------|--------|---------|
| {metric_1} | {quantifiable target} | Yes |
| {metric_2} | {quantifiable target} | No |

### MVP Scope

**In Scope:**
- {capability 1}
- {capability 2}

**Out of Scope:**
- {deferred 1}
- {deferred 2}
```

### 4. Validation

Before proceeding, verify:

| Check | Requirement |
|-------|-------------|
| Vision | 2-3 sentences, clear value proposition |
| Actors | At least 1 actor type with goal |
| Success Metrics | 1-3 metrics with primary designation |
| Scope | At least 2 in-scope, 1 out-of-scope items |

**If validation fails:** Ask targeted questions to fill gaps.

### 5. Report & Menu

**Report:**
- Summary of what was captured
- Any gaps or areas needing clarification

**Menu:**

**[C] Continue** - Proceed to Journeys & Mapping (Step 3)
**[R] Revise** - Discuss changes to Overview
**[P] Party Mode** - Multi-agent review of vision, actors, and scope
**[D] Deep Dive** - Apply advanced elicitation on vision, actors, or scope
**[X] Exit** - Save progress and stop

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-02-discovery'`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss specific changes, update document, return to menu.

**On [P]:** Invoke `/_party-mode` skill with topic "Vision and scope review for [project name]", content = Section 1, focus_agents = `pm`, `architect`, `qa`. After discussion, apply insights and return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore a specific area more thoroughly (vision, actors, success metrics, or scope). After deep dive, update document with insights and return to menu.

**On [X]:** Exit workflow. Do NOT mark this step as complete — document changes are preserved but the step must be re-run on resume to verify completeness.

---

## SUCCESS CRITERIA

- Vision and classification captured
- Actors identified with goals
- Success metrics defined (1-3 with primary designation)
- MVP scope defined (in/out)
- CSV-specific questions asked for identified product category
- Brownfield context flagged for downstream steps (if applicable)
- User confirmed discovery before proceeding
