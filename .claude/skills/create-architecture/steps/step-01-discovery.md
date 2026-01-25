---
name: 'step-01-discovery'
description: 'Discover PRD, extract constraints, select technology stack'
nextStepFile: './step-02-structure.md'
outputFile: '{planning_artifacts}/architecture.md'
templateFile: '{installed_path}/architecture-decision-template.md'
---

# Step 1: Discovery & Technology Selection

**Progress:** Step 1 of 3 → Next: Structure & Patterns

**Goal:** Locate PRD, extract technology constraints, and select the complete technology stack.

---

## Instructions

### 1. Discover PRD

Search for PRD in: `{planning_artifacts}/**`, `{output_folder}/**`, `docs/**`
Pattern: `*prd*.md` or `prd.md`

**If not found:** "Architecture requires a PRD. Please provide the path or run `/prd-create` first."

**If found:** Read completely, confirm with user:
> "Found PRD: [path]. Creating architecture for [project name]. Continue?"

---

### 2. Extract from PRD

Read and extract:

| PRD Section | Extract |
|-------------|---------|
| Section 1 (Overview) | Project name, type (web app, API, mobile, etc.), **Greenfield/Brownfield** |
| Section 4 (NFRs) | Performance, security, scale requirements |
| Section 6 (Tech Constraints) | Decided (locked) vs Open (need selection) |

### 2b. Brownfield Detection

**If PRD Section 1 indicates Brownfield:**

1. Search for Project Charter: `docs/project-charter*.md`
2. If found, read Section 7 (Brownfield Context) for:
   - Existing systems and their disposition (Replace/Integrate/Migrate From)
   - Legacy data migration requirements
   - Technical constraints from legacy systems

3. Search for related documents:
   - Integration spec: `docs/integration-spec*.md` (from `/analyze-integrations`)
   - Data migration plan: `docs/data-migration*.md` (from `/create-data-migration`)
   - Security architecture: `docs/security-architecture*.md` (from `/create-security-architecture`)

4. Inform user of brownfield context:
> "This is a **brownfield project** integrating with existing systems:
> - {list existing systems and dispositions}
> - {note any legacy constraints}
>
> I'll include a Legacy Integration section in the architecture. Continue?"

---

### 3. Select Technology Stack

**For each "Open" decision in PRD Section 6:**

1. Match project type to recommendations:
   - Load `{data_files_path}/project-types.csv` for typical starters
   - Use web search: "[technology] latest stable version 2026"

2. Select technology that aligns with:
   - PRD constraints (Section 6 Decided items)
   - NFR requirements (Section 4)
   - Ecosystem compatibility

3. Document rationale briefly

**Categories (fill all that apply):**

| Category | Selection Inputs |
|----------|------------------|
| Framework | Project type + PRD hints |
| Database | Data complexity (Section 5) + scale (Section 4) |
| ORM | Framework ecosystem |
| Auth | Security requirements (Section 4) |
| Styling | Frontend needs (if applicable) |
| Testing | Framework ecosystem |

**Decision Rule:** If PRD clearly implies one choice, select it. Only ask user if multiple equally valid options exist—then present top 2 with your recommendation.

---

### 4. Initialize Architecture Document

1. Copy `{templateFile}` to `{outputFile}`
2. Fill header:
   - `{{project_name}}` from PRD Section 1
   - `{{date}}` = today
   - `{{prd_path}}` = path to PRD
3. Fill **Technology Stack** table with all selections
4. **If Brownfield:**
   - Check the "Brownfield" checkbox in Section 8
   - Fill Existing Systems table
   - Document Legacy Constraints
   - Note Coexistence Strategy
5. Add frontmatter state:
   ```yaml
   ---
   status: in-progress
   current_step: 1
   prd_source: [path]
   prd_checksum: [first 8 chars of sha256 hash of PRD content]
   project_type: greenfield | brownfield
   legacy_systems: [list if brownfield, empty if greenfield]
   ---
   ```

   The `prd_checksum` enables detection if PRD has changed since architecture was created.

---

### 5. Checkpoint

Present to user:
- Technology stack table (versions + rationale)
- Any decisions where alternatives were considered

**Menu:**
- **[C] Continue** - Proceed to Step 2: Structure
- **[R] Revise** - Adjust technology selections
- **[P] Party Mode** - Discuss stack decisions with architect/dev agents
- **[D] Deep Dive** - Analyze decisions with advanced elicitation methods
- **[X] Exit** - Save progress and stop

**On [P] Party Mode:**
Invoke `_party-mode` skill with:
- `topic`: "Technology stack decisions for [project name]"
- `content`: Technology stack table + PRD constraints summary
- `focus_agents`: `architect`, `dev`

After party mode completes, return to this checkpoint with insights applied.

**On [D] Deep Dive:**
Invoke `_deep-dive` skill with:
- `content`: Technology stack table + rationale
- `focus_area`: "Technology stack validation"
- `content_type`: "architecture"

Recommended method categories: `technical`, `risk`, `competitive`

After deep dive completes, return to this checkpoint with enhancements applied.

**On Continue:** Update frontmatter `current_step: 2`, load `{nextStepFile}`
