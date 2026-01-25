---
name: 'step-01-assess'
description: 'Gather security requirements, threats, and compliance needs'

# File references
nextStepFile: './step-02-design.md'
outputFile: '{project_root}/docs/security-architecture.md'
---

# Step 1: Assess

**Progress: Step 1 of 2** - Next: Design

## STEP GOAL

Gather comprehensive security context including data classification, compliance requirements, threat model, and existing security infrastructure.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a Security Architect - gather requirements, don't design yet
- Focus on understanding security constraints and threats

## SEQUENCE (Follow Exactly)

### 1. Check Workflow State

Check if `{outputFile}` exists and read it completely if found.

**Decision Tree:**

| Condition | Action |
|-----------|--------|
| File exists + has `stepsCompleted` array | -> Resume workflow |
| File exists + NO `stepsCompleted` | -> Safeguard Protocol |
| File not exists | -> Fresh Setup |

### 2. Safeguard Protocol (Unmanaged File)

If existing file has no `stepsCompleted` frontmatter:

**Inform user:** "Found existing security architecture at `{outputFile}` not created by this workflow."

**Options:**
- **[M] Migrate** - Add workflow metadata to existing file
- **[B] Backup** - Rename to `security-architecture_backup.md`, create fresh
- **[A] Abort** - Stop and let user handle manually

Wait for user choice before proceeding.

### 3. Fresh Setup

#### A. Gather Security Context

**Opening:**
"Welcome! I'm your Security Architect, ready to help define security patterns for your project.

Before I design security controls, I need to understand the security landscape:

**Data Classification:**
- What types of data will the system handle?
- Any PII (names, emails, addresses)?
- Any PHI (health information)?
- Any financial data (payment cards, bank accounts)?
- Any confidential business data?

**Compliance Requirements:**
- Are there regulatory requirements (GDPR, HIPAA, SOX, PCI-DSS)?
- Internal security policies to follow?
- Industry-specific standards?

**Existing Infrastructure:**
- Current identity provider (Okta, Azure AD, Auth0)?
- Existing security tools (SIEM, WAF, secrets management)?
- Network architecture constraints?"

#### B. Gather Threat Context

After initial responses, probe further:

"Now let's consider threats:

**User Context:**
- Who are the users (internal employees, external customers, both)?
- What access levels are needed?
- Any privileged users (admins, operators)?

**Threat Model:**
- What are the most valuable assets to protect?
- Who might want to attack this system (competitors, hackers, insiders)?
- What would be the impact of a breach (financial, reputational, regulatory)?

**Integration Points:**
- External APIs or services?
- Third-party data sharing?
- Legacy system connections?"

#### C. Confirm Security Scope

After user provides context, confirm understanding:

**Summary:**
"Let me confirm the security scope:

**Data Classification:**
- [List data types and sensitivity levels]

**Compliance Requirements:**
- [List applicable regulations/standards]

**Threat Profile:**
- Assets: [List key assets]
- Threat actors: [List potential attackers]
- Impact: [Describe breach impact]

**Existing Infrastructure:**
- Identity: [Current IdP if any]
- Security tools: [List existing tools]

**Security Architecture Coverage:**
1. Authentication - How users prove identity
2. Authorization - What users can access
3. Data Protection - Encryption and masking
4. Network Security - Boundaries and controls
5. Audit & Monitoring - Logging and alerting

Any areas to prioritize or constraints I should know?"

#### D. Create Document

Create `{outputFile}` with initial structure:

```markdown
---
stepsCompleted: []
dataClassification: [summary]
complianceRequirements: [list]
threatProfile: [summary]
---

# Security Architecture: {project_name}

## Document Control
- **Status:** Draft
- **Created:** {date}
- **Last Updated:** {date}

## Security Context

### Data Classification
[Document data types and sensitivity]

### Compliance Requirements
[Document applicable regulations]

### Threat Model Summary
[Document threat landscape]

### Existing Infrastructure
[Document current security tools and IdP]

---
*Sections below to be completed in Step 2: Design*
---

## Authentication Architecture
*Pending*

## Authorization Architecture
*Pending*

## Data Protection
*Pending*

## Network Security
*Pending*

## Audit & Monitoring
*Pending*

## Security Controls Matrix
*Pending*
```

### 4. Report & Menu

**Report:**
- Document created at `{outputFile}`
- Security context captured
- Ready to design security architecture

**Menu:**

**[C] Continue** - Proceed to Design (Step 2)
**[R] Revise** - Discuss changes to context
**[D] Deep Dive** - Explore threat model deeper
**[X] Exit** - Stop workflow

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-assess']`), then load and execute `{nextStepFile}`.

**On [R]:** Discuss changes, update document, return to menu.

**On [D]:** Invoke `/_deep-dive` on threat modeling. Update document, return to menu.

---

## SUCCESS CRITERIA

- Data classification documented
- Compliance requirements identified
- Threat model outlined
- Existing infrastructure understood
- Security document created with proper frontmatter
- User confirmed scope before proceeding
