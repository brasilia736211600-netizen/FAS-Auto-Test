# FAS-Pi Autonomous Task Queue

Updated: 2026-09-24

## Current state

Leg 1, L6, Leg 2: VERIFIED CLOSED.
Phase-2:
- B Child Result Contract: VERIFIED COMPLETE.
- C Role + Capability Mapping: VERIFIED COMPLETE; call-site wiring deferred unless a real role field exists.
- A Pi Skills: VERIFIED COMPLETE.
- F Safety Gates: VERIFIED COMPLETE; Pi 0.85.1 in-execution veto limitation remains documented.
- E Workflow Resume: VERIFIED COMPLETE; cross-session/multi-process proof remains UNKNOWN.
- D Local Provider Discovery: VERIFIED PARTIAL; suitable live-provider proof BLOCKED without a daemon.
Current documented regression lineage: 469/469 GREEN.

## Queue 0 — State reconciliation

1. Reconcile all canonical docs with all Phase-2 reports and Git commits.
2. Remove duplicate/stale roadmap sections and stale report paths.
3. Ensure each completed item has one canonical report and commit reference.
4. Verify the actual suite count from the current source/runtime.
5. Create a checkpoint.

## Queue 1 — Residual engineering

1. D suitable-provider live proof only on a host with a real daemon.
2. D registry-admission seam only if current Pi boundary permits it and evidence shows it is needed.
3. E real cross-session/multi-process resume proof when a suitable environment exists.
4. C role-snippet wiring only if a real orchestrator role field already exists.

## Queue 2 — Full-system audit

Run independent read-only passes over every production-relevant FAS, Autopilot, Workflow, Subagents, /compose, Skills, provider/routing, knowledge/learning, safety, resume, install/bootstrap, CI, tests, and documentation surface.

Audit dimensions:
correctness, security, reliability, token/context efficiency, YAGNI, tests, portability, observability.

## Queue 3 — Consolidation

Every finding requires:
concrete deficiency -> smallest fix -> FAIL-FIRST -> focused pass -> full regression -> independent review -> report/state -> commit/push.

Never batch unrelated source changes merely to reduce commit count.

## Queue 4 — Pi compatibility

Build a matrix for Pi 0.85.1 and the current Pi release line. Do not move the production baseline until test parity and parent/child runtime parity are proven and /compose remains intact.

## Queue 4B — Cloud offload option (weak-phone directive)

The operator phone is weak: heavy jobs (app builds, test suites, long runs)
must be runnable on free cloud resources instead of Termux, as an option.
Standing solution: reusable `cloud-offload.yml` (workflow_dispatch) +
`fas offload` dispatcher (dispatch/wait/download) + per-repo `offload-build.sh`
convention. Status: IMPLEMENTED (report
`docs/FAS_PI/reports/2026-09-24_CLOUD_OFFLOAD.md`). Remaining: per-app
`offload-build.sh` files (e.g. Android APK builds) land with their own repos
and evidence, not here.

## Queue 5 — Clean-room portability

Prove installation and autonomous execution on an unrelated repository without copying project source into that target. Include persistence and Subagents where supported.

## Queue 6 — Final autonomous E2E

Exercise discovery -> planning -> implementation -> Subagents -> FAS routing -> bounded fallback -> tests -> verification -> safe Git -> CI -> bounded recovery -> state save.

## Queue 7 — Final security/YAGNI/release audit

Inspect all relevant files for dead code, duplicate abstractions, stale shims, unnecessary dependencies, unsafe shell/Git paths, secret leakage, misleading docs, and untested behavior. Simplify only with regression evidence.

## Queue 8 — Final handoff

Produce validated release package and proposed final repository. Stop at:
FINAL-HANDOFF-READY: USER-APPROVAL-REQUIRED

## Rule

DONE requires report + tests + commit + state update.
BLOCKED, DEFERRED, REPORTED, UNKNOWN are not DONE.
