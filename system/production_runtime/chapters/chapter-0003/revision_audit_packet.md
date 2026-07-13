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
午后的日头被命籍衙的高墙挡在外头，后院只剩一层发青的亮。

墙头盐碱发白，风从泥灯巷吹进来，带着湿泥和细灰。陆沉渊站在命审台下，鞋底的泥干了一半，灰粒嵌进鞋纹，踩一步，便有细小的砂声。

顾家的复核附录摊在台上。

纸角卷着，顾婶按过灯面的地方留下一圈油痕。莫井兰从守灯架边刮下的补墨灰，装在缺口陶片里。陶片薄得透光，陆沉渊捏着边缘，指腹能摸见里头粗砺的砂眼。

仇慎坐在台后，袖口压着半页残册。

“顾家折记，照原册留置。”他道，“附录可存，旁证可记，不改归属，不动征命数。”

顾婶被挡在院门外，手里攥着围裙，指节泛白。莫井兰站在她前头，背弯得低，怀中旧布裹着守灯架，布缝里还沾着灰白细末。

陆沉渊望着附录上那行字。

补墨灰痕，与户灯寿纹错位。

仇慎以指甲在纸上划过，停在“错位”二字上。

“改成未详。”

“我看见的不是未详。”

“你看见的是灰。”仇慎抬眼，“账，不是你能看的。”

“顾婶的命灯寿纹在这儿，补墨灰也在这儿。”

“所以才叫旁证。”仇慎说得很慢，“她的灯有灼痕，只能证明她的灯受过火。谁添了年月，谁落了灰，本地残页给不了定论。”

檐下灯罩被风碰了一下，叮的一声，很轻。

陆沉渊没有回头。他知道顾婶在看他。门缝里的目光不重，却压得他胸口发闷。

仇慎把一枚冷金小印放到木台边。

印还未落，寒气已经漫开。纸上那圈油痕被冻得发白，顾婶的名字像沉进了纸里。

“今日只是午后复核。”仇慎道，“别把一页附录闹成翻衙门的案子。”

“换成未详，附录就只剩掌事一句话。”

“你可以不签。”

一张传核纸被推到陆沉渊面前。

纸上的衙印边缘泛着暗红。昨夜他咳出的冷灰沾过这道印，颜色一直没有褪。

“拒验记。”仇慎道，“拒验者，母子同户的灯先停一盏。”

院外传来一阵细密的沙响。

灰落下来了。

先是几粒，打在门槛上。随后檐角、石阶、墙根一寸寸白下去。风卷着灰钻进后院，落在残册边，落在冷金小印旁。

苏晚站在门外。

她没撑伞。灰粒落在掌背，那里原先针尖大的红点慢慢鼓起，四周却泛着青白。她的手背本就失温，此时像握着一小块冰。

陆沉渊只看了一眼。

苏晚便把手收回袖中。

她没有催他，也没有替他说一句话。

仇慎却朝门外抬了抬下巴。

“先验命灯。”

薄铜验灯被举起。灯焰贴着罩壁，淡得近乎透明。苏晚伸出手，焰尖碰到她指骨，立刻缩成一线。

仇慎翻开残页。

“命灯失温，裂纹见深。”他说，“按规矩，顾家户灯旁证暂扣，待衙内补验。苏晚的灯，也须留验。”

“留验？”顾婶在门外开口，嗓子发紧，“你们拆了我家的灯，再问它为什么不亮，这也叫验？”

莫井兰抬臂挡住她。

旧布滑下一角，露出缝了铜丝的灯架。莫井兰没往前迈，只盯着台上的陶片。

“我认那灰。”

仇慎看向她：“你认什么？”

“认它从哪种灯边落下来。”莫井兰道，“昨夜泥灯巷西檐先响，顾家户灯没熄，顾婶掌背却先红。今早册角补墨的灰，和灯里的灰不是一个味。”

她咽了一下，喉咙里像磨着砂。

“灯灰有油气。册角这灰凉，像浸过水。”

“你闻过天下所有灰？”

“没有。”莫井兰把旧布攥得更紧，“我只守过这一巷的灯。”

冷金印边，那几粒灰被寒气逼成一线。暗红细纹在纸面一闪，像纸底有人用指甲刮过。

陆沉渊不能看任何人的命页。

更不能顺着灰痕追它来处。

眼前能认的，只有命灯铜片上的寿纹、册角补墨的灰线，以及新落下来的这些灰。

顾婶掌背那点红痕，沿着腕骨只分出两道细线，其中一道半途断了。册角灰屑里也有一道折弯的黑线，断口却朝着相反的方向。

“把验灯移近。”陆沉渊道。

仇慎皱眉：“你还要识账？”

“只辨灰。”

“你已经辨过一次。”

“先前辨纸角。如今有新灰。”

仇慎没有动。

陆沉渊取了一粒灰，按到左眼下。

灼痛猛地炸开。

后院褪成灰白。木台、残册、印面，全被银灰火屑勾出模糊的边。验灯罩壁浮起一圈浅红，那红痕不是自灯芯里生出的，像从外头擦进去，靠近衙印时才留下一笔完整的轮廓。

册角补墨也亮起来。

两道纹路本该相接，中间却隔着半指宽的空白。

空白里没有寿火，只有冷灰。

陆沉渊想再看一寸，左眼忽然像被针从眼眶后扎穿。他膝盖一软，掌心撑住木台。

冷灰堵在喉间。

他咳出来时，灰正落在附录最后一行，盖住“未详”二字。

仇慎脸色一沉，抓起冷金印便压。

陆沉渊抬手拦住。

印面擦过掌心，寒气直钻进骨头。掌骨里响起细碎一声，像干木裂开。左眼下的焦纹随之崩到颧骨，黑屑擦落在纸边。

“让开。”仇慎道。

“印不能先落。”

“这是衙印。”

“灰还没验完。”

“你拿什么拦？”

陆沉渊转向门外：“守灯婆，这粒灰，你认不认？”

莫井兰没有马上伸手。

灰雨落在她发间。她看过陆沉渊掌心的青白印痕，又看了眼苏晚藏在袖中的手。

“我认。”

“认它和顾家户灯里的旧灰同味？”

“同味。”

“认它不是顾家自己烧出来的？”

莫井兰嘴唇动了动。

仇慎冷声道：“口述入附录，要留名。想清楚。”

莫井兰却先问顾婶：“你愿意我替你记？”

顾婶伸出手。她掌背的红点已暗下去，皮肤青得发冷。

“记我看见的。”她说，“别替我添。”

莫井兰点头：“顾家户灯昨夜未灭，灰痕先落掌背；册角补墨灰凉而无油，断纹与户灯寿纹相反。至于是谁落的，我不知道。”

院里静了下来。

这几句话不能改账，也不能让仇慎认错。旁人再来，大可以说灰是后来落的，红点是旧伤，守灯人记错了时辰。

可灰、灯、口述，此刻都压在一张附录上。

仇慎把验灯往苏晚方向推了推。

“旁证既要封存，苏晚的灯也该暂熄一刻，等衙印重验。”

苏晚袖口一紧。

陆沉渊低头看着纸上那口灰。潮气洇开墨色，“未详”底下露出一截被补墨遮过的细线，像一个写到半途、又被火燎断的“折”字。

冷金印已举在半空。

落下去，顾婶的旁证便会被锁进衙册；不落，苏晚的验灯先灭。

陆沉渊把掌心覆到印上。

寒气刺进胸骨，他呼吸一滞，眼前的银灰火屑几乎熄尽。

“我签。”

苏晚猛地抬头：“沉渊。”

“只签传核。”

“签了，他们会按拒验记。”

“我认在场。”

他的手抖得厉害，仍捡起笔，在传核纸上落下名字。黑屑从眼角掉下来，混进纸边的灰里。他没有把“未详”上的冷灰擦去。

仇慎立刻收走传核纸。

“顾家附录，暂封。”

“口述。”陆沉渊道。

“随附录封存。”

“陶片里的灰。”

仇慎看向那只缺口陶片。

陆沉渊先将陶片推到莫井兰手边：“守灯见证物，不入衙。”

冷金印停在半空。

苏晚忽然咳了一声。

她从袖中抽出一截白线，线头沾灰，掌背的红点裂开，渗出的不是血，而是一点暗淡的冷光。她把白线放到门槛上，推向院内。

“这是我灯罩上的灰。”她道，“要封，连我的一并封。若不封，就别拿一盏灯吓人。”

仇慎盯着那根白线，手指缩了一下。

门外的灰雨更密。巷中护阵的旧纹隔墙传来颤鸣，像一排牙齿在寒里相撞。陆沉渊扶着台角，胸骨深处那道裂口随呼吸磨着，喉间又泛起冷腥。

仇慎终于放下印。

“顾家附录封存。灰物由守灯人暂带，明日辰时随顾家复核再验。”他道，“苏晚验灯不熄，户灯旁证暂不作改账凭据。”

顾婶闭了闭眼。

陆沉渊按住喉咙，还是咳出一片冷灰。灰落在传核纸边，沾住那道衙印，印痕立刻漫开极细的一圈暗红。

仇慎看见了。

“纸留下。”

陆沉渊用拇指压住那片灰，没有擦。

“签后归档。”

“你的灰沾了衙印。”

“所以更该归档。”

两只手隔着纸角僵住。

门外，莫井兰把陶片塞回旧布夹层。顾婶伸手扶住苏晚，苏晚却没有退。她看着陆沉渊掌心的青白印，看着他左眼下裂到颧骨的焦纹，脸色比灰更白。

冷金印在仇慎袖中轻轻震了一下。

仇慎收回手，压住印。

“明日辰时，顾家与守灯口述都来。缺一人，按拒验续记。灰物有损，视同毁证。”

他的目光落到陆沉渊沾灰的手上。

“你也来。”

灰越过门槛，落在纸上，落在每个人鞋面。没有一粒灰能当场指认谁动过账，可有一粒已经嵌进冷金印的缝里。

仇慎转身时，印缝拖出一道极细的暗红线。

陆沉渊看着那线没入袖口，才伸手握住苏晚的手。

她掌心冷得像未点燃的灯芯。过了很久，才有一点微弱的温度回到他指缝间。

那点温度没合上命灯裂纹，也没抹掉传核纸上的名字。

后院门在身后合拢，门缝里仍有灰往外飘。

明日辰时，那张纸还会摊开。灰要逐粒验，话要逐句复述。谁都可以说今日什么也没有发生。

可冷金印的缝里，已经留下了一道不肯褪的暗红。

## Required JSON
```json
{
  "chapter_id": "chapter-0003",
  "artifact_kind": "revision",
  "artifact_sha256": "8167366cd6811f13f63105eb5e0644bccb5c069e6081e29e4a66150554158b3f",
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
