---
name: 'step-02-generate'
description: 'Generate security checklist with findings'
outputFile: '{project_root}/docs/security-checklist.md'
template: '{skill_base}/security-checklist.template.md'
---

# Step 2: Generate

**Progress:** Step 2 of 2 → Final Step

**Goal:** Generate the security checklist with findings and recommendations.

---

## Instructions

### 1. Create Document

Copy `{template}` to `{outputFile}` and populate.

---

### 2. Complete Checklists

For each security domain, mark items:
- ✅ Passed - requirement met
- ❌ Failed - requirement not met (create finding)
- ⬜ Not assessed - needs verification
- N/A - not applicable to this system

---

### 3. Apply Risk-Based Focus

Based on assessment:

| Risk Level | Focus |
|------------|-------|
| High | All checks, detailed review |
| Medium | All checks, standard review |
| Low | Key checks, abbreviated review |

---

### 4. Create Findings

For each failed check:

```markdown
#### FIND-{NNN}: {Descriptive Title}
| Field | Value |
|-------|-------|
| **Severity** | Critical / Warning / Info |
| **Category** | {Auth/Data/Input/API/etc.} |
| **Description** | {What was found} |
| **Risk** | {What could happen} |
| **Remediation** | {How to fix} |
| **Status** | Open |
```

**Severity Guide:**
- **Critical:** Immediate risk, blocks deployment
- **Warning:** Should fix before or shortly after deployment
- **Info:** Best practice, fix when convenient

---

### 5. Determine Recommendation

| Findings | Recommendation |
|----------|----------------|
| No critical, few warnings | Approve |
| No critical, several warnings | Approve with Conditions |
| Any critical | Block until resolved |

---

### 6. Present Document

"**Security Checklist Generated**

**System:** {name}
**Risk Level:** {level}

**Results:**
- ✅ Passed: {count}
- ❌ Failed: {count}
- ⬜ Not assessed: {count}

**Findings:**
- Critical: {count}
- Warning: {count}

**Recommendation:** {Approve/Conditional/Block}

Review the checklist. Any items to discuss?"

---

### 7. Finalize

**Menu:**
```
[V] View → Display full document
[R] Revise → Adjust findings
[X] Exit → Complete
```

**On [X]:**

Update frontmatter:
```yaml
stepsCompleted: ['step-01-assess', 'step-02-generate']
completedAt: '{timestamp}'
riskLevel: '{level}'
```

**Completion Message:**
"Security checklist saved to `{outputFile}`.

**Next steps:**
1. Address critical findings (if any)
2. Get security sign-off
3. Include in change request documentation
4. Schedule remediation for warnings

**Before deployment:**
- All critical findings must be resolved
- Warnings should have remediation plan
- Security sign-off required

Run `/create-change-request` when security approved."
