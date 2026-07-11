# NRL Production Release Hardening v0.21 Implementation Plan

1. Add failing tests for corpus drift and hierarchical evidence hash binding.
2. Re-attest corpus and bounded chunks on every v0.18 validation/promotion.
3. Add hash-bound, schema-valid v0.19 creation-asset reconciliation apply gate.
4. Add failing tests for chronology, revision re-audit, and observed state deltas.
5. Harden the chapter state machine and atomic persistence.
6. Complete 143 chunk analyses, 18 book syntheses, and cross-book distillation.
7. Run and apply the v0.19 project reconciliation under a bound Owner decision.
8. Run a serial multi-scene Hermes/Antigravity stress test without publishing.
9. Run the full Python suite, frontend build, Astryx doctor, system check,
   release readiness, and git integrity checks; then commit and push.
