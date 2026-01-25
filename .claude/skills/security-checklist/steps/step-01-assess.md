---
name: 'step-01-assess'
description: 'Assess security context and identify risks'
nextStepFile: './step-02-generate.md'
outputFile: '{project_root}/docs/security-checklist.md'
template: '../security-checklist.template.md'
---

# Step 1: Assess

**Progress:** Step 1 of 2 → Next: Generate

**Goal:** Understand the security context and identify potential risks.

---

## Instructions

### 1. Load Context

Look for existing documents:
- `docs/prd.md` - NFRs, data entities, user types
- `docs/architecture.md` - tech stack, infrastructure
- `docs/integration-spec.md` - external connections

Extract security-relevant information.

---

### 2. System Classification

"Let's assess security requirements.

**Basic Classification:**
- What type of data does this system handle?
  - Public
  - Internal
  - Confidential
  - Restricted/PII

- Who are the users?
  - Internal employees only
  - External customers
  - Both

- What's the business criticality?
  - Low (inconvenience if down)
  - Medium (business impact if down)
  - High (significant business impact)
  - Critical (cannot operate without)"

---

### 3. Authentication

"How do users authenticate?

- SSO (which provider)?
- Username/password?
- API keys?
- Certificates?

Any MFA requirements?"

---

### 4. Data Handling

"What sensitive data is involved?

- PII (names, emails, SSN)?
- Financial data?
- Health information?
- Credentials/secrets?

How is it stored and transmitted?"

---

### 5. Integrations

"What external systems does this connect to?

For each:
- How does it authenticate?
- What data is exchanged?
- Is the connection encrypted?"

---

### 6. Compliance

"Any regulatory requirements?

- SOX (financial controls)?
- HIPAA (health data)?
- GDPR (EU personal data)?
- PCI-DSS (payment cards)?
- Internal security policies?"

---

### 7. Known Concerns

"Any specific security concerns?

- Previous security issues?
- High-risk features?
- Areas of uncertainty?"

---

### 8. Risk Assessment

Based on gathered information, determine initial risk level:

| Factor | Risk Indicator |
|--------|----------------|
| PII/Sensitive data | Higher |
| External users | Higher |
| Payment processing | Higher |
| Internet-facing | Higher |
| Integrations with sensitive systems | Higher |
| Internal only, low sensitivity | Lower |

---

### 9. Confirm & Proceed

**Summary:**
"Security Assessment Summary:

- **Data Classification:** {classification}
- **User Base:** {internal/external}
- **Compliance:** {requirements}
- **Initial Risk Level:** {Low/Medium/High}

**Focus Areas:**
- {area 1}
- {area 2}

Ready to generate security checklist?"

**Menu:**
```
[C] Continue → Generate checklist
[R] Revise → Add more context
```

**On [C]:** Update frontmatter, load and execute `{nextStepFile}`.
