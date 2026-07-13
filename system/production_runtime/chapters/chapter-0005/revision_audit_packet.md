# NRL Antigravity Chapter Audit v0.20

Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.
Do not rewrite prose. Return one JSON object only using the exact binding hashes.

## Compact Context
{"chapter_id": "chapter-0005", "dramatic_purpose": "命籍衙以程序理由收紧复核，主角用残页时间差证明一项局部记录无法自洽。", "must_keep": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "不能把程序漏洞直接等同于完整真相；必须留下追查后果。"], "must_avoid": ["不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"], "assets": [{"asset_id": "character_lu_chenyuan", "display_name": "陆沉渊", "family": "characters", "lifecycle_state": "active", "constraints": ["Does not transfer a life-cost to uninvolved residents.", "Each use leaves bodily evidence or increases pursuit risk.", "His mother debt and the lane protection array remain non-negotiable constraints.", "At 燃命境初成 he may only recognize ordinary life marks and local ash-trace mismatches; personal-page reading, chain tracing, covenant glimpses, return-fire casting, and seal breaking remain blocked pending validated advancement."], "relationships": [{"target_id": "bond_mother_su_wan", "relation_type": "son_bound_by_lifespan_debt"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_acquire_after_registered_transition"}, {"target_id": "faction_mudlamp_lane", "relation_type": "protects_and_is_bound_to"}, {"target_id": "technique_embertrace_return", "relation_type": "may_unlock_after_lamp_and_progression_gates"}, {"target_id": "technique_ledger_recognition", "relation_type": "uses_basic_local_ash_trace_scope_of"}]}, {"asset_id": "npc_su_wan", "display_name": "苏晚", "family": "npcs", "lifecycle_state": "active", "constraints": ["苏晚是能拒绝错误救法的行动者，不是可消耗的动机。", "她绝不接受以邻里命火、孩童寿数或无辜者命页抵消自己的寿债。", "她的命灯裂纹、冷灰气息和掌背失温须以感官后果呈现，不以抽象说明替代。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "bond_mother_su_wan", "relation_type": "embodies"}, {"target_id": "faction_mudlamp_lane", "relation_type": "mutual_aid_member_of"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "raises_restraint_threshold_for"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "is_counted_down_by"}]}, {"asset_id": "npc_registrar_qiu_shen", "display_name": "仇慎", "family": "npcs", "lifecycle_state": "active", "constraints": ["仇慎只能掌握本地残页与寿印权限，不能成为无所不知的阴谋解释者。", "其每一次施印必须留下可辨的冷金印痕或命灯失色，并制造可追责的现场后果。", "他可恐惧上级追责，但不能因恐惧自动洗白。", "其独立义务是保住本地呈印资格并避免州府问责；当公开证据使继续施印超出本地权限时，可拖延、议价或退回追缴令，但不得因此获得无证据洗白。"], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "serves_as_registrar_for"}, {"target_id": "character_lu_chenyuan", "relation_type": "supervises_and_targets"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "forwards_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "pressures_with_seals"}]}, {"asset_id": "npc_mo_jinglan", "display_name": "莫井兰", "family": "npcs", "lifecycle_state": "active", "constraints": ["Her knowledge is partial oral memory, never omniscient exposition.", "Helping preserve testimony exposes her remaining life-fire to collection."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "keeps_its_night_lamps"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "witnesses_surface_sign"}]}, {"asset_id": "bond_mother_su_wan", "display_name": "苏晚与陆沉渊的垫寿亲缘", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["The mother is an active moral presence, not expendable motivation.", "Any attempt to relieve her debt must carry an exposure, bodily, or communal consequence."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "deadline_is_tracked_by"}]}, {"asset_id": "bond_mudlamp_lane_trust", "display_name": "泥灯巷共灯之信", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["共同体信任不是主角可提取的资源；巷民有拒绝、质询和撤回见证的权利。", "信任提升必须来自共同承担、返还寿火或公开承担反噬，而非主角单方面胜利。", "任何高风险行动都须显示巷民的恐惧、选择与实际保护行为。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "binds_to_community"}, {"target_id": "faction_mudlamp_lane", "relation_type": "measures_mutual_aid_of"}, {"target_id": "npc_su_wan", "relation_type": "is_guarded_by_moral_boundary_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "conditions_witnessed_return"}]}, {"asset_id": "faction_mudlamp_lane", "display_name": "泥灯巷", "family": "factions", "lifecycle_state": "active", "constraints": ["The mutual-aid network cannot become expendable fuel for a single hero.", "Every communal protection act worsens the protection array's visible lifespan cracks or attracts collectors."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "contains_registered_acquisition_site_for"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "is_tracked_by"}]}, {"asset_id": "faction_life_registry_office", "display_name": "命籍衙", "family": "factions", "lifecycle_state": "active", "constraints": ["其压迫必须通过寿印、命灯、命审台和具体家庭后果显形，不写成现实机构讽刺。", "本地权限只能冻结、登记、送审与申请追缴，不能解释州府或天庭的完整真相。", "命审程序必须成为可被证据、见证和法术反打的冲突场域。"], "relationships": [{"target_id": "npc_registrar_qiu_shen", "relation_type": "employs"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "issues_local_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "assesses_and_pressures"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "contests"}]}, {"asset_id": "technique_ledger_recognition", "display_name": "识账术", "family": "techniques", "lifecycle_state": "active", "constraints": ["At character_lu_chenyuan's current 燃命境初成 stage, the active scope is limited to ordinary life marks and local copy-level ash-trace mismatches visible in the present evidence.", "Personal-page reading is locked to a validated 识账境 transition; chain tracing requires a later audited proof, and ancient-covenant glimpses remain blocked until an independently validated advanced transition and artifact evidence exist.", "The technique cannot directly read minds, predict outcomes, or produce a complete answer at any stage.", "施展后瞳孔浮出焦黑纹路、视野残留银灰火屑，并提升被寿印锁定的风险。", "所有判断须由可见痕迹或受害者见证复核，不能以主角独白定案。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "is_practiced_by"}, {"target_id": "technique_embertrace_return", "relation_type": "verifies_targets_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "increases"}, {"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "cannot_reveal_before_validated_advanced_progression"}]}, {"asset_id": "foreshadowing_cinder_seal_rain", "display_name": "灰雨印痕", "family": "foreshadowing", "lifecycle_state": "active", "constraints": ["The clue appears as sensory supernatural residue, not paperwork.", "Investigating it burns the investigator and raises collection exposure before any revelation."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "is_revealed_by"}, {"target_id": "npc_mo_jinglan", "relation_type": "is_remembered_by"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "payoff_tracks"}]}, {"asset_id": "state_ledger_protagonist_strain", "display_name": "陆沉渊命火与心魄承压", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["状态只记录可叙事化的命火、骨裂、瞳纹、冷灰与心魄恍惚，读者文本不得呈现工程字段。", "任何恢复都不能自动解除母亲寿债、半寿身份或既有追缴。", "承压过界时主角应失去施术窗口或需要他人阻止，而非获得无代价爆发。", "空寿状态是施术锁定与认知承压：不得提升战力；继续行动必须先支付已登记的寿火扣减，并失去至少一个施术或判断能力，恢复须停术和外部看护。", "This asset is the sole writer of sanity_level, caster_lifefire_stability, bone_fissure_severity, eye_pattern_burn, and cold_ash_cough_frequency; it may not write exposure or mother-lamp state."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "tracks_strain_for"}, {"target_id": "technique_ledger_recognition", "relation_type": "is_decreased_by"}, {"target_id": "technique_chain_deflection_seal_breaking", "relation_type": "is_worsened_by"}, {"target_id": "bond_mother_su_wan", "relation_type": "raises_family_risk_for"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_half_life_registry_exposure", "display_name": "半寿残籍暴露", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of half_life_registry_exposure; techniques, artifacts, NPCs, and other ledgers may request a delta but may not write the value directly.", "Exposure never decreases merely because evidence succeeds or life-fire returns; reduction requires a separately evidenced legal, masking, or withdrawal transition.", "Threshold crossings must change pursuit or access state before the atomic transaction can close.", "The Cluster 5 evidence-record exchange requests exactly +10 percentage points within the 0-100 bound and closes only with the protagonist-owned record debit under the same transaction ID; child, resident, and third-party life-fire prices are rejected."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "solely_tracks_registry_exposure_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "npc_cluster5_black_market_transaction_role", "relation_type": "is_increased_by_transaction_with"}]}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "display_name": "苏晚命灯裂纹倒计时", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mother_life_lamp_cracks and the mother-life-debt countdown.", "A communal return or protagonist recovery cannot automatically heal a crack or cancel the unresolved mother debt.", "Any technique transaction that affects Su Wan must record the crack/countdown delta here before closing."], "relationships": [{"target_id": "npc_su_wan", "relation_type": "solely_tracks_lamp_cracks_for"}, {"target_id": "bond_mother_su_wan", "relation_type": "provides_countdown_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "cannot_be_auto_cancelled_by"}]}, {"asset_id": "state_ledger_mudlamp_array_integrity", "display_name": "泥灯巷护阵完整度", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mudlamp_array_integrity; returned fire, resident reserve, and caster strain remain independently owned.", "Array integrity cannot rise from returned fire alone; witnessed repair or stabilization must be recorded.", "Below the registered safety line, lamp activation and return-fire casting fail closed rather than granting emergency power."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_array_integrity_for"}, {"target_id": "artifact_ashlight_cup", "relation_type": "gates_acquisition_and_activation_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_resident_lifefire_reserve", "display_name": "泥灯巷住户命火储备", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of resident_lifefire_reserve; the reserve is never protagonist inventory or an automatic communal resource.", "Every debit requires named consent and preserves the right to refuse or withdraw before transaction closure.", "No black-market price, technique cost, or artifact awakening may debit children, uninvolved residents, or an unspecified crowd."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_consented_reserve_for"}, {"target_id": "bond_mudlamp_lane_trust", "relation_type": "requires_refusal_and_consent_rights_from"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_supply_consented_watchfire_for_awakening"}]}, {"asset_id": "state_ledger_poorcity_returnfire", "display_name": "泥灯巷归火余量", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["A positive return never cancels the mother debt or the protection array burden automatically.", "Every gain must name whose life-fire returned and whose visible backlash or exposure increased.", "This asset is the sole writer of returned_miscollected_lifefire and may not write caster strain, registry exposure, array integrity, resident reserve, or mother-lamp state."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "measures_survival_pressure_for"}, {"target_id": "technique_embertrace_return", "relation_type": "is_changed_by"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_affected"}]}, {"asset_id": "state_ledger_revealed_account_errors", "display_name": "已揭示错账记录", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of revealed_account_errors; evidence, return-fire, and outline assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source evidence and at least one independently owned return-fire, exposure, reputation, pressure, or mystery consequence.", "No inferred or unverified account error may be counted, and no proof may create an implicit credit or debit."], "relationships": [{"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_faction_pressure", "display_name": "既有势力压力", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of faction_pressure; faction, NPC, and scene assets may request but may not apply a mutation.", "Every mutation must identify an existing source asset and settle atomically with exposure, public reputation, or revealed-error consequences.", "No new faction, location, or plot event may be created to justify a pressure change."], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "faction_prefecture_life_treasury", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_public_reputation", "display_name": "公开认知状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of public_reputation; all other assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source, reason, before/after state, and at least one independently owned consequence ledger.", "No success, witness, or exposure event changes reputation implicitly or closes without its peer ledger result."], "relationships": [{"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_unresolved_mysteries", "display_name": "未解账目疑点", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of unresolved_mysteries; foreshadowing and outline assets may request but may not apply a mutation.", "Every add, reclassification, or closure requires an explicit atomic transaction with a revealed-error or map-boundary consequence.", "No new mystery, answer, backstory, or plot event may be created by this ledger."], "relationships": [{"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "tracks_only_registered_questions_from"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_map_unlock_status", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_map_unlock_status", "display_name": "既有地图边界解锁状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of map_unlock_status; references to existing map boundaries may request but may not apply a transition.", "Every transition is atomic and must preserve unresolved boundaries while recording any exposure consequence.", "The ledger cannot introduce a location or unlock a boundary absent from the canonical outline."], "relationships": [{"target_id": "artifact_prefecture_transit_registry_seal", "relation_type": "requires_validated_boundary_evidence_from"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}], "prior_settlements": [{"chapter_id": "chapter-0001", "accepted_revision_sha256": "79d46dc564388fc32d8bae5b8fdc5ebd7a3dc2412e2174f8558844cad1fda874", "state_deltas": [{"fact_id": "chapter-0001-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": null, "after": "顾家的折记暂缓，午后再核"}, {"fact_id": "chapter-0001-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.local_enforcement_status", "operation": "set", "before": "顾家折记待按册落印核验", "after": "顾家折记暂缓至午后复核"}, {"fact_id": "chapter-0001-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": null, "after": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索"}, {"fact_id": "chapter-0001-information-foreshadowing-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨印痕未在本章现场显现", "after": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小"}, {"fact_id": "chapter-0001-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "寿籍司尚未进入泥灯巷核验", "after": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后"}, {"fact_id": "chapter-0001-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "眼尾仅有极淡、藏在睫毛下的焦黑细纹", "after": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0002", "accepted_revision_sha256": "356320d82944a61555f663908889d71d0afff3c35b5fa3c0ede592ef0ecfaeaf", "state_deltas": [{"fact_id": "chapter-0002-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家的折记暂缓，午后再核", "after": "顾家折记继续暂缓，三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "寿籍司完成本次到巷核验并离开，顾家复核被排至午后", "after": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "operation": "set"}, {"fact_id": "chapter-0002-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.procedural_observation_of_lu_chenyuan", "before": null, "after": "陆沉渊被要求往后残籍复核在场；传核缺席按拒验记", "operation": "set"}, {"fact_id": "chapter-0002-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "识别出顾家“折三”补墨处的灰痕与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "operation": "set"}, {"fact_id": "chapter-0002-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": null, "after": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "operation": "set"}, {"fact_id": "chapter-0002-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "顾家“折三”补墨与顾婶命灯寿痕不属同源，属本地账目错位线索", "after": "错位线索被记为本地复核附录，但不作为改账依据", "operation": "set"}, {"fact_id": "chapter-0002-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "before": "灰雨落在陆沉渊与顾婶皮肤上，形成暗红骨上印痕，并使旧阵纹残暖缩小", "after": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "operation": "set"}, {"fact_id": "chapter-0002-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": null, "after": "顾家折记三日内再次复核", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "眼角焦黑细纹因辨认册页灰痕而加重至无法遮掩", "after": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": null, "after": "识账后当场咳出一小片冷灰", "operation": "set"}, {"fact_id": "chapter-0002-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": null, "after": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "operation": "set"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0003", "accepted_revision_sha256": "8167366cd6811f13f63105eb5e0644bccb5c069e6081e29e4a66150554158b3f", "state_deltas": [{"fact_id": "chapter-0003-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "operation": "set", "before": "被要求往后残籍复核在场；传核缺席按拒验记", "after": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来"}, {"fact_id": "chapter-0003-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄"}, {"fact_id": "chapter-0003-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_witness_material", "operation": "set", "before": null, "after": "暂带顾家补墨灰屑陶片作为守灯见证物"}, {"fact_id": "chapter-0003-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_local_lamp_assessment", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "验灯显示命灯失温、焰尖缩成细线，手背红点裂开并渗出暗冷光"}, {"fact_id": "chapter-0003-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "完成顾家午后复核并留存本地复核附录，顾家折记维持暂缓", "after": "顾家附录暂封并列入三日内再验，苏晚户灯旁证暂不作改账凭据"}, {"fact_id": "chapter-0003-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "顾家折记三日内再次复核", "after": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证"}, {"fact_id": "chapter-0003-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "在顾家户灯寿纹、折册补墨灰痕及莫井兰守灯见证相互比对下，形成“补墨灰痕与户灯寿纹错位”的本地复核附录内容", "after": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔"}, {"fact_id": "chapter-0003-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "莫井兰以可撤回口述作证，拒绝献灯或抵命；顾婶以自身所见备录", "after": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界"}, {"fact_id": "chapter-0003-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "operation": "set", "before": "陆沉渊每次施术的反噬尚未被苏晚在本次复核中当场看见", "after": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹"}, {"fact_id": "chapter-0003-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "operation": "set", "before": "错位线索被记为本地复核附录，但不作为改账依据", "after": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据"}, {"fact_id": "chapter-0003-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰粒再次落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线"}, {"fact_id": "chapter-0003-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "顾家折记继续暂缓，三日内再次复核", "after": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "识账后焦黑纹路自眼尾向下爬，眼角皮肤焦裂并蹭下黑屑", "after": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": null, "after": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感"}, {"fact_id": "chapter-0003-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "识账后当场咳出一小片冷灰", "after": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印"}, {"fact_id": "chapter-0003-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "operation": "set", "before": "陆沉渊咳出的灰已被衙印沾认，成为传核与拒验记的程序性锁定迹象", "after": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸"}, {"fact_id": "chapter-0003-physical-state-mother-lamp-001", "asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "operation": "set", "before": "灰粒落在苏晚失温的手背，留下针尖大的红点", "after": "灰雨中苏晚命灯验焰缩成细线，手背红点裂开渗出暗冷光；验灯未被暂熄"}], "resolved_audit_ids": []}, {"chapter_id": "chapter-0004", "accepted_revision_sha256": "e3ed91078715d2b3540da38987cb7db63bcd559ea1e320fb0b07a550d091b6f7", "state_deltas": [{"fact_id": "chapter-0004-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_intent", "operation": "set", "before": "已签传核纸认定在场，并被要求明日辰时携顾家与守灯口述再来", "after": "确认明日辰时到场，但不替任何住户陈述未亲见之事"}, {"fact_id": "chapter-0004-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "operation": "set", "before": "暂带顾家补墨灰屑陶片作为守灯见证物", "after": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句"}, {"fact_id": "chapter-0004-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_refusal_statement", "operation": "set", "before": null, "after": "拒绝以自己抵命，也拒绝以泥灯巷住户命火填补自身裂纹"}, {"fact_id": "chapter-0004-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.latest_local_notice", "operation": "set", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席"}, {"fact_id": "chapter-0004-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "operation": "set", "before": null, "after": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩"}, {"fact_id": "chapter-0004-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "operation": "set", "before": "明日辰时顾家与守灯口述须到场，缺一人按拒验续记；灰物有损视同毁证", "after": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记"}, {"fact_id": "chapter-0004-faction-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "operation": "set", "before": null, "after": "未有住户命火实际投入巷口泥灯；住户保留各自关门、留缝或守灯的选择"}, {"fact_id": "chapter-0004-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "operation": "set", "before": "新落灰、顾婶验灯红痕与册角补墨灰痕之间存在半指宽冷灰空白；验灯红痕仅在靠近命籍衙印处留下完整一笔", "after": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展"}, {"fact_id": "chapter-0004-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "operation": "set", "before": "顾婶同意莫井兰仅记录其所见；莫井兰确认灰与顾家户灯旧灰同味、补墨灰凉而无油且断纹相反，并保留不知来源的口述边界", "after": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片"}, {"fact_id": "chapter-0004-hook-cinder-seal-rain-001", "asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "operation": "set", "before": "灰雨落入命籍衙后院，并有一粒嵌进冷金小印缝里，随仇慎离开拖出暗红细线", "after": "巷口泥灯罩内壁留下不下沉的黑点；薄纸上的冷灰沿纸纤维聚成空白，避开命籍衙印落点"}, {"fact_id": "chapter-0004-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "operation": "set", "before": "午后复核结束，顾家附录及传核纸进入归档/封存程序，下一次本地监督定于明日辰时", "after": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "operation": "set", "before": "再次识账后左眼下焦纹裂至颧骨，签传核时又向下裂一寸并掉落黑屑", "after": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "operation": "set", "before": "本次再次识账后先咳出冷灰盖住“未详”，随后又咳出一片冷灰沾住传核纸衙印", "after": "本次夜间识账后再次咳出冷灰，落在巷口泥地"}, {"fact_id": "chapter-0004-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "operation": "set", "before": "冷金小印擦过掌心后，掌骨深处发出细响，胸骨随呼吸摩擦出裂口感", "after": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声"}], "resolved_audit_ids": []}]}

## Rule Stack
{"version": "0.22", "chapter_id": "chapter-0005", "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "priority_order": ["safety_and_originality", "canonical_story_bible", "volume_outline", "accepted_state_settlements", "creation_asset_constraints", "chapter_must_keep_and_must_avoid", "anti_ai_style_evidence"], "hard_rules": ["no source-work names, scenes, signature systems, or prose imitation", "no untracked power, relationship, location, item, or timeline changes", "all benefits carry an embodied, relational, or systemic cost", "reader-facing prose contains no runtime or database vocabulary", "不得引入未登记人物、势力、器物、地点或能力。", "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。", "不得进行公开审判、高阶斗法、永久清偿或越级胜利。", "不得把审查建议、推测或未观察事实写成状态变化。"], "chapter_rules": ["陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。", "残命灯盏不得取得、唤醒、持有、激活或使用。", "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。", "不能把程序漏洞直接等同于完整真相；必须留下追查后果。"], "scene_constraints": ["舞台限于贫城、泥灯巷与命籍衙的本地压力范围。", "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。", "每次识账都必须带来可见代价或程序性暴露。", "结尾只推进到下一次本地程序追缴或监督，不得换图。"]}

## Compilation Trace
{"version": "0.22", "chapter_id": "chapter-0005", "selected_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "explicit_asset_ids": ["character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors", "state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status"], "dependency_asset_ids": [], "excluded_asset_count": 22, "selection_reason": "explicit chapter intent requirements plus atomic transaction peers", "canonical_hashes": {"borrowed_heaven_life_account_bible": "81575478a441852f18d451e9967245bbfce11d60cddd3af24e9b6565955e0604", "borrowed_heaven_volume1_outline_tree": "1f12fe8ad3262876eb533d40c94ad02abb90b95b38de387d339917fce9184648", "project_assets.v0.2": "90dbcf17d769e8a985fc87880a4382018c30133a2a53f82c3826636c8ed1dc61"}, "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "prior_settlement_count": 4}

## Observed Facts
{"chapter_id": "chapter-0005", "draft_sha256": "e6b9d57e104dd39b1541edd20e5cc8d71aebf81d2eb27baa4fe199ca1a443396", "facts": {"characters": [{"fact_id": "chapter-0005-character-lu-chenyuan-001", "asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "before": "确认明日辰时到场，但不替任何住户陈述未亲见之事", "after": "已到场完成本地复核，并被要求午后护阵旁观重验继续在场；凡本地残页复核不得缺席", "evidence": "仇慎称“此后凡本地残页复核，你不得缺席”，并在窄纸中列明陆沉渊午后在场。"}], "npcs": [{"fact_id": "chapter-0005-npc-registrar-qiu-shen-001", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "before": "顾家附录暂封，灰物由莫井兰暂带，三日内随顾家复核再验；苏晚验灯不熄", "after": "顾家附录继续封存；守灯前三句保留，未知来源不入；护阵旁观追加残页改列次序待核", "evidence": "仇慎宣布“顾家附录继续封……护阵旁观不作无证结案，改列次序待核”。"}, {"fact_id": "chapter-0005-npc-registrar-qiu-shen-002", "asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_local_notice", "before": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席", "after": "已发出今日午后泥灯巷护阵旁观落点重验通知，并列明顾家户灯留衙、莫井兰携陶片、陆沉渊到场的条件", "evidence": "仇慎在窄纸上落印后宣布“今日午后，命籍衙到泥灯巷重验护阵旁观落点”。"}, {"fact_id": "chapter-0005-npc-mo-jinglan-001", "asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "before": "决定携陶片赴明日辰时复核，但不交出陶片；若仇慎索取则不再陈述后半句", "after": "已在复核中陈述顾家旧灰、补墨灰凉无油及断纹相反三句；陶片仍暂带，午后须携带在场", "evidence": "莫井兰逐句陈述后，仇慎称“仍由你暂带”，并要求“莫井兰携陶片在场”。"}, {"fact_id": "chapter-0005-npc-su-wan-001", "asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "before": null, "after": "午后可拒绝验灯，但不得替陆沉渊认灰", "evidence": "窄纸明载“苏晚可拒绝验灯，不得替他认灰”。"}], "locations": [{"fact_id": "chapter-0005-location-mudlamp-lane-001", "asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "before": "巷口泥灯焰尖降低、灯座裂为两道，墙上护阵纹短暂亮起后复暗；仅以旧砖和扫帚暂时扶正灯座与灯罩", "after": "护阵旁观落点被列为今日午后重验对象，尚未完成复核或修补", "evidence": "仇慎下令“今日午后，命籍衙到泥灯巷重验护阵旁观落点”。"}], "factions": [{"fact_id": "chapter-0005-faction-life-registry-office-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "after": "辰时复核已完成并将护阵旁观追加残页列为次序待核；午后转入泥灯巷重验监督", "evidence": "仇慎将右页另压台内，宣布改列次序待核，随后下达午后重验。"}, {"fact_id": "chapter-0005-faction-life-registry-office-002", "asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "before": "明日辰时顾家户灯、守灯口述与泥灯巷护阵旁观须到场；无人认领旁观则按无证护阵记", "after": "今日午后在泥灯巷重验护阵旁观落点；顾家户灯留衙至验毕，莫井兰携陶片、陆沉渊到场，人或物缺一按拒验续记", "evidence": "仇慎在窄纸中写定午后重验及缺席后果。"}], "artifacts": [], "techniques": [{"fact_id": "chapter-0005-technique-ledger-recognition-001", "asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "before": "巷口泥灯座裂缝灰在靠近命籍衙印痕处折转，留下半指宽冷灰空白，未沿护阵纹延展", "after": "顾家附录补墨灰位于冷金印下；护阵旁观残页署时旁灰浮在墨上且被冷金截断，右页存在无法与“昨夜追加”同时自证的局部次序", "evidence": "陆沉渊识账看见两页灰痕与墨锋、冷金印的覆盖先后不同，并明确只指出“至少有一处次序不对”。"}], "relationships": [{"fact_id": "chapter-0005-relationship-mudlamp-lane-trust-001", "asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "before": "莫井兰与顾婶均决定赴核，但各自限定见证范围；顾婶拒绝让孩童命灯受验，莫井兰拒绝代签未知来源或交出陶片", "after": "莫井兰保留前三句限于所见的陈述，拒绝补入未知来源；午后继续以暂带陶片的限定方式到场", "evidence": "莫井兰说完前三句后不向空栏添字，仇慎确认陶片仍由她暂带并要求午后携带在场。"}, {"fact_id": "chapter-0005-relationship-mother-su-wan-001", "asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "before": "苏晚看见陆沉渊掌心的青白印和左眼下无法遮掩的焦黑裂纹", "after": "苏晚在识账反噬中按住陆沉渊腕上发抖的手，未替他认灰或触碰残页", "evidence": "识账后苏晚将他的手按回身侧；窄纸同时明确她不得替陆沉渊认灰。"}], "emotions": [], "information": [{"fact_id": "chapter-0005-information-revealed-account-errors-001", "asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "before": "附录已并列保有冷灰、顾婶掌背红点及莫井兰限于所见的口述，仍未成为改账依据", "after": "护阵旁观追加残页被确认存在局部次序疑处，列为待核；未被认定为顾家折记错误、护阵追加无效或改时原因的证明", "evidence": "仇慎承认“局部次序有疑”，同时否定其当然等同于顾家折记有误或护阵追加无效。"}], "hooks": [], "timeline": [{"fact_id": "chapter-0005-timeline-local-enforcement-001", "asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "before": "命籍衙已于夜间送达明日辰时的护阵旁观追加通知，下一次本地监督仍定于明日辰时", "after": "辰时复核后，程序推进至今日午后的泥灯巷护阵旁观落点重验", "evidence": "复核结束时仇慎以缺角冷金印落下窄纸，定下今日午后重验。"}], "physical_state": [{"fact_id": "chapter-0005-physical-state-protagonist-strain-001", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "before": "本次识账后焦黑纹路再向下爬，左眼疼胀并持续掉落黑屑", "after": "识账时左眼下焦纹沿颧骨再绽开一小截，皮肉现烧焦气味并落下黑屑；银灰火屑未散", "evidence": "识账后焦纹“沿颧骨又绽开一小截”，黑屑落台，结尾仍写其眼中银灰火屑未散。"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-002", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "before": "本次夜间识账后再次咳出冷灰，落在巷口泥地", "after": "本次识账后咳出冷灰落在命审台角，并被冷金小印压入在场认痕", "evidence": "冷灰顶上喉咙后落在台角，仇慎随即用小印压住并称附入在场认痕。"}, {"fact_id": "chapter-0005-physical-state-protagonist-strain-003", "asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "before": "识账后胸骨裂口感使呼吸受阻，撑灯座时掌骨出现摩擦声", "after": "薄纸衙印牵动掌心旧印后掌骨再响，胸口裂口感骤紧，需扶住台沿喘息", "evidence": "暗红印线勒住掌心旧印，掌骨再响，胸口裂口感收紧，陆沉渊扶住台沿。"}, {"fact_id": "chapter-0005-physical-state-registry-exposure-001", "asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "before": "新咳出的冷灰沾住已签传核纸衙印，使印痕泛出暗红；仇慎当场要求留下该纸", "after": "识账所咳冷灰被冷金小印压入在场认痕，薄纸衙印牵出暗红印线锁到陆沉渊掌心旧印", "evidence": "仇慎称“识账落灰，附入在场认痕”；小印亮起后暗红从薄纸衙印勒至掌心旧印。"}], "naming": []}}

## Prose
辰时的光还没翻过贫城低矮的屋脊，命籍衙门前两扇旧门已经合严。

门缝里挤进一线灰白，落在命审台边。顾家的户灯放在台下，灯芯压得很低，青焰细得像一根针。莫井兰守在灯旁，双手拢进袖中，那块沾着补墨灰屑的陶片始终没露出来。

苏晚站在陆沉渊身侧，没挨着他，只隔着半步。她掌背藏在衣褶里，指节一动，袖口下便漏出一点暗冷的红光。

仇慎坐在台后，先把昨夜送往泥灯巷的薄纸压在左手边，又从封存的顾家附录里抽出两张残页，分开摆在面前。

纸角都有缺口，缺口被冷金印压住。细金沿纸纤维蜿蜒，像霜爬上枯草。

“今日只核三件。”仇慎道，“顾家户灯是否到场，守灯口述是否照原言复述，泥灯巷护阵旁观是否有人认领。”

陆沉渊看向台下：“灯到了。”

“灯到，不等于户认。”

“我只认它在这里，不替顾家认别的。”

仇慎指腹按住残页一角。冷金落进纸里，页角原有的灰黄一下褪尽，白得刺眼。

“记，拒代户认。”

莫井兰把袖口攥得更紧。

仇慎将第二张残页推到她面前，只推到她够不着的位置。

“照原言说。少一句，按改口；多一句，按添证。陶片未经过衙印验照，后半句不入册。”

莫井兰望着那张纸，沉默片刻。

昨夜她已经说过顾家旧灰的气味，也说过补墨灰发凉、无油，断纹与户灯寿纹相反。可那些话落到残页上，成了窄窄几栏，每栏后都留着一块冷金空白，仿佛专等她伸手去填。

她没有往前。

“我见过顾家户灯旧灰。”她道，“陶片上的灰和它同味。补墨处的灰凉，无油，断纹相反。灰从哪里来，我不知道。”

仇慎拿起冷金小印，在前三栏逐一压下。

第一印落时，顾家户灯的焰尖褪去一丝青色。

第二印落时，灯罩里浮起湿冷白雾。

第三印压实，焰火只剩米粒大，灯芯里发出极轻的一声噼啪。

苏晚望着那盏灯，没有开口。她抬手横在陆沉渊胸前，隔着衣料，指尖冷得他呼吸一滞。

“别看。”她低声说。

陆沉渊没答，目光仍停在那三枚印上。

仇慎留着最后一栏空白：“未知来源，不记为错账证词，只记守灯人未见。”

“我本来就没说我见过来源。”莫井兰道。

“所以那一栏与你无关。”

“既无关，就别留在我的话后头。”

仇慎抬起眼：“附录按句归列，不按人心归列。”

莫井兰退了半步。她没撤回前三句，也没向空栏里再添一个字。

仇慎转向陆沉渊：“护阵旁观。”

“昨夜我在泥灯巷口。”陆沉渊道，“泥灯焰尖降低，灯座裂成两道。墙上旧阵纹亮过一次，又暗了。没人往灯里添命火。灯座用旧砖垫住，灯罩用扫帚扶正。”

“你碰过灯座？”

“碰过。”

“看过裂缝里的灰？”

苏晚横在他胸前的手慢慢收紧。

陆沉渊没有躲开：“看过一眼。”

仇慎抽出昨夜那张薄纸，平铺在台上。

“旁观者接触护阵，且曾以识账辨灰。护阵之变，不再只作远观口述。”他顿了顿，“你既看过，今日便须说明所见。说不清，按扰验；说出本地灰痕以外的事，按妄识残籍。”

“他昨夜已经咳过灰。”苏晚道。

“所以衙印认得他。”

仇慎将薄纸向前推了半寸。

纸上的暗红衙印微微收缩，陆沉渊掌心那道青白旧印立刻发麻。掌骨深处响了一声，他五指不由蜷起，胸骨像夹进一片薄刃，随呼吸来回刮擦。

莫井兰看见他左眼下的焦纹，脚尖往前挪了些，随即又停住。袖中陶片碰上骨节，发出一声轻响。

“我只说现在能看见的。”陆沉渊道。

“准。”

仇慎把两张残页移到薄纸旁。左页记顾家附录暂封，署时在昨日午后；右页记护阵旁观追加，署时在昨夜。两道冷金印都完整，纸上看不出半点破口。

陆沉渊先看顾家户灯，又看莫井兰袖口露出的一线陶色，最后将目光压回台面。

识账术起时，台上没有异响。

左眼像被粗砂狠狠磨过，纸纹在他眼中骤然深下去。墨字边缘浮起细小的银灰火屑，火屑没变成别的字，也没替他掀开封页下的内容，只贴着眼前的灰痕发颤。

昨夜薄纸上的冷灰避开衙印，在纸纤维间聚出半指空白。

顾家残页的补墨灰被压在印痕下方，断处发凉。

右页署时旁的灰却浮在墨锋上，细屑被新落的冷金截断；可在署时下方，又有一小段灰埋进纸纹，反被墨线压住。

陆沉渊盯得多了一息。

银灰火屑忽然在视野中央炸开。他闭不上眼，左眼下的焦纹沿颧骨裂开，烧焦味贴着鼻腔往里钻。一口冷灰顶上喉咙，他偏过头，灰还是落到了台角，擦过薄纸边缘。

冷金小印猛地亮起。

薄纸上的暗红衙印抽出一线，越过台面，勒在陆沉渊掌心旧印上。掌骨再响，胸口那道裂口感骤然收紧。他扶住台沿，眼前只剩乱飘的银灰残屑。

仇慎没有挪开薄纸，反倒用小印压住那片冷灰。

“识账落灰，附入在场认痕。”他说。

冷金压下时，顾家户灯晃了一下，焰心险些褪成透明。

陆沉渊喘过两口气，抬起发抖的手，隔着台面指向两页残纸之间。

“左页写昨日午后暂封，右页写昨夜追加。”

仇慎没说话。

“左页补墨灰在冷金印下面，是印先压灰。右页署时边的灰浮在墨上，又被这道冷金截断；可署时下头还有一截灰，被字压住。”陆沉渊指尖抖得厉害，只能屈起手指，用骨节对准那处，“若右页真是昨夜才写，灰该先落在昨夜送去泥灯巷的薄纸上。可这页有一段灰，比它写着的署时更早。”

仇慎的手停在印柄上。

“它和左页印下的旧灰，同凉，同断口。”陆沉渊道，“右页这处字反压在灰上。它至少有一处次序不对。要么署时晚了，要么这段字先落过，昨夜才补成追加。两种不能一同当作‘昨夜见旁观无人认领后方才立页’。”

仇慎把右页转了半圈。

肉眼本来难分墨与灰的先后。可冷金一压，浮在墨上的灰沿字口碎开，埋在纸纹里的那一小段却牢牢不动。两层灰隔着同一个署时，一处盖着字，一处被字盖住。

莫井兰没有上前，只在原处道：“这灰的凉味，和陶片上的相近。”

仇慎冷声道：“你未触此页。”

“所以我只说相近，不说同源。”

仇慎看她一眼。小印在掌中越握越紧，印缝里渗出一丝暗红，顺着食指爬到指根。他没有落下第四印。

命审台后静了很久。

顾家户灯的青焰缩在灯芯上，偶尔噼啪一响，像有什么东西在里面断掉。

“局部次序有疑，”仇慎终于开口，“不等于顾家折记有误，也不等于护阵追加无效。”

“我只说这一页不能按它写的次序自证。”陆沉渊道。

“你证明不了是谁先落的灰。”

“证明不了。”

“也证明不了为何改时。”

“证明不了。”

仇慎脸上的筋松了一瞬，又立刻绷回去。他将右页从两张残页中抽出，没退回，也没撕毁，压到命审台最里侧。

“顾家附录继续封。守灯前三句照录，未知来源不入。护阵旁观不作无证结案，改列次序待核。”

莫井兰问：“陶片呢？”

“仍由你暂带。损毁，按毁证；拒绝验照，记拒验。今日不强收。”

她袖中的手这才松开一点。

仇慎又望向陆沉渊：“你以识账指出残页次序不合，所咳冷灰已被衙印收认。往后本地残页复核，你不得缺席。州府命库若催问，本衙只能将次序疑处连同你的认痕一并送审。”

“州府命库”几个字落下，台上三枚冷金印同时暗了一暗，像有极重的东西隔着很远压住了它们。

苏晚把手从陆沉渊胸前移到他腕上。她掌背裂口贴近他的皮肤，冷得像埋在灰里的铁。她没扶他去碰纸，只把他不断发抖的手按回身侧。

仇慎另铺一张窄纸，写了两行，等墨迹干了，才将小印压在最下方。

冷金印落纸，缺了一角。

“今日午后，命籍衙到泥灯巷重验护阵旁观落点。”仇慎道，“顾家户灯留衙至验毕，莫井兰携陶片在场，陆沉渊在场。苏晚可拒绝验灯，不得替他认灰。若残页次序仍不能合，另起本地追缴附记；人、物缺一，按拒验续记。”

窄纸推过来，陆沉渊没有伸手。

苏晚先看完，指尖停在“可拒绝验灯”几个字上，又移到“不得替他认灰”。

“他午后若看不清呢？”她问。

“看不清，照样到场。”

“若再咳灰？”

仇慎收起冷金小印。那道暗红印缝已经爬到他的腕骨，袖口也遮不住。

“衙印会记得。”

门外的辰光终于越过屋脊，从紧闭的门缝里推进来，照到顾家户灯前便停住了。

陆沉渊眼里的银灰火屑尚未散尽。他看不清窄纸上的细字，只看见那枚缺角的冷金印，在灰白光里一点点失色。

## Required JSON
```json
{
  "chapter_id": "chapter-0005",
  "artifact_kind": "revision",
  "artifact_sha256": "f627dd586df7aa3238d6722148adf34f5bf1c4efaf29f254344d138e31525aaa",
  "context_sha256": "a7322e4ef7e95dc834d21769f142ef4d1a8d1e61f88d10a9ac3c073561d3eccb",
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
