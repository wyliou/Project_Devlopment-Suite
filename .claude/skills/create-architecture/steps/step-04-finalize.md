---
name: 'step-04-finalize'
description: 'Generate DB schema, env vars, brownfield section, build-from-prd readiness validation'
outputFile: '{planning_artifacts}/architecture.md'
---

# Step 4: Schema & Finalize

**Progress:** Step 4 of 4 → Final

**Goal:** Generate database schema, environment variables, brownfield integration section, and validate build-from-prd readiness.

---

## Instructions

### 1. Generate Database Schema (If Applicable)

**Skip for:** Libraries, CLI tools without persistent storage.

**For projects with storage:** Transform PRD Data Entities (Section 5) into SQL DDL.

**For each Data Entity:**

1. Create table with columns matching entity attributes
2. Apply type mapping from FR Input constraints (e.g., `email (string, RFC 5322)` → `VARCHAR(255) CHECK (...)`)
3. Add indexes for query patterns implied by FRs
4. Define foreign key relationships between entities

**Format:**

```sql
-- =====================
-- [Entity Name]
-- =====================
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [columns from entity attributes],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
-- Entity: [PRD Entity Name] | FRs: FR-001, FR-002, ...

CREATE INDEX idx_[table]_[column] ON [table]([column]);
```

**Include:**
- UUID primary keys (unless PRD specifies otherwise)
- Foreign keys with explicit references
- Unique constraints where entity requires
- Indexes for common queries
- Timestamps (created_at, updated_at)

Fill Section 6 in `{outputFile}`.

---

### 2. Define Environment Variables

Based on technology stack (Step 2) and integrations:

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Database connection string |
| [AUTH_VAR] | Yes/No | Based on auth choice |
| [FRAMEWORK_VARS] | Varies | Framework-specific |
| [INTEGRATION_VARS] | Varies | Third-party integrations |

Fill Section 7 in `{outputFile}`.

---

### 3. Brownfield Integration (If Applicable)

**Skip if Greenfield.**

If brownfield context was gathered in step 1:

1. Check the "Brownfield" checkbox in Section 8
2. Fill Existing Systems table from PRD + charter context
3. Document Integration Adapters for each legacy system
4. Document Legacy Constraints with impact and mitigation
5. Fill Data Migration Touchpoints (reference `/create-data-migration` if available)
6. Document Coexistence Strategy

Fill Section 8 in `{outputFile}`.

---

### 4. Build-from-prd Readiness Validation

This is the critical quality gate. Verify the architecture document contains every field build-from-prd needs to generate its build plan.

| Requirement | Source Section | Check |
|-------------|---------------|-------|
| language identified | S1 Build Commands | Extractable from stack + commands |
| package_manager identified | S1 Build Commands | Explicit in Install command |
| test_command defined | S1 Build Commands | Explicit and complete |
| src_dir marked | S2 comment | `<!-- src_dir: ... -->` present |
| test_dir marked | S2 comment | `<!-- test_dir: ... -->` present |
| module paths defined | S4 Path column | Every module has a path |
| module test paths defined | S4 Test Path column | Every module has a test path |
| module exports listed | S4 Exports column | Every module has exports |
| module dependencies listed | S4 Depends On column | Every module has deps (or "none") |
| naming conventions complete | S3 table | All 7 rows filled |
| error taxonomy complete | S3 taxonomy | Standard + domain-specific prefixes |
| every FR has contract | S5 | Cross-ref PRD Section 3 |
| every entity has schema | S6 | Cross-ref PRD Section 5 (if applicable) |
| logging pattern defined | S3 | Sub-section present and populated |
| side-effect ownership defined | S3 | Sub-section present and populated |

**Mandatory: Fix all issues before finalizing.**

For each failed check:
1. Identify the specific gap
2. Fill the missing information (derive from PRD or ask user if ambiguous)
3. Re-run the check
4. Repeat until all checks pass

---

### 5. Final Coverage Validation

Cross-reference completeness across all sections:

| Check | Status |
|-------|--------|
| Every FR-* has contract | ✓/✗ |
| Every Data Entity has table (if applicable) | ✓/✗ |
| All FR Input constraints reflected in schema | ✓/✗ |
| All FR Error cases have error codes in taxonomy | ✓/✗ |
| Environment variables complete for stack | ✓/✗ |
| Module graph is acyclic | ✓/✗ |
| All module paths exist in directory structure | ✓/✗ |

**If gaps found:** Fix before finalizing.

---

### 6. Finalize Document

Update `{outputFile}` frontmatter:
```yaml
---
status: complete
current_step: 4
prd_source: [path]
prd_checksum: [first 8 chars of sha256 hash of PRD content]
product_category: [category]
completed_at: [date]
---
```

---

### 7. Present Completion

**Summary:**
```
Architecture complete: {outputFile}

- Technology Stack: {framework} + {database} + {testing}
- Build Commands: {count} defined
- Modules: {count}
- Contracts: {count} ({type}: REST/CLI/Library)
- Database Tables: {count} (or "N/A")
- Environment Variables: {count}
- Build-from-prd Readiness: PASS

PRD + Architecture = complete implementation context.
```

**Suggest next step:** "Run `/build-from-prd` to begin implementation."

**No menu** — workflow complete.
