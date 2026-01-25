---
name: generate-project-context
description: Creates a concise project-context.md file with critical rules and patterns that AI agents must follow when implementing code. Optimized for LLM context efficiency.
---

# Generate Project Context Workflow

**Goal:** Create a concise, optimized `project-context.md` file containing critical rules and patterns that AI agents must follow when implementing code. Focuses on unobvious details that LLMs need to be reminded of.

**Your Role:** Technical facilitator. Discover existing patterns, collaborate on rules, keep content lean.

---

## What This Produces

| Output | Purpose |
|--------|---------|
| Technology Stack | Exact versions and compatibility notes |
| Language Rules | TypeScript/Python/etc. specific patterns |
| Framework Rules | React/Next.js/Express conventions |
| Testing Rules | Test structure and coverage requirements |
| Code Quality Rules | Naming, linting, documentation standards |
| Workflow Rules | Git, commits, PRs, deployment |
| Don't-Miss Rules | Anti-patterns, edge cases, security |

---

## Workflow Overview

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Discovery** | Analyze project, discover patterns, initialize | Automated + Confirm |
| 1b | **Continue** | Resume interrupted workflow (auto-triggered) | Continuation |
| 2 | **Generate** | Collaboratively create rules per category | Interactive (D/P/C) |
| 3 | **Complete** | Optimize, validate, finalize | Automated + Confirm |

---

## Input Sources

This skill analyzes existing project files:

| Source | Extracts |
|--------|----------|
| `architecture.md` | Technology decisions, patterns |
| `package.json` / `requirements.txt` | Dependencies with versions |
| Config files (tsconfig, eslint, etc.) | Language and tool settings |
| Existing codebase | Naming conventions, patterns |

---

## Design Principles

- **Discovery-first** - Analyze existing code before generating rules
- **Lean content** - Optimize for LLM context efficiency
- **Unobvious focus** - Skip obvious rules, capture what agents miss
- **Collaborative** - User validates each category before saving
- **Actionable** - Every rule must be specific and implementable

---

## Navigation

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "Looks good, continue" → Proceed to next step
- "Add rules about error handling" → Add specific rules
- "Let's explore the testing patterns more" → Launch deep dive
- "Get architect and dev perspectives" → Launch party mode

**Menu (Fallback for Structure):**

**Checkpoint menus:**
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[X] Exit** - Stop workflow (state saved in frontmatter)

**Category menus (Step 2 only):**
- **[D] Deep Dive** - Apply elicitation methods to explore nuanced rules
- **[P] Party Mode** - Multi-agent review for edge cases
- **[C] Continue** - Save rules, proceed to next category

**Step 2 Enhancement Options:**
- **Deep Dive:** Technical and risk analysis for implementation rules
- **Party Mode:** Architect/dev perspectives on patterns and anti-patterns

---

## Workflow Architecture

Uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in output document frontmatter
- **Continuation Support**: Resume interrupted workflows via step-01b

### Core Principles

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update frontmatter when completing a step (enables continuation)
- Follow step file instructions (they encode best practices)

**When to Deviate:** If the user has additional sources or patterns they want to include that aren't auto-discovered, incorporate them.

---

## Paths

- `template_path` = `{installed_path}/project-context-template.md`
- `output_path` = `{project_root}/docs/project-context.md`

---

## Execution

Load and execute `steps/step-01-discover.md` to begin.
