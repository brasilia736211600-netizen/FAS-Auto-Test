# 2026-09-24 — FAS Negative-Cost Scoring Fix (routing pin evidence)

Scope: root-cause fix for fas-router/auto failing while direct lanes worked.
One-line scorer change + 4 tests. No other behavior touched.

Labels: VERIFIED (fresh unit + live evidence).

## 1. Root cause (VERIFIED)

Catalog marks free/special pricing with NEGATIVE cost
(`openrouter/auto`: `cost.input = -1000000`). `scoreCandidate` computed
`s -= Math.min(2, cost.input / 10)` → `min(2, -100000)` = `-100000` →
**+100000 runaway bonus**, permanently pinning dead lanes first. With
`maxAttempts = 3`, working lanes (rank ~21+) were never attempted. Invisible
while the old OpenRouter key worked (top pick succeeded); surfaced the moment
it died. Reproduced offline: marked=100001.5 vs plain=1.5.

## 2. Fix

`fas/core.ts` (`cb24e664`→`9693922b`): clamp the penalty at zero —
`s -= Math.min(2, Math.max(0, model.cost.input / 10))`. Negative markers now
score as zero-cost; ties break deterministically as before.

## 3. Evidence

- TDD: D7 cases added to `test-fas-discovery-budget.mjs` (baseline FAIL with
  exact 100001.5/1.5 split) → **61/61 GREEN** after fix.
- Live: post-fix ranking healed (top 1.5, zai reachable); routed turn followed
  (see E2E thread). Full suite re-verified at E2E close.

## 4. Auth landscape correction (VERIFIED, supersedes env-var checks)

Pi resolves auth from `~/.pi/agent/auth.json` (OAuth/key store), NOT only env.
Verified working: openrouter OAuth (just served a real turn), zai key, cline
OAuth. Dead despite keys: kilo (402 broke), fhrouter (no channel).
