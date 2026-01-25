---
name: 'step-03-complete'
description: 'Optimize, validate, and finalize project context'
outputFile: '{project_root}/docs/project-context.md'
---

# Step 3: Complete

**Progress:** Step 3 of 3 → Final

**Goal:** Optimize content for LLM efficiency, validate coverage, and finalize the project context document.

---

## Instructions

### 1. Review Complete Document

Read the entire project context file and analyze:

**Content Check:**
- Total rule count
- Coverage of all critical areas
- Specificity and actionability of rules

**Format Check:**
- Consistent markdown formatting
- Logical section organization
- No redundant or obvious rules

---

### 2. Optimize for LLM Context

Ensure content is lean and efficient:

**Remove:**
- Redundant rules
- Obvious patterns agents already know
- Verbose explanations

**Improve:**
- Combine related rules where possible
- Use specific, actionable language
- Ensure clear hierarchy

**Target:** Maximum information density with minimum token usage.

---

### 3. Add Usage Guidelines

Append to document:

```markdown
---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option

**For Humans:**
- Update when technology stack changes
- Review periodically for outdated rules
- Keep focused on unobvious details

Last Updated: {{date}}
```

---

### 4. Validation Checklist

Verify coverage:

| Check | Status |
|-------|--------|
| Technology versions documented | ✓/✗ |
| Language-specific rules actionable | ✓/✗ |
| Framework rules cover conventions | ✓/✗ |
| Testing rules ensure consistency | ✓/✗ |
| Code quality rules clear | ✓/✗ |
| Workflow rules prevent conflicts | ✓/✗ |
| Anti-patterns documented | ✓/✗ |

**If gaps found:** Add missing items before finalizing.

---

### 5. Finalize Document

Update frontmatter:
```yaml
---
status: complete
current_step: 3
project_name: [name]
created_at: [original date]
completed_at: [today]
rule_count: [total]
categories_completed: [all]
---
```

---

### 6. Present Completion Summary

**Summary:**
- Rule count: [N] critical rules
- Categories: [N] sections
- Optimized for LLM context

**Final Output:**
```
Project context complete: {outputFile}

Summary:
- [N] critical implementation rules
- [N] technology versions documented
- Optimized for LLM context efficiency

This file provides AI agents with the unobvious rules
and patterns needed for consistent implementation.

Next steps:
- AI agents read this before implementing
- Update when stack or patterns change
```

**No menu** - workflow complete.
