---
name: code-simplifier
description: Simplify and clean up source code files
---

# Code Simplifier

Analyze and simplify source code while preserving functionality.

## Usage

Run on a single file:
```
/code-simplifier path/to/file.py
```

Run on a directory:
```
/code-simplifier src/
```

## Simplification Rules

### 1. Remove Dead Code
- Unused imports
- Unused variables
- Unreachable code blocks
- Commented-out code (unless marked `# TODO` or `# FIXME`)

### 2. Reduce Complexity
- Flatten nested conditionals where possible
- Replace complex boolean expressions with named variables
- Extract repeated logic into helper functions (3+ occurrences)
- Simplify redundant type conversions

### 3. Improve Readability
- Replace magic numbers with named constants
- Simplify overly verbose expressions
- Remove redundant else after return/raise/continue/break

### 4. Consolidate Duplicates
- Merge similar functions with minor differences
- Extract common patterns into utilities
- Remove duplicate validation logic

## Constraints

- **DO NOT** change public API signatures
- **DO NOT** remove code marked with `# KEEP` or `# REQUIRED`
- **DO NOT** simplify test files (files matching `*_test.*`, `test_*.*`, `*.test.*`, `**/tests/**`, `**/__tests__/**`)
- **DO NOT** modify configuration files
- **PRESERVE** all existing functionality - simplification must be behavior-preserving
- **DO NOT** add new dependencies

## Process

1. Read the target file(s)
2. Identify simplification opportunities
3. Apply changes incrementally
4. Run linter to verify no errors introduced
5. Run tests to verify no regressions
6. If tests fail: revert changes, try alternative simplification or skip file
7. Report changes made

## Output Format

```
{
  files_modified: N,
  lines_removed: X,
  improvements: [
    "<filename>: removed N unused imports",
    "<filename>: flattened N nested conditionals",
    "<filename>: extracted N helper functions"
  ]
}
```

Or if no changes needed:
```
{
  files_modified: 0,
  lines_removed: 0,
  improvements: []
}
```
