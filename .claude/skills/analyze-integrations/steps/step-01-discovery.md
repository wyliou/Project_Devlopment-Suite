---
name: 'step-01-discovery'
description: 'Discover systems, data flows, and integration requirements'
nextStepFile: '{skill_base}/steps/step-02-document.md'
outputFile: '{project_root}/docs/integration-spec.md'
template: '{skill_base}/integration-spec.template.md'
---

# Step 1: Discovery

**Progress:** Step 1 of 2 → Next: Document

**Goal:** Identify all systems involved, data flows, and integration requirements.

---

## Instructions

### 1. Check for Context

Look for existing documents:
- `docs/stakeholder-research*.md` - may have system landscape
- `docs/project-charter.md` - may list affected systems
- `docs/prd.md` - may have integration requirements

If found, extract system information and confirm with user.

---

### 2. Opening

"Let's map out the integrations for your project.

**What existing systems will this project connect to?**

For each system, I need to understand:
- System name and purpose
- What data flows to/from it
- Who owns/manages it"

---

### 3. For Each System

Build a profile for each identified system:

"For **{system name}**:

1. **Direction:** Does data flow IN, OUT, or BOTH?
2. **What data?** What specific data is exchanged?
3. **How often?** Real-time, near-real-time, or batch?
4. **How?** API, file transfer, database, message queue?
5. **Auth?** How do we authenticate (SSO, API key, etc.)?
6. **Who owns it?** What team manages this system?
7. **How critical?** If this fails, what happens?"

---

### 4. Data Mapping

For each integration:

"What fields need to map between systems?

| Your System Field | {External System} Field | Any transformation? |
|-------------------|------------------------|---------------------|"

---

### 5. Dependencies

"Which integrations depend on others?

For example:
- Must user sync work before order sync?
- Are there systems that must be connected first?"

---

### 6. Risks

"What could go wrong with these integrations?

- Systems that are unreliable?
- Data quality concerns?
- Timing/sequencing issues?
- Access or permission challenges?"

---

### 7. Confirm & Proceed

**Summary:**
"Identified **{count}** integrations:

| System | Direction | Method | Critical? |
|--------|-----------|--------|-----------|
{table}

Ready to generate the integration spec?"

**Menu:**
```
[C] Continue → Generate document
[R] Revise → Add/modify systems
```

**On [C]:** Update frontmatter, load and execute `{nextStepFile}`.
