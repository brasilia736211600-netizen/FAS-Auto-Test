# FAS Live E2E Recovery

This branch is an isolated disposable fixture for proving the real autonomous CI recovery loop.

The fixture intentionally contains a broken `add()` implementation in `e2e/live_fixture.py`. The workflow `.github/workflows/fas-e2e-live.yml` runs the focused fixture test.

## Termux procedure

Clone/check out this branch and ensure `gh` authentication and OpenCode are already configured in Termux.

```bash
fas init .
fas watch --repo . --test-cmd 'python -m pytest -q' --max-attempts 3 --poll-limit 60 --poll-seconds 5
```

Expected autonomous sequence:

```text
existing broken commit
 -> GitHub Actions FAIL
 -> fas watch identifies the failed run
 -> failure log saved under .fas/logs/
 -> OpenCode receives a recovery task
 -> smallest fix is made
 -> focused tests pass
 -> FAS commits
 -> FAS pushes without force
 -> HEAD changes
 -> fas watch observes the new CI run
 -> CI PASS
```

The disposable branch may be deleted after successful verification. Do not use the fixture as the production target.
