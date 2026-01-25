---
stepsCompleted: []
workflowType: 'integration-spec'
systems: []
---

# Integration Specification: {{project_name}}

**Date:** {{date}}
**Author:** {{author}}

---

## System Landscape

```mermaid
graph LR
    NEW[{{project_name}}]
    NEW --> SYS1[{{system_1}}]
    NEW --> SYS2[{{system_2}}]
```

---

## Integration Points

### {{System 1}}

| Attribute | Value |
|-----------|-------|
| **Direction** | {{Inbound / Outbound / Bidirectional}} |
| **Method** | {{API / File / Database / Message Queue}} |
| **Protocol** | {{REST / SOAP / SFTP / JDBC / Kafka}} |
| **Data** | {{what data flows}} |
| **Frequency** | {{Real-time / Batch (schedule)}} |
| **Volume** | {{expected records/transactions}} |
| **Auth** | {{SSO / API Key / OAuth / Certificate}} |
| **Owner** | {{team/contact}} |
| **Environments** | Dev: {{endpoint}}, Prod: {{endpoint}} |
| **Dependency** | {{Critical / Important / Nice-to-have}} |

---

## Data Mapping

### {{Source System}} → {{Target System}}

| Source Field | Target Field | Transform | Notes |
|--------------|--------------|-----------|-------|
| {{field}} | {{field}} | {{transform or "Direct"}} | {{notes}} |

---

## Error Handling

| Integration | Error Scenario | Handling |
|-------------|---------------|----------|
| {{system}} | Connection timeout | {{retry policy}} |
| {{system}} | Invalid data | {{reject/log/alert}} |
| {{system}} | System unavailable | {{queue/fail/fallback}} |

---

## Dependencies & Sequencing

**Implementation Order:**

1. {{system}} - {{reason it must be first}}
2. {{system}} - {{dependency on #1}}
3. {{system}} - {{can be parallel with #2}}

---

## Risks & Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
| {{risk}} | {{High/Med/Low}} | {{mitigation}} |

---

## Open Questions

- {{question needing resolution}}
