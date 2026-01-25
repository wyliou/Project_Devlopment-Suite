---
name: create-architecture
description: Collaborative architectural decision facilitation for AI-agent consistency. Produces a decision-focused architecture document optimized for preventing agent conflicts.
---

# Architecture Workflow

**Goal:** Create an architecture document that gives AI agents everything they need to build the application. Together with the PRD, these two documents provide complete implementation guidance.

**Your Role:** Architectural facilitator. Derive decisions from PRD, only ask when truly ambiguous.

---

## What This Produces (that PRD doesn't provide)

| Output | Purpose |
|--------|---------|
| Technology Stack | Specific choices with versions |
| Project Structure | Exact directory layout |
| Coding Patterns | Naming, error format, conventions |
| Module Boundaries | What code goes where |
| API Contracts | Concrete specs from FRs |
| Database Schema | Actual definitions from Data Entities |
| Legacy Integration | (Brownfield) Integration points, adapters, constraints |

---

## Workflow Overview

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Discovery** | Find PRD, extract constraints, select tech stack | Derive + Confirm |
| 1b | **Continue** | Resume interrupted workflow (auto-triggered) | Continuation |
| 2 | **Structure** | Directory tree, coding patterns, module boundaries | Derive + Confirm |
| 3 | **Specifications** | API contracts, database schema, validate, finalize | Generate |

---

## PRD Integration

**Required Input:** PRD document (7 sections)

| PRD Section | Architecture Uses For |
|-------------|----------------------|
| 1. Overview | Project context, type detection (Greenfield/Brownfield) |
| 2. User Journeys | Flow understanding (read-only) |
| 3. Functional Requirements | API Contracts (Input→Request, Output→Response, Error→Handling) |
| 4. Non-Functional Requirements | Architecture decisions (scale, security, performance) |
| 5. Data Entities | Database Schema generation |
| 6. Technology Constraints | Stack selection (Decided = locked, Open = select) |
| 7. Quick Reference | Priorities and dependencies |

**Optional Input:** Project Charter with Brownfield Context (Section 7)

| Charter Section | Architecture Uses For |
|-----------------|----------------------|
| Existing Systems | Integration points, API compatibility |
| Legacy Data | Migration strategy, schema mapping |
| Technical Constraints | Stack limitations from legacy |

---

## Design Principles

- **Greenfield and Brownfield** - supports both new builds and legacy integration
- **Derive, don't ask** - PRD provides context, only ask if truly ambiguous
- **No menus during generation** - flow through naturally, confirm at checkpoints
- **Lean output** - only what AI needs to build
- **PRD as source of truth** - reference FRs, don't duplicate content
- **Brownfield-aware** - when integrating with legacy, document constraints and integration points

---

## Navigation

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "That stack looks good, continue" → Proceed to next step
- "I'd prefer using PostgreSQL instead" → Revise technology selection
- "Let's get architect and dev perspectives" → Launch party mode
- "Analyze the trade-offs more deeply" → Launch deep dive

**Menu (Fallback for Structure):**
Checkpoints use consistent menu patterns:

- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[P] Party Mode** - Multi-agent discussion (Step 1 only)
- **[D] Deep Dive** - Advanced elicitation methods (Step 1 only)
- **[X] Exit** - Stop workflow (state saved in frontmatter)

**Step 1 Enhancement Options:**
- **Party Mode:** Get perspectives from architect and dev agents on tech stack decisions
- **Deep Dive:** Apply technical, risk, and competitive analysis methods to validate choices

---

## Workflow Architecture

Uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in architecture document frontmatter
- **Continuation Support**: Resume interrupted workflows via step-01b

### Core Principles

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update architecture frontmatter when completing a step (enables continuation)
- Follow step file instructions (they encode best practices)

**When to Deviate:** If the user has specific preferences for structure or patterns that differ from defaults, acknowledge the deviation and proceed.

---

## Paths

- `template_path` = `{installed_path}/architecture-decision-template.md`
- `data_files_path` = `{installed_path}/data/`

---

## Execution

Load and execute `steps/step-01-discovery.md` to begin.
