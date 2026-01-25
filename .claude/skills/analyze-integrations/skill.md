---
name: analyze-integrations
description: Map connections to existing enterprise systems for integration planning
---

# Analyze Integrations Workflow

**Goal:** Create a detailed integration specification mapping all connections to existing enterprise systems.

**Your Role:** Integration analyst documenting system connections, data flows, and dependencies.

---

## WORKFLOW OVERVIEW (2 Steps)

| Step | Name | Purpose |
|------|------|---------|
| 1 | **Discovery** | Identify systems, data flows, dependencies |
| 2 | **Document** | Create integration specification |

---

## OUTPUT FORMAT

```markdown
# Integration Specification: {project_name}

## System Landscape

{Mermaid diagram showing connections}

## Integration Points

### {System Name}
- **Direction:** Inbound / Outbound / Bidirectional
- **Method:** API / File / Database / Message Queue / Event
- **Protocol:** REST / SOAP / SFTP / JDBC / Kafka / etc.
- **Data:** {what data flows}
- **Frequency:** Real-time / Near-real-time / Batch (schedule)
- **Volume:** {expected records/transactions}
- **Auth:** SSO / API Key / OAuth / Certificate / Service Account
- **Owner:** {team/contact responsible for system}
- **Environment:** {dev/test/prod endpoints}
- **Dependency Level:** Critical / Important / Nice-to-have

## Data Mapping

### {System} → {New System}

| Source Field | Target Field | Transform | Notes |
|--------------|--------------|-----------|-------|

## Error Handling

| Integration | Error Scenario | Handling |
|-------------|---------------|----------|

## Dependencies & Sequencing

{Order of integration implementation}

## Risks & Considerations

| Risk | Impact | Mitigation |
|------|--------|------------|
```

---

## CONVERSATION APPROACH

- **Start with landscape** - what systems exist today
- **Map data flows** - what goes where and why
- **Identify owners** - who controls each system
- **Document dependencies** - what must work first

---

## Execution

Load and execute `./steps/step-01-discovery.md` to begin.
