---
name: prd-edit
description: Edit comprehensive PRDs with validation integration
---

# Edit PRD Workflow

**Goal:** Edit and improve PRDs through a streamlined 4-step workflow with validation integration.

**Your Role:** PRD Editor - an improvement specialist converting and refining PRDs to meet guidelines.

---

## WORKFLOW OVERVIEW (4 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Init** | Load PRD, detect format, get edit goals | Interactive |
| 2 | **Plan** | Deep review, build change plan | Interactive |
| 3 | **Edit** | Apply approved changes | Auto-proceed |
| 4 | **Complete** | Summary, offer validation or exit | Interactive |

**Workflow Modes:**
- **Structured PRD:** Direct to planning (steps 1→2→3→4)
- **Legacy PRD:** Conversion assessment, then planning

---

## EDIT CAPABILITIES

- **Content Updates** - Fix density, measurability, traceability issues
- **Format Conversion** - Convert FRs to Input/Rules/Output/Error format
- **Structure Changes** - Add missing sections, reorganize structure
- **Legacy Conversion** - Convert old PRDs to structured format
- **Validation Fixes** - Address issues from validation reports
- **Targeted Edits** - User-specified changes only

---

## TARGET FORMAT

Sections included based on project type. See `_prd-data/prd-purpose.md` for guidance.

| Section | Content | When to Include |
|---------|---------|-----------------|
| 1. Overview | Vision, Users, Success Metric, Scope | Always |
| 2. User Journeys | Step-by-step user flows | UI-based products |
| 3. Functional Requirements | Input/Rules/Output/Error/Log format | Always |
| 4. Non-Functional Requirements | Single-line with metric/target | Production systems |
| 5. Data Entities | Entity, Attributes, Related FRs | Persistent storage |
| 6. Technology Constraints | Decided vs Open | When constraints exist |
| 7. Quick Reference | FR summary with Priority/Depends | 5+ FRs |
| 8. Implementation Reference | Config schemas, output formats, error catalogs, algorithms | Complex systems with defined specs |

---

## FR FORMAT CONVERSION

**Old Format (Given/When/Then):**
```
**FR-001**: User can register
- Given: visitor on registration page
- When: submit valid email and password
- Then: account created
```

**New Format (Input/Rules/Output/Error/Log):**
```
**FR-AUTH-001**: User registers with email and password
- **Input:** email (valid format), password (8+ chars, 1 uppercase, 1 number)
- **Rules:** Email must be unique; hash password before storage
- **Output:** Account created, confirmation email sent within 30 seconds
- **Error:** Duplicate email → "Email already registered"
- **Log:** `[INFO] User registered: {email}` (optional - include when defined logging needed)
```

---

## VALIDATION INTEGRATION

Edit workflow integrates with validation:

- **Auto-detect** validation reports in PRD folder
- **Load findings** to prioritize edits
- **Post-edit validation** available at completion
- **Iterative cycle:** Edit → Validate → Edit → Validate

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in PRD frontmatter
- **Plan-Before-Edit**: Changes approved before execution

### Core Principles

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Get plan approval before editing (prevents unwanted changes)
- Make only approved changes (maintains trust)

**When to Deviate:** If the user wants to skip approval (e.g., minor wording changes) or adjust the workflow (e.g., validate before all edits), acknowledge the deviation and proceed.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "Looks good, proceed with the edits" → Execute approved changes
- "I want to add more changes" → Revise the plan
- "Let's validate what we have" → Run validation
- "Proceed to architecture" → Launch architecture workflow

**Menu (Fallback for Structure):**
If user prefers structured navigation:
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[V] Validate** - Run /prd-validate
- **[A] Architecture** - Proceed to /create-architecture (if ready)
- **[X] Exit** - Stop workflow

---

## Execution

**Prompt for PRD path:** "Which PRD would you like to edit? Please provide the path."

Then load and execute `./steps-edit-prd/step-01-init.md` to begin.
