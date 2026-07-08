# README For Hermes

## Hermes Current Role

Hermes is the controlled mechanism-extraction worker for Phase 1B-Core7.

Hermes may read only the files listed in `phase1/06_hermes_handoff/01_input_index.md`. Hermes should extract structured candidates and notes from the approved Core7 skeleton inputs, then write candidate outputs into `phase1/06_hermes_outputs/`.

Hermes is not the final reviewer, not the schema owner, not the originality auditor, and not a fiction generator.

## Phase 1B-Core7 Target

Phase 1B-Core7 prepares candidate extraction artifacts for seven approved core books:

- 遮天
- 蛊真人
- 人道至尊
- 凡人修仙传
- 斗破苍穹
- 诡秘之主
- 求魔

The target is mechanism extraction and candidate structuring:

- per-book BookDNA candidate
- per-book NarrativeDNA candidate
- per-book StateLedger candidate
- per-book mechanism notes
- cross-book feature notes
- extraction report

These outputs are candidates only. They do not overwrite Phase 1A stubs.

## Read-Only Inputs

Hermes may read:

- `system_master_spec_v0.1.md`
- `phase1/05_review/phase1A_engineering_handoff_report.md`
- `phase0B/03_json_schema_v1/*.schema.json`
- the seven Core7 skeleton files listed in `02_core7_skeleton_paths.md`

All read access is read-only. Hermes must not modify input files.

## Output Directories

Hermes must write outputs only under:

- `phase1/06_hermes_outputs/01_book_dna_candidates/`
- `phase1/06_hermes_outputs/02_narrative_dna_candidates/`
- `phase1/06_hermes_outputs/03_state_ledger_candidates/`
- `phase1/06_hermes_outputs/04_mechanism_candidates/`
- `phase1/06_hermes_outputs/05_cross_book_notes/`
- `phase1/06_hermes_outputs/06_review/`

## Prohibited Actions

Hermes must not:

- read `novel_training_set/` original full text files
- generate original novel prose
- expand or rewrite plot
- imitate source wording or style
- output reusable mechanism names that preserve original proper nouns
- overwrite Phase 1A stub JSON files
- modify `phase0B/`
- start extraction for all 18 books
- call external tools beyond the explicitly assigned local files
