---
name: 'step-02-structure'
description: 'Define project structure, coding patterns, and module boundaries'
nextStepFile: './step-03-specifications.md'
outputFile: '{planning_artifacts}/architecture.md'
---

# Step 2: Structure & Patterns

**Progress:** Step 2 of 3 → Next: Specifications

**Goal:** Define the complete project structure, coding patterns, and module boundaries.

---

## Instructions

### 1. Define Project Structure

Based on framework selected in Step 1, generate directory tree following framework conventions.

**Structure must include:**
- Source code organization (framework-specific)
- Test file locations
- Configuration files
- Database/schema files
- Static assets (if applicable)

**Derive from:**
- Framework conventions (e.g., Next.js app router, NestJS modules)
- PRD functional areas (FR-[AREA]-* → corresponding directories)
- Module count from FRs

**Output:** Complete directory tree with brief inline comments explaining purpose of non-obvious directories.

---

### 2. Define Coding Patterns

**Naming Conventions Table:**

| Element | Convention | Example |
|---------|------------|---------|
| Component files | Framework standard | (derive from framework) |
| Utility files | kebab-case | `user-service.ts` |
| Functions | camelCase | `getUserById` |
| DB Tables | snake_case | `user_accounts` |
| API Routes | kebab-case | `/api/user-profile` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Types/Interfaces | PascalCase | `UserProfile` |

**API Response Format:**

```typescript
// Success
{ data: T, error: null }

// Error
{ data: null, error: { code: string, message: string } }
```

**Error Code Taxonomy:**

| Prefix | Category | HTTP Status |
|--------|----------|-------------|
| AUTH_ | Authentication | 401/403 |
| VAL_ | Validation | 400 |
| RES_ | Resource | 404/409 |
| SYS_ | System | 500 |

Add domain-specific prefixes from PRD FR areas (e.g., FR-ORDER-* → ORDER_).

---

### 3. Define Module Boundaries

Extract capability areas from PRD Functional Requirements (FR-[AREA]-###).

**For each area, create entry:**

| Module | Location | Responsibility | Implements |
|--------|----------|----------------|------------|
| [area] | `src/[path]/` | [what it does] | FR-[AREA]-* |

**Module rules (include in document):**
- Each module owns its FRs completely
- Cross-module calls go through service interfaces
- Database access encapsulated within modules

---

### 4. Update Architecture Document

Update `{outputFile}` with:
- Complete Project Structure (directory tree)
- Coding Patterns (naming, response format, error codes)
- Module Boundaries table

---

### 5. Validation Check

Before proceeding, verify:
- [ ] Every FR-[AREA] has a corresponding module
- [ ] Directory structure supports all modules
- [ ] Naming conventions match framework standards

**If gaps:** Fix before checkpoint.

---

### 6. Checkpoint

Present to user:
- Project structure overview (collapsed view)
- Module boundaries table
- Any pattern decisions made

**Menu:**
- **[C] Continue** - Proceed to Step 3: Specifications
- **[R] Revise** - Adjust structure or patterns
- **[X] Exit** - Save progress and stop

**On Continue:** Update frontmatter `current_step: 3`, load `{nextStepFile}`
