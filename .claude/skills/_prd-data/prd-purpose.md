# PRD Guidelines

**Purpose:** Create PRDs optimized for both human stakeholders and AI agent consumption.

---

## Core Philosophy

### Dual-Audience Design

PRDs serve two audiences:
1. **Humans** - Product managers, stakeholders, developers reviewing requirements
2. **AI Agents** - Architecture generation, epic breakdown, implementation

### Information Density

Every sentence should carry information weight. AI agents consume precise, dense content efficiently.

**Avoid:**
- "The system will allow users to..." → "Users can..."
- "It is important to note that..." → State directly
- "In order to..." → "To..."
- Conversational filler and padding

**Goal:** Maximum information per word. Zero fluff.

---

## Document Structure

### Required Sections (All Projects)

| Section | Purpose |
|---------|---------|
| **1. Overview** | Vision, classification, users, success metric, scope |
| **3. Functional Requirements** | What the system does |

### Conditional Sections (By Project Type)

| Section | Include When |
|---------|--------------|
| **2. User Journeys** | UI-based products (Web App, Mobile, Desktop) |
| **4. Non-Functional Requirements** | Production systems with quality constraints |
| **5. Data Entities** | Systems with persistent storage |
| **6. Technology Constraints** | Existing tech decisions or restrictions |
| **7. Quick Reference** | 5+ functional requirements |

### Project Type Guide

| Project Type | Recommended Sections |
|--------------|---------------------|
| **Web App** | All 7 sections |
| **Mobile App** | All 7 sections |
| **API Service** | 1, 3, 4, 5, 6, 7 (skip User Journeys - use API contracts) |
| **CLI Tool** | 1, 3, 4, 6 (add Command Reference instead of User Journeys) |
| **Library/SDK** | 1, 3, 4, 6 (add API Surface instead of User Journeys) |
| **Prototype/MVP** | 1, 2, 3 (minimal viable documentation) |

---

## Functional Requirements Format

### Recommended FR Structure

```markdown
**[Descriptive ID]**: [Actor] [capability]
- **Input:** field1 (constraints), field2 (constraints)
- **Rules:** Business logic, conditions
- **Output:** Success behavior (testable)
- **Error:** Error cases → handling
- **Depends:** Other FRs this requires (if any)
```

### ID Conventions (Flexible)

Choose an approach that fits your project:

| Style | Example | Best For |
|-------|---------|----------|
| Area-based | `FR-AUTH-001` | Large projects with many FRs |
| Sequential | `FR-001` | Small projects |
| Descriptive | `user-registration` | When readability matters most |

### FR Quality Criteria

- **Actor** is explicit (User, System, Admin)
- **Input** has constraints (types, formats, limits)
- **Rules** capture business logic, not implementation details
- **Output** is specific and testable
- **Error** handling is explicit

---

## Non-Functional Requirements Format

### Single-Line Format

```markdown
**[ID]**: [metric] [target] under [condition]
```

### Examples

```markdown
**NFR-PERF-001**: API response time under 200ms for 95th percentile under normal load
**NFR-SEC-001**: All data encrypted at rest using AES-256
**NFR-REL-001**: 99.9% uptime during business hours
```

### Categories

| Category | Code | Examples |
|----------|------|----------|
| Performance | PERF | Response time, throughput, startup time |
| Security | SEC | Encryption, auth expiry, data protection |
| Scalability | SCALE | Concurrent users, data volume |
| Reliability | REL | Uptime, recovery time, durability |

---

## Data Entities

When your system has persistent storage, document entities:

```markdown
## Data Entities

| Entity | Key Attributes | Related FRs |
|--------|---------------|-------------|
| User | id, email, password_hash, created_at | FR-AUTH-001, FR-AUTH-002 |
| Order | id, user_id, status, total, created_at | FR-ORDER-001 |
```

---

## Technology Constraints

Document decisions that constrain implementation:

```markdown
## Technology Constraints

**Decided:**
- Backend: Python 3.11+ with FastAPI
- Database: PostgreSQL 15+

**Open (implementer decides):**
- ORM choice
- Caching strategy
```

Skip this section if the implementer has full freedom.

---

## Quick Reference

For projects with 5+ FRs, add a summary table:

```markdown
## Quick Reference

| FR ID | Summary | Depends |
|-------|---------|---------|
| FR-AUTH-001 | User registration | - |
| FR-AUTH-002 | Password reset | FR-AUTH-001 |
```

---

## Traceability

Good PRDs maintain traceability:

```
Vision → Success Metric → User Journeys → Functional Requirements → Data Entities
```

- Success metric should be measurable
- User journeys imply required capabilities
- FRs should trace back to user needs
- Data entities should link to FRs that use them

---

## What Makes a Good PRD?

| Principle | Description |
|-----------|-------------|
| **Dense** | Every sentence carries weight |
| **Measurable** | Success metric and NFRs are testable |
| **Traceable** | Requirements link to user needs |
| **Flexible** | Structure fits the project |
| **Actionable** | AI agents can implement from FRs |

The goal is **useful documentation**, not **comprehensive documentation**.
