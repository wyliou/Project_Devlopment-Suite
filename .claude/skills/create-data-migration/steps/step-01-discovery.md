---
name: 'step-01-discovery'
description: 'Identify source systems, data volumes, and mapping needs'

# File references
nextStepFile: './step-02-generate.md'
outputFile: '{project_root}/docs/data-migration.md'
---

# Step 1: Discovery

**Progress: Step 1 of 2** - Next: Generate

## STEP GOAL

Identify all source systems, understand data volumes, discover data quality issues, and establish mapping requirements for the migration.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a Data Migration Architect - gather inventory, don't design yet
- Focus on understanding what data exists and where

## SEQUENCE (Follow Exactly)

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` array | -> Resume workflow |
| File exists + NO `stepsCompleted` | -> Safeguard Protocol |
| File not exists | -> Fresh Setup |

### 2. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing data migration plan at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `data-migration_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 3. Fresh Setup

#### A. Gather Source System Inventory

**Opening:**
"Welcome! I'm your Data Migration Architect, ready to help plan your data migration.

Let's start by understanding your source systems:

**Source Systems:**
- How many source systems need data migrated?
- What type are they (SQL databases, NoSQL, flat files, APIs, legacy systems)?
- Are they on-premises or cloud-hosted?

**For each source system, I'll need:**
- System name and type
- Database/technology (Oracle, SQL Server, MySQL, MongoDB, etc.)
- Approximate number of tables/collections
- Estimated total data size
- Current data owner/steward"

#### B. Gather Data Volume Details

After initial responses, probe for details:

"Now let's understand the data volumes:

**For each source identified:**

| Source System | Question |
|---------------|----------|
| {Source 1} | What are the largest tables? Estimated row counts? |
| {Source 2} | How much historical data? How far back? |
| {Source 3} | What's the data growth rate (records per day/month)? |

**Data Relationships:**
- Are there relationships between source systems?
- Master data that exists in multiple places?
- Circular dependencies to be aware of?"

#### C. Gather Data Quality Context

"Let's discuss data quality:

**Known Issues:**
- Any known data quality problems (duplicates, missing values, inconsistencies)?
- Have there been past migration attempts? What went wrong?
- Data that needs cleansing or transformation?

**Business Rules:**
- Business rules embedded in source systems?
- Calculated fields or derived data?
- Timezone or currency considerations?

**Constraints:**
- Downtime windows available?
- Regulatory requirements for data handling?
- Data that cannot be migrated (must stay in legacy)?"

#### D. Gather Target System Context

"Finally, let's understand the target:

**Target System:**
- What is the target system/database?
- Is the schema defined, or do we need to design it?
- Any schema differences from source?

**Migration Approach:**
- Preference: Big Bang (all at once) vs Phased vs Parallel Run?
- Must legacy and new systems run simultaneously?
- Cutover window constraints?"

#### E. Confirm Discovery Scope

After user provides context, confirm understanding:

**Summary:**
"Let me confirm the migration scope:

**Source Systems:**
| System | Type | Tables | Est. Size | Priority |
|--------|------|--------|-----------|----------|
| [System 1] | [Type] | [#] | [Size] | [H/M/L] |
| [System 2] | [Type] | [#] | [Size] | [H/M/L] |

**Target System:**
- [Target description]
- Schema status: [Defined/To be designed]

**Migration Strategy:**
- Approach: [Big Bang/Phased/Parallel]
- Downtime window: [Duration]

**Known Challenges:**
- [List data quality issues]
- [List constraints]

**Data Relationships:**
- [Key relationships identified]

Anything to add or correct?"

#### F. Create Document

Create `{outputFile}` with initial structure:

```markdown
---
stepsCompleted: []
sourceSystems: [list]
targetSystem: [name]
migrationStrategy: [approach]
---

# Data Migration Plan: {project_name}

## Document Control
- **Status:** Draft
- **Created:** {date}
- **Last Updated:** {date}

## Migration Overview

### Source Systems
[Document each source system]

### Target System
[Document target system]

### Migration Strategy
[Document chosen approach and rationale]

### Constraints & Considerations
[Document downtime windows, regulatory requirements, etc.]

---
*Sections below to be completed in Step 2: Generate*
---

## Data Inventory
*Pending*

## Data Mapping
*Pending*

## Validation Rules
*Pending*

## Migration Sequence
*Pending*

## Rollback Plan
*Pending*

## Cutover Schedule
*Pending*
```

### 4. Report & Menu

**Report:**
- Document created at `{outputFile}`
- Source systems inventoried
- Migration approach identified
- Ready to create detailed migration plan

**Menu:**

**[C] Continue** - Proceed to Generate (Step 2)
**[R] Revise** - Discuss changes to inventory
**[D] Deep Dive** - Explore data quality issues deeper
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-discovery']`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on specific source system or data quality. Update document, return to menu.

---

## SUCCESS CRITERIA

- All source systems identified and documented
- Data volumes estimated for each source
- Target system documented
- Migration strategy selected
- Known data quality issues captured
- Constraints and downtime windows understood
- Document created with proper frontmatter
- User confirmed scope before proceeding
