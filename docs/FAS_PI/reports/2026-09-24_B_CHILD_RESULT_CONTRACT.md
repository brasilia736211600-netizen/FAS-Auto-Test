# 2026-09-24 — B: Child Result Contract (subagents) IMPLEMENTED

Scope: Phase-2 item B ONLY (audit order B→C→A→F→E→D). Minimal structured envelope
for subagents children + parent validation, without replacing workflow's existing
`workflow_phase_result` tool (untouched). No packages, no second system, no
`/compose` change, no prompt/behavior change for unstructured children.

Labels: VERIFIED (fresh test/source evidence this run) · HISTORICAL (prior state) ·
REPORTED (prior claims, not reproven) · UNKNOWN (insufficient evidence).

## 1. Verdict: PASS — B implemented, 351/351 GREEN, docs-only commit in FAS-Auto-Test

## 2. TDD baseline-FAIL-first (VERIFIED)

- Wrote `~/fas-verify/tests/test-fas-child-contract.mjs` (27 assertions) BEFORE the
  implementation. Baseline run: `Error: Cannot find module
  '.../subagents/runtime/child-contract.ts'` — B1 fails on current source. (HISTORICAL
  note: 2E/2F used the same jiti-harness pattern.)

## 3. Implementation (minimal seam, 1 new file + 6 lines)

- NEW `~/.pi/pi-enhanced/extensions/subagents/runtime/child-contract.ts` (pure:
  no imports, no I/O, no Pi coupling):
  - `buildChildResult()` — child-side builder, fenced ```` ```fas-result ```` JSON
    block; envelope `{status, report, files_modified, files_created, tests_run,
    problems, conflicts, data?}`; `status ∈ {ok, fail, blocked}` (required),
    `report` non-empty (required), list fields default `[]`, `data` optional
    object; throws on invalid input (fail fast at source).
  - `parseChildResult()` — parent-side validator; NEVER throws; returns
    `{valid:true,result,raw}` or `{valid:false,errors,raw}`; raw always preserved.
- SEAM `runtime/collaboration-manager.ts::publishCompletion` (+1 import, +5 lines):
  parses the completion payload and attaches the contract ONLY when valid:
  `details: {...activity, childResult}` vs today's `details: activity` for
  unstructured payloads (byte-identical fallback — existing fields untouched,
  no new requirements, no wire-protocol change).
- NOT changed: `canonicalCompletionPayload`, `taskEnvelope`, broker protocol,
  workflow `workflow_phase_result` tool, any prompt text, FAS core, Pi core.

## 4. Test evidence (VERIFIED)

- Focused B suite: **27/27 GREEN** (B1 build 5 · B2 parse 4 · B3 reject 12 across
  6 invalid shapes · B4 passthrough 3 · B5 real-funnel composition 3, incl.
  `canonicalCompletionPayload("completed"|"errored")` round-trip and plain-text
  passthrough).
- Full durable suite: **351/351 GREEN** (324 baseline preserved: 21+13+9+64+57+37
  +75+12+11+25; +27 new), 0 file failures.
- Syntax: `node --check` clean on both touched files.
- Integration-load check: full `collaboration-manager.ts` jiti import fails
  IDENTICALLY at unmodified HEAD (missing `typebox`/bundled-module resolution in
  this harness) — pre-existing harness limitation, not a regression. Upstream
  subagents `bun:test` suites cannot run on Termux (no bun) — PLATFORM-LIMITED;
  no upstream test file was modified.

## 5. Diff proof

- `~/.pi/pi-enhanced` (h4ni0/pi checkout): `M runtime/collaboration-manager.ts`
  (seam only), `?? runtime/child-contract.ts` (new), plus the two pre-existing
  2E/2F seams (`tool-list.ts`, workflow `runner.ts`). FAS ext, compose, Pi core,
  Autopilot untouched (fingerprints re-verified match).
- `~/FAS` (FAS-Auto-Test @ `fas-feature-test`): this report + 3 state-doc edits,
  docs-only. `git status` clean after commit; `git diff --check` clean; pushed and
  remote tree verified.

## 6. Deliberately deferred (not speculation — dependency-ordered)

- Child-side emission instruction in subagent prompts: deferred to **C** (tester
  role requires `tests_run`; role-gated prompt is the correct vehicle, avoiding a
  global prompt change + per-child token cost now). Parent accepts envelopes today.
- Workflow-side adoption: nothing to do — its structured tool already satisfies
  the contract pattern.

## 7. Cleanup

No credentials involved (pure offline unit work). No Codespace used. No staging
files left behind (one `~/fas-verify/tests/test-fas-child-contract.mjs` kept as
the durable gate).
