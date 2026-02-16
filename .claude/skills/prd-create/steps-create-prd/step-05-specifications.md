---
name: 'step-05-specifications'
description: 'Generate Tech Constraints, NFRs, Data Entities, and Implementation Reference'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-06-complete.md'
validationChecks: '{skills_root}/_prd-data/validation-checks.md'
---

# Step 5: Specifications

**Progress: Step 5 of 6** - Next: Complete

## STEP GOAL

Generate all derived and complementary specifications: Technology Constraints, Non-Functional Requirements, Data Entities, and Implementation Reference (Section 7). Tech constraints are gathered first because they inform NFR targets and data entity decisions.

## EXECUTION RULES

- **Interactive step** — requires user feedback
- You are a Product Analyst — deriving specifications from established FRs
- Each sub-section builds on FR analysis from step 4

## SEQUENCE (Follow Exactly)

### 1. Technology Constraints

Discuss with user:
- What technology decisions are already made? (non-negotiable)
- What can the implementing agent decide?

**Brownfield integration:** If brownfield project (from Section 1 Classification):
- Legacy APIs → document as integration points
- Legacy databases → document as decided constraints
- Existing infrastructure → document deployment constraints

```markdown
## 6. Technology Constraints

**Decided (non-negotiable):**
- {language/framework if specified}
- {database if specified}
- {deployment target if specified}

**Open (agent can decide):**
- {implementation details}
```

**Include Integration Points if applicable:**
```markdown
### Integration Points
| System | Direction | Data/Purpose | Auth Method |
|--------|-----------|--------------|-------------|
| {system} | In/Out/Both | {data flow} | {auth} |
```

**Include Compliance Notes if applicable:**
```markdown
### Compliance Notes
{regulatory or policy requirements, or "N/A"}
```

If no constraints mentioned, note "No technology constraints specified."

Update the PRD Section 6 with technology constraints.

### 2. Generate Non-Functional Requirements

Derive NFRs from the combination of success metrics, actor types, FR analysis, and **the tech constraints just captured** (which inform realistic NFR targets). Select NFR categories relevant to the project context — e.g., API services typically need PERF and SEC; web apps need PERF, ACC, and COMPAT.

**Every NFR must include a measurable metric, specific target, and condition.** Vague NFRs like "system should be fast" are not acceptable — rewrite until measurable.

#### NFR Format (Categorized with Single-Line Entries)
```markdown
## 4. Non-Functional Requirements

### Performance
- **NFR-PERF-001**: [metric] [target] under [condition]

### Reliability
- **NFR-REL-001**: [metric] [target] under [condition]
```

#### Categories
| Category | Examples |
|----------|----------|
| PERF | Response time, throughput, batch processing time |
| SEC | Encryption, authentication expiry, data protection |
| SCALE | Concurrent users, data volume, horizontal scaling |
| REL | Uptime, recovery time, data durability |
| ACC | WCAG compliance level, screen reader support, keyboard navigation |
| USE | Task completion rate, learning curve, error recovery |
| MAINT | Code coverage, dependency freshness, deployment frequency |
| COMPAT | Browser support, OS support, API version compatibility |

Select categories relevant to the project — not all apply to every project type. PERF and at least one other are typically required.

**Present draft NFRs to user and ask for feedback.**

Update the PRD Section 4 with generated NFRs.

### 3. Generate Data Entities

Check if Section 5 is applicable: refer to `{validationChecks}` Section Requirements table. If the project type lists Section 5 as Optional and the FRs imply no persistent storage, ask the user: "Section 5 (Data Entities) appears optional for this project. Include it? [Y/N]"

If applicable, analyze FRs to identify implied data entities:

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
- Relationships implied by FR dependencies

**Present entity table to user.** Ask: "Any entities missing? Any attributes to add?"

Update the PRD Section 5 with generated entities.

### 4. Assess Implementation Reference (Section 7)

**First:** Check for `_Section 7 Notes (Temporary)` in the PRD. If present, use these notes as the starting material — they contain implementation details already confirmed with the user during deepening.

Then assess which sub-sections add value based on FR analysis and these notes (algorithms, error codes, format specifications discovered in user answers).

Available sub-sections: Configuration Schema, Output Formats, Error Code Catalog, Algorithm Details, Examples & Edge Cases. Project-specific sub-sections can be added too.

**Quality criteria** (from prd-purpose.md):
- Algorithm steps must be ordered and unambiguous — an AI agent should reproduce the same logic from the description alone
- Error codes must map to specific FR error conditions
- Config schemas must specify types, defaults, and valid ranges
- Examples must show both typical cases and boundary/edge cases

Present your recommendation to the user. For each approved sub-section, gather detail to populate it. If none needed, note "Section 7 not applicable" in the PRD.

**After writing Section 7:** Remove the `_Section 7 Notes (Temporary)` section from the PRD if it exists — its content has been incorporated into the final Section 7.

### 5. Present & Menu

**Before presenting**, verify inline (fix issues during generation, not as a separate pass):
- At least 2 NFRs (PERF + one other), each with metric + target + condition
- Entity Related FRs exist in Section 3
- Decided and Open sections present in Tech Constraints
- Section 7 sub-sections meet quality criteria if applicable

Show the user:
1. Technology Constraints summary
2. NFR summary (count by category)
3. Data Entities summary (or "not applicable")
4. Section 7 status (applicable sections or "not needed")

**Menu:**

**[C] Continue** - Proceed to Complete (Step 6)
**[R] Revise** - Modify specifications
**[X] Exit** - Save progress and stop
*Always available: **[P] Party Mode** | **[D] Deep Dive***

**On [P] Party Mode return:** Review the agents' recommendations. For each actionable item, ask the user: "The agents suggested {X}. Apply this change? [Y/N]" Apply approved changes, then return to this menu.

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-05-specifications'`), then load and execute `{nextStepFile}`.
