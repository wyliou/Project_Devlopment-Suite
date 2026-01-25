---
name: 'step-01-discovery'
description: 'Gather tech stack, environments, and quality gates'

# File references
nextStepFile: '{skill_base}/steps/step-02-generate.md'
outputFile: '{project_root}/docs/cicd-pipeline.md'
---

# Step 1: Discovery

**Progress: Step 1 of 2** - Next: Generate

## STEP GOAL

Gather comprehensive information about the tech stack, CI/CD platform preferences, environment configurations, and quality gate requirements.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a DevOps Engineer - gather requirements, don't generate configs yet
- Focus on understanding the full pipeline needs

## SEQUENCE (Follow Exactly)

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` array | -> Resume workflow |
| File exists + NO `stepsCompleted` | -> Safeguard Protocol |
| File not exists | -> Fresh Setup |

### 2. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing CI/CD pipeline spec at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `cicd-pipeline_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 3. Fresh Setup

#### A. Gather Tech Stack

**Opening:**
"Welcome! I'm your DevOps Engineer, ready to help define your CI/CD pipeline.

Let's start with your tech stack:

**Application:**
- What language(s)? (TypeScript, Python, Go, Java, etc.)
- What framework(s)? (React, Next.js, FastAPI, Spring, etc.)
- Package manager? (npm, yarn, pnpm, pip, poetry, etc.)
- Build tool? (webpack, vite, gradle, maven, etc.)

**Infrastructure:**
- Where will it be deployed? (AWS, Azure, GCP, on-prem)
- Deployment target? (Kubernetes, ECS, Lambda, VMs, etc.)
- Infrastructure as Code? (Terraform, CloudFormation, Pulumi, etc.)

**Code Repository:**
- Where is your code hosted? (GitHub, GitLab, Bitbucket, Azure DevOps)"

#### B. Gather CI/CD Platform Preferences

After initial responses, ask about CI/CD:

"Now let's discuss your CI/CD platform:

**Platform Options:**

| Platform | Best For |
|----------|----------|
| GitHub Actions | GitHub repos, good ecosystem |
| GitLab CI | GitLab repos, built-in DevSecOps |
| Azure DevOps | Microsoft stack, enterprise |
| Jenkins | Self-hosted, maximum flexibility |
| CircleCI | Fast builds, good parallelism |

**Questions:**
- Which CI/CD platform do you want to use?
- Any existing CI/CD infrastructure to integrate with?
- Self-hosted runners or cloud-hosted?
- Any platform restrictions (security, licensing)?"

#### C. Gather Environment Configuration

"Let's define your environments:

**Standard Environments:**

| Environment | Purpose | Typical Trigger |
|-------------|---------|-----------------|
| dev | Development testing | Push to feature branch |
| staging | Pre-production validation | PR merge to main |
| production | Live system | Manual or tag-based |

**Questions:**
- How many environments do you need?
- What are they called and what's their purpose?
- How should deployments to each be triggered?
- Any environment-specific configurations (URLs, databases)?
- Preview/ephemeral environments for PRs?"

#### D. Gather Quality Requirements

"Let's define your quality gates:

**Testing:**
- What test types do you have? (unit, integration, e2e)
- Test commands to run?
- Coverage requirements? (e.g., 80% minimum)
- E2E test framework? (Playwright, Cypress, Selenium)

**Code Quality:**
- Linting tools? (ESLint, Prettier, Black, etc.)
- Static analysis? (SonarQube, CodeClimate)
- Type checking? (TypeScript strict mode)

**Security:**
- Security scanning requirements? (SAST, DAST, SCA)
- Vulnerability thresholds? (block on critical/high?)
- Secrets scanning?

**Performance:**
- Build time limits?
- Artifact size limits?
- Performance testing in pipeline?"

#### E. Gather Additional Requirements

"A few more questions:

**Notifications:**
- Where should build notifications go? (Slack, Teams, Email)
- Who should be notified on failure?

**Artifacts:**
- What artifacts need to be stored? (Docker images, binaries, reports)
- Where should artifacts be stored? (Docker Hub, ECR, Artifactory)
- Retention policy?

**Secrets:**
- How are secrets managed? (GitHub Secrets, Vault, AWS Secrets Manager)
- Any secrets that need to be available during build?"

#### F. Confirm Pipeline Scope

After user provides context, confirm understanding:

**Summary:**
"Let me confirm the CI/CD pipeline scope:

**Tech Stack:**
- Language: {Language}
- Framework: {Framework}
- Package Manager: {Package manager}
- Infrastructure: {Cloud provider + deployment target}

**CI/CD Platform:**
- Platform: {Chosen platform}
- Runners: {Self-hosted/Cloud}

**Environments:**
| Environment | Trigger | Purpose |
|-------------|---------|---------|
| {env1} | {trigger} | {purpose} |
| {env2} | {trigger} | {purpose} |
| {env3} | {trigger} | {purpose} |

**Quality Gates:**
| Gate | Requirement | Blocking |
|------|-------------|----------|
| Unit Tests | {coverage}% | Yes |
| Lint | Pass | Yes |
| Security Scan | {threshold} | {Yes/No} |

**Branching Strategy:**
- {GitFlow/Trunk-based/Feature branches}

Anything to add or correct?"

#### G. Create Document

Create `{outputFile}` with initial structure:

```markdown
---
stepsCompleted: []
platform: {chosen platform}
language: {language}
framework: {framework}
deployTarget: {target}
---

# CI/CD Pipeline: {project_name}

## Document Control
- **Status:** Draft
- **Created:** {date}
- **Last Updated:** {date}

## Pipeline Overview

### Tech Stack
- **Language:** {Language}
- **Framework:** {Framework}
- **Package Manager:** {Package manager}
- **Build Tool:** {Build tool}

### CI/CD Platform
- **Platform:** {Platform}
- **Runners:** {Self-hosted/Cloud}
- **Repository:** {Repo URL}

### Branching Strategy
- **Strategy:** {GitFlow/Trunk-based/Feature branches}
- **Main branch:** {main/master}
- **Release branches:** {Pattern if applicable}

---
*Sections below to be completed in Step 2: Generate*
---

## Environments
*Pending*

## Build Stage
*Pending*

## Test Stage
*Pending*

## Deploy Stage
*Pending*

## Quality Gates
*Pending*

## Notifications
*Pending*

## Pipeline Configuration Files
*Pending*
```

### 4. Report & Menu

**Report:**
- Document created at `{outputFile}`
- Tech stack documented
- CI/CD platform selected
- Environments defined
- Quality gates scoped
- Ready to generate pipeline configuration

**Menu:**

**[C] Continue** - Proceed to Generate (Step 2)
**[R] Revise** - Discuss changes to scope
**[D] Deep Dive** - Explore specific area (e.g., security scanning options)
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-discovery']`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on CI/CD best practices or specific tooling. Update document, return to menu.

---

## SUCCESS CRITERIA

- Tech stack fully documented
- CI/CD platform selected
- All environments defined with triggers
- Quality gates specified with thresholds
- Branching strategy confirmed
- Notification preferences captured
- Document created with proper frontmatter
- User confirmed scope before proceeding
