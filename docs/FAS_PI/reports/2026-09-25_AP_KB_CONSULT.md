# 2026-09-25 — /ap No Longer Switches Onto Dead Lanes (FAS-KB Consult)

Status: FIXED + VERIFIED. Extension sources touched (autopilot only).
KB consult is read-only; legacy behavior preserved with empty KB.

## 1. Symptom (user-reported, reproduced in test)

`/ap` on a working direct lane switched to a dead/quota-exhausted lane
(unavailable / free-limit errors). Root cause: `setupReasoningModel`
ranked ONLY by static `REASONING_MODEL_HINTS` + `id.length`, never
consulting FAS evidence — and the working lanes (`mimo-v2.6-flash`,
`kilo-auto/free`, `big-pickle`, `muse-spark`) are not even in the hint
list, so a healthy lane could never win on merit.

## 2. Fix (autopilot `c00cd1ac`, test-only + autopilot-source change)

- `loadApFasKb()` reads `~/.pi/agent/fas-knowledge.json`
  (`AP_FAS_KB_PATH` override for tests); missing/corrupt → null KB →
  legacy behavior (T2/T4 pins hold).
- `apLaneBlocked()` mirrors core thresholds (lane consec≥3, provider
  consec≥2 within 30min). Blocked lanes sort last, never first;
  fail-safe keeps them eligible when nothing else has auth.
- Proven-current keep: a reasoning current lane with KB successes and
  zero consec failures is kept with NO `setModel` call.
- Healthy-first ordering: successes desc, consec asc, then hint order
  (identical order to legacy when KB is empty — no behavior drift).
- TDD: T5 (blocked top-hint skipped, proven picked, dead never
  attempted) + T6 (proven current kept) FAIL-first 13/16 → 16/16.
  D9 pins the router twin (unknown joins at floor, 65→68).

## 3. Verification

- Focused: autopilot-integration 16/16, autopilot-safety 5/5,
  discovery-budget 68/68, release 86/86.
- Full: **522/522 node + 84/84 pytest, zero failures.**
- Live: direct-edit turn on kilo APKB-DONE/APKB-TEST-OK (marker on
  disk); full `/ap`-tool turn hit a 280 s wall-clock timeout in TUI
  mode (panel path, unrelated to routing — tracked separately);
  kilo + mimo + bare-parent PARENT-OK all green around the run.
- fas-pi copies byte-equal (`c00cd1ac` both sides), verified FROM the
  repo checkout (16/16, 68/68, 5/5).

## 4. Residual / honest limits

- With a fully fresh KB (no successes anywhere) the first pick is
  still hint-order — irreducible without a live probe (quota cost);
  the breaker learns from the first failure as before.
- `--thinking max` on the FAS-inactive path still burns quota faster;
  kept (T2/T4 contract) — follow-up, not this fix.
- `/ap` remains TUI-slash (not agent-callable); full-tool turn
  long-hangs in `-p` TUI-panel mode — separate headless gap.

## Fingerprints (autopilot changed, rest untouched)

autopilot `c00cd1ac` (was `8c038dad`), core `155ae074`, index
`73239dde`, roles `8395d510`, runner `c20f921d`, schema `f95a471c`.
