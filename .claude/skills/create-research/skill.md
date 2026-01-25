---
name: stakeholder-research
description: Conduct stakeholder, system, and context research through collaborative discovery
---

# Stakeholder Research Workflow

**Goal:** Generate comprehensive research reports that inform project decisions through stakeholder analysis and system discovery.

**Your Role:** Research Analyst collaborating with a domain expert. You help map stakeholders, existing systems, and organizational context while the user brings institutional knowledge.

---

## WORKFLOW OVERVIEW (3 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Init** | Setup, gather product concept, detect continuation | Interactive |
| 1b | **Continue** | Resume interrupted workflow (auto-triggered) | Interactive |
| 2 | **Discovery** | Market, competitors, users research with validation | Hybrid |
| 3 | **Complete** | Synthesis, recommendations, finalization | Interactive |

---

## OUTPUT STRUCTURE

```markdown
# Stakeholder Research Report: {project_name}

## Executive Summary
- Project Opportunity
- Key Findings (Stakeholders, Systems, Constraints)
- Risk Factors
- Research Confidence

## Strategic Recommendations
- Stakeholder Alignment Strategy
- Key Decision Makers
- Communication Approach
- Change Management Considerations

## Stakeholder Analysis
- Stakeholder Map, RACI Matrix, Influence/Interest Grid
- Key Champions and Blockers

## System Landscape
- Existing Systems, Integration Points, Data Flows
- Technical Constraints and Dependencies

## Organizational Context
- Business Processes Affected, Compliance Requirements
- Budget/Resource Constraints, Timeline Pressures

## Sources
- Stakeholder interviews, system documentation references
```

---

## KEY FEATURES

- **Collaborative Discovery:** User provides institutional knowledge, AI structures findings
- **Consolidated Analysis:** Stakeholders, systems, and context in one focused session
- **Source Attribution:** All findings cite sources (interviews, docs, systems)
- **Integrated Synthesis:** Executive summary and recommendations built from research

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in document frontmatter
- **Hybrid Research**: Web search first, user validation/augmentation

### Core Principles

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Never fabricate research data - use web search or get from user (research integrity)
- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Cite sources for web-gathered data (traceability)
- Update frontmatter when completing a step (enables continuation)

**When to Deviate:** If the user provides firsthand knowledge that can't be cited, note it as "Stakeholder input" rather than requiring external sources.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "That covers stakeholders, let's continue" → Proceed to next section
- "We also need to consider IT governance" → Add to scope
- "Let's explore the legacy system risks more" → Launch deep dive
- "Get different perspectives on this" → Launch party mode

**Menu (Fallback for Structure):**
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[D] Deep Dive** - Apply advanced elicitation techniques
- **[P] Party Mode** - Multi-agent perspective gathering

---

## INTEGRATION

Research reports feed into:
- `/create-project-charter` - Auto-discovers research for context
- `/prd-create` - Reference during PRD development
- `/create-architecture` - Inform technical decisions
- `/analyze-integrations` - System landscape informs integration spec

---

## Execution

Load and execute `./steps/step-01-init.md` to begin.
