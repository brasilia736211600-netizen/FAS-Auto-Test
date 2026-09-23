# FAS-Pi Project Context

Canonical GitHub context for the current Pi-based FAS (Full Autonomous Stack) project.

Updated: 2026-09-24
Repository: brasilia736211600-netizen/FAS-Auto-Test
Branch: fas-feature-test

## Read before acting

1. MASTER_PROJECT_MAP.md
2. GITHUB_WORKFLOW.md
3. WORKFLOW_STATE.md
4. RESEARCH_AND_DECISIONS_2026-09-23.md
5. ROADMAP.md
6. RESUME.md
7. autonomy/AUTONOMOUS_OPERATOR_MANDATE.md
8. autonomy/EXECUTION_PROTOCOL.md
9. autonomy/TASK_QUEUE.md
10. autonomy/FINALIZATION_AND_HANDOFF.md
11. all reports relevant to the current queue item

## Purpose

This is the durable GitHub execution context for the Pi-based FAS line. Work must be recoverable after interruption without chat memory, model memory, or one permanent provider.

## Current architecture

Pi 0.85.1 -> Autopilot -> Workflow/Subagents -> central FAS supervisor -> capability-aware routing -> bounded fallback -> evidence/learning -> efficiency -> safety -> verification/review -> state/checkpoint

## Source of truth

GitHub source/tests/history and fresh runtime evidence are authoritative. Reports preserve evidence. Chat is context only.

## Directory policy

- docs/FAS_PI/ = state, architecture, workflow, roadmap, resume.
- docs/FAS_PI/reports/ = dated evidence and reports.
- docs/FAS_PI/autonomy/ = autonomous operator mandate, protocol, queue, finalization.
- docs/FAS_PI/checkpoints/ = milestone recovery snapshots.
- docs/FAS_PI/handoff/ = final release/new-repository handoff.

Never store secrets in these locations.

## Current status

Phase 1 runtime closure: COMPLETE.
Phase 2 architecture enhancements: IMPLEMENTED/SUBSTANTIALLY COMPLETE.
Current regression lineage: 469/469 GREEN.
D local-provider suitable-path live proof: BLOCKED unless a real daemon host exists.
E real cross-session/multi-process live proof: residual UNKNOWN.
C role prompt wiring: DEFERRED unless a genuine orchestrator role field exists.
Current next work: autonomous full-system audit -> justified consolidation -> compatibility -> clean-room -> final E2E -> final handoff.

Do not rerun closed runtime legs unless fresh evidence indicates regression.
