# NRL Antigravity Chapter Audit v0.20

Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.
Do not use terminal tools, inspect files, run tests, make a plan, or wait for background work. The complete review packet is inline.
Do not rewrite prose. Return one JSON object only using the exact binding hashes, with no Markdown fence or surrounding text.

## Compact Context
{"chapter_id": "chapter-0007", "dramatic_purpose": "让本地执行者与街坊各自暴露恐惧和利益，主角取得一条可复核但不完整的错账链。", "must_keep": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "不得把敌人写成无理由恶意；证据只覆盖本地一段。"], "must_avoid": ["不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"], "assets": [{"asset_id": "character_lu_chenyuan", "display_name": "陆沉渊", "family": "characters", "lifecycle_state": "active", "constraints": ["Does not transfer a life-cost to uninvolved residents.", "Each use leaves bodily evidence or increases pursuit risk.", "His mother debt and the lane protection array remain non-negotiable constraints.", "At 燃命境初成 he may only recognize ordinary life marks and local ash-trace mismatches; personal-page reading, chain tracing, covenant glimpses, return-fire casting, and seal breaking remain blocked pending validated advancement."], "relationships": [{"target_id": "bond_mother_su_wan", "relation_type": "son_bound_by_lifespan_debt"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_acquire_after_registered_transition"}, {"target_id": "faction_mudlamp_lane", "relation_type": "protects_and_is_bound_to"}, {"target_id": "technique_embertrace_return", "relation_type": "may_unlock_after_lamp_and_progression_gates"}, {"target_id": "technique_ledger_recognition", "relation_type": "uses_basic_local_ash_trace_scope_of"}]}, {"asset_id": "npc_su_wan", "display_name": "苏晚", "family": "npcs", "lifecycle_state": "active", "constraints": ["苏晚是能拒绝错误救法的行动者，不是可消耗的动机。", "她绝不接受以邻里命火、孩童寿数或无辜者命页抵消自己的寿债。", "她的命灯裂纹、冷灰气息和掌背失温须以感官后果呈现，不以抽象说明替代。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "bond_mother_su_wan", "relation_type": "embodies"}, {"target_id": "faction_mudlamp_lane", "relation_type": "mutual_aid_member_of"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "raises_restraint_threshold_for"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "is_counted_down_by"}]}, {"asset_id": "npc_registrar_qiu_shen", "display_name": "仇慎", "family": "npcs", "lifecycle_state": "active", "constraints": ["仇慎只能掌握本地残页与寿印权限，不能成为无所不知的阴谋解释者。", "其每一次施印必须留下可辨的冷金印痕或命灯失色，并制造可追责的现场后果。", "他可恐惧上级追责，但不能因恐惧自动洗白。", "其独立义务是保住本地呈印资格并避免州府问责；当公开证据使继续施印超出本地权限时，可拖延、议价或退回追缴令，但不得因此获得无证据洗白。"], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "serves_as_registrar_for"}, {"target_id": "character_lu_chenyuan", "relation_type": "supervises_and_targets"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "forwards_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "pressures_with_seals"}]}, {"asset_id": "npc_mo_jinglan", "display_name": "莫井兰", "family": "npcs", "lifecycle_state": "active", "constraints": ["Her knowledge is partial oral memory, never omniscient exposition.", "Helping preserve testimony exposes her remaining life-fire to collection."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "keeps_its_night_lamps"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "witnesses_surface_sign"}]}, {"asset_id": "bond_mother_su_wan", "display_name": "苏晚与陆沉渊的垫寿亲缘", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["The mother is an active moral presence, not expendable motivation.", "Any attempt to relieve her debt must carry an exposure, bodily, or communal consequence."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "deadline_is_tracked_by"}]}, {"asset_id": "bond_mudlamp_lane_trust", "display_name": "泥灯巷共灯之信", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["共同体信任不是主角可提取的资源；巷民有拒绝、质询和撤回见证的权利。", "信任提升必须来自共同承担、返还寿火或公开承担反噬，而非主角单方面胜利。", "任何高风险行动都须显示巷民的恐惧、选择与实际保护行为。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "binds_to_community"}, {"target_id": "faction_mudlamp_lane", "relation_type": "measures_mutual_aid_of"}, {"target_id": "npc_su_wan", "relation_type": "is_guarded_by_moral_boundary_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "conditions_witnessed_return"}]}, {"asset_id": "faction_mudlamp_lane", "display_name": "泥灯巷", "family": "factions", "lifecycle_state": "active", "constraints": ["The mutual-aid network cannot become expendable fuel for a single hero.", "Every communal protection act worsens the protection array's visible lifespan cracks or attracts collectors."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "contains_registered_acquisition_site_for"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "is_tracked_by"}]}, {"asset_id": "faction_life_registry_office", "display_name": "命籍衙", "family": "factions", "lifecycle_state": "active", "constraints": ["其压迫必须通过寿印、命灯、命审台和具体家庭后果显形，不写成现实机构讽刺。", "本地权限只能冻结、登记、送审与申请追缴，不能解释州府或天庭的完整真相。", "命审程序必须成为可被证据、见证和法术反打的冲突场域。"], "relationships": [{"target_id": "npc_registrar_qiu_shen", "relation_type": "employs"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "issues_local_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "assesses_and_pressures"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "contests"}]}, {"asset_id": "technique_ledger_recognition", "display_name": "识账术", "family": "techniques", "lifecycle_state": "active", "constraints": ["At character_lu_chenyuan's current 燃命境初成 stage, the active scope is limited to ordinary life marks and local copy-level ash-trace mismatches visible in the present evidence.", "Personal-page reading is locked to a validated 识账境 transition; chain tracing requires a later audited proof, and ancient-covenant glimpses remain blocked until an independently validated advanced transition and artifact evidence exist.", "The technique cannot directly read minds, predict outcomes, or produce a complete answer at any stage.", "施展后瞳孔浮出焦黑纹路、视野残留银灰火屑，并提升被寿印锁定的风险。", "所有判断须由可见痕迹或受害者见证复核，不能以主角独白定案。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "is_practiced_by"}, {"target_id": "technique_embertrace_return", "relation_type": "verifies_targets_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "increases"}, {"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "cannot_reveal_before_validated_advanced_progression"}]}, {"asset_id": "foreshadowing_cinder_seal_rain", "display_name": "灰雨印痕", "family": "foreshadowing", "lifecycle_state": "active", "constraints": ["The clue appears as sensory supernatural residue, not paperwork.", "Investigating it burns the investigator and raises collection exposure before any revelation."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "is_revealed_by"}, {"target_id": "npc_mo_jinglan", "relation_type": "is_remembered_by"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "payoff_tracks"}]}, {"asset_id": "state_ledger_protagonist_strain", "display_name": "陆沉渊命火与心魄承压", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["状态只记录可叙事化的命火、骨裂、瞳纹、冷灰与心魄恍惚，读者文本不得呈现工程字段。", "任何恢复都不能自动解除母亲寿债、半寿身份或既有追缴。", "承压过界时主角应失去施术窗口或需要他人阻止，而非获得无代价爆发。", "空寿状态是施术锁定与认知承压：不得提升战力；继续行动必须先支付已登记的寿火扣减，并失去至少一个施术或判断能力，恢复须停术和外部看护。", "This asset is the sole writer of sanity_level, caster_lifefire_stability, bone_fissure_severity, eye_pattern_burn, and cold_ash_cough_frequency; it may not write exposure or mother-lamp state."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "tracks_strain_for"}, {"target_id": "technique_ledger_recognition", "relation_type": "is_decreased_by"}, {"target_id": "technique_chain_deflection_seal_breaking", "relation_type": "is_worsened_by"}, {"target_id": "bond_mother_su_wan", "relation_type": "raises_family_risk_for"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_half_life_registry_exposure", "display_name": "半寿残籍暴露", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of half_life_registry_exposure; techniques, artifacts, NPCs, and other ledgers may request a delta but may not write the value directly.", "Exposure never decreases merely because evidence succeeds or life-fire returns; reduction requires a separately evidenced legal, masking, or withdrawal transition.", "Threshold crossings must change pursuit or access state before the atomic transaction can close.", "The Cluster 5 evidence-record exchange requests exactly +10 percentage points within the 0-100 bound and closes only with the protagonist-owned record debit under the same transaction ID; child, resident, and third-party life-fire prices are rejected."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "solely_tracks_registry_exposure_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "npc_cluster5_black_market_transaction_role", "relation_type": "is_increased_by_transaction_with"}]}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "display_name": "苏晚命灯裂纹倒计时", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mother_life_lamp_cracks and the mother-life-debt countdown.", "A communal return or protagonist recovery cannot automatically heal a crack or cancel the unresolved mother debt.", "Any technique transaction that affects Su Wan must record the crack/countdown delta here before closing."], "relationships": [{"target_id": "npc_su_wan", "relation_type": "solely_tracks_lamp_cracks_for"}, {"target_id": "bond_mother_su_wan", "relation_type": "provides_countdown_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "cannot_be_auto_cancelled_by"}]}, {"asset_id": "state_ledger_mudlamp_array_integrity", "display_name": "泥灯巷护阵完整度", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mudlamp_array_integrity; returned fire, resident reserve, and caster strain remain independently owned.", "Array integrity cannot rise from returned fire alone; witnessed repair or stabilization must be recorded.", "Below the registered safety line, lamp activation and return-fire casting fail closed rather than granting emergency power."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_array_integrity_for"}, {"target_id": "artifact_ashlight_cup", "relation_type": "gates_acquisition_and_activation_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_resident_lifefire_reserve", "display_name": "泥灯巷住户命火储备", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of resident_lifefire_reserve; the reserve is never protagonist inventory or an automatic communal resource.", "Every debit requires named consent and preserves the right to refuse or withdraw before transaction closure.", "No black-market price, technique cost, or artifact awakening may debit children, uninvolved residents, or an unspecified crowd."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_consented_reserve_for"}, {"target_id": "bond_mudlamp_lane_trust", "relation_type": "requires_refusal_and_consent_rights_from"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_supply_consented_watchfire_for_awakening"}]}, {"asset_id": "state_ledger_poorcity_returnfire", "display_name": "泥灯巷归火余量", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["A positive return never cancels the mother debt or the protection array burden automatically.", "Every gain must name whose life-fire returned and whose visible backlash or exposure increased.", "This asset is the sole writer of returned_miscollected_lifefire and may not write caster strain, registry exposure, array integrity, resident reserve, or mother-lamp state."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "measures_survival_pressure_for"}, {"target_id": "technique_embertrace_return", "relation_type": "is_changed_by"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_affected"}]}, {"asset_id": "state_ledger_revealed_account_errors", "display_name": "已揭示错账记录", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of revealed_account_errors; evidence, return-fire, and outline assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source evidence and at least one independently owned return-fire, exposure, reputation, pressure, or mystery consequence.", "No inferred or unverified account error may be counted, and no proof may create an implicit credit or debit."], "relationships": [{"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_faction_pressure", "display_name": "既有势力压力", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of faction_pressure; faction, NPC, and scene assets may request but may not apply a mutation.", "Every mutation must identify an existing source asset and settle atomically with exposure, public reputation, or revealed-error consequences.", "No new faction, location, or plot event may be created to justify a pressure change."], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "faction_prefecture_life_treasury", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_public_reputation", "display_name": "公开认知状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of public_reputation; all other assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source, reason, before/after state, and at least one independently owned consequence ledger.", "No success, witness, or exposure event changes reputation implicitly or closes without its peer ledger result."], "relationships": [{"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_unresolved_mysteries", "display_name": "未解账目疑点", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of unresolved_mysteries; foreshadowing and outline assets may request but may not apply a mutation.", "Every add, reclassification, or closure requires an explicit atomic transaction with a revealed-error or map-boundary consequence.", "No new mystery, answer, backstory, or plot event may be created by this ledger."], "relationships": [{"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "tracks_only_registered_questions_from"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_map_unlock_status", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_map_unlock_status", "display_name": "既有地图边界解锁状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of map_unlock_status; references to existing map boundaries may request but may not apply a transition.", "Every transition is atomic and must preserve unresolved boundaries while recording any exposure consequence.", "The ledger cannot introduce a location or unlock a boundary absent from the canonical outline."], "relationships": [{"target_id": "artifact_prefecture_transit_registry_seal", "relation_type": "requires_validated_boundary_evidence_from"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}], "prior_settlements": [{"chapter_id": "chapter-0001", "accepted_revision_sha256": "79d46dc564388fc32d8bae5b8fdc5ebd7a3dc2412e2174f8558844cad1fda874", "state_deltas": [{"fact_id": "chapter-0001-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": null, "after": "顾家的折记暂缓，午后再核"}, {"fact_id": "chapter-0001-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.local_enforcement_status", "operation": "set", "before": "顾家折记待按册落印核验", "after": "顾家折记暂缓至午后复核"}, {"fact_id": "chapter-0001-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": null, "after": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索"}, {"fact_id": "chapter-0001-information-foreshadowing-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨印痕未在本章现场显现", "after": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小"}, {"fact_id": "chapter-0001-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "寿籍司尚未进入泥灯巷核验", "after": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后"}, {"fact_id": "chapter-0001-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "眼尾仅有极淡、藏在睫毛下的焦黑细纹", "after": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0002", "accepted_revision_sha256": "356320d82944a61555f663908889d71d0afff3c35b5fa3c0ede592ef0ecfaeaf", "state_deltas": [{"fact_id": "chapter-0002-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家的折记暂缓，午后再核", "after": "顾家折记继续暂缓，三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后", "after": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.procedural_observation_of_lu_chenyuan", "before": null, "after": "陆沉渊被要求往后残籍复核在场；传核缺席按拒验记", "operation": "set"}, {"fact_id": "chapter-0002-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "operation": "set"}, {"fact_id": "chapter-0002-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": null, "after": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "operation": "set"}, {"fact_id": "chapter-0002-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "顾家“折三”补墨与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "错位线索被记为本地复核附录，但不作为改账依据", "operation": "set"}, {"fact_id": "chapter-0002-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小", "after": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "operation": "set"}, {"fact_id": "chapter-0002-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": null, "after": "顾家折记三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩", "after": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": null, "after": "识账后当场咳出一小片冷灰", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": null, "after": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "operation": "set"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0003", "accepted_revision_sha256": "8167366cd6811f13f63105eb5e0644bccb5c069e6081e29e4a66150554158b3f", "state_deltas": [{"fact_id": "chapter-0003-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "被要求往后残籍复核在场；传核缺席按拒验记", "after": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来"}, {"fact_id": "chapter-0003-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄"}, {"fact_id": "chapter-0003-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_witness_material", "operation": "set", "before": null, "after": "暂带顾家补墨灰屑陶片作为守灯见证物"}, {"fact_id": "chapter-0003-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_local_lamp_assessment", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "验灯显示命灯失温、焰尖缩成细线，手背红点裂开并渗出暗冷光"}, {"fact_id": "chapter-0003-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "after": "顾家附录暂封并列入三日内再验，苏晚户灯旁证暂不作改账凭据"}, {"fact_id": "chapter-0003-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "顾家折记三日内再次复核", "after": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证"}, {"fact_id": "chapter-0003-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "after": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔"}, {"fact_id": "chapter-0003-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "after": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界"}, {"fact_id": "chapter-0003-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "陆沉渊每次施术的反噬尚未被苏晚在本次复核中当场看见", "after": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹"}, {"fact_id": "chapter-0003-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "错位线索被记为本地复核附录，但不作为改账依据", "after": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据"}, {"fact_id": "chapter-0003-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线"}, {"fact_id": "chapter-0003-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "after": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": null, "after": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "识账后当场咳出一小片冷灰", "after": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印"}, {"fact_id": "chapter-0003-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "after": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸"}, {"fact_id": "chapter-0003-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "operation": "set", "before": "灰粒落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0004", "accepted_revision_sha256": "e3ed91078715d2b3540da38987cb7db63bcd559ea1e320fb0b07a550d091b6f7", "state_deltas": [{"fact_id": "chapter-0004-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_intent", "operation": "set", "before": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来", "after": "确认明日辰时到场，但不替任何住户陈述未亲见之事"}, {"fact_id": "chapter-0004-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "operation": "set", "before": "暂带顾家补墨灰屑陶片作为守灯见证物", "after": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句"}, {"fact_id": "chapter-0004-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_refusal_statement", "operation": "set", "before": null, "after": "拒绝以自己抵命，也拒绝以泥灯巷住户命火填补自身裂纹"}, {"fact_id": "chapter-0004-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.latest_local_notice", "operation": "set", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席"}, {"fact_id": "chapter-0004-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "operation": "set", "before": null, "after": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩"}, {"fact_id": "chapter-0004-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证", "after": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记"}, {"fact_id": "chapter-0004-faction-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "operation": "set", "before": null, "after": "未有住户命火实际投入巷口泥灯；住户保留各自关门、留缝或守灯的选择"}, {"fact_id": "chapter-0004-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔", "after": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展"}, {"fact_id": "chapter-0004-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界", "after": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片"}, {"fact_id": "chapter-0004-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线", "after": "巷口泥灯罩内壁留下不下沉的黑点；薄纸上的冷灰沿纸纤维聚成空白，避开命籍衙印落点"}, {"fact_id": "chapter-0004-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时", "after": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑", "after": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印", "after": "本次夜间识账后再次咳出冷灰，落在巷口泥地"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感", "after": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0005", "accepted_revision_sha256": "f627dd586df7aa3238d6722148adf34f5bf1c4efaf29f254344d138e31525aaa", "state_deltas": [{"fact_id": "chapter-0005-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "确认明日辰时到场，但不替任何住户陈述未亲见之事", "after": "已到场完成本地复核，并被要求午后护阵旁观重验继续在场；凡本地残页复核不得缺席"}, {"fact_id": "chapter-0005-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "顾家附录继续封存；守灯前三句保留，未知来源不入；护阵旁观追加残页改列次序待核"}, {"fact_id": "chapter-0005-npc-registrar-qiu-shen-002", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_local_notice", "operation": "set", "before": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席", "after": "已发出今日午后泥灯巷护阵旁观落点重验通知，并列明顾家户灯留衙、莫井兰携陶片、陆沉渊到场的条件"}, {"fact_id": "chapter-0005-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "operation": "set", "before": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句", "after": "已在复核中陈述顾家旧灰、补墨灰凉无油及断纹相反三句；陶片仍暂带，午后须携带在场"}, {"fact_id": "chapter-0005-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "operation": "set", "before": null, "after": "午后可拒绝验灯，但不得替陆沉渊认灰"}, {"fact_id": "chapter-0005-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "operation": "set", "before": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩", "after": "护阵旁观落点被列为今日午后重验对象，尚未完成复核或修补"}, {"fact_id": "chapter-0005-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "after": "辰时复核已完成并将护阵旁观追加残页列为次序待核；午后转入泥灯巷重验监督"}, {"fact_id": "chapter-0005-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记", "after": "今日午后在泥灯巷重验护阵旁观落点；顾家户灯留衙至验毕，莫井兰携陶片、陆沉渊到场，人或物缺一按拒验续记"}, {"fact_id": "chapter-0005-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展", "after": "顾家附录补墨灰位于冷金印下；护阵旁观残页署时旁灰浮在墨上且被冷金截断，右页存在无法与“昨夜追加”同时自证的局部次序"}, {"fact_id": "chapter-0005-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片", "after": "莫井兰保留前三句限于所见的陈述，拒绝补入未知来源；午后继续以暂带陶片的限定方式到场"}, {"fact_id": "chapter-0005-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹", "after": "苏晚在识账反噬中按住陆沉渊腕上发抖的手，未替他认灰或触碰残页"}, {"fact_id": "chapter-0005-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据", "after": "护阵旁观追加残页被确认存在局部次序疑处，列为待核；未被认定为顾家折记错误、护阵追加无效或改时原因的证明"}, {"fact_id": "chapter-0005-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "after": "辰时复核后，程序推进至今日午后的泥灯巷护阵旁观落点重验"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑", "after": "识账时左眼下焦纹沿颧骨再绽开一小截，皮肉现烧焦气味并落下黑屑；银灰火屑未散"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "本次夜间识账后再次咳出冷灰，落在巷口泥地", "after": "本次识账后咳出冷灰落在命审台角，并被冷金小印压入在场认痕"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声", "after": "薄纸衙印牵动掌心旧印后掌骨再响，胸口裂口感骤紧，需扶住台沿喘息"}, {"fact_id": "chapter-0005-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸", "after": "识账所咳冷灰被冷金小印压入在场认痕，薄纸衙印牵出暗红印线锁到陆沉渊掌心旧印"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0006", "accepted_revision_sha256": "979947fade25a4f482f4daeb1020de1e01e73f1196c8794ba395a6fb3a8ccf0a", "state_deltas": [{"fact_id": "chapter-0006-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "已到场完成本地复核，并被要求午后护阵旁观重验继续在场；凡本地残页复核不得缺席", "after": "午后重验中以自身在场认痕换取陶片不入衙封；明日卯前新的监督追缴仍须在场"}, {"fact_id": "chapter-0006-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家附录继续封存；守灯前三句保留，未知来源不入；护阵旁观追加残页改列次序待核", "after": "本地残页暂不改；护阵旁观落点保留“灰痕不同”记载，顾家附录继续封"}, {"fact_id": "chapter-0006-npc-registrar-qiu-shen-002", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_local_notice", "operation": "set", "before": "已发出今日午后泥灯巷护阵旁观落点重验通知，并列明顾家户灯留衙、莫井兰携陶片、陆沉渊到场的条件", "after": "明日卯前送达新的监督追缴纸；陆沉渊与莫井兰携陶片须在，顾家户灯仍留衙，苏晚可拒绝验灯但拒绝续记"}, {"fact_id": "chapter-0006-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "operation": "set", "before": "已在复核中陈述顾家旧灰、补墨灰凉无油及断纹相反三句；陶片仍暂带，午后须携带在场", "after": "午后仅见证陶片旧墨边浮灰与薄纸新字上压灰；陶片继续由其携带并须在下一次监督到场"}, {"fact_id": "chapter-0006-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "operation": "set", "before": "午后可拒绝验灯，但不得替陆沉渊认灰", "after": "下一次监督仍可拒绝验灯；拒绝将被续记"}, {"fact_id": "chapter-0006-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "辰时复核已完成并将护阵旁观追加残页列为次序待核；午后转入泥灯巷重验监督", "after": "午后落点重验结束；本地残页暂不改，程序推进至明日卯前的本地监督追缴"}, {"fact_id": "chapter-0006-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "今日午后在泥灯巷重验护阵旁观落点；顾家户灯留衙至验毕，莫井兰携陶片、陆沉渊到场，人或物缺一按拒验续记", "after": "明日卯前送达新的本地监督追缴纸；陆沉渊、莫井兰与陶片须在，顾家户灯仍留衙，苏晚拒绝验灯则续记"}, {"fact_id": "chapter-0006-faction-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "operation": "set", "before": "护阵旁观落点被列为今日午后重验对象，尚未完成复核或修补", "after": "重验后泥灯焰尖缩至几乎只剩火星，灯座旧砖出现细微爆裂声，墙上护阵纹闪后熄回"}, {"fact_id": "chapter-0006-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "顾家附录补墨灰位于冷金印下；护阵旁观残页署时旁灰浮在墨上且被冷金截断，右页存在无法与“昨夜追加”同时自证的局部次序", "after": "泥灯裂缝灰在护阵纹前断开；薄纸署时旁灰压在字墨上；陶片补墨灰浮于旧墨边，三处落灰不同"}, {"fact_id": "chapter-0006-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰保留前三句限于所见的陈述，拒绝补入未知来源；午后继续以暂带陶片的限定方式到场", "after": "莫井兰同意只当面观察陆沉渊所认三处灰痕，不替其担保结论；陶片继续由其自行携带"}, {"fact_id": "chapter-0006-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "苏晚在识账反噬中按住陆沉渊腕上发抖的手，未替他认灰或触碰残页", "after": "苏晚再次看见并直接扶住陆沉渊识账后的失衡，但未碰冷金印或陶片"}, {"fact_id": "chapter-0006-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "护阵旁观追加残页被确认存在局部次序疑处，列为待核；未被认定为顾家折记错误、护阵追加无效或改时原因的证明", "after": "本地记录保留泥灯裂缝、薄纸署时与陶片补墨三处灰痕不同；仍未作为改账、追加原因或顾家折记处理的证明"}, {"fact_id": "chapter-0006-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "巷口泥灯罩内壁留下不下沉的黑点；薄纸上的冷灰沿纸纤维聚成空白，避开命籍衙印落点", "after": "灯罩内壁黑点两次拖出细线，第二道落向灯座裂缝；冷金小印缝中的暗红线在巷外方向绷紧后缩回印内"}, {"fact_id": "chapter-0006-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "辰时复核后，程序推进至今日午后的泥灯巷护阵旁观落点重验", "after": "午后重验已结，结果附于本地残页；下一阶段为明日卯前送达的本地监督追缴"}, {"fact_id": "chapter-0006-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "识账时左眼下焦纹沿颧骨再绽开一小截，皮肉现烧焦气味并落下黑屑；银灰火屑未散", "after": "午后再识账时左眼焦黑裂纹绷紧，视野出现银灰火屑，识账后眼前发黑"}, {"fact_id": "chapter-0006-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "本次识账后咳出冷灰落在命审台角，并被冷金小印压入在场认痕", "after": "午后识账与冷金印压痕后再次咳出冷灰，并被压入湿泥的在场认痕旁"}, {"fact_id": "chapter-0006-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": "薄纸衙印牵动掌心旧印后掌骨再响，胸口裂口感骤紧，需扶住台沿喘息", "after": "午后胸骨先磨响，末尾扶住泥灯座时掌骨在湿泥与旧砖间再次发出细响，胸口疼至只能称再站一会儿"}, {"fact_id": "chapter-0006-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "识账所咳冷灰被冷金小印压入在场认痕，薄纸衙印牵出暗红印线锁到陆沉渊掌心旧印", "after": "午后识账后，冷金小印把陆沉渊咳出的冷灰压入湿泥在场认痕旁；其掌纹暗红印线绕冷金边缘打结"}, {"fact_id": "chapter-0006-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "operation": "set", "before": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄", "after": "小印暗红线现身时，苏晚掌背裂口再次亮起并渗出暗冷光；本次记载未缓解其验灯状态"}], "resolved_audit_ids": []}]}

## Rule Stack
{"version": "0.22", "chapter_id": "chapter-0007", "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "priority_order": ["safety_and_originality", "canonical_story_bible", "volume_outline", "accepted_state_settlements", "creation_asset_constraints", "chapter_must_keep_and_must_avoid", "anti_ai_style_evidence"], "hard_rules": ["no source-work names, scenes, signature systems, or prose imitation", "no untracked power, relationship, location, item, or timeline changes", "all benefits carry an embodied, relational, or systemic cost", "reader-facing prose contains no runtime or database vocabulary", "不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "chapter_rules": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "不得把敌人写成无理由恶意；证据只覆盖本地一段。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"]}

## Compilation Trace
{"version": "0.22", "chapter_id": "chapter-0007", "selected_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "explicit_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "dependency_asset_ids": [], "excluded_asset_count": 22, "selection_reason": "explicit chapter intent requirements plus atomic transaction peers", "canonical_hashes": {"borrowed_heaven_life_account_bible": "81575478a441852f18d451e9967245bbfce11d60cddd3af24e9b6565955e0604", "borrowed_heaven_volume1_outline_tree": "1f12fe8ad3262876eb533d40c94ad02abb90b95b38de387d339917fce9184648", "project_assets.v0.2": "90dbcf17d769e8a985fc87880a4382018c30133a2a53f82c3826636c8ed1dc61"}, "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "prior_settlement_count": 6}

## Observed Facts
{"chapter_id": "chapter-0007", "draft_sha256": "098bda98b2f595429a2166fe690978a14324a3cb362c27c11138e8c3f1062f4a", "facts": {"characters": [{"fact_id": "chapter-0007-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "before": "午后重验中以自身在场认痕换取陶片不入衙封；明日卯前新的监督追缴仍须在场", "after": "本次仅完成监督追缴纸送达；明日午前须到命籍衙，携带本人限于所见的口述", "evidence": "仇慎称“今天只是送达”，并要求陆沉渊明日午前到命籍衙、带自己的口述。"}], "npcs": [{"fact_id": "chapter-0007-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "本地残页暂不改；护阵旁观落点保留“灰痕不同”记载，顾家附录继续封", "after": "今日不收陶片；顾家户灯继续留衙，陆沉渊、莫井兰与顾婶明日午前须各带限定口述或陶片到命籍衙", "evidence": "仇慎说“今日不收陶片”，随后指定三人明日午前到场，并保留顾家户灯留衙。"}, {"fact_id": "chapter-0007-npc-registrar-qiu-shen-002", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_procedural_stake", "before": null, "after": "因本地残页次序若站不住将危及其继续落印资格，而试图将听闻内容压为认词", "evidence": "正文明确写出仇慎要保住落印资格，并要求莫井兰承认其只听见、未亲见的第三处灰痕。"}, {"fact_id": "chapter-0007-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "before": "午后仅见证陶片旧墨边浮灰与薄纸新字上压灰；陶片继续由其携带并须在下一次监督到场", "after": "拒绝交陶片入衙封存；仅陈述亲见的顾家旧灰、补墨灰与薄纸新压灰，不承认未亲见的灯座断痕", "evidence": "莫井兰拒绝解开陶片布结，并说“听见不等于看见”。"}, {"fact_id": "chapter-0007-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "before": "下一次监督仍可拒绝验灯；拒绝将被续记", "after": "当场明确拒绝验灯，并警告仇慎不得动用泥灯巷住户的灯", "evidence": "苏晚接纸后说“我不验灯”，又说“别动巷里人的灯”。"}], "locations": [{"fact_id": "chapter-0007-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "before": "重验后泥灯焰尖缩至几乎只剩火星，灯座旧砖出现细微爆裂声，墙上护阵纹闪后熄回", "after": "巷口泥灯火星被风压至几乎熄灭；灯罩黑线沿灯座裂口牵出半寸后猛地缩回", "evidence": "末段写明火星几乎熄灭，黑线向外牵至半寸又缩回。"}], "factions": [{"fact_id": "chapter-0007-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "午后落点重验结束；本地残页暂不改，程序推进至明日卯前的本地监督追缴", "after": "卯前监督追缴纸已完成送达；程序改为明日午前命籍衙内的三人、陶片与顾家户灯监督", "evidence": "仇慎说明今日只是送达，并规定明日午前到命籍衙；顾家户灯仍留衙。"}, {"fact_id": "chapter-0007-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": "明日卯前送达新的本地监督追缴纸；陆沉渊、莫井兰与陶片须在，顾家户灯仍留衙，苏晚拒绝验灯则续记", "after": "明日午前命籍衙监督：莫井兰携陶片，陆沉渊携本人所见口述，顾婶携自身所见；缺一按拒验续记", "evidence": "仇慎离开前逐一指定三人的携带内容，并说不来则新的监督追缴纸先到各自门上。"}], "artifacts": [], "techniques": [{"fact_id": "chapter-0007-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "泥灯裂缝灰在护阵纹前断开；薄纸署时旁灰压在字墨上；陶片补墨灰浮于旧墨边，三处落灰不同", "after": "灯座灰在护阵纹前平齐断开、薄纸灰压在字墨上、陶片灰浮于旧墨边；三处灰痕不同，且无法证明来自同一路径", "evidence": "陆沉渊以肉眼逐项陈述三处痕迹，明确说“它们至少没有从同一处一路拖过来”，并承认只能看这么多。"}], "relationships": [{"fact_id": "chapter-0007-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": "莫井兰同意只当面观察陆沉渊所认三处灰痕，不替其担保结论；陶片继续由其自行携带", "after": "莫井兰仅为亲见两处灰痕作证；顾婶仅认户灯被带走前焰尖为细线；其余巷民保留仅记自身所见、不作认词的立场", "evidence": "莫井兰拒认第三处，顾婶拒认户灯以外的事，一名住户说“可记，不可认”。"}, {"fact_id": "chapter-0007-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "before": "苏晚再次看见并直接扶住陆沉渊识账后的失衡，但未碰冷金印或陶片", "after": "苏晚在陆沉渊眼角流出黑屑、身体晃动时再次扶住他，并代为接下追缴薄纸", "evidence": "陆沉渊身子晃动后苏晚立刻扶住；此前由她伸手接过仇慎递出的薄纸。"}], "emotions": [{"fact_id": "chapter-0007-emotion-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_fear_and_interest", "before": null, "after": "恐惧本地残页次序问题导致既有印痕回到自己手中、失去呈印资格", "evidence": "正文写明若残页次序站不住，其前面盖过的印会回到手里，州府将追问谁准其盖印。"}], "information": [{"fact_id": "chapter-0007-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "本地记录保留泥灯裂缝、薄纸署时与陶片补墨三处灰痕不同；仍未作为改账、追加原因或顾家折记处理的证明", "after": "薄纸冷灰空白绕开仇慎印落点，延至“顾家户灯留衙”字样后断在“陶片在场”旁；形成可复核但不完整的本地错账链", "evidence": "苏晚与陆沉渊均以肉眼看见冷灰空白的延伸和断点；陆沉渊明确说链外是什么仍没人看见。"}], "hooks": [{"fact_id": "chapter-0007-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灯罩内壁黑点两次拖出细线，第二道落向灯座裂缝；冷金小印缝中的暗红线在巷外方向绷紧后缩回印内", "after": "灯罩黑点沿旧裂缝形成第二道细线，后随冷金小印声响牵出半寸又猛地缩回；追缴薄纸冷灰聚成绕印的极细空白", "evidence": "开篇写黑点拖出第二道细线；仇慎离开时黑线牵出后缩回，薄纸冷灰绕开印落点聚拢。"}], "timeline": [{"fact_id": "chapter-0007-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "午后重验已结，结果附于本地残页；下一阶段为明日卯前送达的本地监督追缴", "after": "卯前追缴纸已送达并宣布明日午前监督；仇慎离开后命籍衙执行者又折返至巷口，新的追缴纸尚未贴门", "evidence": "仇慎说明今日仅送达；结尾明确“新的监督追缴纸还没贴上门，命籍衙的人已经折返到了巷口”。"}], "physical_state": [{"fact_id": "chapter-0007-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "午后再识账时左眼焦黑裂纹绷紧，视野出现银灰火屑，识账后眼前发黑", "after": "未施术时左眼焦纹灼至眉骨，眼角流出焦黑屑；擦落的黑屑在旧砖上冒出细烟", "evidence": "陆沉渊克制未施术，仍出现左眼刺痛、流黑屑，黑屑擦到旧砖后冒烟。"}, {"fact_id": "chapter-0007-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "before": "午后胸骨先磨响，末尾扶住泥灯座时掌骨在湿泥与旧砖间再次发出细响，胸口疼至只能称再站一会儿", "after": "胸骨裂口感持续至卯前，掌心旧印触及追缴薄纸后疼痛沿掌骨上钻", "evidence": "开篇写胸骨如干硬骨片摩擦；末段掌心旧印碰到纸边后疼痛沿掌骨往上钻。"}, {"fact_id": "chapter-0007-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": "午后识账后，冷金小印把陆沉渊咳出的冷灰压入湿泥在场认痕旁；其掌纹暗红印线绕冷金边缘打结", "after": "掌心旧印接触追缴薄纸边时，暗红细线从皮下绕过指根，结成尚未落完的圈", "evidence": "苏晚将薄纸塞入陆沉渊手中后，掌心旧印浮出暗红细线并在指根处结圈。"}, {"fact_id": "chapter-0007-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "before": "小印暗红线现身时，苏晚掌背裂口再次亮起并渗出暗冷光；本次记载未缓解其验灯状态", "after": "苏晚掌背隔布接触追缴薄纸时再次透出暗冷光，旧布角被光浸湿", "evidence": "苏晚接纸时布下透出暗冷光；开篇亦写旧布角已被暗冷光浸湿。"}], "naming": []}}

## Prose
卯时还没到，泥灯巷的天是青灰色的。

巷口那盏泥灯只剩一粒火星，灯罩内壁的黑点沿着旧裂缝拖出第二道细线，像有人用烧红的针，在泥上慢慢划过。线到灯座便停了，裂砖里卡着一点湿黑，风一吹，黑点没有散，反倒贴得更紧。

陆沉渊蹲在灯座旁，掌心压着膝盖。

胸骨里的裂口感没有过去，呼吸一深，里面便像有两片干硬的骨头互相磨擦。他不敢再看灯罩太久。左眼下的焦纹已经爬到颧骨，眼皮一眨，视野里便浮出几粒银灰火屑，悬在巷口、屋檐和人影之间，久久不落。

苏晚站在他身后，掌背裹着一块旧布。

布角已经被暗冷的光浸湿。她把手往袖子里收了收，另一只手扶着门框，指节发白。

“别蹲了。”她说，“仇慎的纸不是叫你守一夜灯。”

陆沉渊没有起身。

“纸上写的是卯前送达，没写谁来。”

“来谁都一样。”

“不会一样。”

他说得很轻，像怕惊动裂砖里的那点灰。

巷子两侧的门缝陆续亮起来。没有人出来，门后的影子却在移动。有人把孩子往里抱，有人将窗纸揭开一条缝，又很快放下。最靠近巷口的一户人家把自家门前的泥灯罩摘了，灯焰缩在掌心大小的陶盏里，主人捧着它退回屋内。

灯罩落地时，灰尘轻轻一震。

“这是怕被验，还是怕被收？”莫井兰问。

她从巷尾走来，怀中仍抱着那块陶片。陶片用旧布包着，布结打在外侧，没有封死。她走得不快，脚底沾着湿泥，额角有一层细汗。

“怕什么都一样。”门后有人低声说，“命籍衙要看灯，就让它看。谁出头，谁家的灯先被记。”

“那顾家的折记怎么办？”另一个声音问。

“顾家的灯还在衙里。”

“所以才不能认。”

门缝后的声音停住了。

陆沉渊抬头，看向那扇半掩的木门。门内灯焰跳了一下，像被谁用手挡住。那人没有说错。顾婶的户灯留在命籍衙，巷里没人能看见它此刻是什么模样。若今日再有人按手认灰，顾家的名字便可能被压进一笔新的续记里；若没人认，泥灯巷便会多一条无证护阵的罪名。

两边都不是他们能承担的。

巷外传来木牌碰撞声。

仇慎到了。

他只带着一名衙役模样的本地执行者，身上没有兵刃，腰间挂着一串冷金小印。那小印在昏光里一明一暗，印缝里的暗红线已经缩回去，只剩一粒针尖大的红色，伏在金边。

仇慎走到灯座前，没有立刻说话。

他的鞋尖避开了那条拖进裂缝的灰线。

“莫井兰，陶片。”

“在我这里。”莫井兰没有解布。

“要入衙封存。”

“昨日说的是携带在场。”

“昨日是昨日。”

仇慎看向陆沉渊：“今日追缴纸换了措辞。缺物，续拒验；拒交，毁证。”

莫井兰的手指在布结上停了一瞬。

陆沉渊站了起来。他起身太快，眼前一黑，掌心按住灯座，湿泥透过衣袖，冷得像一块贴在骨头上的铁。

“昨日重验，你亲眼看见陶片上的浮灰压在旧墨边。”他说。

“所以今日更要入封。”

“入封之后，谁看？”

“命籍衙的人看。”

“还是你看完，再把结果写在你自己的残页上？”

巷中传来一声细响。

不是谁应答，是某扇门后的门闩被悄悄推上了。

仇慎的脸色没有变。他伸手取下一枚冷金小印，拇指在印背上摩挲，指腹被金边磨得发白。

“陆沉渊，你已经在传核纸上留下在场认痕。你的咳灰也压在印旁。今日再阻程序，追缴纸会先落到你身上。”

“你怕它落到我身上？”

仇慎看了一眼巷口的泥灯。

“我怕它落不到该落的人手里。”

这句话说完，他自己也沉默了片刻。

远处，命籍衙方向传来一声钟响。声音隔着贫城的屋脊压过来，沉闷，只有一下，像有人在很远的地方合上了一册厚账。

仇慎把薄纸展开。

纸上没有顾家的全名，只有几列本地字迹：户灯留衙、旁观重验、陶片在场、守灯口述、巷阵无证。最末一行被冷金压过，墨色比其他地方深，纸纤维却向两侧起翘，像落印时纸下垫着不平的东西。

陆沉渊看了一眼便移开视线。

不能再识账。

左眼的焦纹正在发烫，银灰火屑从视野边缘一颗颗浮出来。仇慎的手已经搭在印上，若此时强行辨认，衙印会先认到他掌心，再认到纸。

莫井兰察觉到他的迟疑，低声道：“我来念我看见的。”

仇慎冷笑：“只念三句？”

“只念三句。”

“那三句若不足以说明陶片来源——”

“我没看见来源。”

她说得很平，声音却传过了半条巷子。

“我只看见顾家旧灰留在旧墨边，补墨灰凉、无油，断纹相反。昨日薄纸上有一层新压的灰。其余的，我没看见。”

门后有人吸了一口气。

那声音很小，仍被所有人听见。

仇慎将薄纸往前递：“你若不交陶片，这三句也不入。”

莫井兰抱紧陶片：“那便不入。”

他的眼角抽了一下。

不是怒意，像是算错了一步。

“你知不知道，旁观无证，整巷都要续记？”

“知道。”

“你家的灯也在巷里。”

“知道。”

“还要说？”

莫井兰抬头看他：“我的灯要怎么记，是我的事。你不能拿没看见的东西替我说。”

巷里忽然安静下来。

屋檐滴下一滴水，打在泥灯罩上。罩内黑点沿着细线又往下挪了一点，停在灯座裂口的上方。

仇慎没有再逼她。他把薄纸折了两折，收回袖中，转身朝巷内看去。

“还有谁旁观？”

没有人回答。

一扇门打开半寸，露出一张苍白的脸。那人望了望冷金小印，又望向自家门前捧在手里的陶盏。

“我只看见灯焰昨夜变低。”他说，“没看见你们验什么。”

“这也可记。”

“可记，不可认。”

“认与记有什么差别？”

“记的是我说过，认的是我担着。”

那张脸很快缩回门后。

另一户人家的窗纸被戳破一个小孔。有人隔着孔道：“若顾家的灯不回来，谁赔我们今日的灯油？”

“谁收了谁赔。”屋里有人说。

“你见到谁收了？”

没有回答。

陆沉渊看着那些门缝，忽然明白过来。巷民不是站在他这边，也没有站在仇慎那边。他们守的是自家灯焰，是孩子睡着后还能不能点起一盏灯，是明日衙印落到门上时，自己能不能拿出一条没有错的口述。

莫井兰愿意留下，是因为她看见了陶片上的灰。

其余人不愿意，是因为他们只看见了灯变低。

两者都是真的。

仇慎再次看向陆沉渊：“你呢？你看见什么？”

陆沉渊没有立刻回答。

他蹲下，用一根干枯的灯芯拨开灯座裂缝旁的湿泥。泥里露出一小截灰痕，颜色比裂砖深，边缘却比命籍衙印压出的灰更散。那道灰从灯座外侧伸来，在护阵纹前断开，断口平齐，像被什么冷硬之物截过。

他取出一枚薄木片，轻轻刮过灰痕。

灰没有被带走。

木片先是发白，随后边缘结出一圈冷霜。

陆沉渊的指尖一麻，眼前银灰火屑猛地聚拢。他咬住牙，没有引动识账，只凭肉眼看那道断口。

“灯座裂缝旁的灰，”他说，“在护阵纹前断开。”

仇慎问：“还能说明什么？”

“不能说明是谁落的。”

“那你说它做什么？”

“因为它和薄纸署时旁的灰不同，也和陶片补墨边的灰不同。”

莫井兰看了过来。

陆沉渊把木片放在泥地上，没有再碰那道灰。

“薄纸上的灰压在字墨上，陶片上的灰浮在旧墨边。灯座这道灰，断在护阵纹前。三处不同。它们至少没有从同一处一路拖过来。”

仇慎盯着他：“至少？”

“我只能看这么多。”

“你不是会识账吗？”

陆沉渊抬眼。

左眼里的灼热已经烧到眉骨，焦黑纹路像细裂的炭壳，疼得他半边脸发麻。他没有施术，那些灰便只是灰，冷霜、断口、压墨的痕迹，全都必须由旁人看见。

“识账不是替死人开口。”

仇慎的手指落在冷金小印上。

“你若把这句话写进本地附录，我便能记。”

“你写。”

“你承担后果？”

“在场认痕已经在我掌心。”

“那不够。”

仇慎低头，将小印按向薄纸边角。

莫井兰往前半步，挡住了陶片。

“你要加什么？”

“旁观者承认三处灰痕不同。”

“我没有说三处不同。”她说，“我只说我看见两处。”

“你刚才听见了。”

“听见不等于看见。”

仇慎的脸终于沉了下来。

他不是不明白这句话。他明白得太清楚，所以才要把听见也压成认词。只要本地纸上出现“三处灰痕不同”，下一次监督追缴时便有一段可以重新解释的空白；若纸上只有“两处”，灯座那条断痕便只能留在陆沉渊一个人的口述里。

仇慎想保住的，不只是衙门的面子。

他要保住自己还能落印的资格。

若一张本地残页被证明在次序上站不住，他前面盖过的那些印便会一张张回到他手里。那时州府那边问的不会是“谁看见了灰”，只会问“谁准你这样盖印”。

陆沉渊看着他的拇指。

那上面有一道细小的血口，是冷金边磨出来的。血没有往下流，刚冒出来便被印缝里的暗红吸住，细得像一根绷紧的线。

“仇慎。”陆沉渊说，“你可以记我说的三处，但不能替莫井兰添第四句。”

仇慎望着他，许久没有落印。

巷内一户人家的门终于完全打开。顾婶站在门里，脸色比昨夜更白。她手里没有户灯，只有一块折过的旧布。她看了看仇慎，又看向灯座裂缝。

“我家的灯不在这里。”她说，“我只能认灯被带走前，焰尖是细线。谁若让我认别的，我不认。”

仇慎握着薄纸的手紧了紧。

“你们都很会保自己。”

“你也一样。”顾婶说。

这回没有人关门。

不是因为巷民突然信了谁。只是这句话落地之后，每个人都听见了自己的害怕，也听见了仇慎的害怕。两种害怕挤在同一条窄巷里，谁也没有退开。

仇慎收起小印。

“今日不收陶片。”

莫井兰没有松手。

“但你们三人，”他看着陆沉渊、莫井兰和顾婶，“明日午前到命籍衙。顾家户灯仍留衙。缺一，按拒验续记。”

“今天不是卯前监督？”陆沉渊问。

“今天只是送达。”

仇慎把薄纸递给他。

陆沉渊没有接。

纸边悬在两人之间，纸纤维上的冷灰细细聚拢，避开了落印的位置。仇慎看见了，手腕微不可察地抖了一下。

最后是苏晚伸手接过。

她的掌背刚碰到纸，布下便透出暗冷光。她没有缩回去，只把纸折好，压在门槛上。

“我不验灯。”她说。

仇慎看向她。

“我知道。”

“你也可以续记。”

“我知道。”

“别动巷里人的灯。”

仇慎没有应声。

他转身走向巷外，冷金小印在腰间轻轻相撞。那串声响传出去很远，灯罩里的黑线随之又动了一下，沿着灯座裂口向外牵，牵到半寸处便猛地缩回。

陆沉渊眼前一暗，身子晃了晃。

苏晚立刻扶住他。

“别看了。”

“我没看。”

“你的眼睛在流黑屑。”

陆沉渊抬手摸了一下，指腹沾上一层焦黑。他将那点黑屑擦在旧砖上，砖面没有温度，黑屑却冒出一缕细烟。

巷外，仇慎的脚步停住。

没有回头。

“明日午前，莫井兰带陶片。”他说，“陆沉渊带你的口述。顾婶带她自己的所见。”

“若你们不来，”声音压着风传回来，“新的监督追缴纸会先到你们各自门上。”

他走后，巷子里的门缝仍未合拢。

有人问：“三处灰痕不同，真能让顾家的灯回来吗？”

陆沉渊看着泥灯座。

“不能。”

“那我们认它有什么用？”

“让下一张纸不能只写一处。”

没人说话。

莫井兰把陶片重新系紧，布结仍旧留在外侧。顾婶退回门内，却没有关门。苏晚弯腰捡起那张薄纸，纸面上的冷灰已经聚成一道极细的空白，正好绕开仇慎的印落点，向顾家户灯留衙的字样延伸。

延伸到最后，断了。

陆沉渊伸手想接，指尖刚靠近纸面，左眼便骤然刺痛。

他停下。

这一次，他没有施术。

只用肉眼看见，那道空白没有指向命籍衙，也没有指向顾家。它停在“陶片在场”四个字旁，像一条只走到本地门槛的错账链。

链子是真的。

链外是什么，仍没人看见。

远处又传来一声钟响。

命籍衙的钟声穿过贫城，落到泥灯巷上。巷口的火星被风压低，几乎熄灭。屋内有人将自家灯盏往门后挪了挪；有人留下门缝，继续看着那张纸；有人已经开始收拾明日午前要带的旧衣和口述。

苏晚把薄纸塞进陆沉渊手里。

“拿好。”

纸很冷。

掌心旧印在纸边碰到的一刻，暗红细线从皮下浮出，绕过指根，结成一个尚未落完的圈。疼痛沿着掌骨往上钻，他弯了一下手指，没让纸掉地。

巷外，仇慎带来的脚步声重新响起。

这一次，比刚才更近。

新的监督追缴纸还没贴上门。

命籍衙的人已经折返到了巷口。

## Required JSON
```json
{
  "chapter_id": "chapter-0007",
  "artifact_kind": "draft",
  "artifact_sha256": "098bda98b2f595429a2166fe690978a14324a3cb362c27c11138e8c3f1062f4a",
  "context_sha256": "9d8e5db9fddcde2d205997b10a07e266907837128da6263075ebce51e1b4e101",
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
