---
name: 'step-02-generate'
description: 'Generate user documentation'
outputFile: '{project_root}/docs/user-guide.md'
template: '../user-guide.template.md'
---

# Step 2: Generate

**Progress:** Step 2 of 2 → Final Step

**Goal:** Generate the complete user documentation.

---

## Instructions

### 1. Create Document

Copy `{template}` to `{outputFile}` and populate all sections.

---

### 2. Writing Guidelines

**Tone:**
- Friendly but professional
- Action-oriented ("Click" not "You should click")
- Assume no prior knowledge

**Format:**
- Use numbered steps for procedures
- Use bullet points for lists
- Include expected outcomes ("You'll see...")
- Bold key UI elements

**Examples:**
```
Good: "Click **Submit** to save your changes."
Bad: "The user should then proceed to click on the Submit button."

Good: "You'll see a confirmation message."
Bad: "A confirmation message will be displayed."
```

---

### 3. Validate Completeness

| Section | Required |
|---------|----------|
| Getting Started | What, who, how to access |
| Quick Start | First-time experience |
| How-To Guides | At least 3 common tasks |
| FAQ | At least 3 questions |
| Getting Help | Support contact |

---

### 4. Present Document

"**User Guide Generated**

**System:** {name}

**Coverage:**
- How-to guides: {count}
- FAQ entries: {count}
- Troubleshooting: {count}

Review the document. Any gaps to fill?"

---

### 5. Finalize

**Menu:**
```
[V] View → Display full document
[R] Revise → Make changes
[X] Exit → Complete
```

**On [X]:**

Update frontmatter:
```yaml
stepsCompleted: ['step-01-discovery', 'step-02-generate']
completedAt: '{timestamp}'
```

**Completion Message:**
"User guide saved to `{outputFile}`.

**Adoption checklist:**
- [ ] Review with sample users
- [ ] Test all procedures
- [ ] Publish to user-accessible location
- [ ] Announce to users
- [ ] Plan for updates as system evolves

**Next steps:**
- Run `/create-runbook` for support team docs
- Run `/create-change-request` when ready to deploy"
