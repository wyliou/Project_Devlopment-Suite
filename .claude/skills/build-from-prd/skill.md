---
name: build-from-prd
description: Autonomous skill that builds a working application from PRD and architecture documents using parallel subagent delegation
---

# Build from PRD Workflow

**Goal:** Take PRD.md and architecture.md as inputs and build a working application autonomously without human intervention.

**Your Role:** Build Orchestrator - autonomous executor that delegates module implementation to specialized subagents.

---

## What This Produces

| Output | Purpose |
|--------|---------|
| Project Structure | Directories and files per architecture |
| Installed Dependencies | All packages from tech stack |
| Database Setup | Tables/migrations from schema |
| Implemented Modules | Code for all FR modules |
| Unit Tests | Tests per module |
| Build Report | Summary of build results |

---

## Workflow Overview (4 Steps)

| Step | Name | Purpose | Mode |
|------|------|---------|------|
| 1 | **Analyze** | Find PRD/arch, extract modules, build dependency graph, create plan | Autonomous |
| 1b | **Continue** | Resume interrupted workflow (auto-triggered) | Autonomous |
| 2 | **Scaffold** | Create directories, install deps, setup DB, configure testing | Autonomous |
| 3 | **Implement** | Parallel module implementation via Task subagents (layer-by-layer) | Autonomous |
| 4 | **Validate** | Run tests, validate FR coverage, generate build report | Autonomous |

---

## Input Sources

| Source | Required | Content Used |
|--------|----------|--------------|
| PRD (docs/prd.md) | Yes | FRs, NFRs, Data Entities |
| Architecture (docs/architecture.md) | Yes | Stack, structure, modules, schema |

---

## Design Principles

- **Fully Autonomous:** No menus, no user prompts. Runs to completion automatically.
- **Auto-Retry:** Failed operations retry up to 3 times before marking as failed.
- **Auto-Skip:** Persistently failing modules are skipped; others continue.
- **HALT on Critical:** Only stops for missing inputs, circular deps, or total failure.
- **Progress Reporting:** Status updates output as workflow progresses.
- **Lean Context:** Subagents receive only relevant FRs and architecture sections.

---

## HALT Conditions

The workflow will HALT (stop execution) only for these critical errors:

| Condition | Message |
|-----------|---------|
| Missing PRD | "HALT: Build requires PRD. Not found at expected locations." |
| Missing Architecture | "HALT: Build requires architecture. Not found at expected locations." |
| Circular Dependencies | "HALT: Circular dependency detected: [cycle details]" |
| All Modules Failed | "HALT: All modules failed after retry attempts." |

---

## Workflow Architecture

Uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design:** Each step is a self-contained instruction file
- **Just-In-Time Loading:** Only current step file in memory
- **Sequential Steps:** Steps 1-4 executed in order
- **State Tracking:** Progress tracked in build-state.json
- **Auto-Proceed:** Steps automatically proceed to next without user input

### Core Principles

These principles ensure reliable autonomous execution:

- Load one step file at a time (keeps context focused)
- Read the entire step file before starting (ensures complete understanding)
- Complete steps in order (dependencies build on each other)
- Update build-state.json when completing a step (enables continuation)
- Follow step file instructions (they encode best practices)
- Execute autonomously without user prompts (except for blocking ambiguities)

**Blocking Ambiguity Exception:** If subagents encounter truly blocking ambiguities (conflicting requirements, missing critical information), they collect these issues and the orchestrator surfaces them before validation. This prevents wasted effort on invalid implementations.

---

## State Management

Build state tracked in `{project_root}/build-state.json`:

```json
{
  "status": "pending | in-progress | complete | failed",
  "current_step": 1,
  "mode": "greenfield | brownfield",
  "prd_path": "docs/prd.md",
  "prd_checksum": "abc12345",
  "architecture_path": "docs/architecture.md",
  "architecture_checksum": "def67890",
  "layers": [],
  "completed_modules": [],
  "failed_modules": [],
  "retry_counts": {},
  "ambiguities": [],
  "scaffold_complete": false,
  "started_at": "",
  "completed_at": ""
}
```

The `prd_checksum` and `architecture_checksum` enable detection if source documents change during build. The `ambiguities` array collects blocking issues encountered by subagents for review before validation.

---

## Subagent Delegation

Module implementation uses Claude Code's `Task` tool:

- **Layer-by-Layer:** Process modules by dependency level (L0 = no deps first)
- **Parallel Execution:** Up to 3 concurrent tasks per layer
- **Lean Prompts:** Each task receives only its FRs + relevant patterns
- **Autonomous Tasks:** Subagents implement without user interaction
- **Result Handling:** Success adds to completed, failure triggers retry

---

## Paths

- `stateFile` = `{project_root}/build-state.json`
- `stateTemplate` = `{skill_base}/build-state-template.json`
- `reportFile` = `{project_root}/docs/build-report.md`

---

## Execution

Load and execute `steps/step-01-analyze.md` to begin.
