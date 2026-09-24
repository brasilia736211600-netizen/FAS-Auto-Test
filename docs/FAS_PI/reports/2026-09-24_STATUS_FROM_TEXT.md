# 2026-09-24 — Status-from-Text Advisory Parsing (F3 follow-up 1/3)

Status: SHIPPED (core `f7c52161`→`ac88fe44`, T18, release 86/86, full
regression 504/504 node + 84/84 pytest). Live: PARENT-OK, clean 3/3
cline SERVED streak — KB learning converged, dead lanes avoided by rank.

## 1. Gap

Providers THROW text (`402: {...}`, `404: {...}`) with no status object,
so classification collapsed to `execution:unknown` and learning evidence
could not distinguish credit-death from 404s. But promoting text codes to
hard statuses would REGRESS the breaker: lane-scoped 402/404 must NOT
stop the turn (PARENT-OK lived through exactly that sequence).

## 2. Fix (advisory, colon rule)

`classifyFailure`: a LEADING `^\d{3}\s*:` upgrades the reason
(`credits:402`, `execution:404`, `auth:401`) while forcing
retryable/non-fatal — the breaker, not the classifier, decides the
turn. Bare prose without colon (`401 Unauthorized`) stays conservative;
numeric status events keep hard semantics (T15 pins untouched).

## 3. TDD

- T18 (`test-fas-release.mjs`): FAIL-first 84/86 (the two reason
  asserts) → 86/86 after. Pins: text-402/404 retryable, bare-401
  non-fatal, numeric-401 fatal.
- Pre-change audit: no existing test uses leading-code-colon text;
  numeric paths unaffected.
- Full regression: 504/504 node (18 files) + 84/84 pytest, zero
  failures. `node --check` clean.

## 4. Live effect

Bare-parent probe → PARENT-OK with zero fallback: three straight
cline/gemma SERVED turns. Previous run needed the breaker path;
this run shows rank-level avoidance working (proper reasons feeding
penalties via F1 fields).

## 5. Remaining F3 queue (not started)

Cross-turn cooldown for consec-1 re-burn; persistent provider-level
breaker (needs clock + design). Then: 0.87 migration checklist, cloud
shortlist eval + Q6-overflow.

## Fingerprints

core `ac88fe44`, roles `8395d510`, runner `c20f921d`, schema `f95a471c`,
fas index `669fdeb7`, compose `59a2b7e5`, tool-list `8426bc05`.
