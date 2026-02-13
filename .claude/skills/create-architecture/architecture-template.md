---
status: in-progress
current_step: 1
prd_source:
prd_checksum:
product_category:
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
1. Install tech stack dependencies (use Build Commands)
2. Create directory structure (use src_dir/test_dir markers)
3. Set up database with schema
4. Implement modules following boundaries (use Path, Exports, Depends On)
5. Build contracts matching module assignments
6. Apply coding patterns consistently

RULES:
- Follow naming conventions exactly
- Use error codes from taxonomy
- Keep modules isolated per boundaries
- Follow logging pattern for all log output
- Respect side-effect ownership
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

### Build Commands

| Command | Value |
|---------|-------|
| Install | |
| Test | |
| Lint | |
| Type Check | |
| Format | |
| Build | |

---

## 2. Project Structure

<!-- src_dir: src/ -->
<!-- test_dir: tests/ -->

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

<!-- For web/API: HTTP JSON responses. For CLI: exit codes + stdout format. For libraries: return types + exceptions. -->

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

<!-- Add domain-specific prefixes derived from PRD Section 3 capability area headers -->

### Logging Pattern

<!-- Define log format, levels, and what gets logged.
Example:
- Format: `[{timestamp}] {level} [{module}] {message}`
- Levels: ERROR (failures), WARN (degraded), INFO (state changes), DEBUG (dev only)
- What: State transitions, external calls, errors. NOT: routine reads, internal calculations.
-->

### Side-Effect Ownership

<!-- Define which modules own which side effects.
Each side effect (file I/O, network calls, logging, database writes) should have exactly one owner.
Non-owners must delegate to the owning module.

Example:
| Side Effect | Owner Module | Non-owners Must |
|-------------|-------------|-----------------|
| File writes | file-manager | Call file-manager.write() |
| HTTP calls | api-client | Call api-client.request() |
| Logging | Each module owns its own logging | Use shared logger config |
-->

---

## 4. Module Boundaries

| Module | Path | Test Path | Responsibility | Implements | Exports | Depends On |
|--------|------|-----------|----------------|------------|---------|------------|
| | | | | FR-* | | |

### Import Graph

<!-- Directed dependency graph between modules.
Format: module-a → module-b (what it uses)
Verify: graph must be acyclic.
-->

**Module Rules:**
- Each module owns its FRs completely
- Cross-module calls go through exported interfaces
- Database access encapsulated within modules
- Side effects respect ownership table

---

## 5. Contracts

<!-- For web/API: REST endpoints. For CLI: command specs. For libraries: public API surface. -->
<!-- Each contract entry includes Module: field mapping it to Section 4 -->

<!--
=== WEB/API CONTRACT FORMAT ===
### METHOD /api/route
- **FR:** FR-###
- **Module:** {owning module from Section 4}
- **Request:** `{ field: type }`
- **Response 200:** `{ data: {...} }`
- **Response 4xx:** `{ error: { code: "...", message: "..." } }`

=== CLI CONTRACT FORMAT ===
### command-name
- **FR:** FR-###
- **Module:** {owning module from Section 4}
- **Args:** `<required> [optional]`
- **Flags:** `--flag description (default)`
- **Stdout:** `format description`
- **Exit Codes:** `0: success, 1: error, 2: usage`

=== LIBRARY CONTRACT FORMAT ===
### functionName(params): ReturnType
- **FR:** FR-###
- **Module:** {owning module from Section 4}
- **Parameters:** `param1: Type - description`
- **Returns:** `Type - description`
- **Throws:** `ErrorType - when condition`
-->

---

## 6. Database Schema

<!--
Generated from PRD Data Entities.
Includes: tables, constraints, indexes, relationships.
Skip this section for libraries/CLI tools without storage.

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
