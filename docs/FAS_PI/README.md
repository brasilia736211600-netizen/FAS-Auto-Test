# FAS-Pi Project Context

> Canonical GitHub context for the current Pi-based FAS (Full Autonomous Stack) project.
>
> Updated: 2026-09-23
> Repository: brasilia736211600-netizen/FAS-Auto-Test
> Branch: fas-feature-test

## Purpose

This directory is the durable execution context for the **Pi-based FAS** line. It exists so work can be resumed from GitHub without depending on chat memory, model memory, local unstated state, or one permanent provider.

Read these files before changing the current Pi/FAS implementation:

1. `MASTER_PROJECT_MAP.md`
2. `WORKFLOW_STATE.md`
3. `RESEARCH_AND_DECISIONS_2026-09-23.md`
5. `ROADMAP.md`
6. `RESUME.md`

Dated reports and runtime evidence belong under `docs/FAS_PI/reports/`. Do not place report files directly in this directory.

## Important scope split

The repository already contains an older `.fas/FAS_FINAL_PLAN.md` describing a **Python/OpenCode FAS** line. That document remains historical/parallel context and must not be silently treated as the current Pi/FAS architecture.

The current line documented here is:

`Pi 0.85.1 -> Autopilot -> Workflow/Subagents -> central FAS supervisor -> model/provider routing -> bounded fallback -> evidence/learning -> efficiency -> verification/review`

## Source-of-truth hierarchy

When resuming:

1. GitHub repository code, tests, commits, and this `docs/FAS_PI/` directory are authoritative for project intent/state.
2. The GitHub execution/report workflow in `GITHUB_WORKFLOW.md` defines how changes and reports are persisted. is authoritative for claims about what actually runs.
3. Fresh runtime evidence are historical evidence; do not turn a report into a new runtime claim without reproving it when the claim matters.
4. Existing reports is context only and never completion proof.

## Secret rule

Never store provider keys, tokens, cookies, passwords, or secret-bearing environment output here.

## Current completion philosophy

A checkbox, plan item, or agent statement is not proof. Completion requires fresh evidence appropriate to the claim: source inspection, focused test, full suite, and/or live runtime proof.

## Current next gate

Leg 1, L6, and Leg 2 are CLOSED. The current gate is Phase 2 implementation in the evidence-backed order recorded in `reports/PHASE2_EVIDENCE_AUDIT_2026-09-23.md`.

Do not rerun closed runtime legs unless fresh evidence indicates regression.
