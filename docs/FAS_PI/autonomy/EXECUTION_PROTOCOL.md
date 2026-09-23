# FAS-Pi Autonomous Execution Protocol

Updated: 2026-09-24

## Start

Read the autonomy mandate, queue, finalization rules, all canonical docs/FAS_PI state files, and all reports relevant to current work. Then inspect current GitHub HEAD, branch, source, tests, and diff.

## Select work

Choose the highest-priority incomplete item with concrete evidence, bounded scope, and a test strategy. Never select work solely because it sounds useful.

## Per-item contract

ACCEPTANCE -> FAIL-FIRST -> SMALLEST FIX -> FOCUSED PASS -> FULL REGRESSION -> STATIC CHECKS -> DIFF REVIEW -> RUNTIME PROOF IF REQUIRED -> REPORT -> STATE UPDATE -> COMMIT -> PUSH -> REMOTE VERIFY

The regression count may increase when justified tests are added. Preserve lineage.

## Parallelism

Parallelize only independent read-only work or non-overlapping implementation boundaries after dependencies are satisfied. No concurrent writes to the same production file or shared state record.

## Failure classes

Use exact classes where applicable:
CREDENTIAL_MISSING, TOOLCHAIN_MISMATCH, PROVIDER_FAILURE, CHILD_BOOT_FAILURE, FAS_LOAD_FAILURE, WORKFLOW_FAILURE, TEST_FAILURE, SECURITY_FAILURE, SCOPE_VIOLATION, TELEMETRY_GAP, UNKNOWN.

Preserve evidence. Repair only actionable failures. Stop on unsafe ambiguity or unavailable required infrastructure.

## No-repeat

Before each change inspect state docs, queue, reports, Git history, current source, and tests. Reopen completed work only for regression, a new requirement, or stronger invalidating evidence.

## GitHub reporting

For runtime evidence:
gh codespace ssh -> execute/capture -> write docs/FAS_PI/reports/ -> inspect -> git diff --check -> update state -> git commit -> git push -> verify remote

Use gh for Codespace lifecycle/access and GitHub inspection. Use normal Git for commit/push. A verified Pi/GitHub extension can assist source-only operations but is never a second reporting authority.

## Interruption

Reconnect, read canonical state, inspect Git state/diff, locate the latest checkpoint/report, continue at the first incomplete item, and rerun only invalidated work. If a write may have partially occurred, inspect the diff first.

## Human intervention

Ask the user only for missing credentials, unsafe/ambiguous external action, unavailable external infrastructure, requirements that cannot safely be inferred, or final repository approval. Do not ask the user to repeat facts already stored in GitHub.

## Completion

Do not declare completion until all queue items are VERIFIED or explicitly BLOCKED/DEFERRED, state is consistent, regression is green, runtime limitations are explicit, final audit passes, and handoff artifacts exist.
