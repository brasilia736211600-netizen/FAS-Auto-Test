# 2026-09-24 — C: Role + Capability Mapping IMPLEMENTED

Scope: Phase-2 item C ONLY (after B green). Role→constraint mapping using ONLY the
existing centralized FAS scorer/ranker. No second ranker, no per-role model lists,
no LLM role inference. No packages, no `/compose` change.

Labels: VERIFIED (fresh evidence this run) · REPORTED (prior claims) · UNKNOWN.

## 1. Verdict: PASS — C implemented, 396/396 GREEN, docs-only commit in FAS-Auto-Test

## 2. TDD baseline-FAIL-first (VERIFIED)

- Wrote `~/fas-verify/tests/test-fas-role-routing.mjs` (45 assertions) BEFORE the
  implementation. Baseline: `Cannot find module '.../fas/roles.ts'`. One assertion
  was corrected during development (explorer top-pick: asserted exact model id,
  scorer correctly preferred the cheaper non-reasoning model — assertion narrowed
  to the honest property `reasoning === false`; behavior was right, test was
  over-specific).

## 3. Implementation (1 new file, ZERO modifications to existing files)

- NEW `~/.pi/extensions/fas/roles.ts` (pure: no imports, no I/O, no model calls):
  - `roleTaskConstraints(role)` for `explorer/implementer/tester/reviewer/debugger`:
    explorer `{needsReasoning:false}`, implementer `{}`, tester
    `{needsReasoning:false}`, reviewer `{minContextWindow:64000}` (explicit tested
    policy floor), debugger `{needsReasoning:true}`. Every key is a pre-existing
    `hardFilter`/scorer field (test-locked: unknown keys fail the suite).
  - No `resolveRole`/`classifyRole` export — role choice is explicit by the
    orchestrator (test-locked absent). No scores/weights anywhere in the module.
  - `rolePromptSnippet(role)` — 3-line emission instruction (fence + required
    fields), pay-per-role-use, NOT a global prompt change (zero token cost until used).
  - `validateRoleContract(role, parsed)` — enforces role-required fields on
    status `ok` only (`tester` requires non-empty `tests_run`); `fail`/`blocked`
    never rejected (honest failure stays legal); never throws.
- Core `scoreCandidate`/`rankCandidates`/`hardFilter`/`planFallback` untouched.

## 4. Test evidence (VERIFIED)

- Focused C suite **45/45**: exact shapes (5) · key-allowlist/no-weights (15) ·
  unknown-role-throws + no-classifier (3) · determinism ×3 per role (5) · steering
  via existing ranker (5: explorer/debugger/reviewer/implementer/tester-evidence) ·
  fail-safe under roles (3) · snippets + validation (9).
- Full suite **396/396 GREEN** (351 prior + 45 new), 0 failures.
- `node --check` clean. Upstream `bun:test` suites unrunnable on Termux
  (PLATFORM-LIMITED, no upstream files touched).

## 5. Diff proof

- `~/.pi/extensions/fas/`: `?? roles.ts` only. `core.ts` fingerprint still
  `33aa88d5`; subagents/workflow seams untouched (fingerprints match).
- `~/FAS`: this report + state edits, docs-only; `git diff --check` clean; pushed;
  remote tree verified.

## 6. Deferred

- Wiring `rolePromptSnippet` into role-spawn call sites (workflow phase config /
  Autopilot): needs an orchestrator-declared role field — next-step work, not
  speculated here. `validateRoleContract` is ready for the `publishCompletion`
  seam when a role is declared (B seam passes results through today).
- `researcher` role: dropped per audit (no distinct tool/capability need vs
  explorer). Vision capability: dropped (no vision tool in the 0.85.1 FAS path).
