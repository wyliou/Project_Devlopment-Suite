---
name: 'step-02-generate'
description: 'Create migration spec with mapping, validation, and rollback'

# File references
outputFile: '{project_root}/docs/data-migration.md'
deepDiveSkill: '{skills_dir}/_deep-dive/skill.md'
partyModeSkill: '{skills_dir}/_party-mode/skill.md'
---

# Step 2: Generate

**Progress: Step 2 of 2** - Final Step

## STEP GOAL

Create comprehensive data migration specification including data inventory, field mappings, transformation rules, validation checks, migration sequence, and rollback procedures.

## EXECUTION RULES

- **Hybrid step** - generate based on discovery + user validation
- You are a Data Migration Architect - create specific, executable plans
- All mappings must be explicit and verifiable
- Consider data integrity at every step

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{outputFile}` to get discovery findings from Step 1:
- Source systems and data volumes
- Target system details
- Migration strategy
- Known data quality issues

### 2. Create Data Inventory

For each source system, create detailed inventory:

**Present Inventory:**
"**Data Inventory:**

| Source System | Table/Object | Record Count | Size | Priority | Notes |
|---------------|--------------|--------------|------|----------|-------|
| {System 1} | customers | ~500,000 | 2GB | High | Master data |
| {System 1} | orders | ~2,000,000 | 8GB | High | Transactional |
| {System 1} | order_history | ~10,000,000 | 40GB | Medium | Historical |
| {System 2} | products | ~50,000 | 500MB | High | Reference data |

**Priority Legend:**
- High: Critical for go-live, migrate first
- Medium: Important but can follow
- Low: Historical/archive, migrate last or skip

Can you validate these estimates and priorities?"

Wait for user confirmation.

### 3. Create Data Mapping

For high-priority tables, create field-level mappings:

**Present Mappings:**
"**Data Mapping - {Table Name}:**

| Source Table | Source Field | Target Table | Target Field | Transform | Notes |
|--------------|--------------|--------------|--------------|-----------|-------|
| customers | cust_id | users | id | Direct | PK |
| customers | cust_name | users | full_name | Direct | |
| customers | cust_email | users | email | Lowercase | Normalize |
| customers | create_dt | users | created_at | UTC Convert | TZ handling |
| customers | status_cd | users | status | Lookup | Map codes |
| customers | - | users | migrated_from | Constant | 'legacy_crm' |

**Transformation Rules:**
- **Lowercase:** Convert to lowercase for consistency
- **UTC Convert:** Convert from {source TZ} to UTC
- **Lookup:** Map legacy codes to new enum values
  - 'A' -> 'active'
  - 'I' -> 'inactive'
  - 'D' -> 'deleted'

Any fields missing or transforms to adjust?"

Repeat for each high-priority table. Wait for user confirmation.

### 4. Define Validation Rules

**Present Validation Rules:**
"**Validation Rules:**

| Check | Source Query | Target Query | Tolerance | Action if Fail |
|-------|--------------|--------------|-----------|----------------|
| Row Count | SELECT COUNT(*) FROM customers | SELECT COUNT(*) FROM users WHERE migrated_from='legacy_crm' | 0 | Block |
| Sum Check | SELECT SUM(balance) FROM accounts | SELECT SUM(balance) FROM accounts | 0.01 | Block |
| Null Check | SELECT COUNT(*) WHERE email IS NULL | SELECT COUNT(*) WHERE email IS NULL | 0 | Warn |
| Referential | SELECT COUNT(*) FROM orders WHERE cust_id NOT IN (SELECT id FROM customers) | Same pattern | 0 | Block |
| Duplicate | SELECT email, COUNT(*) GROUP BY email HAVING COUNT(*) > 1 | Same pattern | 0 | Warn |

**Validation Phases:**
1. **Pre-migration:** Validate source data quality
2. **During migration:** Check batch completeness
3. **Post-migration:** Full reconciliation

Any additional validation rules needed?"

Wait for user confirmation.

### 5. Define Migration Sequence

**Present Sequence:**
"**Migration Sequence:**

Based on data dependencies and priorities:

### Phase 1: Reference Data (Prerequisites)
| Order | Table | Source | Dependency | Est. Duration |
|-------|-------|--------|------------|---------------|
| 1.1 | lookup_codes | System 1 | None | 5 min |
| 1.2 | regions | System 1 | None | 5 min |
| 1.3 | products | System 2 | None | 30 min |

### Phase 2: Master Data (Core Entities)
| Order | Table | Source | Dependency | Est. Duration |
|-------|-------|--------|------------|---------------|
| 2.1 | customers | System 1 | Phase 1 | 2 hours |
| 2.2 | suppliers | System 2 | Phase 1 | 1 hour |

### Phase 3: Transactional Data
| Order | Table | Source | Dependency | Est. Duration |
|-------|-------|--------|------------|---------------|
| 3.1 | orders | System 1 | Phase 2 | 4 hours |
| 3.2 | invoices | System 1 | Phase 2 | 3 hours |

### Phase 4: Historical Data (Optional)
| Order | Table | Source | Dependency | Est. Duration |
|-------|-------|--------|------------|---------------|
| 4.1 | order_history | System 1 | Phase 3 | 8 hours |

**Total Estimated Duration:** {Sum}

Does this sequence make sense for your dependencies?"

Wait for user confirmation.

### 6. Define Rollback Plan

**Present Rollback Plan:**
"**Rollback Plan:**

**Rollback Triggers:**
| Trigger | Threshold | Decision Maker |
|---------|-----------|----------------|
| Data loss detected | Any records missing | Migration Lead |
| Validation failures | >1% discrepancy | Migration Lead |
| Performance degradation | >50% slower | Ops Team |
| Critical bug discovered | Severity 1 | Product Owner |

**Rollback Procedures:**

**Phase 1-2 (Reference/Master Data):**
1. Stop migration process
2. Truncate target tables in reverse dependency order
3. Re-enable legacy system connections
4. Verify legacy system functional

**Phase 3 (Transactional - During Cutover):**
1. Stop migration process
2. Export any new transactions from target
3. Restore target from pre-migration backup
4. Apply new transactions to legacy system
5. Switch DNS/load balancer back to legacy

**Point of No Return:**
- After {specific milestone}, rollback becomes impractical
- At this point, forward-fix strategy applies

**Backup Strategy:**
- Full backup of source systems before migration
- Full backup of target system before each phase
- Transaction logs preserved for 30 days

Any adjustments to the rollback strategy?"

Wait for user confirmation.

### 7. Create Cutover Schedule

**Present Cutover Schedule:**
"**Cutover Schedule:**

| Time | Activity | Owner | Duration | Dependencies |
|------|----------|-------|----------|--------------|
| T-7d | Final data quality checks | Data Team | 1 day | |
| T-3d | Full backup of source systems | DBA | 4 hours | |
| T-1d | Freeze changes in legacy system | App Team | - | Communication |
| T-0 | Begin Phase 1 migration | Migration Lead | 1 hour | Freeze confirmed |
| T+1h | Validate Phase 1 | QA Team | 30 min | Phase 1 complete |
| T+1.5h | Begin Phase 2 migration | Migration Lead | 3 hours | Phase 1 validated |
| T+4.5h | Validate Phase 2 | QA Team | 1 hour | Phase 2 complete |
| T+5.5h | Begin Phase 3 migration | Migration Lead | 4 hours | Phase 2 validated |
| T+9.5h | Final validation | QA Team | 2 hours | Phase 3 complete |
| T+11.5h | Go/No-Go decision | Stakeholders | 30 min | All validation pass |
| T+12h | Switch traffic to new system | Ops Team | 30 min | Go decision |
| T+12.5h | Monitor and verify | All Teams | 2 hours | Traffic switched |
| T+14.5h | Migration complete | Migration Lead | - | All green |

**Communication Plan:**
- T-7d: Stakeholder notification of migration window
- T-1d: User notification of planned downtime
- T+12h: User notification of system available
- T+14.5h: Stakeholder notification of success

Any schedule adjustments needed?"

Wait for user confirmation.

### 8. Update Document

Update `{outputFile}` with all sections:

- Replace *Pending* sections with actual content
- Update frontmatter: `stepsCompleted: ['step-01-discovery', 'step-02-generate']`
- Update document status to "Complete"

### 9. Report & Menu

**Report:**
"Data migration plan complete for {project_name}.

**Coverage:**
- ✅ Data Inventory ({N} tables)
- ✅ Data Mapping (field-level for priority tables)
- ✅ Validation Rules ({N} checks)
- ✅ Migration Sequence (4 phases)
- ✅ Rollback Plan
- ✅ Cutover Schedule

**Key Metrics:**
- Total data volume: {Size}
- Estimated duration: {Time}
- Point of no return: {Milestone}

**Next Steps:**
1. Review with DBA and data owners
2. Create test migration scripts
3. Perform dry-run migration
4. Schedule cutover window

Document saved at `{outputFile}`"

**Menu:**

**[R] Revise** - Make changes to any section
**[D] Deep Dive** - Explore specific area (e.g., complex transforms)
**[P] Party Mode** - Get DBA/Dev/QA perspectives
**[X] Exit** - Workflow complete

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on selected section. Update document, return to menu.

**On [P]:** Invoke `/_party-mode` with migration team personas. Update document, return to menu.

---

## SUCCESS CRITERIA

- Data inventory complete with volumes and priorities
- Field-level mappings for high-priority tables
- Transformation rules documented
- Validation rules defined with thresholds
- Migration sequence respects dependencies
- Rollback plan with clear triggers and procedures
- Cutover schedule with owners and durations
- User validated each section
- Document updated with complete migration plan
