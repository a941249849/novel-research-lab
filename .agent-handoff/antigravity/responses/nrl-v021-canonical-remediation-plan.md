# NRL v0.21 Canonical Remediation Plan

## CANONICAL_CHANGES

- **Lamp Acquisition Timing**
  - **Target File**: `phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md`
  - **Exact Semantic Correction**: Insert an explicit acquisition metadata node under Arc Cluster 1 specifying that `artifact_ashlight_cup` is dropped from the Mudlamp Lane array base and awakened using a consented watch-fire. Define this node as the mandatory prerequisite for the lamp's use in Arc Cluster 2.
  - **Preservation Constraints**: The correction must remain purely metadata-based in the outline tree structure. No prose description of the scene, dialogues, or specific execution details may be introduced, keeping the asset strictly dormant in Chapter 1.

- **Empty-Life State Definition**
  - **Target Files**: `phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md` (Lines 194–197) and `phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md` (Lines 83–94)
  - **Exact Semantic Correction**: Delete all textual references depicting the "empty-life" state (空寿状态) as a combat-power booster, combat-amplification mechanism, or battle-power enhancer. Redefine it in both files exclusively as a casting/cognition lock that closes ability windows, incurs prepaid lifefire loss, and requires external care to recover, matching the constraint defined in `project_assets.v0.2.json`.
  - **Preservation Constraints**: Prevent any combat advantages or power-up mechanics from being associated with empty-life. The correction must preserve the character's baseline limits at `燃命境初成` in Chapter 1.

- **Cluster 5 Black-Market Transaction Price**
  - **Target Files**: `phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md` and `system/creation_assets/project_assets.v0.2.json`
  - **Exact Semantic Correction**: Formally register the price domain for the transaction in Arc Cluster 5 as a bounded exchange of protagonist-owned evidence or research records, combined with a defined numeric increase in registry exposure (e.g., +10% `half_life_registry_exposure`). Add a strict validator that rejects child or resident lifefire as a transaction price.
  - **Preservation Constraints**: The transaction role remains name-less, backstory-less, and unaffiliated. The role must retire immediately upon completing the transaction, prohibiting downstream recurrence.

- **Deferred State Metrics Ownership**
  - **Target File**: `system/creation_assets/project_assets.v0.2.json`
  - **Exact Semantic Correction**: Promote the deferred state seeds (`public_reputation`, `faction_pressure`, `map_unlock_status`, `unresolved_mysteries`, `revealed_account_errors`) into active state ledgers. Assign single-writer ownership to each metric (e.g., mapping `revealed_account_errors` to `state_ledger_poorcity_returnfire`, or declaring explicit individual state-ledger objects).
  - **Preservation Constraints**: All mutations of these metrics must be balanced through explicit atomic transactions, forbidding untracked progression or implicit credit/debit changes.

- **Seed Asset Provenance Requirements**
  - **Target File**: `system/creation_assets/project_assets.v0.2.json`
  - **Exact Semantic Correction**: Audit all remaining seed contract assets (`artifacts_project_contract_seed`, `characters_project_contract_seed`, `emotional_bonds_project_contract_seed`, `factions_project_contract_seed`, `foreshadowing_project_contract_seed`, `naming_project_contract_seed`, `npcs_project_contract_seed`, `state_ledger_project_contract_seed`) to strip out all non-packet-bound source references. Restrict their `source_refs` strictly to the Hermez Bible and the Volume 1 Outline Tree.
  - **Preservation Constraints**: Keep these assets locked in the `seed` lifecycle state, preventing their use or active promotion in Chapter 1.

## ASSET_ALIGNMENT

- **Blocker 1 (Lamp Acquisition Timing)**: Affects `artifact_ashlight_cup` and `faction_mudlamp_lane`.
- **Blocker 2 (Empty-Life State Definition)**: Affects `state_ledger_protagonist_strain` and `character_lu_chenyuan`.
- **Blocker 3 (Cluster 5 Price Domain)**: Affects `npc_cluster5_black_market_transaction_role` and `state_ledger_half_life_registry_exposure`.
- **Blocker 4 (Deferred State Metrics Ownership)**: Affects `state_ledger_project_contract_seed` (specifically `public_reputation`, `faction_pressure`, `map_unlock_status`, `unresolved_mysteries`, `revealed_account_errors`), `state_ledger_poorcity_returnfire`, and `state_ledger_half_life_registry_exposure`.
- **Blocker 5 (Seed Asset Provenance)**: Affects `artifacts_project_contract_seed`, `characters_project_contract_seed`, `emotional_bonds_project_contract_seed`, `factions_project_contract_seed`, `foreshadowing_project_contract_seed`, `naming_project_contract_seed`, `npcs_project_contract_seed`, and `state_ledger_project_contract_seed`.

## NON_GOALS

- Do not write, generate, or authorize any chapter prose, scene drafts, or dialogue for Chapter 1 or subsequent chapters.
- Do not invent names, backstories, combat stats, or faction associations for the Cluster 5 black-market merchant role.
- Do not define any specific textual value or exact quantity for the transaction price outside the abstract exposure and evidence domain rules.
- Do not promote any seed assets to the active state within this remediation phase.
- Do not introduce new locations, maps, characters, or factions not already defined in the baseline.

## REVIEW_CRITERIA

- **Schema & Validation Executable Check**: The script `python3 system/runtime/nrl.py validate-creation-assets` must execute with exit code 0 and report zero errors.
- **Traceability Audit**: Every active asset in `project_assets.v0.2.json` must only reference source files from the packet-bound corpus: `phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md`, `phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md`, or the remediation JSON itself.
- **Single-Writer Lock**: No state ledger tracking metric can have more than one writer asset.
- **Gate Enforcement**: The `artifact_ashlight_cup`, `technique_embertrace_return`, and `technique_chain_deflection_seal_breaking` must resolve to `dormant` until the outline-staged prerequisite transitions are validated.
- **Atomic Balance Check**: All return-fire casts and exposure shifts must be validated as atomic transactions, showing that every credit to one ledger has a corresponding debit or exposure increase in another.
