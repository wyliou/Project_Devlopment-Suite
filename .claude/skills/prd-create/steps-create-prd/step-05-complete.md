---
name: 'step-05-complete'
description: 'Generate Quick Reference, architecture-readiness check, final validation, and handoff'

# File references
outputFile: '{project_root}/docs/prd.md'
createArchSkill: '{skills_root}/create-architecture/skill.md'
validateSkill: '{skills_root}/prd-validate/skill.md'
---

# Step 5: Complete

**Progress: Step 5 of 5** - Workflow Complete

## STEP GOAL

Generate Quick Reference table, perform architecture-readiness check, run final validation, and prepare for handoff.

## EXECUTION RULES

- **Interactive step** - presents completion options
- This is the final step
- Architecture-readiness issues MUST be fixed before handoff
- Offer clear next actions

## SEQUENCE (Follow Exactly)

### 1. Generate Quick Reference Table

Create summary table from Section 3 FRs:

```markdown
## 7. Quick Reference

| FR ID | Summary | Depends |
|-------|---------|---------|
| FR-xxx | {brief summary} | {FR-xxx or -} |
```

Mechanically generate from Section 3 — every FR gets a row.

Update `{outputFile}` Section 7.

### 2. Final Validation & Readiness Check

Single comprehensive pass covering document completeness, quality, and architecture readiness.

#### A. Document Structure

| Section | Required | Check |
|---------|----------|-------|
| 1. Overview | Vision, Classification, Users, Success Metric, Scope | All sub-sections present and populated |
| 2. User Journeys | At least 1 journey per user type | Adapted to product category (journeys/commands/scenarios) |
| 3. Functional Requirements | At least 3 FRs with full format | Every FR has Input/Rules/Output/Error |
| 4. Non-Functional Requirements | At least 2 NFRs (PERF + one other) | Single-line format with metric/target/condition |
| 5. Data Entities | At least 1 entity (if applicable) | Attributes and Related FRs populated |
| 6. Technology Constraints | Decided and Open sections | Present even if one is empty |
| 7. Quick Reference | All FRs with dependencies | Every FR from Section 3 has a row |

#### B. Quality & Readiness

| Check | Validation |
|-------|------------|
| FR Input completeness | Fields have type + constraint annotations |
| FR Output testability | Outputs describe observable, testable behavior |
| FR Error coverage | At least 1 error case per FR |
| NFR measurability | Each has metric + target + condition |
| Dependency validity | All `Depends:` references exist, no circular deps |
| Entity traceability | All entity Related FRs exist in Section 3 |
| Journey coverage | Journeys → FRs mapping is complete |
| Information density | No filler phrases or vague descriptors |

**Mandatory: Do not allow handoff with issues.**

If any check fails:
1. List specific issues found
2. Fix each issue (update the relevant section)
3. Re-run the check
4. Repeat until all pass

### 3. Generate Summary Statistics

Calculate and display:
```
PRD Summary:
- Functional Requirements: {count}
- Non-Functional Requirements: {count}
- Data Entities: {count}
- Capability Areas: {list areas}
- Architecture Readiness: PASS
```

### 4. Update Frontmatter

Update `{outputFile}` frontmatter:
```yaml
---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-requirements', 'step-04-specifications', 'step-05-complete']
inputDocuments: [{list of loaded docs}]
workflowType: 'prd'
completedAt: '{timestamp}'
documentChecksum: '{first 8 chars of sha256 hash of document content excluding frontmatter}'
---
```

The `documentChecksum` enables downstream documents (architecture, build state) to detect if the PRD has changed since they were created.

### 5. Present Completion

"**PRD Complete**

**Document:** {outputFile}

**Summary:**
- {FR count} Functional Requirements across {area count} capability areas
- {NFR count} Non-Functional Requirements
- {entity count} Data Entities
- Architecture Readiness: PASS

**Next Steps:**
1. Review the PRD with stakeholders
2. Run /prd-validate to verify quality
3. Run /create-architecture to generate the Architecture document

Ready for architecture generation."

### 6. Menu

**[A] Architecture** - Run /create-architecture workflow
**[V] Validate** - Run /prd-validate to verify quality
**[P] Party Mode** - Multi-agent review before finalizing
**[S] Show PRD** - Display the complete document
**[X] Exit** - Finish

#### Menu Logic:

**A (Architecture):**
"Architecture will derive API contracts and database schema from this PRD."
→ Suggest running `/create-architecture`

**V (Validate):**
"Validation will check the PRD against PRD Guidelines."
→ Suggest running `/prd-validate`

**P (Party Mode):**
Invoke `/_party-mode` skill to get multi-perspective review of the PRD from PM, Architect, Developer, and QA viewpoints. After discussion, capture insights and return to menu with option to revise.

**S (Show PRD):**
Display the full PRD document
Return to menu

**X (Exit):**
"**Complete**
PRD: {outputFile}
Status: Ready for review

**Next Steps:**
- Share with stakeholders for review
- Run /prd-validate to verify quality
- Run /create-architecture when ready"

Exit workflow

---

## WORKFLOW COMPLETE

The PRD workflow is now complete. The document is ready for:
- Stakeholder review and approval
- Validation (via /prd-validate)
- Architecture generation (via /create-architecture)
