# FAS-Pi Resume Procedure

Updated: 2026-09-24

## Mandatory first read

1. docs/FAS_PI/README.md
2. docs/FAS_PI/GITHUB_WORKFLOW.md
3. docs/FAS_PI/autonomy/AUTONOMOUS_OPERATOR_MANDATE.md
4. docs/FAS_PI/autonomy/EXECUTION_PROTOCOL.md
5. docs/FAS_PI/autonomy/TASK_QUEUE.md
6. docs/FAS_PI/autonomy/FINALIZATION_AND_HANDOFF.md
7. docs/FAS_PI/MASTER_PROJECT_MAP.md
8. docs/FAS_PI/WORKFLOW_STATE.md
9. docs/FAS_PI/ROADMAP.md
10. all relevant files under docs/FAS_PI/reports/

Then inspect current GitHub HEAD, branch, source, tests, and diff before changing anything.

## Current state

Phase 1 runtime closure: COMPLETE.
Phase 2 implemented scope: substantially complete.
Current regression lineage: 469/469 GREEN.
D suitable local-provider proof: BLOCKED without a real daemon.
E multi-process resume proof: UNKNOWN.
C role-call-site wiring: DEFERRED unless a real orchestrator role field exists.

## Immediate instruction

Do not rerun completed legs or Phase-2 work merely to reconfirm them.

Start from autonomy/TASK_QUEUE.md and perform the next incomplete evidence-backed item. Use Subagents for independent work with explicit ownership and structured results.

## Per-item loop

READ -> VERIFY -> RECONCILE -> PLAN -> FAIL-FIRST -> MINIMAL CHANGE -> FOCUSED TEST -> FULL REGRESSION -> DIFF/SECURITY/YAGNI REVIEW -> RUNTIME PROOF WHEN REQUIRED -> REPORT -> STATE UPDATE -> COMMIT -> PUSH -> REMOTE VERIFY -> CHECKPOINT -> NEXT

## Interruption recovery

After any interruption:
1. reconnect to a suitable environment;
2. read the canonical files above;
3. inspect Git HEAD and diff;
4. find the latest report/checkpoint;
5. continue from the first incomplete queue item;
6. rerun only evidence invalidated by the interruption.

Never reconstruct state from chat memory.

## Final gate

When all technical work is complete, run the finalization program and create handoff artifacts.

Stop only at:
FINAL-HANDOFF-READY: USER-APPROVAL-REQUIRED

The final repository is not created before explicit approval.
