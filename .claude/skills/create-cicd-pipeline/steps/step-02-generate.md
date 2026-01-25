---
name: 'step-02-generate'
description: 'Create pipeline specification and config files'

# File references
outputFile: '{project_root}/docs/cicd-pipeline.md'
deepDiveSkill: '{skills_root}/_deep-dive/skill.md'
partyModeSkill: '{skills_root}/_party-mode/skill.md'
---

# Step 2: Generate

**Progress: Step 2 of 2** - Final Step

## STEP GOAL

Generate comprehensive CI/CD pipeline specification and actual configuration files for the chosen platform, including build, test, and deploy stages with quality gates.

## EXECUTION RULES

- **Hybrid step** - generate based on discovery + user validation
- You are a DevOps Engineer - create working configuration files
- Configuration must be valid YAML/syntax for the chosen platform
- Follow platform-specific best practices

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{outputFile}` to get discovery findings from Step 1:
- Tech stack details
- CI/CD platform
- Environment configurations
- Quality gate requirements
- Branching strategy

### 2. Document Environments

**Present Environment Configuration:**
"**Environments:**

| Environment | Purpose | URL | Deployment Trigger | Approvals |
|-------------|---------|-----|-------------------|-----------|
| dev | Development testing | dev.{domain} | Push to main | None |
| staging | Pre-production | staging.{domain} | Manual / PR to release | None |
| production | Live system | {domain} | Manual | Required |

**Environment Variables:**
| Variable | dev | staging | production |
|----------|-----|---------|------------|
| DATABASE_URL | {dev-db} | {staging-db} | {prod-db} |
| API_URL | {dev-api} | {staging-api} | {prod-api} |
| LOG_LEVEL | debug | info | warn |

**Secrets (stored in {secrets manager}):**
| Secret | Environments | Purpose |
|--------|--------------|---------|
| DATABASE_PASSWORD | All | Database access |
| API_KEY | All | External API |
| DEPLOY_KEY | staging, prod | Deployment auth |

Does this environment setup work?"

Wait for user confirmation.

### 3. Define Build Stage

**Present Build Stage:**
"**Build Stage:**

**Triggers:**
```
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

**Build Steps:**
1. Checkout code
2. Setup runtime ({language} {version})
3. Cache dependencies
4. Install dependencies
5. Build application
6. Generate artifacts

**Commands:**
```yaml
# Install
{package_manager} install

# Build
{package_manager} run build

# Artifacts
- dist/
- build/
```

**Caching Strategy:**
| Cache | Key | Paths |
|-------|-----|-------|
| Dependencies | {lockfile hash} | node_modules/ or .venv/ |
| Build cache | {source hash} | .next/cache/ or __pycache__/ |

**Build Matrix (if applicable):**
| Dimension | Values |
|-----------|--------|
| OS | ubuntu-latest |
| {Language} version | {versions} |

Any build configuration to adjust?"

Wait for user confirmation.

### 4. Define Test Stage

**Present Test Stage:**
"**Test Stage:**

**Unit Tests:**
```yaml
name: Unit Tests
command: {test_command}
coverage:
  threshold: {coverage_threshold}%
  report: coverage/lcov.info
```

**Integration Tests:**
```yaml
name: Integration Tests
command: {integration_test_command}
services:
  - postgres:14
  - redis:7
```

**E2E Tests (if applicable):**
```yaml
name: E2E Tests
command: {e2e_command}
browser: chromium
artifacts:
  - test-results/
  - playwright-report/
```

**Security Scanning:**

| Scan Type | Tool | Threshold |
|-----------|------|-----------|
| SAST | {tool} | 0 critical |
| SCA (Dependencies) | {tool} | 0 critical/high |
| Secrets | {tool} | 0 findings |

**Lint & Format:**
```yaml
- name: Lint
  command: {lint_command}

- name: Type Check
  command: {typecheck_command}
```

Any test configuration to adjust?"

Wait for user confirmation.

### 5. Define Deploy Stage

**Present Deploy Stage:**
"**Deploy Stage:**

**Deployment Method:** {Container/Serverless/VM/Kubernetes}

**Deploy to dev:**
```yaml
name: Deploy to dev
trigger: Push to main
steps:
  - Build Docker image
  - Push to {registry}
  - Deploy to {target}
  - Run smoke tests
```

**Deploy to staging:**
```yaml
name: Deploy to staging
trigger: Manual / Release branch
steps:
  - Pull verified image
  - Deploy to {target}
  - Run integration tests
  - Notify team
```

**Deploy to production:**
```yaml
name: Deploy to production
trigger: Manual with approval
steps:
  - Require approval from: {approvers}
  - Pull verified image
  - Deploy with {strategy} (rolling/blue-green/canary)
  - Run smoke tests
  - Monitor for 10 minutes
  - Auto-rollback on failure
```

**Infrastructure as Code:**
```yaml
- name: Plan Infrastructure
  command: terraform plan

- name: Apply Infrastructure
  command: terraform apply -auto-approve
  environment: {requires approval for prod}
```

Any deployment configuration to adjust?"

Wait for user confirmation.

### 6. Define Quality Gates

**Present Quality Gates:**
"**Quality Gates:**

| Gate | Threshold | Blocking | Stage |
|------|-----------|----------|-------|
| Unit test coverage | {threshold}% | Yes | Test |
| All tests pass | 100% | Yes | Test |
| Lint errors | 0 | Yes | Test |
| Type errors | 0 | Yes | Test |
| Critical vulnerabilities | 0 | Yes | Security |
| High vulnerabilities | 0 | {Yes/No} | Security |
| Secrets detected | 0 | Yes | Security |
| Build time | < {minutes} min | No | Build |
| Docker image size | < {size} MB | No | Build |

**Gate Enforcement:**
- PRs cannot merge without passing all blocking gates
- Main branch protection enabled
- Required reviewers: {number}

Any quality gates to adjust?"

Wait for user confirmation.

### 7. Define Notifications

**Present Notifications:**
"**Notifications:**

| Event | Channel | Recipients |
|-------|---------|------------|
| Build started | {Slack/Teams} | #dev-builds |
| Build failed | {Slack/Teams} | #dev-builds, @committer |
| Deploy to staging | {Slack/Teams} | #releases |
| Deploy to production | {Slack/Teams} | #releases, @oncall |
| Security vulnerability | Email | security-team@{domain} |

**Notification Content:**
- Build status (pass/fail)
- Commit message and author
- Link to build logs
- Duration

Any notification preferences to adjust?"

Wait for user confirmation.

### 8. Generate Pipeline Configuration

Based on the chosen platform, generate actual configuration files:

**For GitHub Actions:**
"**Pipeline Configuration Files:**

I'll generate the following files:

1. `.github/workflows/ci.yml` - Main CI pipeline
2. `.github/workflows/deploy-staging.yml` - Staging deployment
3. `.github/workflows/deploy-production.yml` - Production deployment

**ci.yml:**
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '{version}'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: '{package_manager}'

      - name: Install dependencies
        run: {install_command}

      - name: Build
        run: {build_command}

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: '{package_manager}'

      - name: Install dependencies
        run: {install_command}

      - name: Run tests
        run: {test_command}

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage/lcov.info

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: '{package_manager}'

      - name: Install dependencies
        run: {install_command}

      - name: Lint
        run: {lint_command}

      - name: Type check
        run: {typecheck_command}

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run security scan
        uses: {security_action}
        with:
          fail-on: critical
```

Should I show the deployment workflows as well?"

Present deployment workflows if user confirms.

### 9. Update Document

Update `{outputFile}` with all sections:

- Replace *Pending* sections with actual content
- Include full pipeline configuration in document
- Update frontmatter: `stepsCompleted: ['step-01-discovery', 'step-02-generate']`
- Update document status to "Complete"

Also offer to write the actual config files:
"Would you like me to write the pipeline configuration files to your repository?

Files to create:
- `.github/workflows/ci.yml`
- `.github/workflows/deploy-staging.yml`
- `.github/workflows/deploy-production.yml`

**[Y] Yes** - Write files
**[N] No** - Just keep in documentation"

### 10. Report & Menu

**Report:**
"CI/CD pipeline specification complete for {project_name}.

**Coverage:**
- ✅ Environment Configuration ({N} environments)
- ✅ Build Stage (with caching)
- ✅ Test Stage (unit, integration, security)
- ✅ Deploy Stage ({deployment method})
- ✅ Quality Gates ({N} gates)
- ✅ Notifications
- ✅ Pipeline Configuration (ready to use)

**Pipeline Files:**
{List of generated files}

**Next Steps:**
1. Review generated configuration
2. Add secrets to {CI/CD platform}
3. Enable branch protection rules
4. Test pipeline with a PR

Document saved at `{outputFile}`
{Files written to repository if applicable}"

**Menu:**

**[R] Revise** - Make changes to any section
**[D] Deep Dive** - Explore specific area (e.g., advanced caching)
**[P] Party Mode** - Get DevOps/Dev/QA perspectives
**[W] Write Files** - Write config files to repository
**[X] Exit** - Workflow complete

**On [R]:** Discuss changes, update document and files, return to menu.

**On [D]:** Invoke `/_deep-dive` on selected section. Update document, return to menu.

**On [P]:** Invoke `/_party-mode` with DevOps team personas. Update document, return to menu.

**On [W]:** Write configuration files to repository, confirm success, return to menu.

---

## SUCCESS CRITERIA

- All environments documented with triggers and variables
- Build stage optimized with caching
- Test stage covers unit, integration, and security
- Deploy stage includes approval gates for production
- Quality gates defined with clear thresholds
- Notifications configured for key events
- Valid pipeline configuration generated for chosen platform
- Configuration files offered to write to repository
- User validated each section
- Document updated with complete pipeline specification
