# NRL Production Chapter Runtime v0.20 Implementation Plan

1. Add tests for stage ordering, immutable accepted artifacts, source hashes,
   invalid state deltas, stale audits, and production readiness.
2. Add chapter runtime schemas and a single chapter registry under
   `system/production_runtime/`.
3. Implement read-only `production-readiness` and `chapter-runtime-status`.
4. Implement bounded artifact preparation and validation commands for intent,
   context, rule stack, trace, observation, audit, revision, and settlement.
5. Implement deterministic anti-AI prose metrics as audit evidence, not an
   automatic literary verdict.
6. Add Hermes writer/reviser and Antigravity auditor adapters behind v0.18 and
   v0.19 gates.
7. Surface the chapter lifecycle and blockers in Studio without adding another
   dashboard-only state source.
8. Run tests and a three-scene stress test before authorizing Chapter 1.
