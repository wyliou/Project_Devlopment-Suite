---
name: 'step-03-implement'
description: 'Parallel module implementation via Task subagents, layer by layer'
nextStepFile: './step-04-validate.md'
stateFile: '{project_root}/build-state.json'
maxConcurrentTasks: 3
maxRetries: 3
---

# Step 3: Implement

**Progress:** Step 3 of 4 - Next: Validate

**Goal:** Implement all modules using parallel subagent delegation, processing layers in dependency order.

---

## Execution Rules

- **Autonomous step** - no user prompts
- Spawn Task subagents for module implementation
- Process layers sequentially (L0 before L1, etc.)
- Max {maxConcurrentTasks} concurrent tasks per layer
- Auto-retry failed modules up to {maxRetries} times
- Skip persistently failing modules and continue
- Auto-proceed to next step when all layers processed

---

## Sequence (Follow Exactly)

### 1. Load Context

Read `{stateFile}` for:
- `layers`: array of layer definitions
- `completed_modules`: already completed
- `failed_modules`: permanently failed
- `retry_counts`: current retry state

Load PRD Section 3 (Functional Requirements).
Load Architecture Sections 3, 4, 5 (Patterns, Modules, APIs).

---

### 2. Process Layers

For each layer (0 to N), in order:

#### 2a. Identify Ready Modules

From current layer, identify modules where:
- Not in `completed_modules`
- Not in `failed_modules`
- All dependencies are in `completed_modules`

If no ready modules and layer not complete:
```
Layer [N] blocked: Dependencies not met.
Missing: [list of blocking deps]
```
Check if blockers are in `failed_modules`. If so, mark dependent modules as failed (cascade).

#### 2b. Spawn Implementation Tasks

For each ready module (up to {maxConcurrentTasks} at a time):

**Build task prompt:**

```
Implement Module: [module_name]
Location: [path from architecture]
Mode: [greenfield/brownfield]

## Functional Requirements
[Only FRs assigned to this module from PRD Section 3]

## API Contracts
[Relevant endpoints from Architecture Section 5]

## Patterns to Follow
[From Architecture Section 3]
- Naming conventions
- Error handling format
- Code organization

## Dependencies
Available imports: [completed modules this can import from]

## Instructions
1. Create module files at specified location
2. Implement all listed FRs
3. Follow the coding patterns exactly
4. Create unit tests for each FR
5. Run tests and fix any failures
6. Report completion status

## Success Criteria
- All FRs implemented
- Unit tests pass
- Code follows patterns
```

**Spawn task:**
```
Task tool with:
- subagent_type: "general-purpose"
- description: "Implement [module_name] module"
- prompt: [built prompt above]
- run_in_background: true (for parallel execution)
```

#### 2c. Wait for Layer Completion

Wait for all spawned tasks to complete.

For each completed task:

**On Success:**
- Add module to `completed_modules`
- Output: "[module_name]: SUCCESS"

**On Failure:**
- Increment `retry_counts[module_name]`
- If retry_count < {maxRetries}:
  - Output: "[module_name]: FAILED (retry [N]/3)"
  - Add back to ready queue for retry
- If retry_count >= {maxRetries}:
  - Add to `failed_modules` with error details
  - Output: "[module_name]: FAILED PERMANENTLY - [error summary]"

#### 2d. Update State After Layer

```json
{
  "layers[N].status": "complete",
  "completed_modules": [...],
  "failed_modules": [...],
  "retry_counts": {...}
}
```

Write updated state to `{stateFile}`.

#### 2e. Layer Summary

```
Layer [N] Complete
------------------
Succeeded: [count] ([module list])
Failed: [count] ([module list])
Proceeding to Layer [N+1]...
```

---

### 3. Handle Edge Cases

**All modules in layer failed:**
- Check if any modules in next layers can still proceed
- If no viable path forward:
  ```
  HALT: All modules in Layer [N] failed.
  No path forward - remaining modules have unmet dependencies.

  Failed modules:
  - [module]: [error]

  Review errors and fix manually, then re-run build.
  ```

**Brownfield conflicts:**
- If module location has existing code, subagent should:
  - Preserve existing functionality
  - Add new FR implementations
  - Run existing tests to prevent regression

---

### 4. Final Implementation Summary

After all layers processed:

```
Implementation Complete
=======================
Total Modules: [N]
Succeeded: [count]
Failed: [count]

Completed:
- [module_a]: FRs [list]
- [module_b]: FRs [list]

Failed:
- [module_x]: [error summary]

Proceeding to validation...
```

---

### 5. Update State

```json
{
  "current_step": 3,
  "implementation_complete": true,
  "completed_modules": [...],
  "failed_modules": [...]
}
```

---

### 6. Auto-Proceed

Update state: `current_step: 4`

Load and execute `{nextStepFile}`.

---

## Subagent Prompt Template

For reference, the full subagent prompt structure:

```markdown
# Module Implementation Task

## Context
- Project: [name]
- Module: [module_name]
- Location: [path]

## Your Goal
Implement this module completely and autonomously. Do not ask questions - make reasonable decisions based on the requirements.

## Functional Requirements to Implement
[FR-XXX]: [title]
- Input: [from PRD]
- Rules: [from PRD]
- Output: [from PRD]
- Errors: [from PRD]

## API Endpoints (if applicable)
[From Architecture Section 5]

## Code Patterns
[From Architecture Section 3]

## Available Dependencies
[List of completed modules that can be imported]

## Deliverables
1. Module source files
2. Unit test files
3. All tests passing

## Handling Ambiguities
If you encounter:
- Conflicting requirements → Note ambiguity, make reasonable assumption, continue
- Missing information → Note ambiguity, use sensible default, continue
- Unclear integration points → Note ambiguity, implement interface, continue

Do NOT stop for ambiguities - implement with best judgment and report what you assumed.

## Completion
When done, report:
- Files created
- FRs implemented
- Test results
- Ambiguities (if any): [{ type, description, assumption, severity: HIGH/MEDIUM/LOW }]
```

---

## Ambiguity Escalation Mechanism

Subagents may encounter blocking ambiguities during implementation. These are collected and surfaced before validation.

### What Qualifies as a Blocking Ambiguity

| Type | Example | Action |
|------|---------|--------|
| Conflicting Requirements | FR-001 says X, FR-002 says opposite | Collect and continue with noted assumption |
| Missing Critical Info | Auth method not specified | Collect and use reasonable default |
| Unclear Integration | How does module A call module B? | Collect and implement best-effort interface |

### Collection Process

1. **During subagent execution:** If ambiguity encountered, subagent notes it in completion report
2. **After layer completion:** Orchestrator collects all ambiguities from completed tasks
3. **Add to state:** `ambiguities: [{ module, type, description, assumption }]`

### Surfacing Before Validation

After all implementation layers complete, **before** proceeding to validation:

```
Ambiguities Encountered During Build
====================================
The following issues were found and resolved with assumptions:

1. [module_name]: [description]
   Assumption: [what was assumed]
   Impact: [potential impact]

2. [module_name]: [description]
   ...

These assumptions may need review. Proceed to validation?
```

**If any HIGH-impact ambiguities:** Pause for user confirmation
**If all LOW-impact:** Continue automatically with ambiguities logged in report

### Ambiguity Severity Classification

| Severity | Criteria | Action |
|----------|----------|--------|
| HIGH | Affects core functionality, security, or data integrity | Pause for user |
| MEDIUM | Affects non-critical features | Log and continue |
| LOW | Style/preference decisions | Log and continue |

---

## Success Criteria

- All layers processed in order
- Modules implemented via subagent Tasks
- Failed modules retried up to 3 times
- Persistent failures logged and skipped
- State updated after each layer
- Auto-proceeded to step-04-validate.md
