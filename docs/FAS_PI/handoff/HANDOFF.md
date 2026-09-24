# FAS-Pi Final Handoff Package (proposed — NOT published)

Status: FINAL-HANDOFF-READY: USER-APPROVAL-REQUIRED. No final repository has
been created. Nothing below publishes anything without explicit approval.

## 1. Verified status

- Phase 1 runtime: Leg 1 / L6 / Leg 2 CLOSED (live Codespace proofs).
- Phase 2: B, C, A, F, E COMPLETE; D PARTIAL (live BLOCKED).
- Extras: autopilot checkpoint hardening, Pi 0.85.1↔0.87.1 matrix (baseline
  pinned), cloud-offload option (2 live green runs), workflow fan-out,
  clean-room structural proof.
- Regression: **516/516 node + 84/84 pytest, 0 failures** (chain
  324→351→396→420→440→458→469→489→496→498→504→510→512→516).
- Router hardening (post-handoff-draft): F1 failure observability (T16),
  F3 within-turn provider breaker (T17), status-from-text advisory (T18),
  persistent provider cooldown (F7), breaker fail-safe neutrality (F8),
  extension-lane visibility (D8). Live: bare-parent PARENT-OK; Termux +
  cloud + purist + mimo + Q8-trial workflow E2Es all PASS; practical
  autopilot trial 10/10 with adversarial containment (report
  2026-09-24_AUTOPILOT_TRIAL.md).
- Working lanes (no key, both hosts): freeflow/mimo-v2.6-flash +
  freeflow/kilo-auto/free; backup cline-free + openrouter; omniroute PARKED.
- Remaining external gates (need user/host, not work): spawn_agent live
  proof (systemd-gated container — rpc children are the supported path),
  E-full + D-live daemon proofs, 0.87 live-turn, Q8 approval itself.

## 2. Exact source inventory (production boundary)

| Path (source of truth today) | Files | Fingerprint | In Git? |
|---|---|---|---|
| `~/.pi/extensions/fas/` | core.ts, index.ts, roles.ts, local-providers.ts | core `155ae074`, index `73239dde`, roles `8395d510` | NO — transfer at publish |
| `~/.pi/agent/extensions/autopilot/` | index.ts | `8c038dad` | NO — transfer at publish |
| `~/.pi/agent/skills/` | 2× SKILL.md | content in report A | NO — transfer at publish |
| pi-enhanced `extensions/workflow/` | runner.ts, schema.ts, resume.ts, safety.ts (+rest untouched) | runner `c20f921d`, schema `f95a471c` | Upstream h4ni0/pi + local seams |
| pi-enhanced `extensions/subagents/` | collaboration-manager.ts, tool-list.ts, child-contract.ts (+rest) | tool-list `8426bc05` | Upstream h4ni0/pi + local seams |
| `~/.pi/workflows/` | staging only (probes removed) | — | n/a |
| FAS-Auto-Test `fas_*.py`, `test_*.py`, `.github/` | Python line + CI + offload | git-tracked | YES |
| FAS-Auto-Test `docs/FAS_PI/` | all state/reports/checkpoints | git-tracked | YES |

Files still outside GitHub: all extension `.ts` sources + Skills (rows above).
Migration must copy exact fingerprinted versions, then re-verify (suite +
fingerprints) in the new checkout.

## 3. Requirements

- Pi baseline **0.85.1** (`npm i -g @earendil-works/pi-coding-agent@0.85.1`);
  0.87.x NOT accepted (TranscriptContext drops `tools` — see compat report).
- Node 26 (native TS; jiti harness for tests).
- Deps: workflow `yaml@2.9.0`; compose none; subagents none beyond pi.
- Providers: any Pi-registered provider; FAS routes `fas-router/auto` →
  registry candidates, ≤3 attempts + ≤1 previous-model delegation, explicit
  fail-safe message when none eligible. At least one provider credential in the
  executing process env for real turns (presence-only; never stored in repo).

## 4. Installation / bootstrap (target machine)

```bash
npm i -g @earendil-works/pi-coding-agent@0.85.1
# copy dirs preserving names:
#   fas/ -> ~/.pi/extensions/fas/
#   autopilot/ -> ~/.pi/agent/extensions/autopilot/
#   skills/*/ -> ~/.pi/agent/skills/*/
#   workflow/ subagents/ -> pi-enhanced checkout extensions/ (keep 2E/2F/B/E/F/P seams)
# verify: node ~/fas-verify/tests/*.mjs (expect 489) + md5 fingerprints above
```

## 5. Tests / CI / runtime validation

- `~/fas-verify/tests/test-*.mjs` (node, jiti): 489 assertions, TDD lineage.
- `pytest` (FAS-Auto-Test root): 84 tests incl. cloud offload.
- CI: `.github/workflows/fas-ci.yml` (pytest), `fas-e2e-live.yml`,
  `cloud-offload.yml` (heavy-job offload for weak hosts).
- Runtime validation commands: Leg-2 probe script pattern (`run-leg2-remote.sh`
  class), xproc cross-process driver pattern, clean-room checklist (all in
  respective reports).

## 6. Security model

- Pre-spawn declaration gates (destructive git, out-of-scope paths); no
  in-execution veto exists in Pi 0.85.1 (observational events only).
- Autopilot checkpoints tracked-only (`git add -u`).
- Deep redaction incl. credential value-shapes; numeric telemetry preserved.
- Never paste live keys into tasks (session JSONL persists raw text).
- `cloud-offload.yml` custom commands = owner-trust (write access required).

## 7. Limitations (explicit)

- Termux/Android: no child cgroup path (subagents spawn unavailable);
  spawn_agent/delegate unusable — inline + Codespace execution only.
- No local-provider live proof; no 0.87 runtime parity; no cross-process live
  resume proof (all BLOCKED, none fabricated).
- Steer during fan-out reaches the most-recent child; fanout targets must be
  `next`-free (v1 join semantics).

## 8. Compatibility notes

- 0.85.1 pinned; 0.87.1 matrix done (23/23 symbols, boot/load/skills green;
  blocker documented). No upgrade without parity proof + /compose invariance.

## 9. Proposed final repository tree

```text
fas-pi/
  extensions/fas/            # core, index, roles, local-providers
  extensions/autopilot/      # index
  extensions/compose/        # index (frozen except proven regressions)
  extensions/workflow/       # full dir (seams included)
  extensions/subagents/      # full dir (seams included)
  skills/fas-*/              # SKILL.md set
  prompts/fas-*/             # fas-status.md, fas-router-debug.md
  python/                    # fas_*.py + test_*.py + install_fas.sh
  workflows/ci/              # fas-ci, e2e-live, cloud-offload
  workflows/pi/              # fase2e-termux.yaml (reference E2E workflow)
  docs/                      # curated state + reports
  tests/                     # fas-verify suite (relocated)
  README.md INSTALL.md SECURITY.md COMPATIBILITY.md
```

## 10. README draft (opening)

"FAS-Pi: a centralized supervisor/policy layer that makes Pi 0.85.1 a
dependable autonomous coding substrate — evidence-weighted routing, bounded
fallback, structured child results, roles, Skills, safety gates, resume, and
parallel fan-out. 516+84 tests green. See INSTALL.md (10 min), SECURITY.md
(gates + limitations), COMPATIBILITY.md (0.85.1 pinned)."

## 11. Migration / publish procedure (after approval ONLY)

1. Approve tree above (or amend).
2. Create repo (public/private per owner), initialize from this package.
3. Transfer exact fingerprinted sources; run full verification (489+84,
   fingerprints, boot smoke, Skills discovery).
4. Publish README/INSTALL; verify remote tree; record URL+commit here.
5. Archive this handoff with the final URL (never delete failure history).
