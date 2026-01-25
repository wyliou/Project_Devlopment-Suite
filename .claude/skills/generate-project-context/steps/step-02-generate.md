---
name: 'step-02-generate'
description: 'Collaboratively generate context rules per category'
nextStepFile: './step-03-complete.md'
outputFile: '{project_root}/docs/project-context.md'
---

# Step 2: Generate Rules

**Progress:** Step 2 of 3 → Next: Complete

**Goal:** Collaboratively generate specific, critical rules for each category. Focus on unobvious details that AI agents might miss.

---

## Instructions

### Rule Categories

Generate rules for each category in sequence:

| # | Category | Focus |
|---|----------|-------|
| 1 | Language Rules | TypeScript/Python strict mode, imports, error handling |
| 2 | Framework Rules | React hooks, routing, state management patterns |
| 3 | Testing Rules | Test structure, mocks, coverage requirements |
| 4 | Code Quality | Naming, linting, documentation standards |
| 5 | Workflow Rules | Git, commits, PRs, deployment |
| 6 | Don't-Miss Rules | Anti-patterns, edge cases, security, performance |

**Skip categories not applicable** to the project's tech stack.

---

### Per-Category Process

For each category:

#### 1. Generate Draft Rules

Based on discovery findings, generate lean, specific rules:

```markdown
### [Category Name]

- **Rule 1:** Specific, actionable instruction
- **Rule 2:** Another specific instruction
- ...
```

**Content Guidelines:**
- Focus on unobvious rules agents might miss
- Use specific, actionable language
- Avoid obvious patterns agents already know
- Keep rules concise (1-2 sentences max)

#### 2. Present to User

Show draft rules:
```
[Category Name] Rules:

[Show markdown content]

What would you like to do?
```

#### 3. Category Menu

**Menu:**
- **[D] Deep Dive** - Explore nuanced rules with elicitation methods
- **[P] Party Mode** - Review from architect/dev perspectives
- **[C] Continue** - Save these rules, proceed to next category

---

### Enhancement Handlers

**On [D] Deep Dive:**
Invoke `_deep-dive` skill with:
- `content`: Current category rules
- `focus_area`: "[Category name] implementation rules"
- `content_type`: "project-context"

Recommended categories: `technical`, `risk`

After completion: Show enhanced rules, ask "Accept changes? [Y/N]"
- If Y: Update rules, return to D/P/C menu
- If N: Keep original, return to D/P/C menu

**On [P] Party Mode:**
Invoke `_party-mode` skill with:
- `topic`: "[Category name] rules for [project_name]"
- `content`: Current category rules + discovery context
- `focus_agents`: `architect`, `dev`

After completion: Show insights, ask "Accept changes? [Y/N]"
- If Y: Update rules, return to D/P/C menu
- If N: Keep original, return to D/P/C menu

**On [C] Continue:**
1. Append category content to `{outputFile}`
2. Update frontmatter: add category to `categories_completed`
3. Proceed to next category (or Step 3 if all complete)

---

### Category Content Format

When saving to file, use this structure:

```markdown
### [Category Name]

- **[Rule subject]:** Specific instruction
- **[Rule subject]:** Specific instruction
```

**Important:** Do not repeat top-level headers (`# Project Context` or `## Critical Implementation Rules`).

---

### Progress Tracking

After each category saved:
- Update frontmatter `categories_completed` array
- Show progress: "Completed [N] of 6 categories"

---

### Step Completion

After all applicable categories are complete:

**Menu:**
- **[C] Continue** - Proceed to Step 3: Complete
- **[R] Revise** - Go back and edit a category
- **[X] Exit** - Save progress and stop

**On Continue:** Update frontmatter `current_step: 3`, load `{nextStepFile}`
