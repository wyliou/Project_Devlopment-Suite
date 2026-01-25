---
name: 'step-03-complete'
description: 'Synthesize research into executive summary and strategic recommendations'

# File references
outputFile: '{planning_artifacts}/research-{{project_name}}.md'
---

# Step 3: Complete

**Progress: Step 3 of 3** - Final Step

## STEP GOAL

Synthesize all research findings into an executive summary and actionable strategic recommendations.

## EXECUTION RULES

- **Interactive step** - requires user confirmation
- You are a Research Analyst - synthesize, don't add new research
- **NEVER** introduce new data not from previous steps
- Draw conclusions from existing research only

## SEQUENCE (Follow Exactly)

### 1. Review Existing Research

Read `{outputFile}` completely and extract key findings:

**From Stakeholder Analysis:**
- Key stakeholders and influence levels
- Champions and blockers
- RACI clarity

**From System Landscape:**
- Existing systems affected
- Integration complexity
- Technical dependencies

**From Organizational Context:**
- Business processes affected
- Compliance requirements
- Resource constraints

### 2. Cross-Section Analysis

Connect findings across all research areas:

- Where do stakeholder priorities align with system constraints?
- Which stakeholders control key integration points?
- What organizational factors affect timing?
- Where is the strongest alignment for project success?

### 3. Generate Executive Summary

**Elements:**

- **Opportunity Statement**: One paragraph synthesizing the opportunity
- **Key Findings**: 3-5 bullets of most important discoveries
- **Risk Factors**: What could challenge success
- **Confidence Assessment**: Overall confidence in the research

### 4. Generate Strategic Recommendations

**Areas:**

1. **Stakeholder Alignment Strategy**: How to gain buy-in based on research
2. **Key Decision Makers**: Who needs to approve and when
3. **Integration Priorities**: What systems to connect first based on dependencies
4. **Change Management Considerations**: Insights for rollout
5. **Further Research**: Questions that remain unanswered

### 5. Present Final Report

**Show to User:**
"Research synthesis complete for {{project_name}}.

**Executive Summary:**

### Opportunity Statement
[One paragraph]

### Key Findings
1. **Stakeholders**: [Key finding]
2. **Systems**: [Key finding]
3. **Organization**: [Key finding]
4. **Timing**: [Why now]

### Risk Factors
- [Risk 1]
- [Risk 2]

### Research Confidence
[Overall confidence level and caveats]

---

**Strategic Recommendations:**

### Stakeholder Alignment Strategy
[How to gain buy-in]

### Key Decision Makers
[Who to engage and when]

### Integration Priorities
1. [System] - [rationale]
2. [System] - [rationale]
3. [System] - [rationale]

### Change Management Considerations
[Rollout insights]

### Areas for Further Research
[Unanswered questions, if any]

---

Any adjustments to the summary or recommendations?"

### 6. Finalize Document

**Prepend** executive summary and recommendations after the document title:

```markdown
# Stakeholder Research Report: {{project_name}}

## Executive Summary

### Opportunity Statement
[Paragraph]

### Key Findings
1. **Stakeholders**: [Finding]
2. **Systems**: [Finding]
3. **Organization**: [Finding]
4. **Timing**: [Why now]

### Risk Factors
- [Risk 1]
- [Risk 2]

### Research Confidence
[Confidence level and caveats]

---

## Strategic Recommendations

### Stakeholder Alignment Strategy
[Strategy]

### Key Decision Makers
[Who and when]

### Integration Priorities
1. [System] - [rationale]
2. [System] - [rationale]
3. [System] - [rationale]

### Change Management Considerations
[Insights]

### Areas for Further Research
[Remaining questions]

---

[Existing Stakeholder/System/Organization research sections follow]
```

Update frontmatter: `stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-complete']`

### 7. Closing

**Completion Message:**
"Your research report is complete and saved to `{outputFile}`.

**Research Coverage:**
- ✅ Stakeholder Analysis (influence, champions, RACI)
- ✅ System Landscape (integrations, dependencies)
- ✅ Organizational Context (processes, compliance)
- ✅ Executive Summary
- ✅ Strategic Recommendations

**Next Steps:**
This research feeds into:
- `/create-project-charter` - Auto-discovers this research
- `/prd-create` - Reference during PRD development
- `/create-architecture` - Inform technical decisions
- `/analyze-integrations` - Detailed integration specification

Thank you for collaborating on this research!"

---

## SUCCESS CRITERIA

- Executive summary synthesizes all research areas (stakeholders, systems, organization)
- Recommendations are actionable and grounded in findings
- Risk factors acknowledge uncertainties
- Confidence level is honest about research quality
- Document is complete with all sections
- Frontmatter updated with final step
- User informed about next steps and integrations
