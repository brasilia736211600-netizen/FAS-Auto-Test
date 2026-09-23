# FAS-Pi Roadmap

Updated: 2026-09-23

## Phase 0 — Baseline preservation
Status: COMPLETE

- Freeze Pi baseline at 0.85.1 for the current proof cycle.
- Preserve 324/324 green baseline.
- Preserve /compose.
- Preserve closed seams and runtime evidence.

## Phase 1 — Runtime proof closure
Status: COMPLETE (2026-09-23)

### 1.1 Toolchain
COMPLETE

- Node default = 26.4.0.
- Pi = 0.85.1.
- Linux platform confirmed.
- Existing nvm reused.
- No repository source changed.

### 1.2 Leg 1
COMPLETE

- Linux child runtime path proven.
- FAS extension load proven.
- child argv proof captured.
- real child completion proven.

### 1.3 L6
COMPLETE

- all-candidates-fail/no-previous-model path live-proven cleanly.

### 1.4 Leg 2
COMPLETE (2026-09-23)

One real provider turn through Workflow child under `fas-router/auto` — proven.

Acceptance evidence (all captured in `docs/FAS_PI/reports/LEG2_WORKFLOW_SUCCESS_2026-09-23.md`):

- credential visible to the same process without value disclosure;
- child argv;
- FAS extension load;
- FAS routing;
- provider request/response success;
- workflow success;
- cleanup.

## Phase 2 — Evidence-backed architecture enhancement
Status: READY TO IMPLEMENT

Evidence audit: `docs/FAS_PI/reports/PHASE2_EVIDENCE_AUDIT_2026-09-23.md` (audits A–F,
read-only, zero source changes). Implementation order: B contract → C roles →
A Skills → F safety → E resume-from-phase → D local provider.

Do these in evidence-first order.

### 2.1 Pi Skills / progressive disclosure
Goal: move reusable declarative policy into on-demand Skills without duplicating executable FAS logic.

Checks:

- identify stable policy text;
- measure context/token effect;
- add only the minimum Skill set;
- verify Pi load behavior;
- regression-test FAS behavior.

Status: COMPLETE (2026-09-24; `docs/FAS_PI/reports/2026-09-24_A_PI_SKILLS.md`).
Key finding: FAS injects zero policy text today, so A avoids future prompt cost
(2 Skills, 1,059 B always-on metadata, bodies on demand, 24 focused, 440/440).
No source modified.

### 2.2 Child Result Contract
Goal: standardize child output as structured evidence.

Minimum candidate fields:

- status;
- files_modified;
- files_created;
- tests_run;
- evidence;
- problems;
- conflicts.

Acceptance (all met 2026-09-24; `docs/FAS_PI/reports/2026-09-24_B_CHILD_RESULT_CONTRACT.md`):

- schema test (27-assertion focused suite, baseline FAIL first);
- parent consumption test (funnel round-trip + valid-only details attach);
- no breakage to existing child dispatch (unstructured payloads byte-identical,
  324 baseline preserved, 351/351 total).

Status: COMPLETE for subagents relay. Child-side emission instruction deferred to
C (role-gated prompt); workflow's existing structured tool left untouched.

### 2.3 Role + Capability Profiles — COMPLETE (2026-09-24)

Implemented as pure role→constraint mapping over existing scorer fields
(`~/.pi/extensions/fas/roles.ts`, zero existing-file modifications):
explorer/implementer/tester/reviewer/debugger, deterministic routing tests,
fallback preserved, no second ranker, no per-role model lists, no LLM inference.
Evidence: `docs/FAS_PI/reports/2026-09-24_C_ROLE_ROUTING.md` (45 focused, 396/396).

Remaining: wiring snippets into role-spawn call sites (needs orchestrator-declared
role field — future step, not speculated).

### 2.3 Role + Capability Profiles
Goal: route based on task needs rather than only model names.

Minimum candidate roles:

- explorer;
- implementer;
- tester;
- reviewer;
- researcher;
- debugger.

Minimum candidate capability metadata:

- reasoning/complexity;
- tool compatibility;
- context capacity;
- vision requirement;
- thinking levels;
- provider availability;
- reliability state.

Acceptance:

- deterministic routing test;
- fallback test;
- no duplicate ranking systems.

### 2.4 Local Provider Resilience
Goal: discover and verify local model providers when available.

Candidates may include Ollama/LM Studio or another Pi-supported local lane.

Rules:

- discovery first;
- capability filter;
- live verification;
- use only when suitable;
- never assume local quality or availability.

Acceptance:

- discovery test;
- unavailable-path test;
- suitable-path test;
- fallback integration test.

### 2.5 Durability
Goal: make long-running work resilient to process/session interruption.

Candidate concepts:

- journal;
- checkpoint;
- receipt;
- lease;
- resume;
- explicit uncertain-external-write handling.

Acceptance requires a demonstrated failure/restart gap. Do not add a durability framework merely because OpenMuse/AlphaCode have one.

### 2.6 Safety/permission boundary
Goal: make autonomous execution policy explicit where current FAS behavior is insufficient.

Possible scope:

- destructive Git operation gate;
- external write review;
- secret boundary;
- workspace scope;
- risky tool classification.

Acceptance requires concrete abuse/regression tests.

Status: COMPLETE (2026-09-24; `docs/FAS_PI/reports/2026-09-24_F_SAFETY_GATES.md`).
Pre-spawn declaration gates (destructive git + out-of-scope paths) in runPhase,
credential value-shape redaction hardening, 20 abuse/regression tests, 440/440.
In-execution veto impossible in Pi 0.85.1 API (observational events only) —
documented residual risk, no speculative framework added.

### 2.7 Theme
Goal: optional observability-oriented FAS TUI theme.

Only display state that already exists:

- route;
- thinking;
- fallback attempt;
- evidence status;
- verification status.

No new runtime state may be introduced merely for cosmetics.

## Phase 3 — Pi compatibility track
Status: FUTURE

Current Pi release is 0.87.1 as of 2026-09-22, while this FAS baseline is 0.85.1.

Do NOT upgrade the baseline directly.

Instead:

1. create a compatibility branch/matrix;
2. run existing tests against 0.87.x;
3. identify actual API/behavior differences;
4. adapt behind compatibility seams;
5. prove parity;
6. only then decide whether the baseline should move.

## Phase 4 — Long-horizon autonomy
Status: FUTURE

Potential target:

`goal -> plan -> execute -> verify -> recover -> checkpoint -> resume -> complete`

with no hidden retries and explicit bounded stop conditions.

## Phase 5 — Android integrated runtime
Status: SEPARATE / FUTURE

The existing `docs/FAS_ANDROID_INTEGRATED_RUNTIME_PLAN.md` belongs to the earlier Android/OpenCode product line. The Pi/FAS enhancement track must not silently conflate with that roadmap.

Any integrated Android runtime work needs its own requirements, architecture, tests, and acceptance gate.

## Phase ordering rule

Never skip a prerequisite phase because a later feature appears attractive.

The sequence is evidence -> smallest implementation -> focused regression -> full suite -> runtime proof -> state save.
