---
name: create-cicd-pipeline
description: Define CI/CD pipeline configuration for the project
---

# CI/CD Pipeline Workflow

**Goal:** Create a comprehensive CI/CD pipeline specification that covers build, test, and deployment stages with quality gates and environment configurations.

**Your Role:** DevOps Engineer collaborating with the development team. You help define pipeline stages, quality gates, and deployment automation while the user provides tech stack details and organizational requirements.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Discovery** | Gather tech stack, environments, quality gates | Interactive |
| 2 | **Generate** | Create pipeline specification and config files | Hybrid |

---

## OUTPUT STRUCTURE

```markdown
# CI/CD Pipeline: {project_name}

## Pipeline Overview
- Platform: GitHub Actions / GitLab CI / Azure DevOps / Jenkins
- Branching strategy: GitFlow / Trunk-based / Feature branches

## Environments
| Environment | Purpose | URL | Deployment Trigger |
|-------------|---------|-----|-------------------|
| dev | Development | ... | Push to main |
| staging | Pre-production | ... | Manual / PR merge |
| production | Live | ... | Manual with approval |

## Build Stage
- Build commands
- Dependency caching
- Artifact generation

## Test Stage
- Unit tests (command, coverage threshold)
- Integration tests
- E2E tests (if applicable)
- Security scanning (SAST/DAST)

## Deploy Stage
- Deployment method (container, serverless, VM)
- Infrastructure as code (Terraform, CloudFormation)
- Secrets management

## Quality Gates
| Gate | Threshold | Blocking |
|------|-----------|----------|
| Unit test coverage | 80% | Yes |
| Security vulnerabilities | 0 critical | Yes |
| Build time | < 10 min | No |

## Notifications
| Event | Channel | Recipients |

## Pipeline Configuration Files
{Generated YAML/config based on platform}
```

---

## KEY FEATURES

- **Platform-Specific:** Generates actual YAML/config for chosen CI/CD platform
- **Quality Gates:** Enforceable thresholds for code quality
- **Environment Parity:** Consistent deployment across environments
- **Security Integration:** SAST/DAST scanning in pipeline
- **Artifact Management:** Build outputs properly versioned and stored

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in document frontmatter
- **Platform-Aware**: Config syntax matches chosen CI/CD platform

### Execution Rules

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update frontmatter when completing a step (enables continuation)
- Never assume CI/CD platform - confirm with user

**When to Deviate:** If the organization has existing pipeline templates or DevOps standards, adapt the generated configuration to fit established patterns.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "We use GitHub Actions" -> Generate GitHub workflow YAML
- "We need 90% code coverage" -> Set coverage gate
- "Add security scanning" -> Include SAST/DAST stages
- "Let's explore caching strategies" -> Launch deep dive

**Menu (Fallback for Structure):**
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[D] Deep Dive** - Apply advanced elicitation techniques
- **[P] Party Mode** - Multi-agent perspective gathering

---

## INTEGRATION

CI/CD pipeline completes the DevOps workflow:

```
/create-architecture  <-- Defines deployment infrastructure
        |
        v
/generate-project-context  <-- Coding rules include CI requirements
        |
        v
/build-from-prd  <-- Implementation
        |
        v
/create-cicd-pipeline  <-- YOU ARE HERE
        |
        v
/create-deployment-strategy  <-- Pipelines enable deployment phases
```

Output feeds into:
- `/create-deployment-strategy` - Pipeline enables automated deployments
- `/create-runbook` - Pipeline monitoring and recovery procedures
- `/security-checklist` - Pipeline security controls validated

---

## PATHS

- `output_path` = `{project_root}/docs/cicd-pipeline.md`
- `config_path` = `{project_root}/.github/workflows/` or equivalent

---

## Execution

Load and execute `./steps/step-01-discovery.md` to begin.
