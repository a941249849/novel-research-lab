# NRL Antigravity Full Corpus Handoff v0.7 Design

## Decision

NRL v0.7 adds a structured Antigravity full-corpus handoff and intake contract. The architecture is already frozen as the v0.4 ten-layer Corpus-to-Creation system; v0.7 does not redesign it. It makes the next external work batch usable by the runtime instead of becoming another prose report.

## Goal

Give the Owner a single command packet to paste into Antigravity, and give Codex a deterministic way to validate the returned full-corpus review before any asset production or Hermes writing begins.

## Non-Goals

- Do not call Antigravity directly from Codex.
- Do not call Hermes.
- Do not write novel prose, first chapters, outlines, scenes, or final creative assets.
- Do not quote or copy raw novel text into repo artifacts.
- Do not read `novel_training_set/` from the runtime path.
- Do not bypass the Phase 2E Owner Gate.

## Operating Model

Antigravity remains `manual_external_literary_review`. Codex prepares the task packet, validates output shape, checks boundaries, and records the job state. The Owner manually runs Antigravity against the shared local project folder and returns the result under `system/agent_ops/inbox/`.

## Data Contract

The v0.7 Antigravity output must include both:

- A Markdown review file for human reading.
- A JSON manifest block that Codex can validate.

The manifest must include:

- `job_id`: fixed as `job-v07-full-corpus-antigravity-review`.
- `contract_version`: fixed as `0.7`.
- `review_scope`: fixed as `full_remaining_corpus`.
- `architecture_version`: fixed as `0.4`.
- `corpus_policy`: confirms no raw prose is quoted in the returned artifact.
- `book_reviews`: per-book structured review entries.
- `cross_book_mechanisms`: mechanism candidates distilled across books.
- `asset_family_evidence`: coverage for the nine creation asset families.
- `originality_risks`: risks and mitigation notes.
- `recommended_next_ingestion`: safe next Codex action after validation.

## Required Human Sections

The Markdown review must include these exact headings:

- `## Job ID`
- `## Scope`
- `## Corpus Coverage`
- `## Cross-Book Mechanisms`
- `## Creation Asset Evidence`
- `## Originality Risk`
- `## Recommended Next Ingestion`
- `## JSON Manifest`

## Creation Asset Families

The nine families remain:

- `characters`
- `npcs`
- `factions`
- `artifacts`
- `techniques`
- `naming`
- `emotional_bonds`
- `foreshadowing`
- `state_ledger`

Every family must be represented in `asset_family_evidence`. Missing evidence is valid only if it is explicitly marked as `missing` with a reason.

## Validation Rules

Codex accepts the output only if:

- The expected job id is present.
- All required headings are present.
- The JSON manifest parses.
- The manifest version and architecture version match.
- All nine creation asset families are represented.
- There is at least one book review.
- There is at least one cross-book mechanism.
- The artifact does not contain forbidden raw-prose or content-generation markers.

Forbidden markers include:

- `novel_training_set/`
- `第一章`
- `正文`
- `Chapter 1`
- `Hermes 已执行`
- `最终正文`

## Runtime Interfaces

Add CLI commands:

```bash
python3 system/runtime/nrl.py antigravity-full-corpus-pack
python3 system/runtime/nrl.py antigravity-full-corpus-status
python3 system/runtime/nrl.py antigravity-full-corpus-ingest --file system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md
python3 system/runtime/nrl.py antigravity-full-corpus-validate
```

The pack command writes:

- `system/agent_ops/packets/job-v07-full-corpus-antigravity-review.md`
- `system/agent_ops/packets/job-v07-full-corpus-antigravity-command.md`

The command file is the Owner-facing Antigravity paste packet.

## Production Meaning

After v0.7, the Owner can safely start Antigravity full-corpus work. Codex can validate the returned output and then build subsequent family-specific producers. Hermes remains blocked until the research and creation-asset layers are sufficiently populated and explicitly authorized.

