---
name: 'step-01-discovery'
description: 'Identify users, tasks, and documentation needs'
nextStepFile: './step-02-generate.md'
outputFile: '{project_root}/docs/user-guide.md'
template: '../user-guide.template.md'
---

# Step 1: Discovery

**Progress:** Step 1 of 2 → Next: Generate

**Goal:** Understand users and their tasks to create relevant documentation.

---

## Instructions

### 1. Check for Context

Look for existing documents:
- `docs/prd.md` - user types, journeys, features
- `docs/ux-design.md` - user flows, interface details
- `docs/project-charter.md` - user goals, pain points

Extract user information and key tasks.

---

### 2. System Basics

"Let's create user documentation.

**Basic Information:**
- What's the system name?
- How do users access it? (URL, app, etc.)
- How do users log in? (SSO, credentials)"

---

### 3. Users

"Who are the users?

For each user type:
- What's their role?
- What's their primary goal?
- What's their technical comfort level?"

---

### 4. Key Tasks

"What are the main things users need to do?

List the top 5-7 tasks in order of frequency:
1. Most common task
2. Second most common
3. etc.

For each, what's the basic flow?"

---

### 5. Gotchas & Confusion

"What trips users up?

- Common mistakes?
- Confusing terminology?
- Non-obvious features?
- Things that work differently than expected?"

---

### 6. FAQ

"What questions do users frequently ask?

Think about:
- 'How do I...?'
- 'Why can't I...?'
- 'What does X mean?'
- 'Who do I contact for...?'"

---

### 7. Support

"How do users get help?

- Who do they contact?
- What channels? (email, chat, ticket)
- Are there training resources?"

---

### 8. Confirm & Proceed

**Summary:**
"User guide will cover:

- System: {name}
- User types: {count}
- How-to guides: {count} tasks
- FAQ: {count} questions
- Troubleshooting: {count} issues

Ready to generate?"

**Menu:**
```
[C] Continue → Generate document
[R] Revise → Add more details
```

**On [C]:** Update frontmatter, load and execute `{nextStepFile}`.
