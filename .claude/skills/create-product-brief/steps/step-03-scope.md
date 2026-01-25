---
name: 'step-03-scope'
description: 'Define success metric, MVP scope, and context'
nextStepFile: '{skill_base}/steps/step-04-complete.md'
outputFile: '{project_root}/docs/project-charter.md'
---

# Step 3: Scope

**Progress:** Step 3 of 4 → Next: Complete

**Goal:** Define the ONE success metric, MVP scope boundaries, and relevant context.

---

## Instructions

### 1. Success Metric

Start with the most important question:

"What's the ONE metric that tells you this product is succeeding?

Not a list - the single most important number."

**Push for specificity:**
- "Users are happy" → "What behavior shows they're happy?"
- "Revenue" → "How much? By when?"
- "Adoption" → "How many users? Doing what?"

---

### 2. Supporting Indicators

Once the key metric is clear:

"What 2-3 other signals would support that metric?"

**These should be:**
- Leading indicators (predict success)
- Easily measurable
- Connected to user value

---

### 3. MVP Scope

Define boundaries:

"For the first version (MVP), what are the 3-5 core things it MUST do?"

Wait for response.

Then ask: "And what are you explicitly NOT doing in v1?"

**Goal:** Clear in/out scope that prevents scope creep.

---

### 4. Context

Gather relevant context:

"Any constraints I should know about?
- Technology preferences or requirements?
- Timeline?
- Domain-specific considerations?"

If none, that's fine - note "No specific constraints."

---

### 5. Update Document

Update `{outputFile}` with Success, MVP Scope, and Context sections:

**Section 3: Success**
```markdown
## 3. Success

### Key Success Metric
{THE ONE metric}

### Supporting Indicators
- {indicator 1}
- {indicator 2}
```

**Section 4: MVP Scope**
```markdown
## 4. MVP Scope

**In Scope:**
- {capability 1}
- {capability 2}
- {capability 3}

**Out of Scope:**
- {deferred 1}
- {deferred 2}
```

**Section 5: Context**
```markdown
## 5. Context

### Technology Preferences
{preferences or "No preferences"}

### Timeline
{timeline or "Flexible"}

### Domain Notes
{domain context or "None noted"}
```

---

### 6. Validate & Menu

Present summary:

"Here's the scope:

**Success Metric:** {metric}
**MVP In Scope:** {count} capabilities
**Out of Scope:** {count} items deferred

This brief is ready to feed into PRD creation."

**Menu:**
```
[C] Continue → Complete (Step 4)
[R] Revise → Make changes
```

**On [C]:** Update frontmatter (`stepsCompleted` add `'step-03-scope'`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

---

## Quality Checks

Before proceeding:
- Key Success Metric is ONE specific metric
- MVP scope has 3-5 in-scope items (not too many)
- Out of scope has at least 1 item (shows discipline)
- Success metric connects to user value
