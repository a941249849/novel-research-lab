# NRL Final Assets Independent Audit v0.16

## Role

Act as the independent literary-architecture reviewer for Novel Research Lab.
Review only the promoted final creation assets for `《借天改命账》`; do not
write or propose novel prose.

## Allowed Inputs

- `system/agent_ops/inbox/hermes-final-asset-bundle-v015.json`
- `system/creation_assets/project_assets.v0.2.json`
- `system/creation_assets/promotions/hermes_final_asset_bundle_v0.15.json`
- `phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md`
- `phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md`
- `system/creation_assets/schemas/*.schema.json`

Do not read `novel_training_set/` or any unlisted corpus material.

## Audit Questions

1. Do the nine final assets remain faithful to the approved Story Bible:
   mother lifespan debt, Poverty City mutual aid, protection-array pressure,
   embodied supernatural cost, and escalation potential?
2. Are the character, NPC, faction, artifact, technique, bond, foreshadowing,
   naming, and state ledger mutually coherent and original enough to support a
   bounded prose test without source-work mimicry?
3. Is any asset structurally incomplete, contradictory, too abstract, or
   likely to make the prose read as an audit/policy metaphor rather than
   Chinese fantasy?
4. Does the bundle need rework before a controlled prose test?

## Required Output

Return Markdown only, with exactly these headings:

```text
# Antigravity Final Assets Audit v0.16
## Verdict
## Strengths
## Blocking Issues
## Non-Blocking Improvements
## Controlled Prose Test Constraints
```

`## Verdict` must start with exactly one of `ACCEPT`, `ACCEPT_WITH_WARNINGS`,
or `REWORK_REQUIRED`. `REWORK_REQUIRED` is mandatory for a structural blocker.

## Hard Boundary

Do not generate a chapter, scene, dialogue, narration, or an asset rewrite.
