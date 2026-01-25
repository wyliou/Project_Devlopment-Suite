---
name: security-checklist
description: Enterprise security validation checklist
---

# Security Checklist Workflow

**Goal:** Validate security requirements against enterprise standards and OWASP guidelines.

**Your Role:** Security analyst reviewing the project for security compliance.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Assess** | Gather security context, identify risks |
| 2 | **Generate** | Create security checklist with findings |

---

## OUTPUT FORMAT

```markdown
# Security Checklist: {system_name}

## Summary
- Risk Level: Low / Medium / High
- Findings: X critical, Y warning, Z info

## Authentication & Authorization
- [ ] Check items

## Data Protection
- [ ] Check items

## Input Validation
- [ ] Check items

## API Security
- [ ] Check items

## Infrastructure
- [ ] Check items

## Compliance
- [ ] Check items

## Findings & Recommendations
- Detailed findings with remediation
```

---

## SECURITY DOMAINS

| Domain | Focus |
|--------|-------|
| Authentication | How users prove identity |
| Authorization | What users can access |
| Data Protection | Encryption, PII handling |
| Input Validation | Injection prevention |
| API Security | Endpoint protection |
| Logging & Monitoring | Audit trails |
| Infrastructure | Hosting, network security |
| Compliance | Regulatory requirements |

---

## Execution

Load and execute `./steps/step-01-assess.md` to begin.
