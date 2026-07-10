# Antigravity Review Request: NRL v0.8 Full-Corpus Proof Gate

You are reviewing Novel Research Lab from the shared local workspace.

## Context

Novel Research Lab is intended to run:

corpus reading -> single-book DNA -> cross-book mechanism distillation -> creation motherbase -> original novel generation.

Codex owns local runtime, engineering, validation, orchestration. Antigravity owns long-context literary review and independent structural critique. Hermes is paused and reserved for final writing/literary enrichment later.

## Current Problem

The latest v0.7 full-corpus output at:

`system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md`

passes the existing runtime command:

`python3 system/runtime/nrl.py antigravity-full-corpus-validate`

But local evidence shows it is only schema-valid, not depth-verified:

- `novel_training_set/` contains 18 `.txt` files totaling about 197,294,465 bytes.
- The full-corpus report is about 87,474 bytes / 1,733 lines.
- The report Manifest has 18 `book_reviews` and all nine asset families.
- The Manifest has no `reading_receipts`, no source file hashes, no source file sizes, no per-book chunk ledger, no early/middle/late/ending locator coverage, and no proof that each raw file was actually read.
- v0.7 validator checks headings, forbidden markers, JSON shape, and asset-family presence only.

This means the system accepted "format looks right" as "full-corpus reading completed".

## Files To Review

- `system/runtime/nrl_full_corpus_handoff.py`
- `tests/test_antigravity_full_corpus_v07.py`
- `system/agent_ops/full_corpus_job.v0.7.json`
- `system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md`
- `docs/superpowers/specs/2026-07-09-nrl-antigravity-full-corpus-handoff-v0.7-design.md`
- `docs/superpowers/specs/2026-07-09-nrl-architecture-reconciliation-v0.4-design.md`

Do not read or quote raw novel prose. If you need corpus facts, only use file names, byte sizes, hashes, and chunk counts.

## Questions

1. Is the root cause correctly described as a missing proof-of-work / proof-of-reading gate rather than a failure of the v0.4 architecture itself?
2. What should v0.8 add so Codex can safely distinguish:
   - `schema_valid_but_depth_unverified`
   - `proof_verified`
   - `promotable_research_asset`
3. Should full-corpus work be one giant report, or split into per-book/per-chunk Antigravity jobs with machine-verifiable receipts?
4. What exact receipt fields should be required?
5. What should remain forbidden until proof is verified?

## Required Output

Return a concise markdown report with:

- `## Root Cause`
- `## v0.8 Required Gate`
- `## Receipt Contract`
- `## Runtime Commands`
- `## Promotion Rule`
- `## Risks`

Do not write novel content, chapter plans, final character sheets, or Hermes instructions.
