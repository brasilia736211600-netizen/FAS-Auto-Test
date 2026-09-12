# FAS — Full Autonomous Stack

## 0. Status

- Repository: `brasilia736211600-netizen/FAS-Auto-Test`
- Active branch: `fas-feature-test`
- Purpose: build and validate a phone-first autonomous software-engineering stack controlled from Termux.
- Current validated implementation stage: autonomous local execution, testing, recovery, commit, subagents, parallel work, shared `.fas` state, and model benchmarking.
- Next engineering stage: formalize model policy/router, finalize `.fas` state contract, add Git push and GitHub Actions CI ingestion, then bounded autonomous CI recovery and end-to-end validation.

This document is the official human-readable FAS master plan. It is intentionally free of secrets, API keys, tokens, private keys, and encryption passwords.

---

## 1. Vision

FAS (Full Autonomous Stack) is an orchestration and engineering-control layer around OpenCode.

The user should provide one high-level task. FAS should then coordinate discovery, planning, implementation, testing, independent verification, commit/push, CI validation, diagnosis, and bounded recovery with minimal human intervention.

### Target loop

```text
YOU
  |
  v
ONE TASK / GOAL
  |
  v
FAS ORCHESTRATOR
  |
  v
OpenCode
  |
  +--> Agent / Subagents / Models / Parallelism
  |
  v
Discovery / Planning
  |
  v
Parallel Subagents when independence is proven
  |
  v
Shared FAS State (.fas/)
  |
  v
Build / Implementation
  |
  v
Tests
  |
  v
Independent Review / Verification
  |
  v
Commit
  |
  v
Push
  |
  v
GitHub Actions
  |
  +--> PASS --> DONE
  |
  +--> FAIL --> logs --> diagnosis --> repair --> tests --> commit --> push --> CI
```

---

## 2. Core Responsibility Split

### OpenCode

OpenCode is the primary coding engine and execution environment.

It is responsible for:
- repository exploration;
- planning and implementation;
- agent and subagent invocation;
- selecting or using the model configured by FAS;
- editing files;
- running commands and tests inside the workspace.

### FAS

FAS is the orchestration, policy, state, verification, and recovery layer.

FAS is responsible for:
- task normalization;
- lifecycle control;
- model capability policy/router;
- safe concurrency decisions;
- durable shared state;
- evidence collection;
- independent verification;
- bounded retries and recovery;
- git safety policy;
- CI result ingestion;
- deciding whether the task is actually complete.

FAS must not duplicate capabilities that OpenCode already performs reliably. YAGNI applies to the orchestration layer.

---

## 3. Non-Negotiable Engineering Principles

1. TDD whenever behavior is changed or introduced.
2. YAGNI: implement only what is needed by the task and current architecture.
3. Evidence over claims: tests, diffs, git status, CI logs, and concrete artifacts are authoritative.
4. Never treat an agent Todo state as proof of completion.
5. Use parallelism only when work is genuinely independent and merge/conflict risk is understood.
6. Keep autonomous recovery bounded; no infinite retry loops.
7. Git is the source of truth for code state.
8. `.fas/` is the source of truth for operational orchestration state.
9. Do not expose secrets to free or untrusted model providers.
10. Do not use destructive git operations in autonomous mode.
11. Prefer minimal, reversible changes.
12. Runtime-phone testing is reserved primarily for consolidated validation; routine progress must not block on repeated manual APK testing.

---

## 4. Proven OpenCode Agent Model

Validated Subagents:

- `Explore`: read-only repository/code exploration.
- `General`: suitable for independent multi-unit work and parallel tasks.
- `Scout`: documentation/dependency research.

Primary agents used by the validated OpenCode workflow:
- `Plan`
- `Build`

OpenCode has demonstrated actual subagent invocation and parallel execution in FAS benchmarks. FAS should therefore orchestrate at the task level rather than inventing a second agent framework.

FAS must not hard-code assumptions such as "model X always uses Explore" or "model Y always performs Build". OpenCode should retain agent selection freedom where possible.

---

## 5. Durable FAS State

The orchestration state must survive session loss, model changes, and agent restarts.

Target structure:

```text
.fas/
  state.json
  plan.md
  findings/
  decisions/
  artifacts/
  verification/
  logs/
```

### Required state concepts

`state.json` should eventually record at least:
- task identifier;
- current lifecycle phase;
- selected capability class/model;
- attempt number;
- active work units;
- artifact paths;
- test command and result;
- verification result;
- git commit SHA when committed;
- CI run identifier/result when available;
- failure classification and recovery status;
- timestamps needed for external-duration measurement.

### State rules

- State must be machine-readable where practical.
- Findings should be stored as durable artifacts, not only returned through chat/session memory.
- Main agents must be able to consume findings written by subagents.
- State must distinguish planned, attempted, verified, committed, and CI-validated status.
- A checked box is not proof unless backed by evidence.

---

## 6. FAS Lifecycle

The target lifecycle is:

```text
READ
  -> VERIFY
  -> RECONCILE
  -> PLAN
  -> EXECUTE
  -> TEST
  -> DIFF
  -> REVIEW
  -> COMMIT
  -> PUSH
  -> CI
  -> RECOVER (bounded, only on failure)
```

### READ
Read authoritative repository context and task inputs.

### VERIFY
Establish current branch, clean/dirty state, relevant files, test baseline, and applicable project rules.

### RECONCILE
Resolve conflicts between task requirements, repository reality, and stored FAS state.

### PLAN
Create a minimal implementation plan with explicit verification criteria.

### EXECUTE
Use OpenCode agents/subagents and parallelism only where justified.

### TEST
Run focused tests first, then broader relevant tests.

### DIFF
Check patch correctness, scope, and `git diff --check`.

### REVIEW
Perform an independent verification pass. The reviewer must not simply trust the implementation agent's self-report.

### COMMIT
Commit only verified task-related changes with a compliant message.

### PUSH
Push only through the configured safe branch policy.

### CI
Consume GitHub Actions results and logs.

### RECOVER
On failure, classify the failure, repair the smallest necessary scope, retest, re-review, and retry within a strict attempt limit.

---

## 7. Safe Git Policy

Autonomous mode must not execute:

- `git reset --hard`
- `git clean`
- force-push
- arbitrary deletion of unrelated files
- checkout/overwrite operations that destroy user work
- writes outside the intended workspace

Before mutation:
- establish repository and branch;
- reject unexpected dirty state unless the workflow explicitly allows it;
- keep task scope bounded;
- inspect the resulting diff before commit.

---

## 8. Current FAS Runner

Validated runner path:

```text
~/bin/fas-run
```

Current execution contract:

```text
fas-run <repo> <task-file>
```

Current behavior:
- rejects dirty working trees;
- invokes `opencode run --auto --model provider/model --agent build`;
- supports `FAS_MODEL`;
- supports `FAS_TEST_CMD`;
- performs `git diff --check`;
- supports optional autonomous commit through `FAS_COMMIT=1`;
- does not yet implement autonomous push/CI recovery.

The runner is intentionally small. New orchestration should be introduced only when required by the next lifecycle gaps.

---

## 9. Proven Capabilities

The following capabilities have been demonstrated in the FAS test repository:

### Autonomous coding
OpenCode created and modified project files from a task prompt and executed tests.

### Recovery
OpenCode corrected intentionally broken behavior and reached passing tests.

### Engineering fixes
Multiple tasks with several seeded defects were repaired with successful tests.

### Autonomous commit
With `FAS_COMMIT=1`, the runner produced a verified git commit and left the working tree clean.

### Subagents
OpenCode actually launched subagents rather than merely claiming to do so.

### Parallel subagents
Two Explore agents were actually launched in parallel for an FAS benchmark.

### Shared state
Subagents wrote durable `.fas/findings/*.md` artifacts and a state file; the main agent consumed those artifacts in later execution.

### Independent verification
A separate verification pass has been used to expose bugs that implementation-side self-reports did not reliably surface.

### External timing
FAS benchmarks use wall-clock duration measured outside the model's own reported timing, because model self-reported timing is not considered authoritative.

---

## 10. Model Policy

FAS should not permanently hard-code a single model as universally best.

Instead use capability classes:

```text
FAST / SIMPLE
NORMAL CODING
COMPLEX / AMBIGUOUS
EXPLORATION
RECOVERY
CRITICAL REVIEW
```

The router should use measured evidence and task characteristics. Candidate models have included:

- `opencode/ling-3.0-flash-fin-free`
- `opencode/nemotron-3.5-lightning-free`
- `opencode/nemotron-3-ultra-free`
- `opencode/mimo-v2.5-free`
- `opencode/muse-spark-1.3-contributor-free`
- `opencode/big-pickle`

Current benchmark interpretation is qualitative, not a permanent ranking:
- Ling: very fast and strong discovery, but needs scope guardrails.
- MiMo: strong speed/quality balance; narrower edge-case discovery in some tests.
- Muse: strong balanced behavior and good scope discipline.
- Big Pickle: strongest overall balance in the latest multi-layer benchmark.
- Nemotron 3.5 Lightning: reasonable speed but shallower discovery in some tasks.
- Nemotron 3 Ultra: stronger reasoning in some cases, but high latency.

These observations must remain empirical and revisable. Free-model availability and behavior can change.

---

## 11. Model Router Requirements

The next router must:

1. classify task difficulty/capability needs;
2. choose from currently available configured models;
3. avoid rigid model-to-phase mappings unless evidence requires them;
4. record selection rationale in `.fas/state.json`;
5. measure actual wall time;
6. support fallback after bounded failure;
7. avoid sending secrets or sensitive repository content to unsuitable providers;
8. remain replaceable when model availability changes.

The first version should be deterministic and small rather than an ML-based router.

---

## 12. Verification Architecture

Verification is intentionally separate from implementation claims.

Minimum local verification pipeline:

```text
focused tests
  -> relevant suite
  -> git diff --check
  -> inspect changed files
  -> independent review
  -> git status
```

CI verification pipeline:

```text
push
  -> GitHub Actions
  -> status/log capture
  -> PASS or FAILURE CLASS
```

Failure classes should eventually include:
- test failure;
- lint/static analysis failure;
- build failure;
- dependency/toolchain failure;
- workflow/configuration failure;
- environment/network failure;
- scope/safety violation;
- unclear/unknown failure.

Only failures that are safely actionable should enter autonomous repair.

---

## 13. Autonomous Recovery

Recovery must be bounded.

Target policy:

```text
MAX_ATTEMPTS = 3
```

The exact value may be adjusted by evidence, but there must always be a hard upper bound.

Recovery loop:

```text
CI/local failure
  -> collect evidence
  -> classify failure
  -> create minimal repair hypothesis
  -> implement repair
  -> focused tests
  -> full relevant tests
  -> independent review
  -> commit
  -> push
  -> CI
```

Stop conditions:
- verified success;
- maximum attempts reached;
- unsafe or ambiguous failure;
- unrelated repository changes detected;
- missing required credentials/tooling;
- repeated identical failure without new evidence.

---

## 14. GitHub / CI Integration

Target capabilities:

- safe branch push;
- GitHub Actions workflow execution;
- run/result identification;
- log retrieval;
- failure diagnosis;
- bounded repair;
- second CI attempt;
- final durable verification record.

GitHub remains the authoritative remote source of truth for repository code and CI state.

---

## 15. GitHub Actions Testing Strategy

The project should prioritize automated CI over repeated manual phone testing.

Recommended layers:

1. Unit tests.
2. Repository integration tests.
3. FAS runner tests.
4. Autonomous-agent smoke tests.
5. Git/commit safety tests.
6. GitHub Actions validation.
7. Consolidated Android runtime validation at the end when required.

The CI pipeline must not depend on the user's physical Android device for ordinary development progress.

---

## 16. Secret Handling

The official FAS plan must never contain the encryption key.

When confidential plan storage is needed:
- use GitHub Environment/Secrets;
- keep the secret out of Git history;
- never pass it as an ordinary workflow input;
- do not print it in logs;
- use short-lived encrypted/decrypted artifacts;
- delete temporary artifacts when no longer required.

The repository currently contains workflow scaffolding for plan encryption/decryption. Those workflows are not part of the core FAS execution loop and should be corrected/tested before being relied upon for cryptographic storage.

Important implementation note: the earlier encryption workflow used OpenSSL AES-GCM through `openssl enc`; many OpenSSL versions do not support AEAD modes such as GCM through `enc`. This must be fixed before the workflow is considered production-valid.

---

## 17. Current Known Limitations

1. Push is not yet integrated into the local FAS runner.
2. GitHub Actions result ingestion is not yet integrated into an autonomous repair loop.
3. Model routing is not yet formalized as a tested policy component.
4. `.fas/state.json` schema is conceptually defined but not yet finalized as a stable contract.
5. Recovery is demonstrated locally but not yet closed through the full GitHub CI loop.
6. Free-model behavior/availability may change.
7. Some model benchmark tasks contained architectural ambiguity; benchmark rankings must not be treated as absolute.
8. The current encryption workflow requires correction before confidential-plan automation is trusted.

---

## 18. Immediate Next Engineering Sequence

The next work sequence is deliberately narrow:

### Stage A — Model Policy / Router

Build a minimal capability-based router with:
- task classification;
- model candidate registry/config;
- fallback policy;
- external timing;
- state recording;
- tests.

### Stage B — Stable `.fas` State Contract

Define and test the first stable `state.json` schema and lifecycle transitions.

### Stage C — Safe Push

Extend the runner with an explicit safe push stage after successful verification/commit.

### Stage D — GitHub Actions Validation

Add a CI workflow that exercises the FAS repository's required tests and emits machine-consumable status information.

### Stage E — CI Failure Ingestion

Capture workflow result and logs, classify failure, and write evidence into `.fas/verification/` and `.fas/logs/`.

### Stage F — Bounded Autonomous CI Recovery

Implement a small recovery controller with a strict maximum retry count.

### Stage G — Full End-to-End Benchmark

Validate the complete path:

```text
task
 -> model selection
 -> OpenCode
 -> subagents/parallelism when justified
 -> shared state
 -> implementation
 -> tests
 -> independent review
 -> commit
 -> push
 -> GitHub Actions
 -> intentional failure
 -> diagnosis
 -> repair
 -> retest
 -> commit
 -> push
 -> CI PASS
```

Only after Stage G should FAS be considered a consolidated autonomous engineering loop.

---

## 19. Definition of Done for FAS Core

FAS Core is considered complete when a single task can be handed to FAS and, without routine human intervention, it can:

1. inspect authoritative repository state;
2. choose an appropriate model capability path;
3. plan and execute the change through OpenCode;
4. use subagents/parallelism when justified;
5. persist shared state and findings;
6. run required tests;
7. perform independent verification;
8. reject unsafe/unrelated changes;
9. commit verified changes;
10. push through safe policy;
11. read GitHub Actions outcome;
12. repair actionable failures within a bounded retry budget;
13. stop with durable evidence of success or a precise failure state.

The system is not complete merely because an agent says "done" or because local tests pass.

---

## 20. Change-Control Rule for This Plan

This file is the official plan reference, but it is not self-updating.

After each major FAS milestone, review whether this plan remains accurate.

A new official version must only be written to GitHub after explicit human authorization.

No automatic milestone process may silently replace the official plan.

---

## 21. Evidence Log Snapshot

Validated repository milestones to date include:

- `511a6d6` — `test: establish FAS autonomous baseline`
- `4d63122` — `test: validate FAS runner execution`
- `49b3540` — `feat: autonomous FAS task`

Latest validated commit `49b3540` demonstrated autonomous task execution with tests, diff validation, and an actual autonomous commit.

Subsequent benchmarks also validated subagents, parallel subagents, shared state, independent verification, recovery, and comparative model testing.

---

## 22. Guiding Principle

FAS should remain a small, evidence-driven control plane around a capable coding engine.

Do not build orchestration for its own sake.

Every new component must answer three questions:

1. What failure or capability gap does it solve?
2. What evidence verifies that it works?
3. Why can OpenCode, GitHub Actions, or an existing project mechanism not already solve it safely?

If those answers are not clear, do not add the component.
