---
name: 'step-02-discovery'
description: 'Gather vision, problem, solution, and users through focused conversation'
nextStepFile: './step-03-scope.md'
outputFile: '{project_root}/docs/project-charter.md'
---

# Step 2: Discovery

**Progress:** Step 2 of 4 → Next: Scope

**Goal:** Extract vision, problem, solution, and users through focused conversation.

---

## Instructions

### 1. Opening Question

Start with a focused opening:

"Let's define what you're building.

**Tell me in 2-3 sentences:**
- What problem are you solving?
- Who has this problem?"

Wait for response.

---

### 2. Problem Clarification

Based on response, dig deeper on the problem:

"What happens today when someone faces this problem? What do they do?"

**Listen for:**
- Current workarounds
- Pain intensity
- Frequency of problem

If vague, push: "Can you give me a specific example?"

---

### 3. Solution Extraction

Once problem is clear:

"How does your solution fix this? What's different about your approach?"

**Listen for:**
- Core capability
- Key differentiators
- Why existing solutions fall short

---

### 4. User Identification

Clarify who the users are:

"Who are the main users? Are there different types with different needs?"

**Build a simple table:**

| User Type | Primary Goal | Pain Points |
|-----------|--------------|-------------|

---

### 5. Greenfield vs Brownfield Detection

Determine project type:

"Is this a completely new system (greenfield) or does it replace/integrate with existing systems (brownfield)?"

**If Brownfield, ask:**

"Tell me about the existing systems:
- What systems are you replacing or integrating with?
- Is there legacy data that needs to be migrated?
- Who are the current users and what workflows might be disrupted?"

**Build brownfield context if applicable:**

| System | Role | Disposition |
|--------|------|-------------|
| {name} | {what it does} | Replace / Integrate / Migrate From |

---

### 6. Update Document

Update `{outputFile}` with Vision, Users, Project Type, and Brownfield sections:

**Section 1: Vision**
```markdown
## 1. Vision

### Problem Statement
{2-3 sentences from conversation}

### Solution Overview
{2-3 sentences from conversation}

### Key Differentiators
- {differentiator 1}
- {differentiator 2}
```

**Section 2: Users**
```markdown
## 2. Users

| User Type | Primary Goal | Pain Points |
|-----------|--------------|-------------|
| {type} | {goal} | {pain} |
```

**Section 6: Project Type**
```markdown
## 6. Project Type

| Attribute | Value |
|-----------|-------|
| **Type** | {Greenfield / Brownfield} |
| **Category** | {Web App / API / Mobile / Desktop / CLI} |
```

**Section 7: Brownfield Context (if brownfield)**
```markdown
## 7. Brownfield Context (If Applicable)

### Existing Systems
| System | Role | Disposition |
|--------|------|-------------|
| {system} | {role} | {Replace / Integrate / Migrate From} |

### Legacy Data
- **Data to migrate:** {description}
- **Data quality concerns:** {issues or "None known"}
- **Migration strategy:** {Big Bang / Phased / Parallel Run}

### Current Users & Workflows
- **Affected users:** {count and types}
- **Critical workflows:** {workflows that cannot be disrupted}

### Technical Constraints from Legacy
- {constraint 1}
- {constraint 2}
```

---

### 7. Validate & Menu

Present what was captured:

"Here's what I captured:

**Problem:** {1-sentence summary}
**Solution:** {1-sentence summary}
**Users:** {list user types}
**Project Type:** {Greenfield/Brownfield}
{If brownfield: **Existing Systems:** {list systems and dispositions}}

Does this look right?"

**Menu:**
```
[C] Continue → Scope (Step 3)
[R] Revise → Make changes
```

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-02-discovery'`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

---

## Quality Checks

Before proceeding:
- Problem is specific (not vague)
- Solution addresses the problem directly
- At least 1 user type with clear goal
- Differentiators are real (not "better" or "faster")
- Project type identified (Greenfield/Brownfield)
- If Brownfield: existing systems documented with disposition
