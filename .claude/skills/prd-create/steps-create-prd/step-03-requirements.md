---
name: 'step-03-requirements'
description: 'Generate FRs, NFRs, Data Entities, Tech Constraints, and Quick Reference'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-04-complete.md'
outputFile: '{project_root}/docs/prd.md'
prdPurpose: '{skills_root}/_prd-data/prd-purpose.md'
---

# Step 3: Requirements

**Progress: Step 3 of 4** - Next: Complete

## STEP GOAL

Generate comprehensive, AI-implementation-ready requirements with integrated validation.

## EXECUTION RULES

- **Interactive step** - requires user feedback on requirements
- You are a PRD Creator - generating AI-optimized requirements
- Apply quality checks during generation, not as separate step

## SEQUENCE (Follow Exactly)

### 1. Analyze Context

Review the PRD document sections 1-2 (Overview, User Journeys) to understand:
- User types and their goals
- MVP scope items
- User journey steps → these imply capabilities

### 2. Generate Functional Requirements

For each capability area identified from scope and journeys:

#### FR Format
```markdown
**FR-[AREA]-###**: [Actor] [capability]
- **Input:** field1 (constraints), field2 (constraints)
- **Rules:** IF condition THEN action; business logic
- **Output:** success behavior
- **Error:** error case → handling
- **Log:** expected log message format (optional - include when output needs specific logging)
- **Depends:** FR-xxx (if any)
```

#### Area Codes
| Code | Domain |
|------|--------|
| AUTH | Authentication, authorization |
| USER | User management, profiles |
| DATA | Data storage, retrieval |
| PROC | Processing, transformation |
| FILE | File operations |
| API | External integrations |
| ADMIN | Administration, configuration |
| NOTIF | Notifications, messaging |

#### Quality Checks (Apply During Generation)
- Actor is explicit (User, System, Admin)
- Input has constraints (types, formats, limits)
- Rules capture business logic, not implementation
- Output is specific and testable
- Error handling is explicit
- Dependencies are noted

### 3. Generate Non-Functional Requirements

#### NFR Format (Single Line)
```markdown
**NFR-[CAT]-###**: [metric] [target] under [condition]
```

#### Categories
| Category | Examples |
|----------|----------|
| PERF | Response time, throughput, batch processing time |
| SEC | Encryption, authentication expiry, data protection |
| SCALE | Concurrent users, data volume, horizontal scaling |
| REL | Uptime, recovery time, data durability |

**Derive NFRs from:**
- Success metric (implies performance target)
- User type expectations (enterprise = stricter security)
- Product category (CLI = fast startup, API = low latency)

### 4. Generate Data Entities

Analyze FRs to identify implied data entities:

```markdown
## 5. Data Entities

| Entity | Key Attributes | Related FRs |
|--------|---------------|-------------|
| {Entity} | id, {attr1}, {attr2}, created_at | FR-xxx, FR-xxx |
```

**Derive from:**
- FR inputs (what data is needed)
- FR outputs (what data is created/modified)
- State changes mentioned in rules

### 5. Technology Constraints

Discuss with user:
- What technology decisions are already made? (non-negotiable)
- What can the implementing agent decide?

```markdown
## 6. Technology Constraints

**Decided (non-negotiable):**
- {language/framework if specified}
- {database if specified}
- {deployment target if specified}

**Open (agent can decide):**
- {implementation details}
```

If no constraints mentioned, note "No technology constraints specified."

### 6. Identify Implementation Reference Needs

Assess whether the project needs detailed implementation specifications in Section 8.

**Ask user about these indicators:**

| Indicator | Section Needed | Question |
|-----------|----------------|----------|
| User-editable config files | 8.1 Configuration Schema | "Will users configure the system via files (YAML, JSON, etc.)?" |
| Defined output formats | 8.2 Output Formats | "Does the system have specific console output, file formats, or API responses that must follow exact patterns?" |
| Error/status codes | 8.3 Error Code Catalog | "Will the system use coded errors (ERR_001) or status classifications (SUCCESS/FAILED)?" |
| Multi-step algorithms | 8.4 Algorithm Details | "Are there calculations, processing pipelines, or multi-step logic that need precise specification?" |
| Complex edge cases | 8.5 Examples & Edge Cases | "Are there tricky scenarios where examples would clarify expected behavior?" |

**For each "yes" answer:**
- Note which Section 8 sub-sections are needed
- Gather enough detail to populate those sections
- These become reference material for implementing agents

**If no implementation details needed:**
- Skip Section 8 entirely
- Note in PRD: "Section 8 not applicable - no complex implementation specs required"

### 7. Generate Quick Reference Table

Create summary table with all FRs:

```markdown
## 7. Quick Reference

| FR ID | Summary | Priority | Depends |
|-------|---------|----------|---------|
| FR-xxx | {brief summary} | {P0/P1/P2/P3} | {FR-xxx or -} |
```

**Priority Assignment:**
- P0-Critical: Blocks other FRs or is core to MVP
- P1-High: Must have for MVP
- P2-Medium: Should have for MVP
- P3-Low: Nice to have

### 8. Generate Implementation Reference (If Needed)

Based on Step 6 assessment, populate applicable Section 8 sub-sections:

**8.1 Configuration Schema** - Document structure, field types, validation rules
**8.2 Output Formats** - Exact console output, file formats, API response examples
**8.3 Error Code Catalog** - All error/warning codes with descriptions, causes, resolutions
**8.4 Algorithm Details** - Step-by-step logic for complex processing
**8.5 Examples & Edge Cases** - Concrete scenarios showing expected behavior

**Quality checks for Section 8:**
- Each sub-section has enough detail for implementation without guesswork
- Error codes cover all error cases mentioned in FRs
- Output formats match what FRs describe as output
- Algorithm steps align with FR rules

### 9. Integrated Validation

Validate before completion:

| Check | Requirement |
|-------|-------------|
| FR Count | At least 3 FRs for MVP scope items |
| FR Format | All FRs have Input, Rules, Output, Error |
| FR Coverage | Each MVP scope item has at least 1 FR |
| Journey Coverage | Each journey step maps to at least 1 FR |
| NFR Count | At least 2 NFRs (PERF + one other) |
| NFR Format | All NFRs are single-line with metric/target/condition |
| Entities | At least 1 entity per major FR area |
| Dependencies | All `Depends:` references exist |
| Quick Reference | All FRs in table with priority |
| Section 8 | If applicable, all identified sub-sections populated with sufficient detail |

**If validation fails:** Fix issues before proceeding.

### 10. Present to User

Show the user:
1. Summary: "Generated X FRs across Y areas, Z NFRs, W entities"
2. Key dependencies identified
3. Any assumptions made

Ask for feedback on:
- Missing capabilities?
- Priority adjustments?
- Constraint clarifications?
- Implementation details need more depth?

### 11. Report & Menu

**Menu:**

**[C] Continue** - Proceed to Complete (Step 4)
**[R] Revise** - Modify requirements, add missing capabilities
**[D] Deep Dive** - Apply advanced elicitation on complex requirements

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-03-requirements'`), then load and execute `{nextStepFile}`.

**On [R]:** Make specific changes, re-validate, return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore complex requirements, edge cases, or business rules more thoroughly. After deep dive, update requirements with insights and return to menu.

---

## SUCCESS CRITERIA

- FRs generated with Input/Rules/Output/Error format (+ optional Log field)
- NFRs generated in single-line format
- Data Entities table created
- Technology Constraints documented
- Quick Reference table complete
- Implementation Reference (Section 8) assessed and populated if needed
- All validations pass
- User confirmed requirements before proceeding
