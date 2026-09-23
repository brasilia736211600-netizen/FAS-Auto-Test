# 2026-09-24 — A: Minimal Pi Skills IMPLEMENTED

Scope: Phase-2 item A ONLY (after B/C green). Progressive-disclosure Skills for
declarative FAS policy only. No executable routing/fallback/thinking math moved
into Markdown (test-locked). No packages.

Labels: VERIFIED (fresh evidence this run) · REPORTED · UNKNOWN.

## 1. Verdict: PASS — A implemented, 440/440 GREEN (suite incl. 24 A tests)

## 2. Key evidence finding (VERIFIED, reshaped the implementation)

FAS injects ZERO policy text into prompts today (`~/.pi/extensions/fas/index.ts`:
custom provider `fas-router/auto` + `streamSimple` only — read fully, no
registerTool/registerCommand/promptSnippet). So there were no always-on bytes to
remove. The honest A is avoided-future-cost: B/C follow-ups (role snippets,
evidence-convention references) are delivered as on-demand Skills instead of
prompt text. No FAS source file was modified for A.

## 3. Implementation (2 data files, zero source changes)

- `~/.pi/agent/skills/fas-evidence-conventions/SKILL.md` (1,626 B): B envelope
  shape, fence format, roles + required fields, validation rules.
- `~/.pi/agent/skills/fas-routing-policy/SKILL.md` (1,618 B): decision order,
  fallback bounds, thinking-budget summary (merged — a third thinking-only Skill
  was considered and rejected as non-minimal).
- Discovery: Pi user scope (`<agentDir>/skills`, VERIFIED in
  `dist/core/skills.js::loadSkills`). Third Skill rejected; drafts with
  executable markers rejected by test A4.

## 4. Test evidence (VERIFIED)

- Focused A suite **24/24** (`~/fas-verify/tests/test-fas-skills.mjs`,
  baseline FAIL first: skills dir absent): discovery of exactly the minimum set
  with zero diagnostics (A1); metadata-only prompt, body markers
  (`"files_modified"`, `consecutiveFailures`, `needsReasoning`) absent until read
  (A2); measured META 1,059 B vs BODY 3,244 B on a fixed load (A3 — always-on
  cost stays ~1 KB regardless of body growth); declarative-only guard (A4);
  valid names/descriptions (A5).
- One test corrected honestly during development (10x leverage bar was an
  invented threshold; replaced with the evidence-backed property
  body > metadata — behavior right, bar wrong).
- Full suite **440/440 GREEN** (396 prior + 24 A + 20 F), 0 failures.
- Upstream `bun:test` suites unrunnable on Termux (PLATFORM-LIMITED, untouched).

## 5. Token/cost statement (honest)

Static fixed-script measurement: +1,059 B (~265 tokens) always-on metadata for
both Skills; bodies (~3.2 KB) cost zero until the model reads one. Whether the
model reads a Skill per task is model behavior (UNKNOWN until a live A/B turn
count; NOT claimed as saved tokens). The structural win is VERIFIED: policy
growth no longer grows the prompt.

## 6. Diff proof

Zero modifications to any source file for A (extensions, Pi core, tests infra
untouched — fingerprints match pre-A values). New: 2 SKILL.md files (user scope)
+ 1 durable test file. `~/FAS`: this report + state edits, docs-only.
