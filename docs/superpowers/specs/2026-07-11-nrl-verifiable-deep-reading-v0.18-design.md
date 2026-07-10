# NRL Verifiable Deep Reading v0.18 Design

## Problem

The v0.8 full-corpus proof gate verifies source-file identity and four sampled
byte ranges. It does not prove continuous reading coverage. Calling that state
`proof_verified` overstated the evidence and allowed shallow per-book reports
to be promoted as if they represented full-text literary analysis.

## Decision

NRL v0.18 introduces a separate, resumable deep-reading pipeline. The old v0.8
artifact remains historical evidence of source access, but its effective status
is `access_sample_verified`, never `deep_read_verified`.

The new pipeline is:

```text
corpus inventory
  -> chapter-aware contiguous byte ranges
  -> Antigravity chunk analyses
  -> deterministic coverage and response validation
  -> per-book synthesis
  -> cross-book mechanism distillation
  -> project impact review
  -> Owner promotion gate
```

## Evidence Standard

Each source file is divided into non-overlapping contiguous chunks covering
every byte from zero to file size. A chunk record contains source SHA-256,
start/end byte offsets, chunk SHA-256, ordinal, and any detected chapter
headings. A valid Antigravity response must bind to those exact values and
provide structured observations for events, character/state transitions,
long-form mechanisms, continuity, style, creation-family evidence, and
originality risks.

`deep_read_verified` requires:

- 100% byte coverage for all 18 corpus files, with no gaps or overlaps.
- Every planned chunk has one schema-valid response with matching hashes.
- Every book has a synthesis referencing all of its validated chunks.
- Cross-book mechanisms identify source books and source chunk IDs.
- No raw corpus prose is copied into promoted research assets.
- Existing project assets are not silently rewritten; they require a separate
  impact review and promotion record.

## Runtime States

- `missing`: no v0.18 plan.
- `planned`: deterministic chunk plan exists.
- `in_progress`: some chunk responses validate.
- `chunk_coverage_verified`: every byte range and response validates.
- `book_synthesis_verified`: all per-book syntheses validate.
- `deep_read_verified`: cross-book distillation also validates.
- `blocked`: an execution or validation error requires intervention.

## Agent Boundaries

- Codex owns inventory, chunk planning, hashes, validation, orchestration,
  promotion, runtime integration, and project reconciliation.
- Antigravity reads bounded source chunks and performs literary analysis and
  independent synthesis.
- Hermes is excluded until deep reading, project impact review, and creation
  asset validation pass. It is used later for bounded prose stress tests.
- Owner authorization is required only for promotion into production research
  assets and prose scope changes, not for resumable research execution.

## Product Truthfulness

Studio and CLI must display the old v0.8 result as sampled access evidence.
They must not describe the corpus as fully or deeply read until v0.18 reaches
`deep_read_verified`. Existing architecture and asset validation may remain
healthy while corpus literary depth is explicitly incomplete.

## Non-Goals

- No imitation of source prose or source-specific style transfer.
- No raw corpus files or chunk text committed to Git.
- No automatic novel prose or full-chapter generation.
- No replacement of Story Bible or Volume 1 assets without an audited impact
  review.
