---
name: 'step-03-specifications'
description: 'Generate API contracts, database schema, finalize architecture'
outputFile: '{planning_artifacts}/architecture.md'
---

# Step 3: Specifications

**Progress:** Step 3 of 3 → Final

**Goal:** Generate API contracts from FRs, database schema from Data Entities, and finalize the architecture document.

---

## Instructions

### 1. Generate API Contracts

Transform each PRD Functional Requirement into an API contract.

**Mapping:**

| PRD FR Field | Maps To |
|--------------|---------|
| FR Input | Request body/params |
| FR Rules | Implementation notes (keep in PRD, reference only) |
| FR Output | Success response (200) |
| FR Error | Error responses (4xx) |

**Format:**

```markdown
### METHOD /api/[route]
- **FR:** FR-AREA-###
- **Request:** `{ field: type, ... }`
- **Response 200:** `{ data: { ... } }`
- **Response 4xx:** `{ error: { code: "...", message: "..." } }`
```

**Organize by module** from Step 2 Module Boundaries table.

**Notes:**
- Derive route from FR subject (e.g., "Create Order" → POST /api/orders)
- Use error codes from Step 2 taxonomy
- Include path params where appropriate (e.g., `/api/orders/:id`)

---

### 2. Generate Database Schema

Transform PRD Data Entities (Section 5) into database schema.

**For each Data Entity:**

1. Create table with columns matching entity attributes
2. Add constraints from FR Input validation rules
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
-- Entity: [PRD Entity Name] | FRs: FR-AREA-*

CREATE INDEX idx_[table]_[column] ON [table]([column]);
```

**Include:**
- UUID primary keys (unless PRD specifies otherwise)
- Foreign keys with explicit references
- Unique constraints where entity requires
- Indexes for common queries
- Timestamps (created_at, updated_at)

---

### 3. Define Environment Variables

Based on technology stack (Step 1) and integrations:

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Database connection string |
| [AUTH_VAR] | Yes/No | Based on auth choice |
| [FRAMEWORK_VARS] | Varies | Framework-specific |
| [INTEGRATION_VARS] | Varies | Third-party integrations |

---

### 4. Final Validation

Verify complete coverage:

| Check | Status |
|-------|--------|
| Every FR-* has API endpoint | ✓/✗ |
| Every Data Entity has table | ✓/✗ |
| All FR Input constraints in schema | ✓/✗ |
| All FR Error cases have error codes | ✓/✗ |
| Environment variables complete | ✓/✗ |

**If gaps found:** Add missing items before finalizing.

---

### 5. Finalize Document

Update `{outputFile}` with:
- Complete API Contracts section
- Complete Database Schema section
- Environment Variables table

Update frontmatter:
```yaml
---
status: complete
current_step: 3
completed_at: [date]
---
```

---

### 6. Complete

Present to user:

**Summary:**
- API endpoints: [count]
- Database tables: [count]
- Modules: [count]

**Final Output:**
```
Architecture complete: {outputFile}

PRD + Architecture = complete implementation context.
Ready for development.
```

**No menu** - workflow complete.
