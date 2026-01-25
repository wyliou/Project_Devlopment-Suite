---
status: in-progress
current_step: 1
prd_source:
prd_checksum:
completed_at:
---

# Architecture: {{project_name}}

> Generated: {{date}}
> PRD: {{prd_path}}

<!--
=============================================================================
AI IMPLEMENTATION GUIDE

This document + PRD = complete implementation context.
- PRD defines WHAT (requirements with Input/Rules/Output/Error)
- Architecture defines HOW (stack, structure, patterns, specifications)

IMPLEMENTATION ORDER:
1. Install tech stack dependencies
2. Create directory structure
3. Set up database with schema
4. Implement modules following boundaries
5. Build API endpoints matching contracts
6. Apply coding patterns consistently

RULES:
- Follow naming conventions exactly
- Use error codes from taxonomy
- Keep modules isolated per boundaries
- Match API responses to contract format
=============================================================================
-->

---

## 1. Technology Stack

| Category | Choice | Version | Rationale |
|----------|--------|---------|-----------|
| Framework | | | |
| Database | | | |
| ORM | | | |
| Auth | | | |
| Styling | | | |
| Testing | | | |

---

## 2. Project Structure

```
project/
├── src/
├── tests/
└── ...
```

---

## 3. Coding Patterns

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Component files | | |
| Utility files | | |
| Functions | | |
| DB Tables | | |
| API Routes | | |
| Constants | | |
| Types/Interfaces | | |

### API Response Format

```typescript
// Success response
{
  data: T,
  error: null
}

// Error response
{
  data: null,
  error: {
    code: string,    // From error taxonomy
    message: string  // Human-readable
  }
}
```

### Error Code Taxonomy

| Prefix | Category | HTTP Status | Example |
|--------|----------|-------------|---------|
| AUTH_ | Authentication | 401/403 | AUTH_INVALID_TOKEN |
| VAL_ | Validation | 400 | VAL_REQUIRED_FIELD |
| RES_ | Resource | 404/409 | RES_NOT_FOUND |
| SYS_ | System | 500 | SYS_DATABASE_ERROR |

<!-- Add domain-specific prefixes derived from PRD FR areas -->

---

## 4. Module Boundaries

| Module | Location | Responsibility | Implements |
|--------|----------|----------------|------------|
| | | | FR-* |

**Module Rules:**
- Each module owns its FRs completely
- Cross-module calls go through service interfaces
- Database access encapsulated within modules

---

## 5. API Contracts

<!--
Generated from PRD Functional Requirements.
Organized by module from Section 4.

Format:
### METHOD /api/route
- **FR:** FR-AREA-###
- **Request:** `{ field: type }`
- **Response 200:** `{ data: {...} }`
- **Response 4xx:** `{ error: { code: "...", message: "..." } }`
-->

---

## 6. Database Schema

<!--
Generated from PRD Data Entities.
Includes: tables, constraints, indexes, relationships.

Format:
```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ...
);
-- Entity: [name] | FRs: FR-*
```
-->

---

## 7. Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Database connection string |
| | | |

---

## 8. Legacy Integration (Brownfield Only)

<!--
Include this section only for brownfield projects.
Document integration points, adapters, and constraints from existing systems.
-->

### Project Type
- [ ] Greenfield (new system)
- [ ] Brownfield (integrates with/replaces existing systems)

### Existing Systems

| System | Integration Type | Protocol | Notes |
|--------|-----------------|----------|-------|
| | API / Database / File / Message Queue | | |

### Integration Adapters

<!--
For each legacy system, define how the new system will integrate.

Format:
### {Legacy System} Adapter
- **Direction:** Inbound / Outbound / Bidirectional
- **Protocol:** REST / SOAP / JDBC / File / MQ
- **Data Format:** JSON / XML / CSV / Binary
- **Auth:** How to authenticate with legacy system
- **Error Handling:** How to handle legacy system failures
-->

### Legacy Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| | | |

### Data Migration Touchpoints

<!--
Reference /create-data-migration output if available.
List tables/entities that need mapping between legacy and new schemas.
-->

| Legacy Entity | New Entity | Mapping Notes |
|---------------|------------|---------------|
| | | |

### Coexistence Strategy

<!--
How will old and new systems run together during transition?
- Parallel run with data sync
- Strangler fig pattern (gradual replacement)
- Big bang cutover
-->

**Strategy:** {{Parallel Run / Strangler Fig / Big Bang / Phased Cutover}}

**Sync Mechanism:** {{How data stays in sync during transition}}

**Cutover Criteria:** {{When to fully switch to new system}}
