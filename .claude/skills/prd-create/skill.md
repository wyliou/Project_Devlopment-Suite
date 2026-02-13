---
name: prd-create
description: Create comprehensive PRDs optimized for AI-powered development
---

# Create PRD Workflow

**Goal:** Create PRDs optimized for AI agent consumption through a streamlined 5-step workflow with dedicated FR generation and architecture-readiness validation.

**Your Role:** PRD Creator - a product-focused facilitator collaborating with the user as domain expert.

---

## WORKFLOW OVERVIEW (5 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Init** | Setup, discover docs, detect continuation (inline) | Interactive |
| 2 | **Discovery** | Vision, users, scope, journeys, capability-area preview | Interactive |
| 3 | **Requirements** | Functional Requirements with systematic capability mapping | Interactive |
| 4 | **Specifications** | NFRs, Data Entities, Tech Constraints, Section 8 | Interactive |
| 5 | **Complete** | Quick Reference, architecture-readiness check, validation, handoff | Interactive |

---

## OUTPUT STRUCTURE (8 Sections)

1. **Overview** - Vision, classification, users, success metric, scope
2. **User Journeys** - Brief 3-5 step journeys per user type
3. **Functional Requirements** - Input/Rules/Output/Error format
4. **Non-Functional Requirements** - Single-line format
5. **Data Entities** - Table with key attributes and FR mapping
6. **Technology Constraints** - Decided vs. Open decisions
7. **Quick Reference** - FR summary with dependencies
8. **Implementation Reference** (Optional) - Config schemas, output formats, error catalogs, algorithms, examples

---

## KEY FEATURES

- **Dedicated FR Step:** Step 3 focuses exclusively on Functional Requirements with systematic capability mapping
- **Capability Mapping:** Coverage matrix ensures every scope item and journey maps to FRs before generation
- **Architecture-Readiness Checkpoint:** Step 5 validates PRD has everything create-architecture and build-from-prd need
- **Separated Concerns:** FRs (step 3) isolated from derived specifications (step 4)
- **Structured FR Output:** Input/Rules/Output/Error format optimized for downstream architecture and build pipeline extraction
- **Inline Continuation:** Resume interrupted workflows without separate continuation file

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in PRD frontmatter
- **Inline Continuation**: Resume interrupted workflows detected in step-01

### Execution Rules

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
