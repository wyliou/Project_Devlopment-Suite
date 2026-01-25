---
name: create-security-architecture
description: Define security patterns BEFORE detailed architecture design
---

# Security Architecture Workflow

**Goal:** Create a comprehensive security architecture document that defines security patterns, controls, and requirements before detailed technical architecture design.

**Your Role:** Security Architect collaborating with stakeholders. You help identify security requirements, threat models, and appropriate controls while the user provides organizational context and compliance requirements.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Assess** | Gather security requirements, threats, compliance needs | Interactive |
| 2 | **Design** | Create security architecture with patterns and controls | Hybrid |

---

## OUTPUT STRUCTURE

```markdown
# Security Architecture: {project_name}

## Security Context
- Data classification (PII, PHI, financial, public)
- Compliance requirements (GDPR, HIPAA, SOX, PCI-DSS)
- Threat model summary

## Authentication Architecture
- Method (SSO, OAuth2, SAML, API keys)
- Identity provider integration
- Session management

## Authorization Architecture
- Model (RBAC, ABAC, ACL)
- Role definitions
- Permission matrix

## Data Protection
- Encryption at rest (algorithm, key management)
- Encryption in transit (TLS version, certificate strategy)
- Data masking/tokenization

## Network Security
- Network boundaries
- Firewall rules
- API gateway security

## Audit & Monitoring
- Audit logging requirements
- Security monitoring
- Incident response hooks

## Security Controls Matrix
| Control | Requirement | Implementation | Status |
```

---

## KEY FEATURES

- **Early Security Focus:** Run BEFORE `/create-architecture` to inform technology decisions
- **Compliance-Driven:** Maps controls to regulatory requirements
- **Threat-Aware:** Considers attack vectors and mitigation strategies
- **Actionable Controls:** Produces specific, implementable security measures

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file
- **Just-In-Time Loading**: Only current step file in memory
- **Sequential Enforcement**: Steps completed in order, no skipping
- **State Tracking**: Progress tracked in document frontmatter
- **Compliance Mapping**: All controls traced to requirements

### Execution Rules

These principles ensure reliable execution. Deviate only with explicit reasoning documented in conversation:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update frontmatter when completing a step (enables continuation)
- Never assume compliance requirements - confirm with user

**When to Deviate:** If the user has specific organizational security policies or standards that differ from general best practices, adapt recommendations accordingly.

---

## NAVIGATION

**Natural Conversation (Preferred):**
Allow user to direct the workflow conversationally:
- "We need HIPAA compliance" -> Add healthcare-specific controls
- "Let's focus on API security" -> Prioritize that section
- "We use Okta for SSO" -> Incorporate existing identity infrastructure
- "Get different perspectives on this" -> Launch party mode

**Menu (Fallback for Structure):**
- **[C] Continue** - Proceed to next step
- **[R] Revise** - Make changes before proceeding
- **[D] Deep Dive** - Apply advanced elicitation techniques
- **[P] Party Mode** - Multi-agent perspective gathering

---

## INTEGRATION

Security architecture should be created early in the workflow:

```
/create-business-case
        |
        v
/stakeholder-research
        |
        v
/create-project-charter
        |
        v
/create-security-architecture  <-- YOU ARE HERE
        |
        v
/create-architecture  <-- Security decisions inform this
        |
        v
/prd-create
```

Output feeds into:
- `/create-architecture` - Security patterns inform technology choices
- `/security-checklist` - Validates implementation against this spec
- `/build-from-prd` - Subagents follow security patterns

---

## PATHS

- `output_path` = `{project_root}/docs/security-architecture.md`

---

## Execution

Load and execute `./steps/step-01-assess.md` to begin.
