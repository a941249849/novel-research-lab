# Creation Asset Registry v0.1 Design Spec

## Baseline

`Novel Research Lab Studio v0.1` made the product shape visible and exposed the next structural gap: long-form creation assets are not yet an operating system. The next step is not Phase 2F and not prose production. It is a read-only infrastructure layer that turns the Creation Coverage Matrix into inspectable, validated asset registries.

## Goal

Build `Creation Asset Registry v0.1` so Novel Research Lab can track long-form creative asset readiness without advancing content. The registry must make each coverage gap actionable: what asset family exists, what status it has, why it is not complete, which source artifacts support the assessment, and what the next safe system action is.

## Hard Non-Goals

- Do not progress to Phase 2F.
- Do not write novel prose.
- Do not write chapter plans as content deliverables.
- Do not generate full character cards.
- Do not create final NPC sheets, faction dossiers, technique trees, naming dictionaries, or item catalogs as creative content.
- Do not call Hermes.
- Do not call Antigravity.
- Do not read raw `novel_training_set/` files.
- Do not replace `current_phase_state.json` or `mission_registry.json`.
- Do not mark any long-form asset family `complete` in v0.1.

## Asset Families

The registry must cover the same nine long-form asset families exposed in Studio:

1. Characters
2. NPCs
3. Factions
4. Artifacts
5. Techniques
6. Naming
7. Emotional Bonds
8. Foreshadowing
9. State Ledger

Each family must include:

- `asset_id`
- `label`
- `status`: one of `missing`, `seed`, `partial`
- `readiness_score`: integer 0-100
- `why_not_complete`
- `known_support`
- `missing_capabilities`
- `source_artifacts`
- `next_safe_action`
- `blocked_actions`

## Runtime Contract

Add a read-only runtime command:

```bash
python3 system/runtime/nrl.py creation-assets
```

It must return one JSON object with:

- `registry_name`
- `version`
- `project`
- `mode`
- `source_of_truth`
- `asset_families`
- `coverage_summary`
- `guardrails`
- `next_safe_action`

The command must be deterministic and read-only. It may derive state from current runtime files and a registry JSON artifact, but it must not mutate state.

## Registry Artifact

Create a focused registry artifact:

```text
system/creation_assets/creation_asset_registry.v0.1.json
```

This artifact is system metadata, not creative generation. It records coverage readiness and missing capabilities, not final content.

## Studio Integration

Studio must expose Creation Asset Registry drill-down under the Creation Coverage Matrix:

- summary counts by status
- per-family readiness score
- known support
- missing capabilities
- source artifacts
- next safe action
- blocked actions

Studio still remains read-only and must not provide mutation controls.

## Guardrails

- Owner Gate remains active and content progression remains frozen.
- `advance` must still stop at Owner Gate.
- No stale Owner Gate decision may be reused.
- No generated novel content or chapter planning artifacts.
- No raw corpus reads.
- `complete` is forbidden for all registry asset families in v0.1.

## Acceptance Checks

- `python3 system/runtime/nrl.py creation-assets` returns all nine asset families.
- No family has status `complete`.
- Coverage summary counts match the family list.
- Studio data includes the asset registry drill-down.
- Built Studio contains `Creation Asset Registry`, `Characters`, `NPCs`, `Techniques`, `Naming`, and `No family is complete in v0.1`.
- `system-status` still reports `SYSTEM_HARDENING` and `FROZEN_AT_OWNER_GATE`.
- `advance` still stops at Owner Gate.
- Full runtime tests and frontend build pass.
