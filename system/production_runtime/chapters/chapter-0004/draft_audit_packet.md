# NRL Antigravity Chapter Audit v0.20

Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.
Do not rewrite prose. Return one JSON object only using the exact binding hashes.

## Compact Context
{"chapter_id": "chapter-0004", "dramatic_purpose": "把一户人的命灯压力扩展为泥灯巷的共同风险，让陆沉渊接受街坊有拒绝见证的权利。", "must_keep": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "共同体不被当作资源；任何帮助都保留退出与拒绝。"], "must_avoid": ["不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"], "assets": [{"asset_id": "character_lu_chenyuan", "display_name": "陆沉渊", "family": "characters", "lifecycle_state": "active", "constraints": ["Does not transfer a life-cost to uninvolved residents.", "Each use leaves bodily evidence or increases pursuit risk.", "His mother debt and the lane protection array remain non-negotiable constraints.", "At 燃命境初成 he may only recognize ordinary life marks and local ash-trace mismatches; personal-page reading, chain tracing, covenant glimpses, return-fire casting, and seal breaking remain blocked pending validated advancement."], "relationships": [{"target_id": "bond_mother_su_wan", "relation_type": "son_bound_by_lifespan_debt"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_acquire_after_registered_transition"}, {"target_id": "faction_mudlamp_lane", "relation_type": "protects_and_is_bound_to"}, {"target_id": "technique_embertrace_return", "relation_type": "may_unlock_after_lamp_and_progression_gates"}, {"target_id": "technique_ledger_recognition", "relation_type": "uses_basic_local_ash_trace_scope_of"}]}, {"asset_id": "npc_su_wan", "display_name": "苏晚", "family": "npcs", "lifecycle_state": "active", "constraints": ["苏晚是能拒绝错误救法的行动者，不是可消耗的动机。", "她绝不接受以邻里命火、孩童寿数或无辜者命页抵消自己的寿债。", "她的命灯裂纹、冷灰气息和掌背失温须以感官后果呈现，不以抽象说明替代。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "bond_mother_su_wan", "relation_type": "embodies"}, {"target_id": "faction_mudlamp_lane", "relation_type": "mutual_aid_member_of"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "raises_restraint_threshold_for"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "is_counted_down_by"}]}, {"asset_id": "npc_registrar_qiu_shen", "display_name": "仇慎", "family": "npcs", "lifecycle_state": "active", "constraints": ["仇慎只能掌握本地残页与寿印权限，不能成为无所不知的阴谋解释者。", "其每一次施印必须留下可辨的冷金印痕或命灯失色，并制造可追责的现场后果。", "他可恐惧上级追责，但不能因恐惧自动洗白。", "其独立义务是保住本地呈印资格并避免州府问责；当公开证据使继续施印超出本地权限时，可拖延、议价或退回追缴令，但不得因此获得无证据洗白。"], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "serves_as_registrar_for"}, {"target_id": "character_lu_chenyuan", "relation_type": "supervises_and_targets"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "forwards_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "pressures_with_seals"}]}, {"asset_id": "npc_mo_jinglan", "display_name": "莫井兰", "family": "npcs", "lifecycle_state": "active", "constraints": ["Her knowledge is partial oral memory, never omniscient exposition.", "Helping preserve testimony exposes her remaining life-fire to collection."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "keeps_its_night_lamps"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "witnesses_surface_sign"}]}, {"asset_id": "bond_mother_su_wan", "display_name": "苏晚与陆沉渊的垫寿亲缘", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["The mother is an active moral presence, not expendable motivation.", "Any attempt to relieve her debt must carry an exposure, bodily, or communal consequence."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "deadline_is_tracked_by"}]}, {"asset_id": "bond_mudlamp_lane_trust", "display_name": "泥灯巷共灯之信", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["共同体信任不是主角可提取的资源；巷民有拒绝、质询和撤回见证的权利。", "信任提升必须来自共同承担、返还寿火或公开承担反噬，而非主角单方面胜利。", "任何高风险行动都须显示巷民的恐惧、选择与实际保护行为。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "binds_to_community"}, {"target_id": "faction_mudlamp_lane", "relation_type": "measures_mutual_aid_of"}, {"target_id": "npc_su_wan", "relation_type": "is_guarded_by_moral_boundary_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "conditions_witnessed_return"}]}, {"asset_id": "faction_mudlamp_lane", "display_name": "泥灯巷", "family": "factions", "lifecycle_state": "active", "constraints": ["The mutual-aid network cannot become expendable fuel for a single hero.", "Every communal protection act worsens the protection array's visible lifespan cracks or attracts collectors."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "contains_registered_acquisition_site_for"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "is_tracked_by"}]}, {"asset_id": "faction_life_registry_office", "display_name": "命籍衙", "family": "factions", "lifecycle_state": "active", "constraints": ["其压迫必须通过寿印、命灯、命审台和具体家庭后果显形，不写成现实机构讽刺。", "本地权限只能冻结、登记、送审与申请追缴，不能解释州府或天庭的完整真相。", "命审程序必须成为可被证据、见证和法术反打的冲突场域。"], "relationships": [{"target_id": "npc_registrar_qiu_shen", "relation_type": "employs"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "issues_local_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "assesses_and_pressures"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "contests"}]}, {"asset_id": "technique_ledger_recognition", "display_name": "识账术", "family": "techniques", "lifecycle_state": "active", "constraints": ["At character_lu_chenyuan's current 燃命境初成 stage, the active scope is limited to ordinary life marks and local copy-level ash-trace mismatches visible in the present evidence.", "Personal-page reading is locked to a validated 识账境 transition; chain tracing requires a later audited proof, and ancient-covenant glimpses remain blocked until an independently validated advanced transition and artifact evidence exist.", "The technique cannot directly read minds, predict outcomes, or produce a complete answer at any stage.", "施展后瞳孔浮出焦黑纹路、视野残留银灰火屑，并提升被寿印锁定的风险。", "所有判断须由可见痕迹或受害者见证复核，不能以主角独白定案。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "is_practiced_by"}, {"target_id": "technique_embertrace_return", "relation_type": "verifies_targets_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "increases"}, {"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "cannot_reveal_before_validated_advanced_progression"}]}, {"asset_id": "foreshadowing_cinder_seal_rain", "display_name": "灰雨印痕", "family": "foreshadowing", "lifecycle_state": "active", "constraints": ["The clue appears as sensory supernatural residue, not paperwork.", "Investigating it burns the investigator and raises collection exposure before any revelation."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "is_revealed_by"}, {"target_id": "npc_mo_jinglan", "relation_type": "is_remembered_by"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "payoff_tracks"}]}, {"asset_id": "state_ledger_protagonist_strain", "display_name": "陆沉渊命火与心魄承压", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["状态只记录可叙事化的命火、骨裂、瞳纹、冷灰与心魄恍惚，读者文本不得呈现工程字段。", "任何恢复都不能自动解除母亲寿债、半寿身份或既有追缴。", "承压过界时主角应失去施术窗口或需要他人阻止，而非获得无代价爆发。", "空寿状态是施术锁定与认知承压：不得提升战力；继续行动必须先支付已登记的寿火扣减，并失去至少一个施术或判断能力，恢复须停术和外部看护。", "This asset is the sole writer of sanity_level, caster_lifefire_stability, bone_fissure_severity, eye_pattern_burn, and cold_ash_cough_frequency; it may not write exposure or mother-lamp state."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "tracks_strain_for"}, {"target_id": "technique_ledger_recognition", "relation_type": "is_decreased_by"}, {"target_id": "technique_chain_deflection_seal_breaking", "relation_type": "is_worsened_by"}, {"target_id": "bond_mother_su_wan", "relation_type": "raises_family_risk_for"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_half_life_registry_exposure", "display_name": "半寿残籍暴露", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of half_life_registry_exposure; techniques, artifacts, NPCs, and other ledgers may request a delta but may not write the value directly.", "Exposure never decreases merely because evidence succeeds or life-fire returns; reduction requires a separately evidenced legal, masking, or withdrawal transition.", "Threshold crossings must change pursuit or access state before the atomic transaction can close.", "The Cluster 5 evidence-record exchange requests exactly +10 percentage points within the 0-100 bound and closes only with the protagonist-owned record debit under the same transaction ID; child, resident, and third-party life-fire prices are rejected."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "solely_tracks_registry_exposure_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "npc_cluster5_black_market_transaction_role", "relation_type": "is_increased_by_transaction_with"}]}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "display_name": "苏晚命灯裂纹倒计时", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mother_life_lamp_cracks and the mother-life-debt countdown.", "A communal return or protagonist recovery cannot automatically heal a crack or cancel the unresolved mother debt.", "Any technique transaction that affects Su Wan must record the crack/countdown delta here before closing."], "relationships": [{"target_id": "npc_su_wan", "relation_type": "solely_tracks_lamp_cracks_for"}, {"target_id": "bond_mother_su_wan", "relation_type": "provides_countdown_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "cannot_be_auto_cancelled_by"}]}, {"asset_id": "state_ledger_mudlamp_array_integrity", "display_name": "泥灯巷护阵完整度", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mudlamp_array_integrity; returned fire, resident reserve, and caster strain remain independently owned.", "Array integrity cannot rise from returned fire alone; witnessed repair or stabilization must be recorded.", "Below the registered safety line, lamp activation and return-fire casting fail closed rather than granting emergency power."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_array_integrity_for"}, {"target_id": "artifact_ashlight_cup", "relation_type": "gates_acquisition_and_activation_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_resident_lifefire_reserve", "display_name": "泥灯巷住户命火储备", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of resident_lifefire_reserve; the reserve is never protagonist inventory or an automatic communal resource.", "Every debit requires named consent and preserves the right to refuse or withdraw before transaction closure.", "No black-market price, technique cost, or artifact awakening may debit children, uninvolved residents, or an unspecified crowd."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_consented_reserve_for"}, {"target_id": "bond_mudlamp_lane_trust", "relation_type": "requires_refusal_and_consent_rights_from"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_supply_consented_watchfire_for_awakening"}]}, {"asset_id": "state_ledger_poorcity_returnfire", "display_name": "泥灯巷归火余量", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["A positive return never cancels the mother debt or the protection array burden automatically.", "Every gain must name whose life-fire returned and whose visible backlash or exposure increased.", "This asset is the sole writer of returned_miscollected_lifefire and may not write caster strain, registry exposure, array integrity, resident reserve, or mother-lamp state."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "measures_survival_pressure_for"}, {"target_id": "technique_embertrace_return", "relation_type": "is_changed_by"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_affected"}]}, {"asset_id": "state_ledger_revealed_account_errors", "display_name": "已揭示错账记录", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of revealed_account_errors; evidence, return-fire, and outline assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source evidence and at least one independently owned return-fire, exposure, reputation, pressure, or mystery consequence.", "No inferred or unverified account error may be counted, and no proof may create an implicit credit or debit."], "relationships": [{"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_faction_pressure", "display_name": "既有势力压力", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of faction_pressure; faction, NPC, and scene assets may request but may not apply a mutation.", "Every mutation must identify an existing source asset and settle atomically with exposure, public reputation, or revealed-error consequences.", "No new faction, location, or plot event may be created to justify a pressure change."], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "faction_prefecture_life_treasury", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_public_reputation", "display_name": "公开认知状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of public_reputation; all other assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source, reason, before/after state, and at least one independently owned consequence ledger.", "No success, witness, or exposure event changes reputation implicitly or closes without its peer ledger result."], "relationships": [{"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_unresolved_mysteries", "display_name": "未解账目疑点", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of unresolved_mysteries; foreshadowing and outline assets may request but may not apply a mutation.", "Every add, reclassification, or closure requires an explicit atomic transaction with a revealed-error or map-boundary consequence.", "No new mystery, answer, backstory, or plot event may be created by this ledger."], "relationships": [{"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "tracks_only_registered_questions_from"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_map_unlock_status", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_map_unlock_status", "display_name": "既有地图边界解锁状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of map_unlock_status; references to existing map boundaries may request but may not apply a transition.", "Every transition is atomic and must preserve unresolved boundaries while recording any exposure consequence.", "The ledger cannot introduce a location or unlock a boundary absent from the canonical outline."], "relationships": [{"target_id": "artifact_prefecture_transit_registry_seal", "relation_type": "requires_validated_boundary_evidence_from"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}], "prior_settlements": [{"chapter_id": "chapter-0001", "accepted_revision_sha256": "79d46dc564388fc32d8bae5b8fdc5ebd7a3dc2412e2174f8558844cad1fda874", "state_deltas": [{"fact_id": "chapter-0001-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": null, "after": "顾家的折记暂缓，午后再核"}, {"fact_id": "chapter-0001-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.local_enforcement_status", "operation": "set", "before": "顾家折记待按册落印核验", "after": "顾家折记暂缓至午后复核"}, {"fact_id": "chapter-0001-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": null, "after": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索"}, {"fact_id": "chapter-0001-information-foreshadowing-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨印痕未在本章现场显现", "after": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小"}, {"fact_id": "chapter-0001-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "寿籍司尚未进入泥灯巷核验", "after": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后"}, {"fact_id": "chapter-0001-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "眼尾仅有极淡、藏在睫毛下的焦黑细纹", "after": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0002", "accepted_revision_sha256": "356320d82944a61555f663908889d71d0afff3c35b5fa3c0ede592ef0ecfaeaf", "state_deltas": [{"fact_id": "chapter-0002-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家的折记暂缓，午后再核", "after": "顾家折记继续暂缓，三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后", "after": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.procedural_observation_of_lu_chenyuan", "before": null, "after": "陆沉渊被要求往后残籍复核在场；传核缺席按拒验记", "operation": "set"}, {"fact_id": "chapter-0002-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "operation": "set"}, {"fact_id": "chapter-0002-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": null, "after": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "operation": "set"}, {"fact_id": "chapter-0002-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "顾家“折三”补墨与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "错位线索被记为本地复核附录，但不作为改账依据", "operation": "set"}, {"fact_id": "chapter-0002-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小", "after": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "operation": "set"}, {"fact_id": "chapter-0002-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": null, "after": "顾家折记三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩", "after": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": null, "after": "识账后当场咳出一小片冷灰", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": null, "after": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "operation": "set"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0003", "accepted_revision_sha256": "8167366cd6811f13f63105eb5e0644bccb5c069e6081e29e4a66150554158b3f", "state_deltas": [{"fact_id": "chapter-0003-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "被要求往后残籍复核在场；传核缺席按拒验记", "after": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来"}, {"fact_id": "chapter-0003-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄"}, {"fact_id": "chapter-0003-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_witness_material", "operation": "set", "before": null, "after": "暂带顾家补墨灰屑陶片作为守灯见证物"}, {"fact_id": "chapter-0003-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_local_lamp_assessment", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "验灯显示命灯失温、焰尖缩成细线，手背红点裂开并渗出暗冷光"}, {"fact_id": "chapter-0003-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "after": "顾家附录暂封并列入三日内再验，苏晚户灯旁证暂不作改账凭据"}, {"fact_id": "chapter-0003-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "顾家折记三日内再次复核", "after": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证"}, {"fact_id": "chapter-0003-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "after": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔"}, {"fact_id": "chapter-0003-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "after": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界"}, {"fact_id": "chapter-0003-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "陆沉渊每次施术的反噬尚未被苏晚在本次复核中当场看见", "after": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹"}, {"fact_id": "chapter-0003-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "错位线索被记为本地复核附录，但不作为改账依据", "after": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据"}, {"fact_id": "chapter-0003-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线"}, {"fact_id": "chapter-0003-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "after": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": null, "after": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "识账后当场咳出一小片冷灰", "after": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印"}, {"fact_id": "chapter-0003-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "after": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸"}, {"fact_id": "chapter-0003-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "operation": "set", "before": "灰粒落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄"}], "resolved_audit_ids": []}]}

## Rule Stack
{"version": "0.22", "chapter_id": "chapter-0004", "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "priority_order": ["safety_and_originality", "canonical_story_bible", "volume_outline", "accepted_state_settlements", "creation_asset_constraints", "chapter_must_keep_and_must_avoid", "anti_ai_style_evidence"], "hard_rules": ["no source-work names, scenes, signature systems, or prose imitation", "no untracked power, relationship, location, item, or timeline changes", "all benefits carry an embodied, relational, or systemic cost", "reader-facing prose contains no runtime or database vocabulary", "不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "chapter_rules": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "共同体不被当作资源；任何帮助都保留退出与拒绝。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"]}

## Compilation Trace
{"version": "0.22", "chapter_id": "chapter-0004", "selected_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "explicit_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "dependency_asset_ids": [], "excluded_asset_count": 22, "selection_reason": "explicit chapter intent requirements plus atomic transaction peers", "canonical_hashes": {"borrowed_heaven_life_account_bible": "81575478a441852f18d451e9967245bbfce11d60cddd3af24e9b6565955e0604", "borrowed_heaven_volume1_outline_tree": "1f12fe8ad3262876eb533d40c94ad02abb90b95b38de387d339917fce9184648", "project_assets.v0.2": "90dbcf17d769e8a985fc87880a4382018c30133a2a53f82c3826636c8ed1dc61"}, "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "prior_settlement_count": 3}

## Observed Facts
{"chapter_id": "chapter-0004", "draft_sha256": "0829554f4c08b74322d9e8cf44cdb7c9164e86f9bc5026b61874807bd16fecb3", "facts": {"characters": [{"fact_id": "chapter-0004-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_intent", "before": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来", "after": "确认明日辰时到场，但不替任何住户陈述未亲见之事", "evidence": "陆沉渊答“去”，并对顾婶说“所以我不替任何人说没看见的事”。"}], "npcs": [{"fact_id": "chapter-0004-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "before": "暂带顾家补墨灰屑陶片作为守灯见证物", "after": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句", "evidence": "莫井兰说“那我去。但我只带这包灰，不把它交出去。若仇慎要收，我就不说后半句”。"}, {"fact_id": "chapter-0004-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_refusal_statement", "before": null, "after": "拒绝以自己抵命，也拒绝以泥灯巷住户命火填补自身裂纹", "evidence": "苏晚说“我不去替谁抵命，也不许谁拿巷里的灯来填我的裂纹”。"}, {"fact_id": "chapter-0004-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.latest_local_notice", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席", "evidence": "门外推入压着冷金小印的薄纸，并传话“明日辰时，顾家户灯、守灯口述，另加泥灯巷护阵旁观。不得缺席”。"}], "locations": [{"fact_id": "chapter-0004-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "before": null, "after": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩", "evidence": "灯座“裂成两道”；陆沉渊扶正后阵纹“亮了一瞬，随后又暗下”，莫井兰压砖、顾婶撑灯罩。"}], "factions": [{"fact_id": "chapter-0004-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证", "after": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记", "evidence": "门外补充“巷中若无人认领旁观，便按无证护阵记”。"}, {"fact_id": "chapter-0004-faction-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "before": null, "after": "未有住户命火实际投入巷口泥灯；住户保留各自关门、留缝或守灯的选择", "evidence": "苏晚要求“谁愿意守，就自己站灯下。谁不愿意，回屋关门”，结尾写明“没有人伸手把自己的灯火递出来”。"}], "artifacts": [], "techniques": [{"fact_id": "chapter-0004-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔", "after": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展", "evidence": "陆沉渊识账所见：裂缝灰“没有沿着阵纹走”，在靠近命籍衙印痕处“折了一下，留下半指宽的冷灰空白”。"}], "relationships": [{"fact_id": "chapter-0004-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界", "after": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片", "evidence": "莫井兰限定“我能说”“我不知道”；顾婶答“我也去。只说我家的灯”，并说“不想让孩子的灯被他们顺手照一遍”。"}], "emotions": [], "information": [], "hooks": [{"fact_id": "chapter-0004-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线", "after": "巷口泥灯罩内壁留下不下沉的黑点；薄纸上的冷灰沿纸纤维聚成空白，避开命籍衙印落点", "evidence": "灯罩黑点“全黏在火光照不到的那一面”；纸背冷灰“聚成一条细细的空白，正好避开命籍衙印落下的位置”。"}], "timeline": [{"fact_id": "chapter-0004-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时", "after": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "evidence": "后半夜仇慎未入巷，仅从门缝下推入通知薄纸，并重复“明日辰时”。"}], "physical_state": [{"fact_id": "chapter-0004-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑", "after": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑", "evidence": "识账时“焦黑纹路从眼尾再往下爬”；其后左眼疼胀，黑屑又落一片。"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印", "after": "本次夜间识账后再次咳出冷灰，落在巷口泥地", "evidence": "胸骨错裂后，陆沉渊弯腰咳嗽，“冷灰从喉间涌出来，落在泥地上”。"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "before": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感", "after": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声", "evidence": "“呼吸撞在裂口上”；陆沉渊撑住灯座时“掌骨里传出细微的摩擦声”。"}], "naming": []}}

## Prose
夜里，泥灯巷没有人先关门。

巷口那盏歪斜的泥灯还在烧，焰尖比平日低了一截，风从砖缝里钻过去，火光便跟着缩。每缩一次，墙上的护阵纹就暗一块，像有人拿湿布从旧墙上抹过。

苏晚坐在门槛里，手背搭着膝。那粒灰雨留下的红点已经裂开，裂口不深，却一直泛着暗冷的光。她没有包扎，指尖捻着一小截麻线，麻线缠了三圈，怎么也系不紧。

陆沉渊蹲在她面前，把门缝下扫进来的灰拨到掌心。

灰冷得像井底的泥。

“别看了。”苏晚说。

“我只辨巷里的灰痕。”

“看也不能把它变干净。”

她的声音不重。巷子里却有人把碗放下，瓷底磕在木桌上，闷闷一声。隔壁顾家的门半掩着，顾婶站在里面，脸色被灯火照得发黄。那片装着补墨灰屑的陶片还在莫井兰手里，用旧布包着，贴在她腰侧。

莫井兰没有进门。

她站在巷中那盏泥灯旁，抬头看着灯焰。灰雨落过后，灯罩内壁多了一层细细的黑点，黑点并不往下沉，全黏在火光照不到的那一面，像一圈闭着的眼睛。

“仇慎送回来的话，”她说，“明日辰时，顾家和我都得去。缺一个，纸上就多一笔拒验。”

顾婶攥紧门框。

“我去。”

“你可以不去。”莫井兰转过头，“我也可以不去。”

顾婶愣了愣。

莫井兰把那包陶片取下来，放在灯下，却没拆布。

“我说过的只限于我看见的。顾家灯上的旧灰是什么味，补墨灰凉不凉，断纹朝哪边，我能说。灰从哪里来，我不知道。陆沉渊有没有资格碰它，我也不知道。明日若要我在纸上替这句不知道按手印——我不按。”

顾婶的嘴唇动了一下，没出声。

屋里传来孩童翻身的声响，床板轻响，紧接着又静下去。莫井兰看了那扇门一眼，伸手把泥灯往外挪了半寸。她的手背在灯下显出一层薄薄的青色，指节像浸过冷水。

“那他们会把我家算进去。”顾婶说。

“算进去和你替他们补一句，原本就是两回事。”

“你说得轻巧。”

“我没说轻巧。”

莫井兰的目光落回灯上。

“我只是告诉你，手伸出去之前，先看是不是自己的。”

巷子里陆续有人出来。没有人带灯，也没有人靠得太近。墙根下摆着几只空瓦罐，罐口蒙着灰布，风一吹，灰布便轻轻鼓起。有人隔着门问，明日是不是要挨家验灯；没人回答。又有人问，顾家的账若翻不过去，下一户会不会轮到自己。

那声音很快被另一道更低的声音压住。

“别问了，叫衙里听见。”

“衙里不听见，印也能落下来。”

陆沉渊站起来时，左眼下的焦黑裂纹牵得颧骨发紧。他抬手按了一下，黑屑从皮肤上掉到袖口。他没有去擦。

“先把巷灯熄了。”他说。

这句话一落，几扇门同时开了。

苏晚抬眼看他。

“熄了，明日他们拿什么说护阵还在？”

“护阵已经快撑不住了。”

“你凭什么说？”

“凭灯焰。”

“灯焰缩了，不等于要熄。”

苏晚把麻线放下，掌背贴到门槛上。石头的凉意透进去，她的手指却没有收回。

“你看见的是灰痕，不是命。别把两样东西混在一起。”

陆沉渊没有答。

他转身走到巷口，靠近那盏泥灯。灯座下的泥已经裂成两道，裂缝里留着白日灰雨干后的细粉。那粉末比顾家陶片上的灰更细，贴着泥缝打旋，旋到护阵残纹边缘便停住。

他屏住呼吸，伸出两指，隔着一指宽的距离悬在灯座上方。

识账术起得很慢。

眼底像被人塞进一把烧红的砂。焦黑纹路从眼尾再往下爬，视野里浮出银灰火屑，巷中每一盏泥灯都被勾出一圈模糊的寿痕。寻常的火，暖而散；护阵上的火，细而相连。灯座裂缝里的灰却没有沿着阵纹走，它在靠近命籍衙印痕的地方折了一下，留下半指宽的冷灰空白。

那空白像一口没有填上的井。

陆沉渊想再看清一点，胸骨深处忽然一错，呼吸撞在裂口上。他弯腰咳嗽，冷灰从喉间涌出来，落在泥地上，散成几粒白点。

巷中安静下来。

有人退了一步。

有人把门关到只剩一条缝。

陆沉渊撑住灯座，掌骨里传出细微的摩擦声。眼前的银灰火屑一片片熄灭，灯焰重新浮回视野，却比刚才更低。

苏晚从门里站起来。

“够了。”

她走得不快，脚下却有些虚。陆沉渊伸手去扶，她侧身避开，只把自己的袖口递给他。

“扶衣服。”

他的手停在半空。

“我扶你。”

“我知道。”她说，“可我现在不想让你把自己也压进来。”

他抓住她的袖口。布料薄，里面的手腕凉得没有温度。

顾婶从门后走出半步。

“若明日只验我家的灯，巷里的阵会不会被一并记上？”

陆沉渊看着她，没有立刻回答。

巷口的灯火在风里晃了一下。那圈黏在灯罩内壁的黑点随之移位，落下两粒灰，穿过火焰，落在泥灯外沿。火焰没有烧掉它们。

“我不知道。”他说。

这三个字比任何判断都让人难受。

顾婶低头看自己的手背。红痕已经淡了，灯光一照，仍能看见裂口里那缕暗冷的亮。

“那你明日还去吗？”

“去。”

“你去，仇慎会盯着你。”

“他已经在盯。”

“你若在纸上多说一句，他们就能把整条巷子写成同案。”

陆沉渊松开苏晚的袖口，转向她。

“所以我不替任何人说没看见的事。”

顾婶看着他，眼神里没有松动，只有一层疲惫的戒备。

“你替我家说了，能救我家的灯吗？”

“不能保证。”

“能让命籍衙退印吗？”

“不能。”

“那你还要我去？”

“你可以不去。”

这回，陆沉渊说得很慢。

“你不去，纸上会留下缺席。你去了，只说你亲眼看见的。选哪一个，由你。”

顾婶的手指从门框上一根根松开。她回头看了看屋里，声音压得极低。

“我不想让孩子的灯被他们顺手照一遍。”

“那就说不让。”

巷子里有人吸了一口凉气。

苏晚侧过脸，望着陆沉渊。

“你知道说不让要担什么？”

“知道一点。”

“只是一点？”

“我知道他们会把拒绝写成不合作。”

“还会把不合作递给更上面。”她说，“上面不会看你有没有苦衷，只看纸上有没有空。”

陆沉渊的左眼疼得发胀，黑屑又落了一片。他用拇指抹掉，指腹留下焦黑的痕。

“那也不能把孩子的命火放上去。”

“谁说要放孩子的？”

巷尾一道声音传来。

顾婶回头。一个住户站在自家窗后，只露出半张脸。他没有走出来，也没有报姓名。

“我家的可以先借半夜。”他说，“只照巷灯，不给衙印。”

“闭嘴。”旁边有人厉声道。

窗后的脸缩了一下。

苏晚抬手，挡住陆沉渊将要开口的动作。

“你家的也不用。”

“可巷灯——”

“巷灯坏了，修巷灯。别拿命火去堵。”

她的手背在空中停着，红痕随着她的喘息微微发亮。

“谁愿意守，就自己站灯下。谁不愿意，回屋关门。谁都不用解释。”

没有人立刻应声。

莫井兰先把陶片的包裹收回怀里。她看着陆沉渊，问：“若我明日不去，你会不会在纸上替我写见证？”

“不会。”

“若他们逼你写？”

“那我写你拒绝。”

“连我说过的话也不替我补？”

“只写你亲口说的。”

莫井兰点了点头。

“那我去。但我只带这包灰，不把它交出去。若仇慎要收，我就不说后半句。”

顾婶咬住牙，过了片刻，终于道：“我也去。只说我家的灯，还有我看见陆沉渊掌心发青。别把他的伤写成顾家的证。”

陆沉渊抬头。

顾婶没看他。

“你要是倒在命审台上，他们会说是我家拖累的。先把这句记清。”

苏晚轻轻笑了一下，笑意很短。

“听见没有？”

“听见了。”

“还有我。”她说，“我不去替谁抵命，也不许谁拿巷里的灯来填我的裂纹。仇慎若问，就让他听见这句话。”

巷中几扇门重新合上，仍没有全关。门缝里漏出的灯光细细长长，落在湿泥上，彼此没有连成一片。

陆沉渊看着那些光，忽然明白，护阵并非只有亮与灭。有人把门敞开，有人只留缝，有人连缝也不肯留。那点微弱的照见，不能由他替谁收拢。

他走到巷口，把泥灯扶正。

灯座裂缝随即发出一声轻响，火焰向旁边歪去。墙上的护阵纹亮了一瞬，随后又暗下。没有新的火从谁家灯里流出来，只有莫井兰把一块旧砖压在灯座旁，顾婶拿扫帚撑住倾斜的灯罩。两个人做完便退开，各自回门内。

苏晚没有帮忙。她坐回门槛，把手背藏进袖子里。

陆沉渊也没有催她。

后半夜，巷外传来铁片刮过石路的声音。

那声音从远处一点点逼近，停在巷口。仇慎没有进来，只把一张薄纸从门缝下推入。纸角压着冷金小印，印缝里那条暗红细线已经干了，像一根卡死的血丝。

“明日辰时，顾家户灯、守灯口述，另加泥灯巷护阵旁观。”门外的人说，“不得缺席。”

没人回答。

“旁观不收灯火，不碰孩童命页。”

还是没人回答。

仇慎停了一会儿，声音低了些：“巷中若无人认领旁观，便按无证护阵记。”

苏晚从门槛上起身，走到纸边，却没有弯腰捡。

“仇慎，”她隔着门说，“我家灯若再失温，你敢不敢把验灯手印落在纸上？”

门外沉默。

“敢，就进来验。不敢，就把话带回去，别拿空印吓人。”

冷金小印在门外轻轻碰了一下纸面。

“明日辰时。”

脚步声退远，铁片声重新拖过石路。

陆沉渊俯身拾起那张纸。纸背沾着他方才咳出的冷灰，灰粒没有散，沿着纸纤维聚成一条细细的空白，正好避开命籍衙印落下的位置。

他看了片刻，将纸递给苏晚。

苏晚没有接。

“收着。”她说，“明天带去。”

“你不看？”

“我听见了。”

巷口的泥灯又缩了一下。

这一次，没有人伸手把自己的灯火递出来。门缝里的光各自亮着，照着各自的脚边，也照着那张写明辰时的纸。

## Required JSON
```json
{
  "chapter_id": "chapter-0004",
  "artifact_kind": "draft",
  "artifact_sha256": "0829554f4c08b74322d9e8cf44cdb7c9164e86f9bc5026b61874807bd16fecb3",
  "context_sha256": "65a8bf61104cfa25dfc2014d94f290aea7569588c654883bc378a26688f135d3",
  "verdict": "ACCEPT_WITH_WARNINGS",
  "dimensions": {
    "canon": [],
    "character": [],
    "state": [],
    "causality": [],
    "pacing": [],
    "life_force": [],
    "anti_ai_taste": [],
    "originality": []
  },
  "issues": []
}
```
