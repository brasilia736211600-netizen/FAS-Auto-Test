# 2026-09-24 — Persistent Provider Breaker (F3 follow-up 2/3)

Status: SHIPPED (core `ac88fe44`→`155ae074`, index `669fdeb7`→`73239dde`,
F7, fallback-learning 43/43, full regression 510/510 node + 84/84 pytest).
Live: PARENT-OK ×3, breaker fields persisting (`cline: consec 0`).

## 1. Gap

Within-turn breaker (F3 v1) stops same-turn lane-burn, but nothing
survived across turns: a credit-dead provider was re-entered every turn
(63 lanes at consec-1). Lane penalties can't fix provider-death — only
provider-level memory can.

## 2. Fix (lane-independent, time-boxed)

- `recordOutcome` maintains `store.providers[p] = {consec, lastSeen,
  lastKind}` (failure +1, success resets; ~15 providers, tiny).
- `providerInCooldown`: `consec >= 2` (THRESHOLD) and
  `now - lastSeen < 30 min` (COOLDOWN) → `shouldSkipCandidate` skips the
  provider's lanes. Single failures never trip; expiry re-admits (credits
  may arrive); success resets.
- Clock threading: `rankCandidates(..., nowMs = Date.now())`,
  `shouldSkipCandidate(..., nowMs)`; production passes `deps.now()`;
  all existing 3-arg callers unaffected (verified by suite).
- `parseKnowledge`/`mergeKnowledge` preserve the rollup; fail-safe
  (empty rank → full pool) still bounds worst case.
- Serialization fix (found live): `index.ts save()` dropped `providers`
  on every write — one-line fix, verified by live KB contents.

## 3. TDD

- F7 (`test-fas-fallback-learning.mjs`): FAIL-first 41/43 → 43/43.
  Pins: single failure no trip, two trip, other providers unaffected,
  rank drops cooled lanes (fail-safe keeps the rest), 30-min expiry,
  success reset.
- Existing threshold pins (F3/F4/C6/D5) pass unmodified — breaker only
  fires on recent homogeneous failure, never on old or proven lanes.
- Full regression: 510/510 node (18 files) + 84/84 pytest, zero
  failures. `node --check` clean on both files.

## 4. Live effect

Three straight bare-parent PARENT-OK turns; last two needed no fallback
(clean cline streaks). KB now carries `providers` + per-lane
`lastError`/`lastStatus` — the next diagnosis (if any) starts with data,
not guessing.

## 5. Remaining (not started)

Cross-turn lane nuance beyond provider scope (diminishing value —
defer unless evidence demands); 0.87 migration checklist; cloud
shortlist eval + Q6-overflow.

## Fingerprints

core `155ae074`, index `73239dde`, roles `8395d510`, runner `c20f921d`,
schema `f95a471c`, compose `59a2b7e5`, tool-list `8426bc05`.
