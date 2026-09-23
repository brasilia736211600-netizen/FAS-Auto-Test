# FAS-Pi Master Project Map

Updated: 2026-09-23

## 1. Identity

FAS = **Full Autonomous Stack**.

Current engineering target: make Pi a dependable autonomous coding substrate by placing a central FAS supervisor/policy layer around Pi's existing harness, while preserving Pi core responsibilities and avoiding duplicate orchestration systems.

## 2. Target architecture

```text
USER
  |
  v
PI CORE
  |
  +--> AUTOPILOT
  |
  +--> WORKFLOW
  |      |
  |      +--> SUBAGENTS
  |
  v
CENTRAL FAS SUPERVISOR
  |
  +--> task classification
  +--> role/capability selection
  +--> provider/model selection
  +--> deterministic ranking
  +--> bounded fallback
  +--> evidence and reliability learning
  +--> thinking/output/context efficiency policy
  |
  v
EXECUTION
  |
  +--> real provider
  +--> child agents
  +--> tools
  |
  v
EVIDENCE
  |
  +--> child result contract
  +--> tests
  +--> runtime telemetry
  +--> receipts
  +--> conflicts
  |
  v
VERIFICATION -> REVIEW -> CHECKPOINT/STATE -> DONE
```

## 3. Responsibilities by layer

### Pi Core

Own the core agent harness, context/session model, native compaction, model/provider APIs, TUI/RPC/SDK facilities, and normal extension lifecycle.

FAS must not create a competing compaction engine or replace Pi's context machinery.

### Autopilot

Own high-level task orchestration/lifecycle.

### Workflow

Own phases, dependencies, DAG/phase ordering, and child execution semantics.

### Subagents

Own child dispatch/execution.

### FAS

Own centralized policy decisions that must remain consistent across parent and child execution:

- model/provider routing;
- capability filtering;
- deterministic ranking;
- bounded fallback;
- evidence-based escalation;
- reliability/learning state;
- thinking/output efficiency where the Pi API supports it;
- telemetry that can be observed without inventing unsupported APIs.

FAS is not a second workflow engine.

## 4. Current FAS runtime contract

Current provider/model:

`fas-router / auto`

Current commands:

- `/fas-router:on`
- `/fas-router:off`
- `/fas-router:status`
- `/token-efficiency`

Current knowledge store:

`~/.pi/agent/fas-knowledge.json`

Knowledge policy:

- v1;
- bounded to 200 records;
- keeps 100 recent records;
- threshold-based learning;
- recovery clears failure pressure;
- persistence/reload/corrupt-state fail-safe proven.

## 5. Current baseline evidence

Known current baseline from the project execution reports:

- release status: `RELEASE-STABLE-WITH-PLATFORM-LIMITATIONS`;
- latest full suite: **324/324 GREEN**;
- component history preserved: 21 + 13 + 9 + 64 + 57 + 37 + 75 + 12 + 11 + 25;
- FAS core md5: `33aa88d56a7f94d2bc877a40a086c0a1`;
- FAS index md5: `669fdeb74f8cbaaa7be19e4e726ec73f`;
- FAS package md5: `cfde92559392c96f88537fec99ecb8e4`;
- /compose md5: `59a2b7e5`;
- subagents tool-list md5: `8426bc05`;
- workflow runner md5: `0d9352e3`;
- autopilot md5: `0b542928`.

These hashes describe the captured project baseline and should be rechecked from the actual runtime/source before treating them as current after modifications.

## 6. Completed hardening

### Compaction

Manual `ctx.compact()` invocation from `turn_end` was removed after it caused a compaction reentrancy problem.

Regression: 9/9.

Native Pi compaction remains authoritative.

### Thinking control

FAS uses Pi's thinking API rather than inventing a separate thinking mechanism.

Proven:

- `ctx.thinkingLevel`;
- `pi.setThinkingLevel()`;
- minimum-sufficient thinking;
- evidence-based escalation;
- max output token enforcement.

Unsupported Pi extension APIs remain advisory-only; FAS must not pretend to enforce unsupported maxRounds/trim controls.

### Provider discovery/routing

FAS discovers provider-local shortlists (3-5), then applies:

- global deduplication;
- self-exclusion;
- capability filtering;
- deterministic ranking;
- available/verified-live separation.

Historical catalog counts are not treated as current availability.

### Fallback and learning

Fallback is bounded to:

- up to 3 candidate attempts;
- at most one previous-model delegation.

Known proof: forced two failures followed by success, 37/37 focused suite.

Learning threshold: 3 consecutive failures.

Recovery clears the failure pressure.

### /compose

`/compose` is frozen and isolated from FAS design changes.

Semantics:

- multiline modal;
- Enter = newline;
- Ctrl+Enter = send;
- Esc/Ctrl+C = cancel;
- complete text is sent once via Pi's message API;
- empty input rejected.

Release tests: 21/21.

Never modify `/compose` as part of FAS improvements unless a separately proven regression requires it.

## 7. Completed integration seams

### 2E: Subagents <-> FAS

When the parent model is `fas-router/auto`, the subagents tool-list seam appends:

- FAS extension load;
- `--model fas-router/auto`.

No broad FAS/compose/Pi-core/Autopilot rewrite was needed.

### 2F: Workflow <-> FAS

Workflow child spawning is FAS-aware when the effective child model is `fas-router/auto`.

The seam preserves:

- phase model overrides;
- thinking;
- tools;
- DAG behavior;
- RPC/error behavior.

Focused seam suite: 25/25.

Full suite after integration: 324/324.

### 2G evidence gate

Result: **NO-2G**.

Live knowledge evidence showed 168/169 and 44/44 successes with zero keys at consecutiveFailures >= 2 under a threshold of 3. No tuning was justified and no production files were changed.

## 8. Linux runtime proof status

### Codespace

Used for Linux-only runtime proof because Android/Termux cannot satisfy the required child-process cgroup-v2 path.

The earlier Linux environment was validated with:

- Ubuntu 22.04;
- Linux 6.8.x x86_64;
- cgroup-v2;
- Node 26.4.0;
- Pi 0.85.1.

### Leg 1: child FAS path

**CLOSED.**

Live proof observed a child process chain including:

`node wrapper -> bwrap -> node cli.js --mode rpc ... -e pty-subagents-harness.ts -e FAS index.ts -e subagents/index.ts --model fas-router/auto --thinking off`

The child routed through the pty provider harness and completed successfully.

### L6: all-candidates-fail/no-previous-model

**CLOSED.**

Live execution produced the clean no-fallback outcome:

`FAS router: no eligible candidate; no fallback model available`

No TypeError/crash occurred.

### Leg 2: Workflow success path

**OPEN / NOT YET EXECUTED.**

Required proof:

`Workflow -> child -> FAS -> real provider -> successful turn -> workflow success`

One provider credential must be available in the same process environment that launches Pi.

## 9. Codespace/toolchain state

Most recent toolchain repair:

- default Node switched from 24.21.0 to 26.4.0 using pre-existing nvm;
- `nvm alias default 26.4.0`;
- fresh shell reported Node v26.4.0;
- Pi 0.85.1 became available on PATH because the pre-existing install belonged to the selected Node 26.4.0 environment;
- `process.platform` = linux;
- no Pi/FAS repository files were modified;
- Codespace was stopped.

At that moment `OPENROUTER_API_KEY` was absent from the exact shell used by the validation run. The user later observed it set in a different shell. Therefore credential visibility remains a same-process runtime precondition, not a permanently proven environment fact.

## 10. External research-derived design rules

### Pi Skills

Use Skills for specialized instructions and supporting files that should be loaded on demand, not for new executable integration points.

Implication for FAS:

Potential future declarative policy skills:

- routing policy;
- verification policy;
- evidence policy;
- recovery policy;
- autonomous coding policy.

These must not duplicate FAS executable logic.

### Pi Packages

Packages can ship extensions, skills, prompt templates, and themes together and can be installed from npm, git, URL, or local path.

Third-party executable package source must be reviewed before installation.

Implication: prefer small, version-pinned, purpose-specific additions rather than installing a large bundle of overlapping agent frameworks.

### AlphaCode

Useful concepts:

- smallest-change rule;
- explicit verify phase;
- structured child reports;
- file conflict detection;
- phase quality gates;
- checkpoints;
- persistence before execution.

Do not import its entire runtime; use the concepts only where they close a demonstrated FAS gap.

### OpenMuse

Useful concepts:

- durable jobs;
- checkpoints and leases;
- saved action receipts;
- pause/resume/cancel/retry;
- persistent browser/workspace;
- server-side policy gateway;
- explicit handling of uncertain external writes.

These are future durability patterns, not a reason to replace Pi or add a second orchestrator now.

### Freebuff

Useful concepts:

- multiple model options;
- specialized agents;
- zero-key/free access as an availability strategy.

Security/privacy note: Freebuff's current policy describes processing of prompts, code, files, repository data and agent traces, and data treatment can depend on the selected product/model/features. Treat third-party hosted agents as policy-controlled providers, not as the trust boundary for private project state.

### Themes

Themes are presentation-only. They should be considered after runtime correctness, evidence, durability, and safety.

## 11. Design decisions

### D1 — Keep Pi as the harness

Do not replace Pi with AlphaCode, Freebuff, OpenMuse, or another coding-agent runtime.

### D2 — Keep FAS centralized

A single FAS supervisor should decide model/provider policy for parent and child execution.

### D3 — Do not add another orchestrator

Autopilot + Workflow + Subagents already provide orchestration semantics.

### D4 — Pi core owns compaction/context

Do not implement a parallel compaction system.

### D5 — Prefer Skills for declarative policy

Policy text that is not an executable integration point should be load-on-demand.

### D6 — Evidence before enhancement

A new subsystem requires a demonstrated deficiency plus focused regression proof.

### D7 — Local providers are a future resilience lane

FAS may discover/verify local model providers and use them when capability and reliability permit, rather than hard-coding them as always-on fallbacks.

### D8 — Durability is a later capability layer

Journal/checkpoint/receipt/lease/resume can extend FAS after the current runtime gate is closed.

### D9 — Provider routing and tool/service routing can remain separate

A model can be best for reasoning while a different service is best for web/browser access. Do not collapse these concerns prematurely.

## 12. Non-goals

Do not add:

- a second compaction engine;
- a second memory engine;
- a second workflow engine;
- a second model router;
- another /compose implementation;
- an all-in-one third-party agent stack;
- unrestricted autonomous execution;
- dozens of third-party Pi packages without evidence;
- theme work before the core runtime gates are closed.

## 13. Target end state

The mature architecture should be:

`Pi -> Autopilot -> Workflow/Subagents -> FAS Supervisor -> capability-aware routing -> bounded execution/fallback -> evidence -> learning -> efficiency -> safety -> verification -> review`

with declarative FAS policies available as on-demand Pi Skills and with optional local-provider and durability capabilities added only after verification.

## 14. Definition of done for the current Pi/FAS runtime milestone

Leg 2 was live-proven on 2026-09-23
(`docs/FAS_PI/reports/LEG2_WORKFLOW_SUCCESS_2026-09-23.md`): Leg 1, L6, and Leg 2 are
all CLOSED and the 324/324 baseline is green. The Phase-1 runtime milestone is
complete.

The next milestone is Phase-2 implementation in the exact audit order B → C → A →
F → E → D (`docs/FAS_PI/reports/PHASE2_EVIDENCE_AUDIT_2026-09-23.md`), each step behind
its own focused test + full-suite + state save.

## 15. Hard anti-hallucination rule

When a future agent is unsure whether a capability is implemented:

1. inspect GitHub source;
2. inspect tests;
3. inspect saved reports;
4. run a focused proof if runtime behavior matters;
5. mark it UNKNOWN/BLOCKED rather than guessing.
