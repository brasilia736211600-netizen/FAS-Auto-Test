# FAS Live E2E Recovery

This document records the completed disposable end-to-end proof of the autonomous FAS CI-recovery loop.

The disposable fixture is under `e2e/`. During the live proof, `e2e/live_fixture.py` intentionally returned subtraction instead of addition. FAS detected the GitHub Actions failure, persisted the failure evidence, constrained recovery to `e2e/`, delegated the repair to OpenCode, ran the focused E2E test, committed only the allowed change, pushed without force, and observed a successful GitHub Actions run.

## Termux procedure

Clone/check out the recovery branch and ensure `gh` authentication and OpenCode are configured in Termux.

Initialize FAS once:

```bash
python fas_cli.py init .
```

For this disposable recovery fixture, use the same focused test command as the workflow:

```bash
python fas_cli.py watch --repo . --test-cmd 'python -m pytest -q e2e/' --max-attempts 3 --poll-limit 60 --poll-seconds 5
```

The focused command is intentional. Using the full repository suite during recovery can block an otherwise correct fixture repair on unrelated failures.

## Proven sequence

```text
broken commit
 -> GitHub Actions FAIL
 -> FAS Watch identifies the failed run
 -> failure log saved under .fas/logs/
 -> recovery scope resolved to e2e/
 -> OpenCode receives a bounded recovery task
 -> smallest fix is made
 -> focused E2E test passes
 -> FAS commits only allowed paths
 -> FAS pushes without force
 -> GitHub Actions runs on the new SHA
 -> CI PASS
```

## Verified result

The live recovery produced commit `8727a27` with only the intended fixture file changed, and the subsequent `FAS E2E Live` workflow passed. The later CLI fixture-contract fix was committed as `fe14bc8`; the full FAS CI then passed with `74 passed`.

This branch/fixture is disposable proof infrastructure, not a production target. Keep the recovery mechanism; do not couple production projects to the fixture itself.
