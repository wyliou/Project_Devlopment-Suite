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
- **Log:** {{expected log message format, if applicable}}
- **Depends:** FR-xxx (if any)

**FR-AREA-002**: [Actor] [capability]
- **Input:** field1 (constraints), field2 (constraints)
- **Rules:** IF condition THEN action
- **Output:** success behavior
- **Error:** error case → handling
- **Log:** {{if applicable}}

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

| FR ID | Summary | Depends |
|-------|---------|---------|
| FR-AREA-001 | {{brief summary}} | - |
| FR-AREA-002 | {{brief summary}} | FR-AREA-001 |
| FR-AREA-003 | {{brief summary}} | - |

---

## 8. Implementation Reference (Optional)

> *Include sections below when your project has defined formats, codes, or algorithms that implementing agents need as reference. Skip sections that don't apply.*

### 8.1 Configuration Schema

> *Include when: Project has user-editable configuration files (YAML, JSON, env vars)*

```yaml
# Example structure - replace with actual schema
{{config_section}}:
  {{field}}: {{type}}  # {{description}}
```

### 8.2 Output Formats

> *Include when: Project has defined console output, file formats, or API response structures*

**{{Output Type}} Format:**
```
{{exact format specification with examples}}
```

### 8.3 Error/Status Code Catalog

> *Include when: Project uses coded errors (ERR_001) or status codes for consistent reporting*

| Code | Description | Cause | Resolution |
|------|-------------|-------|------------|
| {{ERR_001}} | {{description}} | {{what triggers it}} | {{how to fix}} |
| {{ATT_001}} | {{description}} | {{what triggers it}} | {{action needed}} |

### 8.4 Algorithm Details

> *Include when: Project has multi-step logic, calculations, or processing pipelines that need exact specification*

**{{Algorithm Name}}:**

1. **Step 1:** {{description}}
   - Input: {{what it receives}}
   - Process: {{what it does}}
   - Output: {{what it produces}}

2. **Step 2:** {{description}}
   - ...

### 8.5 Examples & Edge Cases

> *Include when: Complex rules benefit from concrete examples showing expected behavior*

**Example: {{Scenario Name}}**
```
Input: {{example input}}
Expected: {{expected behavior/output}}
Reason: {{why this is correct}}
```

**Edge Case: {{Edge Case Name}}**
```
Situation: {{description}}
Handling: {{how system should respond}}
```
