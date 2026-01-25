wt---
stepsCompleted: []
inputDocuments: []
workflowType: 'prd'
sourceVersion: ''
documentChecksum: ''
---

# Product Requirements Document - {{project_name}}

**Author:** {{user_name}}
**Date:** {{date}}

---

## 1. Overview

### Vision
{{2-3 sentences describing the core product vision and value proposition}}

### Classification
| Attribute | Value |
|-----------|-------|
| Project Type | {{Greenfield / Brownfield}} |
| Product Category | {{CLI Tool / Web App / API Service / Desktop App / Mobile App / Library}} |
| Primary Context | {{Enterprise / Consumer / Internal / B2B}} |

### Users
| User Type | Primary Goal |
|-----------|--------------|
| {{user_type_1}} | {{what they want to accomplish}} |
| {{user_type_2}} | {{what they want to accomplish}} |

### Key Success Metric
{{The single most important metric that defines success for this product}}

### MVP Scope

**In Scope:**
- {{core capability 1}}
- {{core capability 2}}
- {{core capability 3}}

**Out of Scope:**
- {{deferred capability 1}}
- {{deferred capability 2}}

---

## 2. User Journeys

### {{User Type 1}}: {{Journey Name}}
1. {{Step 1}} → {{Step 2}} → {{Step 3}} → {{Step 4}} → {{Outcome}}

### {{User Type 2}}: {{Journey Name}}
1. {{Step 1}} → {{Step 2}} → {{Step 3}} → {{Outcome}}

---

## 3. Functional Requirements

### {{Capability Area 1}}

**FR-AREA-001**: [Actor] [capability]
- **Input:** field1 (constraints), field2 (constraints)
- **Rules:** IF condition THEN action; business logic
- **Output:** success behavior
- **Error:** error case → handling
- **Depends:** FR-xxx (if any)

**FR-AREA-002**: [Actor] [capability]
- **Input:** field1 (constraints), field2 (constraints)
- **Rules:** IF condition THEN action
- **Output:** success behavior
- **Error:** error case → handling

### {{Capability Area 2}}

**FR-AREA-003**: [Actor] [capability]
- **Input:** field1 (constraints)
- **Rules:** business logic
- **Output:** success behavior
- **Error:** error case → handling

---

## 4. Non-Functional Requirements

### Performance
- **NFR-PERF-001**: {{metric}} {{target}} under {{condition}}
- **NFR-PERF-002**: {{metric}} {{target}} under {{condition}}

### Security
- **NFR-SEC-001**: {{metric}} {{target}} under {{condition}}

### Scalability
- **NFR-SCALE-001**: {{metric}} {{target}} under {{condition}}

### Reliability
- **NFR-REL-001**: {{metric}} {{target}} under {{condition}}

---

## 5. Data Entities

| Entity | Key Attributes | Related FRs |
|--------|---------------|-------------|
| {{Entity1}} | id, {{attr1}}, {{attr2}}, created_at | FR-xxx, FR-xxx |
| {{Entity2}} | id, {{attr1}}, {{attr2}} | FR-xxx |

---

## 6. Technology Constraints

**Decided (non-negotiable):**
- {{constraint 1}}
- {{constraint 2}}

**Open (agent can decide):**
- {{decision area 1}}
- {{decision area 2}}

### Integration Points (Optional)

> *Complete for projects connecting to existing systems. Skip if greenfield with no integrations.*

| System | Direction | Data/Purpose | Auth Method |
|--------|-----------|--------------|-------------|
| {{system name}} | In/Out/Both | {{what data flows}} | {{SSO/API Key/etc.}} |

### Compliance Notes (Optional)

> *Single line summarizing regulatory or policy requirements.*

{{e.g., "SOX audit logging required" or "Contains PII - encryption at rest" or "N/A"}}

---

## 7. Quick Reference

| FR ID | Summary | Priority | Depends |
|-------|---------|----------|---------|
| FR-AREA-001 | {{brief summary}} | P0-Critical | - |
| FR-AREA-002 | {{brief summary}} | P1-High | FR-AREA-001 |
| FR-AREA-003 | {{brief summary}} | P2-Medium | - |

**Priority Levels:**
- P0-Critical: Must have for MVP, blocks other work
- P1-High: Must have for MVP
- P2-Medium: Should have for MVP
- P3-Low: Nice to have, can defer
