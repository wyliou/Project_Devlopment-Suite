---
name: prd-create
description: Create comprehensive PRDs optimized for AI-powered development
---

# Create PRD Workflow

**Goal:** Create PRDs optimized for AI agent consumption through a streamlined 4-step workflow.

**Your Role:** PRD Creator - a product-focused facilitator collaborating with the user as domain expert.

---

## WORKFLOW OVERVIEW (4 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Init** | Setup, discover docs, detect continuation | Interactive |
| 1b | **Continue** | Resume interrupted workflow (auto-triggered) | Interactive |
| 2 | **Discovery** | Vision, users, success criteria, scope, journeys | Interactive |
| 3 | **Requirements** | FRs, NFRs, data entities, tech constraints, quick reference | Interactive |
| 4 | **Complete** | Validation summary and handoff | Interactive |

---

## OUTPUT STRUCTURE (7 Sections)

1. **Overview** - Vision, classification, users, success metric, scope
2. **User Journeys** - Brief 3-5 step journeys per user type
3. **Functional Requirements** - Input/Rules/Output/Error format
4. **Non-Functional Requirements** - Single-line format
5. **Data Entities** - Table with key attributes and FR mapping
6. **Technology Constraints** - Decided vs. Open decisions
7. **Quick Reference** - FR summary with priorities and dependencies

---

## KEY FEATURES

- **Consolidated Discovery:** Vision, users, scope, and journeys in one conversation
- **AI-Optimized FR Format:** Input/Rules/Output/Error structure for clear implementation
- **Single-Line NFRs:** Measurable metrics with target and condition
- **Integrated Validation:** Quality checks throughout, no separate optimization step
- **Quick Reference:** Summary table with priorities and dependencies

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in PRD frontmatter
- **Continuation Support**: Resume interrupted workflows via step-01b

### Core Principles

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update PRD frontmatter when completing a step (enables continuation)
- Follow step file instructions (they encode best practices)

**When to Deviate:** If the user has a valid reason to skip or reorder steps (e.g., section already complete from previous work), acknowledge the deviation and proceed.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "Looks good, let's continue" → Proceed to next step
- "I want to change the scope" → Make changes
- "Let's stop here for now" → Exit workflow

**Menu (Fallback for Structure):**
If user prefers structured navigation:
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[X] Exit** - Stop workflow

---

## Execution

Load and execute `./steps-create-prd/step-01-init.md` to begin.
