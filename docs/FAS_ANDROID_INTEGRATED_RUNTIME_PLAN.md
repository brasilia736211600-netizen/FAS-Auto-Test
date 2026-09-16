# FAS Android Integrated Runtime Plan

Status: architecture/implementation kickoff
Baseline: `fas-e2e-live` @ `2974530ee4a8b912947df8027b6d727e04821c8d`

## Product goal

Build a single installable Android application named FAS that provides the FAS autonomous controller while embedding the runtime needed to run OpenCode and a Linux/Termux-compatible execution environment. The user should not need a separately installed Termux or OpenCode application.

## Non-goals for the first milestone

- Full IDE/editor
- Terminal emulator beyond what FAS execution requires
- Plugin marketplace
- Arbitrary host shell access
- Multi-device collaboration

## Architecture direction

Android UI -> FAS Controller -> policy/scope engine -> runtime manager -> embedded Linux runtime -> OpenCode engine
                                   |-> GitHub API / Actions
                                   |-> AI provider abstraction
                                   |-> durable recovery/report state

GitHub remains the repository/CI source of truth.

## First implementation milestones

1. Create Android application skeleton and independent feature branch.
2. Extract a platform-neutral FAS core boundary from the current Python implementation where practical.
3. Define Android interfaces for GitHub, AI provider, runtime manager, OpenCode engine, scope enforcement, recovery controller, and durable state.
4. Prototype embedded Linux runtime boot on arm64-v8a.
5. Prototype OpenCode process lifecycle inside that runtime.
6. Implement a minimal Android controller/UI for repository/branch/task/recovery state.
7. Add unit/integration tests and GitHub Actions Android build + test workflow.
8. Add real emulator smoke coverage before expanding functionality.
9. Add an end-to-end proof that the integrated runtime can execute a bounded repository recovery task.

## Safety requirements

- Never reset/clean/force-push or delete unrelated work.
- Enforce repository-relative recovery scope before edits.
- Keep credentials outside AI/OpenCode context.
- Treat AI output as untrusted proposals.
- FAS validates before execution.
- Keep the existing FAS functional baseline intact on its current branch.

## Decision gate

Do not package the final APK until the embedded runtime, OpenCode lifecycle, GitHub integration, scope enforcement, and background state have independent tests and a real E2E path.
