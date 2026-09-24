# 2026-09-24 — Extension-Lane Visibility (freeflow/… in the live pool)

Status: NO SOURCE CHANGE NEEDED + D8 SHIPPED. Live proof that
extension-registered lanes route: bare-parent PARENT-OK on the cline
streak; freeflow direct K1-OK/K2-OK and CLOUD-K-OK. Full regression
516/516 node + 84/84 pytest.

## 1. Question (from the /model observation)

`/model` lists 33 freeflow lanes; `models-store.json` has only 6
providers and no freeflow key. Are extension lanes actually in the
pool FAS ranks — or is the router blind to them?

## 2. Answer (code-read + measured rank dump)

FAS ranks `modelRegistry.getAll()` (live, all extensions), never
`models-store.json` (a diagnostics snapshot). Measured on Termux:
pool 832 = registry lanes. The store gap is cosmetic: freeflow lanes
receive no KB history simply because the bare-parent runs served cline
lanes (168/44/8 historic successes outrank everything). Direct probes
prove the lanes work: K1-OK/K2-OK locally, CLOUD-K-OK on the codespace.

## 3. Booking rule for the multi-provider set

Kinds that persist auth (cline OAuth, zai/fhrouter keys,
`OPENROUTER_API_KEY`) travel with the user and appear on any machine.
Kinds that inherit the host (freeflow shared-IP quota, opencode-cli
TUI gate, `/freeflow cline login` browser pool) are host-local:
Termux-freeflow working says nothing about cloud-freeflow, and
cloud-freeflow 429 says nothing about Termux. Book per (lane, host).
omniroute rechecked today: same 114-byte lander, still PARKED.

## 4. D8 (this turn's test, discovery suite 65/65)

Pins: extension-shaped lanes (`freeflow/kilo-auto/free`) survive rank,
a served one outranks unproven lanes, and failure evidence +
provider rollup record under the lane's own key. No production change
was required — the seam already handles unknown-provider lanes
correctly; now that is locked by test instead of assumed.

## 5. Live turns this session

T1 `freeflow/kilo-auto/free` → K1-OK (pre-change baseline);
T2 bare-parent `fas-router/auto` → PARENT-OK (cline streak ×3,
`providers: {cline: consec 0}`). No source touched between them
except the test file.

## Fingerprints (unchanged — test-only change)

core `155ae074`, index `73239dde`, roles `8395d510`, runner `c20f921d`,
schema `f95a471c`; discovery suite 65/65 (D8 new).
