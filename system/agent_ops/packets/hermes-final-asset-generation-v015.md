# Hermes Final Asset Generation Packet v0.15

## Mission

Generate the first bounded, original final-asset bundle for `《借天改命账》`.
This is an asset-generation task, not a prose task. Do not write a chapter,
scene, dialogue, or narration.

## Authorized Scope

- `generate_final_creation_assets`
- `execute_hermes_final_asset_generation`
- `prepare_controlled_writing_test`

## Forbidden Scope

- `generate_novel_prose`
- `generate_full_chapter`
- `read_raw_novel_training_set`
- `bypass_asset_validation`

## Allowed Inputs

- `phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md`
- `phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md`
- `phase2C/03_codex_validation/phase2C_bible_validation_report.md`
- `phase2C/03_codex_validation/phase2C_antigravity_bible_review_report.md`
- `system/creation_assets/project_assets.v0.2.json`
- `system/creation_assets/schemas/common.schema.json`
- `system/creation_assets/schemas/*.schema.json`
- `system/research_assets/evidence_packs/manifest.v0.11.json`
- `system/research_index/creation_context_index.v0.12.json`

Do not read any other corpus, prior candidate project, or `novel_training_set/`
file.

## Required Output

Write exactly one JSON object to:

```text
system/agent_ops/inbox/hermes-final-asset-bundle-v015.json
```

The object must contain:

```json
{
  "version": "0.15",
  "project": "《借天改命账》",
  "assets": []
}
```

The `assets` array must contain exactly nine new schema-valid assets, one for
each family:

```text
characters
npcs
factions
artifacts
techniques
naming
emotional_bonds
foreshadowing
state_ledger
```

Use original, project-specific IDs and names. Set each asset to
`lifecycle_state: active`; retain the seed contracts already in the project
asset store rather than editing or deleting them. Add explicit cross-asset
references only when their targets are present in this same nine-asset bundle.

## Quality Constraints

- Every advantage must name a cost, visible physical backlash, exposure risk,
  or tracked consequence.
- Preserve the mother lifespan debt, Poverty City mutual aid, and the city
  protection array as active emotional and moral constraints.
- Make the life-ledger pressure supernatural and embodied. Never make the
  story world read as policy commentary, a spreadsheet, or a procedural audit.
- Preserve the Phase 2E pacing variation, sensory evidence, local-anchor, and
  anti-jargon requirements.
- Do not reuse source-work names, title patterns, iconic objects, rank
  sequences, factions, relationships, scenes, or causal chains.
- Do not use the forbidden naming terms in the project schemas.

## Completion Response

After writing the JSON file, return only its path and a one-line statement
that no prose was generated.
