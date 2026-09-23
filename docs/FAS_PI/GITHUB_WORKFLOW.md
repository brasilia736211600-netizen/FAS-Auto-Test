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

## Muse execution and report-persistence rule

**Default path: GitHub Codespace + normal Git.** Muse should generate runtime/audit reports inside the same Codespace checkout that produced the evidence, then persist them through the repository Git history.

Preferred sequence:

`gh codespace ssh -> run/verify -> write report under docs/FAS_PI/reports/ -> inspect report -> git status/diff -> git diff --check -> update state docs when required -> git commit -> git push -> verify remote tree/commit`

Use `gh` for Codespace lifecycle/access and GitHub inspection when supported; use normal `git` for file staging, commit, and push. `gh` itself is not the report persistence layer; the pushed Git commit is.

A previously verified Pi/GitHub extension may be used for GitHub file operations only when it preserves the same checked-out branch, commit history, report path, and verification chain. Do not use it as a parallel reporting authority, and do not generate runtime reports from a detached/local copy when the evidence was produced in Codespace.

For source-only/documentation audits, a verified GitHub extension can be acceptable; for runtime evidence, **Codespace-local report generation is the canonical path**.

## Report lifecycle

A report is created after the evidence is collected, not before. A BLOCKED/FAILED run still receives a report when the attempt materially changes project state or establishes a useful blocker.

For each milestone, prefer one coherent commit containing the report plus the corresponding state updates; never batch unrelated source changes merely to reduce commit count.

Before push, the agent must verify the report path, inspect the exact diff, and confirm no secrets or raw environment dumps are present. After push, verify the remote commit/path so the report is actually recoverable from GitHub.

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
