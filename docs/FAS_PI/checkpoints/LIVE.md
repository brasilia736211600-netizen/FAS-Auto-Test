# LIVE operator state — SAVED 2026-09-24 (resume here after hours)

HEAD: see `git rev-parse` (all below pushed; tree clean). Suites: node
`489/489` + D7 discovery cases (61/61 file) · pytest `84/84`. Re-verify with:
`for t in ~/fas-verify/tests/test-*.mjs; do node $t; done` + `python -m pytest` in ~/FAS.

## Last completed point (continue AFTER this)

1. Provider DECIDED: zai (direct 3/3 live OK) + openrouter-OAuth (served a real
   turn) + cline-OAuth (CLINE-OK). opencode bridge REJECTED (upstream TUI-only
   enforcement, Sep-20 evidence). omniroute PARKED (JS-walled site, no
   verifiable API/key — adopt only with key + live test).
2. FAS negative-cost scoring fix DONE (core `cb24e664`→`9693922b`, D7 test
   green, report `2026-09-24_SCORING_FIX.md` committed).
3. Firewall/port check DONE: 443 open to all providers from Termux; failures
   are account-side, never network. No action needed.
4. Auth truth-source CORRECTION: pi uses `~/.pi/agent/auth.json` (OAuth/key
   store), NOT env vars. Env-empty readings earlier were wrong-scope.

## NEXT (first thing on return)

Full workflow E2E on Termux: parent fas-router/auto + `--no-extensions`
(clean 426-model pool) + `-e fas/workflow/subagents/compose`, 2 real phases in
a fixture repo (implement tiny feature + run test), safety negative run,
git check, report + commit. Design ONLY — not started, nothing half-written.

## Then (in order)

- Cloud decision (Codespace vs Google Cloud CLI) — MY call, AFTER provider
  (provider now settled: decide on return).
- Queue 6 E2E overflow (subagents-child parts — needs cgroup host).
- E cross-process live + D live (need credential/daemon respectively).
- User approvals pending: credential restore (optional now — Termux lanes
  work), final repository creation (FORBIDDEN until full live proof passes).

## Fingerprints (extension sources, unversioned — re-verify on any touch)

core `9693922b`, roles `8395d510`, autopilot `8c038dad`, runner `c20f921d`,
schema `f95a471c`; unchanged: fas index `669fdeb7`, compose `59a2b7e5`,
tool-list `8426bc05`.

## Staging (safe to delete, kept for evidence)

~/cleanroom-demo, ~/cleanroom-home, ~/pi-matrix/087, ~/offload-result,
~/LEG2_PSCAPTURE_2026-09-23.txt, ~/fanout.bak, ~/fas-learn-loop.sh,
~/fas-probe/.

## Recovery rule

`git -C ~/FAS pull --ff-only`; read this file + TASK_QUEUE.md + latest report;
continue at NEXT above. Never rerun green items. Never create the final repo
without explicit approval AND a passing full live proof.
