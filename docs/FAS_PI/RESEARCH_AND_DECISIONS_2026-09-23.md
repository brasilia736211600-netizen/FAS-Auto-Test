# FAS-Pi Research and Architecture Decisions

Research date: 2026-09-23

## Scope

Reviewed the requested sources for architecture/capability lessons relevant to FAS-Pi:

- https://alphacli.github.io/
- https://github.com/dragonked2/alphacode
- https://github.com/CopilotKit/OpenMuse
- https://freebuff.ai/
- https://pi.dev/
- Pi documentation pages for Packages, Skills, and current releases.

This document records source-derived observations and the resulting FAS decisions. It does not treat marketing claims as runtime proof.

## 1. Pi

Source: https://pi.dev/docs/latest/skills

Key observation:
Pi Skills provide specialized instructions/supporting files and are loaded when the task needs them. This is a progressive-disclosure mechanism.

Decision:
Use Skills for declarative FAS policy where appropriate. Do not move executable routing/fallback logic into Skills.

Source: https://pi.dev/docs/latest/packages

Key observation:
Pi packages can bundle extensions, skills, prompt templates, and themes and can be installed from npm/git/local sources. Project package loading is gated by project trust, and executable extensions have the same process-level authority as Pi.

Decision:
Prefer small, version-pinned dependencies; review third-party executable code before installation; do not bulk-install overlapping agent frameworks.

Source: https://pi.dev/news/releases/0.87.1

Key observation:
Pi 0.87.1 was released 2026-09-22 and changes provider/model support and other behavior.

Decision:
Keep the current FAS baseline pinned to Pi 0.85.1 until a compatibility matrix proves a safe upgrade. No direct baseline upgrade.

## 2. AlphaCode

Sources:
- https://alphacli.github.io/
- https://github.com/dragonked2/alphacode

Useful architectural patterns observed in the repository/documentation:

- smallest-change + verify discipline;
- structured child-agent reports;
- file-conflict detection;
- phase quality gates;
- checkpoints;
- persistent tool-step recording.

Decision:
Use these as design references, especially the structured child result contract. Do not import AlphaCode's runtime or create a second agent engine.

## 3. OpenMuse

Sources:
- https://github.com/CopilotKit/OpenMuse
- https://github.com/CopilotKit/OpenMuse/blob/main/ROADMAP.md

Useful patterns:

- server-owned durable jobs;
- plans/checkpoints/leases;
- pause/resume/cancel/retry;
- saved action receipts;
- persistent browser/workspace state;
- explicit review for external writes;
- separate gateway/policy boundaries.

Decision:
Treat durability and action receipts as future FAS capability candidates, but only after a concrete gap is demonstrated in the current Pi/FAS loop.

Important limitation:
OpenMuse is an alpha application with its own client/server/worker architecture, not a direct replacement for the Pi harness.

## 4. Freebuff

Sources:
- https://freebuff.ai/
- https://freebuff.ai/privacy-policy

Observed capabilities include a free hosted lane, multiple model options, CLI/desktop/cloud surfaces, and specialized-agent positioning.

Privacy decision:
Freebuff's privacy policy states that prompts, code, files, repository data, agent activity/traces, and other project data may be processed by the service and/or model providers depending on product/model/features. FAS therefore must treat hosted third-party agents/providers as policy-controlled execution lanes, not as the core trust boundary for private project state.

Decision:
Freebuff is a reference for provider availability and specialized-agent patterns, not a dependency of the FAS core.

## 5. Cross-source conclusions

### C1 — Central supervisor remains correct

Multiple projects use task/role specialization. FAS should centralize the final model/provider choice rather than letting each agent independently choose an unrelated policy.

### C2 — Declarative policy should be lazy

Pi Skills provide a better fit than permanent system-prompt expansion for reusable policy text.

### C3 — Structured evidence is a real missing seam

Child agents should eventually return structured results that the parent can validate rather than relying on unstructured natural-language completion claims.

### C4 — Durability is distinct from model intelligence

OpenMuse and AlphaCode show durable task/checkpoint patterns. These are orthogonal to model routing and should not be mixed into the router itself.

### C5 — Hosted free models are availability, not trust

A free model lane can increase resilience, but secret/data policy must remain explicit.

### C6 — Tool/service routing may differ from model routing

A model can be suitable for reasoning while another service is suitable for browser/web access. FAS should avoid prematurely merging these decisions.

### C7 — Themes do not improve autonomy

Theme work is optional presentation work and should remain last.

## 6. Rejected directions

Reject for the current baseline:

- replacing Pi with AlphaCode;
- replacing Pi with OpenMuse;
- making Freebuff a core runtime dependency;
- adding a second orchestrator;
- adding a second compaction system;
- adding a second memory system solely because another project has one;
- bulk installing Pi packages before identifying a concrete gap;
- upgrading Pi solely because 0.87.1 is newer.

## 7. Decision test for every future addition

Before adding a package/subsystem, answer:

1. What current deficiency does it close?
2. Can Pi/FAS already solve it?
3. What exact API/capability does it add?
4. What is the measurable context/token/runtime cost?
5. What focused test proves the benefit?
6. What regression test protects existing behavior?
7. Can it be removed cleanly?
8. Does it create a competing source of truth?

If the answers are weak, do not add it.
