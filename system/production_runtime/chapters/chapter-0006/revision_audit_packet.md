# NRL Antigravity Chapter Audit v0.20

Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.
Do not use terminal tools, inspect files, run tests, make a plan, or wait for background work. The complete review packet is inline.
Do not rewrite prose. Return one JSON object only using the exact binding hashes, with no Markdown fence or surrounding text.

## Compact Context
{"chapter_id": "chapter-0006", "dramatic_purpose": "母亲的命灯余波迫使主角放弃一次安全选择，换取不伤及邻里的有限证据保全。", "must_keep": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "亲缘选择不许以第三方寿火代偿。"], "must_avoid": ["不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"], "assets": [{"asset_id": "character_lu_chenyuan", "display_name": "陆沉渊", "family": "characters", "lifecycle_state": "active", "constraints": ["Does not transfer a life-cost to uninvolved residents.", "Each use leaves bodily evidence or increases pursuit risk.", "His mother debt and the lane protection array remain non-negotiable constraints.", "At 燃命境初成 he may only recognize ordinary life marks and local ash-trace mismatches; personal-page reading, chain tracing, covenant glimpses, return-fire casting, and seal breaking remain blocked pending validated advancement."], "relationships": [{"target_id": "bond_mother_su_wan", "relation_type": "son_bound_by_lifespan_debt"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_acquire_after_registered_transition"}, {"target_id": "faction_mudlamp_lane", "relation_type": "protects_and_is_bound_to"}, {"target_id": "technique_embertrace_return", "relation_type": "may_unlock_after_lamp_and_progression_gates"}, {"target_id": "technique_ledger_recognition", "relation_type": "uses_basic_local_ash_trace_scope_of"}]}, {"asset_id": "npc_su_wan", "display_name": "苏晚", "family": "npcs", "lifecycle_state": "active", "constraints": ["苏晚是能拒绝错误救法的行动者，不是可消耗的动机。", "她绝不接受以邻里命火、孩童寿数或无辜者命页抵消自己的寿债。", "她的命灯裂纹、冷灰气息和掌背失温须以感官后果呈现，不以抽象说明替代。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "bond_mother_su_wan", "relation_type": "embodies"}, {"target_id": "faction_mudlamp_lane", "relation_type": "mutual_aid_member_of"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "raises_restraint_threshold_for"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "is_counted_down_by"}]}, {"asset_id": "npc_registrar_qiu_shen", "display_name": "仇慎", "family": "npcs", "lifecycle_state": "active", "constraints": ["仇慎只能掌握本地残页与寿印权限，不能成为无所不知的阴谋解释者。", "其每一次施印必须留下可辨的冷金印痕或命灯失色，并制造可追责的现场后果。", "他可恐惧上级追责，但不能因恐惧自动洗白。", "其独立义务是保住本地呈印资格并避免州府问责；当公开证据使继续施印超出本地权限时，可拖延、议价或退回追缴令，但不得因此获得无证据洗白。"], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "serves_as_registrar_for"}, {"target_id": "character_lu_chenyuan", "relation_type": "supervises_and_targets"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "forwards_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "pressures_with_seals"}]}, {"asset_id": "npc_mo_jinglan", "display_name": "莫井兰", "family": "npcs", "lifecycle_state": "active", "constraints": ["Her knowledge is partial oral memory, never omniscient exposition.", "Helping preserve testimony exposes her remaining life-fire to collection."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "keeps_its_night_lamps"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "witnesses_surface_sign"}]}, {"asset_id": "bond_mother_su_wan", "display_name": "苏晚与陆沉渊的垫寿亲缘", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["The mother is an active moral presence, not expendable motivation.", "Any attempt to relieve her debt must carry an exposure, bodily, or communal consequence."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "deadline_is_tracked_by"}]}, {"asset_id": "bond_mudlamp_lane_trust", "display_name": "泥灯巷共灯之信", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["共同体信任不是主角可提取的资源；巷民有拒绝、质询和撤回见证的权利。", "信任提升必须来自共同承担、返还寿火或公开承担反噬，而非主角单方面胜利。", "任何高风险行动都须显示巷民的恐惧、选择与实际保护行为。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "binds_to_community"}, {"target_id": "faction_mudlamp_lane", "relation_type": "measures_mutual_aid_of"}, {"target_id": "npc_su_wan", "relation_type": "is_guarded_by_moral_boundary_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "conditions_witnessed_return"}]}, {"asset_id": "faction_mudlamp_lane", "display_name": "泥灯巷", "family": "factions", "lifecycle_state": "active", "constraints": ["The mutual-aid network cannot become expendable fuel for a single hero.", "Every communal protection act worsens the protection array's visible lifespan cracks or attracts collectors."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "contains_registered_acquisition_site_for"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "is_tracked_by"}]}, {"asset_id": "faction_life_registry_office", "display_name": "命籍衙", "family": "factions", "lifecycle_state": "active", "constraints": ["其压迫必须通过寿印、命灯、命审台和具体家庭后果显形，不写成现实机构讽刺。", "本地权限只能冻结、登记、送审与申请追缴，不能解释州府或天庭的完整真相。", "命审程序必须成为可被证据、见证和法术反打的冲突场域。"], "relationships": [{"target_id": "npc_registrar_qiu_shen", "relation_type": "employs"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "issues_local_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "assesses_and_pressures"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "contests"}]}, {"asset_id": "technique_ledger_recognition", "display_name": "识账术", "family": "techniques", "lifecycle_state": "active", "constraints": ["At character_lu_chenyuan's current 燃命境初成 stage, the active scope is limited to ordinary life marks and local copy-level ash-trace mismatches visible in the present evidence.", "Personal-page reading is locked to a validated 识账境 transition; chain tracing requires a later audited proof, and ancient-covenant glimpses remain blocked until an independently validated advanced transition and artifact evidence exist.", "The technique cannot directly read minds, predict outcomes, or produce a complete answer at any stage.", "施展后瞳孔浮出焦黑纹路、视野残留银灰火屑，并提升被寿印锁定的风险。", "所有判断须由可见痕迹或受害者见证复核，不能以主角独白定案。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "is_practiced_by"}, {"target_id": "technique_embertrace_return", "relation_type": "verifies_targets_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "increases"}, {"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "cannot_reveal_before_validated_advanced_progression"}]}, {"asset_id": "foreshadowing_cinder_seal_rain", "display_name": "灰雨印痕", "family": "foreshadowing", "lifecycle_state": "active", "constraints": ["The clue appears as sensory supernatural residue, not paperwork.", "Investigating it burns the investigator and raises collection exposure before any revelation."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "is_revealed_by"}, {"target_id": "npc_mo_jinglan", "relation_type": "is_remembered_by"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "payoff_tracks"}]}, {"asset_id": "state_ledger_protagonist_strain", "display_name": "陆沉渊命火与心魄承压", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["状态只记录可叙事化的命火、骨裂、瞳纹、冷灰与心魄恍惚，读者文本不得呈现工程字段。", "任何恢复都不能自动解除母亲寿债、半寿身份或既有追缴。", "承压过界时主角应失去施术窗口或需要他人阻止，而非获得无代价爆发。", "空寿状态是施术锁定与认知承压：不得提升战力；继续行动必须先支付已登记的寿火扣减，并失去至少一个施术或判断能力，恢复须停术和外部看护。", "This asset is the sole writer of sanity_level, caster_lifefire_stability, bone_fissure_severity, eye_pattern_burn, and cold_ash_cough_frequency; it may not write exposure or mother-lamp state."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "tracks_strain_for"}, {"target_id": "technique_ledger_recognition", "relation_type": "is_decreased_by"}, {"target_id": "technique_chain_deflection_seal_breaking", "relation_type": "is_worsened_by"}, {"target_id": "bond_mother_su_wan", "relation_type": "raises_family_risk_for"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_half_life_registry_exposure", "display_name": "半寿残籍暴露", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of half_life_registry_exposure; techniques, artifacts, NPCs, and other ledgers may request a delta but may not write the value directly.", "Exposure never decreases merely because evidence succeeds or life-fire returns; reduction requires a separately evidenced legal, masking, or withdrawal transition.", "Threshold crossings must change pursuit or access state before the atomic transaction can close.", "The Cluster 5 evidence-record exchange requests exactly +10 percentage points within the 0-100 bound and closes only with the protagonist-owned record debit under the same transaction ID; child, resident, and third-party life-fire prices are rejected."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "solely_tracks_registry_exposure_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "npc_cluster5_black_market_transaction_role", "relation_type": "is_increased_by_transaction_with"}]}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "display_name": "苏晚命灯裂纹倒计时", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mother_life_lamp_cracks and the mother-life-debt countdown.", "A communal return or protagonist recovery cannot automatically heal a crack or cancel the unresolved mother debt.", "Any technique transaction that affects Su Wan must record the crack/countdown delta here before closing."], "relationships": [{"target_id": "npc_su_wan", "relation_type": "solely_tracks_lamp_cracks_for"}, {"target_id": "bond_mother_su_wan", "relation_type": "provides_countdown_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "cannot_be_auto_cancelled_by"}]}, {"asset_id": "state_ledger_mudlamp_array_integrity", "display_name": "泥灯巷护阵完整度", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mudlamp_array_integrity; returned fire, resident reserve, and caster strain remain independently owned.", "Array integrity cannot rise from returned fire alone; witnessed repair or stabilization must be recorded.", "Below the registered safety line, lamp activation and return-fire casting fail closed rather than granting emergency power."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_array_integrity_for"}, {"target_id": "artifact_ashlight_cup", "relation_type": "gates_acquisition_and_activation_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_resident_lifefire_reserve", "display_name": "泥灯巷住户命火储备", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of resident_lifefire_reserve; the reserve is never protagonist inventory or an automatic communal resource.", "Every debit requires named consent and preserves the right to refuse or withdraw before transaction closure.", "No black-market price, technique cost, or artifact awakening may debit children, uninvolved residents, or an unspecified crowd."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_consented_reserve_for"}, {"target_id": "bond_mudlamp_lane_trust", "relation_type": "requires_refusal_and_consent_rights_from"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_supply_consented_watchfire_for_awakening"}]}, {"asset_id": "state_ledger_poorcity_returnfire", "display_name": "泥灯巷归火余量", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["A positive return never cancels the mother debt or the protection array burden automatically.", "Every gain must name whose life-fire returned and whose visible backlash or exposure increased.", "This asset is the sole writer of returned_miscollected_lifefire and may not write caster strain, registry exposure, array integrity, resident reserve, or mother-lamp state."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "measures_survival_pressure_for"}, {"target_id": "technique_embertrace_return", "relation_type": "is_changed_by"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_affected"}]}, {"asset_id": "state_ledger_revealed_account_errors", "display_name": "已揭示错账记录", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of revealed_account_errors; evidence, return-fire, and outline assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source evidence and at least one independently owned return-fire, exposure, reputation, pressure, or mystery consequence.", "No inferred or unverified account error may be counted, and no proof may create an implicit credit or debit."], "relationships": [{"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_faction_pressure", "display_name": "既有势力压力", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of faction_pressure; faction, NPC, and scene assets may request but may not apply a mutation.", "Every mutation must identify an existing source asset and settle atomically with exposure, public reputation, or revealed-error consequences.", "No new faction, location, or plot event may be created to justify a pressure change."], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "faction_prefecture_life_treasury", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_public_reputation", "display_name": "公开认知状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of public_reputation; all other assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source, reason, before/after state, and at least one independently owned consequence ledger.", "No success, witness, or exposure event changes reputation implicitly or closes without its peer ledger result."], "relationships": [{"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_unresolved_mysteries", "display_name": "未解账目疑点", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of unresolved_mysteries; foreshadowing and outline assets may request but may not apply a mutation.", "Every add, reclassification, or closure requires an explicit atomic transaction with a revealed-error or map-boundary consequence.", "No new mystery, answer, backstory, or plot event may be created by this ledger."], "relationships": [{"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "tracks_only_registered_questions_from"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_map_unlock_status", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_map_unlock_status", "display_name": "既有地图边界解锁状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of map_unlock_status; references to existing map boundaries may request but may not apply a transition.", "Every transition is atomic and must preserve unresolved boundaries while recording any exposure consequence.", "The ledger cannot introduce a location or unlock a boundary absent from the canonical outline."], "relationships": [{"target_id": "artifact_prefecture_transit_registry_seal", "relation_type": "requires_validated_boundary_evidence_from"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}], "prior_settlements": [{"chapter_id": "chapter-0001", "accepted_revision_sha256": "79d46dc564388fc32d8bae5b8fdc5ebd7a3dc2412e2174f8558844cad1fda874", "state_deltas": [{"fact_id": "chapter-0001-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": null, "after": "顾家的折记暂缓，午后再核"}, {"fact_id": "chapter-0001-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.local_enforcement_status", "operation": "set", "before": "顾家折记待按册落印核验", "after": "顾家折记暂缓至午后复核"}, {"fact_id": "chapter-0001-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": null, "after": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索"}, {"fact_id": "chapter-0001-information-foreshadowing-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨印痕未在本章现场显现", "after": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小"}, {"fact_id": "chapter-0001-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "寿籍司尚未进入泥灯巷核验", "after": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后"}, {"fact_id": "chapter-0001-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "眼尾仅有极淡、藏在睫毛下的焦黑细纹", "after": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0002", "accepted_revision_sha256": "356320d82944a61555f663908889d71d0afff3c35b5fa3c0ede592ef0ecfaeaf", "state_deltas": [{"fact_id": "chapter-0002-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家的折记暂缓，午后再核", "after": "顾家折记继续暂缓，三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后", "after": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.procedural_observation_of_lu_chenyuan", "before": null, "after": "陆沉渊被要求往后残籍复核在场；传核缺席按拒验记", "operation": "set"}, {"fact_id": "chapter-0002-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "operation": "set"}, {"fact_id": "chapter-0002-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": null, "after": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "operation": "set"}, {"fact_id": "chapter-0002-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "顾家“折三”补墨与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "错位线索被记为本地复核附录，但不作为改账依据", "operation": "set"}, {"fact_id": "chapter-0002-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小", "after": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "operation": "set"}, {"fact_id": "chapter-0002-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": null, "after": "顾家折记三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩", "after": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": null, "after": "识账后当场咳出一小片冷灰", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": null, "after": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "operation": "set"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0003", "accepted_revision_sha256": "8167366cd6811f13f63105eb5e0644bccb5c069e6081e29e4a66150554158b3f", "state_deltas": [{"fact_id": "chapter-0003-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "被要求往后残籍复核在场；传核缺席按拒验记", "after": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来"}, {"fact_id": "chapter-0003-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄"}, {"fact_id": "chapter-0003-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_witness_material", "operation": "set", "before": null, "after": "暂带顾家补墨灰屑陶片作为守灯见证物"}, {"fact_id": "chapter-0003-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_local_lamp_assessment", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "验灯显示命灯失温、焰尖缩成细线，手背红点裂开并渗出暗冷光"}, {"fact_id": "chapter-0003-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "after": "顾家附录暂封并列入三日内再验，苏晚户灯旁证暂不作改账凭据"}, {"fact_id": "chapter-0003-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "顾家折记三日内再次复核", "after": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证"}, {"fact_id": "chapter-0003-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "after": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔"}, {"fact_id": "chapter-0003-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "after": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界"}, {"fact_id": "chapter-0003-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "陆沉渊每次施术的反噬尚未被苏晚在本次复核中当场看见", "after": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹"}, {"fact_id": "chapter-0003-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "错位线索被记为本地复核附录，但不作为改账依据", "after": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据"}, {"fact_id": "chapter-0003-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线"}, {"fact_id": "chapter-0003-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "after": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": null, "after": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "识账后当场咳出一小片冷灰", "after": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印"}, {"fact_id": "chapter-0003-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "after": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸"}, {"fact_id": "chapter-0003-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "operation": "set", "before": "灰粒落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0004", "accepted_revision_sha256": "e3ed91078715d2b3540da38987cb7db63bcd559ea1e320fb0b07a550d091b6f7", "state_deltas": [{"fact_id": "chapter-0004-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_intent", "operation": "set", "before": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来", "after": "确认明日辰时到场，但不替任何住户陈述未亲见之事"}, {"fact_id": "chapter-0004-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "operation": "set", "before": "暂带顾家补墨灰屑陶片作为守灯见证物", "after": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句"}, {"fact_id": "chapter-0004-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_refusal_statement", "operation": "set", "before": null, "after": "拒绝以自己抵命，也拒绝以泥灯巷住户命火填补自身裂纹"}, {"fact_id": "chapter-0004-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.latest_local_notice", "operation": "set", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席"}, {"fact_id": "chapter-0004-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "operation": "set", "before": null, "after": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩"}, {"fact_id": "chapter-0004-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证", "after": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记"}, {"fact_id": "chapter-0004-faction-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "operation": "set", "before": null, "after": "未有住户命火实际投入巷口泥灯；住户保留各自关门、留缝或守灯的选择"}, {"fact_id": "chapter-0004-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔", "after": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展"}, {"fact_id": "chapter-0004-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界", "after": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片"}, {"fact_id": "chapter-0004-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线", "after": "巷口泥灯罩内壁留下不下沉的黑点；薄纸上的冷灰沿纸纤维聚成空白，避开命籍衙印落点"}, {"fact_id": "chapter-0004-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时", "after": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑", "after": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印", "after": "本次夜间识账后再次咳出冷灰，落在巷口泥地"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感", "after": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0005", "accepted_revision_sha256": "f627dd586df7aa3238d6722148adf34f5bf1c4efaf29f254344d138e31525aaa", "state_deltas": [{"fact_id": "chapter-0005-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "确认明日辰时到场，但不替任何住户陈述未亲见之事", "after": "已到场完成本地复核，并被要求午后护阵旁观重验继续在场；凡本地残页复核不得缺席"}, {"fact_id": "chapter-0005-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "顾家附录继续封存；守灯前三句保留，未知来源不入；护阵旁观追加残页改列次序待核"}, {"fact_id": "chapter-0005-npc-registrar-qiu-shen-002", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_local_notice", "operation": "set", "before": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席", "after": "已发出今日午后泥灯巷护阵旁观落点重验通知，并列明顾家户灯留衙、莫井兰携陶片、陆沉渊到场的条件"}, {"fact_id": "chapter-0005-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "operation": "set", "before": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句", "after": "已在复核中陈述顾家旧灰、补墨灰凉无油及断纹相反三句；陶片仍暂带，午后须携带在场"}, {"fact_id": "chapter-0005-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "operation": "set", "before": null, "after": "午后可拒绝验灯，但不得替陆沉渊认灰"}, {"fact_id": "chapter-0005-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "operation": "set", "before": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩", "after": "护阵旁观落点被列为今日午后重验对象，尚未完成复核或修补"}, {"fact_id": "chapter-0005-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "after": "辰时复核已完成并将护阵旁观追加残页列为次序待核；午后转入泥灯巷重验监督"}, {"fact_id": "chapter-0005-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记", "after": "今日午后在泥灯巷重验护阵旁观落点；顾家户灯留衙至验毕，莫井兰携陶片、陆沉渊到场，人或物缺一按拒验续记"}, {"fact_id": "chapter-0005-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展", "after": "顾家附录补墨灰位于冷金印下；护阵旁观残页署时旁灰浮在墨上且被冷金截断，右页存在无法与“昨夜追加”同时自证的局部次序"}, {"fact_id": "chapter-0005-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片", "after": "莫井兰保留前三句限于所见的陈述，拒绝补入未知来源；午后继续以暂带陶片的限定方式到场"}, {"fact_id": "chapter-0005-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹", "after": "苏晚在识账反噬中按住陆沉渊腕上发抖的手，未替他认灰或触碰残页"}, {"fact_id": "chapter-0005-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据", "after": "护阵旁观追加残页被确认存在局部次序疑处，列为待核；未被认定为顾家折记错误、护阵追加无效或改时原因的证明"}, {"fact_id": "chapter-0005-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "after": "辰时复核后，程序推进至今日午后的泥灯巷护阵旁观落点重验"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑", "after": "识账时左眼下焦纹沿颧骨再绽开一小截，皮肉现烧焦气味并落下黑屑；银灰火屑未散"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "本次夜间识账后再次咳出冷灰，落在巷口泥地", "after": "本次识账后咳出冷灰落在命审台角，并被冷金小印压入在场认痕"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声", "after": "薄纸衙印牵动掌心旧印后掌骨再响，胸口裂口感骤紧，需扶住台沿喘息"}, {"fact_id": "chapter-0005-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸", "after": "识账所咳冷灰被冷金小印压入在场认痕，薄纸衙印牵出暗红印线锁到陆沉渊掌心旧印"}], "resolved_audit_ids": []}]}

## Rule Stack
{"version": "0.22", "chapter_id": "chapter-0006", "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "priority_order": ["safety_and_originality", "canonical_story_bible", "volume_outline", "accepted_state_settlements", "creation_asset_constraints", "chapter_must_keep_and_must_avoid", "anti_ai_style_evidence"], "hard_rules": ["no source-work names, scenes, signature systems, or prose imitation", "no untracked power, relationship, location, item, or timeline changes", "all benefits carry an embodied, relational, or systemic cost", "reader-facing prose contains no runtime or database vocabulary", "不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "chapter_rules": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "亲缘选择不许以第三方寿火代偿。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"]}

## Compilation Trace
{"version": "0.22", "chapter_id": "chapter-0006", "selected_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "explicit_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "dependency_asset_ids": [], "excluded_asset_count": 22, "selection_reason": "explicit chapter intent requirements plus atomic transaction peers", "canonical_hashes": {"borrowed_heaven_life_account_bible": "81575478a441852f18d451e9967245bbfce11d60cddd3af24e9b6565955e0604", "borrowed_heaven_volume1_outline_tree": "1f12fe8ad3262876eb533d40c94ad02abb90b95b38de387d339917fce9184648", "project_assets.v0.2": "90dbcf17d769e8a985fc87880a4382018c30133a2a53f82c3826636c8ed1dc61"}, "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "prior_settlement_count": 5}

## Observed Facts
{"chapter_id": "chapter-0006", "draft_sha256": "fbd98d4e786e91923d703b47eef9fa8f45b718916af68a336ef1582fb5db28e1", "facts": {"characters": [{"fact_id": "chapter-0006-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "before": "已到场完成本地复核，并被要求午后护阵旁观重验继续在场；凡本地残页复核不得缺席", "after": "午后重验中以自身在场认痕换取陶片不入衙封；明日卯前新的监督追缴仍须在场", "evidence": "陆沉渊提出“陶片不入封”，仇慎随后称“暂由守灯者携带”；末尾通知“陆沉渊须在”。"}], "npcs": [{"fact_id": "chapter-0006-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家附录继续封存；守灯前三句保留，未知来源不入；护阵旁观追加残页改列次序待核", "after": "本地残页暂不改；护阵旁观落点保留“灰痕不同”记载，顾家附录继续封", "evidence": "仇慎结论为“本地残页暂不改。护阵旁观落点，保留灰痕不同的记载。顾家附录继续封”。"}, {"fact_id": "chapter-0006-npc-registrar-qiu-shen-002", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_local_notice", "before": "已发出今日午后泥灯巷护阵旁观落点重验通知，并列明顾家户灯留衙、莫井兰携陶片、陆沉渊到场的条件", "after": "明日卯前送达新的监督追缴纸；陆沉渊与莫井兰携陶片须在，顾家户灯仍留衙，苏晚可拒绝验灯但拒绝续记", "evidence": "仇慎称“明日卯前，命籍衙会送新的追缴纸……陆沉渊须在。莫井兰携陶片在。顾家户灯仍留衙。苏晚可拒绝验灯，拒绝便续记”。"}, {"fact_id": "chapter-0006-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "before": "已在复核中陈述顾家旧灰、补墨灰凉无油及断纹相反三句；陶片仍暂带，午后须携带在场", "after": "午后仅见证陶片旧墨边浮灰与薄纸新字上压灰；陶片继续由其携带并须在下一次监督到场", "evidence": "莫井兰说“陶片上的灰，我看着是浮在旧墨边。薄纸上的，我看着压着新字”；仇慎规定陶片“暂由守灯者携带，下一次监督仍须到场”。"}, {"fact_id": "chapter-0006-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "before": "午后可拒绝验灯，但不得替陆沉渊认灰", "after": "下一次监督仍可拒绝验灯；拒绝将被续记", "evidence": "仇慎通知“苏晚可拒绝验灯，拒绝便续记”。"}], "locations": [], "factions": [{"fact_id": "chapter-0006-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "辰时复核已完成并将护阵旁观追加残页列为次序待核；午后转入泥灯巷重验监督", "after": "午后落点重验结束；本地残页暂不改，程序推进至明日卯前的本地监督追缴", "evidence": "仇慎完成午后记载处理后，明言“明日卯前，命籍衙会送新的追缴纸……不是改账，是监督”。"}, {"fact_id": "chapter-0006-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": "今日午后在泥灯巷重验护阵旁观落点；顾家户灯留衙至验毕，莫井兰携陶片、陆沉渊到场，人或物缺一按拒验续记", "after": "明日卯前送达新的本地监督追缴纸；陆沉渊、莫井兰与陶片须在，顾家户灯仍留衙，苏晚拒绝验灯则续记", "evidence": "仇慎临走前逐项说明明日监督的到场、留衙和拒验续记条件。"}, {"fact_id": "chapter-0006-faction-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "before": "护阵旁观落点被列为今日午后重验对象，尚未完成复核或修补", "after": "重验后泥灯焰尖缩至几乎只剩火星，灯座旧砖出现细微爆裂声，墙上护阵纹闪后熄回", "evidence": "陆沉渊识账与冷金印落下后，泥灯两度缩焰；末段写旧砖爆裂、护阵纹闪后熄回，泥灯只余火星。"}], "artifacts": [], "techniques": [{"fact_id": "chapter-0006-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "顾家附录补墨灰位于冷金印下；护阵旁观残页署时旁灰浮在墨上且被冷金截断，右页存在无法与“昨夜追加”同时自证的局部次序", "after": "泥灯裂缝灰在护阵纹前断开；薄纸署时旁灰压在字墨上；陶片补墨灰浮于旧墨边，三处落灰不同", "evidence": "陆沉渊识账后逐项陈述三处灰痕；莫井兰仅复核陶片灰浮在旧墨边、薄纸灰压着新字。"}], "relationships": [{"fact_id": "chapter-0006-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": "莫井兰保留前三句限于所见的陈述，拒绝补入未知来源；午后继续以暂带陶片的限定方式到场", "after": "莫井兰同意只当面观察陆沉渊所认三处灰痕，不替其担保结论；陶片继续由其自行携带", "evidence": "陆沉渊说明她“只需看我说的三处是不是当着你的面”；莫井兰答“我看。我不保你说的对”。"}, {"fact_id": "chapter-0006-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "before": "苏晚在识账反噬中按住陆沉渊腕上发抖的手，未替他认灰或触碰残页", "after": "苏晚再次看见并直接扶住陆沉渊识账后的失衡，但未碰冷金印或陶片", "evidence": "陆沉渊咳灰、眼前发黑后，苏晚按住其后背撑住他；正文明确她“没有碰印，没有碰陶片”。"}], "emotions": [], "information": [{"fact_id": "chapter-0006-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "护阵旁观追加残页被确认存在局部次序疑处，列为待核；未被认定为顾家折记错误、护阵追加无效或改时原因的证明", "after": "本地记录保留泥灯裂缝、薄纸署时与陶片补墨三处灰痕不同；仍未作为改账、追加原因或顾家折记处理的证明", "evidence": "陆沉渊明确“三处落灰不同”，并说明“说明不了谁改账，说明不了为什么追加，也说明不了顾家折记该怎么改”；仇慎保留该记载且称本地残页暂不改。"}], "hooks": [{"fact_id": "chapter-0006-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "巷口泥灯罩内壁留下不下沉的黑点；薄纸上的冷灰沿纸纤维聚成空白，避开命籍衙印落点", "after": "灯罩内壁黑点两次拖出细线，第二道落向灯座裂缝；冷金小印缝中的暗红线在巷外方向绷紧后缩回印内", "evidence": "黑点先后拖出两道细线，第二道落向灯座裂缝；仇慎小印印缝暗红线朝巷外绷着，临走时缩回。"}], "timeline": [{"fact_id": "chapter-0006-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "辰时复核后，程序推进至今日午后的泥灯巷护阵旁观落点重验", "after": "午后重验已结，结果附于本地残页；下一阶段为明日卯前送达的本地监督追缴", "evidence": "仇慎将午后结果处理为“午后结果附于本地残页”，并宣布明日卯前的新追缴纸“不是改账，是监督”。"}], "physical_state": [{"fact_id": "chapter-0006-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "识账时左眼下焦纹沿颧骨再绽开一小截，皮肉现烧焦气味并落下黑屑；银灰火屑未散", "after": "午后再识账时左眼焦黑裂纹绷紧，视野出现银灰火屑，识账后眼前发黑", "evidence": "陆沉渊闭眼再睁，左眼如塞烧红细砂，焦黑裂纹绷紧，银灰火屑黏在裂缝旁；冷金印落后“眼前一黑”。"}, {"fact_id": "chapter-0006-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": "本次识账后咳出冷灰落在命审台角，并被冷金小印压入在场认痕", "after": "午后识账与冷金印压痕后再次咳出冷灰，并被压入湿泥的在场认痕旁", "evidence": "陆沉渊在暗红印线窜出后偏脸咳灰；仇慎用印角把那一小片灰压进“在场认痕”旁。"}, {"fact_id": "chapter-0006-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "before": "薄纸衙印牵动掌心旧印后掌骨再响，胸口裂口感骤紧，需扶住台沿喘息", "after": "午后胸骨先磨响，末尾扶住泥灯座时掌骨在湿泥与旧砖间再次发出细响，胸口疼至只能称再站一会儿", "evidence": "陆沉渊先听见胸骨磨响；苏晚问能否站住时，他因胸口疼而扶住灯座，掌骨又磨出细响。"}, {"fact_id": "chapter-0006-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": "识账所咳冷灰被冷金小印压入在场认痕，薄纸衙印牵出暗红印线锁到陆沉渊掌心旧印", "after": "午后识账后，冷金小印把陆沉渊咳出的冷灰压入湿泥在场认痕旁；其掌纹暗红印线绕冷金边缘打结", "evidence": "仇慎以印压在陆沉渊掌心湿泥旁，暗红印线窜出并绕冷金边缘打结，之后又压入咳出的冷灰。"}, {"fact_id": "chapter-0006-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "before": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄", "after": "小印暗红线现身时，苏晚掌背裂口再次亮起并渗出暗冷光；本次记载未缓解其验灯状态", "evidence": "印缝暗红线出现时，苏晚掌背红点“同时亮了一下”，暗冷光从裂口渗出；仇慎随后称“苏晚验灯，不因这一笔缓”。"}], "naming": []}}

## Prose
午后的泥灯巷比辰时更窄。

日头压着破墙，墙缝里的湿泥晒出一层发白的灰。巷口那盏泥灯仍歪着，旧砖顶在灯座下，扫帚横在一旁。灯焰细得像根不肯断的线，灯罩内壁那颗黑点还贴在那里，既不下沉，也不散。

顾家的户灯没有送回。

命籍衙说验毕再发，巷里便少了一点昏黄。门缝一扇接一扇收窄，没人出来，只剩衣料擦过门板的细响。莫井兰站在泥灯边，陶片包在掌心，灰把她指节磨得发白。

“我只说早上那三句。”她没看陆沉渊，“陶片还在我手里。谁要它，我就不往下说。”

陆沉渊扶着墙，胸口一阵紧过一阵，开口时声音很低：“没人逼你多说。”

莫井兰抬眼，皱纹里的灰轻轻颤了一下。

“命籍衙会逼。”

巷外靴底踩进湿泥，不急，也不重，每一步却都踩得很实。仇慎进来时，手里只有一张薄纸与一枚冷金小印。那金属在日头下没有亮色，像井底捞出来的旧铁。

他停在泥灯前，先看灯座裂缝，又看莫井兰的手。

“午后重验，只验落点。”仇慎把薄纸摊开，“护阵旁观残页、顾家附录、陶片、昨夜追加纸。人都在，物也在。谁先说？”

没人应。

仇慎等了一会儿，目光落到陆沉渊左眼下。

那道焦黑裂纹已沿着颧骨往下爬，边缘起着干硬的皮。他来时走得急，黑屑蹭在衣领上，像洗不掉的烟灰。仇慎看了很久，才把薄纸往前递了半寸。

“你可以不认。”他说，“按追加纸，护阵旁观无人认领，便记无证护阵。顾家附录继续封，陶片随封。你母亲的验灯另列，不牵进这一笔。”

这是一条干净路。

陆沉渊只要点头，今夜就能少挨一道印。莫井兰不必把陶片摊在冷金印下，门里的人也不必被点名开门。护阵旁观既成无证，衙里照程序往下记，谁都不用当场再伤一回。

苏晚站在他身后。

她掌背那点红裂口还没合上，暗冷的光伏在里面，像灰里埋着一点薄冰。她的手指搭住陆沉渊袖口，冷得像沾湿的纸。

“沉渊。”她叫他。

陆沉渊回头。

苏晚没有劝他认，也没有替莫井兰开口。她望着泥灯，隔了片刻才说：“你想留东西，先问清楚，谁要替它受伤。”

仇慎眉心微动。

“只是复核。”他说。

“复核完，陶片归谁？”苏晚问。

仇慎没答。

莫井兰的手指收紧，陶片边缘从掌缝里露出一点灰白。那上面沾着顾家补墨留下的冷灰，也沾着她守灯时扫落的旧灰。若入衙封存，或许能留下；也或许从此只剩一行不许人看的封记。

“按规矩，暂入衙封存。”仇慎终于道。

“封到什么时候？”

“待后续核。”

“谁来看？”

仇慎的视线落到薄纸上，拇指压住被风掀起的纸角。冷金小印硌在他掌心，印缝里似乎有一点暗红。

“本地呈印先看。”他说，“有上催，再送。”

“有文书么？”苏晚问。

仇慎抬起眼，答得很快：“没有。”

没有文书，便只能算他手里的印发涩，不能算别的。可他说完，巷口泥灯的焰尖忽然矮了一截。

不是风。

灯罩内壁的黑点轻轻一颤，沿着烟痕拖出半寸细线。苏晚掌背的红点也亮了一下，裂口里的暗冷光渗出来，映得她脸色更白。她吸了一口气，却没去捂手，只把陆沉渊的袖口攥得更紧。

陆沉渊胸骨里传出一声极轻的磨响。

仇慎低头看小印。印缝中的暗红细线朝巷外绷着，到了他脚边的泥地，便停住了。没有缠上任何一扇门，也没有钻进泥灯。

莫井兰望着那条线：“这也要封进衙里？”

“这不是证。”仇慎道。

“陶片呢？”

“陶片是物证。”

“它若进衙封，谁替它活到后续核？”

仇慎脸色沉下来：“守灯者既带它来，就该知道规矩。”

“我知道。”莫井兰说，“所以我只带，不交。”

巷里静了下来。

门缝后有人把门关得更紧，也有人没动。没人替莫井兰作保，没人说愿意拿自家的灯、自己的火去换一块陶片。那些沉默不是怯懦，是各家都清楚自己剩下什么。

陆沉渊咽下喉间的腥冷，往前一步。

苏晚拦住他。

“你再看，眼睛要废。”她说。

“我不看人。”陆沉渊望着灯座下的裂缝，“只看灰。”

仇慎抬起冷金小印：“你一旦认灰，便入在场认痕。午后这笔留档，往后的残籍复核你绕不开。”

“陶片不入封。”陆沉渊道。

“你没有提条件的资格。”

“那我不认。”

这正是仇慎给他的路。

他只要退开，今日的重验便能按无证落下。仇慎不必在薄纸上添一笔难看的记载；莫井兰可以把陶片带回去，却也要眼看着护阵裂缝里的灰被下一场雨冲散。等那半指宽的空白没了，谁也不能再说它曾避开过护阵纹。

陆沉渊盯着那道裂缝，许久没有动。

他不能拿巷里人的灯去撑一条证据。

更不能让苏晚把裂开的手伸到印下。

他把掌心翻出来。那道青白旧印横在掌纹里，先前被薄纸牵过，边缘泛着暗红。他把手按进泥灯座旁的湿泥，冷意顺着掌骨往上钻。

“我认这一处。”他说，“只认泥灯裂缝、薄纸印落点、陶片上的补墨灰。莫井兰拿着陶片，不交。她只看我说的三处，不替我断谁改账，也不替我担后果。”

莫井兰看着他。

“我为什么替你留？”她问。

“你可以不留。”陆沉渊道，“你现在回去，陶片还在你手里。你留下，也只看当着你面的东西。我说错了，你就说我错了；我没看见的，你一个字也不用补。”

莫井兰沉默良久，慢慢把陶片露出来。

“我看。”她说，“我不保你说得对。”

“好。”

仇慎盯着陆沉渊按进泥里的手，像在看一只主动伸进锁里的腕子。

“识账。”

陆沉渊闭上左眼。

再睁开时，右眼里的泥灯、薄纸、陶片都还在原处；左眼却像塞进了一把烧红的细砂。焦黑裂纹绷紧，银灰火屑浮在视野边缘，飘不过三寸，就黏在泥灯裂缝旁。

他没去看仇慎，也没去看门缝后的人。

湿泥里有两种灰。

一股贴着裂缝，细而干，落到护阵旧纹边缘便散开；另一股伏在冷金印留下的浅坑周围，颜色更冷，像被什么压住。两者之间隔着半指宽的空白。那道空白从灯座底下绕出去，正好避开护阵纹最暗的一截。

陶片上的灰也浮了一下。

不是陶片动，是他眼里的银灰火屑贴了上去。补墨留下的冷灰浮在旧墨边，断纹斜斜朝下；薄纸上“昨夜追加”四字旁的灰却压着字墨，断纹朝冷金印边缘折去。它们都凉，却不是同一条落法。

陆沉渊呼吸断了一拍。

“说。”仇慎道。

“泥灯座裂缝里的灰，在护阵纹前断开。”陆沉渊声音发哑，“薄纸署时旁的灰压在字墨上。陶片补墨的灰不压墨。”

仇慎握印的手指收紧。

“说明什么？”

“只说明三处落灰不同。”陆沉渊把手从湿泥里拔出来，泥黏在旧印上，“说明不了谁改账，说明不了为何追加，也说明不了顾家折记该怎么改。”

莫井兰低头看陶片，又看薄纸。

“陶片上的灰，我看着浮在旧墨边。”她说，“薄纸上的灰，我看着压着新字。别的我不知道。”

仇慎忽然抬印。

冷金印没有压向陶片。

它重重落在陆沉渊掌边的湿泥上。泥里闷出一声轻响，暗红印线从掌纹窜出，绕着冷金边缘打了个结。陆沉渊眼前一黑，喉头的冷灰直冲上来。他偏过脸咳了一声。

一小片冷灰落进泥地。

仇慎用印角把灰压进“在场认痕”旁。

苏晚立刻按住陆沉渊后背。她掌心冷得厉害，隔着衣料也让他发颤。她没有碰印，没有碰陶片，只撑着他不让他跪下去。

泥灯焰尖又缩了一下。

灯罩里的黑点拖出第二道细线，落向灯座裂缝。旧砖被热得发出细微的爆响，墙上的护阵纹闪了闪，随即暗下去。

门缝后终于传来一声压不住的吸气。

仇慎听见了，脸上的肉绷得很紧。他拿起薄纸，重新看上面的字，又看陆沉渊掌心旁压出的暗红印线。

“你认的是灰痕不同。”

“是。”

“莫井兰只认所见。”

“是。”

“陶片不入衙封。”

莫井兰抬起头。

仇慎停了片刻，才道：“暂由守灯者携带，午后结果附于本地残页。下一次监督，陶片仍须到场。毁损、遗失，仍按毁证。”

“谁保它？”莫井兰问。

“你自己。”

“那你今天压了什么？”

仇慎没有答她。

他从薄纸上撕下一角，盖上冷金印。印落下去时，灯罩里的黑点不再拖线，泥灯却矮得只剩一点火星。仇慎把印角递给陆沉渊，手一松，纸角便落在湿泥上。

“本地残页暂不改。”仇慎道，“护阵旁观落点，保留灰痕不同的记载。顾家附录继续封。苏晚验灯，不因这一笔缓。”

苏晚按在陆沉渊背后的手微微收紧。

她没有争，也没有看自己的掌背。

“站得住么？”她轻声问。

陆沉渊想说能，胸口却先疼得发裂。他扶住泥灯座，掌骨在湿泥与旧砖间磨出细响。

“站一会儿。”

仇慎收起小印，转身前又回头看了一眼巷口。

“明日卯前，命籍衙送新的追缴纸。”他说，“不是改账，是监督。陆沉渊须在，莫井兰携陶片在，顾家户灯仍留衙。苏晚可拒验；拒验，照规矩续记。”

说完，冷金印缝里的暗红线颤了一下，缩回印里。

巷子重新安静。

莫井兰把陶片包回掌心，没有道谢。门缝后有人把门拉开半寸，又停住。泥灯座下那半指宽的空白仍在，湿泥里多了一枚冷金印，也多了一点陆沉渊咳出的冷灰。

苏晚扶着他离开灯座一步。

那一点火星在两人身后轻轻晃着，没有熄。

## Required JSON
```json
{
  "chapter_id": "chapter-0006",
  "artifact_kind": "revision",
  "artifact_sha256": "979947fade25a4f482f4daeb1020de1e01e73f1196c8794ba395a6fb3a8ccf0a",
  "context_sha256": "19b6a7705cdc2712c03bb3871162e278e006a36b1878798c8c783b1914476786",
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
