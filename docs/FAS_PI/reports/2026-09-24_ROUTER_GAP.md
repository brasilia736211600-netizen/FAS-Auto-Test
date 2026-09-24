# 2026-09-24 — Router-Gap Diagnosis + Failure-Observability Fix (F1)

Status: DIAGNOSED + F1 SHIPPED (core `9693922b`→`26f3d323`, T16, 78/78,
full regression 496/496 node + 84/84 pytest). F3 (exploration trap) DESIGNED,
not yet implemented. Extension sources unversioned — fingerprinted below.

## 1. Symptom (live, Termux, reproduced 17:52–17:53)

Bare-parent `fas-router/auto` turn → `all candidates failed or budget
exhausted; no fallback model available`, while direct lanes work
(`CLINE-OK`, openrouter 200). The probe burned 4 fresh kilo lanes, each
`execution:unknown`, status None. KB consec histogram: **63 lanes at
consec-1, 5 at 0** — the router burns ~3 fresh lanes per turn and never
re-tries a lane.

## 2. Root mechanics (code-read + live evidence)

- `maxAttempts = 3`, `fallbackModel = previousModel` (none on bare
  `--no-session` parent) → 3 strikes = terminal verdict. As designed.
- Failing lanes are kilo (credit-dead: cf. 402 `Paid Model` for kilo/lyria)
  whose `streamSimple` THROWS instead of yielding an error event →
  `catch (e)` → `classifyFailure({errorMessage})` → no status →
  `execution:unknown`, retryable → next lane. Per-lane error text was then
  DISCARDED (persist kept reason only) — the exact information needed to
  distinguish "no credits" from "network" never reached the KB.
- Exploration trap (F3, open): `shouldSkipCandidate` fires only at
  consec ≥ 3, but ranking prefers unexplored lanes, so no lane ever
  reaches 3. Penalty (−1.5/failure) never overcomes the fresh-lane supply
  (832 catalog). Verified-failure is unreachable by construction.
- Audited and CLEARED: stats-key alignment (`modelKey` ≡ `failureKey` ≡
  `provider/id`, registry `Model.id` field) — bonus/penalty keys match;
  no fix needed. Registry healthy at probe time (893 models listed, no
  error burst in free.log) — not a registry outage.

## 3. F1 fix (this report's change, TDD)

- `recordOutcome` keeps `lastStatus` (number) + `lastError` (truncated 200
  chars) — bounded, two fields, eviction unchanged.
- All four `persist` sites pass provider `error` (+ `status: 401` on the
  auth path; status already passed on the stream path).
- Test: `test-fas-release.mjs` T16 (FAIL-first 76/78 → PASS 78/78).
- Full regression: node **496/496** (18 files) + pytest **84/84**, zero
  failures. `node --check` clean.

## 4. F3 design (next, needs TDD on cloud or phone)

Cooldown/circuit-breaker: skip consec-1 lanes for N turns (or weight
penalty × consec), plus provider-level breaker when a provider's lanes
fail homogeneously (kilo pattern). Must not regress the 496 baseline;
FAIl-first in `test-fas-discovery-budget.mjs`.

## 5. Cloud decision (recorded)

**Codespace primary, Google Cloud Shell fallback.** Evidence: `gh` authed
(`brasilia736211600-netizen`), existing `Shutdown` codespace
`opulent-space-happiness` on `fas-feature-test` (wake via
`gh codespace ssh`, auto-starts), cgroup-v2 + Leg2 PASS proven there.
GCloud CLI not installed, no project evaluated — fallback only.

## 6. pi.dev excellent-additions queue (from 2026-09-24 research)

- DONE here: none (diagnosis + F1 only, single-finding rule).
- QUEUED: FAS prompt templates (`~/.pi/agent/prompts/fas-*.md`, new files,
  zero source risk); 0.87 breaking checklist → compat matrix/ROADMAP
  (turn_end removal, shouldStopAfterTurn→finishTurn, SessionManager
  canonical); eval shortlist on cloud (dynamic-workflows routing ideas,
  pi-loop durability, smart-compact pipeline, auto-review broker,
  web-access as Firecrawl replacement). Skills already spec-compliant —
  no work.

## Fingerprints

core `26f3d323`, roles `8395d510`, runner `c20f921d`, schema `f95a471c`,
fas index `669fdeb7`, compose `59a2b7e5`, tool-list `8426bc05`;
release suite 78/78 (T16 new).
