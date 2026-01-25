---
name: 'step-01-discovery'
description: 'Gather business problem, solution, benefits, and costs'
nextStepFile: '{skill_base}/steps/step-02-generate.md'
outputFile: '{project_root}/docs/business-case.md'
template: '{skill_base}/business-case.template.md'
---

# Step 1: Discovery

**Progress:** Step 1 of 2 → Next: Generate

**Goal:** Gather information about the business problem, proposed solution, benefits, and costs.

---

## Instructions

### 1. Opening

"Let's build a business case for your project.

**First, tell me:**
- What business problem are you trying to solve?
- What's the impact of this problem today? (time, money, risk)"

---

### 2. Solution & Sponsor

Once problem is clear:

"Who is sponsoring this project, and which business unit owns it?

What's your proposed solution in 1-2 sentences?"

---

### 3. Benefits

"What benefits do you expect? Let's quantify them:

| Benefit | How to Measure | Current State | Target |
|---------|----------------|---------------|--------|

Examples:
- Time saved → Hours/week → Currently 10 hrs → Target 2 hrs
- Error reduction → Error rate → Currently 5% → Target 0.5%
- Revenue → Monthly amount → Currently $X → Target $Y"

---

### 4. Costs

"Let's estimate costs:

**One-time costs:**
- Development (internal hours or external cost)
- Infrastructure setup
- Licenses (initial)
- Training

**Recurring costs (annual):**
- Infrastructure/hosting
- License renewals
- Support/maintenance

Rough estimates are fine - we can refine later."

---

### 5. Risks

"What could go wrong? Top 2-3 risks:

- Technical risks?
- Adoption risks?
- Resource risks?
- Integration risks?"

---

### 6. Confirm & Proceed

**Summary:**
"Here's what I have:

**Problem:** {summary}
**Solution:** {summary}
**Key Benefit:** {primary benefit with numbers}
**Estimated Cost:** {rough total}
**Top Risk:** {main risk}

Ready to generate the business case?"

**Menu:**
```
[C] Continue → Generate document
[R] Revise → Adjust inputs
```

**On [C]:** Update frontmatter (`stepsCompleted: ['step-01-discovery']`), load and execute `{nextStepFile}`.
