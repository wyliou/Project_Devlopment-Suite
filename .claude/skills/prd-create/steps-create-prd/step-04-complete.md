---
name: 'step-04-complete'
description: 'Finalize PRD with validation summary and handoff'

# File references
outputFile: '{project_root}/docs/prd.md'
createArchSkill: '{skills_root}/create-architecture/skill.md'
validateSkill: '{skills_root}/prd-validate/skill.md'
---

# Step 4: Complete

**Progress: Step 4 of 4** - Workflow Complete

## STEP GOAL

Finalize the PRD with validation summary and prepare for handoff.

## EXECUTION RULES

- **Interactive step** - presents completion options
- This is the final step
- Offer clear next actions

## SEQUENCE (Follow Exactly)

### 1. Final Validation

Perform comprehensive validation:

#### Document Structure
| Section | Required |
|---------|----------|
| 1. Overview | Vision, Classification, Users, Success Metric, Scope |
| 2. User Journeys | At least 1 journey per user type |
| 3. Functional Requirements | At least 3 FRs with full format |
| 4. Non-Functional Requirements | At least 2 NFRs |
| 5. Data Entities | At least 1 entity |
| 6. Technology Constraints | Decided and Open sections |
| 7. Quick Reference | All FRs with dependencies |

#### Quality Checks
| Check | Validation |
|-------|------------|
| FR Format | All have Input/Rules/Output/Error |
| NFR Format | All are single-line with metric/target/condition |
| Dependencies | All `Depends:` references exist |
| Traceability | Journeys → FRs mapping is complete |

### 2. Generate Summary Statistics

Calculate and display:
```
PRD Summary:
- Functional Requirements: {count}
- Non-Functional Requirements: {count}
- Data Entities: {count}
- Capability Areas: {list areas}
```

### 3. Update Frontmatter

Update `{outputFile}` frontmatter:
```yaml
---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-requirements', 'step-04-complete']
inputDocuments: [{list of loaded docs}]
workflowType: 'prd'
completedAt: '{timestamp}'
documentChecksum: '{first 8 chars of sha256 hash of document content excluding frontmatter}'
---
```

The `documentChecksum` enables downstream documents (architecture, build state) to detect if the PRD has changed since they were created.

### 4. Present Completion

"**PRD Complete**

**Document:** {outputFile}

**Summary:**
- {FR count} Functional Requirements across {area count} capability areas
- {NFR count} Non-Functional Requirements
- {entity count} Data Entities

**Next Steps:**
1. Review the PRD with stakeholders
2. Run /prd-validate to verify quality
3. Run /create-architecture to generate the Architecture document

Ready for architecture generation."

### 5. Menu

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
- Epic breakdown (after architecture is complete)
