# FAS Autopilot

FAS now has a persistent autonomous controller for a local checkout.

## Control loop

`fas-autopilot` repeatedly performs:

1. observe the current `HEAD` and its GitHub Actions run;
2. wait for CI completion when queued/in progress;
3. stop immediately on non-actionable outcomes;
4. on failure, collect failed logs and workflow evidence;
5. derive a conservative recovery scope;
6. use the bounded read-only model diagnosis when concrete scope is missing;
7. invoke the existing OpenCode recovery path;
8. run configured repository tests;
9. enforce the recovery scope before commit;
10. push the repair and watch the new commit;
11. after success, wait for the next `HEAD` instead of exiting.

The controller stops on a safety boundary such as unknown scope, scope violation, push failure, repair failure, or exhausted recovery budget.

## Termux usage

After installing FAS from the repository:

```bash
fas-autopilot /path/to/WebLibre
```

Useful bounded verification:

```bash
fas-autopilot /path/to/WebLibre --max-cycles 1
```

The controller is intentionally local because the recovery path requires the local checkout, OpenCode, model credentials, and the existing scoped git safety controls. GitHub remains the CI source of truth.

## Safety

Autopilot does not reset, clean, force-push, delete unrelated work, or modify secrets. Autonomous recovery remains bounded by `max_attempts` and the existing scope guard.
