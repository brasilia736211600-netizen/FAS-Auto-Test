# FAS-Pi GitHub Workflow

Updated: 2026-09-24

## Purpose

GitHub is the durable source of truth for the Pi/FAS project state, reports, code changes, tests, and recovery evidence.

## Canonical layout

```text
docs/FAS_PI/
  README.md
  MASTER_PROJECT_MAP.md
  WORKFLOW_STATE.md
  ROADMAP.md
  RESUME.md
  RESEARCH_AND_DECISIONS_*.md
  GITHUB_WORKFLOW.md
  reports/
    README.md
    dated reports and runtime evidence
```

Do not create dated reports directly under `docs/FAS_PI/`.

## Muse execution rule

Muse may create/update reports from the same GitHub Codespace/runtime used for the work. This is preferred for runtime evidence because the report is generated beside the exact source, tests, logs, process evidence, and branch state being validated.

Preferred persistence path:

`Codespace -> write report -> inspect report -> git diff -> git commit -> git push`

Use `gh` for Codespace/GitHub operations when it is the supported mechanism in that environment; use normal `git` for add/commit/push. Never rely on a separate local copy of a report.

A Pi/GitHub extension may be used only when it already participates in the established project workflow and has been verified not to bypass the Codespace/source-of-truth path. It must not create a second reporting authority.

## Report policy

Every runtime or audit report must:

1. live under `docs/FAS_PI/reports/`;
2. have a date and descriptive subject in its filename;
3. state the exact scope;
4. distinguish VERIFIED/HISTORICAL/REPORTED/UNKNOWN/BLOCKED;
5. cite source paths, test names, commits, and runtime evidence when available;
6. never contain secrets or raw secret-bearing environment output;
7. preserve failures and blockers rather than rewriting them away;
8. record cleanup status and final Git status when relevant.

## State update policy

After a milestone changes project state, update in the same change set where practical:

- `WORKFLOW_STATE.md`;
- `MASTER_PROJECT_MAP.md`;
- `RESUME.md`;
- `ROADMAP.md` when status/order changes;
- the corresponding dated report under `reports/`.

## Resume protocol

A new agent must read the canonical FAS-Pi context before acting. Chat history is not completion proof.

For every material claim:

`claim -> GitHub source -> focused test -> runtime proof when required -> report -> state update`

## No-speculation rule

Do not add packages, architecture, providers, routers, orchestrators, or features because another project has them. First identify a concrete current deficiency, then prove the smallest useful change.

## Current execution baseline

Current Pi baseline: `0.85.1`.

Current FAS model contract: `fas-router/auto`.

Current full-suite baseline: `324/324 GREEN`.

Leg 1, L6, and Leg 2 are closed. Phase 2 follows the evidence audit order recorded in `reports/PHASE2_EVIDENCE_AUDIT_2026-09-23.md`.
