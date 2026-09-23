# Phase-2 Evidence Audit (2026-09-23)

Read-only audits A–F performed AFTER Leg-2 closure (see
`../REPORTS/LEG2_WORKFLOW_SUCCESS_2026-09-23.md`), with zero source/test/CI/config
changes and zero package installs. Labels: `VERIFIED` (fresh source/test/runtime
evidence this cycle) · `HISTORICAL` (earlier recorded state) · `REPORTED` (prior
agent/run claim, not freshly reproven) · `UNKNOWN` (insufficient evidence).

Baseline for all findings: Pi `0.85.1`, FAS fingerprints
`33aa88d5/669fdeb7/59a2b7e5/8426bc05/0d9352e3`, suite `324/324 GREEN`.

## A. Pi Skills / progressive disclosure + token cost — VERIFIED mechanism, estimated savings

- VERIFIED: Pi 0.85.1 implements progressive disclosure (`dist/core/skills.js`:
  `loadSkills`/`loadSkillsFromDir`/`formatSkillsForPrompt`). Only
  name/description/location lines are injected per Skill; body loads on demand via
  the `read` tool. This is the correct vehicle for declarative FAS policy.
- VERIFIED: FAS executable surface that must NOT move into Skills: `discoverCandidates`,
  `hardFilter`, `scoreCandidate`, `rankCandidates`, `planFallback`, `decideThinking`,
  `planBudgets`, streaming supervisor (`~/.pi/extensions/fas/core.ts`, 618 lines /
  31,009 bytes; `index.ts` 4,448 bytes). Routing/fallback/thinking math stays code.
- VERIFIED: Skill-suitable declarative text exists: thinking/budget policy block
  (`core.ts` §`Thinking / budget policy`), task-inference bounds, evidence-escalation
  notes. Candidate minimal Skill set (3): `fas-thinking-policy`, `fas-routing-policy`
  (read-only description of how the router decides, for debuggability),
  `fas-evidence-conventions` (status/report/data shapes once B lands).
- Estimated cost: moving ~2–4 KB of stable policy out of the always-on path saves
  roughly that many input tokens per turn (~500–1,000 tokens at ~4 chars/token);
  Skill metadata costs ~10 lines total. Net win after ~2 turns. Exact measurement
  requires a before/after token diff test (listed below).
- Rejected: moving scoring/fallback/thinking-decision logic to Skills (executable
  logic in Markdown duplicates the router and cannot be unit-tested); bulk Skill
  installation before a concrete gap.
- Tests required: Skill load test (Pi discovers + lists, body NOT in prompt until
  read); token-diff test (input tokens with vs without Skill-ified policy over a
  fixed 3-turn script); full 324/324 regression (FAS behavior unchanged).
- Dependencies: B (contract shapes stabilize what `fas-evidence-conventions` documents).

## B. Minimal Child Result Contract — VERIFIED partial existence, concrete gap in subagents

- VERIFIED: workflow children ALREADY return structured results:
  `workflow_phase_result` tool (`status` + `report` + optional `data`,
  `terminate: true`, required non-empty status/report, optional status enum + data
  schema per phase output config). Leg-2's `LEG2-PROBE-OK` flowed through it.
- VERIFIED gap: subagents children relay unstructured completion (`CHILD-OK` +
  free text; parent matches text). No status enum, no required report, no
  files/tests fields, no parent-side validation.
- Candidate minimal envelope for subagents relay (each field justified):
  `status` (required enum: ok/fail/blocked — parent can branch deterministically);
  `report` (required Markdown — same bar as workflow phases); `files_modified`,
  `files_created` (arrays — parent verifies claims without re-reading the tree);
  `tests_run` (array of command+result — verification chain); `problems`,
  `conflicts` (arrays — honest failure surfacing); open `data` object (forward
  compatibility, mirroring workflow `data`). Drop nothing else; add nothing else
  (no durations/costs — telemetry already exists separately).
- Expected cost: +~150–300 output tokens per child turn; one extra validation pass
  in parent (no extra model turn on success).
- Rejected: replacing workflow's existing tool (it already satisfies the contract —
  B only extends the pattern to subagents + adds parent validation); free-text-only
  status (unverifiable); moving contract enforcement into a Skill (needs code).
- Tests required: schema test (valid/invalid payloads); parent-consumption test
  (parent branches on status, rejects missing report); subagents integration test
  extension (new W-cases in `test-fas-subagents-integration.mjs` style); 324/324.
- Dependencies: none (first in implementation order).

## C. Role + Capability + deterministic routing — VERIFIED deterministic base, no roles today

- VERIFIED: routing is centralized and deterministic: `hardFilter` (task constraints:
  `requiredInput`, `minContextWindow`, `needsReasoning`, excluded providers/models)
  → `scoreCandidate` (evidence-weighted: +successes, −failures×1.5,
  −consecutiveFailures×2, −latency, cost penalty, reasoning bonus) →
  deterministic tie-breaks (successes, latency, `modelKey` localeCompare) →
  `rankCandidates` fail-safe returns pool rather than nothing →
  `planFallback` bounded (3 candidates + max one previous-model delegation,
  HISTORICAL proof). No second ranker exists; none may be added.
- VERIFIED: no role/capability metadata exists in FAS today. (`brokerCapability` in
  subagents is an RPC auth token, unrelated.) Task classification exists only as
  bounded observable-input inference (`Task inference` section — no heuristics
  beyond inputs).
- Candidate (thin, no new ranker): role → task-constraint mapping. Roles kept:
  explorer (read-only tools, low thinking), implementer, tester (test tools,
  must return `tests_run`), reviewer (no-write tools, reads diff), debugger
  (failure evidence injected). Dropped: researcher (no distinct tool/capability
  need vs explorer — would duplicate). Capability fields kept: reasoning flag,
  tool compatibility, context capacity, thinking levels, provider availability,
  reliability state (already in KB). Dropped: vision requirement (no vision tool
  in the 0.85.1 FAS path — UNKNOWN need; re-add only with a vision tool present).
- Expected cost: role expansion is a pure function over existing KB fields (~0
  tokens); adds one determinism test vector per role.
- Rejected: per-role model lists (static, rots); second scoring system (competing
  source of truth); LLM-based role inference per turn (token waste, nondeterminism).
- Tests required: deterministic routing test (fixed KB+task → identical route ×N);
  role→constraint mapping test; fallback-with-roles test; 324/324.
- Dependencies: B (tester role's `tests_run` requirement needs the contract).

## D. Local-provider discovery/resilience — VERIFIED absent, design only

- VERIFIED: no local lane in Pi 0.85.1 distribution (`ollama|lmstudio` absent from
  `dist/`) and none in FAS (`core.ts` has no localhost/127.0.0.1 handling).
  FAS candidates come exclusively from Pi's model registry
  (`discoverCandidates(all, available)`, self-excludes `fas-router`).
- VERIFIED: no local endpoint on this host (Termux): `:11434` and `:1234`
  unreachable. Any local-provider claim is therefore UNKNOWN until a host with a
  live endpoint is tested.
- Candidate design (discovery-first, no assumptions): probe known endpoints →
  capability filter (registry-shape check: id, context window, reasoning flag) →
  live verification (one minimal turn) → use only when suitable → unavailable-path
  returns pool unchanged. Never assume local quality, availability, or cost.
- Expected cost: one probe per session start (2 HTTP GETs, ~0 tokens when absent);
  verification turn cost only when an endpoint answers.
- Rejected: hardcoded `ollama/*` candidates (phantom models when daemon absent);
  preferring local by default (quality UNKNOWN); local lane as core dependency.
- Tests required: discovery test (mock endpoint shapes); unavailable-path test
  (no endpoint → pool unchanged, zero errors); suitable-path test (mock suitable
  endpoint → candidate admitted with capability flags); fallback integration test.
- Dependencies: C (capability fields are where verified local flags attach). Last
  in order — needs a Linux host with a real daemon for the suitable-path proof.

## E. Durability gap — VERIFIED partial persistence, one demonstrated gap

- VERIFIED: workflow run-state persist/restore exists and is versioned
  (`snapshotRunState` with 50 KB cap, `persist` via session `appendEntry`,
  `restore()` on `session_start` with `SNAPSHOT_VERSION` check). FAS evidence KB
  persists across sessions (`fas-knowledge.json`, corrupt-state fail-safe,
  HISTORICAL proof).
- VERIFIED gap (source-traced): `restore()` rebuilds state for inspection but
  clears `activeController`/`activePromise`/`activeSlot` — a run interrupted
  mid-phase restores as reviewable state, NOT as a resumable run. Interruption
  trace: `timeout`/kill during a phase child → child process dies → snapshot holds
  completed phases + report-so-far → resume re-runs from phase 1 (completed-phase
  outputs are visible but not skipped automatically).
- Candidate (minimal): resume-from-phase entry point reusing the persisted snapshot
  (skip phases with terminal successful output, re-run from the first
  non-succeeded phase). No journal/lease/receipt framework — explicitly rejected
  until a gap THEY would close is demonstrated (none found: single-active-slot
  design means no concurrent-run conflicts; receipts add nothing over existing
  phase outputs).
- Expected cost: resume planning pass over snapshot phases (~0 model tokens,
  code-only); re-run cost bounded by remaining phases.
- Rejected: server-owned durable jobs/leases (OpenMuse pattern — solves a
  multi-worker problem this single-slot runner does not have); persistent
  tool-step recording (session JSONL already records it); checkpoint-bragging
  without a resume entry point.
- Tests required: kill-mid-phase test (snapshot exists, state reviewable);
  resume test (completed phases skipped, remainder re-runs, identical final
  report); version-mismatch test (old snapshot refused cleanly); 324/324.
- Dependencies: B (phase success must be machine-readable `status` for skip logic).

## F. Safety/permission gap — VERIFIED partial gates, two concrete gaps

- VERIFIED present: project-trust gating (`isProjectTrusted` scopes project
  workflow discovery; `--no-approve` CLI); FAS deep redaction (`redact()`:
  credential-shaped keys → `[REDACTED]`, numeric telemetry preserved);
  Python-line guards (`~/FAS/fas_git.py`: `FORBIDDEN_GIT_OPERATIONS =
  {reset --hard, clean, push --force/-f}`, scope-violation codes) — but those guard
  the Python CLI, NOT Pi child execution.
- VERIFIED gaps: (1) Pi-side FAS/workflow/subagents children run with full tool
  authority — no destructive-git gate in the dispatch path (`git push --force`,
  `reset --hard`, `clean -fd` via `bash` tool are unenforced); (2) no risky-tool
  classification surfaced to the router (a destructive task routes on latency,
  not on blast radius).
- Candidate minimal gates (keep/drop): destructive-git gate in child dispatch
  (deny `reset --hard`, `clean -fd`, `push --force/-f` unless explicit task
  declaration — KEEP, mirrors proven `fas_git.py` list); external-write review
  flag (KEEP, cheap: tasks touching outside `cwd` require declaration);
  secret boundary test (KEEP: redact() coverage test with OpenRouter-shaped keys);
  workspace scope (KEEP as declaration, same mechanism as external-write);
  risky-tool classification for routing demotion (KEEP minimal: destructive-capable
  tool use demotes candidate score slightly — uses existing scorer, no new system).
  Dropped: interactive approval prompts mid-autonomy (breaks the autonomy loop;
  declaration+deny is the deterministic substitute).
- Expected cost: gate checks are string matches (~0 tokens); one redaction pass
  over evidence records (already exists — test-only cost).
- Rejected: second permission framework; per-model safety tiers (no evidence any
  current candidate misbehaves — gates target ACTIONS, not models); blocking all
  network tools (would break provider turns).
- Tests required: concrete abuse tests (each forbidden git op denied with the
  exact gate error); external-write declaration test; redaction coverage test
  (credential-shaped values never in logs/evidence); score-demotion test; 324/324.
- Dependencies: none for gates; routing demotion fits naturally after C.

## Recommended implementation order (exact)

1. **B — Child Result Contract** (unblocks verifiable autonomy claims; no deps).
2. **C — Role + capability mapping** (needs B's `tests_run`/status shapes).
3. **A — Skills** (needs B's shapes documented; policy stable by then).
4. **F — Safety gates** (independent code, but most valuable once B/C route
   more autonomously; redaction test can land any time).
5. **E — Resume-from-phase** (needs B's machine-readable phase status).
6. **D — Local provider** (needs C's capability fields + a host with a live
   daemon for the suitable-path proof; discovery/unavailable-path tests can land
   earlier without the daemon).

Each step: smallest diff → focused test (baseline FAIL first) → 324/324 →
runtime proof only where the claim needs it → state save. No step may add a
package, a second router/ranker, a second orchestrator, or speculative tuning.
