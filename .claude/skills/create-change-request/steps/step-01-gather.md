---
name: 'step-01-gather'
description: 'Gather change details, impact assessment, and deployment plan'
nextStepFile: '{skill_base}/steps/step-02-generate.md'
outputFile: '{project_root}/docs/change-request.md'
template: '{skill_base}/change-request.template.md'
---

# Step 1: Gather

**Progress:** Step 1 of 2 → Next: Generate

**Goal:** Gather all information needed for the change request.

---

## Instructions

### 1. Check for Context

Look for existing documents:
- `docs/prd.md` - system details, requirements
- `docs/architecture.md` - technical details
- `docs/integration-spec.md` - affected integrations

Extract relevant information to pre-fill where possible.

---

### 2. Change Basics

"Let's create a change request for your deployment.

**Basic Information:**
- What system is being changed?
- What type of change? (Standard/Normal/Emergency)
- When do you want to deploy?
- What's the priority? (Low/Medium/High/Critical)"

---

### 3. Description

"Describe what's being changed in 2-3 sentences.

What will be different after this deployment?"

---

### 4. Impact Assessment

"Let's assess the impact:

1. **Users:** How many users affected? Which groups?
2. **Downtime:** Any downtime required? How long?
3. **Systems:** What other systems are affected?
4. **Data:** Any data migrations or schema changes?
5. **Integrations:** Any integrations impacted?"

---

### 5. Implementation Plan

"Walk me through the deployment steps:

1. What happens before deployment? (backups, notifications)
2. What are the actual deployment steps?
3. How do you verify it worked?
4. Any post-deployment tasks?"

---

### 6. Rollback Plan

"If something goes wrong:

1. What triggers a rollback decision?
2. How do you roll back?
3. How long do you have to decide? (rollback window)"

---

### 7. Testing Status

"What testing has been completed?

- Unit tests?
- Integration tests?
- UAT sign-off?
- Performance testing?
- Security scan?"

---

### 8. Communication

"Who needs to know about this change?

- End users?
- Support team?
- Stakeholders?

How and when will they be notified?"

---

### 9. Confirm & Proceed

**Summary:**
"Change Request Summary:

- **System:** {system}
- **Type:** {type}
- **Date:** {date}
- **Downtime:** {downtime}
- **Rollback:** {available/defined}

Ready to generate the CR document?"

**Menu:**
```
[C] Continue → Generate document
[R] Revise → Adjust details
```

**On [C]:** Update frontmatter, load and execute `{nextStepFile}`.
