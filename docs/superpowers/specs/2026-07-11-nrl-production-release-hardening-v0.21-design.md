# NRL Production Release Hardening v0.21

## Purpose

Close the release blockers found by the independent architecture review before
any chapter prose is produced. v0.4 remains the canonical ten-layer design;
v0.21 hardens evidence and state transitions rather than adding another product
layer.

## Release Invariants

1. A saved deep-reading result is invalid if the protected corpus inventory,
   source hashes, byte ranges, or bounded chunk hashes drift.
   GB18030/GBK sources are decoded explicitly into UTF-8 reading copies while
   preserving and binding both the original byte hash and normalized copy hash.
2. Per-book syntheses bind the hashes of every chunk analysis; cross-book
   distillation binds the hashes of every per-book synthesis.
3. Reconciliation output cannot alter project assets directly. Full replacement
   candidates must preserve asset IDs/families, validate as one complete store,
   cite the verified cross-book distillation, and require a response-hash-bound
   Owner decision before atomic application.
4. Production readiness requires the applied reconciliation manifest to match
   the current project asset store.
5. Chapters are strictly sequential. Only accepted predecessor settlements can
   enter compiled context.
6. Draft audit and revision audit are separate gates. `REWORK_REQUIRED` never
   advances state.
7. Settlement deltas must match schema-valid observed facts and the accepted
   revision hash.
8. JSON state writes use atomic replacement. Agent empty responses are not
   persisted as evidence and quota failures remain resumable.

## Non-Goals

- No prose or chapter generation.
- No claim that 18 books are deeply read before 143/143 chunks, 18/18 book
  syntheses, and cross-book distillation validate.
- No direct reuse of source names, scenes, systems, wording, or author style.
- No new orchestration framework while the local state machine remains
  sufficient.

## Release Gate

Production remains blocked until v0.18, v0.19 application, schema validation,
two-pass chapter audit, and a multi-scene serial stress test all pass with fresh
evidence.
