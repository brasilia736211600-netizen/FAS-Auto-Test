# AlphaCode on Android/Termux — OpenCode Execution Plan

## Objective

Install and validate AlphaCode v1.0.68 from source on the user's Android/Termux environment, while preserving the existing Hermes, Pi/FAS, OpenCode, Noranuim, and other active development environments.

The execution must be autonomous, evidence-driven, resource-aware, and minimal. Do not make broad system changes merely to force a build.

## Environment assumptions

- Android/Termux on ARM64/aarch64.
- Termux uses Android/Bionic rather than a conventional desktop Linux/glibc environment.
- Rust is already newer than AlphaCode's pinned Rust 1.94.1; do not downgrade it unless an actual compatibility failure proves that it is required.
- Device memory is limited. Cargo compilation must therefore be conservative.
- The AlphaCode repository is currently available locally at `~/alphacode` when this plan is executed, but always verify the actual location and repository state first.

## Phase 0 — Establish a safety baseline

Before modifying anything:

1. Identify:
   - `$HOME`
   - `$PREFIX`
   - current working directory
   - AlphaCode repository and Git state
   - Hermes installation/state
   - Pi/FAS installation/state
   - OpenCode installation/state
   - active Git repositories under the user's development locations
   - available storage
   - RAM and swap
   - Rust, Cargo, Clang, Git, Python and Termux versions.
2. Record the baseline in the final report.
3. Do not assume that a file is disposable simply because it is old.

## Phase 1 — Safe Termux storage cleanup

The phone has constrained storage. Clean only files that are demonstrably disposable or reproducible.

### Mandatory protections

Never delete, move, truncate, or modify:

- Hermes and all of its configuration, state, skills, caches required for operation, providers, credentials, or repositories.
- Pi/FAS and its extensions/configuration/state.
- OpenCode and its configuration/state.
- FAS repositories, including `FAS-Auto-Test` and `fas-pi`.
- Noranuim/HebLibre or any other active Git repository.
- `$PREFIX` binaries, libraries, package databases, package-manager state, or configuration.
- SSH/GPG credentials and configuration.
- API keys, tokens, environment configuration, authentication state, shell configuration, Git configuration, or user data.
- Source trees, build manifests, lockfiles, scripts, documentation, or unknown files.
- Any file currently being used by a running process.

### Cleanup policy

A modification time of approximately 30 days or older is only a **candidate signal**, never sufficient proof for deletion.

A candidate may be removed only when all of these are true:

1. It is clearly disposable/rebuildable.
2. It is not part of an active project or required tool.
3. It is not configuration, state, credentials, source, package-manager data, or user data.
4. No active process depends on it.
5. Removing it will not impair Hermes, Pi/FAS, OpenCode, Git, Rust/Cargo, Termux, or other active workflows.
6. The cleanup can be explained precisely in the final report.

Prefer safe targets such as clearly identified stale temporary files, obsolete logs, failed build artifacts, and application-specific disposable caches. Do not blindly delete `~/.cache`, Cargo registries, package caches, or entire directories.

### Forbidden cleanup commands

Do not use broad destructive commands such as:

- `rm -rf ~/*`
- blanket deletion of `~/.cache`
- `find ~ ... -delete`
- wildcard deletion across HOME
- deletion based only on age
- deletion of unknown directories/files merely because they are large.

Before deletion, calculate the exact paths and sizes. After deletion, verify the protected tools and repositories remain intact.

## Phase 2 — AlphaCode source audit

Inspect the actual AlphaCode checkout and verify:

- repository URL, branch, commit and version;
- `Cargo.toml`;
- `rust-toolchain.toml`;
- `build.rs`;
- installation/build scripts;
- feature flags;
- target-specific `cfg` conditions;
- dependency tree;
- browser-agent XPI/resource requirements;
- Linux-specific functionality;
- accessibility/AT-SPI2 dependencies;
- Wayland/X11 dependencies;
- clipboard implementation;
- `arboard` configuration;
- `crossterm`/terminal dependencies;
- optional heavyweight dependencies/features.

Do not infer Android compatibility from the project name or documentation alone. Determine it from the source and actual build graph.

## Phase 3 — Android/Termux compatibility strategy

The official release installer targets conventional Linux/macOS architectures and must not be assumed to produce an Android/Bionic-compatible executable.

Prefer:

1. Native ARM64 Android/Termux source compilation.
2. Existing portable code paths/features.
3. Minimal, isolated Android-specific conditional compilation only where an actual build error proves it is necessary.

Do **not**:

- install a desktop Linux stack merely because a dependency normally exists on Linux;
- force glibc binaries onto Android;
- add random compatibility packages;
- remove useful functionality without evidence;
- rewrite architecture unnecessarily;
- disable security features just to obtain a successful compilation.

The absence of `libxkbcommon` in current Termux repositories must be treated as a compatibility constraint, not as a reason to blindly install unrelated packages.

## Phase 4 — Dependency and feature minimization

Resolve the real dependency graph for the intended AlphaCode CLI build.

Disable optional features that are not required for normal CLI operation, especially heavyweight or unrelated integrations, unless the source proves that they are mandatory.

Examples include optional embeddings, AWS/Bedrock integrations, PDF/Mermaid/email functionality, profiling/jemalloc features, and other optional components.

Do not modify dependency versions without a concrete reason and evidence.

## Phase 5 — Resource-aware build

The phone is memory constrained.

Use conservative compilation settings, starting with:

- `CARGO_BUILD_JOBS=1`

Only increase parallelism if measurements prove the device remains stable.

During compilation:

- monitor available RAM and swap;
- avoid simultaneously running unnecessary heavy applications/processes;
- do not allow compilation to consume essentially all available memory;
- if memory pressure becomes dangerous, reduce parallelism or stop safely and diagnose;
- do not repeatedly restart a failing build without identifying the root cause.

A successful build that destabilizes Termux is not considered successful.

## Phase 6 — Build and diagnose

Run progressively stronger checks:

1. Cargo metadata/dependency resolution.
2. Target/feature validation.
3. Compilation/check.
4. Release build.
5. Repeat only when necessary after fixing a demonstrated root cause.

When a command fails:

- capture the actual error;
- classify it as source, dependency, platform, toolchain, resource, environment, or missing asset;
- identify the smallest correct fix;
- apply only that fix;
- rerun the relevant validation.

Do not use random package installation or arbitrary source changes as troubleshooting.

## Phase 7 — Installation

After a successful build:

1. Identify the resulting executable precisely.
2. Verify it is ARM64 and suitable for Android/Termux.
3. Install it into an appropriate Termux executable directory, preferably `$PREFIX/bin/alphacode`.
4. Ensure permissions are correct.
5. Do not overwrite unrelated executables.
6. Preserve the source tree unless there is a clear reason to remove it.

## Phase 8 — Runtime verification

Verify at minimum:

- `alphacode --version` or the project's actual version command;
- `alphacode --help`;
- executable architecture/interpreter;
- dynamic/runtime dependencies;
- startup without immediate crash;
- configuration discovery;
- provider/model discovery if supported;
- a minimal non-destructive CLI operation.

If AlphaCode requires authentication for a meaningful test, do not invent or expose credentials. Validate everything possible without credentials and clearly identify what remains unverified.

## Phase 9 — Regression protection

After installation, verify that:

- Hermes still launches/operates;
- Pi/FAS remains intact;
- OpenCode remains intact;
- active Git repositories are unchanged except for intentional AlphaCode-related changes;
- no credentials/configuration were altered;
- no protected directories were deleted;
- Termux remains usable.

Do not perform unnecessary upgrades of unrelated tools.

## Phase 10 — Final report

Create:

`~/ALPHACODE_TERMUX_COMPLETION_REPORT.md`

The report must include:

- date/time;
- Android/Termux environment;
- architecture;
- AlphaCode version and commit;
- source repository;
- installation method;
- exact build command(s);
- features enabled/disabled;
- dependency/platform findings;
- Android-specific changes, if any;
- tests and their results;
- installed executable path;
- executable/runtime verification;
- storage before/after;
- RAM/swap before/after;
- cleanup candidates inspected;
- exact files/directories removed and why;
- protected systems verified;
- remaining limitations;
- final PASS/PARTIAL/FAIL verdict.

## Completion criteria

Declare **PASS** only when AlphaCode is installed and demonstrably starts and performs the available basic CLI checks on Android/Termux, with no material regression to the protected development environment.

Declare **PARTIAL** when the source/build/install work succeeds but a clearly identified runtime capability cannot be validated because of an external requirement such as credentials or an unavailable service.

Declare **FAIL** only after evidence shows that the current environment cannot provide a correct installation without unacceptable architectural changes.

Do not stop merely because the first build fails. Continue through diagnosis and the smallest evidence-based correction until the task is genuinely complete or a technically justified blocker remains.

## Operating principle

You are the execution agent. Read this plan, inspect the real environment, make decisions from fresh evidence, execute the complete workflow, verify the result, and leave a durable report. Do not ask the user to manually repeat routine steps that can safely be performed autonomously. When an irreversible or potentially destructive action is not clearly justified by the rules above, do not perform it.
