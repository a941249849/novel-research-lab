# Phase 1B-Core7 Hermes Output Contract

Hermes must produce candidate outputs only. Candidate files are not final project assets until reviewed.

## Per-Book Outputs

For each Core7 book, Hermes must create:

1. BookDNA candidate
   - Directory: `phase1/06_hermes_outputs/01_book_dna_candidates/`
   - Filename: `{book_name}_book_dna_candidate.json`
   - Must conform as closely as possible to `phase0B/03_json_schema_v1/book_dna.schema.json`

2. NarrativeDNA candidate
   - Directory: `phase1/06_hermes_outputs/02_narrative_dna_candidates/`
   - Filename: `{book_name}_narrative_dna_candidate.json`
   - Must conform as closely as possible to `phase0B/03_json_schema_v1/narrative_dna.schema.json`

3. StateLedger candidate
   - Directory: `phase1/06_hermes_outputs/03_state_ledger_candidates/`
   - Filename: `{book_name}_state_ledger_candidate.json`
   - Must conform as closely as possible to `phase0B/03_json_schema_v1/state_ledger.schema.json`

4. Mechanism notes
   - Directory: `phase1/06_hermes_outputs/04_mechanism_candidates/`
   - Filename: `{book_name}_mechanism_notes.md`
   - Must describe abstract mechanisms, not reusable source-specific names.

## Cross-Book Outputs

Hermes must create:

1. Cross-book feature notes
   - Path: `phase1/06_hermes_outputs/05_cross_book_notes/cross_book_feature_notes.md`
   - Purpose: compare recurring abstract mechanisms across the seven Core7 skeletons.

2. Extraction report
   - Path: `phase1/06_hermes_outputs/06_review/phase1B_core7_extraction_report.md`
   - Purpose: summarize inputs read, outputs written, validation status, uncertainty, and red-line compliance.

## Output Rules

- Do not overwrite any file under `phase1/02_book_dna/`, `phase1/02_narrative_dna/`, or `phase1/02_state_ledgers/`.
- Do not modify any file under `phase0B/`.
- JSON candidates should be UTF-8 encoded and pretty-printed.
- Markdown notes should avoid quoting source prose. Prefer paraphrase and abstraction.
- If evidence is insufficient from skeleton slices, mark the field as `TBD` or document uncertainty in the review report.
