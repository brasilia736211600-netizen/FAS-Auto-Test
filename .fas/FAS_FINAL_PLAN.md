# FAS — Full Autonomous Stack

## 0. Status

- Purpose: phone-first autonomous software engineering controlled from Termux.
- Control engine: OpenCode.
- Control plane: FAS.
- Target: one user goal -> autonomous discovery/planning/build/test/review/commit/push/CI/recovery with minimal human intervention.
- Current milestone: portable runtime, model routing/fallback, durable state, Git safety, CI evidence/recovery primitives, and `fas watch` are implemented and tested.
- Latest validated CI milestone: 59 tests passed on GitHub Actions.
- Current next milestone: real E2E CI failure -> repair -> push -> CI PASS, then clean-room portability and final Termux packaging/security validation.

This file is the official human-readable FAS master plan. It contains no secrets.

---

## 1. Vision

```text
YOU -> ONE TASK -> FAS ORCHESTRATOR -> OpenCode
    -> agents/subagents/parallelism when justified
    -> shared .fas state
    -> implementation -> tests -> independent verification
    -> commit -> safe push -> GitHub Actions
    -> PASS -> DONE
    -> FAIL -> logs -> diagnosis -> repair -> tests -> commit -> push -> CI
```

FAS is the orchestration/policy/state/verification/recovery layer. OpenCode remains the coding and execution engine.

---

## 2. Non-Negotiable Principles

1. TDD for introduced/changed behavior.
2. YAGNI and minimal scope.
3. Evidence over claims.
4. Todo/check-box state is never completion proof.
5. Parallelism only when independence is proven.
6. Recovery has a hard bound; default `MAX_ATTEMPTS=3`.
7. Git is authoritative for code state.
8. `.fas/` is authoritative for FAS operational state.
9. Never expose secrets to unsuitable model providers.
10. No destructive Git operations in autonomous mode.
11. Prefer reversible, inspectable changes.
12. Physical-device testing must not block ordinary progress.
13. FAS must be portable across unrelated repositories.
14. Normal operation must not depend on ChatGPT, this conversation, chat memory, or one permanent model.

---

## 3. OpenCode Agent Model

Validated subagents:
- `Explore`: read-only exploration.
- `General`: independent multi-unit work and parallel tasks.
- `Scout`: documentation/dependency research.

Primary agents:
- `Plan`
- `Build`

OpenCode has demonstrated actual subagent invocation and parallel execution. FAS orchestrates at the task/policy level and does not create a duplicate agent framework.

---

## 4. Durable State

Operational structure:

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

The state contract records repository/task identity, lifecycle phase, route/model, attempt budget, tests, verification, Git data, CI data, failures, and timestamps. State must survive process/session/model changes.

`.fas/` is operational state, not project source. FAS excludes it locally from Git without changing the target project's tracked configuration by default.

---

## 5. Portability and Independence

FAS is installed once on the operator device and can target unrelated repositories:

```text
FAS installation -> Repository A
                 -> Repository B
                 -> Repository C
```

FAS must not copy its source into the target project. Normal operation must not require manual transfer of findings between models or any return to this conversation.

Human intervention is reserved for bounded stop conditions: missing credentials, unsafe/destructive actions, unresolved ambiguity, repeated failure, or missing required tooling.

A clean-room repository test is mandatory for completion.

---

## 6. Lifecycle

```text
READ -> VERIFY -> RECONCILE -> PLAN -> EXECUTE -> TEST
     -> DIFF -> REVIEW -> COMMIT -> PUSH -> CI
     -> RECOVER (bounded on actionable failure)
```

Each transition requires evidence appropriate to the phase.

---

## 7. Safe Git Policy

Never use:
- `git reset --hard`
- `git clean`
- force-push
- arbitrary deletion of unrelated files
- destructive checkout/overwrite operations
- writes outside the intended workspace

Before mutation, establish repository/branch state and detect unexpected changes. Before commit, inspect diff scope. Push is non-force and policy controlled.

---

## 8. Current Runtime

Portable CLI:

```text
fas init [repo]
fas run <task> --repo <repo>
fas watch --repo <repo>
```

Implemented runtime pieces include:
- `fas_cli.py`
- `fas_runtime.py`
- `model_router.py`
- `fas_fallback.py`
- `fas_git.py`
- `fas_ci.py`
- `fas_recovery.py`
- `fas_watch.py`

Optional controls include `FAS_MODEL`, `FAS_TEST_CMD`, `FAS_COMMIT`, `FAS_COMMIT_MESSAGE`, and `FAS_PUSH`.

---

## 9. Proven Capabilities

Demonstrated:
- autonomous coding/testing;
- local recovery from seeded defects;
- autonomous commit;
- real subagents;
- real parallel subagents;
- durable shared findings/state;
- independent verification;
- external wall-clock measurement;
- bounded model fallback;
- Git safety;
- GitHub Actions execution and evidence artifacts.

The latest validated CI run reached `59 passed`.

---

## 10. Model Policy

Capability classes:

```text
FAST / SIMPLE
NORMAL CODING
COMPLEX / AMBIGUOUS
EXPLORATION
RECOVERY
CRITICAL REVIEW
```

Previously benchmarked candidates include Ling, MiMo, Muse, Big Pickle, Nemotron 3.5 Lightning, and Nemotron 3 Ultra through their OpenCode model IDs.

The router is intentionally deterministic and capability-based. It records the planned route and effective model, supports bounded fallback, and does not treat any free model as permanently best. External wall time is authoritative over model self-reported timing.

---

## 11. Verification

Local evidence chain:

```text
focused tests -> relevant suite -> git diff --check
-> changed-file inspection -> independent review -> git status
```

CI evidence chain:

```text
push -> GitHub Actions -> status/log capture -> PASS or failure class
```

Actionable failures may enter autonomous repair; unsafe or unknown failures stop the system.

---

## 12. Autonomous Recovery

Target:

```text
MAX_ATTEMPTS=3
```

Recovery:

```text
CI failure
 -> collect logs
 -> classify
 -> smallest repair hypothesis
 -> OpenCode repair
 -> focused/relevant tests
 -> independent verification
 -> commit
 -> push
 -> CI
```

Stop on success, exhausted budget, unsafe ambiguity, unrelated changes, missing credentials/tooling, or repeated identical failure without new evidence.

Model fallback and CI recovery are separate controls.

---

## 13. GitHub / CI Integration

Implemented building blocks support:
- safe branch push;
- GitHub Actions execution;
- machine-readable CI evidence;
- failure-log capture;
- recovery-task generation;
- bounded `fas watch` recovery control.

The critical remaining proof is an actual end-to-end cycle where CI is intentionally failed, FAS consumes the failure, repairs it, pushes the repair, and observes CI PASS.

---

## 14. Testing Strategy

Priority:
1. unit tests;
2. repository integration tests;
3. FAS CLI/runtime tests;
4. agent/subagent smoke tests;
5. Git safety tests;
6. GitHub Actions validation;
7. real E2E CI recovery;
8. final Android runtime validation only when required.

Prefer combined automated checks and avoid repeated manual APK cycles.

---

## 15. Secrets and Encryption

The plan must never contain keys/tokens/passwords.

Confidential plan storage, when used, must rely on GitHub Environment/Secrets and short-lived artifacts. The existing encryption workflow scaffolding must be corrected and tested before being trusted; the previous `openssl enc` AES-GCM approach is not considered production-valid across OpenSSL versions.

Encryption is separate from the core autonomous coding loop.

---

## 16. Current Milestone

### Completed / validated
- Model capability router core.
- Durable state implementation/schema v1 tests.
- Model fallback with workspace-safety guard.
- Git commit and non-force push primitives.
- Portable CLI/bootstrap.
- CI evidence generation.
- CI log/recovery primitives.
- `fas watch` boundary.
- 59-test green GitHub Actions milestone.

### Still required
- real E2E CI failure -> recovery -> CI PASS;
- clean-room portability test on an unrelated repository;
- final Termux installer/package workflow;
- security/reliability review;
- final real-project validation.

---

## 17. Immediate Engineering Sequence

### Stage H — Real E2E Recovery

Use a disposable CI fixture that intentionally fails once. FAS must identify the correct run, ingest its logs, formulate a repair task, perform one bounded repair, retest, commit/push, and observe the next CI run reach PASS. Persist final evidence.

### Stage I — Clean-Room Portability

Use a repository with no FAS implementation files and prove the installed FAS runtime can initialize, execute, test, commit/push when enabled, watch CI, recover, and leave no unexpected FAS source files or Git configuration changes.

### Stage J — Termux Packaging

Produce the smallest practical installer/bootstrap for the phone-first environment so the CLI is available from any target repository.

### Stage K — Security / Reliability Gate

Review shell invocation, paths, Git safety, permissions, secrets, model providers, fallback rules, retry budgets, and stop conditions.

### Stage L — Final Consolidated Validation

Run the complete flow on a disposable repository, then one carefully selected real project. Only then declare FAS Core complete.

---

## 18. Definition of Done

FAS Core is complete only when one installed FAS instance, on a repository other than `FAS-Auto-Test`, can autonomously:

1. inspect authoritative repository state;
2. select a suitable capability/model path;
3. plan and execute through OpenCode;
4. use subagents/parallelism when justified;
5. persist state/findings;
6. run tests and independent verification;
7. reject unsafe/unrelated changes;
8. commit and push safely;
9. identify and consume GitHub Actions results;
10. repair actionable CI failures within a hard retry budget;
11. re-run verification and CI;
12. finish with durable evidence of success or a precise terminal failure.

Normal operation must not require this conversation, ChatGPT, manual model-to-model coordination, or one permanent model.

---

## 19. Change Control

This file is the official FAS plan and is not self-updating. It is updated only after explicit authorization. It must never contain secrets.

---

## 20. Guiding Principle

For every proposed component ask:

1. Does this directly support the autonomous engineering loop?
2. Is it independently verifiable?
3. Why can OpenCode, GitHub Actions, or an existing project mechanism not already solve it safely?

If these answers are not clear, do not add the component.
