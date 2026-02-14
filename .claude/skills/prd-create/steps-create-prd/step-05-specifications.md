---
name: 'step-05-specifications'
description: 'Generate Tech Constraints, NFRs, Data Entities, and Implementation Reference'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-06-complete.md'
projectTypesCSV: '{skills_root}/_prd-data/project-types.csv'
---

# Step 5: Specifications

**Progress: Step 5 of 6** - Next: Complete

## STEP GOAL

Generate all derived and complementary specifications: Technology Constraints, Non-Functional Requirements, Data Entities, and Implementation Reference (Section 8). Tech constraints are gathered first because they inform NFR targets and data entity decisions.

## EXECUTION RULES

- **Interactive step** — requires user feedback
- You are a PRD Creator — deriving specifications from established FRs
- **One question at a time:** Ask a single focused question, wait for the answer, then ask the next. Never batch multiple questions into one message.
- Each sub-section builds on FR analysis from step 4
- **Compose-then-write principle:** Gather all information for a section before writing it to the document.

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

Derive NFRs from the combination of success metrics, actor types, product category, FR analysis, and **the tech constraints just captured** (which inform realistic NFR targets).

Load `{projectTypesCSV}` and use the matching product category row to recommend relevant NFR categories. For example, API services typically need PERF and SEC; web apps need PERF, ACC, and COMPAT.

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

**Derive NFRs from:**
- Success metrics (implies performance target)
- Actor type expectations (enterprise = stricter security)
- Product category (CLI = fast startup, API = low latency)
- FR analysis (data volume from entities, processing from rules)
- Tech constraints captured above (infrastructure limits, compliance requirements)

**Present draft NFRs to user and ask for feedback.** Adjust based on response.

Update the PRD Section 4 with generated NFRs.

### 3. Generate Data Entities

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
- Relationships implied by FR dependencies

**Present entity table to user.** Ask: "Any entities missing? Any attributes to add?"

Update the PRD Section 5 with generated entities.

### 4. Assess Implementation Reference (Section 8)

Now that FRs are complete, assess whether the project needs detailed implementation specifications.

**Agent-assessed recommendation:** Analyze the FRs and product category to determine which sub-sections add value. Present your assessment to the user in one exchange:

```
Based on the requirements, I recommend including:
- 8.1 Configuration Schema — [reason from FR analysis]
- 8.3 Error Code Catalog — [reason from FR analysis]

Not needed:
- 8.2 Output Formats — [reason]
- 8.4 Algorithm Details — [reason]
- 8.5 Examples & Edge Cases — [reason]

Agree? Any adjustments?
```

**Assessment signals by project type:**

| Sub-section | Signal |
|-------------|--------|
| 8.1 Configuration Schema | FRs reference configurable settings, environment setup, or user preferences |
| 8.2 Output Formats | FRs describe specific report formats, file exports, structured console output, or API response schemas |
| 8.3 Error Code Catalog | FRs have many error cases, or product needs consistent error reporting (APIs, CLI tools) |
| 8.4 Algorithm Details | FRs contain multi-step processing, calculations, scoring, or ranking logic |
| 8.5 Examples & Edge Cases | FRs have complex conditional rules where examples clarify intent |

**Extensibility note:** Sub-sections 8.1-8.5 are the common set. Project-specific sub-sections can be added as needed (e.g., Deployment Procedures, Monitoring Requirements, Data Retention Policies, Migration Procedures). Ask the user if any project-specific sections would be valuable.

**For each recommended sub-section:** Gather detail from user to populate it.

**If no sub-sections needed:** Skip Section 8 entirely. Note in PRD: "Section 8 not applicable."

Update the PRD Section 8 with implementation reference (if applicable).

### 5. Present & Menu

**Before presenting**, verify inline (fix issues during generation, not as a separate pass):
- At least 2 NFRs (PERF + one other), single-line format
- Entity Related FRs exist in Section 3
- Decided and Open sections present in Tech Constraints
- Section 8 sub-sections populated if applicable

Verification order matches the new sequence: Tech Constraints → NFRs → Data Entities → Section 8.

Show the user:
1. Technology Constraints summary
2. NFR summary (count by category)
3. Data Entities summary
4. Section 8 status (applicable sections or "not needed")

**Menu:**

**[C] Continue** - Proceed to Complete (Step 6)
**[R] Revise** - Modify specifications
**[P] Party Mode** - Multi-agent review of NFRs, tech constraints, and entities
**[D] Deep Dive** - Apply advanced elicitation on NFRs, entities, or implementation details
**[X] Exit** - Save progress and stop

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-05-specifications'`), then load and execute `{nextStepFile}`.

**On [R]:** Make specific changes, return to menu.

**On [P]:** Invoke `/_party-mode` skill with topic "Specifications review for [project name]", content = Sections 4, 5, 6, 8, focus_agents = `architect`, `qa`, `devops`. After discussion, apply insights and return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore complex specifications more thoroughly. After deep dive, update with insights and return to menu.

**On [X]:** Exit workflow. Do NOT mark this step as complete — document changes are preserved but the step must be re-run on resume to verify completeness.

---

## SUCCESS CRITERIA

- Technology Constraints documented first (Decided + Open, brownfield integration if applicable)
- NFRs generated in single-line format with measurable targets, informed by tech constraints
- CSV-driven NFR category recommendations applied
- Data Entities table created with FR mappings
- Section 8 assessed with extensibility consideration and populated if needed
- Step-scoped validation passes
- User confirmed specifications before proceeding
