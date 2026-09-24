# 2026-09-24 — Parallel Fan-out/Fan-in (workflow) IMPLEMENTED

Scope: user-ordered parallel-work feature ("add it if missing"). Investigation
VERIFIED it was missing at every layer: workflow strictly sequential (single
`while` loop), FAS fallback sequential by output-stream safety (racing full
turns would corrupt the single output — documented, not implemented), subagents
guidance advisory-only. Implemented the one correct layer: workflow fan-out.

Labels: VERIFIED (fresh evidence this run).

## 1. Verdict: PASS — fan-out implemented, 489/489 GREEN, docs-only commit

## 2. TDD baseline-FAIL-first (VERIFIED)

`~/fas-verify/tests/test-fas-workflow-fanout.mjs` (15 assertions) written first;
baseline: `phase 1: unknown field: fanout`. (Test-file spiral cut short: one
typo fixed during writing — `};` vs `};` — caught by direct run, not review.)

## 3. Implementation (schema + contained runner seam)

- `schema.ts` (`f95a471c`): `WorkflowPhase.fanout?: string[]`; `parseFanout` +
  `validatePhaseFanout` (targets exist, no self/dupes, no `next` on fanning
  phase, no `next`/`fanout` on targets — v1 unambiguous join semantics).
- `runner.ts` (`c20f921d`): `runFanoutTargets()` — concurrent `runPhase` via
  `Promise.allSettled` with shared outputs map; all-of join (first failure
  aborts through the standard path); continue AFTER last target; consumed-set
  prevents re-runs; transitions budgeted; resume outputs adopted per target
  (fan-out composes with E resume instead of breaking it).
- `activeClients: Set` replaces single-client assumptions in abort/shutdown
  (superset of old behavior for linear runs); steer during fan-out reaches the
  most-recent child (documented v1 limitation, same as today's single-phase
  behavior generalized).

## 4. Test evidence (VERIFIED)

- Focused **15/15**: schema accept + 5 rejections · rendezvous overlap proof
  (max in-flight 2 — sequential execution would time out and fail) · join
  (spawn order a-first/d-last, all spawned once, merged report) · failure
  propagation (run fails, both forks attempted) · no-fanout byte-identical.
- Full suite **489/489 GREEN** (474 prior + 15), 0 failures. `node --check`
  clean. Upstream bun suites PLATFORM-LIMITED, untouched.

## 5. Diff proof

- pi-enhanced: `M schema.ts`, `M runner.ts` (4 seams: 2F argv + F gate + E
  resume + P fan-out). Untouched: everything else (fas core `cb24e664`,
  roles, safety, resume, child-contract, compose `59a2b7e5`, tool-list
  `8426bc05`, Pi core, Autopilot).
- `~/FAS`: this report + state edits, docs-only; `git diff --check` clean;
  pushed; remote tree verified.

## 6. Deliberately not done

- Concurrent FAS fallback racing: UNSAFE (single output stream) — documented,
  not implemented. FAS-side parallelism stays at zero by design.
- `spawn_many` tool: existing spawn + wait-all already achieves parallel
  spawning; a dedicated tool adds no capability (YAGNI).
- Fan-out target `next` rules: rejected by validation (v1 join semantics).
