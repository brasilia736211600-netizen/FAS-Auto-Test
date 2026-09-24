# 2026-09-24 — Queue 7 Final Security/YAGNI/Release Audit

Scope: final proof-pass over the whole production boundary (13 files, §1),
security + secrets, YAGNI/dead-code, docs consistency. No speculative changes.

Labels: VERIFIED (fresh evidence) · DEFERRED (documented) · residual UNKNOWN.

## 1. Boundary inventory (one responsibility each)

- fas/core.ts (622): evidence-weighted routing/scoring/fallback/thinking + redact.
- fas/index.ts (100): provider registration, KB persistence, streamSimple wiring.
- fas/roles.ts (117): role→constraint mapping + snippets + role validation.
- fas/local-providers.ts (150): loopback discovery + capability validation.
- autopilot/index.ts (363): bounded code-task loop (8 rounds) + checkpoints.
- workflow/runner.ts (879): phase dispatch (2F argv, F gate, E resume, P fan-out).
- workflow/schema.ts (809): definition validation (incl. fanout/resume shapes).
- workflow/resume.ts (65) + safety.ts (64): pure resume/safety helpers.
- subagents/collaboration-manager.ts (2695): child lifecycle (+B contract attach).
- subagents/runtime/tool-list.ts (187): spawn extension inheritance (2E seam).
- subagents/runtime/child-contract.ts (150): envelope build/parse.
- subagents/prompts.ts (93): system prompts + completion payload funnel.

## 2. Concrete fix from this audit (TDD, 5/5)

- Autopilot `checkpointIfRepo` ran `git add -A`: untracked files (`.env`,
  keys) auto-committed into user history. Fixed to `git add -u` (tracked
  modifications only) + exported for testability.
  (`~/fas-verify/tests/test-fas-autopilot-safety.mjs`, 5/5; fingerprint
  `0b542928`→`8c038dad`.) No other destructive git found boundary-wide.

## 3. YAGNI verdict: nothing deleted (evidence-backed)

- Uncalled-by-production exports (role mapping/validation/snippets, local
  validate/probe, resume extractors, contract builder) are roadmap-required API
  with tests and named DEFERRED consumers (C wiring, D admission, role emission).
  Deleting them would contradict the approved plan; keeping them costs zero
  runtime tokens (never loaded unless imported).
- No duplicate router/ranker/orchestrator/memory/compaction (grep-verified).
- `spawn_many` tool and FAS fallback racing explicitly rejected (existing
  spawn+wait-all suffices; racing corrupts the single output stream).

## 4. Security verdict

- execSync surfaces: autopilot `command -v` uses static list only; `runTests`
  executes the USER's own command (owner trust, bounded 180s); no
  model-controlled shell interpolation anywhere in boundary.
- Secrets: FAS evidence redacted incl. value-shapes (F); autopilot untracked
  exclusion (this audit); workflow snapshots persist raw task text in session
  JSONL (pi-core behavior, outside boundary — residual: never paste live keys
  into tasks).
- `cloud-offload.yml` `${{ inputs.run }}`: trigger requires write access
  (owner-trust equivalent to push) — acceptable, documented.
- Pushed-docs secret scan: clean.

## 5. Lineage repair (this report)

Full chain now on record: 324 → 351 (B) → 396 (C) → 420 (A, intermediate,
observed 2026-09-24) → 440 (F) → 458 (E) → 469 (D) → 489 (autopilot safety 5 +
fan-out 15) → pytest 84/84 (cloud offload). Final: **489 + 84, 0 failures.**

## 6. Docs consistency

reports/README indexes all 12 reports; WORKFLOW_STATE carries per-item totals;
TASK_QUEUE has Queue 4B; no stale duplicates found (Queue 0 reconciliation holds).
