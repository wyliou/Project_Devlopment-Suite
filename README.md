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

### Example 1: ETL Pipeline for Data Warehouse

Building a batch ETL pipeline to populate an enterprise data warehouse.

```bash
/create-business-case           # ROI: reduced reporting time, data quality
/stakeholder-research           # Data owners, analysts, BI team

/create-project-charter         # Define scope: sources, targets, SLAs

/create-security-architecture   # Data classification, encryption at rest
                                # Access controls for PII columns
                                # Audit logging for data access

/prd-create                     # FRs: extraction, transformation, loading rules
                                # NFRs: processing time < 4 hours, 99.9% accuracy

/create-architecture            # Tech stack: Airflow, dbt, Snowflake
                                # Batch scheduling, retry logic, monitoring

/create-cicd-pipeline           # dbt test gates, data quality checks
                                # Staging → Production promotion

/create-deployment-strategy     # Phase 1: Sales data → Phase 2: Finance → Phase 3: All sources
```

**Key Flow:** Security → Architecture → CI/CD → Phased Deployment

---

### Example 2: Real-time Data Streaming Platform

Building a real-time event processing system with Kafka.

```bash
/create-project-charter         # Event-driven architecture for order processing

/create-security-architecture   # mTLS for Kafka, schema registry auth
                                # Data masking for sensitive fields

/prd-create                     # FRs: event schemas, processing rules, dead letter handling
                                # NFRs: < 100ms latency, 10K events/sec throughput

/create-architecture            # Kafka, Flink/Spark Streaming, Schema Registry
                                # Exactly-once semantics, partition strategy

/create-cicd-pipeline           # Schema compatibility checks
                                # Canary deployment for consumers
                                # Performance benchmarks as gates

/create-deployment-strategy     # Canary: 1% traffic → 10% → 50% → 100%
                                # Rollback: revert consumer offset
```

**Key Flow:** Security → Architecture → CI/CD → Canary Deployment

---

### Example 3: Data Lake Migration (Brownfield)

Migrating from on-prem Hadoop to cloud-based data lake.

```bash
/stakeholder-research           # Discovers: 5 Hadoop clusters, 50TB data
                                # 200+ Hive tables, 50 Spark jobs

/analyze-integrations           # Maps: upstream sources, downstream consumers
                                # Job dependencies, scheduling

/create-data-migration          # Output:
                                #   - Table inventory (200 tables, partitioning)
                                #   - Schema mappings (Hive → Delta Lake)
                                #   - Data validation: row counts, checksums
                                #   - Job migration sequence
                                #   - Parallel run strategy

/create-architecture            # Target: Databricks, Delta Lake, Unity Catalog
                                # Coexistence: dual-write during transition

/create-deployment-strategy     # Phase 1: Reference/dimension tables
                                # Phase 2: Fact tables (parallel validation)
                                # Phase 3: Job migration, cutover
                                # Phase 4: Decommission Hadoop

/create-change-request          # Includes rollback to Hadoop if needed
```

**Key Flow:** Integrations → Data Migration → Architecture → Phased Cutover

---

### Example 4: ML Feature Store (Quick Internal Tool)

Internal feature store for ML team.

```bash
/create-project-charter         # Centralized feature management
/prd-create                     # Feature registration, versioning, serving APIs

/create-architecture            # Feast/Tecton, Redis for online, S3 for offline
                                # Point-in-time correctness

/create-cicd-pipeline           # Feature validation tests
                                # Schema drift detection

# Skip: security-architecture (internal ML team only)
# Skip: data-migration (greenfield)
# Skip: deployment-strategy (single team rollout)
```

---

### Example 5: Enterprise Data Hub (Full Workflow)

Central data platform consolidating multiple business units with regulatory requirements.

```bash
/create-business-case           # Single source of truth, reduced redundancy
/stakeholder-research           # 5 business units, compliance team, IT

/create-security-architecture   # GDPR, SOX compliance
                                # Column-level encryption, data masking
                                # Row-level security per business unit
                                # Full audit trail, data lineage

/analyze-integrations           # SAP, Salesforce, 3 legacy databases
                                # Real-time CDC, batch extracts, APIs

/prd-create → /prd-validate     # Data domains, ownership, quality rules
                                # SLAs per data product

/create-architecture            # Medallion architecture (Bronze/Silver/Gold)
                                # Data mesh principles, domain ownership
                                # Unity Catalog for governance

/create-data-migration          # 3 legacy DBs → Bronze layer
                                # Historical data: 10 years, 5TB
                                # Validation: business rule checks

/create-cicd-pipeline           # Data quality gates (Great Expectations)
                                # Schema evolution checks
                                # Lineage tracking updates

/create-deployment-strategy     # Phase 1: Sales domain (pilot)
                                # Phase 2: Finance domain
                                # Phase 3: Operations, HR
                                # Phase 4: Self-service analytics

/create-test-plan               # Data quality UAT per domain
/security-checklist             # GDPR compliance validation
/create-runbook                 # Data ops procedures, incident response
/create-change-request          # CAB approval with compliance sign-off
```

**Key Flow:** Full enterprise workflow with data governance focus

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

## Human Involvement Levels

Skills vary in how much human participation they require. Choose based on your available time and domain expertise.

### High Involvement
User actively participates throughout, provides domain expertise. Best when you have deep context to share.

| Skill | Why High |
|-------|----------|
| `/prd-create` | User drives requirements, defines scope, validates FRs |
| `/create-product-brief` | User defines vision, problem, solution |
| `/create-research` | User provides institutional knowledge |
| `/create-ux-design` | Collaborative visual exploration |
| `/create-architecture` | User confirms technology decisions |

### Medium Involvement
User provides input at checkpoints, AI generates content. Good balance of guidance and automation.

| Skill | Why Medium |
|-------|------------|
| `/prd-edit` | User approves plan, AI executes edits |
| `/prd-validate` | AI validates, user reviews findings |
| `/generate-project-context` | AI discovers patterns, user validates rules |
| `/create-business-case` | User provides data, AI structures case |
| `/analyze-integrations` | User describes systems, AI documents spec |
| `/create-security-architecture` | User provides context, AI designs controls |
| `/create-data-migration` | User describes sources, AI creates plan |
| `/create-deployment-strategy` | User provides context, AI creates strategy |
| `/create-cicd-pipeline` | User provides tech stack, AI generates config |
| `/create-test-plan` | AI derives from PRD, user validates |
| `/security-checklist` | AI assesses, user confirms findings |
| `/create-change-request` | User provides details, AI formats CR |
| `/create-runbook` | User provides ops details, AI creates runbook |
| `/create-user-docs` | User provides context, AI generates docs |

### Low Involvement
Autonomous execution with minimal human input. Ideal for well-defined inputs.

| Skill | Why Low |
|-------|---------|
| `/build-from-prd` | Fully autonomous from PRD + architecture |

### Enhancement Tools
These are helper skills invoked within other workflows, not standalone.

| Skill | Purpose |
|-------|---------|
| `/_deep-dive` | Apply 50+ elicitation methods to enhance content |
| `/_party-mode` | Multi-agent discussion for diverse perspectives |

---

## Workflow Continuity

All skills support interruption and resumption:
- Progress saved in document frontmatter
- Re-run same command to continue where you left off
