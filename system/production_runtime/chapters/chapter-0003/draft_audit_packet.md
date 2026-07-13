# NRL Antigravity Chapter Audit v0.20

Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.
Do not rewrite prose. Return one JSON object only using the exact binding hashes.

## Compact Context
{"chapter_id": "chapter-0003", "dramatic_purpose": "让午后复核留下可被第三方否认也可被追查的局部痕迹，陆沉渊必须选择保住母亲命灯还是保住证据。", "must_keep": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "可见灰痕与口述必须互相校验；识账只可辨认本地错位。"], "must_avoid": ["不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"], "assets": [{"asset_id": "character_lu_chenyuan", "display_name": "陆沉渊", "family": "characters", "lifecycle_state": "active", "constraints": ["Does not transfer a life-cost to uninvolved residents.", "Each use leaves bodily evidence or increases pursuit risk.", "His mother debt and the lane protection array remain non-negotiable constraints.", "At 燃命境初成 he may only recognize ordinary life marks and local ash-trace mismatches; personal-page reading, chain tracing, covenant glimpses, return-fire casting, and seal breaking remain blocked pending validated advancement."], "relationships": [{"target_id": "bond_mother_su_wan", "relation_type": "son_bound_by_lifespan_debt"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_acquire_after_registered_transition"}, {"target_id": "faction_mudlamp_lane", "relation_type": "protects_and_is_bound_to"}, {"target_id": "technique_embertrace_return", "relation_type": "may_unlock_after_lamp_and_progression_gates"}, {"target_id": "technique_ledger_recognition", "relation_type": "uses_basic_local_ash_trace_scope_of"}]}, {"asset_id": "npc_su_wan", "display_name": "苏晚", "family": "npcs", "lifecycle_state": "active", "constraints": ["苏晚是能拒绝错误救法的行动者，不是可消耗的动机。", "她绝不接受以邻里命火、孩童寿数或无辜者命页抵消自己的寿债。", "她的命灯裂纹、冷灰气息和掌背失温须以感官后果呈现，不以抽象说明替代。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "bond_mother_su_wan", "relation_type": "embodies"}, {"target_id": "faction_mudlamp_lane", "relation_type": "mutual_aid_member_of"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "raises_restraint_threshold_for"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "is_counted_down_by"}]}, {"asset_id": "npc_registrar_qiu_shen", "display_name": "仇慎", "family": "npcs", "lifecycle_state": "active", "constraints": ["仇慎只能掌握本地残页与寿印权限，不能成为无所不知的阴谋解释者。", "其每一次施印必须留下可辨的冷金印痕或命灯失色，并制造可追责的现场后果。", "他可恐惧上级追责，但不能因恐惧自动洗白。", "其独立义务是保住本地呈印资格并避免州府问责；当公开证据使继续施印超出本地权限时，可拖延、议价或退回追缴令，但不得因此获得无证据洗白。"], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "serves_as_registrar_for"}, {"target_id": "character_lu_chenyuan", "relation_type": "supervises_and_targets"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "forwards_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "pressures_with_seals"}]}, {"asset_id": "npc_mo_jinglan", "display_name": "莫井兰", "family": "npcs", "lifecycle_state": "active", "constraints": ["Her knowledge is partial oral memory, never omniscient exposition.", "Helping preserve testimony exposes her remaining life-fire to collection."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "keeps_its_night_lamps"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "witnesses_surface_sign"}]}, {"asset_id": "bond_mother_su_wan", "display_name": "苏晚与陆沉渊的垫寿亲缘", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["The mother is an active moral presence, not expendable motivation.", "Any attempt to relieve her debt must carry an exposure, bodily, or communal consequence."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "deadline_is_tracked_by"}]}, {"asset_id": "bond_mudlamp_lane_trust", "display_name": "泥灯巷共灯之信", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["共同体信任不是主角可提取的资源；巷民有拒绝、质询和撤回见证的权利。", "信任提升必须来自共同承担、返还寿火或公开承担反噬，而非主角单方面胜利。", "任何高风险行动都须显示巷民的恐惧、选择与实际保护行为。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "binds_to_community"}, {"target_id": "faction_mudlamp_lane", "relation_type": "measures_mutual_aid_of"}, {"target_id": "npc_su_wan", "relation_type": "is_guarded_by_moral_boundary_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "conditions_witnessed_return"}]}, {"asset_id": "faction_mudlamp_lane", "display_name": "泥灯巷", "family": "factions", "lifecycle_state": "active", "constraints": ["The mutual-aid network cannot become expendable fuel for a single hero.", "Every communal protection act worsens the protection array's visible lifespan cracks or attracts collectors."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "contains_registered_acquisition_site_for"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "is_tracked_by"}]}, {"asset_id": "faction_life_registry_office", "display_name": "命籍衙", "family": "factions", "lifecycle_state": "active", "constraints": ["其压迫必须通过寿印、命灯、命审台和具体家庭后果显形，不写成现实机构讽刺。", "本地权限只能冻结、登记、送审与申请追缴，不能解释州府或天庭的完整真相。", "命审程序必须成为可被证据、见证和法术反打的冲突场域。"], "relationships": [{"target_id": "npc_registrar_qiu_shen", "relation_type": "employs"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "issues_local_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "assesses_and_pressures"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "contests"}]}, {"asset_id": "technique_ledger_recognition", "display_name": "识账术", "family": "techniques", "lifecycle_state": "active", "constraints": ["At character_lu_chenyuan's current 燃命境初成 stage, the active scope is limited to ordinary life marks and local copy-level ash-trace mismatches visible in the present evidence.", "Personal-page reading is locked to a validated 识账境 transition; chain tracing requires a later audited proof, and ancient-covenant glimpses remain blocked until an independently validated advanced transition and artifact evidence exist.", "The technique cannot directly read minds, predict outcomes, or produce a complete answer at any stage.", "施展后瞳孔浮出焦黑纹路、视野残留银灰火屑，并提升被寿印锁定的风险。", "所有判断须由可见痕迹或受害者见证复核，不能以主角独白定案。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "is_practiced_by"}, {"target_id": "technique_embertrace_return", "relation_type": "verifies_targets_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "increases"}, {"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "cannot_reveal_before_validated_advanced_progression"}]}, {"asset_id": "foreshadowing_cinder_seal_rain", "display_name": "灰雨印痕", "family": "foreshadowing", "lifecycle_state": "active", "constraints": ["The clue appears as sensory supernatural residue, not paperwork.", "Investigating it burns the investigator and raises collection exposure before any revelation."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "is_revealed_by"}, {"target_id": "npc_mo_jinglan", "relation_type": "is_remembered_by"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "payoff_tracks"}]}, {"asset_id": "state_ledger_protagonist_strain", "display_name": "陆沉渊命火与心魄承压", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["状态只记录可叙事化的命火、骨裂、瞳纹、冷灰与心魄恍惚，读者文本不得呈现工程字段。", "任何恢复都不能自动解除母亲寿债、半寿身份或既有追缴。", "承压过界时主角应失去施术窗口或需要他人阻止，而非获得无代价爆发。", "空寿状态是施术锁定与认知承压：不得提升战力；继续行动必须先支付已登记的寿火扣减，并失去至少一个施术或判断能力，恢复须停术和外部看护。", "This asset is the sole writer of sanity_level, caster_lifefire_stability, bone_fissure_severity, eye_pattern_burn, and cold_ash_cough_frequency; it may not write exposure or mother-lamp state."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "tracks_strain_for"}, {"target_id": "technique_ledger_recognition", "relation_type": "is_decreased_by"}, {"target_id": "technique_chain_deflection_seal_breaking", "relation_type": "is_worsened_by"}, {"target_id": "bond_mother_su_wan", "relation_type": "raises_family_risk_for"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_half_life_registry_exposure", "display_name": "半寿残籍暴露", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of half_life_registry_exposure; techniques, artifacts, NPCs, and other ledgers may request a delta but may not write the value directly.", "Exposure never decreases merely because evidence succeeds or life-fire returns; reduction requires a separately evidenced legal, masking, or withdrawal transition.", "Threshold crossings must change pursuit or access state before the atomic transaction can close.", "The Cluster 5 evidence-record exchange requests exactly +10 percentage points within the 0-100 bound and closes only with the protagonist-owned record debit under the same transaction ID; child, resident, and third-party life-fire prices are rejected."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "solely_tracks_registry_exposure_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "npc_cluster5_black_market_transaction_role", "relation_type": "is_increased_by_transaction_with"}]}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "display_name": "苏晚命灯裂纹倒计时", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mother_life_lamp_cracks and the mother-life-debt countdown.", "A communal return or protagonist recovery cannot automatically heal a crack or cancel the unresolved mother debt.", "Any technique transaction that affects Su Wan must record the crack/countdown delta here before closing."], "relationships": [{"target_id": "npc_su_wan", "relation_type": "solely_tracks_lamp_cracks_for"}, {"target_id": "bond_mother_su_wan", "relation_type": "provides_countdown_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "cannot_be_auto_cancelled_by"}]}, {"asset_id": "state_ledger_mudlamp_array_integrity", "display_name": "泥灯巷护阵完整度", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mudlamp_array_integrity; returned fire, resident reserve, and caster strain remain independently owned.", "Array integrity cannot rise from returned fire alone; witnessed repair or stabilization must be recorded.", "Below the registered safety line, lamp activation and return-fire casting fail closed rather than granting emergency power."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_array_integrity_for"}, {"target_id": "artifact_ashlight_cup", "relation_type": "gates_acquisition_and_activation_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_resident_lifefire_reserve", "display_name": "泥灯巷住户命火储备", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of resident_lifefire_reserve; the reserve is never protagonist inventory or an automatic communal resource.", "Every debit requires named consent and preserves the right to refuse or withdraw before transaction closure.", "No black-market price, technique cost, or artifact awakening may debit children, uninvolved residents, or an unspecified crowd."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_consented_reserve_for"}, {"target_id": "bond_mudlamp_lane_trust", "relation_type": "requires_refusal_and_consent_rights_from"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_supply_consented_watchfire_for_awakening"}]}, {"asset_id": "state_ledger_poorcity_returnfire", "display_name": "泥灯巷归火余量", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["A positive return never cancels the mother debt or the protection array burden automatically.", "Every gain must name whose life-fire returned and whose visible backlash or exposure increased.", "This asset is the sole writer of returned_miscollected_lifefire and may not write caster strain, registry exposure, array integrity, resident reserve, or mother-lamp state."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "measures_survival_pressure_for"}, {"target_id": "technique_embertrace_return", "relation_type": "is_changed_by"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_affected"}]}, {"asset_id": "state_ledger_revealed_account_errors", "display_name": "已揭示错账记录", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of revealed_account_errors; evidence, return-fire, and outline assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source evidence and at least one independently owned return-fire, exposure, reputation, pressure, or mystery consequence.", "No inferred or unverified account error may be counted, and no proof may create an implicit credit or debit."], "relationships": [{"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_faction_pressure", "display_name": "既有势力压力", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of faction_pressure; faction, NPC, and scene assets may request but may not apply a mutation.", "Every mutation must identify an existing source asset and settle atomically with exposure, public reputation, or revealed-error consequences.", "No new faction, location, or plot event may be created to justify a pressure change."], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "faction_prefecture_life_treasury", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_public_reputation", "display_name": "公开认知状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of public_reputation; all other assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source, reason, before/after state, and at least one independently owned consequence ledger.", "No success, witness, or exposure event changes reputation implicitly or closes without its peer ledger result."], "relationships": [{"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_unresolved_mysteries", "display_name": "未解账目疑点", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of unresolved_mysteries; foreshadowing and outline assets may request but may not apply a mutation.", "Every add, reclassification, or closure requires an explicit atomic transaction with a revealed-error or map-boundary consequence.", "No new mystery, answer, backstory, or plot event may be created by this ledger."], "relationships": [{"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "tracks_only_registered_questions_from"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_map_unlock_status", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_map_unlock_status", "display_name": "既有地图边界解锁状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of map_unlock_status; references to existing map boundaries may request but may not apply a transition.", "Every transition is atomic and must preserve unresolved boundaries while recording any exposure consequence.", "The ledger cannot introduce a location or unlock a boundary absent from the canonical outline."], "relationships": [{"target_id": "artifact_prefecture_transit_registry_seal", "relation_type": "requires_validated_boundary_evidence_from"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}], "prior_settlements": [{"chapter_id": "chapter-0001", "accepted_revision_sha256": "79d46dc564388fc32d8bae5b8fdc5ebd7a3dc2412e2174f8558844cad1fda874", "state_deltas": [{"fact_id": "chapter-0001-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": null, "after": "顾家的折记暂缓，午后再核"}, {"fact_id": "chapter-0001-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.local_enforcement_status", "operation": "set", "before": "顾家折记待按册落印核验", "after": "顾家折记暂缓至午后复核"}, {"fact_id": "chapter-0001-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": null, "after": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索"}, {"fact_id": "chapter-0001-information-foreshadowing-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨印痕未在本章现场显现", "after": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小"}, {"fact_id": "chapter-0001-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "寿籍司尚未进入泥灯巷核验", "after": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后"}, {"fact_id": "chapter-0001-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "眼尾仅有极淡、藏在睫毛下的焦黑细纹", "after": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0002", "accepted_revision_sha256": "356320d82944a61555f663908889d71d0afff3c35b5fa3c0ede592ef0ecfaeaf", "state_deltas": [{"fact_id": "chapter-0002-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家的折记暂缓，午后再核", "after": "顾家折记继续暂缓，三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后", "after": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.procedural_observation_of_lu_chenyuan", "before": null, "after": "陆沉渊被要求往后残籍复核在场；传核缺席按拒验记", "operation": "set"}, {"fact_id": "chapter-0002-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "operation": "set"}, {"fact_id": "chapter-0002-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": null, "after": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "operation": "set"}, {"fact_id": "chapter-0002-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "顾家“折三”补墨与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "错位线索被记为本地复核附录，但不作为改账依据", "operation": "set"}, {"fact_id": "chapter-0002-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小", "after": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "operation": "set"}, {"fact_id": "chapter-0002-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": null, "after": "顾家折记三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩", "after": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": null, "after": "识账后当场咳出一小片冷灰", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": null, "after": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "operation": "set"}], "resolved_audit_ids": []}]}

## Rule Stack
{"version": "0.22", "chapter_id": "chapter-0003", "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "priority_order": ["safety_and_originality", "canonical_story_bible", "volume_outline", "accepted_state_settlements", "creation_asset_constraints", "chapter_must_keep_and_must_avoid", "anti_ai_style_evidence"], "hard_rules": ["no source-work names, scenes, signature systems, or prose imitation", "no untracked power, relationship, location, item, or timeline changes", "all benefits carry an embodied, relational, or systemic cost", "reader-facing prose contains no runtime or database vocabulary", "不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "chapter_rules": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "可见灰痕与口述必须互相校验；识账只可辨认本地错位。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"]}

## Compilation Trace
{"version": "0.22", "chapter_id": "chapter-0003", "selected_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "explicit_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "dependency_asset_ids": [], "excluded_asset_count": 22, "selection_reason": "explicit chapter intent requirements plus atomic transaction peers", "canonical_hashes": {"borrowed_heaven_life_account_bible": "81575478a441852f18d451e9967245bbfce11d60cddd3af24e9b6565955e0604", "borrowed_heaven_volume1_outline_tree": "1f12fe8ad3262876eb533d40c94ad02abb90b95b38de387d339917fce9184648", "project_assets.v0.2": "90dbcf17d769e8a985fc87880a4382018c30133a2a53f82c3826636c8ed1dc61"}, "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "prior_settlement_count": 2}

## Observed Facts
{"chapter_id": "chapter-0003", "draft_sha256": "cb75a467d08b6e6c0b382b9e4a6bb53bb58a87ac4c386aa6eca633ddc1352022", "facts": {"characters": [{"fact_id": "chapter-0003-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "before": "被要求往后残籍复核在场；传核缺席按拒验记", "after": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来", "evidence": "陆沉渊在传核纸上写下名字；仇慎随后命他明日辰时再来。"}], "npcs": [{"fact_id": "chapter-0003-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家折记继续暂缓，三日内再次复核", "after": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "evidence": "仇慎放下印后明确作出封存附录、守灯人暂带灰物、三日内再验及验灯不熄的决定。"}, {"fact_id": "chapter-0003-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_witness_material", "before": null, "after": "暂带顾家补墨灰屑陶片作为守灯见证物", "evidence": "陆沉渊将陶片推到莫井兰手边，莫井兰将其塞进旧布夹层；仇慎准其暂带。"}, {"fact_id": "chapter-0003-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_local_lamp_assessment", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "验灯显示命灯失温、焰尖缩成细线，手背红点裂开并渗出暗冷光", "evidence": "薄铜验灯在苏晚指骨上缩成细线；其手背红点裂开，渗出的不是血而是一点暗暗冷光。"}], "locations": [], "factions": [{"fact_id": "chapter-0003-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "after": "顾家附录暂封并列入三日内再验，苏晚户灯旁证暂不作改账凭据", "evidence": "仇慎宣布附录封存、三日内再验，并称苏晚户灯旁证暂不作改账凭据。"}, {"fact_id": "chapter-0003-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": "顾家折记三日内再次复核", "after": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证", "evidence": "仇慎规定明日辰时携顾家与守灯口述再来，并说明缺人及灰物受损的程序后果。"}], "artifacts": [], "techniques": [{"fact_id": "chapter-0003-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "after": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔", "evidence": "陆沉渊以识账只辨眼前灰痕，看见两边纹路中隔着无寿火的冷灰空白，并见验灯红痕靠近衙印处完整。"}], "relationships": [{"fact_id": "chapter-0003-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "after": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界", "evidence": "莫井兰先询问顾婶是否愿意代记，随后逐项说出可认灰痕，并明确“至于是谁落的，我不知道”。"}, {"fact_id": "chapter-0003-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "before": "陆沉渊每次施术的反噬尚未被苏晚在本次复核中当场看见", "after": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹", "evidence": "正文明确写苏晚看见他掌心青白印和左眼下再也遮不住的焦黑裂纹。"}], "emotions": [], "information": [{"fact_id": "chapter-0003-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "错位线索被记为本地复核附录，但不作为改账依据", "after": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据", "evidence": "灰落在附录上，顾婶红点与莫井兰口述被要求记入；仇慎仍称户灯旁证暂不作改账凭据。"}], "hooks": [{"fact_id": "chapter-0003-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线", "evidence": "灰雨蒙住院内；结尾明确一粒灰嵌进冷金印缝，随仇慎转身拖出暗红线。"}], "timeline": [{"fact_id": "chapter-0003-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "顾家折记继续暂缓，三日内再次复核", "after": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时", "evidence": "仇慎收走传核纸并宣布附录暂封，命明日辰时带顾家与守灯口述再来。"}], "physical_state": [{"fact_id": "chapter-0003-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "after": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑", "evidence": "识账后焦纹裂到颧骨；落笔签名时焦纹又往下裂一寸，黑屑掉在纸边。"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "before": null, "after": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感", "evidence": "印面擦过掌心后掌骨如干木掰裂；其后陆沉渊听见胸骨裂口随呼吸摩擦。"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": "识账后当场咳出一小片冷灰", "after": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印", "evidence": "陆沉渊识账后冷灰落在附录“未详”上；后又咳出冷灰，沾住传核纸边的衙印。"}, {"fact_id": "chapter-0003-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "after": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸", "evidence": "灰沾住传核纸衙印后印痕泛暗红，仇慎随即要求把那张纸留下。"}, {"fact_id": "chapter-0003-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "before": "灰粒落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄", "evidence": "验灯焰尖缩成细线，红点裂开渗冷光；仇慎最终明言“苏晚验灯不熄”。"}], "naming": []}}

## Prose
午后的太阳没有照进命籍衙后院。

院墙高，墙头压着一层发白的盐碱，日头落在外头，里头只剩一片薄薄的青光。陆沉渊站在命审台下，鞋底沾着泥灯巷的湿泥。泥里有细灰，踩开以后，灰粒便嵌进鞋纹，像一群不肯散去的小虫。

顾家的复核附录摊在台上。

纸角已经卷了，顾婶按过灯面的那一处，留着一圈不齐的油痕。补墨的灰屑被莫井兰从守灯架边刮来，装在一只缺口的小陶片里。陶片很薄，陆沉渊拿起来时，指腹能摸到里面粗糙的砂眼。

仇慎坐在台后，袖口压住半边册页。

“顾家折记，仍照原册。”他说，“附录只记作待核旁证，不改归属，不动征命数。”

顾婶被挡在院门外，只能隔着一条门缝看里面。她没有出声，手指紧紧拽着围裙。莫井兰站在她身后，背弯得更低，怀里抱着守灯用的旧布，布角缝线里还藏着些灰白细末。

陆沉渊看了一眼台上的纸。

“补墨灰痕，与户灯寿纹错位。”仇慎用指甲在那句话上划了一道，“你写得太实。”

“是我看见的。”

“你能看见灰，不能看见账。”仇慎抬眼，“把‘错位’二字换成‘未详’。”

“顾婶的命灯寿纹就在这里。”

“那也只能证明她的灯有过灼痕，不能证明是谁把年月添进了顾家的折记。”

仇慎说得很慢，每个字都像在纸面上钉下一枚小钉子。门外风一动，檐下的灯罩轻轻相碰，发出细碎的响。

陆沉渊没有去看顾婶。

他知道她在看自己。那目光很轻，却压得胸口发闷。

仇慎将一枚冷金小印放在台边。印面没有落下，先有寒气渗出来，纸上那圈油痕立即褪了颜色。顾婶的名字像被一只看不见的手从纸里往下按，墨线变得发灰。

“今日只做复核。”仇慎说，“不必把事情弄得像有人要翻衙门的桌子。”

“若换成未详，午后复核就只剩仇掌事一句话。”

“你也可以不签。”

仇慎从袖中抽出一张薄薄的传核纸，推到陆沉渊面前。纸上那道衙印正是昨夜沾过他咳出冷灰的印，边缘有一圈暗红，像未干的血。

“你不签，按拒验记。”仇慎道，“拒验的人，母子同户的灯先停一盏。”

外头忽然传来一声闷响。

不是雷。

泥灯巷的方向，灰从天上落了下来。

先是几粒，打在门槛上，发出极轻的沙声。随后檐角、墙根、石阶，全都蒙上一层白。风将灰送进院里，落在命审台上，落在那枚冷金小印旁边。

苏晚站在院门外。

她没有撑伞。灰粒落在她掌背上，针尖大的红点很快鼓起，像皮下埋了一粒烧红的砂。她的手背本来就冷，红点周围却没有温度，反而泛出一圈青白。

陆沉渊的视线在她手背上停了一下。

苏晚抬起眼，隔着灰雨看他。

那一眼没有催促。

她只把手慢慢收回袖中。

仇慎也看见了。他将冷金小印往前一推，印底磕到木台，发出清脆的一声。

“先验命灯。”

门外的小吏举起一盏薄铜验灯。灯焰贴着罩壁，颜色淡得近乎透明。苏晚伸手过去，焰尖在她指骨上停了停，立刻缩成一根细线。

仇慎翻开本地残页，目光掠过纸面。

“命灯失温，裂纹加深。”他说，“按午后复核规矩，须暂扣户灯旁证，等命籍衙补验。”

“那不是补验。”顾婶在门外说，“那是把我家灯先拆了，再问灯为什么不亮。”

小吏回头瞪她。

莫井兰伸手挡在顾婶身前，旧布从她臂弯滑下来，露出一截缝着铜丝的灯架。她没有往前，只低声道：“我能认那灰。”

仇慎盯着她。

“你认什么？”

“认它从哪盏灯边落下来的。”莫井兰说，“昨夜落灰时，泥灯巷西檐先响，顾家户灯没有熄，顾婶掌背却先红。今早补墨灰在册角，和灯里的灰不一个味。”

她说到这里，停了一下，喉咙里起了沙。

“灯灰有油味。册角的灰，凉，像浸过水。”

“你闻过天下所有灰？”

“没有。”莫井兰把旧布攥紧，“我只守过这一巷的灯。”

仇慎的手按在册页上，冷金小印的寒气顺着木台爬过来。陆沉渊看见那几粒灰在印边聚成一线，暗红的细纹一闪，像有人在纸底下用指甲刮了一下。

他不能看顾婶的个人命页。

也不能追那道灰痕去了哪里。

他能辨认的，只有眼前这点错位。

普通的寿纹，落在命灯铜片上时，会沿着灯骨自然分成三道。顾婶掌背的红点却只有两道细痕，其中一道断在腕骨之前。册角补墨里的灰屑，正好有一道弯折的黑线，断口朝向与她手背相反。

陆沉渊伸手，捏起陶片里一粒灰。

“把验灯移近。”

仇慎皱眉：“你还要识账？”

“只辨灰。”

“你刚才已经辨过。”

“刚才辨的是纸角。现在有新灰落下来。”

仇慎没有答应。

陆沉渊却已经将灰粒按在自己左眼下方。

灼痛在皮肤里炸开。

眼前的院子顿时褪成一片灰白。木台、册页、冷金小印，所有边缘都被细细的银灰火屑勾出轮廓。顾婶的验灯焰尖摇晃着，灯罩上浮出一圈极淡的红痕。那红痕不是从灯芯里生出的，像从灯罩外被擦进去，只有在靠近命籍衙印的地方才留下完整的一笔。

册角的补墨灰痕也亮了。

两边本该相接的纹路，中间隔着半指宽的空白。

那空白里没有寿火。

只有一层冷灰。

陆沉渊想再往里看，左眼忽然像被针从眼眶后面扎穿。银灰火屑猛地旋转起来，他的膝盖一软，手掌撑住命审台。

一口冷灰堵在喉咙里。

他咳出来时，灰落在附录最后一行，正盖住“未详”二字。

顾婶惊呼了一声。

仇慎的脸色变了。他抓起冷金小印，朝那口灰压下去。

陆沉渊抬手挡住。

印面擦过他的掌心，寒意顺着骨头钻入胸腔。掌骨深处传来一声细响，像干木被掰开一道缝。他眼前黑了半瞬，再睁眼时，左眼下方的焦纹已经裂到颧骨。

“让开。”仇慎说。

“印不能落在灰上。”

“这是衙印。”

“灰还没验完。”

“你有什么资格拦印？”

陆沉渊没有回答。他转身看向门外的莫井兰：“守灯婆，你认不认这粒灰？”

莫井兰没有立即伸手。

灰雨落在她头发上，落在眉毛上。她盯着陆沉渊掌心被冷金擦出的青白印痕，又看了一眼苏晚藏在袖里的手。

“我认。”她说。

“认它和顾家户灯里的旧灰同味？”

“同味。”

“认它不是顾家自己烧出来的？”

莫井兰的嘴唇动了动。

仇慎在台后冷声道：“想清楚再说。口述一旦入附录，便要留名。”

莫井兰望着门内那张薄纸。她没有看仇慎，反而问顾婶：“你愿意让我替你记吗？”

顾婶的手从袖中伸出来，红点已经暗下去，掌背冷得发青。

“记。”她说，“记我看见的。别替我添一句。”

莫井兰点头：“那就记，顾家户灯昨夜未灭，灰痕先落掌背；册角补墨灰凉而无油，断纹与户灯寿纹相反。至于是谁落的，我不知道。”

最后三个字落下，院中很静。

陆沉渊看着那粒灰。

这便够了。

它不能逼仇慎承认什么，也不能让顾家立刻改账。第三个人若来，只会看见一粒沾在附录上的冷灰，看见顾婶的红点，看见守灯老妇留下的口述，然后可以说灰是后来落的，红点是旧伤，口述是记错了。

可那些东西已经在同一张纸上。

灰与口述互相咬住了。

仇慎却将验灯朝苏晚推去。

“户灯旁证须先封存。”他说，“若不封，按私藏命证处理。苏晚的灯，也要暂熄一刻，等衙印重验。”

苏晚袖口微微一紧。

陆沉渊心里像被那句话剜开。

她的命灯不能再熄。

他低头看向附录。那口冷灰沾在“未详”上，潮气将墨洇开，黑字下露出一小截原本被补墨遮住的细线。细线很短，像有人在纸背写过一个“折”字，又被火燎断。

仇慎的冷金印已经举起。

落印，顾婶的旁证便会被封入衙册；不落印，苏晚的验灯会先灭。

陆沉渊把掌心贴上那枚冷金印。

寒气刺入胸骨。

“我签。”

苏晚猛地抬头：“沉渊。”

“只签传核。”

“签了就认拒验—”

“我认在场。”

他手指发抖，捡起笔。笔尖落下时，左眼的焦纹又往下裂了一寸，黑屑掉在纸边。他没有把灰抹开，任它压在“未详”两字上，随后在传核纸上写下自己的名字。

仇慎立即收走传核纸。

“顾家附录，暂封。”他说。

“口述呢？”陆沉渊问。

“随附录封存。”

“灰呢？”

仇慎看向陶片。

陆沉渊先一步将陶片推到莫井兰手边。

“灰是守灯见证物。封纸可以，灰不入衙。”

仇慎的冷金小印停在半空。

苏晚忽然咳了一声。

她从袖中取出一截白线，线头沾着灰，手背上的红点已经裂开，渗出的不是血，是一点暗暗的冷光。她把白线放在门槛上，向前推了半寸。

“这是我灯罩上的灰。”她说，“若要封，连我的一并封。若不封，就别拿一盏灯吓孩子。”

没有孩子在院里。

这话却让仇慎的手指缩了一下。

他看着苏晚，像第一次发现这盏失温的命灯并非只会等着别人替它说话。

门外，灰雨忽然密了。

屋檐下的灯罩一盏接一盏发出轻响。巷中护阵的旧纹隔着墙传来颤鸣，像一排疲惫的牙齿在寒里相碰。陆沉渊眼中的银灰火屑没有散，视野边缘一阵阵发黑。他扶着台角，听见胸骨里的裂口随着呼吸摩擦。

仇慎终于放下印。

“顾家附录封存，灰物由守灯人暂带，三日内随顾家复核再验。”他说，“苏晚验灯不熄，但户灯旁证暂不作改账凭据。”

这句话比先前更重。

它保住了一盏灯，也把追缴的手留在了门外。

陆沉渊按住喉咙，还是咳出了一片冷灰。灰落在自己的传核纸边，沾住那道衙印，印痕立刻泛出一圈极细的暗红。

仇慎看见了。

他的脸色一点点沉下去。

“把那张纸留下。”

陆沉渊用拇指压住灰，没有擦掉。

“按规矩，传核纸在我签名后归档。”

“你咳出的灰沾了衙印。”

“所以更该归档。”

两人的手隔着纸角僵住。

院门外，莫井兰把陶片塞进旧布的夹层。顾婶伸手扶住苏晚，苏晚却没有退，仍站在灰雨里看着陆沉渊。

她看见了他掌心的青白印。

也看见了他左眼下那道再也遮不住的焦黑裂纹。

陆沉渊知道她会问。

他也知道自己暂时不能说。

命审台上的冷金印忽然轻轻震了一下，像远处某个看不见的东西隔着层层命页，敲了一次门。

仇慎收回手，将印压回袖中。

“明日辰时，”他说，“带顾家与守灯口述再来。若缺一人，按拒验续记。若灰物有损，视同毁证。”

他顿了顿，目光落在陆沉渊沾灰的手掌上。

“你也来。”

灰雨越过门槛，落在传核纸、木台和每个人的鞋面上。没有一粒灰能证明谁动过账，却有一粒嵌进了冷金印的缝里，随着仇慎转身，拖出一道极细的暗红线。

陆沉渊看着那道线消失在袖口。

然后伸手，把苏晚藏在袖中的手握住。

她的掌心冷得像一块未点燃的灯芯。隔了片刻，才有一点微弱的温度回到他指缝间。

那点温度没有治好命灯上的裂纹。

也没有抹掉传核纸上的名字。

命籍衙后院的门在他们身后合上，门缝里仍有灰往外飘。明日辰时，仇慎会再把那张纸摊开，叫人逐粒称灰，逐句复述。

到那时，谁都可以说今天什么也没有发生。

可那道印缝里的暗红，已经先一步留下了自己的去处。

## Required JSON
```json
{
  "chapter_id": "chapter-0003",
  "artifact_kind": "draft",
  "artifact_sha256": "cb75a467d08b6e6c0b382b9e4a6bb53bb58a87ac4c386aa6eca633ddc1352022",
  "context_sha256": "2f0b64f42c16cecccac386afb8086bff999488fff8f303ddb34fbfed5d494903",
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
