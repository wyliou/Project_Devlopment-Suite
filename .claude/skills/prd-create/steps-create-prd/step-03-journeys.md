---
name: 'step-03-journeys'
description: 'Journeys/workflows and capability mapping with priority'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-04-requirements.md'
---

# Step 3: Journeys & Capability Mapping

**Progress: Step 3 of 6** - Next: Requirements

## STEP GOAL

Document journeys/workflows for each actor type and build the capability mapping with priorities. This creates the foundation for FR generation in step 4.

## EXECUTION RULES

- **Interactive step** — requires user feedback on journeys and capability areas
- You are a PRD Creator — mapping actor flows to system capabilities
- **One question at a time:** Ask a single focused question, wait for the answer, then ask the next. Never batch multiple questions into one message.
- **Compose-then-write principle:** Gather all journey information and build the complete capability mapping before writing to the document.

## SEQUENCE (Follow Exactly)

### 1. Check Section Applicability

Read the product category from Section 1 Classification and determine which sections apply. Refer to the validation-checks.md Section Requirements table.

**Section 2 (Journeys/Workflows):**
- **Required for:** Web App, Mobile, Full Stack App, Data Pipeline, ML Model/Service, Microservices System
- **Recommended for:** Infrastructure/IaC, Plugin/Extension, Prototype/MVP
- **Optional for:** API Service, CLI Tool, Library/SDK

If Section 2 is optional for this project type, ask the user: "Section 2 (Journeys) is optional for {category} projects. Include it? [Y/N]"
If skipped, note "Section 2: Not applicable for {category}" in the PRD and proceed directly to capability mapping.

**Note:** Even when Section 2 is skipped, the section format adapts by project type (Command Workflows for CLI, Integration Scenarios for Library, etc.) when included.

### 2. Journeys/Workflows

Gather journeys/workflows for each actor type identified in Section 1. Each actor type should have at least one journey with 3-5 steps.

**Adapt Section 2 format to product category:**

| Product Category | Section 2 Format |
|-----------------|------------------|
| Web App / Mobile / Desktop | **User Journeys** — 3-5 step flows per actor type |
| API Service | **API Consumer Journeys** — request/response flows, briefer |
| CLI Tool | **Command Workflows** — command sequences with expected outputs |
| Library/SDK | **Integration Scenarios** — code usage patterns showing typical integration |
| Data Pipeline | **Data Workflows** — data flow from source to destination per pipeline |
| ML Model/Service | **Training/Inference Workflows** — model lifecycle flows |
| Infrastructure/IaC | **Operational Workflows** — provisioning, scaling, recovery flows |
| Microservices System | **Service Interaction Flows** — cross-service request flows |
| Plugin/Extension | **Extension Scenarios** — plugin lifecycle and interaction patterns |
| Full Stack App | **User Journeys** — end-to-end flows spanning frontend and backend |
| Prototype/MVP | **User Journeys** — simplified, 2-3 steps |

**Journey Validation:**
- At least 1 journey per actor type
- 3-5 steps each (2-3 for prototypes)
- Brownfield projects: must include a migration/transition journey if legacy data or users exist

**If validation fails:** Ask targeted questions to fill gaps.

### 3. Capability Mapping

Build the capability area mapping from scope items and journey steps:

1. **Check frontmatter `capabilityAreas` array** in the PRD
   - If populated: use as starting point (already user-approved from a previous session)
   - If empty: derive from scope items + journey steps

2. **Build coverage map** to verify completeness:

```markdown
| Scope Item | Capability Area | Capabilities | Journey References |
|------------|----------------|--------------|-------------------|
| {scope item 1} | {area name} | {what the system must do} | {journey step refs} |
| {scope item 2} | {area name} | {what the system must do} | {journey step refs} |
```

3. **Cross-reference:** Flag scope items without a capability area, and capability areas with no scope items.

4. **Brownfield-Specific Capability Areas:** If brownfield project detected in Section 1, ask the user which of these apply (one at a time):
   - **Data Migration** — "Do you need to migrate legacy data to the new system?"
   - **Legacy Compatibility** — "Do you need to maintain interfaces with systems not yet replaced?"
   - **Transition Management** — "Do you need a managed cutover period?"
   Add only the areas the user confirms.

5. **Prioritize Capability Areas:** Assign `[Must]`, `[Should]`, or `[Could]` to each area:
   - **Must** — Core functionality required for MVP. Build fails without these.
   - **Should** — Important functionality expected in production. Can be deferred to a later batch if necessary.
   - **Could** — Nice-to-have. Only build if time/budget allows.

   Explain to user: "Priority tags inform build batch ordering — Must areas are implemented first."

6. **Present to user for confirmation** — only if changes were made or areas were derived fresh. If using the persisted list unchanged, briefly confirm and proceed.

### 4. Write to Document

After gathering all information, write to the PRD:

1. **Write Section 2** (Journeys/Workflows) — or note "Not applicable for {category}" if skipped

```markdown
## 2. Journeys/Workflows

### {Actor Type}: {Journey Name}
1. {Step 1} → {Step 2} → {Step 3} → {Outcome}
```

2. **Persist `capabilityAreas` to frontmatter:**

```yaml
capabilityAreas:
  - {name: 'Authentication', priority: 'Must'}
  - {name: 'User Management', priority: 'Should'}
  - {name: 'Reporting', priority: 'Could'}
```

### 5. Report & Menu

**Report:**
- Journeys gathered (count by actor type)
- Capability areas mapped with priorities
- Coverage summary (scope items → capability areas)

**Menu:**

**[C] Continue** - Proceed to FR Generation (Step 4)
**[R] Revise** - Modify journeys or capability areas
**[P] Party Mode** - Multi-agent review of journeys and capability mapping
**[D] Deep Dive** - Apply advanced elicitation on journeys or capability areas
**[X] Exit** - Save progress and stop

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-03-journeys'`), then load and execute `{nextStepFile}`.

**On [R]:** Make specific changes, return to menu.

**On [P]:** Invoke `/_party-mode` skill with topic "Journeys and capability mapping review for [project name]", content = Section 2 + capability mapping, focus_agents = `pm`, `architect`, `qa`. After discussion, apply insights and return to menu.

**On [D]:** Invoke `/_deep-dive` skill to explore journeys or capability areas more thoroughly. After deep dive, update with insights and return to menu.

**On [X]:** Exit workflow. Do NOT mark this step as complete — document changes are preserved but the step must be re-run on resume to verify completeness.

---

## SUCCESS CRITERIA

- Section applicability determined based on product category
- Journeys/workflows gathered for each actor type (adapted by product category)
- Brownfield projects include migration/transition journey (if applicable)
- Capability mapping built with priority tags and confirmed by user
- Capability areas persisted to frontmatter `capabilityAreas` array
- Every scope item maps to at least one capability area
- Section 2 written to document (or marked not applicable)
- User confirmed journeys and mapping before proceeding
