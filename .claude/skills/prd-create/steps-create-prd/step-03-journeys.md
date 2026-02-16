---
name: 'step-03-journeys'
description: 'Journeys/workflows and capability mapping with priority'

# File references
nextStepFile: '{skill_base}/steps-create-prd/step-04-requirements.md'
validationChecks: '{skills_root}/_prd-data/validation-checks.md'
---

# Step 3: Journeys & Capability Mapping

**Progress: Step 3 of 6** - Next: Requirements

## STEP GOAL

Document journeys/workflows for each actor type and build the capability mapping with priorities. This creates the foundation for FR generation in step 4.

## EXECUTION RULES

- **Interactive step** — requires user feedback on journeys and capability areas
- You are a Product Analyst — mapping actor flows to system capabilities

## SEQUENCE (Follow Exactly)

### 1. Check Section Applicability

Read the product category from Section 1 Classification. Refer to the `{validationChecks}` Section Requirements table to determine if Section 2 is Required, Recommended, or Optional for this project type.

If Section 2 is optional, ask the user: "Section 2 (Journeys) is optional for {category} projects. Include it? [Y/N]"
If skipped, note "Section 2: Not applicable for {category}" in the PRD and proceed directly to capability mapping (step 3).

### 2. Journeys/Workflows

For each actor type identified in Section 1, propose a draft journey based on the vision and scope, then ask the user to confirm or refine. Work through one actor type at a time.

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

1. **Check Section 3 headers** in the PRD for existing `### Area` headers
   - If present: use as starting point (already user-approved from a previous session)
   - If absent: derive from scope items + journey steps

2. **Build coverage map** — verify every scope item maps to a capability area and vice versa. If gaps are found, propose new capability areas to cover unmapped scope items and ask the user to confirm.

3. **Brownfield-Specific Capability Areas:** Brownfield context discovered in step 2 is stored in Section 1 under `### Brownfield Context` (per the template). Reference this section when adding brownfield-specific capability areas below and when informing tech constraints in step 5.

   If brownfield project detected in Section 1, ask the user which of these apply (one at a time):
   - **Data Migration** — "Do you need to migrate legacy data to the new system?"
   - **Legacy Compatibility** — "Do you need to maintain interfaces with systems not yet replaced?"
   - **Transition Management** — "Do you need a managed cutover period?"
   Add only the areas the user confirms.

### 4. Write to Document

After gathering all information, write to the PRD:

1. **Write Section 2** (Journeys/Workflows) — or note "Not applicable for {category}" if skipped
2. **Verify capability areas are reflected in Section 3** as `### Area` headers

### 5. Report & Menu

**Report:**
- Journeys gathered (count by actor type)
- Capability areas mapped with priorities
- Coverage summary (scope items → capability areas)

**Menu:**

**[C] Continue** - Proceed to FR Generation (Step 4)
**[R] Revise** - Modify journeys or capability areas
**[X] Exit** - Save progress and stop
*Always available: **[P] Party Mode** | **[D] Deep Dive***

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-03-journeys'`), then load and execute `{nextStepFile}`.
