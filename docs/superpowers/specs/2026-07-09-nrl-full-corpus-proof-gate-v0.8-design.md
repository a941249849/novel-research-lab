# NRL Full-Corpus Proof Gate v0.8 Design

## Purpose

v0.7 proved that a formatted Antigravity full-corpus report can pass schema checks without proving that the 18 source novels were actually read. v0.8 adds a read-proof gate between `schema_valid` and `promotable_research_asset`.

## Root Cause

The v0.4 architecture remains valid. The failure is in the execution contract: `antigravity-full-corpus-validate` checks headings, forbidden markers, JSON shape, and asset-family coverage, but it does not require machine-verifiable reading receipts.

## States

- `schema_valid_but_depth_unverified`: report shape may be valid, but no complete reading receipts were verified.
- `proof_verified`: every corpus file has a receipt with matching file size, file SHA-256, and early/middle/late/ending byte-range chunk hashes.
- `promotable_research_asset`: future state; requires `proof_verified` plus explicit Owner approval.

## Receipt Contract

Each receipt must include:

- `book_title`
- `source_file`
- `source_file_size_bytes`
- `source_file_sha256`
- `read_scope: full_text_reviewed`
- `segments`

Each segment must include:

- `chunk_id`
- `phase`: one of `early`, `middle`, `late`, `ending`
- `start_byte`
- `end_byte`
- `chunk_sha256`

The verifier does not store or require raw prose snippets.

## Runtime Commands

- `python3 system/runtime/nrl.py full-corpus-proof-status`
- `python3 system/runtime/nrl.py full-corpus-proof-pack --all`
- `python3 system/runtime/nrl.py full-corpus-proof-validate --file <path>`

## Guardrails

- Do not promote v0.7 output to research assets without v0.8 proof verification.
- Do not generate novel prose, chapter plans, final character sheets, naming dictionaries, or technique trees.
- Do not call Hermes.
- Antigravity may be called through the CLI bridge for bounded per-book proof tasks.
