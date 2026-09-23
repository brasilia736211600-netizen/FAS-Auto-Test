# FAS-Pi Resume Procedure

Updated: 2026-09-23

## Mandatory first read

A new agent/session must read, in this order:

1. `docs/FAS_PI/README.md`
2. `docs/FAS_PI/GITHUB_WORKFLOW.md`
3. `docs/FAS_PI/MASTER_PROJECT_MAP.md`
4. `docs/FAS_PI/WORKFLOW_STATE.md`
5. `docs/FAS_PI/ROADMAP.md`
6. `docs/FAS_PI/RESEARCH_AND_DECISIONS_2026-09-23.md`

Then inspect the current GitHub branch and relevant source/tests before making any edits.

## Current immediate action

Leg 2 is CLOSED (2026-09-23; `docs/FAS_PI/reports/LEG2_WORKFLOW_SUCCESS_2026-09-23.md`).
B Child Result Contract is COMPLETE (2026-09-24;
`docs/FAS_PI/reports/2026-09-24_B_CHILD_RESULT_CONTRACT.md`).
C Role+Capability mapping is COMPLETE (2026-09-24;
`docs/FAS_PI/reports/2026-09-24_C_ROLE_ROUTING.md`).
Run Phase-2 implementation in audit order: **A → F → E → D** per
`docs/FAS_PI/reports/PHASE2_EVIDENCE_AUDIT_2026-09-23.md`.

Do not spend time redoing closed work. Do not rerun Leg 1, L6, or Leg 2 unless
fresh evidence shows regression.

## Leg 2 acceptance sequence

1. Start/reuse Linux Codespace.
2. Verify the same shell/process has:
   - Node v26.4.0;
   - Pi 0.85.1;
   - Linux platform;
   - `OPENROUTER_API_KEY` present.
3. Never print the key.
4. Run the Workflow success path using effective child model `fas-router/auto`.
5. Capture child argv.
6. Prove FAS extension loading.
7. Prove the real provider request succeeds.
8. Prove the Workflow turn completes successfully.
9. Capture fresh evidence.
10. Stop immediately on missing credentials or unsupported runtime prerequisites.
11. Do not modify FAS/Autopilot/Subagents/Workflow/compose/Pi source during the proof.
12. Clean credential-bearing runtime state.
13. Stop the Codespace.
14. Save the exact result.
15. Update this directory before starting unrelated enhancement work.

## If Leg 2 fails

Classify first:

- `CREDENTIAL_MISSING`
- `TOOLCHAIN_MISMATCH`
- `PROVIDER_FAILURE`
- `CHILD_BOOT_FAILURE`
- `FAS_LOAD_FAILURE`
- `WORKFLOW_FAILURE`
- `TELEMETRY_GAP`
- `UNKNOWN`

Then change the smallest thing necessary. A failure must never trigger speculative architecture changes.

## After Leg 2 passes

Perform the Phase 2 evidence review in roadmap order, but parallelize read-only research where useful:

A. Pi Skills inventory and load/cost analysis.
B. Child result contract draft.
C. Role/capability profile draft.
D. Local provider capability inventory.
E. Durability gap analysis.
F. Safety/permission gap analysis.

Only merge changes that close a demonstrated gap.

## Anti-hallucination protocol

For any future claim:

`claim -> source -> test -> runtime proof when needed -> state update`

Use these labels:

- `VERIFIED`: directly supported by current source/test/runtime evidence.
- `HISTORICAL`: true of an earlier recorded state.
- `REPORTED`: reported by a prior agent/run but not freshly reproven.
- `UNKNOWN`: insufficient evidence.
- `BLOCKED`: required prerequisite unavailable.

Never upgrade UNKNOWN/REPORTED to VERIFIED by assumption.

## No-secret protocol

The context directory is public-safe documentation.

Never write:

- API keys;
- access tokens;
- cookies;
- passwords;
- private authentication payloads;
- raw secret-bearing environment dumps.

Use presence-only language for credentials.
