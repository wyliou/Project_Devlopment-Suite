---
name: 'step-01-discovery'
description: 'Gather operational details and procedures'
nextStepFile: './step-02-generate.md'
outputFile: '{project_root}/docs/runbook.md'
template: '../runbook.template.md'
---

# Step 1: Discovery

**Progress:** Step 1 of 2 → Next: Generate

**Goal:** Gather all operational information needed for the runbook.

---

## Instructions

### 1. Check for Context

Look for existing documents:
- `docs/architecture.md` - system components, dependencies
- `docs/integration-spec.md` - connected systems
- `docs/prd.md` - system purpose, NFRs

Extract relevant operational details.

---

### 2. System Basics

"Let's create a runbook for your system.

**Basic Information:**
- What's the system name?
- What team owns it?
- What support tier handles it? (L1/L2/L3)
- Who's on-call or primary contact?"

---

### 3. Health & Monitoring

"How do we know if the system is healthy?

- How to check if it's running?
- What metrics matter? (CPU, memory, response time, etc.)
- What are normal vs. concerning values?
- Is there a monitoring dashboard?"

---

### 4. Common Procedures

"What are the routine operations?

- How to start/stop/restart?
- Where are the logs?
- How to check configuration?
- Any cache clearing or maintenance tasks?"

---

### 5. Troubleshooting

"What commonly goes wrong?

For each issue:
- What are the symptoms?
- How do you diagnose it?
- How do you fix it?
- When should support escalate?"

---

### 6. Dependencies & Integrations

"What external systems does this depend on?

- Databases?
- APIs?
- Authentication services?
- What happens if each is down?"

---

### 7. Backup & Recovery

"What's the backup situation?

- What's backed up and how often?
- How do you restore?
- What's the target recovery time?"

---

### 8. Escalation

"Who gets called when?

- L1 can't resolve → who?
- Critical issue → who?
- After hours → who?"

---

### 9. Confirm & Proceed

**Summary:**
"Runbook will cover:

- System: {name}
- Owner: {team}
- Health checks: {count} metrics
- Procedures: {count} documented
- Troubleshooting: {count} issues
- Contacts: {count} people

Ready to generate?"

**Menu:**
```
[C] Continue → Generate document
[R] Revise → Add more details
```

**On [C]:** Update frontmatter, load and execute `{nextStepFile}`.
