---
name: prd-create
description: Create comprehensive PRDs optimized for AI-powered development
---

# Create PRD Workflow

**Goal:** Create PRDs optimized for AI agent consumption through a streamlined 6-step workflow with dedicated FR generation, priority system, and readiness gate validation.

**Output:** A structured PRD document (up to 8 sections: Overview, Journeys, Functional Requirements, NFRs, Data Entities, Tech Constraints, Quick Reference, Implementation Reference) saved to the user's chosen path.

**Your Role:** PRD Creator - a product-focused facilitator collaborating with the user as domain expert.

---

## WORKFLOW OVERVIEW (6 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Init** | Discover existing PRDs, determine output path, detect continuation |
| 2 | **Discovery** | Vision, classification, actors, success metrics, scope |
| 3 | **Journeys & Mapping** | Journeys/workflows, capability mapping with priority |
| 4 | **Requirements** | FR generation, completeness verification, FR deepening |
| 5 | **Specifications** | Tech Constraints, NFRs, Data Entities, Section 8 |
| 6 | **Complete** | Quick Reference with priority, readiness gate, handoff |

---

## KEY RULES

- **One Question at a Time:** Ask a single focused question, wait for the answer, then ask the next. Never batch multiple questions. The only exception is the step-end menu.
- **Smart Defaults:** Before asking a question, check loaded input documents and prior context for relevant information. If found, propose it and ask the user to confirm or refine — don't make the user repeat what's already known.
- **Compose-Then-Write:** Gather all information for a section completely before writing it to the document. Never leave a section in a partial state. Different sections can be written at different times.
- **Priority System:** Must/Should/Could tags on capability areas inform build batch ordering.
- **Readiness Gate:** Step 6 validates structural completeness only; deep quality validation is /prd-validate's domain.

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

**Always Available (any step):**
- **[P] Party Mode** — Multi-agent review of current step's output via `/_party-mode`
- **[D] Deep Dive** — Advanced elicitation on any area via `/_deep-dive`

**Deviation:** If the user has a valid reason to skip or reorder steps, acknowledge and proceed.

---

## Execution

Load and execute `./steps-create-prd/step-01-init.md` to begin.
