# NRL v0.20 Final Creation Asset Graph Review

## 1. VERDICT
`REWORK_REQUIRED`

## 2. ASSET_FAMILY_COVERAGE
| Family | Chapter 1 Sufficiency | Blocked Before Serial Prose |
| :--- | :--- | :--- |
| `characters` | Sufficient. The protagonist (`character_lu_chenyuan`) is properly bounded in his low-status registry copying job with his mother's debt. | Stage-progression updates beyond the starting state (`燃命境初成`) must remain blocked. |
| `npcs` | Sufficient. Bounded roles exist for the mother (`npc_su_wan`), supervisors (`npc_registrar_qiu_shen`), and basic collectors (`npc_debt_collector_gu_xun`). | Bounded transaction roles for the black-market merchant/fugitive and independent motivations or divergent behaviors for recurring opponents must remain blocked. |
| `factions` | Sufficient. The neighborhood (`faction_mudlamp_lane`) and local bureaucracy (`faction_life_registry_office`) are properly established. | Faction expansion, alliance shifts, and higher-level treasury operations must remain blocked. |
| `artifacts` | Insufficient. The core lamp has a naming split (`残命灯盏` vs `灰烬回灯盏`) and lacks a staged acquisition transition prior to its use in Arc Cluster 2. | Use of `artifact_ashlight_cup` in prose must remain blocked until name mappings are unified and its Mudlamp Lane acquisition is staged. |
| `techniques` | Insufficient. A mismatch exists where `technique_ledger_recognition` is used by a `燃命境初成` character instead of the required `识账境`. In addition, dependency relationships are reversed. | All techniques other than basic local copy-level reading must remain blocked until progression gating is reconciled and counter dependencies are corrected. |
| `naming` | Sufficient. Local naming principles support sensory and local terms for Chapter 1. | Generation of high-level celestial titles and prefecture terminology must remain blocked until screened for collisions. |
| `emotional_bonds` | Sufficient. Bounded trust relationships are established via `bond_mother_su_wan` and `bond_mudlamp_lane_trust`. | Trust-state transitions and major sacrifices must remain blocked. |
| `foreshadowing` | Sufficient. Covers `foreshadowing_cinder_seal_rain` for early sensory anomalies. | Payoffs or revelations of `foreshadowing_ancient_debt_covenant_fragment` and `artifact_prefecture_transit_registry_seal` must remain blocked. |
| `state_ledger` | Insufficient. Overlapping ownership of metrics between `state_ledger_protagonist_strain` and `state_ledger_poorcity_returnfire` exists, and independent assets for key variables are missing. | All state ledger updates must remain blocked until single-writer ownership rules and transaction boundaries are defined. |

## 3. CROSS_ASSET_INTEGRITY
- **Naming Divergence**: `artifact_ashlight_cup` is registered as `灰烬回灯盏` but referenced in the bible and outline as `残命灯盏`, splitting the identity of the core asset.
- **Dependency Reversal**: `technique_embertrace_return` incorrectly lists its required tool `artifact_ashlight_cup` under `counter_ids` rather than as a prerequisite.
- **Progression Gating Mismatch**: `character_lu_chenyuan` is starting at `燃命境初成` but practices `technique_ledger_recognition` which can inspect chains and covenant glimpses. The bible gates these advanced capabilities under `识账境`.
- **State Ownership Overlap**: Both `state_ledger_protagonist_strain` and `state_ledger_poorcity_returnfire` write to `caster_lifefire_stability`, `half_life_registry_exposure`, and `mother_life_lamp_cracks`, creating synchronization risks.
- **Missing Faction/NPC Assets**: The black-market merchant required in Arc Cluster 5 has no active asset.
- **Self-referential Provenance**: `naming_lifefire_local_style` references `system/creation_assets/project_assets.v0.2.json` under `source_refs`.
- **Out-of-Packet References**: `character_lu_chenyuan`, `npc_debt_collector_gu_xun`, `npc_mo_jinglan`, `npc_prefecture_shadow_envoy`, `npc_registrar_qiu_shen`, `npc_su_wan`, `state_ledger_protagonist_strain`, `technique_chain_deflection_seal_breaking`, and `technique_ledger_recognition` list out-of-packet files like `antigravity-volume1-readiness-audit-v017.md`, `phase2E_chapter_plan_control_pack.md`, etc., as promotion evidence.

## 4. LONG_FORM_RISKS
- **Continuity Risks**:
  - Repetition of structural cycles: The outline reveals a formulaic cycle in each cluster (`pressure -> evidence -> combat -> public reversal -> backlash -> higher pursuit`). Without variance in outcomes (failed proof, partial recovery, negotiations), the long-form serial becomes predictable.
  - Sensory and physical backlash template: The immediate manifestation of white hair, split skin, and cold-ash cough on every spell activation risks becoming a formulaic text template, reducing the weight of cost.
- **Escalation Risks**:
  - Incompatible rules for empty-life overload: A risk where the empty-life state acts as a combat power boost in the outline, contradicting the ledger constraint of casting-window loss. This undermines the progression logic of a debt-bearing world.
  - Level-only progression: The progression system must avoid renaming ranks or scaling opponents in wider maps, ensuring each tier requires distinct proof (role competence, social authorization, multi-system control) as setting scope expands.
- **Emotional Relation Risks**:
  - Crowd-character abstraction: Untracked minor characters (craftsmen,小吏, witnesses) risk being reduced to uniform background fuel for the protagonist.
  - Adversarial flatness: Opponents (`npc_registrar_qiu_shen`, `npc_debt_collector_gu_xun`, `npc_prefecture_shadow_envoy`) are mapped strictly to enforcement roles, lacking independent personal motives or competing loyalties that allow adaptation, bargaining, or divergence.
- **Information-Reveal Risks**:
  - Over-revealing world limits: Early access to regional transits, the celestial account, or the ancient covenant in Volume 1 would collapse the long-term mystery.
  - Abstract reskinning: The world risks feeling like a single life-finance metaphor repeatedly reskinned if naming and lore are not populated with everyday family practices, non-account labor, and communal disagreements.

## 5. REQUIRED_REMEDIATIONS
1. Unify naming references for `artifact_ashlight_cup` across schemas, outline nodes, and bible references to resolve the `残命灯盏` / `灰烬回灯盏` split.
2. Establish a single-writer constraint or atomic transaction boundary for shared variables between `state_ledger_protagonist_strain` and `state_ledger_poorcity_returnfire`. Register independent assets for variables like `mudlamp_array_integrity` and `resident_lifefire_reserve`.
3. Reconcile the progression gap between `character_lu_chenyuan`'s starting tier `燃命境初成` and `technique_ledger_recognition`'s active scope by either upgrading the starting stage or restricting the technique's capabilities until the required transition is validated.
4. Correct `technique_embertrace_return.counter_ids` to show the lamp as an amplifier/prerequisite rather than a counter, and stage the acquisition of `artifact_ashlight_cup` in the outline before its first use.
5. Standardize empty-life overload as a casting limit and cognitive strain to match the constraints of `state_ledger_protagonist_strain`, removing the combat-boost contradiction in the outline.
6. Register the transaction-role assets for the Cluster 5 black-market merchant and specify independent obligations and knowledge limits for recurring opponents.
7. Clean up `source_refs` by removing self-referential paths and references to files outside the packet-bound corpus to restore auditability.

## 6. PROSE_GATE_RECOMMENDATION
The separate controlled-prose authorization must remain blocked. The naming splits, state ownership overlaps, progression mismatches, and out-of-packet dependencies represent significant risks that must be remediated at the metadata level before any serial prose production is initiated.
