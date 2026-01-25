---
name: 'step-02-validate'
description: 'Run all validation checks: structure, format, quality, compliance'

# File references
nextStepFile: '{skill_base}/steps-validate-prd/step-03-assess.md'
validationChecks: '{skills_root}/_prd-data/validation-checks.md'
---

# Step 2: Validate

**Progress: Step 2 of 4** - Next: Assess

## STEP GOAL

Run comprehensive validation checks against PRD Guidelines: structure, format, quality, and compliance.

## EXECUTION RULES

- **Auto-proceed step** - no user input required
- Run all checks in sequence
- Display progress, append findings, auto-proceed to next step
- Reference `{validationChecks}` for detailed criteria

## SEQUENCE (Follow Exactly)

---

### PART A: STRUCTURE & FORMAT

#### A1. Extract PRD Structure

Scan entire PRD and extract:
- All `##` (Level 2) section headers in order
- Frontmatter metadata if present

#### A2. Check Section Structure

First, identify project type from Overview/Classification. Then check sections based on type:

| Section | Variations | Required For |
|---------|------------|--------------|
| 1. Overview | Executive Summary, Introduction | All |
| 2. User Journeys | User Stories, User Flows | Web/Mobile/Desktop |
| 3. Functional Requirements | Features, Capabilities | All |
| 4. Non-Functional Requirements | NFRs, Quality Attributes | Production systems |
| 5. Data Entities | Data Model, Entities | Persistent storage |
| 6. Technology Constraints | Tech Stack, Constraints | When constraints exist |
| 7. Quick Reference | Summary, Reference | 5+ FRs |

**Classify:**
- Complete: All recommended sections for project type
- Adequate: Required sections + some recommended
- Minimal: Required sections only
- Incomplete: Missing required sections

#### A3. FR ID Format Check

**Accept any consistent format:**
- Area-based: `FR-AUTH-001`
- Sequential: `FR-001`
- Descriptive: `user-registration`

**Check:**
- IDs are present
- IDs are consistent in style
- No duplicates

#### A4. FR Structure Check

For each FR, verify:
- [ ] Has Input with constraints
- [ ] Has Rules with business logic
- [ ] Has Output with testable behavior
- [ ] Has Error with handling
- [ ] Has Depends if references other FRs

Calculate FR format compliance: (complete FRs / total FRs) * 100

#### A5. NFR ID Format Check (If NFRs Present)

**Accept any consistent format** (NFR-PERF-001, NFR-001, or descriptive)
- Check IDs are present and consistent

#### A6. NFR Structure Check

For each NFR:
- [ ] Has measurable metric
- [ ] Has specific target
- [ ] Has condition/context

#### A7. Dependency Validation

- Verify all `Depends: FR-xxx` references exist
- Flag orphaned dependencies

---

### PART B: CONTENT QUALITY

#### B1. Information Density Check

Scan for anti-patterns:
- "The system will allow users to..."
- "It is important to note that..."
- "In order to", "Due to the fact that"
- Redundant phrases

Count violations. Severity: Critical (>10) / Warning (5-10) / Pass (<5)

#### B2. Measurability Check

**Success Metric (Section 1):**
- Is Key Success Metric quantifiable with target?

**NFRs:**
- Count NFRs with metric + target + condition

Severity: Critical (<50%) / Warning (50-80%) / Pass (>80%)

#### B3. FR Quality Check

For each FR:
- Input has specific fields with constraints?
- Rules capture business logic (not implementation)?
- Output is observable and testable?
- Error lists specific cases with handling?

#### B4. Implementation Leakage Check

Scan Sections 1-5, 7 for technology names:
- Frameworks (React, Django, FastAPI)
- Databases (PostgreSQL, MongoDB)
- Cloud (AWS, Azure, S3)
- Languages in requirements

**Exception:** Section 6 (Technology Constraints) MAY contain these

Severity: Critical (>5) / Warning (2-5) / Pass (<2)

#### B5. Data Entities Quality

- Each entity has Related FRs?
- Related FRs exist?
- No orphaned references?

#### B6. Quick Reference Quality

- All FRs in table?
- Priority uses P0/P1/P2/P3?
- Dependencies valid?

---

### PART C: COMPLIANCE

#### C1. Extract Classification

From Overview, extract:
- Project Type, Product Category, Primary Context

#### C2. Domain Compliance

Based on Primary Context, check required patterns:

**Enterprise/B2B:** Security NFRs, audit/logging, role-based access
**Consumer:** Privacy, UX metrics, accessibility
**Fintech:** Encryption, compliance, audit trail
**Healthcare:** Privacy (HIPAA), consent management

#### C3. Project-Type Compliance

Based on Product Category, check required elements:

**CLI Tool:** Input/output formats, exit codes, config
**Web App:** Responsive, session/auth, frontend NFRs
**API Service:** API FRs, rate limiting, auth, error format
**Desktop App:** Platform targets, installation, offline
**Mobile App:** Platform targets, offline, push notifications

#### C4. Technology Constraints Check

- Decided section present with non-negotiable items?
- Open section present with areas for agent decision?

---

### PART D: APPEND TO REPORT

```markdown
## Structure & Format

**Sections:** {count}/7 - {classification}
**FR Format:** {compliance}% ({count}/{total} with Input/Rules/Output/Error)
**NFR Format:** {compliance}% ({count}/{total} single-line)
**Dependencies:** {valid}/{total} valid

### FR Format Details
| Check | Pass | Fail |
|-------|------|------|
| Has Input | {n} | {n} |
| Has Rules | {n} | {n} |
| Has Output | {n} | {n} |
| Has Error | {n} | {n} |

## Content Quality

**Information Density:** {severity} ({count} violations)
**Measurability:** {severity} ({percentage}%)
**FR Quality Score:** {percentage}%
**Implementation Leakage:** {severity} ({count} found)
**Data Entities:** {count} entities, {orphans} orphaned
**Quick Reference:** {coverage}% FR coverage

{If violations, list top 5 examples with locations}

## Compliance

**Domain ({context}):** {percentage}% ({met}/{total})
**Project-Type ({category}):** {percentage}% ({met}/{total})
**Technology Constraints:** {status}

### Compliance Gaps
| Gap | Impact | Remediation |
|-----|--------|-------------|
{gaps or "No significant gaps"}
```

Update frontmatter: add `'step-02-validate'` to `stepsCompleted`

---

### PART E: DISPLAY PROGRESS AND PROCEED

"**Validation Complete**
- Structure: {classification} ({count}/7 sections)
- FR Format: {severity} ({percentage}%)
- NFR Format: {severity} ({percentage}%)
- Quality: {severity}
- Compliance: {severity}

Proceeding to assessment..."

**Auto-proceed:** Load and execute `{nextStepFile}`

---

## SUCCESS CRITERIA

- All structure checks completed
- All format checks completed
- All quality checks completed
- All compliance checks completed
- Findings appended to report
- Auto-proceeds without user input
