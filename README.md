# Enterprise Skills Suite

AI-human collaborative skills for enterprise internal project development. Structured workflows from business case to deployment and support handoff.

## Quick Start

```
/create-business-case     # Justify the project
/create-project-charter   # Define scope
/prd-create               # Detail requirements
/build-from-prd           # Build it
/create-test-plan         # Prepare UAT
/security-checklist       # Security review
/create-change-request    # Get CAB approval
/create-runbook           # Ops handoff
/create-user-docs         # End-user training
```

---

## Skills Overview

### Planning & Discovery

| Skill | Purpose | Output |
|-------|---------|--------|
| `/create-business-case` | ROI and budget justification | Business case |
| `/stakeholder-research` | Map stakeholders, systems, constraints | Research report |
| `/create-project-charter` | Define vision, users, MVP scope | Project charter |
| `/create-security-architecture` | Early security patterns before design | Security architecture |

### Requirements & Design

| Skill | Purpose | Output |
|-------|---------|--------|
| `/prd-create` | Comprehensive requirements | 7-section PRD |
| `/prd-validate` | Quality check PRD | Validation report |
| `/prd-edit` | Improve existing PRD | Updated PRD |
| `/create-ux-design` | UI/UX specifications | UX design spec |
| `/create-architecture` | Technical design decisions | Architecture doc |
| `/analyze-integrations` | Map enterprise system connections | Integration spec |

### Implementation

| Skill | Purpose | Output |
|-------|---------|--------|
| `/generate-project-context` | AI coding rules | project-context.md |
| `/build-from-prd` | Autonomous implementation | Working application |
| `/create-cicd-pipeline` | CI/CD pipeline configuration | Pipeline spec + config files |

### Quality & Security

| Skill | Purpose | Output |
|-------|---------|--------|
| `/create-test-plan` | UAT test cases from PRD | Test plan |
| `/security-checklist` | Enterprise security validation | Security checklist |

### Deployment & Handoff

| Skill | Purpose | Output |
|-------|---------|--------|
| `/create-deployment-strategy` | Phased rollout planning | Deployment strategy |
| `/create-data-migration` | Data migration planning | Migration plan |
| `/create-change-request` | CAB approval documentation | Change request |
| `/create-runbook` | Operational procedures | Runbook |
| `/create-user-docs` | End-user documentation | User guide |

### Enhancement Tools

| Skill | Purpose |
|-------|---------|
| `/_deep-dive` | Apply 50+ elicitation methods |
| `/_party-mode` | Multi-agent discussion |

---

## Workflow Routes

### Route 1: Full Enterprise Project

Complete workflow for new internal projects.

```
/create-business-case        Budget approval
         │
         ▼
/stakeholder-research        Map stakeholders & systems
         │
         ▼
/create-project-charter      Define scope
         │
         ▼
/create-security-architecture  Security patterns (before architecture)
         │
         ▼
/analyze-integrations        Detail system connections
         │
         ▼
/prd-create → /prd-validate  Requirements
         │
         ▼
/create-ux-design            UI/UX (if needed)
         │
         ▼
/create-architecture         Technical design
         │
         ▼
/create-cicd-pipeline        CI/CD configuration
         │
         ▼
/build-from-prd              Implementation
         │
         ▼
/create-test-plan            UAT preparation
         │
         ▼
/security-checklist          Security review
         │
         ▼
/create-data-migration       Data migration (if brownfield)
         │
         ▼
/create-deployment-strategy  Phased rollout plan
         │
         ▼
/create-runbook              Ops documentation
         │
         ▼
/create-user-docs            End-user training
         │
         ▼
/create-change-request       CAB approval
         │
         ▼
Deploy
```

### Route 2: Quick Internal Tool

Smaller projects with clear scope.

```
/create-project-charter → /prd-create → /create-architecture → /build-from-prd → /create-change-request
```

### Route 3: Integration Project

Focus on connecting existing systems.

```
/stakeholder-research → /analyze-integrations → /prd-create → /create-architecture
```

### Route 3b: Brownfield Modernization

Replacing or modernizing legacy systems.

```
/stakeholder-research        Map existing systems & stakeholders
         │
         ▼
/analyze-integrations        Document current integrations
         │
         ▼
/create-project-charter      Define scope (includes Brownfield Context)
         │
         ▼
/create-security-architecture  Security requirements
         │
         ▼
/prd-create                  Requirements (Brownfield classification)
         │
         ▼
/create-architecture         Tech design (includes Legacy Integration section)
         │
         ▼
/create-data-migration       Data migration plan
         │
         ▼
/create-cicd-pipeline        CI/CD with deployment automation
         │
         ▼
/build-from-prd              Implementation
         │
         ▼
/create-deployment-strategy  Phased rollout with parallel run
         │
         ▼
/create-change-request       CAB approval
```

### Route 4: PRD Improvement

Fix or enhance existing requirements.

```
/prd-validate → Review findings → /prd-edit
```

### Route 5: Deployment Prep

System built, preparing for deployment.

```
/create-test-plan → /security-checklist → /create-runbook → /create-user-docs → /create-change-request
```

---

## Skill Integration

### How Skills Connect

```
                    ┌─────────────────────────────────────┐
                    │   /create-security-architecture     │
                    │   (Run BEFORE architecture design)  │
                    └───────────────┬─────────────────────┘
                                    │ Informs
                                    ▼
┌────────────────────┐    ┌─────────────────────────────────────┐
│/analyze-integrations│───▶│       /create-architecture          │
└────────────────────┘    └───────────────┬─────────────────────┘
         │                                │
         │                                ▼
         │                ┌─────────────────────────────────────┐
         │                │       /create-cicd-pipeline         │
         │                └───────────────┬─────────────────────┘
         │                                │
         ▼                                ▼
┌────────────────────┐    ┌─────────────────────────────────────┐
│/create-data-migration│──▶│    /create-deployment-strategy      │
└────────────────────┘    └───────────────┬─────────────────────┘
                                          │
                                          ▼
                          ┌─────────────────────────────────────┐
                          │       /create-change-request        │
                          └───────────  ──────────────────────────┘
```

### When to Use Each Skill

| Skill | Use When | Skip When |
|-------|----------|-----------|
| `/create-security-architecture` | Compliance requirements, PII/PHI data, public-facing, high-risk | Internal tools, low-risk, no sensitive data |
| `/create-data-migration` | Brownfield, legacy data, system replacement | Greenfield, no existing data |
| `/create-deployment-strategy` | Large user base, high-risk, phased rollout needed | Small team, low-risk, single deployment |
| `/create-cicd-pipeline` | Any project with code, automated deployments | Manual deployments, scripts only |

---

## Practical Examples

### Example 1: Healthcare Application (Compliance-Driven)

Building a patient portal with HIPAA requirements.

```bash
/create-business-case           # Budget justification
/stakeholder-research           # Map stakeholders
/create-project-charter         # Define scope

# CRITICAL: Security architecture FIRST (HIPAA)
/create-security-architecture   # Auth, encryption, audit logging, PHI handling
                                # → Output feeds into architecture decisions

/create-architecture            # Uses security decisions for tech choices
/create-cicd-pipeline           # HIPAA-compliant artifact storage, security gates
/create-deployment-strategy     # Phase 1: Single clinic → Phase 2: Regional → Phase 3: Full
```

**Key Flow:** Security Architecture → Architecture → CI/CD → Deployment

---

### Example 2: Legacy System Modernization (Brownfield)

Migrating from Oracle ERP to modern microservices.

```bash
/stakeholder-research           # Discovers: 3 Oracle DBs, 15 years of data
/analyze-integrations           # Maps: Data flows, API dependencies

/create-data-migration          # Output:
                                #   - Data inventory (500 tables, 2TB)
                                #   - Field mappings with transforms
                                #   - Validation rules
                                #   - Migration sequence
                                #   - Rollback procedures

/create-deployment-strategy     # Aligned with migration phases:
                                #   Phase 1: Reference data, parallel run
                                #   Phase 2: Customers, limited pilot
                                #   Phase 3: Transactions, cutover weekend

/create-change-request          # References migration + deployment plans
```

**Key Flow:** Integrations → Data Migration → Deployment Strategy → Change Request

---

### Example 3: Public API Platform (DevOps Focus)

Building a public API with strict SLAs.

```bash
/create-security-architecture   # OAuth2, rate limiting, WAF, DDoS protection

/create-architecture            # API gateway selection, auth service design

/create-cicd-pipeline           # Platform: GitHub Actions
                                # Gates: 90% coverage, 0 critical vulns
                                # Output: Actual workflow YAML files

/create-deployment-strategy     # Canary: 1% → 10% → 50% → 100%
                                # Feature flags, rollback triggers
```

**Key Flow:** Security → Architecture → CI/CD → Deployment

---

### Example 4: Quick Internal Tool (Minimal Path)

Simple dashboard for internal team.

```bash
/create-project-charter         # Define scope
/prd-create                     # Requirements
/create-architecture            # Simple architecture
/create-cicd-pipeline           # Basic CI/CD

# Skip: security-architecture (internal, low risk)
# Skip: data-migration (greenfield)
# Skip: deployment-strategy (small user base)
```

---

### Example 5: High-Risk Financial System (Full Workflow)

Trading platform with regulatory requirements.

```bash
/create-business-case
/stakeholder-research

/create-security-architecture   # SOX, PCI-DSS compliance
                                # Encryption, tokenization, audit logging

/analyze-integrations           # Market data feeds, clearing houses
/prd-create → /prd-validate

/create-architecture            # Informed by security requirements

/create-cicd-pipeline           # 95% coverage, 0 vulnerabilities
                                # Mandatory code review, audit trail

/create-data-migration          # Historical trade data
                                # Zero tolerance for data loss

/create-deployment-strategy     # Blue-green (zero downtime)
                                # Paper trading pilot
                                # Regulatory sign-off gates

/create-test-plan
/security-checklist             # Validate against security architecture
/create-runbook
/create-change-request          # Multiple approvals required
```

---

## Output Locations

| Document | Location |
|----------|----------|
| Business Case | `docs/business-case.md` |
| Stakeholder Research | `docs/stakeholder-research.md` |
| Project Charter | `docs/project-charter.md` |
| Security Architecture | `docs/security-architecture.md` |
| Integration Spec | `docs/integration-spec.md` |
| PRD | `docs/prd.md` |
| UX Design | `docs/ux-design.md` |
| Architecture | `docs/architecture.md` |
| CI/CD Pipeline | `docs/cicd-pipeline.md` |
| Data Migration | `docs/data-migration.md` |
| Deployment Strategy | `docs/deployment-strategy.md` |
| Test Plan | `docs/test-plan.md` |
| Security Checklist | `docs/security-checklist.md` |
| Runbook | `docs/runbook.md` |
| User Guide | `docs/user-guide.md` |
| Change Request | `docs/change-request.md` |
| Project Context | `project-context.md` |

---

## Project Structure

```
.claude/skills/
├── _deep-dive/              # Enhancement: elicitation methods
├── _party-mode/             # Enhancement: multi-agent discussions
├── _prd-data/               # Shared templates and validation
├── analyze-integrations/    # Enterprise integration mapping
├── build-from-prd/          # Autonomous implementation
├── create-architecture/     # Technical architecture
├── create-business-case/    # ROI and budget justification
├── create-change-request/   # CAB documentation
├── create-cicd-pipeline/    # CI/CD pipeline configuration
├── create-data-migration/   # Data migration planning
├── create-deployment-strategy/ # Phased rollout planning
├── create-product-brief/    # Project charter
├── create-research/         # Stakeholder research
├── create-runbook/          # Operational procedures
├── create-security-architecture/ # Early security patterns
├── create-test-plan/        # UAT test planning
├── create-user-docs/        # End-user documentation
├── create-ux-design/        # UX specifications
├── generate-project-context/# AI coding rules
├── prd-create/              # PRD creation
├── prd-edit/                # PRD editing
├── prd-validate/            # PRD validation
└── security-checklist/      # Security validation
```

---

## Usage Tips

1. **Start with business case** for projects needing budget approval
2. **Use stakeholder research** to map organizational landscape early
3. **Run validation** before architecture to catch requirement gaps
4. **Integration spec** is critical when connecting to existing systems
5. **Test plan** derives test cases directly from PRD requirements
6. **Security checklist** before change request for compliance
7. **Runbook** ensures support team can operate the system
8. **User docs** drive adoption after deployment

---

## Brownfield Project Support

When working with existing systems (brownfield), skills automatically capture additional context:

| Skill | Brownfield Support |
|-------|-------------------|
| `/create-project-charter` | Section 7: Brownfield Context (existing systems, legacy data, constraints) |
| `/prd-create` | Classification includes existing system disposition and coexistence strategy |
| `/create-architecture` | Section 8: Legacy Integration (adapters, constraints, migration touchpoints) |
| `/analyze-integrations` | Maps connections to existing enterprise systems |
| `/create-data-migration` | Full data migration planning (mapping, validation, rollback) |
| `/create-deployment-strategy` | Supports parallel run, phased cutover strategies |

**Brownfield Detection:** Skills detect brownfield projects when:
- User indicates "Brownfield" during discovery
- Existing systems are identified in stakeholder research
- Project charter includes Brownfield Context section

**Recommended Brownfield Flow:**
1. `/stakeholder-research` - Discover all existing systems
2. `/analyze-integrations` - Map current integration points
3. `/create-project-charter` - Capture brownfield context
4. `/create-data-migration` - Plan data movement
5. `/create-architecture` - Design with legacy integration section
6. `/create-deployment-strategy` - Plan parallel run or phased cutover

---

## Workflow Continuity

All skills support interruption and resumption:
- Progress saved in document frontmatter
- Re-run same command to continue where you left off
