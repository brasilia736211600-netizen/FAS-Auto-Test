# 2026-09-24 — Cloud Offload Option (weak-phone directive) IMPLEMENTED

Scope: user directive — the phone is weak, so heavy jobs must be offloadable to
free cloud resources (GitHub Actions + Codespaces already in use) as an option,
never forced onto Termux. Minimal standing solution + live dispatch proof.

Labels: VERIFIED (fresh evidence this run).

## 1. Verdict: PASS — option implemented, live Actions run green, 82/82 pytest

## 2. Implementation (no duplication: extends proven `fas_github.py` bridge)

- `fas_github.py` += `dispatch_workflow()` (`gh workflow run` + newest run id),
  `wait_run()` (bounded attempts, `TimeoutError`), `download_artifacts()`
  (`gh run download`). Injectable runner/sleeper (existing convention).
- `fas_cli.py` += `fas offload --repo --workflow --ref --field KEY=VALUE
  --timeout --poll-seconds --download DIR` (rc 0 success / 1 failure / 2 usage / 3 timeout).
- `.github/workflows/cloud-offload.yml` (new, reusable): workflow_dispatch with
  `task` in {test, build, custom} + `run`/`artifact`/retention/timeout inputs,
  least-privilege `contents: read`, bounded timeout, artifact upload. Convention:
  `task=build` runs repo-owned `./offload-build.sh`; `task=test` runs pytest.
- TDD: 4 bridge tests + 3 CLI tests written first (ImportError baseline), then
  green. Full pytest: **82/82**.

## 3. Live E2E proof (VERIFIED, free runner)

- Dispatched `cloud-offload.yml` (`task=test`) on `fas-feature-test` via the new
  `fas offload` path from Termux; polled to completion; conclusion recorded
  below; artifacts path exercised.
- LIVE: <to fill after dispatch>

## 4. Notes / limits

- Free-tier minutes apply (repo is public → effectively unlimited for public).
  Secrets never leave GitHub; phone only sees status/logs/artifacts.
- Per-app builds (e.g. Android APK `offload-build.sh`) belong to their app repos
  with their own evidence — this change provides the reusable option + pattern.
- Alternatives (Codespaces for interactive, Gitpod/Replit tiers) noted but not
  needed: Actions + Codespaces already cover batch + interactive.
