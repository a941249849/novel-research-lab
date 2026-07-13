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

巷口那盏歪斜的泥灯仍烧着。焰尖比平日矮了一截，风从砖缝钻过，火光便往灯芯上缩。每缩一次，墙上的护阵纹就暗掉一块，像被湿布擦去一层。

门槛内，苏晚把手背搭在膝头。灰雨留下的红点已经裂开，伤口不深，里头却不住渗出暗冷的光。她没包扎，只拿一截麻线绕了三圈。手指使不上力，绳结怎么也收不紧。

陆沉渊蹲在她面前，将门缝下扫进来的灰拢入掌心。

灰冷得像井底的泥。

“别看了。”

“我只辨巷里的灰痕。”

“看清了，也不能把它变干净。”

她说得不重，隔壁却传来碗底磕桌的闷响。

顾家的门半掩着。顾婶站在门后，脸被灯火照得蜡黄。装着补墨灰屑的陶片仍由莫井兰带着，裹在旧布里，贴于腰侧。守灯人没进谁家的门，只站在巷灯旁仰头看火。

灰雨落过以后，灯罩内壁多了一圈细黑点。那些黑点不往下坠，全黏在火光照不到的一面，密密挤着。

“仇慎送回来的话，明日辰时，顾家和我都得去。”莫井兰按了按腰间旧布，“缺一个，纸上便多一笔拒验。”

门框被顾婶攥得咯吱一声。

“我去。”

“你可以不去，我也可以。”

那只攥门框的手顿住了。

旧布包被取下来，搁到灯下，却没有拆开。

“我说过的话，只限我看见的。顾家灯上的旧灰是什么味，补墨灰凉不凉，断纹朝哪边，我能说。灰从哪儿来，我不知道；陆沉渊有没有资格碰它，我也不知道。明日若要我替这句‘不知道’按手印，我不按。”

顾婶嘴唇动了动。

屋里响起孩童翻身的窸窣声，床板轻轻一沉，又归于安静。莫井兰往那边看了一眼，将巷灯向外挪了半寸。手背暴露在灯下，泛着浸过冷水似的青，指节僵硬得迟迟没有收拢。

“那他们会把我家算进去。”

“算进去是一回事，你替他们补一句，是另一回事。”

“你说得轻巧。”

“我没说轻巧。”

灯焰映在莫井兰眼底，摇了两下。

“手伸出去以前，先看是不是自己的。”

巷中陆续有了人影。没人提灯，也没人靠得太近。墙根摆着几只空瓦罐，罐口蒙的灰布被风吹得一鼓一瘪。有人隔门问，明日是不是要挨家验灯；没人能答。另一扇窗后又传来声音，问顾家的账若翻不过去，下一户会不会轮到自己。

“别问了，叫衙里听见。”

“衙里不听，印也能落下来。”

起身时，陆沉渊左眼下那道焦纹扯得颧骨发紧。他抬手按住眼尾，指缝间落下一片黑屑。

“先把巷灯熄了。”

几扇门同时被推开。

苏晚抬起眼：“熄了，明日他们拿什么说护阵还在？”

“护阵快撑不住了。”

“凭什么？”

“凭灯焰。”

“灯焰缩了，不等于该熄。”

麻线被放到一旁。她把掌背贴上石门槛，寒气透入伤口，五指却没有缩回来。

“你能看灰痕，不能拿灰痕替命火作主。”

巷口的泥灯被风压低，灯芯发出细细的噼啪声。

陆沉渊没有再争，转身走到灯前。泥座下方裂开两道缝，里面积着白日灰雨干后的细粉。这些灰比陶片上的补墨灰更细，贴着泥缝打旋，触到护阵残纹便停。

两根手指悬在灯座上方，隔着一指距离。

识账术起得极慢。

眼底先是一烫，仿佛有人塞进一把烧红的砂。焦黑纹路顺着眼尾往下钻，视野里浮出银灰色的碎屑。巷中泥灯各自显出模糊寿痕，寻常火色暖而散，护阵上的火则细细相连。唯有裂缝中的灰不沿阵纹行走，到了命籍衙印痕附近，突兀地折向一旁。

折痕之间，空着半指宽。

那块空白没有余温，也不沾灯油，像一截被生生剜去的泥缝。

再往里看时，银灰火屑蓦地晃成重影。陆沉渊分不清哪道是阵纹，哪道只是眼底烧出的残痕。胸骨深处随呼吸错了一下，掌骨也跟着发出轻微摩擦声。他扶住灯座，咳得弯下腰，一蓬冷灰从喉间涌出，散落在湿泥上。

巷子静得只剩风声。

有人后退半步，有人把门关到只留一线。

待银灰残影逐片熄去，灯焰才重新浮回眼前。它比方才更矮了。

“够了。”

苏晚扶门站起，步子发虚。陆沉渊伸手，她侧过身，只将袖口递过去。

“扶衣服。”

那只手停在半空。

“我扶你。”

“我知道。”她喘了一口气，“可我不想让你把自己也压进去。”

手指只得抓住衣袖。薄布底下，她的手腕凉得没有一丝温度。

顾婶从门后迈出半步：“若明日只验我家的灯，巷里的阵会不会一并记上？”

无人立刻作答。

灯罩内壁的黑点被火光一晃，落下两粒。灰穿过焰心，黏在泥灯外沿，竟没被烧掉。

“我不知道。”陆沉渊说。

这三个字落下，顾婶把脸转开，看向自己手背。旧红痕已经淡了，灯下一照，裂口里仍有一线暗冷。

“那你明日还去？”

“去。”

“仇慎会盯着你。”

“他已经在盯。”

“纸上只要多一句，他们就能把整条巷写成同案。”

“所以我不替任何人说没见过的事。”

疲惫的戒备仍横在顾婶眼里。

“你替我家说话，能救我家的灯吗？”

“不能保证。”

“能让命籍衙退印吗？”

“不能。”

“那还要我去？”

陆沉渊摇了摇头：“你可以不去。不去，纸上会留下缺席；去了，只说亲眼所见。选哪一个，由你。”

门框上的五根手指慢慢松开。顾婶回头看向屋内，声音压得很低。

“我不想让他们顺手照孩子的灯。”

“那就说不让。”

巷中响起一道短促的抽气声。

苏晚偏头看他：“你知道这句话要担什么？”

“知道一点。”

“只有一点？”

“他们会把拒绝写成不合作。”

“还会往上递。上面不看苦衷，只看纸上有没有空。”

左眼深处又胀又痛，仿佛那把热砂仍嵌在里面。陆沉渊抹去掉到颧骨上的黑屑，拇指沾了一道焦痕。

“那也不能让孩子的命火填这张纸。”

巷尾一扇窗后，有人低声开口：“我家的可以先借半夜，只照巷灯，不给衙印。”

“闭嘴！”

旁边的呵斥来得又快又狠。窗后那半张脸立刻缩回黑暗。

苏晚抬手，拦住将要出声的儿子。

“你家的也不用。”

“可巷灯——”

“灯坏了便修灯，别拿命火堵裂缝。”

她的手背悬在空中，红痕随着喘息一明一暗。

“谁愿意守，自己站在灯下。谁不愿意，回屋关门。用不着向谁解释。”

门窗之后，一时无人应声。

莫井兰先将旧布包重新收回怀里：“明日我若不去，你会不会替我写见证？”

“不会。”

“他们逼你呢？”

“我只写你拒绝。”

“连说过的话也不替我补？”

“只记你亲口认下的。”

她点了点头。

“那我去。灰由我带着，不交出去。仇慎若要收，我便不说后半句。”

又过了片刻，顾婶咬着牙开口：“我也去。只说我家的灯，再说我看见你掌心发青。你的伤不能算成顾家的证。”

陆沉渊抬眼，她却没往这边看。

“你若倒在命审台上，他们会说是我家拖累的。这句先记清楚。”

苏晚笑了一声，短得像灯芯爆出的火星。

“听见了？”

“听见了。”

“还有我的话。”她将裂开的手背露在灯下，“我不替谁抵命，也不许谁拿巷里的灯填我的裂纹。仇慎若问，就让他听见。”

几扇门先后合拢，却都没有关死。细长灯光从缝中漏出，落在湿泥上，各照着自家门前一小块地方，谁也没越过谁家的门槛。

巷口泥灯歪得更厉害了。

陆沉渊走过去，将灯座缓缓扶正。泥缝随即响了一声，火焰斜向墙根，护阵纹短暂亮起，转眼又暗下去。

没有命火从任何一户流出来。

莫井兰找来一块旧砖，垫在灯座旁；顾婶拿扫帚抵住倾斜的灯罩。两人做完便松手，各自退回门内。苏晚也没来帮忙，只坐回门槛，把伤手藏进袖中。

没人催她。

到了后半夜，巷外传来铁片刮擦石路的声音。

一下，又一下。

声音从远处拖近，停在巷口。仇慎没进来，只将一张薄纸从门缝下推入。纸角压着冷金小印，印缝中那条暗红细线已经干透，像卡死在金属里的一根血丝。

“明日辰时，顾家户灯、守灯口述，另加泥灯巷护阵旁观。不得缺席。”

门内没有回答。

“旁观不收灯火，不碰孩童命页。”

仍是一片沉默。

铁片在石上挪了半寸。门外的声音低了些：“巷中若无人认领旁观，便按无证护阵记。”

苏晚撑着门框起身，走到纸边，没有弯腰。

“仇慎，我家灯若再失温，你敢不敢把验灯手印落在纸上？”

外面静了一会儿。

“敢，就进来验。不敢，就把话带回去。别拿空印吓人。”

冷金小印轻轻碰了碰纸面。

“明日辰时。”

脚步退远，铁片声重新拖过石路，渐渐没入夜色。

陆沉渊俯身拾纸。纸背恰好压过先前咳落的冷灰，灰粒没有散开，反而顺着纸纤维聚成一条细长空白，避开了命籍衙印落下的位置。

他看了两眼，将纸递向母亲。

苏晚没有接。

“收着，明天带去。”

“你不看？”

“我听见了。”

巷灯又缩了一下。

没有人伸手把自家的火递出来。门缝中的光仍各自亮着，照住各自脚边，也照着那张写明辰时的纸。

## Required JSON
```json
{
  "chapter_id": "chapter-0004",
  "artifact_kind": "revision",
  "artifact_sha256": "e3ed91078715d2b3540da38987cb7db63bcd559ea1e320fb0b07a550d091b6f7",
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
