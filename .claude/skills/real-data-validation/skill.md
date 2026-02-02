---
name: real-data-validation
description: Validate implementation against real data, classify failures as code bugs or input issues
---

# Validate Real Data

Run against ALL test inputs, analyze failures, fix code bugs, report non-code issues.

**Inputs:** Entry point, test data (`data/`, `samples/`, `fixtures/`), PRD.md

---

## 1. Initial Run

Run tool against ALL inputs. If 100% SUCCESS → output summary and exit.

## 2. Analyze Failures

**Scope: ALL non-SUCCESS outcomes** - not just hard errors. Warnings and degraded outputs can also be code bugs.

For each non-SUCCESS file:

1. **Identify:** Which function failed? What value caused it?
2. **Cross-ref PRD:** Does PRD require handling this?
3. **Classify:**

| Classification | Criteria | Action |
|----------------|----------|--------|
| `code_bug` | Implementation broken | Fix it |
| `integration_gap` | Function exists but never called | Wire it up |
| `delegation_gap` | PRD requires it, not implemented | Implement it |
| `needs_deep_analysis` | Data-related, pattern unknown | → Step 3 |

**Signs of `integration_gap`:** Function exported but no call sites in pipeline.
**Signs of `delegation_gap`:** PRD has rule/pattern not found in code.

## 3. Deep Analysis (REQUIRED before input_issue)

For `needs_deep_analysis` files:

**3.1 Extract actual data causing failure:**
- Part mismatch → list ALL parts from both sheets
- Empty field → show detected columns + actual values
- Weight error → show all weights + positions

**3.2 Compare across files for patterns:**
```
File 1: Invoice "ABC-001" vs Packing "ABC001" (dash)
File 2: Invoice "XYZ-002" vs Packing "XYZ002" (dash)
→ PATTERN: Dash normalization needed
```

**3.3 Pattern checklist:**
- String: case, whitespace, dashes, underscores
- Prefix/suffix: "P/N:", trailing spaces
- Type coercion: "001" vs 1
- Encoding: unicode variants

**3.4 Final classification:**

| Classification | Criteria | Action |
|----------------|----------|--------|
| `code_bug` | Pattern found, code fix possible | Agent fixes |
| `requires_user_action` | Pattern found, needs config/schema change | Report only |
| `input_issue` | No pattern, unique error | Document only |

**CRITICAL:** Agent only modifies code. Config/schema changes → `requires_user_action`.

## 4. Fix Issues

**Code bugs / Integration gaps / Delegation gaps:**
1. Implement fix
2. Re-run ALL files
3. Max 3 iterations per bug

## 5. Summary

```
Results: X/Y passed (Z%)
- Code bugs fixed: N
- Integration gaps fixed: N
- Delegation gaps fixed: N
- Requires user action: N (pattern found, non-code fix)
- Input issues: N (verified unique)

Patterns fixed: <list with evidence>
Requires user action: <pattern + suggested fix>
Input issues: <file: specific unique issue>
```

## Output

```
{inputs_total, inputs_passed, bugs_fixed, integration_gaps, delegation_gaps, requires_user_action, input_issues}
```
