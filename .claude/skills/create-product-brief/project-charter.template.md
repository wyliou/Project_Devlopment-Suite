---
stepsCompleted: []
inputDocuments: []
workflowType: 'project-charter'
---

# Project Charter: {{project_name}}

**Author:** {{user_name}}
**Date:** {{date}}

---

## 1. Vision

### Problem Statement
{{2-3 sentences describing the core problem users face}}

### Solution Overview
{{2-3 sentences describing how this product solves it}}

### Key Differentiators
- {{differentiator 1}}
- {{differentiator 2}}

---

## 2. Users

| User Type | Primary Goal | Pain Points |
|-----------|--------------|-------------|
| {{user_type}} | {{primary goal}} | {{key pain points}} |

---

## 3. Success

### Key Success Metric
{{THE ONE metric that defines success for this product}}

### Supporting Indicators
- {{indicator 1}}
- {{indicator 2}}

---

## 4. MVP Scope

**In Scope:**
- {{core capability 1}}
- {{core capability 2}}
- {{core capability 3}}

**Out of Scope:**
- {{deferred capability 1}}
- {{deferred capability 2}}

---

## 5. Context

### Technology Preferences
{{Any decided technologies or "No preferences - open to recommendations"}}

### Timeline
{{Target timeline or "Flexible"}}

### Domain Notes
{{Relevant domain context, regulations, or constraints}}

---

## 6. Project Type

| Attribute | Value |
|-----------|-------|
| **Type** | {{Greenfield / Brownfield}} |
| **Category** | {{Web App / API / Mobile / Desktop / CLI}} |

---

## 7. Brownfield Context (If Applicable)

> *Complete this section for brownfield projects (replacing or integrating with existing systems). Skip for greenfield.*

### Existing Systems

| System | Role | Disposition |
|--------|------|-------------|
| {{system_name}} | {{what it does}} | {{Replace / Integrate / Migrate From}} |

### Legacy Data
- **Data to migrate:** {{description of data, estimated volume}}
- **Data quality concerns:** {{known issues}}
- **Migration strategy:** {{Big Bang / Phased / Parallel Run}}

### Current Users & Workflows
- **Affected users:** {{count and types}}
- **Critical workflows:** {{workflows that cannot be disrupted}}
- **Training needs:** {{what users need to learn}}

### Technical Constraints from Legacy
- {{constraint 1 - e.g., must integrate with Oracle DB}}
- {{constraint 2 - e.g., must support existing API consumers}}

---

## 8. Enterprise Context (Optional)

> *Complete this section for internal/enterprise projects. Skip for external products.*

| Field | Value |
|-------|-------|
| **Sponsor** | {{name, title}} |
| **Business Unit** | {{department}} |
| **Budget Code** | {{cost center if known}} |

### Compliance Notes
{{Any regulatory drivers: SOX, HIPAA, GDPR, internal policies, etc.}}

---

<!--
CHARTER → PRD MAPPING:
This charter feeds directly into /prd-create:
- Vision → PRD Section 1 Overview (Vision)
- Users table → PRD Section 1 Overview (Users table)
- Key Success Metric → PRD Section 1 Overview (Key Success Metric)
- MVP Scope → PRD Section 1 Overview (MVP Scope)
- Technology Preferences → PRD Section 6 Technology Constraints
- Domain Notes → PRD context for FRs and NFRs
- Enterprise Context → PRD Section 6 Technology Constraints (Integration Points, Compliance)
-->
