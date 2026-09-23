# 2026-09-24 — F: Minimal Safety Gates IMPLEMENTED

Scope: Phase-2 item F ONLY (parallel with A, independent file ownership).
Deterministic gates from the audit: forbidden destructive Git ops in Pi child
execution, external-write/workspace-scope declaration checks, secret-boundary /
redaction hardening. No second permission framework, no interactive approval
loop. No packages, no `/compose` change.

Labels: VERIFIED (fresh evidence this run) · UNKNOWN (residual risks).

## 1. Verdict: PASS — F implemented, 440/440 GREEN, docs-only commit in FAS-Auto-Test

## 2. TDD baseline-FAIL-first (VERIFIED)

`~/fas-verify/tests/test-fas-safety-gates.mjs` (20 assertions) written first;
baseline: `Cannot find module '.../workflow/safety.ts'`. (A harness alias lesson
re-learned honestly: runner.ts needs the `pi-coding-agent` jiti alias that the
2F suite already uses — test-only fix, no source impact.)

## 3. Implementation (2 new/pure + 2 minimal seams)

- NEW `workflow/safety.ts` (pure, node:path only): `scanTaskText(text, cwd)` →
  violations, never throws. Forbidden git list mirrors proven
  `~/FAS/fas_git.py::FORBIDDEN_GIT_OPERATIONS` (`reset --hard`, `clean -f*`,
  `push --force/-f`; legit `push`/`status` pass). Scope rule flags absolute paths
  outside cwd + `..` escapes; relative/in-cwd paths pass.
- SEAM `runner.ts::runPhase` (+import, +10 lines): gate runs on the rendered
  prompt BEFORE persist/spawn; denials throw `WorkflowRunError("FAS safety gate
  denied phase…")` through the standard phase-failure path. Clean tasks are
  byte-identical to today.
- HARDENING `fas/core.ts::redact` (+2 lines, fingerprint `33aa88d5`→`cb24e664`):
  credential-shaped VALUES (`sk-or-v1-`, `sk-ant-`, `sk-`, `ghp_`,
  `github_pat_`, `xox[bap]-`) redacted even under neutral keys — a REAL gap
  found by testing (old code only matched key NAMES). Numeric telemetry and
  normal strings still pass.
- Deliberately NOT done (evidence-backed, not dodged): in-execution tool veto is
  impossible — `tool_execution_start` handlers return void (VERIFIED in Pi 0.85.1
  `ExtensionAPI` types), so the spawn gate is the enforceable layer; scorer
  "demotion" is realized as dispatch denial (no unproduced scorer branch was
  added — speculative per project rule); subagents spawn-path wiring deferred
  (same helper is ready; spawn registration graph doesn't load under the jiti
  harness — REPORTED limitation).

## 4. Test evidence (VERIFIED)

- Focused F suite **20/20**: git scan 7 · scope+null-safety 5 · live `runPhase`
  gate via 2F-style FakeClient harness (gated task fails with "safety gate",
  clean task succeeds) 3 · value-shape redaction 5.
- Full suite **440/440 GREEN** (420 prior + 20 F), 0 failures. `node --check`
  clean on all touched files. Upstream bun suites PLATFORM-LIMITED, untouched.

## 5. Diff proof

- pi-enhanced: `M runner.ts` (2 seams: 2F + F), `?? safety.ts`.
- fas ext: `M core.ts` (redact only; new print `cb24e664`), `?? roles.ts` (C).
  Untouched: fas index (`669fdeb7`), compose (`59a2b7e5`), tool-list (`8426bc05`),
  Pi core, Autopilot.
- `~/FAS`: this report + A report + state edits, docs-only; `git diff --check`
  clean; pushed; remote tree verified.

## 6. Residual risks (UNKNOWN, explicit)

- A model child can improvise destructive commands mid-turn that no static
  pre-spawn scan sees (no veto API). Mitigations in place: `--no-approve` trust
  default preserved, phase tools lists unchanged, failures stay explicit.
- Bare `reset --hard` without a `git` prefix is not flagged (documented
  limitation; git-anchored forms are).
