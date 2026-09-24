# 2026-09-24 — Post-Crash Session: Cloud Routing Wins + Breaker Hardening

Status: CLOUD ROUTING PROVEN, F8 SHIPPED, cloud staging REVERTED to stock.
Termux: F8 FAIL-first 45/45, full 512/512 + 84/84, live PARENT-OK.

## 1. What survived the Termux crash (nothing lost)

Git HEAD `56d170c` == origin, clean; fas fingerprints unchanged
(core `155ae074`, index `73239dde`); cloud had synced core/index before
the crash. Continued from `LIVE.md` NEXT.

## 2. Cloud routing: FAS routes LIVE without any user key (evidence)

- Local Termux: `freeflow/kilo-auto/free` → K1-OK; bare-parent
  `fas-router/auto` → PARENT-OK.
- Cloud codespace (pi 0.85.1, no user key): same lanes →
  `CLOUD-K-OK`; cloud `fase2e-termux` workflow E2E → **CLOUD-E2E-DONE
  VERIFY-PASS** (`// E2E-MARKER` on disk, `E2E-TEST-OK`). KB proves
  routing, not luck: `openrouter/openrouter/auto` SERVED ×2, then
  `freeflow/big-pickle` SERVED ×4 straight.
- 33-lane cloud scan: kilo-auto/free + big-pickle LIVE; cohere/north,
  liquid/lfm, nex-n2.5 → bare `free` (upstream silent); dots → 400
  AtlasCloud; Cline lanes → 401 `cline_pool_exhausted`
  (`/freeflow cline login` needed — the /model path the user mentioned).
- Cross-process resume (E): session `e2e-cross-2` aborted mid-workflow,
  resumed in-session → CROSS2-DONE (implement/verify/review all PASS).
  Full resume.ts path still needs the credential-gated cloud rerun
  design (unchanged).

## 3. spawn_agent on cloud: TWO stacked gates (both proven, neither is FAS)

1. D-Bus: absent (`NO bus`) → works under `dbus-run-session` (conda
   ships it). Cleared.
2. systemd transient scopes: container has bwrap + systemd-run but no
   systemd as PID 1; `/sys/fs/cgroup/init` root-owned (move → EBUSY).
   Patching `createOwnedCgroup` to fall back to the writable cgroup
   root unblocked process start — but the child then starved:
   `no eligible candidate` (cloud free pool down to llm7 only at that
   hour). Spawn with an explicit working model still returns only
   `No result provided`. **Verdict: spawn_agent stays cloud-unproven;
   workflow rpc children (2E/2F + cloud E2E here) remain the supported
   parallel path.**

## 4. F8 fix (breaker fail-safe neutrality, TDD)

Cloud evidence showed single-provider pools during outages. F8 pins:
tripped breaker + solo-provider pool → both lanes stay rankable
(`rankCandidates` existing fail-safe covers it; now tested). Local:
FAIL-first shape added → 45/45 fallback-learning, full **512/512 node
+ 84/84 pytest**, live PARENT-OK after.

## 5. Cloud staging reverted (no drift)

Cloud `rpc-process.ts` restored from `~/fas-verify/fas-remote/backup/`
(md5 `21ec487e`); cloud fas core/index byte-equal to Termux
(`155ae074`/`73239dde`); runner `c20f921d`. One functional stub daemon
(`ollama /api/tags` + lmstudio `/v1/models` on :11434) left running for
the D-live design; probe verified: ollama lanes discovered + validated,
lmstudio stub present.

## 6. Queued (unchanged, credential-gated)

Q6-overflow workflow-rpc live run (supported path), E cross-process
full proof, D-live daemon ingestion, 0.87 live-turn parity, Q8
handoff (approval-gated). `/freeflow cline login` on cloud would
unlock 5 more lanes (user's /model observation is correct).

## Fingerprints

core `155ae074`, index `73239dde`, roles `8395d510`, runner `c20f921d`,
schema `f95a471c`, compose `59a2b7e5`, tool-list `8426bc05`;
fallback-learning 45/45 (F8 new).
