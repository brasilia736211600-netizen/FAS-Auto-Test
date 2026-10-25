# REA on Android/Termux — Autonomous Setup and Integration Mission

**Status:** Execution plan  
**Primary agent:** OpenCode  
**Target environment:** Android / Termux / ARM64  
**Repository:** `morluto/rea` (verify official identity before use)  
**Report destination:** `~/rea-lab/reports/REA_TERMUX_COMPLETION_REPORT.md`

## 1. Mission

Set up and validate REA (Reverse Engineer Anything) in the user's existing Android/Termux environment, then integrate it with OpenCode and evaluate optional integration with Hermes, Pi, and Alphacode.

This is an execution mission, not a request for a theoretical guide. Inspect the real environment, verify current official documentation, make the smallest safe changes, test actual behavior, diagnose failures, and produce an evidence-based report.

Do not assume REA, its CLI, any integration, or any external reverse-engineering engine is compatible with Android/Termux until tested.

## 2. Constraints and priorities

The phone has limited RAM (approximately 3.4 GiB physical memory based on prior observations) and runs Android/Termux on ARM64. Treat these as provisional facts and re-measure the current environment.

Priorities:

1. Protect the existing Termux, OpenCode, Hermes, Pi/FAS, Alphacode, Git repositories, user files, credentials, and configuration.
2. Verify platform compatibility before installing or modifying anything.
3. Prefer free, open-source, lightweight components where practical.
4. Prove the complete tool path with tests, not just a successful package installation.
5. Keep memory, CPU, disk use, and background processes bounded.
6. Preserve all useful findings and commands in durable Markdown reports.

Never expose API keys, tokens, passwords, SSH/GPG secrets, or private environment values in logs or reports. Report only whether a credential is configured when that fact matters.

## 3. Phase A — Baseline and discovery

Before changing files or installing packages, record:

- Android version, Termux environment, architecture, `$HOME`, `$PREFIX`, current directory, and free storage.
- Available RAM and swap from `/proc/meminfo`.
- Versions and executable paths for Node.js, npm, Python, Git, OpenCode, Hermes, Pi, and Alphacode when present.
- Existing REA installations, checkouts, processes, MCP servers, and configuration files.
- Current Git status for any repository you might touch.
- Existing MCP configurations and their current contents, without printing secrets.
- Network reachability to the official REA source and npm registry, if safely testable.

Create a dedicated workspace under `~/rea-lab/`, including `reports/` and `samples/`. Do not use or repurpose another active project directory.

Save a baseline report. Do not make assumptions based solely on previous conversation notes.

## 4. Phase B — Verify the official project and installation path

Start with the official source and current documentation:

- Repository: https://github.com/morluto/rea
- Inspect its README, installation documentation, CLI help, client/MCP configuration documentation, release information, and package metadata.
- Verify the official npm package name, latest suitable version, Node.js engine constraints, supported commands/options, and external dependencies from the actual version being considered.
- Inspect any installation script before running it. Do not pipe remote scripts directly into a shell.
- Distinguish verified documentation from claims that still require a runtime test.

Check the actual Node.js version against the current requirements. Do not upgrade Node.js, downgrade toolchains, run a broad Termux upgrade, or install arbitrary packages without identifying a concrete need and a safe compatibility path.

Prefer a locally scoped or otherwise isolated installation when supported. Avoid global installation unless the documented workflow genuinely requires it.

If installation fails, capture the exact error and classify it (Node version, unsupported platform, native dependency, permissions, network, missing executable, or other cause). Do not blindly repeat the same command.

## 5. Phase C — Validate the CLI

Run the real documented help/version commands for the installed version. Verify the command syntax from the package documentation or its own help output; do not invent subcommands or flags.

If the project provides a dry-run/setup-preview mode, use it before changing agent configuration.

Record:

- Exact package and version.
- Exact commands executed.
- Exit status and meaningful output.
- Any limitations specific to Android/Termux.
- Whether a server can actually start and remain running.

Downloading a package or creating an MCP configuration is not proof that REA works.

## 6. Phase D — Build a controlled sample and run a real analysis

Create a small, self-owned JavaScript sample in `~/rea-lab/samples/` with multiple modules, imports/exports, and a simple function whose behavior is independently verifiable.

Use only documented commands and options supported by the installed REA version. Run REA against this sample and preserve the actual output.

Verify:

1. The analysis process starts and exits as expected.
2. The tool returns substantive results.
3. Findings correspond to the known sample source.
4. Results contain traceable evidence (file/module/function references) where the tool claims to provide it.
5. Output can be saved to a report.
6. Invalid paths or malformed inputs fail safely.
7. Resource usage is reasonable for a small sample.

If JavaScript/Electron analysis is not available in the installed version, select another documented, lightweight test that can be verified locally. Do not fabricate results or mark an untested capability as supported.

## 7. Phase E — Integrate with OpenCode

OpenCode is the primary client and must be tested first.

1. Inspect the installed OpenCode version and its current MCP configuration format using its own documentation/help.
2. Identify the exact configuration file(s) that would be affected.
3. Back up each file before editing.
4. Preserve all existing providers, servers, options, permissions, and unrelated configuration.
5. Prefer the official REA setup workflow if it is supported by the current versions; inspect its preview/dry-run output first when available.
6. Apply only the minimum required configuration change.
7. Restart or reload the client as required.
8. Verify the MCP server connects and that REA tools appear in the actual OpenCode session.
9. Invoke at least one real REA tool from inside OpenCode against the controlled sample.
10. Verify that the returned result matches the CLI/sample evidence.

A valid configuration file alone is not a successful integration. The acceptance criterion is a real tool invocation through OpenCode and a verifiable response.

If integration fails, inspect server logs and process output, identify the root cause, make a minimal reversible correction, and retest.

## 8. Phase F — Evaluate other agents

Only after OpenCode integration is proven, evaluate Hermes, Pi, and Alphacode separately.

For each client:

- Inspect the actual installed version and current documented tool/MCP configuration mechanism.
- Determine whether REA supports that client and whether the client supports the required transport.
- Inspect existing configuration before making changes.
- Use the documented setup route or a minimal manual configuration only when the format is verified.
- Preserve unrelated settings and credentials.
- Restart/reload the client and verify an actual REA tool call.
- Record the result as `VERIFIED`, `PARTIAL`, `BLOCKED`, `NOT TESTED`, or `UNSUPPORTED`.

Do not assume that one client's MCP configuration can be copied to another. Do not edit the internals of Hermes, Pi/FAS, or Alphacode when a separate configuration can achieve the same goal. Avoid running multiple heavy agents or duplicate servers concurrently on this phone.

## 9. Phase G — Assess reverse-engineering tool coverage

Determine which analysis capabilities are genuinely available in this environment. Inspect dependencies and test availability before claiming support for any category.

Potential targets include:

- JavaScript and Electron projects.
- Android APK contents and DEX/resources.
- Native ELF binaries and shared libraries.
- .NET assemblies.
- Static-analysis workflows and, if explicitly supported, dynamic/runtime analysis.

REA is an orchestrator/integration layer; do not assume every reverse-engineering engine is bundled with it.

For Android packages, tools such as JADX or Apktool may be relevant, but install them only if needed and after checking compatibility and resource costs. For native binaries, verify whether a suitable engine such as Ghidra or another supported tool is realistically usable on Android/Termux. Do not assume desktop Linux instructions apply to Android/Bionic.

Prefer lightweight static inspection first. Do not install heavyweight engines merely to make the environment appear complete. If a capability requires a separate host or external service, explain the requirement and do not upload private target files without explicit authorization.

Only analyze software the user owns or is authorized to assess. Do not perform credential theft, unauthorized access, or testing against systems without permission.

## 10. Phase H — Resource-aware operation

Measure memory and disk before and after significant tests. Use conservative defaults:

- One analysis job at a time.
- No persistent background service unless necessary and explicitly justified.
- Reasonable command timeouts.
- Avoid large outputs in model context; save full results to disk and summarize them.
- Do not run large builds or multiple heavyweight clients concurrently.
- Do not kill unrelated processes to free memory.
- If memory pressure becomes unsafe, stop the current task gracefully and document the blocker.
- Do not claim that RSS alone represents total system memory consumption.

A successful setup that destabilizes Termux is not an acceptable outcome.

## 11. Phase I — Optional local helper commands

If the core integration works, create small local helper scripts only where they materially simplify use. Possible helpers:

- Check REA CLI readiness.
- Check the MCP server/client connection.
- Run a documented analysis command on an explicitly supplied path.
- Save results under `~/rea-lab/reports/`.
- Record before/after memory snapshots.
- Produce clear error messages for missing dependencies or invalid paths.

Validate user-supplied paths and arguments. Do not automatically analyze arbitrary files. Do not add startup hooks, persistent daemons, broad permissions, or destructive cleanup.

## 12. Safety and authorization boundaries

You are authorized to perform routine, reversible local actions required for this mission. However:

- Never delete user data, repositories, credentials, or configuration.
- Never overwrite an entire configuration file when a minimal merge is possible.
- Never request root access or attempt to bypass Android security/bootloader protections.
- Never upload private files to external services without explicit permission.
- Never publish code, push commits, create accounts, or incur paid costs.
- Never modify unrelated projects.
- Do not perform irreversible or destructive actions without separate explicit approval.
- If a step requires unavailable permissions, payment, external data transfer, or a risky irreversible change, stop at that boundary and report the exact blocker.

## 13. Verification and regression checks

At minimum, test and record:

1. CLI help/version or the documented equivalent.
2. Successful analysis of the controlled sample.
3. Evidence/results match the sample's known behavior.
4. Report generation.
5. Graceful handling of a nonexistent path.
6. Missing-dependency/error behavior when safely testable.
7. OpenCode MCP connection.
8. A real REA tool invocation inside OpenCode.
9. Existing MCP configuration preserved.
10. No credentials leaked into reports.
11. OpenCode still launches.
12. Hermes, Pi/FAS, and Alphacode were not damaged; perform lightweight launch/config checks where available without triggering expensive workflows.

After any fix, rerun the relevant failed test. Never claim a test passed without observing evidence.

## 14. Required final report

Create:

`~/rea-lab/reports/REA_TERMUX_COMPLETION_REPORT.md`

Include:

- Timestamp and environment baseline.
- Official source and exact REA version/package.
- Compatibility findings and documentation references.
- Installation method and exact commands.
- CLI/server startup results.
- Sample project description and analysis evidence.
- OpenCode MCP configuration and real tool-call result.
- Separate Hermes, Pi, and Alphacode status.
- External engines/tools actually available and tested.
- RAM, swap, and storage observations.
- Files created or changed and backups made.
- Tests, outcomes, and evidence.
- Known limitations and unresolved blockers.
- Safe daily-use commands.
- Final verdict: `PASS`, `PARTIAL`, or `FAIL`.

Use these capability labels consistently:

- `VERIFIED`: successfully tested with observable evidence.
- `PARTIAL`: some components work, but a material part remains unavailable or unverified.
- `BLOCKED`: a specific blocker prevents progress.
- `NOT TESTED`: not actually tested.
- `UNSUPPORTED`: incompatibility or lack of support has been established with evidence.

Declare `PASS` only if the CLI works, a controlled analysis succeeds, and OpenCode can invoke a real REA tool with a verifiable result, without material damage to the existing environment. Use `PARTIAL` if some functions cannot be verified because of a clearly stated platform or external requirement. Never hide failures.

## 15. Execution protocol

Work autonomously through this loop:

**Discover → Plan → Execute → Test → Diagnose → Fix → Retest → Document.**

Do not ask the user to perform routine checks that you can safely run yourself. Do not stop after the first failure; diagnose it and try the smallest evidence-based fix. Do not repeat a failed attempt without changing the diagnosis or approach.

If the current OpenCode runtime cannot access the phone's Termux filesystem or execute local commands, state that limitation immediately. Do not pretend to have inspected or changed the device. In that case, prepare the exact, minimal Termux-side commands or scripts needed and clearly distinguish prepared work from executed work.

Begin with Phase A now, then continue through all safe phases and leave the final report at the specified path.
