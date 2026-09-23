# Leg 2 — Workflow Success-Path Turn: PASS (2026-09-23)

Scope: Phase-1.4 Leg 2 ONLY. `Workflow success path -> child -> FAS extension loaded ->
fas-router/auto -> real provider turn -> workflow success` on the reusable Linux
Codespace. No Leg-1/L6 rerun. No source/config/test/CI modification during the proof.
Credential presence-only (never printed, logged, persisted, or committed).

Prior history preserved: Leg 2 was `CREDENTIAL_MISSING`-blocked on 2026-09-23
(`~/FAS_LEG2_CODESPACE_RESULT_2026-09-23.md`, `~/FAS_LEG2_CODESPACE_READY_2026-09-23.md`).
This run executed only after the same-process presence gate reported `CRED:SET`
(user-authorized mechanism; value never touched).

## 1. Verdict: PASS — Leg 2 CLOSED (objective complete, system PASS)

## 2. Precondition proof (same process environment, values redacted to facts only)

- Codespace reused (not recreated): `opulent-space-happiness-wvg76j459744cgjg`
  (repo `brasilia736211600-netizen/FAS-Auto-Test`, branch `fas-feature-test`,
  machine `basicLinux32gb`). Prior `Shutdown` state woken via `gh codespace ssh`
  (this `gh` has no `start` subcommand; ssh auto-starts).
- Same-shell verification before the leg:
  Node `v26.4.0` · Pi `0.85.1` · `process.platform linux` (re-verified) ·
  cgroup-v2 controllers `cpuset cpu io memory hugetlb pids rdma misc` ·
  `OPENROUTER_API_KEY` presence `SET` (test `[ -n "${OPENROUTER_API_KEY}" ]`).
- Remote fingerprints byte-equal to local before the run:
  fas core `33aa88d5`, index `669fdeb7`, compose `59a2b7e5`,
  tool-list `8426bc05`, runner `0d9352e3`.
- Codespace repo checkout at `c91f654` (matches `WORKFLOW_STATE.md` baseline ref);
  local `~/FAS` later pulled `83efff9..c709030` (docs-only upstream, no conflict).

## 3. Parent-level pre-check (same env, one cheap turn): PASS

`pi --no-approve --no-session --model fas-router/auto -e <fas> -p "Reply with exactly:
LEG2-PARENT-OK"` → transcript `LEG2-PARENT-OK`. Proves CLI model acceptance,
FAS routing, and the real-provider path before spending the workflow leg.

## 4. Leg-2 probe (staging only, removed afterwards)

- Probe workflow `fasprobe-leg2` (one phase `probe`, `thinking: off`, `tools: [read]`,
  trivial exact-output task) staged at `~/.pi/workflows/fasprobe-leg2.yaml` on the
  codespace, triggered via TUI `/workflow fasprobe-leg2 ...` under pty
  (`script -qec`), parent flags `--model fas-router/auto -e <fas> -e <workflow>
  -e <subagents> -e <compose>`, isolated `PI_CODING_AGENT_DIR` (`ptyhome-leg2`).
  Staging script: `~/fas-verify/run-leg2-remote.sh` (codespace-local, not repo source).
- Full transcript: `~/fas-verify/test-run/leg2-pty.out` (19,278 bytes, codespace volume).

## 5. Acceptance evidence (fresh, secret-free)

- Fresh child argv (ps-captured live process, `leg2-pscapture.txt`):
  `node .../pi --mode rpc --name workflow:fasprobe-leg2:probe:9e18e02f --no-session
  --model fas-router/auto -e /home/codespace/.pi/extensions/fas/index.ts
  --thinking off --tools read --no-approve ...`
  → fresh child argv: YES · FAS extension load (`-e <fas>`): YES ·
  effective child model `fas-router/auto`: YES.
- FAS routing: parent transcript `FAS router active`; child resolved `fas-router/auto`
  to a real candidate and completed (an unrouted child fails `no eligible candidate`
  instead of answering — cf. 2F offline evidence). → YES.
- Real provider request/response: child exact-output `LEG2-PROBE-OK` in the workflow
  panel; parent pre-check `LEG2-PARENT-OK`. → YES.
- Workflow success: transcript `phase probe` + `succeeded` (x2 refs), `Workflow
  finished · panel retained in chat`, script `LEG2-DONE rc=0`. Zero `failed` markers. → YES.
- Cleanup: probe YAML removed (`~/.pi/workflows/` verified empty after run); no repo
  source/config/test/CI touched; credential lived only in process env (never written). → YES.

## 6. Post-leg regression + diff proof (local, after the leg)

- Full durable suite: **324/324 GREEN**
  (`21+13+9+64+57+37+75+12+11+25`, 10 files, 0 failures).
- `git -C ~/FAS status`: clean at `c709030`. `git -C ~/.pi/pi-enhanced status`: only the
  two pre-existing 2E/2F seam edits. Local fingerprints re-verified match §2.
  → No unrelated diff.

## 7. Remaining gaps after this report

- Runtime proof track: Leg 1 CLOSED, L6 CLOSED, Leg 2 CLOSED. Phase-1 runtime closure COMPLETE.
- Next: Phase-2 evidence-backed enhancements in audit order
  (`docs/FAS_PI/PHASE2_EVIDENCE_AUDIT_2026-09-23.md`).
- Codespace stopped after credential-state cleanup (volume evidence retained until
  retention expiry; reports now live in `docs/REPORTS/` so volume loss is acceptable).
