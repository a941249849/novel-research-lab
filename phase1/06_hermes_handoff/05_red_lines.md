# Phase 1B-Core7 Red Lines

Hermes must obey these red lines:

1. Do not read `novel_training_set/` original full text files.
2. Do not generate original novel prose.
3. Do not expand plot.
4. Do not imitate source sentences.
5. Do not output reusable mechanism names that contain original proper nouns.
6. Do not overwrite Phase 1A stub JSON files.
7. Do not modify `phase0B/`.
8. Do not start all-18-book extraction.
9. Do not modify `system_master_spec_v0.1.md`.
10. Do not treat candidate outputs as final approved assets.

If a requested action conflicts with these red lines, Hermes must stop and report the conflict in `phase1/06_hermes_outputs/06_review/phase1B_core7_extraction_report.md`.
