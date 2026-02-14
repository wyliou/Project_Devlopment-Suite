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

**Compose-then-write principle:** Generate all FRs and complete the deepening pass before writing Section 3 to the document.

## EXECUTION RULES

- **Interactive step** — requires user feedback on requirements
- You are a PRD Creator — generating AI-optimized requirements
- **One question at a time:** Ask a single focused question, wait for the answer, then ask the next. Never batch multiple questions into one message. This is especially important during FR deepening — go through each FR sequentially, asking one clarifying question per exchange.
- Apply quality checks during generation, not as separate step
- This step handles FRs only — do NOT generate NFRs, Data Entities, or Tech Constraints here

## SEQUENCE (Follow Exactly)

### 1. Generate Functional Requirements

For each capability area from the frontmatter `capabilityAreas` array:

#### FR Format
```markdown
### {Capability Area Name} [Must/Should/Could]

**FR-001**: [Actor] [capability]
- **Input:** field1 (type, format constraint, validation rule), field2 (type, constraints)
- **Rules:** IF condition THEN action; ELSE alternative. Express as business logic, not implementation.
- **Output:** Observable result. What changes in system state? What does the actor see?
- **Error:** trigger condition → handling; second condition → handling. Be exhaustive.
- **Depends:** FR-xxx (if any)
```

FRs are grouped under `### Capability Area Name [Priority]` section headers. The header carries the domain context and priority tag — IDs are sequential (`FR-001`, `FR-002`, ...).

**For large projects (15+ FRs):** Area-based IDs (`FR-AUTH-001`) are acceptable if the user prefers them. The capability area is still in the section header regardless of ID format.

#### Expanded Field-Level Guidance

| Field | Guidance |
|-------|----------|
| **Input** | List every field with type, format constraint, and validation rule. E.g., `email (string, RFC 5322, required, unique)` |
| **Rules** | Express as IF/THEN/ELSE business logic. Avoid implementation language (no "database", "API call"). Focus on what, not how. |
| **Output** | Describe observable result. What changes in system state? What does the actor see/receive? Must be testable. |
| **Error** | List each error case with `trigger condition → handling`. Be exhaustive — cover validation errors, authorization failures, state conflicts, resource limits. |
| **Depends** | Reference other FRs this requires. Only include if there's a true dependency. |

#### FR Depth Adaptation

Adapt detail level based on project context from Classification:

| Project Context | Depth Guidance |
|----------------|----------------|
| Enterprise / Production | Full detail — exhaustive input constraints, comprehensive error cases, precise validation rules |
| Consumer / Internal | Standard detail — key constraints and common error cases. Include important edge cases. |
| Prototype / MVP | Essential detail — primary constraints and primary error cases. Skip edge-case errors and granular validation rules. |

Derive the appropriate depth from the Classification context in Section 1 (Primary Context + Product Category).

The Input/Rules/Output/Error **format** is always used (downstream tools depend on it). What changes is the **depth** within each field.

#### Quality Checks (Apply During Generation)
- Actor is explicit (User, System, Admin, Operator)
- Input has constraints (types, formats, limits)
- Rules capture business logic, not implementation
- Output is specific and testable
- Error handling is explicit (exhaustive for enterprise; primary cases for prototypes)
- Dependencies are noted

### 2. FR Completeness Verification

After generating all FRs, produce a summary:

**"Generated X FRs across Y capability areas, Z gaps found."**

Show full coverage matrix on request only:

```markdown
| Scope Item | FRs | Coverage |
|------------|-----|----------|
| {scope item 1} | FR-xxx, FR-xxx | Complete / Partial / Missing |

| Journey Step | FRs | Coverage |
|--------------|-----|----------|
| {actor type}: {step} | FR-xxx | Complete / Partial / Missing |
```

**Every scope item must map to at least 1 FR.** Every journey step must map to at least 1 FR.

**If gaps found:** Generate additional FRs to fill coverage gaps before proceeding.

### 3. FR Deepening Pass

After initial FR generation and completeness verification, **deepen each FR one at a time** through focused Q&A with the user. This is where FRs gain the precision needed for AI-agent implementation.

#### Deepening Scope Selection

Present the user with scope options to manage conversation length:

"Generated {X} FRs. Now I can deepen each one with targeted questions to improve implementation precision. This typically takes 1-3 exchanges per FR.

**Deepening strategy:**
**[All]** Deepen every FR (~{X*2} exchanges)
**[Must]** Deepen Must-priority FRs only (faster, focuses on core)
**[Custom]** Select specific FRs to deepen
**[Skip]** Skip deepening, proceed to writing"

If user selects [All] and FR count > 15: Warn "This will take 30+ exchanges. Consider [Must] for a focused pass. Continue with All? [Y/N]"

#### Deepening Process

For each FR in the selected scope:
1. Identify the most important gap or ambiguity (e.g., missing algorithm detail, unclear boundary condition, unspecified error handling)
2. Ask **one question** about that gap
3. Wait for the user's answer
4. If the answer reveals further gaps in the same FR, ask the next question
5. When the FR is sufficiently specified, move to the next FR

**What to probe for (one question at a time):**
- Algorithms and detection logic (e.g., "How does the system detect where data rows end?")
- Boundary conditions and edge cases (e.g., "What happens if no rows match the threshold?")
- Data flow specifics (e.g., "Is matching case-sensitive or case-insensitive?")
- Error handling details (e.g., "Does validation stop at first error or report all?")
- Configuration vs hardcoded decisions (e.g., "Are these values configurable or fixed?")
- Real data validation (e.g., "Can I check the example files to verify this behavior?")

**Tip:** When available, examine real data/config files to inform questions. Concrete examples produce better answers than abstract questions.

### 4. Write to Document

**Now write all gathered content to the PRD at once:**
1. Write Section 3 (Functional Requirements) with all deepened FRs
2. Update Section 8 (Implementation Reference) with any new algorithms, error codes, or format specifications discovered during deepening

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
**[P] Party Mode** - Multi-agent review of requirements completeness and quality
**[D] Deep Dive** - Apply advanced elicitation on complex requirements
**[X] Exit** - Save progress and stop

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-04-requirements'`), then load and execute `{nextStepFile}`.

**On [R]:** Selective regeneration options:
1. **Specific FRs** — revise individual requirements (keep existing IDs)
2. **Entire capability area** — regenerate all FRs for an area (reassign IDs sequentially, update all `Depends:` references)
3. **Add new area** — add new capability area with FRs (start at next sequential ID, e.g., if last is FR-015, new area starts at FR-016)
4. **Delete area** — remove all FRs in the area, update dependencies in other areas
5. **Change priorities** — adjust Must/Should/Could tags (no renumbering)
6. **Adjust depth** — change FR detail level (no renumbering)

**FR ID rules during revision:** Never insert IDs in the middle. New FRs get the next sequential number. If deleting a FR that others depend on, update those dependencies. After any revision, re-verify coverage and update Quick Reference.

Make specific changes, re-verify coverage, return to menu.

**On [P]:** Invoke `/_party-mode` skill with topic "Requirements review for [project name]", content = Section 3 FRs + coverage summary, focus_agents = `pm`, `architect`, `dev`, `qa`. After discussion, apply insights and return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore complex requirements, edge cases, or business rules more thoroughly. After deep dive, update requirements with insights and return to menu.

**On [X]:** Exit workflow. Do NOT mark this step as complete — document changes are preserved but the step must be re-run on resume to verify completeness.

---

## SUCCESS CRITERIA

- FRs generated with Input/Rules/Output/Error format and priority tags on headers
- FR depth adapted to project context (enterprise/consumer/prototype)
- Every scope item maps to at least 1 FR
- Every journey step maps to at least 1 FR
- FR quality checks pass (explicit actors, constrained inputs, testable outputs, exhaustive errors)
- FRs deepened through focused Q&A (scope selected by user)
- Section 3 written to document
- Section 8 updated with algorithms/error codes from deepening (if any)
- User confirmed requirements before proceeding
