# 2026-09-24 — 43-Package Evaluation: What Joins Pi/FAS, What Leaves Pi

Method: npm registry metadata (exact versions, dependency counts) + full
readme reads for all 43. Zero installs, zero downloads beyond metadata.
Local Pi inventory audited from disk (extensions/skills/prompts/npm).
Ratings are /5 for FAS-project value, not general quality.

Local baseline: `~/.pi/extensions/` = code-state, compose, fas, fast-mode,
firecrawl-web.ts, image-gen, memory, pi-tool-display, side-chat, subagents,
ui, workflow; `~/.pi/agent/extensions/` = autopilot;
npm = opencode-pi, pi-free, pi-freeflow, pi-freerouter, pi-model-fallback,
pi-opencode-bridge; skills = fas-evidence-conventions, fas-routing-policy;
prompts = fas-status.md, fas-router-debug.md.

## Tier 1 — ADD (Termux-safe, direct FAS value)

- @juicesharp/rpiv-ask-user-question@2.11.0 (deps 2) — structured
  questionnaire with typed options + previews, works in RPC/ACP. USE: any
  turn that would otherwise guess (provider choice, handoff approval,
  destructive ops). WHEN: interactive sessions, approval gates. 5/5.
- @juicesharp/rpiv-todo@2.11.0 (deps 2) — todo overlay surviving
  /reload + compaction, blockedBy sequencing. USE: long autonomous runs.
  WHEN: always-on after eval; complements (never replaces) Git LIVE.md. 5/5.
- pi-prompt-template-model@0.12.3 (deps 1) — model/skill/thinking
  frontmatter; self-contained agent modes with auto-restore. USE: pin
  /fas-status to a cheap lane, /deep-analysis to a strong lane. WHEN:
  immediately after eval; upgrades our two templates. 5/5.
- pi-simplify@0.2.3 (deps 0) — /simplify reviews only git-changed lines,
  preserves behavior, runs tests. USE: pre-commit clarity pass. WHEN:
  after every source edit; complements Queue 7. 4/5.
- pi-powerline-footer@0.17.2 (deps 0) — status bar, editor stash (Alt+S),
  queue-during-compaction, vibes. USE: daily TUI. WHEN: always-on. 4/5.
- @moyai/pi-session-hoarder@0.2.0 (deps 2) — auto-archives sessions to
  content-addressed gzip + sidecars; /hoarder status/sync/prune. USE:
  crash insurance (our Termux crash is the receipt). WHEN: always-on;
  complements Git LIVE.md. 4/5.

## Tier 2 — EVALUATE on cloud, adopt at most one per row

- Subagents (pick ONE): pi-subagents@0.71.0 (deps 5, 455K/mo,
  extension+skill+prompt, council/parallel-review/fleet) vs
  @tintinweb/pi-subagents@0.19.0 (deps 4, fleet view, viewer, steering,
  scripted SubagentWorkflow). USE: parallel audits/reviews. WHEN: cloud
  eval incl. spawn-mechanism check (rpc vs systemd = Termux verdict).
  5/5 each; installing both = two subagent universes, forbidden.
- @quintinshaw/pi-dynamic-workflows@3.13.0 (deps 1) — 16-concurrent /
  1000-total fan-out, real model routing, token/cost accounting,
  journaled resume, verify/judgePanel/loopUntilDry. USE: codebase-wide
  audits; steal routing/accounting/resume schemas for FAS. WHEN: first
  eval; budgets mandatory on free lanes. 5/5.
- pi-background-tasks@2.6.5 (deps 1) — durable bg shell jobs, delegated
  inspect-only agents, 3-candidate Fusion + blind eval + merger. USE:
  long builds/tests without blocking. WHEN: cloud long-runs. 4/5.
- @gotgenes/pi-permission-system@33.1.1 (deps 3) — hides disallowed
  tools, bash wildcards, path rules, fail-closed, UI prompt events. USE:
  always-on safety base (auto-review plugs into it). WHEN: before any
  autonomous cloud run. 5/5.
- Memory (pick ONE): pi-memory@0.4.2 (deps 0, markdown + qmd search,
  most popular) vs pi-hermes-memory@0.9.9 (deps 3, categories, secret
  scan, FTS5, auto-consolidation, background learning). USE: durable
  facts. WHEN: after eval, loser deleted incl. local `memory` ext. 4/5
  vs 5/5.
- Goals (pick ONE): pi-goal-x@0.31.9 (deps 0, /goal + completion
  auditor, top-0.3%) vs pi-goal-list-loop-audit@0.38.98 (deps 0,
  mission control for hours/days, six-label recaps). USE: operator UX
  for long goals; steal auditor/recap patterns for Q8. WHEN: cloud
  eval. 4/5 each.
- @janvitos/pi-plan-build@0.1.114 (deps 0) — Plan/Build modes,
  explicit approval, clean-session option. USE: every non-trivial
  change. WHEN: after eval. 4/5.
- pi-advisor-flow@0.8.2 (deps 0) — executor/advisor second opinion,
  loop detection, model whitelist, privacy controls. USE:
  consequential decisions, pre-handoff review. WHEN: after eval. 4/5.
- @langfuse/pi-observability-plugin@0.1.2 (deps 5, experimental) —
  traces to Langfuse (turns, generations, tools, nested subagents). USE:
  router debugging + cost tracking. WHEN: cloud, needs Langfuse key.
  Pick Langfuse OR LangSmith, never both. 4/5.
- pi-provider-litellm@3.2.0 (deps 0) — LiteLLM proxy provider + model
  discovery. USE: only with a self-hosted proxy; candidate chassis for
  an omniroute endpoint. WHEN: conditional. 3/5 (4/5 with proxy).
- @llblab/pi-telegram@0.51.4 (deps 0) — Telegram DM as operator
  surface (queue, previews, files, controls). USE: supervise cloud runs
  from the phone. WHEN: needs bot token. 4/5.
- pi-lens@4.2.1 (deps 6) — LSP + linters + ast-grep/tree-sitter +
  review graph on every write. USE: verify/review phases. WHEN:
  cloud-only (LSP too heavy for the phone). 4/5 cloud, 2/5 Termux.

## Tier 3 — LATER / DEFER / REFERENCE (no install)

- LATER: @luan.sh/pi-xsettings (3/5, only when 5+ extensions need
  settings UI), pi-cache-optimizer (3/5, optimize after measuring).
- DEFER: pi-agent-browser-native (2/5 now — pinned to Pi 0.87.0, we
  run 0.85.1; 4/5 after migration; Firecrawl-replacement candidate).
- REFERENCE (steal ideas, never install): ponytail 3/5 (minimal-code
  discipline), bigpowers 3/5 (phase gates + cockpit), gentle-pi 3/5
  (review guardrails), @mjasnikovs/pi-task 3/5 (grill/critique gates;
  AGPL — do not install).

## Tier 4 — SKIP (never)

- @companion-ai/feynman 2/5 (separate CLI, 10 deps, not an extension).
- @plannotator/pi-extension 2/5 (browser UI unusable from Termux).
- context-mode 2/5 (MCP, unverifiable 98% claim, overlaps FAS compact).
- @akagilnc/pi-workflow-roles 2/5 (parallel role universe, competing CLI).
- @langchain/langsmith-pi-extension 3/5 (dup of Langfuse — pick one).
- confluence-cli 1/5 (enterprise wiki; our docs live in Git).
- @agentskit/doc-bridge 2/5 (19 deps, heaviest; no doc-site need).
- cc-safety-net 3/5 (second safety universe; permission-system covers it).
- @trim21/personal-pi-extensions 2/5 (bwrap has no Bionic support).
- pi-fabric 2/5 (15 deps, parallel universe + recursion quota risk).
- @luan.sh/pi-code-mode 2/5 (needs Rust toolchain on Termux).
- pi-cc-extensions 3/5 (third TUI stack; local ui + tool-display exist).
- pi-rtk-optimizer 2/5 (no rtk binary on phone or cloud).
- billion-context 2/5 (empty readme = opaque proxy-in-the-middle).
- @cgh567/agent 1/5 (49 deps, overwrites ~/.pi/agent, competing operator).

## What LEAVES local Pi (delete list, verify-then-delete order)

1. `firecrawl-web.ts` — backend proven failing; delete after a
   replacement (browser-native or evaluated web path) is green.
2. Bridge dup: exactly ONE of opencode-pi / pi-opencode-bridge survives
   (live probe decides); the other is deleted.
3. Free-provider dup: keep freeflow + at most one fallback
   (pi-free / pi-freerouter loser deleted after lane audit).
4. TUI dup: pi-tool-display vs ui vs side-chat consolidate to ONE stack
   (audit, then delete; powerline-footer joins the winner, not a fourth).
5. Local `memory` ext: deleted only when the hermes/pi-memory eval
   names its replacement.
6. fast-mode, code-state, image-gen, side-chat: audit-then-decide (no
   blind deletion; overlap with FAS thinking/budgets unproven).
7. NEVER deleted: fas, workflow, subagents, autopilot, compose, both
   FAS skills, both FAS prompt templates, pi-model-fallback (infra).

## Install order (cloud-first, phone follows)

1. Cloud eval: dynamic-workflows, subagents-duel, permission-system,
   memory-duel, goals-duel, plan-build, advisor-flow, background-tasks,
   prompt-template-model, simplify, hoarder, rpiv pair, powerline.
2. Promote Termux-safe winners to the phone (zero/low-dep set).
3. Credential-gated: Langfuse, Telegram, LiteLLM-proxy.
4. Post-0.87: browser-native re-score. Never: Tier 4.
