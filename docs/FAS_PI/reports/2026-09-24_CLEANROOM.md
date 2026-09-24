# 2026-09-24 — Clean-room Portability Proof (structural)

Scope: Queue 5. Unrelated fixture repo (`~/cleanroom-demo`: app.js +
package.json only), fresh agent home (`~/cleanroom-home`), extensions loaded
ONLY via `-e` flags — zero project source copied into the target.

Labels: VERIFIED (fresh evidence) · BLOCKED (provider-turn execution).

## 1. Verdict: STRUCTURAL PASS — install/boot/persistence/fail-safe proven;
real-turn execution BLOCKED on credential (same gate as Queue 6)

## 2. Evidence (VERIFIED, all offline, no credential)

- Boot: `pi --help` with `-e fas + workflow + subagents + compose` in foreign
  cwd + fresh home → exit 0, no factory throw.
- FAS decision loop runs in clean room: `-p --model fas-router/auto` →
  `FAS router: no eligible candidate; no fallback model available`, exit 0,
  no crash (L6-class behavior reproduced outside the project).
- Persistence: `--session-id cleanroom-1` created
  `sessions/.../2026-09-24T01-47-31-048Z_cleanroom-1.jsonl` in the clean home.
- Target untouched: `git status` clean; no `.ts` files in target (nothing copied).
- Fixture dirs are local-only staging (not in Git); safe to delete.

## 3. Residual (BLOCKED, explicit)

- Real provider turn + child execution in clean room needs a credential —
  merges with Queue 6 E2E when available. No structural reason it would differ
  (same binaries, flags, and fail-safe paths as proven hosts).
