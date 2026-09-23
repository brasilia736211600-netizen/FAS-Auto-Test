# FAS-Pi Workflow State

Updated: 2026-09-23

## State

`RELEASE-STABLE-WITH-PLATFORM-LIMITATIONS`

Current baseline Pi version: `0.85.1`

Current provider/model: `fas-router/auto`

Current GitHub repo used for Linux runtime proof: `brasilia736211600-netizen/FAS-Auto-Test`

Current branch: `fas-feature-test`

Latest GitHub baseline commit before the Phase-2 documentation updates: `c91f65409469e92271a05f0a93394d6e087ce356`.
Current HEAD is advanced by documentation/report updates; inspect GitHub before making source changes.

## Main test baseline

**324/324 GREEN**

Component historical counts:

`21 + 13 + 9 + 64 + 57 + 37 + 75 + 12 + 11 + 25`

Do not replace this baseline with a smaller focused-suite result.

## Closed work

- FAS compaction reentrancy regression fixed.
- Thinking API corrected to Pi-native APIs.
- Minimum-sufficient thinking and evidence escalation proven.
- maxOutputTokens enforcement proven.
- Provider discovery/routing hardening proven.
- Bounded fallback (3 candidates + max one previous-model delegation) proven.
- Learning threshold/recovery/persistence/corrupt-state behavior proven.
- /compose release contract proven and frozen.
- 2E Subagents/FAS seam complete.
- 2F Workflow/FAS seam complete.
- 2G evidence gate: NO-2G.
- Comprehensive architecture audit recorded.
- Codespace Linux child path (Leg 1) live-closed.
- L6 all-candidates-fail/no-previous-model live-closed.
- Codespace Node/Pi toolchain default repair complete.
- Leg 2 Workflow success-path turn live-proven (2026-09-23; report
  `docs/FAS_PI/reports/LEG2_WORKFLOW_SUCCESS_2026-09-23.md`; 324/324 re-verified).
- B Child Result Contract implemented for subagents (2026-09-24; report
  `docs/FAS_PI/reports/2026-09-24_B_CHILD_RESULT_CONTRACT.md`; 351/351 GREEN).
- C Role+Capability mapping implemented (2026-09-24; report
  `docs/FAS_PI/reports/2026-09-24_C_ROLE_ROUTING.md`; 396/396 GREEN).
- A minimal Pi Skills implemented (2026-09-24; report
  `docs/FAS_PI/reports/2026-09-24_A_PI_SKILLS.md`; zero source changes).
- F minimal safety gates implemented (2026-09-24; report
  `docs/FAS_PI/reports/2026-09-24_F_SAFETY_GATES.md`; 440/440 GREEN).

## Open work

### CLOSED-1 — Leg 2 (proven 2026-09-23)

Proved (evidence: `docs/FAS_PI/reports/LEG2_WORKFLOW_SUCCESS_2026-09-23.md`):

`Workflow success path -> child -> FAS extension loaded -> fas-router/auto -> real provider turn -> workflow success`

Fresh ps-captured child argv with `-e <fas>` + `--model fas-router/auto`, FAS
routing active, exact-output provider turn (`LEG2-PROBE-OK`), phase `succeeded`,
`Workflow finished`, credential presence-only, staging cleaned, 324/324 GREEN,
no unrelated diff.

### OPEN-2 — Post-Leg-2 enhancement review (audit complete, implementation pending)

Only after Leg 2:

1. reconcile all current GitHub state;
2. rerun the full suite;
3. inspect whether Pi Skills can express stable FAS policy without runtime duplication;
4. design a minimal child-result contract;
5. design role/capability profiles;
6. evaluate local provider discovery;
7. evaluate durability only if a current gap remains;
8. evaluate safety/permission gate only where an actual gap is demonstrated;
9. evaluate optional theme last.

## Execution policy

Use:

`READ -> VERIFY -> RECONCILE -> PLAN -> EXECUTE -> TEST -> DIFF -> REVIEW -> COMMIT -> SAVE STATE`

For runtime proof:

`prepare -> verify prerequisites -> run one target leg -> capture evidence -> clean secrets/runtime -> stop environment -> save result`

## Parallelism rule

Parallelize only independent work. Never run concurrent edits against the same production boundary unless ownership and merge semantics are explicit.

Safe parallel candidates after Leg 2:

- Pi Skills inventory;
- child result contract design;
- local provider capability research;
- durability gap analysis;
- safety/permission gap analysis.

Do not parallelize changes to the same source file.

## State updates

Every completed milestone must update:

- this file;
- `MASTER_PROJECT_MAP.md`;
- `RESUME.md`;
- `ROADMAP.md` if sequence/status changed;
- a dated evidence report when a runtime claim changed.

Never modify state docs to hide a failure. Preserve the failure class and exact evidence.

## Current environment limitation

Android/Termux cannot currently provide the Linux child cgroup-v2 runtime path used for the required child proof. Linux Codespace is therefore the validation environment for Leg 1/2.

This is a platform limitation, not a reason to bypass safety gates.

## Credential handling

A provider credential is a prerequisite for the real-provider leg. It must exist in the same process environment that launches Pi. Presence may be tested; the value must never be printed or persisted in these docs.

## Completion gates

Phase 1 runtime closure is COMPLETE because Leg 1, L6, and Leg 2 have fresh evidence and the 324/324 suite was re-verified.

For every future milestone, do not accept source changes, passing unit tests, or an agent statement alone as completion proof. Use the evidence chain in `GITHUB_WORKFLOW.md`.
