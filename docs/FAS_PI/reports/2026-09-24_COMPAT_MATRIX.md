# 2026-09-24 — Pi 0.85.1 ↔ 0.87.1 Compatibility Matrix

Scope: Queue 4. Isolated 0.87.1 install (`~/pi-matrix/087`, global 0.85.1
untouched). No baseline move (mandate rule 17).

Labels: VERIFIED (fresh evidence) · BLOCKED (0.87 runtime proof).

## 1. Verdict: MATRIX COMPLETE — baseline stays 0.85.1; one concrete 0.87
blocker identified, adaptation deferred pending runtime proof

## 2. Evidence (VERIFIED)

- Used-symbol presence across 23 FAS-depended APIs (setModel, thinking levels,
  ctx.thinkingLevel, waitForIdle, sendUserMessage, registerTool/Command,
  getCommands, tool activation set, appendEntry, streamSimple, registry reads,
  session manager, trust/idle, event-stream factory, Skills loader/formatter):
  **23/23 present in both distributions** (counts equal or higher in 0.87.1).
- Boot + FAS extension load on 0.87.1: `pi --help` with `-e fas/index.ts`
  exits 0, no factory throw.
- Skills behavior on 0.87.1: both FAS Skills discovered, zero diagnostics,
  metadata-only prompt, body deferred (same as 0.85.1).
- pi-ai 0.85.1 → 0.87.1: `createAssistantMessageEventStream` present in both;
  `streamSimple` signature renamed `Context` → `TranscriptContext`.

## 3. Blocker: TranscriptContext drops `tools` (VERIFIED by type evidence)

- 0.85 `Context`: `{systemPrompt?, messages[], tools?[]}`.
- 0.87 `TranscriptContext`: `{messages[], brand}` — systemPrompt/tools folded
  into a leading system message by `normalizeContext`.
- Impact surface in FAS (only reader: `inferTask`): `messages` path intact
  (image detection works); `tools` path degrades — `toolCount` always 0 →
  complexity always `low` → `needsReasoning` never auto-set (silent routing
  change). Forwarding paths (`any`-typed) unaffected.
- Required adaptation (NOT implemented): defensive complexity inference that
  does not depend on `context.tools` — needs its own evidence + 0.87 runtime
  proof first. Baseline stays 0.85.1.

## 4. Residuals

- Full durable suite under 0.87: harness hardcodes 0.85.1 paths (needs
  parametrization work — small, future).
- 0.87 parent/child runtime parity turn: BLOCKED (needs credential).
- Matrix install retained at `~/pi-matrix/087` (local only, not in Git).
