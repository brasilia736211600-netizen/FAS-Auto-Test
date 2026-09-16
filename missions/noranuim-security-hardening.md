# FAS mission: complete Noranuim security hardening

## Target
- Repository: `brasilia736211600-netizen/Noranuim`
- Branch: `security/hardening-from-working-state`
- Protected backup branch: `backup/working-state-2026-09-14`
- Protected backup commit: `bdef69715577b50f4ef10079cfeb5b5a073a74d2`
- Staging PR: `#5`
- Tracking issue: `#9`
- Current handoff HEAD: `e43b5379e3ae3761d0890813cb3da96a84a67c22`

## Invariant
A request for Profile X must resolve to exactly Profile X or fail closed. It must never silently reuse the global/default CookieManager or another profile's Chromium storage.

## Completed before this mission
- Proxy username/password/PAC URL removed from cloud settings sync; values preserved locally by profile.
- Android cleartext traffic disabled by default.
- Standalone `FLAG_SECURE` added.
- WebView permissions hardened to deny-by-default outside an explicit allowlist.
- Non-default cookie access made fail-closed when multi-profile support is unavailable.
- Main WebView profile setup/navigation and popup handling made fail-closed.
- Standalone profile changes create a new WebView/activity instead of reusing one from another profile.
- Static profile-isolation regression guards added.
- Android instrumentation exists for cookies, DOM storage and profile object scoping.
- Security Profile Runtime workflow exists and uses `working-directory: ./android`.
- Full Unit/Component, Full Android and FOSS Android validations previously passed.

## Current checkpoint
### CP3 — storage/permission isolation coverage
The implementation is present, but runtime proof is incomplete.

Required runtime evidence:
- Cookies isolation.
- WebStorage isolation.
- IndexedDB content isolation.
- Service Worker registration/content isolation.
- Cache API content isolation.
- Permission state isolation.
- Repeated profile switching.
- Activity/app restart and restoration.
- Popup isolation.
- Missing/invalid/unsupported profile must fail closed.

Known CI history:
- Run `35023322697` failed before the test because the emulator action executed from the wrong working directory.
- Commit `4f0dbcfb4dcad8e3b692f3b8c226924434d2e5ba` changed the workflow to use `working-directory: ./android` and `./gradlew`.
- Run `35028886426` on the remediation commit was cancelled; this is not runtime proof.

## CP4 — consolidated regression
After CP3 passes, run:
- all Unit/Component tests;
- Full Android validation;
- FOSS Android validation;
- static security tests;
- Android runtime isolation tests;
- Android smoke where relevant.

## CP5 — final security review
After CP4 passes:
- review complete diff against `bdef69715577b50f4ef10079cfeb5b5a073a74d2`;
- verify there are no unrelated deletions or broad WebView rewrites;
- verify proxy secrets, cleartext policy and permission allowlists;
- verify every profile entry point fails closed;
- run CodeRabbit or equivalent substantive review;
- update PR #5 and issue #9 state documents;
- do not merge automatically unless the explicit completion policy requires it.

## Historical guardrail
A previous intermediate edit `b905996...` caused unrelated comment deletions and an unrelated locale regression. It was removed from the reachable history; `ddb02d33...` restored the locale assignment. Never repeat a broad replacement of `NoraView.kt`; use surgical changes and compare against the protected baseline before accepting them.

## Execution policy for FAS
- Read the repository handoff/state documents before editing.
- Verify branch/HEAD and protected backup before any write.
- Work only on `security/hardening-from-working-state`.
- Use TDD and YAGNI.
- Prefer the smallest change that produces fresh runtime evidence.
- Use fresh evidence after every failed or cancelled attempt.
- Do not reset, clean, force-push, delete unrelated work, or modify secrets.
- Do not call a cancelled run a pass.
- If infrastructure blocks the gate, diagnose the infrastructure cause and make only the minimal CI/runtime change required.
- Commit and push completed work, then monitor GitHub CI.
- Continue through CP3 → CP4 → CP5 until the acceptance criteria are met or a safety boundary is reached.
- On safety boundary, stop and emit a durable report explaining the exact blocker.
