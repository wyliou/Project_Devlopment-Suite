---
name: create-data-migration
description: Plan data movement from legacy systems to new application
---

# Data Migration Workflow

**Goal:** Create a comprehensive data migration plan that covers source system analysis, data mapping, validation rules, migration sequence, and rollback procedures.

**Your Role:** Data Migration Architect collaborating with stakeholders. You help identify data sources, define mappings, and plan migration phases while the user provides system knowledge and business context.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Discovery** | Identify source systems, data volumes, mapping needs | Interactive |
| 2 | **Generate** | Create migration spec with mapping, validation, rollback | Hybrid |

---

## OUTPUT STRUCTURE

```markdown
# Data Migration Plan: {project_name}

## Migration Overview
- Source systems, target system, strategy (big bang/phased/parallel)

## Data Inventory
| Source System | Tables/Objects | Record Count | Size | Priority |

## Data Mapping
| Source Table | Source Field | Target Table | Target Field | Transform |

## Validation Rules
| Check | Source Query | Target Query | Tolerance |

## Migration Sequence
1. {phase 1 - reference data}
2. {phase 2 - transactional data}
3. {phase 3 - historical data}

## Rollback Plan
- Criteria for rollback
- Steps to restore

## Cutover Schedule
| Activity | Owner | Duration | Dependencies |
```

---

## KEY FEATURES

- **Source System Analysis:** Complete inventory of data to migrate
- **Transformation Rules:** Clear mapping from source to target schema
- **Validation Strategy:** Pre and post-migration data integrity checks
- **Phased Approach:** Sequenced migration reducing risk
- **Rollback Ready:** Clear criteria and procedures for reverting

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in document frontmatter
- **Data-Driven**: Actual record counts and sizes inform planning

### Execution Rules

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update frontmatter when completing a step (enables continuation)
- Never assume data volumes - confirm with user

**When to Deviate:** If the user has existing ETL tools or migration scripts, incorporate them into the plan rather than designing from scratch.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "We have 3 legacy databases" -> Document all sources
- "Customer data is most critical" -> Prioritize accordingly
- "We need zero downtime" -> Plan for parallel run strategy
- "Let's explore the data quality issues" -> Launch deep dive

**Menu (Fallback for Structure):**
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[D] Deep Dive** - Apply advanced elicitation techniques
- **[P] Party Mode** - Multi-agent perspective gathering

---

## INTEGRATION

Data migration is critical for brownfield projects:

```
/stakeholder-research  <-- Identifies legacy systems
        |
        v
/analyze-integrations  <-- Maps system connections
        |
        v
/create-data-migration  <-- YOU ARE HERE
        |
        v
/create-deployment-strategy  <-- Migration phases align with deployment
```

Output feeds into:
- `/create-deployment-strategy` - Migration phases inform deployment phases
- `/create-test-plan` - Data validation becomes test cases
- `/create-runbook` - Cutover procedures documented

---

## PATHS

- `output_path` = `{project_root}/docs/data-migration.md`

---

## Execution

Load and execute `./steps/step-01-discovery.md` to begin.
