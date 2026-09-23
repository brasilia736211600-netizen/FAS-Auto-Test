# FAS-Pi Roadmap

Updated: 2026-09-24

## Phase 0 — Baseline preservation
Status: COMPLETE

Pi 0.85.1 remains the proven production baseline for this proof cycle.
Initial full regression lineage: 324/324.
The lineage later expanded legitimately as tests were added.

## Phase 1 — Runtime proof closure
Status: COMPLETE

- Toolchain: Node 26.4.0, Pi 0.85.1, Linux, cgroup-v2.
- Leg 1: child FAS path live-proven.
- L6: all-candidates-fail/no-previous-model live-proven.
- Leg 2: Workflow -> child -> FAS -> real provider -> success live-proven.
- Full baseline reverified.

## Phase 2 — Evidence-backed architecture enhancement
Status: IMPLEMENTED WITH EXPLICIT RESIDUALS

### B — Child Result Contract
COMPLETE
Structured subagent result envelope and parent validation implemented.
351/351 after B.

### C — Role + Capability Mapping
COMPLETE WITH DEFERRED WIRING
Pure role-to-existing-constraint mapping for explorer, implementer, tester, reviewer, debugger.
396/396 after C.
Do not invent a role field merely to consume the helper.

### A — Pi Skills
COMPLETE
Two minimal declarative on-demand Skills.
No executable routing/fallback/thinking logic moved to Markdown.
440/440 after A/F combined lineage.

### F — Safety Gates
COMPLETE WITH RESIDUAL PLATFORM LIMITATION
Pre-spawn destructive Git and out-of-scope path gates plus credential-value redaction.
Pi 0.85.1 has no enforceable in-execution veto hook; preserve this limitation explicitly.
440/440 after F.

### E — Workflow Resume
COMPLETE FOR CURRENT MECHANISM
Resume-from-phase skips verified succeeded outputs and reruns the first non-success.
458/458 after E.
Cross-session/multi-process live proof remains UNKNOWN.

### D — Local Provider Discovery
PARTIAL
Discovery, capability validation, and unavailable path are tested.
469/469 after D.
Suitable-provider live proof is BLOCKED without a live daemon.
Registry admission remains conditional on a future evidence-backed boundary.

## Phase 2.5 — Autonomous completion program
Status: IN PROGRESS

This is the current main project phase.

1. State reconciliation.
2. Full source and file inventory.
3. Independent correctness audit.
4. Independent security audit.
5. TDD coverage-gap audit.
6. YAGNI/dead-code/duplication audit.
7. Token/context/thinking/fallback efficiency audit.
8. Subagents/Workflow/Autopilot/FAS integration audit.
9. Bootstrap/install/package audit.
10. Pi compatibility matrix.
11. Clean-room portability proof.
12. Final autonomous E2E coding/recovery proof.
13. Consolidation of only evidence-backed findings.
14. Final release/security/YAGNI audit.
15. Final handoff package.

## Phase 3 — Pi compatibility
Status: FUTURE / REQUIRED BEFORE ANY BASELINE MOVE

Compare Pi 0.85.1 with the current Pi release line.
Prove API and runtime parity, parent/child FAS seams, and /compose invariance.
Do not upgrade the production baseline merely because a newer version exists.

## Phase 4 — Long-horizon autonomy
Status: FUTURE / ONLY IF FINAL AUDIT JUSTIFIES IT

Goal:
goal -> plan -> execute -> verify -> bounded recover -> checkpoint -> resume -> complete

No hidden retries.
No second orchestrator.
No unbounded autonomous loops.

## Phase 5 — Final repository publication
Status: GATED

The current repository is the engineering/evidence repository.
The final repository is created only after technical completion and explicit user approval.

The operator must prepare:
- final source inventory;
- release manifest;
- README;
- installation/bootstrap;
- providers/fallbacks;
- tests/CI;
- security model;
- limitations;
- compatibility;
- migration procedure;
- proposed repository tree.

Then stop at FINAL-HANDOFF-READY: USER-APPROVAL-REQUIRED.

## Permanent phase rule

Never skip evidence -> smallest implementation -> focused regression -> full regression -> runtime proof -> state save.
