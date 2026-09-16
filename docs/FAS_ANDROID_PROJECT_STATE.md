# FAS Android Integrated Runtime — Project State

## State

**PLANNED / READY TO RESUME**

This document is the authoritative restart point for the future Android edition of FAS. The current FAS functional baseline remains frozen and verified separately in `docs/FAS_BASELINE.md`.

## Current FAS baseline

- Repository: `brasilia736211600-netizen/FAS-Auto-Test`
- Baseline branch: `fas-e2e-live`
- Baseline HEAD: `2974530ee4a8b912947df8027b6d727e04821c8d`
- Verified E2E workflow: `FAS E2E Live`
- Verified E2E run: `34923903317` — success
- Verified FAS CI run for the baseline record: `34924165380` — success
- Full FAS suite: success
- Live fixture: success

## Product to build later

Target product name: **FAS Android**.

The intended product is a single installable Android application that presents one unified FAS experience while embedding the required runtime layers internally.

Target architecture:

```text
FAS Android APK
├── Android UI
├── FAS Autonomous Controller
├── GitHub API / CI monitor
├── Recovery + Scope + Safety engine
├── Embedded Linux runtime
├── OpenCode runtime/engine
├── AI provider abstraction + fallback
├── Secure credential storage
├── Durable task state
└── Background execution
```

The user should not need to install or launch Termux or OpenCode separately.

## Integration decision

Do **not** build a thin GUI wrapper around external Termux/OpenCode applications.

Instead:

- FAS is the primary product and authority.
- OpenCode is an internal coding-agent engine.
- Termux/Linux capabilities are an internal runtime layer where technically justified.
- GitHub remains the source of truth for repositories, branches, commits, Actions, logs, and CI results.

The first Android implementation should reuse the proven FAS concepts rather than rewrite them unnecessarily.

## Proven capabilities to preserve

- autonomous CI observation
- actionable failure detection
- CI evidence collection
- conservative recovery scope
- external-path containment
- model-assisted diagnosis when direct scope is insufficient
- OpenCode repair path
- configured testing
- scope enforcement before commit
- safe commit/push behavior
- disposable recovery workspaces
- retry context after rejected repairs
- persistent recovery reports
- bounded recovery attempts
- safety-stop behavior
- GitHub-first supervision

## Android-specific target

The Android edition must eventually support:

1. GitHub authentication without exposing credentials to the AI layer.
2. Repository and branch selection.
3. Natural-language task/objective entry.
4. Autonomous monitoring and recovery.
5. Embedded Linux/runtime startup and health checks.
6. Embedded OpenCode startup/session/tool execution.
7. AI provider abstraction with fallback.
8. Secure workspace isolation.
9. Background execution using Android-appropriate mechanisms.
10. Durable task state across lifecycle/process recreation.
11. Diff/scope/security validation before commit.
12. Commit or PR creation through safe GitHub operations.
13. CI monitoring and repeated bounded recovery.
14. Recovery history and exportable reports.
15. Installable APK produced by CI.

## Runtime research gate

Before implementation of the embedded runtime, evaluate current open-source runtime options and their licenses, maintenance status, Android compatibility, ARM64 support, packaging model, security boundaries, storage cost, and background behavior.

A candidate such as `libtermux-android` may be evaluated, but its current experimental status must be treated as a risk signal rather than an automatic dependency choice.

The runtime decision must be evidence-based and minimal.

## OpenCode integration gate

OpenCode must not remain a runtime dependency on an externally installed application.

The future integration should provide an internal engine abstraction capable of:

- initialize
- start
- stop
- restart
- session management
- prompt submission
- streaming output
- tool execution
- failure handling

Pin versions and verify packaged artifacts/checksums where applicable.

## Security model

Use the following authority boundary:

```text
AI proposes
FAS validates
FAS executes
```

The AI layer must not receive GitHub tokens or other secrets.

The controller must enforce:

- repository boundaries
- workspace boundaries
- recovery scope
- forbidden paths
- forbidden git operations
- secret protection
- retry limits

## TDD / YAGNI

Use TDD and YAGNI.

Do not add a full IDE, complex plugin marketplace, arbitrary shell access, local Git hosting, collaborative editing, or other features outside the autonomous GitHub recovery objective.

## Development workflow

Use:

```text
READ
→ AUDIT
→ ARCHITECTURE
→ PROTOTYPE
→ TDD
→ IMPLEMENT
→ TEST
→ RUNTIME TEST
→ OPENCODE TEST
→ E2E
→ SECURITY REVIEW
→ DIFF REVIEW
→ CI
→ APK BUILD
→ INSTALL TEST
→ VERIFY
→ DOCUMENT
```

Use a separate feature branch for Android work. Keep `fas-e2e-live` as the functional regression reference until a replacement test strategy is proven.

## Definition of complete

Do not mark FAS Android complete until there is evidence for:

- successful APK build
- installability
- startup without external Termux
- startup without external OpenCode
- working GitHub authentication
- repository/branch selection
- working AI provider abstraction
- embedded runtime functioning
- embedded OpenCode functioning
- bounded repair and scope enforcement
- safe commit/PR flow
- autonomous CI monitoring/recovery
- durable background/lifecycle behavior
- real E2E failure → repair → CI PASS
- security validation

## Resume instruction

When returning to this project, read this document first, then `docs/FAS_BASELINE.md`, then inspect the current GitHub HEAD and CI before making changes.

Do not assume any unfinished implementation exists unless it is present in the repository.

## Relationship to current work

This project state is intentionally saved in the FAS repository so it can be resumed later without relying on chat history. It does not require changes to the existing verified FAS functional baseline until Android work is explicitly started.
