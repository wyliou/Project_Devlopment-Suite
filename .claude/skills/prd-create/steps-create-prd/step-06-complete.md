---
name: 'step-06-complete'
description: 'Generate Quick Reference with priority, readiness gate, and handoff'

# File references
createArchSkill: '{skills_root}/create-architecture/skill.md'
validateSkill: '{skills_root}/prd-validate/skill.md'
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

Create summary table from Section 3 FRs with Capability Area and Priority columns:

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

Read the product category from Section 1 Classification. Use the validation-checks.md Section Requirements table to determine which sections are **Required**, **Recommended**, or **Optional** for this project type. Required sections MUST be populated. Recommended sections should be populated but are not blockers. Optional sections are skipped silently.

| Section | Check (if required/recommended for project type) |
|---------|-------|
| 1. Overview | Vision, Classification, Actors, Success Metrics, Scope — all sub-sections present and populated |
| 2. Journeys/Workflows | At least 1 journey per actor type, adapted to product category. If marked "Not applicable" in step 3, skip. |
| 3. Functional Requirements | At least 1 FR per capability area (minimum 3 total). Every FR has Input/Rules/Output/Error. |
| 4. Non-Functional Requirements | At least 2 NFRs (PERF + one other). Single-line format with metric/target/condition. |
| 5. Data Entities | At least 1 entity (if applicable). Attributes and Related FRs populated. |
| 6. Technology Constraints | Decided and Open sections. Present even if one is empty. |
| 7. Quick Reference | All FRs with dependencies. Every FR from Section 3 has a row, Priority column present. |
| 8. Implementation Reference | If present, verify no `{{placeholder}}` content remains. Skip if not applicable. |

#### B. Placeholder Cleanup

Scan the entire document for template placeholder patterns (`{{...}}`). Remove or fill all occurrences. If a section is complete but still contains placeholders, remove the placeholder lines.

#### C. Cross-Reference Integrity

| Check | Validation |
|-------|------------|
| Dependency validity | All `Depends:` references exist, no circular deps |
| Entity traceability | All entity Related FRs exist in Section 3 |
| Quick Reference completeness | All FRs from Section 3 appear in Section 7 |
| Priority consistency | Priority tags in Section 7 match Section 3 capability area headers |

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
- Non-Functional Requirements: {count}
- Data Entities: {count}
- Capability Areas: {list areas with priorities}
- Readiness Gate: PASS
```

### 4. Update Frontmatter

Update the PRD frontmatter:
```yaml
---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-journeys', 'step-04-requirements', 'step-05-specifications', 'step-06-complete']
inputDocuments: [{list of loaded docs}]
workflowType: 'prd'
completedAt: '{timestamp}'
documentChecksum: '{first 8 chars of sha256 hash of document content excluding frontmatter}'
capabilityAreas: [{name, priority} array from step 3]
outputPath: '{outputPath}'
---
```

The `documentChecksum` enables downstream documents (architecture, build state) to detect if the PRD has changed since they were created.

### 5. Present Completion

"**PRD Complete**

**Document:** {outputPath}

**Summary:**
- {FR count} Functional Requirements across {area count} capability areas ({must_count} Must, {should_count} Should, {could_count} Could)
- {NFR count} Non-Functional Requirements
- {entity count} Data Entities
- Readiness Gate: PASS

**Next Steps:**
1. Review the PRD with stakeholders
2. Run /prd-validate for deep quality validation (density, measurability, traceability)
3. Run /create-architecture to generate the Architecture document

Ready for architecture generation."

### 6. Menu

**[A] Architecture** - Run /create-architecture workflow
**[V] Validate** - Run /prd-validate for deep quality validation
**[P] Party Mode** - Multi-agent review before finalizing
**[S] Show PRD** - Display the complete document
**[X] Exit** - Finish

#### Menu Logic:

**A (Architecture):**
"Architecture will derive API contracts and database schema from this PRD."
→ Suggest running `/create-architecture`

**V (Validate):**
"Deep quality validation will check density, measurability, traceability, and compliance against PRD Guidelines."
→ Suggest running `/prd-validate`

**P (Party Mode):**
Invoke `/_party-mode` skill to get multi-perspective review of the PRD from PM, Architect, Developer, and QA viewpoints. After discussion, capture insights and return to menu with option to revise.

**S (Show PRD):**
Display the full PRD document
Return to menu

**X (Exit):**
"**Complete**
PRD: {outputPath}
Status: Ready for review

**Next Steps:**
- Share with stakeholders for review
- Run /prd-validate for deep quality validation
- Run /create-architecture when ready"

Exit workflow

---

## WORKFLOW COMPLETE

The PRD workflow is now complete. The document is ready for:
- Stakeholder review and approval
- Deep quality validation (via /prd-validate)
- Architecture generation (via /create-architecture)
