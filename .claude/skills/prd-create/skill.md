---
name: prd-create
description: Create comprehensive PRDs optimized for AI-powered development
---

# Create PRD Workflow

**Goal:** Create PRDs optimized for AI agent consumption through a streamlined 6-step workflow with dedicated FR generation, priority system, and readiness gate validation.

**Your Role:** PRD Creator - a product-focused facilitator collaborating with the user as domain expert.

---

## WORKFLOW OVERVIEW (6 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Init** | Setup, discover docs, detect continuation, determine output path | Interactive |
| 2 | **Discovery** | Vision, classification, actors, success metrics, scope | Interactive |
| 3 | **Journeys & Mapping** | Journeys/workflows, capability mapping with priority | Interactive |
| 4 | **Requirements** | FR generation, completeness verification, FR deepening | Interactive |
| 5 | **Specifications** | Tech Constraints, NFRs, Data Entities, Section 8 | Interactive |
| 6 | **Complete** | Quick Reference with priority, readiness gate, handoff | Interactive |

---

## OUTPUT STRUCTURE (8 Sections)

1. **Overview** - Vision, classification, actors, success metrics, scope
2. **Journeys/Workflows** - Actor flows adapted by product category (journeys, data workflows, command workflows, etc.)
3. **Functional Requirements** - Input/Rules/Output/Error format with prioritized capability area headers [Must/Should/Could]
4. **Non-Functional Requirements** - Single-line format
5. **Data Entities** - Table with key attributes and FR mapping
6. **Technology Constraints** - Decided vs. Open decisions
7. **Quick Reference** - FR summary with Capability Area, Priority, and Depends columns
8. **Implementation Reference** (Optional) - Config schemas, output formats, error catalogs, algorithms, plus extensible project-specific sections

---

## KEY FEATURES

- **One Question at a Time:** Ask a single focused question, wait for the answer, then ask the next. Never batch multiple questions into one message. This keeps the conversation manageable and produces higher-quality answers. The only exception is the step-end menu (which presents navigation options, not discovery questions).
- **Flexible Output Path:** User chooses where to save PRD; multi-PRD discovery finds existing PRDs
- **Priority System:** Must/Should/Could tags on capability areas inform build batch ordering
- **Compose-Then-Write:** Gather information completely before writing to document — no partial sections
- **CSV Integration:** Project-type-specific discovery questions from `project-types.csv`
- **Dedicated FR Step:** Step 4 focuses exclusively on FR generation and deepening
- **Capability Mapping:** Step 3 builds coverage matrix ensuring every scope item and journey maps to capability areas before FR generation
- **Readiness Gate:** Step 6 validates structural completeness and cross-reference integrity; deep quality validation is /prd-validate's domain
- **Separated Concerns:** Journeys/mapping (step 3), FRs (step 4), and derived specifications (step 5) are each isolated
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
