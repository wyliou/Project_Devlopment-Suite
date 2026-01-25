---
name: 'step-02-generate'
description: 'Generate runbook document'
outputFile: '{project_root}/docs/runbook.md'
template: '../runbook.template.md'
---

# Step 2: Generate

**Progress:** Step 2 of 2 → Final Step

**Goal:** Generate the complete runbook document.

---

## Instructions

### 1. Create Document

Copy `{template}` to `{outputFile}` and populate all sections.

---

### 2. Validate Completeness

Essential sections for support handoff:

| Section | Required |
|---------|----------|
| Quick Reference | Contact info, escalation |
| System Overview | Purpose, dependencies |
| Health Checks | At least 1 method |
| Common Procedures | Start/stop/restart, logs |
| Troubleshooting | At least 2 common issues |
| Contacts | Primary + escalation path |

Flag gaps for user to complete.

---

### 3. Format Commands

Ensure all commands are:
- Copy-pasteable
- Include environment variables clearly marked
- Have expected output noted where helpful

---

### 4. Present Document

"**Runbook Generated**

**System:** {name}
**Owner:** {team}

**Coverage:**
- Health checks: {count}
- Procedures: {count}
- Troubleshooting guides: {count}
- Contacts: {count}

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
"Runbook saved to `{outputFile}`.

**Handoff checklist:**
- [ ] Review with support team
- [ ] Verify procedures work
- [ ] Add to team knowledge base
- [ ] Schedule periodic review/updates

**Next steps:**
- Run `/create-user-docs` for end-user documentation
- Run `/create-change-request` when ready to deploy"
