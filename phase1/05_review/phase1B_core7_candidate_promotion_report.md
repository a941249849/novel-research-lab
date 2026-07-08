# Phase 1B-Core7 Candidate Promotion Report

## 1. Task Metadata

- phase: Phase 1B-Core7
- task_name: Candidate Promotion
- promoted_at: 2026-07-08 04:19:14 CST
- executor: Codex
- project_root: `/Users/liuneng/Documents/Novel Research Lab`
- status: pass

## 2. Promotion Preconditions

Promotion was executed after the following approvals were stated:

- Hermes Core7 candidate extraction: complete
- Codex validation report: PASS
- Antigravity content review: PASS
- Owner Review: APPROVE CANDIDATE PROMOTION

## 3. Promotion Input Sources

Candidate source directories:

- `phase1/06_hermes_outputs/01_book_dna_candidates/`
- `phase1/06_hermes_outputs/02_narrative_dna_candidates/`
- `phase1/06_hermes_outputs/03_state_ledger_candidates/`
- `phase1/06_hermes_outputs/04_mechanism_candidates/`
- `phase1/06_hermes_outputs/05_cross_book_notes/cross_book_feature_notes.md`

Validation source:

- `phase1/06_hermes_outputs/06_review/phase1B_core7_codex_validation_report.md`

## 4. Phase 1A Stub Archive

Archive root:

- `phase1/00_archive/phase1A_stubs/`

Archived paths:

- `phase1/02_book_dna/` -> `phase1/00_archive/phase1A_stubs/02_book_dna/`
- `phase1/02_narrative_dna/` -> `phase1/00_archive/phase1A_stubs/02_narrative_dna/`
- `phase1/02_state_ledgers/` -> `phase1/00_archive/phase1A_stubs/02_state_ledgers/`

Archive file counts:

- archived BookDNA stubs: `18`
- archived NarrativeDNA stubs: `18`
- archived StateLedger stubs: `18`

## 5. Promoted Core7 Assets

Core7 books:

- 遮天
- 蛊真人
- 人道至尊
- 凡人修仙传
- 斗破苍穹
- 诡秘之主
- 求魔

Promoted JSON assets:

| Book | BookDNA target | NarrativeDNA target | StateLedger target |
| --- | --- | --- | --- |
| 遮天 | `phase1/02_book_dna/遮天_dna.json` | `phase1/02_narrative_dna/遮天_narrative.json` | `phase1/02_state_ledgers/遮天_ledger.json` |
| 蛊真人 | `phase1/02_book_dna/蛊真人_dna.json` | `phase1/02_narrative_dna/蛊真人_narrative.json` | `phase1/02_state_ledgers/蛊真人_ledger.json` |
| 人道至尊 | `phase1/02_book_dna/人道至尊_dna.json` | `phase1/02_narrative_dna/人道至尊_narrative.json` | `phase1/02_state_ledgers/人道至尊_ledger.json` |
| 凡人修仙传 | `phase1/02_book_dna/凡人修仙传_dna.json` | `phase1/02_narrative_dna/凡人修仙传_narrative.json` | `phase1/02_state_ledgers/凡人修仙传_ledger.json` |
| 斗破苍穹 | `phase1/02_book_dna/斗破苍穹_dna.json` | `phase1/02_narrative_dna/斗破苍穹_narrative.json` | `phase1/02_state_ledgers/斗破苍穹_ledger.json` |
| 诡秘之主 | `phase1/02_book_dna/诡秘之主_dna.json` | `phase1/02_narrative_dna/诡秘之主_narrative.json` | `phase1/02_state_ledgers/诡秘之主_ledger.json` |
| 求魔 | `phase1/02_book_dna/求魔_dna.json` | `phase1/02_narrative_dna/求魔_narrative.json` | `phase1/02_state_ledgers/求魔_ledger.json` |

Promoted mechanism notes:

- `phase1/04_mechanism_library/core7_notes/遮天_mechanism_notes.md`
- `phase1/04_mechanism_library/core7_notes/蛊真人_mechanism_notes.md`
- `phase1/04_mechanism_library/core7_notes/人道至尊_mechanism_notes.md`
- `phase1/04_mechanism_library/core7_notes/凡人修仙传_mechanism_notes.md`
- `phase1/04_mechanism_library/core7_notes/斗破苍穹_mechanism_notes.md`
- `phase1/04_mechanism_library/core7_notes/诡秘之主_mechanism_notes.md`
- `phase1/04_mechanism_library/core7_notes/求魔_mechanism_notes.md`

Promoted cross-book feature notes:

- `phase1/03_features/cross_book_feature_notes.md`

## 6. Overwrite Status

Intentional overwrites occurred only for the seven Core7 files in each existing formal JSON directory:

- `phase1/02_book_dna/{book_name}_dna.json`
- `phase1/02_narrative_dna/{book_name}_narrative.json`
- `phase1/02_state_ledgers/{book_name}_ledger.json`

These overwrites are reversible because all pre-promotion Phase 1A stub files were copied to `phase1/00_archive/phase1A_stubs/` before promotion.

No deletion was performed on:

- `phase1/06_hermes_outputs/`
- `phase0B/`
- `novel_training_set/`

## 7. Promotion Integrity Checks

Hash comparison results:

- BookDNA promoted files match source candidates: `7 / 7`
- NarrativeDNA promoted files match source candidates: `7 / 7`
- StateLedger promoted files match source candidates: `7 / 7`
- Mechanism notes promoted files match source candidates: `7 / 7`
- Cross-book feature notes match source candidate: `1 / 1`

Hermes outputs retained:

- `phase1/06_hermes_outputs/` remains present.
- Candidate and review files remain available for audit.

## 8. Schema Validation Result

Schema validation command:

```bash
python3 scripts/validate_schemas_draft7.py --validate-phase1-stubs --report phase1/05_review/phase1B_core7_promotion_schema_validation_report.md
```

Result:

- return code: `0`
- status: `pass`
- schema report: `phase1/05_review/phase1B_core7_promotion_schema_validation_report.md`
- Draft-07 schema files checked: `5 / 5` pass
- formal BookDNA JSON instances checked: `18 / 18` pass
- formal NarrativeDNA JSON instances checked: `18 / 18` pass
- formal StateLedger JSON instances checked: `18 / 18` pass
- total formal JSON instances checked: `54 / 54` pass

## 9. Rollback Plan

Rollback is available from:

- `phase1/00_archive/phase1A_stubs/02_book_dna/`
- `phase1/00_archive/phase1A_stubs/02_narrative_dna/`
- `phase1/00_archive/phase1A_stubs/02_state_ledgers/`

Rollback method:

1. Copy archived JSON files from the archive directories back into their corresponding formal directories.
2. Re-run:

```bash
python3 scripts/validate_schemas_draft7.py --validate-phase1-stubs --report phase1/05_review/rollback_schema_validation_report.md
```

Rollback does not require deleting Hermes outputs.

## 10. Commands Run

| Command | Return Code | Summary |
| --- | ---: | --- |
| `mkdir -p phase1/00_archive/phase1A_stubs/... phase1/04_mechanism_library/core7_notes phase1/03_features` | 0 | Created archive and promotion target directories. |
| `cp -p phase1/02_book_dna/*.json phase1/00_archive/phase1A_stubs/02_book_dna/` | 0 | Archived 18 BookDNA stubs. |
| `cp -p phase1/02_narrative_dna/*.json phase1/00_archive/phase1A_stubs/02_narrative_dna/` | 0 | Archived 18 NarrativeDNA stubs. |
| `cp -p phase1/02_state_ledgers/*.json phase1/00_archive/phase1A_stubs/02_state_ledgers/` | 0 | Archived 18 StateLedger stubs. |
| Core7 copy loop | 0 | Promoted 21 JSON files and 7 mechanism notes. |
| `cp -p phase1/06_hermes_outputs/05_cross_book_notes/cross_book_feature_notes.md phase1/03_features/cross_book_feature_notes.md` | 0 | Promoted cross-book notes. |
| `python3 scripts/validate_schemas_draft7.py --validate-phase1-stubs --report phase1/05_review/phase1B_core7_promotion_schema_validation_report.md` | 0 | Schema validation passed. |
| Hash/integrity check script | 0 | Confirmed promoted files match source candidates. |

## 11. Next Step Recommendation

Proceed to Phase 1B post-promotion review / Phase 1B closeout.

Do not start 18-book full extraction until Owner explicitly authorizes the next phase.
