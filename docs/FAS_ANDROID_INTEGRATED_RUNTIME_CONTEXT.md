# FAS Android Integrated Runtime — Authoritative Resume Context

## Status

- Project: `brasilia736211600-netizen/FAS-Auto-Test`
- Baseline branch: `fas-e2e-live`
- Verified functional baseline before this context commit: `2974530ee4a8b912947df8027b6d727e04821c8d`
- FAS CI after baseline documentation: run `34924165380` — SUCCESS.
- FAS E2E Live validation: run `34923903317` — SUCCESS.
- `fas-e2e-live` E2E proves: CI FAIL → evidence/log collection → bounded recovery → repair → commit/push → CI PASS.

## Baseline architecture already proven

FAS currently provides:

- GitHub-first repository/branch observation.
- CI run detection and polling.
- Failure log/evidence collection.
- Conservative recovery scope extraction.
- External-path containment protection.
- Read-only model diagnosis when direct scope is missing.
- OpenCode-backed repair path.
- Fresh disposable checkout per recovery attempt in GitHub-first mode.
- Retry context so rejected repairs are not blindly repeated.
- Scope enforcement before commit.
- Safe Git behavior: no reset, clean, force-push, unrelated deletion, or secret modification.
- Persistent recovery report.
- GitHub-first reporting identity.
- Autonomous continuous controller with bounded attempts/cycles.

References:
- `docs/FAS_AUTOPILOT.md`
- `docs/FAS_E2E_LIVE.md`
- `fas_autopilot.py`
- `fas_remote.py`
- `fas_recovery.py`
- `fas_report.py`

## Important regression that was fixed

Commit `930a258225d7e6b45d97de1c519e2dcf047409c9` introduced external-path containment but accidentally changed `recovery_scope()` granularity from parent-directory scope to file scope. Tests exposed this. Commit `2974530ee4a8b912947df8027b6d727e04821c8d` restored the original directory-scope contract while retaining containment protection.

## New product decision

The next product is **FAS Android Integrated Runtime**, not a GUI wrapper.

Target:

`FAS Android APK`
→ Android UI
→ FAS Controller
→ GitHub API
→ CI Monitor
→ AI Provider Layer
→ Embedded Linux Runtime
→ OpenCode Runtime
→ scoped repair/test/commit/PR/recovery

The user explicitly decided that OpenCode and a Termux/Linux-style runtime may be **integrated inside the same FAS app**, rather than requiring separate Termux/OpenCode installation.

## Product goal

The final user experience should be:

1. Install `FAS.apk`.
2. Open FAS.
3. Authenticate with GitHub.
4. Select repository and branch.
5. Enter an objective in natural language.
6. Start autonomous work.
7. FAS observes GitHub/CI, gathers evidence, diagnoses, invokes internal OpenCode, performs bounded repair, validates diff/scope/tests, commits/pushes or opens PR, monitors CI, and retries safely.
8. User receives a persistent PASS/FAIL/SAFETY_STOPPED report.

The user should not need to separately install or open:

- Termux
- OpenCode
- Python
- Git CLI
- `gh` CLI

## Preferred architecture

Do NOT simply embed the Termux APK UI.

Preferred design:

```text
FAS Android
├── UI
├── FAS Controller / State Machine
├── GitHub API Client
├── CI / Evidence Engine
├── Scope + Security Engine
├── AIProvider abstraction
├── Embedded Linux Runtime
├── OpenCode Engine
├── Workspace Manager
├── Secure Credential Store
├── Background Worker / WorkManager
└── Recovery Report Store
```

Termux concepts/runtime may provide implementation components, but FAS must remain the primary product and authority. OpenCode is an internal execution engine, not an external application dependency.

## Core state machine

`IDLE → OBSERVING → WAITING_FOR_CI → COLLECTING_EVIDENCE → DIAGNOSING → PLANNING → REPAIRING → TESTING → REVIEWING → COMMITTING → PUSHING → MONITORING_CI → RECOVERING → SUCCEEDED/FAILED/SAFETY_STOPPED/CANCELLED`

Rule:

`AI proposes → FAS validates → FAS executes`

AI must never receive credentials or bypass FAS safety boundaries.

## Runtime decision requirements

The next implementation session must evaluate embedded Linux/runtime options with evidence before choosing one. `libtermux-android` is a candidate, but was identified as experimental and must not be adopted blindly. Any selected runtime must be checked for:

- license compatibility
- Android compatibility
- ARM64 support
- bootstrap method
- native dependencies
- background execution behavior
- storage footprint
- maintenance status
- security isolation
- reproducibility

Target architecture for first release: `arm64-v8a`.

## OpenCode integration requirements

Create a FAS-owned abstraction such as `OpenCodeEngine` with lifecycle/session APIs:

- initialize
- start
- stop
- restart
- session
- prompt
- tool execution
- streamed output
- error handling

Pin OpenCode version and native/runtime dependencies. Verify artifacts/checksums. Do not download arbitrary runtime code at execution time.

## GitHub requirements

GitHub remains the source of truth for:

- repositories
- branches
- HEAD
- commits
- pull requests
- Actions
- workflow runs
- jobs
- logs
- artifacts

Avoid a permanent local checkout of the target project. Any workspace should be temporary and reconstructible from GitHub HEAD.

## Security requirements

Preserve all FAS safety guarantees:

- no reset
- no clean
- no force-push
- no unrelated deletion
- no secret modification
- no out-of-scope file changes
- reject path traversal
- reject absolute paths outside repository
- exclude `.git`
- exclude internal FAS state from repair scope
- sandbox execution
- mask secrets in UI/logs

Store credentials with Android Keystore/secure storage. Separate GitHub credentials from AI credentials.

## AI provider requirements

Use a provider abstraction with:

- primary provider
- fallback provider
- timeout
- retry
- rate-limit handling
- network failure handling
- provider failure reason

No hard dependency on one vendor/model.

## Background requirements

Use Android background execution appropriate for long-running work, preferably WorkManager plus foreground execution when required.

The task must survive:

- leaving the UI
- activity recreation
- process recreation where feasible
- temporary network loss

Persist state and resume safely.

## Testing requirements

TDD + YAGNI.

Required categories:

- unit
- integration
- Android instrumentation/UI
- security
- scope
- runtime
- OpenCode integration
- recovery
- GitHub integration
- E2E

Critical E2E:

`intentional CI failure → FAS detects → evidence → AI diagnosis → internal OpenCode repair → scope/diff validation → tests → commit/PR → GitHub CI PASS`

Do not declare success from mocks for the final E2E.

## Definition of Done for Android product

Do not use COMPLETE until there is evidence for:

1. APK build succeeds.
2. APK can be installed.
3. App starts without external Termux.
4. App starts without external OpenCode.
5. GitHub auth works.
6. Repository/branch selection works.
7. Objective/task creation works.
8. Embedded runtime starts.
9. Internal OpenCode starts.
10. Recovery path works.
11. Scope/security validation works.
12. Tests pass.
13. GitHub Actions pass.
14. Real E2E recovery passes.
15. Background state is durable.
16. No hidden dependency on developer tooling.

## Execution workflow for next session

`READ → AUDIT → ARCHITECTURE → RUNTIME EVALUATION → PROTOTYPE → TDD → IMPLEMENT → TEST → E2E → SECURITY REVIEW → DIFF REVIEW → CI → APK BUILD → INSTALL/EMULATOR VERIFY → DOCUMENT`

Do not add an IDE, plugin marketplace, arbitrary terminal, local Git server, collaboration system, or other non-goal in v1.

## User's intended outcome

A single installable `FAS.apk` that feels like one autonomous coding/recovery environment, while internally combining FAS controller + embedded Linux/Termux-style runtime + OpenCode + GitHub + configurable AI providers.

## Resume instruction

On resume, read this document first and treat it as authoritative for the Android direction. Re-read the current GitHub HEAD and CI before making any code changes. Preserve the existing FAS functional baseline and build the Android integration on a dedicated feature branch.