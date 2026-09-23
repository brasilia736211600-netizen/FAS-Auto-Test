# FAS-Pi Master Project Map

Updated: 2026-09-24

## Identity

FAS = Full Autonomous Stack.

Current target:
Pi -> Autopilot -> Workflow/Subagents -> central FAS supervisor -> capability-aware routing -> bounded fallback -> evidence/learning -> efficiency -> safety -> verification/review -> state/checkpoint -> DONE.

## Layer ownership

Pi Core: harness, sessions, context, native compaction, model/provider APIs, normal extension lifecycle.
Autopilot: high-level task lifecycle.
Workflow: phases, dependencies, DAG, child execution semantics, persisted run state.
Subagents: child dispatch/execution and collaboration.
FAS: centralized routing, capability filtering, deterministic ranking, bounded fallback, evidence-gated learning, thinking/output efficiency, and compatible telemetry.

Never create a competing orchestrator, router/ranker, memory engine, or compaction engine without a demonstrated gap and acceptance proof.

## Current runtime contract

Provider/model: fas-router/auto.
Commands: /fas-router:on, /fas-router:off, /fas-router:status, /token-efficiency.
Knowledge: ~/.pi/agent/fas-knowledge.json, bounded v1 store, threshold-based learning and recovery.

## Verified baseline

Pi baseline: 0.85.1.
Regression lineage: 469/469 GREEN.
Leg 1: CLOSED.
L6: CLOSED.
Leg 2: CLOSED.
Phase 1 runtime closure: COMPLETE.

Current fingerprints from the most recent documented Phase-2 state must be rechecked from source before release packaging:
- FAS core: cb24e664 after safety redaction hardening.
- FAS index: 669fdeb7.
- compose: 59a2b7e5.
- subagents tool-list: 8426bc05.
- workflow runner changed by F/E seams; current value in latest report: 74434c36.

## Phase 2 status

B Child Result Contract: COMPLETE, 351/351.
C Role + Capability Mapping: COMPLETE, 396/396; role-call-site wiring deferred unless a real orchestrator role field exists.
A Pi Skills: COMPLETE, 440/440; declarative on-demand policy only, no executable routing math in Skills.
F Safety Gates: COMPLETE, 440/440; pre-spawn destructive Git/scope gates and secret-value redaction; Pi 0.85.1 in-execution veto remains a documented platform/API limitation.
E Workflow Resume: COMPLETE, 458/458; cross-session/multi-process live proof remains UNKNOWN.
D Local Provider Discovery: PARTIAL, 469/469; discovery/validation/unavailable paths proven, suitable-provider live proof BLOCKED without a real daemon.

## Canonical evidence

All dated reports are under docs/FAS_PI/reports/.

The complete autonomy operating contract is under docs/FAS_PI/autonomy/:
AUTONOMOUS_OPERATOR_MANDATE.md
EXECUTION_PROTOCOL.md
TASK_QUEUE.md
FINALIZATION_AND_HANDOFF.md
LAUNCH_PROMPT.md

## Current project milestone

AUTONOMOUS FULL-SYSTEM COMPLETION PROGRAM.

Order:
1. reconcile state and evidence;
2. close only justified residuals;
3. full source/code/security/YAGNI/TDD/efficiency audit;
4. consolidate evidence-backed fixes;
5. Pi compatibility matrix;
6. clean-room portability;
7. final autonomous E2E;
8. final security/YAGNI/release audit;
9. handoff package;
10. stop at FINAL-HANDOFF-READY: USER-APPROVAL-REQUIRED.

## Anti-hallucination rule

For every material claim:
GitHub source -> focused test -> relevant full regression -> runtime proof when required -> report -> state update.

Use VERIFIED, HISTORICAL, REPORTED, UNKNOWN, BLOCKED, DEFERRED.

Never convert an unverified claim into a verified claim by repetition or memory.
