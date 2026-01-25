---
name: 'step-01-init'
description: 'Initialize PRD workflow - detect state, discover inputs, setup document'

# File references
nextStepFile: './step-02-discovery.md'
continueStepFile: './step-01b-continue.md'
outputFile: '{project_root}/docs/prd.md'
prdTemplate: '../../_prd-data/prd-template.md'
prdPurpose: '../../_prd-data/prd-purpose.md'
---

# Step 1: Init

**Progress: Step 1 of 4** - Next: Discovery

## STEP GOAL

Detect workflow state, discover input documents, and setup PRD document.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a PRD Creator - a product-focused facilitator
- Focus on setup - no content creation yet

## SEQUENCE (Follow Exactly)

### 1. Load Standards

Load and read `{prdPurpose}` to understand PRD Guidelines philosophy.

### 2. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` + missing `step-04-complete` | → Load `{continueStepFile}` (auto-proceed) |
| File exists + NO `stepsCompleted` (unmanaged) | → Safeguard Protocol |
| File not exists | → Fresh Setup |

### 3. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing PRD at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `prd_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 4. Fresh Setup

#### A. Discover Input Documents

Search locations: `{product_knowledge}/**`, `docs/**`

| Type | Pattern |
|------|---------|
| Product Brief | `*brief*.md` or `*brief*/index.md` |
| Research | `*research*.md` or `*research*/index.md` |
| Project Docs | Other `.md` files in search locations |

**Detect Project Type:**
- Scan for source code (`src/**/*.py`, `**/*.js`, etc.)
- Source found → **Brownfield**
- No source → **Greenfield**

**Report discoveries to user and ask for confirmation before loading.**

#### B. Validate & Load Files

Before loading:
1. Verify each confirmed file exists
2. If missing files, present options: [S]kip / [P]rovide path / [A]bort
3. Verify `{prdTemplate}` exists
4. Load all confirmed files completely (no offset/limit)

#### C. Create Document

- Copy `{prdTemplate}` to `{outputFile}`
- Initialize frontmatter with `inputDocuments` array and `stepsCompleted: []`

### 5. Report & Menu

**Report:**
- Document created/migrated
- Input documents loaded (with counts by type)
- Project type (Brownfield/Greenfield)

**Menu:**

**[C] Continue** - Proceed to Discovery (Step 2)
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-init']`), then load and execute `{nextStepFile}`.

---

## SUCCESS CRITERIA

- Workflow state detected correctly
- Input documents discovered and loaded
- PRD document created or migrated
- User confirmed setup before proceeding
