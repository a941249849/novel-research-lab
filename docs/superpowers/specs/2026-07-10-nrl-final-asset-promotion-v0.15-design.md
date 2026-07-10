# NRL Final Asset Promotion v0.15 Design

## Purpose

Turn a Hermes-produced final-asset candidate for `《借天改命账》` into a
validated, auditable creation-store update without opening prose generation.

## Boundary

Hermes produces a candidate JSON file in the controlled inbox. Codex validates
the envelope, exact nine-family coverage, source-path boundary, uniqueness,
cross-asset references, and the combined creation store. Only Codex promotes a
valid candidate after locating the matching Owner decision.

## Contract

- Candidate: `system/agent_ops/inbox/hermes-final-asset-bundle-v015.json`.
- Exactly one `active` asset per creation family; candidate IDs must be new.
- Source references must remain in the packet allowlist and may never name
  `novel_training_set/`.
- Promotion preserves all seed assets and writes a hash-bearing manifest.
- The Owner decision must authorize `generate_final_creation_assets` and expire
  at `phase2f_final_asset_generation`.
- `generate_novel_prose` remains forbidden in validation results and manifests.

## Runtime Interface

```bash
python3 system/runtime/nrl.py final-assets-validate --file system/agent_ops/inbox/hermes-final-asset-bundle-v015.json
python3 system/runtime/nrl.py final-assets-promote --file system/agent_ops/inbox/hermes-final-asset-bundle-v015.json
```

## Non-Goals

This workflow creates no chapter plan, scene, dialogue, narration, or other
novel prose. It does not read raw files under `novel_training_set/`.
