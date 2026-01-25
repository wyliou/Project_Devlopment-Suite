---
stepsCompleted: []
workflowType: 'security-checklist'
riskLevel: ''
---

# Security Checklist: {{system_name}}

**Date:** {{date}}
**Reviewer:** {{reviewer}}
**Version:** {{version}}

---

## Summary

| Item | Value |
|------|-------|
| **Overall Risk Level** | {{Low / Medium / High / Critical}} |
| **Critical Findings** | {{count}} |
| **Warnings** | {{count}} |
| **Passed Checks** | {{count}} |
| **Recommendation** | {{Approve / Approve with Conditions / Block}} |

---

## Authentication & Authorization

### Authentication
| Check | Status | Notes |
|-------|--------|-------|
| SSO/Enterprise auth used | ⬜ ✅ ❌ | {{notes}} |
| Password policy enforced (if applicable) | ⬜ ✅ ❌ N/A | {{notes}} |
| MFA available/required | ⬜ ✅ ❌ N/A | {{notes}} |
| Session timeout configured | ⬜ ✅ ❌ | {{notes}} |
| Secure session management | ⬜ ✅ ❌ | {{notes}} |
| Account lockout policy | ⬜ ✅ ❌ | {{notes}} |

### Authorization
| Check | Status | Notes |
|-------|--------|-------|
| Role-based access control | ⬜ ✅ ❌ | {{notes}} |
| Principle of least privilege | ⬜ ✅ ❌ | {{notes}} |
| Authorization checked server-side | ⬜ ✅ ❌ | {{notes}} |
| Sensitive functions protected | ⬜ ✅ ❌ | {{notes}} |

---

## Data Protection

### Data at Rest
| Check | Status | Notes |
|-------|--------|-------|
| Sensitive data encrypted | ⬜ ✅ ❌ N/A | {{notes}} |
| PII identified and protected | ⬜ ✅ ❌ N/A | {{notes}} |
| Database credentials secured | ⬜ ✅ ❌ | {{notes}} |
| Backups encrypted | ⬜ ✅ ❌ | {{notes}} |

### Data in Transit
| Check | Status | Notes |
|-------|--------|-------|
| HTTPS enforced | ⬜ ✅ ❌ | {{notes}} |
| TLS 1.2+ required | ⬜ ✅ ❌ | {{notes}} |
| Certificate valid and managed | ⬜ ✅ ❌ | {{notes}} |
| API calls encrypted | ⬜ ✅ ❌ | {{notes}} |

### Data Classification
| Check | Status | Notes |
|-------|--------|-------|
| Data classification defined | ⬜ ✅ ❌ | {{notes}} |
| Handling matches classification | ⬜ ✅ ❌ | {{notes}} |
| Retention policy defined | ⬜ ✅ ❌ | {{notes}} |

---

## Input Validation (OWASP Top 10)

| Check | Status | Notes |
|-------|--------|-------|
| SQL injection prevention | ⬜ ✅ ❌ N/A | {{Parameterized queries}} |
| XSS prevention | ⬜ ✅ ❌ N/A | {{Output encoding}} |
| CSRF protection | ⬜ ✅ ❌ N/A | {{Tokens used}} |
| Input validation (server-side) | ⬜ ✅ ❌ | {{notes}} |
| File upload restrictions | ⬜ ✅ ❌ N/A | {{notes}} |
| Command injection prevention | ⬜ ✅ ❌ N/A | {{notes}} |

---

## API Security

| Check | Status | Notes |
|-------|--------|-------|
| Authentication required | ⬜ ✅ ❌ | {{notes}} |
| Rate limiting implemented | ⬜ ✅ ❌ | {{notes}} |
| Input validation on all endpoints | ⬜ ✅ ❌ | {{notes}} |
| Error messages don't leak info | ⬜ ✅ ❌ | {{notes}} |
| API versioning | ⬜ ✅ ❌ | {{notes}} |
| CORS configured properly | ⬜ ✅ ❌ N/A | {{notes}} |

---

## Logging & Monitoring

| Check | Status | Notes |
|-------|--------|-------|
| Security events logged | ⬜ ✅ ❌ | {{Login, failures, changes}} |
| Logs don't contain sensitive data | ⬜ ✅ ❌ | {{No passwords, PII}} |
| Log retention meets requirements | ⬜ ✅ ❌ | {{notes}} |
| Alerting configured | ⬜ ✅ ❌ | {{notes}} |
| Audit trail for sensitive actions | ⬜ ✅ ❌ | {{notes}} |

---

## Infrastructure

| Check | Status | Notes |
|-------|--------|-------|
| Firewall configured | ⬜ ✅ ❌ | {{notes}} |
| Unnecessary ports closed | ⬜ ✅ ❌ | {{notes}} |
| Dependencies up to date | ⬜ ✅ ❌ | {{notes}} |
| Vulnerability scanning done | ⬜ ✅ ❌ | {{notes}} |
| Secrets management (no hardcoded) | ⬜ ✅ ❌ | {{notes}} |
| Environment separation | ⬜ ✅ ❌ | {{Dev/Test/Prod}} |

---

## Compliance

| Requirement | Applicable | Status | Notes |
|-------------|------------|--------|-------|
| SOX | ⬜ Yes ⬜ No | ⬜ ✅ ❌ | {{notes}} |
| HIPAA | ⬜ Yes ⬜ No | ⬜ ✅ ❌ | {{notes}} |
| GDPR | ⬜ Yes ⬜ No | ⬜ ✅ ❌ | {{notes}} |
| PCI-DSS | ⬜ Yes ⬜ No | ⬜ ✅ ❌ | {{notes}} |
| Internal Policy | ⬜ Yes ⬜ No | ⬜ ✅ ❌ | {{notes}} |

---

## Findings

### Critical

#### FIND-001: {{Finding Title}}
| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Category** | {{category}} |
| **Description** | {{what was found}} |
| **Risk** | {{what could happen}} |
| **Remediation** | {{how to fix}} |
| **Status** | Open / In Progress / Resolved |

---

### Warnings

#### FIND-002: {{Finding Title}}
| Field | Value |
|-------|-------|
| **Severity** | Warning |
| **Category** | {{category}} |
| **Description** | {{what was found}} |
| **Remediation** | {{how to fix}} |
| **Status** | Open |

---

## Recommendations

1. {{Priority recommendation}}
2. {{Second recommendation}}
3. {{Third recommendation}}

---

## Sign-Off

| Role | Name | Date | Decision |
|------|------|------|----------|
| Security Reviewer | | | |
| IT Security Lead | | | Approve / Reject |
| Project Manager | | | Acknowledged |

---

## Appendix

### Tools Used
- {{Security scanning tools}}

### References
- OWASP Top 10: https://owasp.org/Top10/
- {{Enterprise security policy link}}
