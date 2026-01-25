---
name: 'step-02-generate'
description: 'Generate business case document with ROI calculation'
outputFile: '{project_root}/docs/business-case.md'
template: '{skill_base}/business-case.template.md'
---

# Step 2: Generate

**Progress:** Step 2 of 2 → Final Step

**Goal:** Generate the complete business case document with ROI calculations.

---

## Instructions

### 1. Create Document

Copy `{template}` to `{outputFile}` and populate all sections from discovery.

---

### 2. Calculate ROI

**Formulas:**

```
Total Investment (Year 1) = One-time costs + Year 1 recurring costs

Annual Value = Sum of quantified benefits (annualized)

Payback Period (months) = (Total Investment / Annual Value) × 12

3-Year ROI = ((Annual Value × 3) - Total Investment) / Total Investment × 100
```

---

### 3. Generate Recommendation

Based on analysis:

| ROI | Payback | Recommendation |
|-----|---------|----------------|
| > 100% | < 12 months | Strong Go |
| 50-100% | 12-18 months | Go |
| 25-50% | 18-24 months | Conditional - review scope |
| < 25% | > 24 months | No-Go or re-scope |

Adjust based on strategic value, risk, and organizational context.

---

### 4. Present Document

Display the complete business case to user.

"**Business Case Generated**

**Summary:**
- Investment: {total}
- Annual Value: {value}
- Payback: {months} months
- 3-Year ROI: {percentage}%

**Recommendation:** {Go/No-Go/Conditional}

Review the document above. Any adjustments needed?"

---

### 5. Finalize

**Menu:**
```
[V] View → Display full document
[R] Revise → Make changes
[X] Exit → Complete
```

**On [X]:**

Update frontmatter:
```yaml
stepsCompleted: ['step-01-discovery', 'step-02-generate']
completedAt: '{timestamp}'
```

**Completion Message:**
"Business case saved to `{outputFile}`.

**Next steps:**
- Get sponsor sign-off
- Submit for budget approval
- Once approved, run `/create-project-charter` to define scope"
