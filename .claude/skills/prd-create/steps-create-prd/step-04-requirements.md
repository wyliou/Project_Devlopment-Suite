---
name: 'step-04-requirements'
description: 'FR generation, completeness verification, and deepening'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-05-specifications.md'
---

# Step 4: Functional Requirements

**Progress: Step 4 of 6** - Next: Specifications

## STEP GOAL

Generate Functional Requirements from the capability mapping established in step 3, verify completeness, and deepen each FR through focused Q&A.

## EXECUTION RULES

- **Interactive step** — requires user feedback on requirements
- You are a Product Analyst — generating AI-optimized requirements
- Apply FR Quality Criteria from prd-purpose.md during generation: explicit actor, constrained inputs, business-logic-only rules, testable output, exhaustive errors, boundary conditions, state transitions, data flow direction
- This step handles FRs only — do NOT generate NFRs, Data Entities, or Tech Constraints here

## SEQUENCE (Follow Exactly)

### 1. Generate Functional Requirements

For each capability area from Section 3's `### Area` headers:

#### FR Format
```markdown
### {Capability Area Name}

**FR-001**: [Actor] [capability]
- **Input:** field1 (type, format constraint, validation rule), field2 (type, constraints)
- **Rules:** IF condition THEN action; ELSE alternative. Express as business logic, not implementation.
- **Output:** Observable result. What changes in system state? What does the actor see?
- **Error:** trigger condition → handling; second condition → handling. Be exhaustive.
- **Depends:** FR-xxx (if any)
- **Priority:** Must
```

Default from capability area priority. User can adjust per-FR during deepening.

FRs are grouped under `### Capability Area Name` section headers. The header carries the domain context — IDs are sequential (`FR-001`, `FR-002`, ...).

**For large projects (15+ FRs):** Area-based IDs (`FR-AUTH-001`) are acceptable if the user prefers them. The capability area is still in the section header regardless of ID format.

Each FR receives a Priority field (Must/Should/Could) defaulting from its capability area. Override per-FR during deepening if needed.

Match detail depth to project context from Section 1 Classification — enterprise gets exhaustive detail, prototypes get essentials only. The Input/Rules/Output/Error **format** is always used; what changes is the **depth** within each field.

### 2. Present Draft & Completeness Verification

Present the generated FRs to the user grouped by capability area. Then produce a completeness summary:

**"Generated X FRs across Y capability areas, Z gaps found."**

Every scope item and journey step must map to at least 1 FR. Show coverage matrix on request.

Ask the user: "Review the draft FRs above. Any missing capabilities, wrong groupings, or FRs to remove before we proceed to deepening?"

**If gaps found (by agent or user):** Generate additional FRs or adjust, then re-verify coverage.

### 2b. Granularity Check

Before deepening, review each FR for single-responsibility:
- Does the FR contain two distinct algorithms or processes?
- Could the FR's Input/Rules be split into independent operations?
- Would an implementing agent naturally build this as two separate functions?

If any FR does double duty, recommend splitting and get user approval BEFORE deepening begins. Splitting after deepening wastes work.

### 3. FR Deepening Pass

After the user approves the draft (including any granularity splits), **deepen each FR one at a time** through focused Q&A. This is where FRs gain the precision needed for AI-agent implementation.

#### Deepening Scope Selection

Present the user with scope options to manage conversation length:

"Now I can deepen each FR with targeted questions to improve implementation precision. This typically takes 1-3 exchanges per FR.

**Deepening strategy:**
**[All]** Deepen every FR (~{X*2} exchanges)
**[Area]** Select capability areas to deepen (e.g., "Authentication and Data Processing")
**[Skip]** Skip deepening, proceed to writing"

If user selects [Area]: Present the capability area list with FR counts per area. User selects one or more areas. Deepen only FRs under those area headers. Remaining FRs keep their draft state.

If user selects [All] and FR count > 15: Warn "This will take 30+ exchanges. Consider [Area] for a focused pass. Continue with All? [Y/N]"

#### Deepening Process

For each FR in the selected scope:
1. Identify the most important gap or ambiguity (e.g., missing algorithm detail, unclear boundary condition, unspecified error handling)
2. Ask **one question** about that gap
3. Wait for the user's answer
4. If the answer reveals further gaps in the same FR, ask the next question
5. When the FR is sufficiently specified, move to the next FR

Probe for: algorithms, boundary conditions, data flow specifics, error handling, configuration vs hardcoded decisions.

**Real data examination:** When the project has existing data, config files, or source code, proactively examine them to inform your questions. Real-world patterns are more reliable than hypothetical scenarios. If the user suggests checking real data, always do so.

**Efficient absorption:** If the user provides comprehensive detail that fully addresses the FR's gaps, acknowledge it, confirm understanding, and move to the next FR. Do not ask additional questions just to fill an expected exchange count.

#### Section 7 Discovery Capture

When the user's answer reveals implementation-level detail (algorithms, error codes, format specs, config schemas), append it immediately to a running Section 7 notes block at the bottom of the PRD:

```markdown
## _Section 7 Notes (Temporary)
- **Algorithm: {topic} ({FR-ID})** — {details}
- **Error Code: {code} ({FR-ID})** — {details}
- **Format: {topic} ({FR-ID})** — {details}
```

Step 5 consumes and replaces this temporary section with the final Section 7/8. Do not write Section 7 proper yet.

### 4. Write to Document

**Now write all gathered content to the PRD at once:**
1. Write Section 3 (Functional Requirements) with all deepened FRs

This batch write ensures Section 3 is never left in a partial state.

### 5. Report & Menu

Show the user:
1. Summary: "Generated X FRs across Y capability areas (Z Must, W Should, V Could)"
2. Coverage summary (gaps or complete)
3. Key dependencies identified
4. Any assumptions made

**Menu:**

**[C] Continue** - Proceed to Specifications (Step 5)
**[R] Revise** - Modify requirements
**[X] Exit** - Save progress and stop
*Always available: **[P] Party Mode** | **[D] Deep Dive***

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-04-requirements'`), then load and execute `{nextStepFile}`.

**On [R]:** Make requested changes. New FRs get the next sequential ID (never insert in the middle). If deleting a FR, update its dependents. Re-verify coverage after changes, return to menu.
