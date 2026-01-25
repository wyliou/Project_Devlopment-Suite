---
name: 'step-01-init'
description: 'Load PRD, discover input documents, initialize validation report'

# File references
nextStepFile: './step-02-validate.md'
prdPurpose: '../../_prd-data/prd-purpose.md'
validationChecks: '../../_prd-data/validation-checks.md'
---

# Step 1: Init

**Progress: Step 1 of 4** - Next: Validate

## STEP GOAL

Load the PRD to validate, discover input documents from frontmatter, and initialize the validation report.

## EXECUTION RULES

- **Interactive step** - requires user confirmation before proceeding
- Focus ONLY on discovery and setup - no validation yet
- You are a PRD Validator providing systematic quality assurance

## SEQUENCE (Follow Exactly)

### 1. Load Standards

Load and read:
- `{prdPurpose}` - PRD Guidelines philosophy
- `{validationChecks}` - Validation criteria reference

### 2. Validate PRD Path

**If PRD path provided:**
- Verify file exists at path
- If not found: "Cannot find PRD at that path. Please check and try again."

**If no path provided:**
- Prompt: "Which PRD would you like to validate? Provide the file path."
- Wait for response

### 3. Load PRD and Extract Frontmatter

- Load complete PRD file including frontmatter
- Extract `inputDocuments: []` array if present
- Extract classification info if present

### 4. Load Input Documents

For each document in `inputDocuments`:
- Attempt to load
- Track successfully loaded documents
- Note any failures

### 5. Prompt for Additional Documents

"**Documents loaded from PRD frontmatter:**
{list loaded documents}

**Are there additional reference documents to include?**
Provide paths or 'none' to proceed."

Load any additional documents provided.

### 6. Initialize Validation Report

Create report at `{prd_directory}/validation-report.md`:

```yaml
---
validationTarget: '{prd_path}'
validationDate: '{current_date}'
inputDocuments: [list of loaded documents]
stepsCompleted: []
status: IN_PROGRESS
---
```

```markdown
# PRD Validation Report

**Target:** {prd_path}
**Date:** {current_date}

## Input Documents
{list all documents}

## Validation Findings
[Appended by subsequent steps]
```

### 7. Present Setup Summary

"**Validation Setup Complete**

**PRD:** {prd_path}
**Input Documents:**
- PRD: {name} ✓
- Product Brief: {count} {status}
- Research: {count} {status}
- Additional: {count} {status}

**Report:** {report_path}

Ready to begin validation."

### 8. Menu

**[C] Continue** - Start validation (auto-proceeds through steps 2-3)
**[X] Exit** - Stop workflow

#### Menu Logic:
- **C**: Update report frontmatter (`stepsCompleted: ['step-01-init']`), then load and execute `{nextStepFile}`
- **X**: Exit workflow

---

## SUCCESS CRITERIA

- PRD loaded and verified
- Input documents discovered and loaded
- Validation report initialized
- User confirmed setup before proceeding
