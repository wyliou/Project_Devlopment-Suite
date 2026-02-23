# Project Development Suite

A collection of Claude Code skills that guide software projects from idea through deployment. Each skill is invoked as a slash command (e.g., `/prd-create`) and walks you through a structured, collaborative workflow.

Skills are listed below in the order you would use them across a project lifecycle. Not every project needs every skill -- pick the ones that fit.

---

## Phase 1 -- Discovery

Understand the problem space before writing requirements.

| # | Command | What it does |
|---|---------|--------------|
| 1a | `/create-research` | Conduct stakeholder, system, and context research. Maps stakeholders, existing systems, and organizational constraints. |
| 1b | `/analyze-integrations` | Map connections to existing enterprise systems. Documents system landscape, integration points, data flows, and dependencies. |
| 1c | `/create-product-brief` | Create a project charter optimized for PRD generation. Produces vision, users, success metrics, and MVP scope. |
| 1d | `/create-business-case` | Create a business case with ROI and budget justification for project approval. |

> **Start here.** `/create-research` for brownfield projects with unclear requirements. `/create-product-brief` when you already know the vision. `/create-business-case` when you need funding approval first.

---

## Phase 2 -- Requirements

Turn discovery outputs into a structured PRD.

| # | Command | What it does |
|---|---------|--------------|
| 2a | `/prd-create` | Create a comprehensive PRD optimized for AI-powered development. 6-step workflow with structured functional requirements (Input/Rules/Output/Error) and a readiness gate. |
| 2b | `/prd-validate` | Validate a PRD against PRD Guidelines. Checks structure, format, quality, and compliance; produces quality ratings. |
| 2c | `/prd-edit` | Edit an existing PRD with validation integration. Also converts legacy PRDs to the structured format. |

> **Flow:** `/prd-create` -> `/prd-validate` -> fix issues with `/prd-edit` -> re-validate until ready.

---

## Phase 3 -- Design

Shape the system before building it.

| # | Command | What it does |
|---|---------|--------------|
| 3a | `/create-ux-design` | Create UX design specs through collaborative visual exploration. Journey-first approach producing design tokens, components, patterns, and accessibility specs. |
| 3b | `/create-security-architecture` | Define security patterns before detailed architecture. Covers authentication, authorization, data protection, and compliance controls. |
| 3c | `/create-architecture` | Collaborative architectural decisions for AI-agent consistency. Outputs tech stack, project structure, module boundaries, contracts, testing strategy, and build order. |

> **Order matters.** UX and security architecture feed into `/create-architecture`, so run them first if your project needs them. `/create-architecture` is required before implementation.

---

## Phase 4 -- Implementation

Build the application from your specs.

| # | Command | What it does |
|---|---------|--------------|
| 4a | `/generate-project-context` | Generate a `project-context.md` with critical rules and patterns AI agents must follow. Run this before building if you have an existing codebase. |
| 4b | `/build-from-prd` | Autonomous build from PRD + architecture. A tech-lead agent orchestrates parallel subagents across 5 phases: discover, scaffold, delegate, integrate, validate. |
| 4c | `/quick-build` | Faster build from PRD + architecture. Direct implementation without subagent delegation -- builds modules and verifies incrementally. |

> **Choose one builder.** `/build-from-prd` for larger projects (parallel subagents). `/quick-build` for smaller or simpler projects.

---

## Phase 5 -- Testing & Quality

Verify the implementation works correctly.

| # | Command | What it does |
|---|---------|--------------|
| 5a | `/write-tests` | Write tests for existing code. Ranks modules by risk and writes unit/edge/error/behavioral tests against specs. |
| 5b | `/real-data-validation` | Run implementation against real data. Classifies failures as code bugs, integration gaps, or input issues, and auto-fixes code bugs. |
| 5c | `/code-simplifier` | Simplify and clean up source code. Removes dead code, reduces complexity, consolidates duplicates while preserving public APIs. |
| 5d | `/create-test-plan` | Create a UAT test plan from the PRD. Derives test cases from functional requirements with pass/fail tracking. |
| 5e | `/security-checklist` | Enterprise security validation. Validates against OWASP and enterprise standards covering auth, data protection, input validation, APIs, and infrastructure. |

> **Typical order:** `/write-tests` -> `/real-data-validation` -> `/code-simplifier` -> `/create-test-plan` -> `/security-checklist`.

---

## Phase 6 -- Deployment

Prepare for release.

| # | Command | What it does |
|---|---------|--------------|
| 6a | `/create-cicd-pipeline` | Define CI/CD pipeline configuration. Produces platform-specific YAML (GitHub Actions, GitLab CI, etc.) with quality gates. |
| 6b | `/create-deployment-strategy` | Plan phased rollout, pilots, and staged delivery. Defines phases, pilot groups, feature flags, rollback triggers, and success metrics. |
| 6c | `/create-data-migration` | Plan data movement from legacy to new systems. Documents source inventory, mapping, validation rules, and rollback procedures. |
| 6d | `/create-change-request` | Create CAB documentation for deployment approval. Documents change details, impact, implementation plan, and rollback plan. |

> `/create-data-migration` and `/create-change-request` are only needed for brownfield/enterprise projects.

---

## Phase 7 -- Operations & Handoff

Hand off to the people who will run and use the system.

| # | Command | What it does |
|---|---------|--------------|
| 7a | `/create-runbook` | Create an operational runbook for support teams. Covers health checks, procedures, troubleshooting, alerts, and escalation paths. |
| 7b | `/create-user-docs` | Create end-user documentation and training materials. Produces getting-started guides, how-tos, FAQs, and troubleshooting. |

---

## Meta Skills

Used internally by other skills or invoked directly for advanced analysis.

| Command | What it does |
|---------|--------------|
| `/_deep-dive` | Apply advanced elicitation methods to enhance specific content. 50+ specialized techniques with context-aware selection. |
| `/_party-mode` | Orchestrate group discussions between multiple AI agents with distinct personas for multi-perspective analysis. |

---

## Example Pipelines

### Greenfield (full)

```
1. /create-product-brief
2. /prd-create  ->  /prd-validate
3. /create-ux-design  ->  /create-architecture
4. /build-from-prd
5. /write-tests  ->  /real-data-validation  ->  /code-simplifier
6. /create-cicd-pipeline  ->  /create-deployment-strategy
7. /create-runbook  ->  /create-user-docs
```

### Greenfield (minimal)

```
1. /prd-create
2. /create-architecture
3. /quick-build
4. /write-tests
```

### Brownfield

```
1. /create-research  ->  /analyze-integrations
2. /prd-create  ->  /prd-validate
3. /create-architecture
4. /build-from-prd
5. /write-tests  ->  /real-data-validation
6. /create-data-migration  ->  /create-deployment-strategy
```

### Enterprise (governance required)

```
1. /create-business-case  ->  /create-product-brief
2. /prd-create  ->  /prd-validate
3. /create-security-architecture  ->  /create-architecture
4. /build-from-prd
5. /write-tests  ->  /security-checklist
6. /create-change-request  ->  /create-deployment-strategy
7. /create-runbook  ->  /create-user-docs
```

---

## Skill Structure

Each skill lives under `.claude/skills/` and follows this layout:

```
skill-name/
├── skill.md              # Skill definition (frontmatter + instructions)
└── steps-*/              # Step files for multi-step workflows (optional)
    ├── step-01-*.md
    ├── step-02-*.md
    └── ...
```

Shared PRD resources are in `_prd-data/`:

- `prd-template.md` -- PRD document template
- `prd-purpose.md` -- PRD guidelines and best practices
- `validation-checks.md` -- Validation criteria for PRD quality
