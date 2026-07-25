# NRL v0.20 Asset Graph Remediation Re-review

## VERDICT
ACCEPT_WITH_WARNINGS

## RESOLVED_FINDINGS
- **Core Lamp Naming Split**: Resolved. The schema in `system/creation_assets/project_assets.v0.2.json` establishes `artifact_ashlight_cup` with display name `残命灯盏` as canonical, normalizing `灰烬回灯盏` as a deprecated internal alias.
- **State Ownership Overlap**: Resolved. Independent state ledger assets (`state_ledger_mudlamp_array_integrity`, `state_ledger_resident_lifefire_reserve`, `state_ledger_half_life_registry_exposure`, and `state_ledger_mother_life_lamp_countdown` in `system/creation_assets/project_assets.v0.2.json`) have been registered with single-writer constraints to prevent concurrent synchronization risks.
- **Progression Gating Mismatch**: Resolved. In `system/creation_assets/project_assets.v0.2.json`, `technique_ledger_recognition` restricts active capabilities to local, visible ash-trace mismatches for `character_lu_chenyuan` at the starting `燃命境初成` stage, locking advanced reading and covenant capabilities behind validated transitions.
- **Dependency Reversal & Lamp Acquisition Staging**: Partially Resolved. The schema in `system/creation_assets/project_assets.v0.2.json` corrects the dependency reversal by listing `artifact_ashlight_cup` as an active prerequisite instead of a counter for `technique_embertrace_return` and sets it to `dormant`. Staging its acquisition in `phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md` remains blocked because outline edits were excluded from the remediation scope.
- **Empty-Life Overload Standard**: Partially Resolved. The schema in `system/creation_assets/project_assets.v0.2.json` remediates `state_ledger_protagonist_strain` to define empty-life as a casting and cognitive lock with prepaid loss rather than a combat boost. However, the text contradiction in `phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md` and the outline remains unresolved and must remain blocked.
- **Missing Black-Market Merchant & Opponent Obligations**: Resolved. The bounded transaction role `npc_cluster5_black_market_transaction_role` has been registered, and independent obligations and knowledge limits have been specified for recurring opponents (`npc_debt_collector_gu_xun`, `npc_prefecture_shadow_envoy`, `npc_registrar_qiu_shen`) in `system/creation_assets/project_assets.v0.2.json`.
- **Clean up source_refs**: Resolved. All self-referential paths and references to files outside the packet-bound corpus have been cleaned up in the `source_refs` of `system/creation_assets/project_assets.v0.2.json`.

## REMAINING_BLOCKERS
- None. The asset graph and state ledger are fully bounded and safe for a restricted Chapter 1 intent (誊录吏 starting state and basic local ash-trace recognition, with advanced techniques and artifacts locked in `dormant` states).

## SERIAL_PROSE_BLOCKERS
- **Missing outline staging for lamp acquisition** (`outline_missing_lamp_acquisition_transition`): The outline (`phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md`) uses `artifact_ashlight_cup` in Arc Cluster 2 without staging its acquisition or watch-fire awakening in Arc Cluster 1 or prior, which conflicts with its dormant state.
- **Bible and Outline empty-life combat-boost contradiction** (`canonical_empty_life_text_conflict`): The text descriptions in the Bible (`phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md`) and Outline still describe empty-life as a combat-power booster, contradicting the state graph contract.
- **Cluster 5 exact transaction price** (`cluster5_exact_price_not_canonical`): The outline does not specify the exact price or price domain for the black-market merchant role, blocking any concrete transaction in prose until a bounded protagonist-owned price is registered from canonical evidence.
- **Unremediated state seed metrics** (`deferred_state_seed_ownership`): Metrics like public reputation, faction pressure, map unlock status, unresolved mysteries, and revealed account errors remain outline seeds without active writers.
- **Seed asset promotion provenance** (`seed_asset_promotion_provenance`): Seed contract assets still carry pre-remediation references and require a separate audit before promotion to active.

## RECOMMENDED_NEXT_GATE
`freeze_asset_baseline`
