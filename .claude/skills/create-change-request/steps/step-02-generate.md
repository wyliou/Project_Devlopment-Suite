---
name: 'step-02-generate'
description: 'Generate change request document'
outputFile: '{project_root}/docs/change-request.md'
template: '{skill_base}/change-request.template.md'
---

# Step 2: Generate

**Progress:** Step 2 of 2 → Final Step

**Goal:** Generate the complete change request document.

---

## Instructions

### 1. Generate CR Number

Format: `CR-{YYYYMMDD}-{seq}`

Example: `CR-20240115-001`

---

### 2. Create Document

Copy `{template}` to `{outputFile}` and populate all sections.

---

### 3. Validate Completeness

Check all required fields:

| Section | Required |
|---------|----------|
| Summary table | All fields |
| Description | Clear and specific |
| Business Justification | Links to approved project |
| Impact Assessment | All areas addressed |
| Implementation Plan | Steps with owners and times |
| Rollback Plan | Trigger + steps defined |
| Testing Summary | All relevant tests |
| Communication Plan | At least 1 audience |

Flag any gaps for user to complete.

---

### 4. Risk Assessment

Based on gathered information, assess risks:

| Factor | Risk Level |
|--------|------------|
| First deployment of this type | Higher |
| Multiple systems affected | Higher |
| Data migration involved | Higher |
| Downtime required | Higher |
| No rollback possible | Higher |
| Standard/routine change | Lower |
| Zero downtime deployment | Lower |
| Isolated system | Lower |

---

### 5. Present Document

Display the complete CR to user.

"**Change Request Generated**

**CR Number:** {cr_number}

**Summary:**
- System: {system}
- Type: {type}
- Date: {date}
- Risk Level: {Low/Medium/High}

**Checklist:**
- [ ] Implementation plan reviewed
- [ ] Rollback plan tested
- [ ] Communications scheduled
- [ ] Approvals identified

Review the document. Any adjustments needed?"

---

### 6. Finalize

**Menu:**
```
[V] View → Display full document
[R] Revise → Make changes
[X] Exit → Complete
```

**On [X]:**

Update frontmatter:
```yaml
stepsCompleted: ['step-01-gather', 'step-02-generate']
completedAt: '{timestamp}'
crNumber: '{cr_number}'
```

**Completion Message:**
"Change request saved to `{outputFile}`.

**Next steps:**
1. Review with deployment team
2. Get business owner approval
3. Submit to CAB for review
4. Schedule deployment window
5. Execute communication plan

Good luck with your deployment!"
