# 2026-09-24 — D: Local-Provider Discovery IMPLEMENTED (live proof BLOCKED)

Scope: Phase-2 item D ONLY (last), implemented strictly to the extent the
environment supports. Discovery-first probing, capability validation,
unavailable-path handling. No phantom models, no fabricated suitable-provider
proof. No packages, no `/compose` change.

Labels: VERIFIED (fresh evidence) · BLOCKED (live suitable-path proof: no daemon).

## 1. Verdict: PARTIAL-PASS — discovery/validation implemented (469/469 GREEN);
live suitable-path verification BLOCKED (no local daemon on this host)

## 2. TDD baseline-FAIL-first (VERIFIED)

`~/fas-verify/tests/test-fas-local-providers.mjs` (11 assertions) written first;
baseline: `Cannot find module '.../fas/local-providers.ts'`. Development caught
one real defect: endpoint alias `lm-studio` was rejected (only `lmstudio`
accepted) — normalized in the module with canonical `lmstudio` provider output.

## 3. Implementation (1 new pure module, ZERO existing-file modifications)

- NEW `~/.pi/extensions/fas/local-providers.ts` (injectable fetch; never throws):
  - `probeLocalProviders()` — sequential short-timeout loopback probes
    (`127.0.0.1:11434` ollama dialect, `:1234` lm-studio dialect); unreachable /
    HTTP-error / malformed / unknown-dialect → skipped; results are
    registry-shape `{provider, id, local: true, quality: "unknown"}`.
  - `validateLocalCandidate()` — shape check only (known provider, non-empty
    id); quality is ALWAYS `"unknown"` (never assumed).
  - Candidates exist ONLY when an endpoint actually answers — no hardcoded
    `ollama/*` phantoms (test-locked: refusal → `[]`).
- Registry admission deliberately NOT implemented: candidate admission to Pi's
  model registry is Pi-core territory (unmodifiable boundary). Exact next step:
  on a host with a live daemon, run the suitable-path turn, then propose the
  admission seam with that evidence.

## 4. Test evidence (VERIFIED + BLOCKED)

- Focused D suite **11/11** (mock-fetch only, zero real network): unavailable →
  `[]` · both dialects parsed · malformed skipped/valid kept · validation
  accept/reject/quality-unknown · loopback-only probing.
- **Live probe on this host: `LIVE-PROBE-COUNT=0`** (both endpoints refused) —
  suitable-path proof BLOCKED, not attempted, nothing fabricated.
- Full suite **469/469 GREEN** (458 prior + 11 D), 0 failures. `node --check`
  clean. Upstream bun suites PLATFORM-LIMITED, untouched.

## 5. Diff proof

- fas ext: `?? local-providers.ts` only. All existing files untouched
  (fingerprints: core `cb24e664`, roles `5d931cbd`, runner `74434c36`).
- `~/FAS`: this report + state edits, docs-only; `git diff --check` clean;
  pushed; remote tree verified.
