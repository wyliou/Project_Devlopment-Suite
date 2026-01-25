---
name: 'step-02-design'
description: 'Create security architecture with patterns and controls'

# File references
outputFile: '{project_root}/docs/security-architecture.md'
deepDiveSkill: '{skills_dir}/_deep-dive/skill.md'
partyModeSkill: '{skills_dir}/_party-mode/skill.md'
---

# Step 2: Design

**Progress: Step 2 of 2** - Final Step

## STEP GOAL

Design comprehensive security architecture covering authentication, authorization, data protection, network security, and audit controls based on the assessment from Step 1.

## EXECUTION RULES

- **Hybrid step** - design based on context + user validation
- You are a Security Architect - create specific, implementable controls
- All controls must map to compliance requirements identified in Step 1
- Consider both security and usability

## SEQUENCE (Follow Exactly)

### 1. Load Context

Read `{outputFile}` to get security context from Step 1:
- Data classification
- Compliance requirements
- Threat model
- Existing infrastructure

### 2. Design Authentication Architecture

Based on context, design authentication:

**Present Design:**
"**Authentication Architecture:**

**Recommended Method:** [SSO/OAuth2/SAML/API Keys/MFA]
- Rationale: [Why this fits the requirements]

**Identity Provider:**
- Provider: [Okta/Azure AD/Auth0/Custom]
- Integration: [OIDC/SAML/LDAP]

**Session Management:**
- Session duration: [Recommended timeout]
- Token type: [JWT/Opaque/Session cookie]
- Refresh strategy: [Sliding window/Fixed expiry]

**MFA Requirements:**
- Required for: [Admin users/All users/Sensitive operations]
- Methods: [TOTP/Push notification/Hardware key]

Does this align with your requirements? Any changes?"

Wait for user confirmation before proceeding.

### 3. Design Authorization Architecture

**Present Design:**
"**Authorization Architecture:**

**Model:** [RBAC/ABAC/ACL]
- Rationale: [Why this fits]

**Role Definitions:**
| Role | Description | Key Permissions |
|------|-------------|-----------------|
| Admin | System administration | Full access |
| Manager | Team oversight | Read all, write own team |
| User | Standard access | Read/write own data |
| Viewer | Read-only | Read assigned resources |

**Permission Matrix:**
| Resource | Admin | Manager | User | Viewer |
|----------|-------|---------|------|--------|
| [Resource 1] | CRUD | CRU | CR | R |
| [Resource 2] | CRUD | R | R | - |

**Special Considerations:**
- [Data isolation requirements]
- [Cross-tenant access if applicable]

Does this authorization model fit your needs?"

Wait for user confirmation.

### 4. Design Data Protection

**Present Design:**
"**Data Protection:**

**Encryption at Rest:**
- Algorithm: AES-256-GCM
- Key management: [AWS KMS/Azure Key Vault/HashiCorp Vault]
- Key rotation: [Frequency]

**Encryption in Transit:**
- TLS Version: 1.3 (minimum 1.2)
- Certificate strategy: [Let's Encrypt/Corporate CA/Purchased]
- HSTS: Enabled

**Data Masking/Tokenization:**
| Data Type | Masking Rule | Storage |
|-----------|--------------|---------|
| SSN | Show last 4 only | Tokenized |
| Credit Card | PCI tokenization | External vault |
| Email | Full in DB, masked in logs | Encrypted |

**Data Retention:**
- Active data: [Retention period]
- Archived data: [Retention period]
- Deletion: [Soft delete/Hard delete/Anonymization]

Any adjustments needed?"

Wait for user confirmation.

### 5. Design Network Security

**Present Design:**
"**Network Security:**

**Network Boundaries:**
- Public tier: [CDN, Load balancer]
- Application tier: [App servers - private subnet]
- Data tier: [Database - isolated subnet]

**Firewall Rules:**
| Source | Destination | Port | Protocol | Action |
|--------|-------------|------|----------|--------|
| Internet | Load Balancer | 443 | HTTPS | Allow |
| Load Balancer | App Servers | 8080 | HTTP | Allow |
| App Servers | Database | 5432 | PostgreSQL | Allow |
| * | * | * | * | Deny |

**API Gateway Security:**
- Rate limiting: [Requests per minute]
- Request validation: [Schema validation enabled]
- WAF rules: [OWASP Core Rule Set]

**DDoS Protection:**
- [Cloud provider DDoS/Cloudflare/Custom]

Any network constraints I should account for?"

Wait for user confirmation.

### 6. Design Audit & Monitoring

**Present Design:**
"**Audit & Monitoring:**

**Audit Logging:**
| Event Category | Events Logged | Retention |
|----------------|---------------|-----------|
| Authentication | Login, logout, failed attempts | 2 years |
| Authorization | Permission changes, access denials | 2 years |
| Data Access | Read/write of sensitive data | 7 years |
| Admin Actions | Config changes, user management | 7 years |

**Log Format:**
- Timestamp, user ID, action, resource, result, IP address, user agent

**Security Monitoring:**
- SIEM integration: [Splunk/ELK/Azure Sentinel]
- Alert thresholds:
  - Failed logins: 5 in 5 minutes -> Alert
  - Privilege escalation: Any -> Alert
  - Data exfiltration: >1000 records -> Alert

**Incident Response Hooks:**
- Alert channels: [PagerDuty/Slack/Email]
- Escalation path: [L1 -> L2 -> Security team]
- Automated responses: [Account lockout, IP blocking]

Does this monitoring approach meet compliance needs?"

Wait for user confirmation.

### 7. Create Security Controls Matrix

**Present Summary:**
"**Security Controls Matrix:**

| Control | Requirement | Implementation | Status |
|---------|-------------|----------------|--------|
| Authentication | [Compliance req] | [Chosen method] | Planned |
| MFA | [Compliance req] | [Chosen method] | Planned |
| Authorization | [Compliance req] | [Chosen model] | Planned |
| Encryption at Rest | [Compliance req] | AES-256 | Planned |
| Encryption in Transit | [Compliance req] | TLS 1.3 | Planned |
| Audit Logging | [Compliance req] | [Chosen SIEM] | Planned |
| Access Reviews | [Compliance req] | Quarterly | Planned |

This matrix will be used by `/security-checklist` to validate implementation."

### 8. Update Document

Update `{outputFile}` with all security architecture sections:

- Replace *Pending* sections with actual designs
- Add Security Controls Matrix
- Update frontmatter: `stepsCompleted: ['step-01-assess', 'step-02-design']`
- Update document status to "Complete"

### 9. Report & Menu

**Report:**
"Security architecture complete for {project_name}.

**Coverage:**
- ✅ Authentication Architecture
- ✅ Authorization Architecture
- ✅ Data Protection
- ✅ Network Security
- ✅ Audit & Monitoring
- ✅ Security Controls Matrix

**Key Decisions:**
- Authentication: [Summary]
- Authorization: [Summary]
- Encryption: [Summary]

**Next Steps:**
1. Run `/create-architecture` - Security decisions inform technology choices
2. Later, run `/security-checklist` to validate implementation

Document saved at `{outputFile}`"

**Menu:**

**[R] Revise** - Make changes to any section
**[D] Deep Dive** - Explore specific area with advanced techniques
**[P] Party Mode** - Get security team perspectives
**[X] Exit** - Workflow complete

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on selected section. Update document, return to menu.

**On [P]:** Invoke `/_party-mode` with security personas. Update document, return to menu.

---

## SUCCESS CRITERIA

- All five security architecture sections completed
- Controls mapped to compliance requirements
- Security Controls Matrix created
- User validated each section
- Document updated with complete architecture
- Clear integration point with `/create-architecture`
