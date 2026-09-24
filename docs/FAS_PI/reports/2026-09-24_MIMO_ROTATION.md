# 2026-09-24 — Working-Lane Rotation: mimo-v2.6-flash Replaces big-pickle

Status: ROTATED + PROVEN. mimo-v2.6-flash (alias form) serves on BOTH
hosts (Termux + codespace, live replies); cloud workflow E2E on mimo →
MIMO-E2E-DONE VERIFY-PASS (`// E2E-MARKER` on disk, `E2E-TEST-OK`).
Zero source changes, zero commits to extensions (docs-only).

## 1. Why the rotation

big-pickle served 5 straight on cloud then went silent in KB (UNSEEN
locally — shared-IP quota shifts per host/hour). mimo-v2.6-flash-free
was already triple-verified (FF/MIMO/LING batch + KILO-TUI session).
Rotation policy: working set = lanes green TODAY on BOTH hosts.

## 2. Alias vs full id (measured, both forms green)

`freeflow/mimo-v2.6-flash-free` and alias `freeflow/mimo-v2.6-flash`
(both resolve per models.ts:504) serve on both hosts. Canonical
working id: **`freeflow/mimo-v2.6-flash`** (short alias form; KB keys
whatever id the turn actually used).

## 3. Model behavior note (measured, not assumed)

mimo is `reasoning: true` with `off: null` in its thinking map:
default-effort turns return `content: null` + root usage intact
(`prompt 363 / completion 14` — tokens spent, text withheld), while
`--thinking high/medium` returns real text (`Hello there`).
Handling: drive mimo turns at high/medium (FAS `decideThinking` already
raises off→min-sufficient per B1; mimo's map starts at low). No source
change — observed behavior folds into existing selection logic.
Watch item: if mimo ever starves the pool at default effort, pin its
floor explicitly (queued, not started).

## 4. Evidence (secret-free)

- Termux: mimo alias + `--thinking high` → `Hello there`; cloud: same
  → `Hello there`. kilo-auto/free baseline green on both (`Hello
  there.` cloud).
- Cloud session `e2e-mimo-1` (parent mimo-direct): implement edited
  `app.js`, verify VERIFY-PASS; disk `// E2E-MARKER` + `E2E-TEST-OK`.
- Cloud KB before this run: big-pickle SERVED ×5 (prior working set —
  now rotated out, still pool-eligible, breaker-managed).
- Full regression untouched this turn (test-only + docs): 516/516 +
  84/84 stands.

## 5. Current working set (both hosts, today)

PRIMARY: `freeflow/mimo-v2.6-flash`, `freeflow/kilo-auto/free`.
BACKUP: cline-free lanes (168/44/8 historic), openrouter free/OAuth.
POOL (breaker-managed): kilo direct, zai, fhrouter, big-pickle.
PARKED: omniroute (114-byte lander, unchanged).

## Fingerprints (unchanged)

core `155ae074`, index `73239dde`, roles `8395d510`, runner `c20f921d`,
schema `f95a471c`.
