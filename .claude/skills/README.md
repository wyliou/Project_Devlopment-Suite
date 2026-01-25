# Skills Catalog

This directory contains Claude Code skills for the Project Development Suite. Skills are invoked with `/<skill-name>` (e.g., `/prd-create`).

## Quick Reference

| Phase | Skills |
|-------|--------|
| Discovery | `/create-product-brief`, `/create-research` |
| Requirements | `/prd-create`, `/prd-edit`, `/prd-validate` |
| Design | `/create-ux-design`, `/create-security-architecture`, `/create-architecture` |
| Implementation | `/build-from-prd`, `/generate-project-context` |
| Testing | `/create-test-plan`, `/security-checklist` |
| Deployment | `/create-cicd-pipeline`, `/create-deployment-strategy`, `/create-data-migration` |
| Operations | `/create-runbook`, `/create-user-docs`, `/create-change-request` |
| Enterprise | `/create-business-case`, `/analyze-integrations` |

---

## Skills by Category

### Discovery & Planning

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| Product Brief | `/create-product-brief` | Create project charters optimized for PRD generation | Starting a new project; need to capture vision and scope |
| Research | `/create-research` | Conduct stakeholder, system, and context research through collaborative discovery | Before PRD when requirements are unclear; brownfield projects |

### PRD & Requirements

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| PRD Create | `/prd-create` | Create comprehensive PRDs optimized for AI-powered development | New project needs a PRD from scratch |
| PRD Edit | `/prd-edit` | Edit comprehensive PRDs with validation integration | Existing PRD needs updates or format conversion |
| PRD Validate | `/prd-validate` | Validate PRDs against PRD Guidelines | Check PRD quality before implementation |

### Design & Architecture

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| UX Design | `/create-ux-design` | Create comprehensive UX design specifications through collaborative visual exploration | UI-based products needing wireframes/flows |
| Security Architecture | `/create-security-architecture` | Define security patterns BEFORE detailed architecture design | Projects with security requirements; enterprise systems |
| Architecture | `/create-architecture` | Collaborative architectural decision facilitation for AI-agent consistency | After PRD, before implementation; prevents agent conflicts |

### Implementation

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| Build from PRD | `/build-from-prd` | Autonomous skill that builds a working application from PRD and architecture documents using parallel subagent delegation | Ready to implement; have PRD + architecture |
| Project Context | `/generate-project-context` | Creates a concise project-context.md file with critical rules and patterns that AI agents must follow | Existing codebase needs agent guidance |

### Testing & Quality

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| Test Plan | `/create-test-plan` | Create UAT test plan and test cases from PRD | Before UAT; need structured test coverage |
| Security Checklist | `/security-checklist` | Enterprise security validation checklist | Pre-deployment security review |

### Deployment & Operations

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| CI/CD Pipeline | `/create-cicd-pipeline` | Define CI/CD pipeline configuration for the project | Setting up automated build/deploy |
| Deployment Strategy | `/create-deployment-strategy` | Plan phased rollout, pilots, and staged delivery | Complex rollouts; enterprise deployments |
| Data Migration | `/create-data-migration` | Plan data movement from legacy systems to new application | Brownfield projects; system replacements |
| Runbook | `/create-runbook` | Create operational runbook for support team handoff | Pre-production handoff to ops team |
| User Docs | `/create-user-docs` | Create end-user documentation and training materials | Before launch; user training needed |
| Change Request | `/create-change-request` | Create CAB documentation for deployment approval | Enterprise change management process |

### Enterprise & Governance

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| Business Case | `/create-business-case` | Create business case with ROI and budget justification for project approval | Need funding/approval for project |
| Integration Analysis | `/analyze-integrations` | Map connections to existing enterprise systems for integration planning | Brownfield; connecting to existing systems |

### Meta Skills (Internal)

These skills are used internally by other skills or for advanced workflows.

| Skill | Command | Description | When to Use |
|-------|---------|-------------|-------------|
| Deep Dive | `/_deep-dive` | Apply advanced elicitation methods iteratively to enhance specific content | Called by other skills for deeper exploration |
| Party Mode | `/_party-mode` | Orchestrates group discussions between multiple agents | Multi-perspective analysis needed |

---

## Typical Workflows

### Greenfield Project (New Build)

```
/create-product-brief → /prd-create → /prd-validate → /create-architecture → /build-from-prd
```

### Brownfield Project (Existing System)

```
/create-research → /analyze-integrations → /prd-create → /create-data-migration → /create-architecture
```

### Enterprise Project (Governance Required)

```
/create-business-case → /create-product-brief → /prd-create → /create-security-architecture → /create-change-request
```

### Quick Implementation

```
/prd-create → /create-architecture → /build-from-prd
```

---

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── skill.md              # Main skill definition (frontmatter + instructions)
└── steps-*/              # Step files for multi-step workflows (optional)
    ├── step-01-*.md
    ├── step-02-*.md
    └── ...
```

### Shared Resources

The `_prd-data/` directory contains shared templates and validation rules used by PRD-related skills:

- `prd-template.md` - PRD document template
- `prd-purpose.md` - PRD guidelines and best practices
- `validation-checks.md` - Validation criteria for PRD quality

---

## Adding New Skills

1. Create a new directory under `.claude/skills/`
2. Add `skill.md` with frontmatter (`name`, `description`) and instructions
3. For multi-step workflows, create a `steps-*/` subdirectory
4. Update this README with the new skill

See existing skills for examples of different patterns:
- Simple skill: `security-checklist/`
- Multi-step workflow: `prd-create/`
- Autonomous agent: `build-from-prd/`
