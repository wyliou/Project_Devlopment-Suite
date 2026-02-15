---
name: 'step-06-complete'
description: 'Generate Quick Reference with priority, readiness gate, and handoff'

# File references
validationChecks: '{skills_root}/_prd-data/validation-checks.md'
---

# Step 6: Complete

**Progress: Step 6 of 6** - Workflow Complete

## STEP GOAL

Generate Quick Reference table with priority columns, perform readiness gate (structural completeness + cross-reference integrity), and prepare for handoff.

## EXECUTION RULES

- **Interactive step** — presents completion options
- This is the final step
- Readiness gate issues MUST be fixed before handoff
- Deep quality validation (density, measurability, leakage) is /prd-validate's domain — do not duplicate here
- Offer clear next actions

## SEQUENCE (Follow Exactly)

### 1. Generate Quick Reference Table

**Check FR count first.** If fewer than 5 FRs, skip Section 7 — it would just duplicate Section 3. Note "Section 7: Not applicable (fewer than 5 FRs)" in the PRD.

If 5+ FRs, create summary table from Section 3:

```markdown
## 7. Quick Reference

| FR ID | Summary | Capability Area | Priority | Depends |
|-------|---------|----------------|----------|---------|
| FR-xxx | {brief summary} | {area name} | {Must/Should/Could} | {FR-xxx or -} |
```

Mechanically generate from Section 3 — every FR gets a row. Derive Capability Area and Priority from the `### Area Name [Priority]` headers.

Update the PRD Section 7.

### 2. Readiness Gate

Structural completeness and cross-reference integrity checks only. This is NOT deep quality validation — that's /prd-validate's role.

#### A. Document Structure

Refer to `{validationChecks}` Section Requirements table to determine which sections are **Required**, **Recommended**, or **Optional** for this product type. Verify each required section is populated. Recommended sections should be populated but are not blockers.

#### B. Placeholder Cleanup

Scan the entire document for template placeholder patterns (`{{...}}`). Remove or fill all occurrences. If a section is complete but still contains placeholders, remove the placeholder lines.

#### C. Cross-Reference Integrity

| Check | Validation |
|-------|------------|
| Dependency validity | All `Depends:` references exist, no circular deps |
| Entity traceability | All entity Related FRs exist in Section 3 (skip if Section 5 not applicable) |
| Quick Reference completeness | All FRs from Section 3 appear in Section 7 (skip if Section 7 not applicable) |
| Priority consistency | Priority tags in Section 7 match Section 3 capability area headers (skip if Section 7 not applicable) |

**Mandatory: Do not allow handoff with structural issues.**

If any check fails:
1. List specific issues found
2. Fix each issue (update the relevant section)
3. Re-run the check
4. Repeat until all pass

### 3. Generate Summary Statistics

Calculate and display:
```
PRD Summary:
- Functional Requirements: {count} ({must_count} Must, {should_count} Should, {could_count} Could)
- Non-Functional Requirements: {count or "N/A"}
- Data Entities: {count or "N/A"}
- Capability Areas: {list areas with priorities}
- Readiness Gate: PASS
```

### 4. Update Frontmatter

Update the PRD frontmatter:
```yaml
---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-journeys', 'step-04-requirements', 'step-05-specifications', 'step-06-complete']
capabilityAreas: [{name, priority} array from step 3]
outputPath: '{outputPath}'
---
```

### 5. Present Completion

"**PRD Complete**

**Document:** {outputPath}

**Summary:**
- {FR count} Functional Requirements across {area count} capability areas ({must_count} Must, {should_count} Should, {could_count} Could)
- {NFR count} Non-Functional Requirements {or "N/A"}
- {entity count} Data Entities {or "N/A"}
- Readiness Gate: PASS

**Next Steps:**
1. Review the PRD with stakeholders
2. Run /prd-validate for deep quality validation (density, measurability, traceability)
3. Run /create-architecture to generate the Architecture document"

### 6. Menu

**[A] Architecture** - Run /create-architecture
**[V] Validate** - Run /prd-validate
**[S] Show PRD** - Display the complete document
**[X] Exit** - Finish
*Always available: **[P] Party Mode** | **[D] Deep Dive***
