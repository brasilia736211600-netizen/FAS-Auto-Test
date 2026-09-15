# FAS Baseline

## Status

**COMPLETE — functional baseline verified.**

This document records the verified FAS-Auto-Test baseline on `fas-e2e-live`. It is a freeze point for the current functional scope, not a request for additional features.

## Verified baseline

- Repository: `brasilia736211600-netizen/FAS-Auto-Test`
- Branch: `fas-e2e-live`
- Baseline HEAD: `2974530ee4a8b912947df8027b6d727e04821c8d`
- Baseline commit: `fix: preserve directory recovery scope`
- Verified E2E workflow: `FAS E2E Live`
- Verified CI run: `34923903317`
- Verified job: `fixture`
- `Run full FAS suite`: **success**
- `Run live fixture`: **success**

## Functional contract proven

FAS has a verified autonomous recovery path covering:

```text
observe GitHub HEAD / CI
 -> detect actionable failure
 -> collect failed CI evidence
 -> derive bounded recovery scope
 -> diagnose when direct scope is insufficient
 -> invoke OpenCode repair
 -> run configured tests
 -> enforce scope before commit
 -> commit and push without force
 -> observe the new CI run
 -> recover again within the bounded attempt budget
 -> report the result
```

The live E2E fixture has demonstrated the critical recovery transition from a deliberately failing state to a passing state. The recovery scope regression was also repaired while retaining the external-path containment guard.

## Safety boundary

The verified controller remains bounded by recovery attempts and scope enforcement. It does not reset, clean, force-push, delete unrelated work, or modify secrets.

GitHub-first supervision uses disposable remote checkouts and can supervise a target branch without using the user's WebLibre checkout.

## Scope decision

Freeze the current FAS functional surface as the baseline. Do not add new capabilities merely to extend the baseline. Future changes should start as a separate requirement and must preserve this verified contract.

## Next intended use

Use this baseline FAS instance to supervise a real target repository/branch. The disposable `fas-e2e-live` fixture remains a verification harness and is not itself the production target.
