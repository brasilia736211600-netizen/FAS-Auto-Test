# FAS Autopilot

FAS has a persistent autonomous controller for local or GitHub-first supervision.

## Mission mode

GitHub-first mode can execute one explicit mission before entering CI supervision:

```bash
python fas_autopilot.py \
  --github OWNER/REPO \
  --branch BRANCH \
  --objective-file missions/task.md \
  --scope path/to/relevant/code/ \
  --scope path/to/relevant/tests/ \
  --workflow "CI Workflow" \
  --test-cmd 'python -m pytest -q' \
  --max-attempts 3 \
  --poll-limit 60
```

Mission mode requires explicit `--scope` entries. The mission runs in a fresh disposable checkout, uses the existing OpenCode execution path, commits and pushes only within the declared scope, and then hands control to the normal CI recovery loop.

The mission file should define the objective, invariants, checkpoints, acceptance criteria and safety boundaries. FAS treats it as an execution contract, not as permission to bypass its safety controls.

## Control loop

`fas-autopilot` performs:

1. observe branch HEAD and its GitHub Actions run;
2. wait for CI completion when queued/in progress;
3. stop on non-actionable outcomes;
4. on failure, collect failed logs and workflow evidence;
5. derive a conservative recovery scope;
6. use bounded read-only model diagnosis when concrete scope is missing;
7. invoke OpenCode recovery;
8. run configured repository tests;
9. enforce scope before commit;
10. push the repair and watch the new commit;
11. after success, wait for the next HEAD when running without a cycle limit.

Mission mode adds an explicit objective before this loop. A mission failure is not converted into CI success.

## Safety

Autopilot does not reset, clean, force-push, delete unrelated work, or modify secrets. Recovery remains bounded by `max_attempts` and the existing scope guard. Mission execution also requires an explicit repository-relative scope and uses a disposable checkout.
