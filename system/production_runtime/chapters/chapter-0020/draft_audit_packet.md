# NRL Antigravity Chapter Audit v0.20

Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.
Do not use terminal tools, inspect files, run tests, make a plan, or wait for background work. The complete review packet is inline.
Do not rewrite prose. Return one JSON object only using the exact binding hashes, with no Markdown fence or surrounding text.

## Compact Context
{"chapter_id": "chapter-0020", "dramatic_purpose": "护阵寿裂：兑现窗口承诺并留下下一窗口的更高法权压力，服务于“护阵、住户与共同体证据”。", "story_beat": {"chapter_id": "chapter-0020", "working_title": "共拒", "event": "命籍衙执行封存令时，住户不交命火也不抢灯盏，只共同证明保管链与每一次拒绝。", "scene_anchor": "清晨巷口公开封存桌与十张拒验纸", "conflict": "仇慎若强收将越过本地见证权限，不收则必须把缺角半印和异常保管链一并上报。", "character_choice": "仇慎暂停本地封存并承担上报风险，陆沉渊则接受灯盏不能立即使用的结果。", "irreversible_change": "一项本地追缴程序被暂停，州府复核成为下一窗口的明确外部压力。", "emotional_turn": "零散拒绝汇成共同体的程序性站立。", "hook_out": "上报文书出现州府命库的回执印位，但尚未落印。", "expected_state_deltas": ["本地封存程序暂停", "州府复核压力进入可见边缘", "窗口共同体证据完成"], "required_asset_ids": ["faction_life_registry_office", "faction_mudlamp_lane", "npc_registrar_qiu_shen", "bond_mudlamp_lane_trust", "artifact_ashlight_cup"], "source_status": "planned", "window": {"start": 11, "end": 20, "name": "护阵寿裂"}, "window_name": "护阵寿裂", "window_end_target": ["泥灯巷住户以公开拒绝而非献祭命火形成第一份共同体证据。", "残命灯盏只完成可追溯取得，仍保持 dormant，未获得无代价力量。", "仇慎被迫暂停一项本地追缴程序，但将异常上报，州府压力第一次有可见边缘。", "陆沉渊失去在泥灯旁继续识账的安全窗口，下一段必须改变行动方法。"], "contract_path": "system/production_runtime/story_windows/window-011-020.v1.json"}, "must_keep": ["陆沉渊仍只能在已验证的本地权限内识账；任何收益都必须付出身体、关系、身份或程序代价。", "苏晚、街坊与见证者均有拒绝权，不得把共同体信任、住户命火或第三方寿火作为资源。", "监督下仅允许一次有行动代价的有限遮掩；共同体可拒绝。", "每项可写状态变化必须能由正文观察绑定到既有资产、返还对象、承担方与可观察后果。"], "must_avoid": ["不得引入未登记人物、势力、器物、地点、能力或地图结论。", "不得将审查建议、推测或叙事解释写成已经发生的状态变化。", "不得以越级胜利、永久清偿、无代价升级或共同体牺牲解决冲突。", "不得复制语料作品的名称、场景、签名系统、情节或语言风格。"], "scene_constraints": ["本章只推进第 11-20 章窗口“护阵、住户与共同体证据”中的一个可观察步骤。", "至少呈现一项具体动作、感官后果或关系选择；禁止用设定说明替代场景。", "结尾必须留下下一次程序追缴、见证选择或证据复核，不得跳过窗口节奏。"], "assets": [{"asset_id": "artifact_ashlight_cup", "display_name": "残命灯盏", "family": "artifacts", "lifecycle_state": "dormant", "constraints": ["`残命灯盏` is the canonical reader-facing name; `灰烬回灯盏` is a deprecated internal alias and every reference must normalize to `artifact_ashlight_cup`.", "It stores only mistakenly taken residual fire, never fresh life directly stolen from a person.", "Activation visibly cracks the user's skin with ember lines and alerts pursuit through the lamp's smoke.", "Its acquisition from the Mudlamp Lane array base and awakening by voluntarily offered watch-fire must be recorded before first use.", "The asset remains dormant until acquisition, consented watch-fire awakening, and the linked array/resident ledger transaction all validate.", "Chapter 1 is locked to dormant: acquisition, awakening, activation, possession, and use may not be backdated into Chapter 1."], "relationships": [{"target_id": "technique_embertrace_return", "relation_type": "is_required_prerequisite_for"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "reveals_traces_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "updates"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "acquisition_depends_on"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "awakening_requires_consented_watchfire_from"}]}, {"asset_id": "bond_mother_su_wan", "display_name": "苏晚与陆沉渊的垫寿亲缘", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["The mother is an active moral presence, not expendable motivation.", "Any attempt to relieve her debt must carry an exposure, bodily, or communal consequence."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "deadline_is_tracked_by"}]}, {"asset_id": "bond_mudlamp_lane_trust", "display_name": "泥灯巷共灯之信", "family": "emotional_bonds", "lifecycle_state": "active", "constraints": ["共同体信任不是主角可提取的资源；巷民有拒绝、质询和撤回见证的权利。", "信任提升必须来自共同承担、返还寿火或公开承担反噬，而非主角单方面胜利。", "任何高风险行动都须显示巷民的恐惧、选择与实际保护行为。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "binds_to_community"}, {"target_id": "faction_mudlamp_lane", "relation_type": "measures_mutual_aid_of"}, {"target_id": "npc_su_wan", "relation_type": "is_guarded_by_moral_boundary_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "conditions_witnessed_return"}]}, {"asset_id": "character_lu_chenyuan", "display_name": "陆沉渊", "family": "characters", "lifecycle_state": "active", "constraints": ["Does not transfer a life-cost to uninvolved residents.", "Each use leaves bodily evidence or increases pursuit risk.", "His mother debt and the lane protection array remain non-negotiable constraints.", "At 燃命境初成 he may only recognize ordinary life marks and local ash-trace mismatches; personal-page reading, chain tracing, covenant glimpses, return-fire casting, and seal breaking remain blocked pending validated advancement."], "relationships": [{"target_id": "bond_mother_su_wan", "relation_type": "son_bound_by_lifespan_debt"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_acquire_after_registered_transition"}, {"target_id": "faction_mudlamp_lane", "relation_type": "protects_and_is_bound_to"}, {"target_id": "technique_embertrace_return", "relation_type": "may_unlock_after_lamp_and_progression_gates"}, {"target_id": "technique_ledger_recognition", "relation_type": "uses_basic_local_ash_trace_scope_of"}]}, {"asset_id": "faction_life_registry_office", "display_name": "命籍衙", "family": "factions", "lifecycle_state": "active", "constraints": ["其压迫必须通过寿印、命灯、命审台和具体家庭后果显形，不写成现实机构讽刺。", "本地权限只能冻结、登记、送审与申请追缴，不能解释州府或天庭的完整真相。", "命审程序必须成为可被证据、见证和法术反打的冲突场域。"], "relationships": [{"target_id": "npc_registrar_qiu_shen", "relation_type": "employs"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "issues_local_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "assesses_and_pressures"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "contests"}]}, {"asset_id": "faction_mudlamp_lane", "display_name": "泥灯巷", "family": "factions", "lifecycle_state": "active", "constraints": ["The mutual-aid network cannot become expendable fuel for a single hero.", "Every communal protection act worsens the protection array's visible lifespan cracks or attracts collectors."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "contains_registered_acquisition_site_for"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "is_tracked_by"}]}, {"asset_id": "foreshadowing_cinder_seal_rain", "display_name": "灰雨印痕", "family": "foreshadowing", "lifecycle_state": "active", "constraints": ["The clue appears as sensory supernatural residue, not paperwork.", "Investigating it burns the investigator and raises collection exposure before any revelation."], "relationships": [{"target_id": "artifact_ashlight_cup", "relation_type": "is_revealed_by"}, {"target_id": "npc_mo_jinglan", "relation_type": "is_remembered_by"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "payoff_tracks"}]}, {"asset_id": "npc_mo_jinglan", "display_name": "莫井兰", "family": "npcs", "lifecycle_state": "active", "constraints": ["Her knowledge is partial oral memory, never omniscient exposition.", "Helping preserve testimony exposes her remaining life-fire to collection."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "keeps_its_night_lamps"}, {"target_id": "foreshadowing_cinder_seal_rain", "relation_type": "witnesses_surface_sign"}]}, {"asset_id": "npc_registrar_qiu_shen", "display_name": "仇慎", "family": "npcs", "lifecycle_state": "active", "constraints": ["仇慎只能掌握本地残页与寿印权限，不能成为无所不知的阴谋解释者。", "其每一次施印必须留下可辨的冷金印痕或命灯失色，并制造可追责的现场后果。", "他可恐惧上级追责，但不能因恐惧自动洗白。", "其独立义务是保住本地呈印资格并避免州府问责；当公开证据使继续施印超出本地权限时，可拖延、议价或退回追缴令，但不得因此获得无证据洗白。"], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "serves_as_registrar_for"}, {"target_id": "character_lu_chenyuan", "relation_type": "supervises_and_targets"}, {"target_id": "npc_debt_collector_gu_xun", "relation_type": "forwards_writs_to"}, {"target_id": "faction_mudlamp_lane", "relation_type": "pressures_with_seals"}]}, {"asset_id": "npc_su_wan", "display_name": "苏晚", "family": "npcs", "lifecycle_state": "active", "constraints": ["苏晚是能拒绝错误救法的行动者，不是可消耗的动机。", "她绝不接受以邻里命火、孩童寿数或无辜者命页抵消自己的寿债。", "她的命灯裂纹、冷灰气息和掌背失温须以感官后果呈现，不以抽象说明替代。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "mother_of"}, {"target_id": "bond_mother_su_wan", "relation_type": "embodies"}, {"target_id": "faction_mudlamp_lane", "relation_type": "mutual_aid_member_of"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "raises_restraint_threshold_for"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "is_counted_down_by"}]}, {"asset_id": "state_ledger_faction_pressure", "display_name": "既有势力压力", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of faction_pressure; faction, NPC, and scene assets may request but may not apply a mutation.", "Every mutation must identify an existing source asset and settle atomically with exposure, public reputation, or revealed-error consequences.", "No new faction, location, or plot event may be created to justify a pressure change."], "relationships": [{"target_id": "faction_life_registry_office", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "faction_prefecture_life_treasury", "relation_type": "solely_tracks_pressure_from"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_half_life_registry_exposure", "display_name": "半寿残籍暴露", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of half_life_registry_exposure; techniques, artifacts, NPCs, and other ledgers may request a delta but may not write the value directly.", "Exposure never decreases merely because evidence succeeds or life-fire returns; reduction requires a separately evidenced legal, masking, or withdrawal transition.", "Threshold crossings must change pursuit or access state before the atomic transaction can close.", "The Cluster 5 evidence-record exchange requests exactly +10 percentage points within the 0-100 bound and closes only with the protagonist-owned record debit under the same transaction ID; child, resident, and third-party life-fire prices are rejected."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "solely_tracks_registry_exposure_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "npc_cluster5_black_market_transaction_role", "relation_type": "is_increased_by_transaction_with"}]}, {"asset_id": "state_ledger_map_unlock_status", "display_name": "既有地图边界解锁状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of map_unlock_status; references to existing map boundaries may request but may not apply a transition.", "Every transition is atomic and must preserve unresolved boundaries while recording any exposure consequence.", "The ledger cannot introduce a location or unlock a boundary absent from the canonical outline."], "relationships": [{"target_id": "artifact_prefecture_transit_registry_seal", "relation_type": "requires_validated_boundary_evidence_from"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "display_name": "苏晚命灯裂纹倒计时", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mother_life_lamp_cracks and the mother-life-debt countdown.", "A communal return or protagonist recovery cannot automatically heal a crack or cancel the unresolved mother debt.", "Any technique transaction that affects Su Wan must record the crack/countdown delta here before closing."], "relationships": [{"target_id": "npc_su_wan", "relation_type": "solely_tracks_lamp_cracks_for"}, {"target_id": "bond_mother_su_wan", "relation_type": "provides_countdown_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "cannot_be_auto_cancelled_by"}]}, {"asset_id": "state_ledger_mudlamp_array_integrity", "display_name": "泥灯巷护阵完整度", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of mudlamp_array_integrity; returned fire, resident reserve, and caster strain remain independently owned.", "Array integrity cannot rise from returned fire alone; witnessed repair or stabilization must be recorded.", "Below the registered safety line, lamp activation and return-fire casting fail closed rather than granting emergency power."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_array_integrity_for"}, {"target_id": "artifact_ashlight_cup", "relation_type": "gates_acquisition_and_activation_of"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_poorcity_returnfire", "display_name": "泥灯巷归火余量", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["A positive return never cancels the mother debt or the protection array burden automatically.", "Every gain must name whose life-fire returned and whose visible backlash or exposure increased.", "This asset is the sole writer of returned_miscollected_lifefire and may not write caster strain, registry exposure, array integrity, resident reserve, or mother-lamp state."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "measures_survival_pressure_for"}, {"target_id": "technique_embertrace_return", "relation_type": "is_changed_by"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_resident_lifefire_reserve", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_affected"}]}, {"asset_id": "state_ledger_protagonist_strain", "display_name": "陆沉渊命火与心魄承压", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["状态只记录可叙事化的命火、骨裂、瞳纹、冷灰与心魄恍惚，读者文本不得呈现工程字段。", "任何恢复都不能自动解除母亲寿债、半寿身份或既有追缴。", "承压过界时主角应失去施术窗口或需要他人阻止，而非获得无代价爆发。", "空寿状态是施术锁定与认知承压：不得提升战力；继续行动必须先支付已登记的寿火扣减，并失去至少一个施术或判断能力，恢复须停术和外部看护。", "This asset is the sole writer of sanity_level, caster_lifefire_stability, bone_fissure_severity, eye_pattern_burn, and cold_ash_cough_frequency; it may not write exposure or mother-lamp state."], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "tracks_strain_for"}, {"target_id": "technique_ledger_recognition", "relation_type": "is_decreased_by"}, {"target_id": "technique_chain_deflection_seal_breaking", "relation_type": "is_worsened_by"}, {"target_id": "bond_mother_su_wan", "relation_type": "raises_family_risk_for"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_mother_life_lamp_countdown", "relation_type": "atomic_transaction_peer_when_family_backlash_occurs"}, {"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_public_reputation", "display_name": "公开认知状态", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of public_reputation; all other assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source, reason, before/after state, and at least one independently owned consequence ledger.", "No success, witness, or exposure event changes reputation implicitly or closes without its peer ledger result."], "relationships": [{"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_resident_lifefire_reserve", "display_name": "泥灯巷住户命火储备", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of resident_lifefire_reserve; the reserve is never protagonist inventory or an automatic communal resource.", "Every debit requires named consent and preserves the right to refuse or withdraw before transaction closure.", "No black-market price, technique cost, or artifact awakening may debit children, uninvolved residents, or an unspecified crowd."], "relationships": [{"target_id": "faction_mudlamp_lane", "relation_type": "solely_tracks_consented_reserve_for"}, {"target_id": "bond_mudlamp_lane_trust", "relation_type": "requires_refusal_and_consent_rights_from"}, {"target_id": "state_ledger_mudlamp_array_integrity", "relation_type": "atomic_transaction_peer"}, {"target_id": "artifact_ashlight_cup", "relation_type": "may_supply_consented_watchfire_for_awakening"}]}, {"asset_id": "state_ledger_revealed_account_errors", "display_name": "已揭示错账记录", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of revealed_account_errors; evidence, return-fire, and outline assets may request but may not apply a mutation.", "Every mutation requires an explicit atomic transaction with source evidence and at least one independently owned return-fire, exposure, reputation, pressure, or mystery consequence.", "No inferred or unverified account error may be counted, and no proof may create an implicit credit or debit."], "relationships": [{"target_id": "state_ledger_poorcity_returnfire", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_half_life_registry_exposure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_public_reputation", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_faction_pressure", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_unresolved_mysteries", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "state_ledger_unresolved_mysteries", "display_name": "未解账目疑点", "family": "state_ledger", "lifecycle_state": "active", "constraints": ["This asset is the sole writer of unresolved_mysteries; foreshadowing and outline assets may request but may not apply a mutation.", "Every add, reclassification, or closure requires an explicit atomic transaction with a revealed-error or map-boundary consequence.", "No new mystery, answer, backstory, or plot event may be created by this ledger."], "relationships": [{"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "tracks_only_registered_questions_from"}, {"target_id": "state_ledger_revealed_account_errors", "relation_type": "atomic_transaction_peer"}, {"target_id": "state_ledger_map_unlock_status", "relation_type": "atomic_transaction_peer"}]}, {"asset_id": "technique_backlash_guard", "display_name": "Backlash Guard Candidate", "family": "techniques", "lifecycle_state": "seed", "constraints": ["seed candidate only", "not a final in-world technique name", "do not use for combat scene drafting", "must preserve a cost or counter path"], "relationships": []}, {"asset_id": "technique_ledger_recognition", "display_name": "识账术", "family": "techniques", "lifecycle_state": "active", "constraints": ["At character_lu_chenyuan's current 燃命境初成 stage, the active scope is limited to ordinary life marks and local copy-level ash-trace mismatches visible in the present evidence.", "Personal-page reading is locked to a validated 识账境 transition; chain tracing requires a later audited proof, and ancient-covenant glimpses remain blocked until an independently validated advanced transition and artifact evidence exist.", "The technique cannot directly read minds, predict outcomes, or produce a complete answer at any stage.", "施展后瞳孔浮出焦黑纹路、视野残留银灰火屑，并提升被寿印锁定的风险。", "所有判断须由可见痕迹或受害者见证复核，不能以主角独白定案。"], "relationships": [{"target_id": "character_lu_chenyuan", "relation_type": "is_practiced_by"}, {"target_id": "technique_embertrace_return", "relation_type": "verifies_targets_for"}, {"target_id": "state_ledger_protagonist_strain", "relation_type": "increases"}, {"target_id": "foreshadowing_ancient_debt_covenant_fragment", "relation_type": "cannot_reveal_before_validated_advanced_progression"}]}], "rolling_state": {"source_chapter_count": 19, "latest_fields": [{"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_acquisition_status", "value": "残命灯盏已从灯座基部取出并完成可追溯取得", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_awakening_status", "value": "三户拒绝提供守火，残命灯盏继续保持未唤醒状态", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_chapter_step", "value": "雨停后在三户公开监督圈内取出残命灯盏，并转入三户轮守", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_naming_status", "value": "莫井兰以“残命灯盏”称呼它，但仍不认用途、认主或已唤醒", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_seal_status", "value": "点火口被湿泥与轮守纸角封死，封口完整成为交接记录条件", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_status", "value": "正文未出现残命灯盏", "chapter_id": "chapter-0013", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_visible_trace", "value": "浅盏灰黑冰冷，外壁有灰黑斑痕，盏底带泥痕；内壁仅映出顾家一线余火", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.lifecycle_state", "value": "dormant", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.next_review_hook", "value": "灰黑陶沿留在灯座裂口下方，等待明日申前只许看、不许认的复核；残命灯盏仍未取得、未唤醒", "chapter_id": "chapter-0016", "evidence": null}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.reader_facing_name", "value": "正文首次出现“残命灯盏”这一登记资产名，但未发生认主或唤醒", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_debt_status", "value": "本次返还形成短暂缓冲，但苏晚原有寿债与命灯裂纹均未解除或合拢", "chapter_id": "chapter-0010", "evidence": null}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_procedural_boundary", "value": "与陆沉渊共同承担一息遮印的行动代价，同时未替他答复持有选择", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visibility_of_lu_chenyuan_backlash", "value": "苏晚亲见纸展开后掌心血口再开、胸骨再次钝响、冷灰落在衣摆，并在其退出后扶住他", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visible_support", "value": "苏晚只压稳桌面阻止陆沉渊继续取泥，未扶他本人，也未让自己的命火承担点火代价", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_collective_emotion", "value": "住户将对守火的拒绝公开化，陆沉渊因守住拒绝权而失去继续追查的兴奋", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_custody_rule", "value": "建立三户轮流保管、交接只记亲见、任一户可退出并公开退回的共同保管规则", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_refusal_boundary", "value": "共同体公开形成“接物、不接火”的拒绝边界，并要求未来开启重新征询三户", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "value": "见证被拆分为各户亲见范围；第三户撤回未看清的第二步，三户分别保留后续撤回或退出权", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_action_limit", "value": "接受本轮无法继续借守火显现更多灰痕", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_local_evidence_statement", "value": "确认在场认痕与残页下灰之间存在一线断口，不能据此认定其碰过残页、认定接触者、断裂时间或灰的来源", "chapter_id": "chapter-0010", "evidence": null}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_observed_choice", "value": "亲手封住灯盏点火口，并规定重新开启必须召集三户重新询问同意", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_intent", "value": "确认明日辰时到场，但不替任何住户陈述未亲见之事", "chapter_id": "chapter-0004", "evidence": null}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_procedural_status", "value": "明日申前先验在场次序；须带未愈血口，只看不识账、不碰阵；见证可来、可拒、可撤", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_visible_condition", "value": "遮印后胸骨剧烈抽痛，右眼压成漆黑，咳出冷灰并短时无法站立", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.current_enforcement_record", "value": "追缴纸旁注记录原位灰痕在下、次序待核，未撤销追缴", "chapter_id": "chapter-0008", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "value": "旧追缴暂停至复核结束但不撤销，仇慎将异常上报州府", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.current_scene_sequence", "value": "黄昏轮值桌公开询问守火；三户拒绝后顾婶限定核火；陆沉渊封口；仇慎发布最后一次本地封存令", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.local_enforcement_status", "value": "顾家折记暂缓至午后复核", "chapter_id": "chapter-0001", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.next_local_notice", "value": "明日申前先验第一户是否仍愿保管、再验盏底泥痕；任一户退出即在圈内交还，离开三户轮守则旧追缴续行", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.next_local_review_schedule", "value": "明日申前复核三枚拒验指印与未封句子；护阵裂口另验，陆沉渊仍须带未愈血口只看、不识账、不碰阵", "chapter_id": "chapter-0016", "evidence": null}, {"asset_id": "faction_life_registry_office", "field_path": "faction.procedural_observation_of_lu_chenyuan", "value": "陆沉渊被要求往后残籍复核在场；传核缺席按拒验记", "chapter_id": "chapter-0002", "evidence": null}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_chapter_step", "value": "雨夜复核陶沿雨痕与刻痕连接；确认两股灰的相反流向、陶沿外角新裂及一次无住户牵动的微弱回火", "chapter_id": "chapter-0017", "evidence": null}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "value": "三户逐一公开拒绝守火，但仍接受器物轮守；共同体把器物保管与命火提供明确分开", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "value": "取盏后灯座失去一处旧撑，裂口向下塌了半指，暗红火星断开一处，仅剩两截微弱红痕", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_scene_sequence", "value": "戌后密雨冲开灰壳并分流；随后积水加剧裂口；子夜后雨缓，陶沿内侧发生一次微弱回火；结尾等待明日复核", "chapter_id": "chapter-0017", "evidence": null}, {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "value": "暮光中余火线彻底隐没但未熄灭，且未向任何住户墙根延伸", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.next_review_hook", "value": "下一次程序复核扩展为顾家余火口述、三户拒绝是否维持及封口完整性", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_artifact", "value": "负责第一回交接，将残命灯盏交给第一户轮守", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_witness_material", "value": "暂带顾家补墨灰屑陶片作为守灯见证物", "chapter_id": "chapter-0003", "evidence": null}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_returnfire_witness", "value": "只确认陶沿内侧亮过一次，未确认取走任何住户命火或回火来处", "chapter_id": "chapter-0017", "evidence": null}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_visible_injury", "value": "取盏时手背被旧砖粗边磨开一道口子，流血但未让血落入泥中", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "value": "逐项记录三户拒绝守火，并确认封口完整作为后续交接依据", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_local_notice", "value": "明日申前先验在场次序；纸先到、半印后到；陆沉渊只看，苏晚可拒验，莫井兰可来、可不来或撤回未封句子", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_seal_condition", "value": "半枚印仍未露面；袖中半印撞腕骨并使其僵硬左手进一步承压", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.current_visible_fear", "value": "仇慎持续出汗、左手僵硬，仍以逐句记录、分开封记和保留空位控制程序风险", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.latest_local_notice", "value": "以冷金小印薄纸通知明日辰时顾家户灯、守灯口述及泥灯巷护阵旁观均不得缺席", "chapter_id": "chapter-0004", "evidence": null}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "value": "暂停带回封存，改记原位取出、三户轮守、随时退还，并登记未点火、未认主、住户命灯不列调用", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.next_local_notice", "value": "发布本地最后一次封存令：残命灯盏不得点火、移出泥灯巷或毁去封口，明日申前复核顾家余火口述及三户拒绝是否维持", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "npc_su_wan", "field_path": "npc.current_emotional_choice", "value": "以自身手臂和命灯承受持帘负担，同时拒绝用陆沉渊的身体代替自己的承担", "chapter_id": "chapter-0017", "evidence": null}, {"asset_id": "npc_su_wan", "field_path": "npc.current_local_lamp_assessment", "value": "验灯显示命灯失温、焰尖缩成细线，手背红点裂开并渗出暗冷光", "chapter_id": "chapter-0003", "evidence": null}, {"asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "value": "与陆沉渊共同遮住仇慎袖口冷金印光一息，未越泥圈且未代他承担全部重量", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "npc_su_wan", "field_path": "npc.current_refusal_statement", "value": "拒绝以自己抵命，也拒绝以泥灯巷住户命火填补自身裂纹", "chapter_id": "chapter-0004", "evidence": null}, {"asset_id": "npc_su_wan", "field_path": "npc.current_visible_lamp_consequence", "value": "冷金印出现时暗冷光向腕骨下缩，五指攥紧桌沿；未显示命灯恢复", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "state_ledger_half_life_registry_exposure", "field_path": "state_ledger.registry_locking_sign", "value": "纸展开时掌心暗红线被勒紧并沿腕内拖行；半印未出袖，远离后暗线仅略松，旧追缴与血口证据继续保留", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "state_ledger_mother_life_lamp_countdown", "field_path": "state_ledger.current_visible_lamp_consequence", "value": "掌背暗冷光仍在皮下明灭并贴近腕骨；正文未显示裂纹合拢、命债解除或命灯缓解", "chapter_id": "chapter-0016", "evidence": null}, {"asset_id": "state_ledger_mudlamp_array_integrity", "field_path": "state_ledger.current_visible_integrity_consequence", "value": "裂口处两截暗红火痕继续时明时灭，未因本章行动获得修复", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "state_ledger_poorcity_returnfire", "field_path": "state_ledger.current_return_transaction", "value": "仍未发生命火转移；顾家余火只被确认尚存，未被调用或归还", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.bone_fissure_severity", "value": "纸完全展开后胸骨再次钝响，随后起身时裂处磨响；陆沉渊无法自行站稳并被苏晚按回", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.cold_ash_cough_frequency", "value": "雨中再次咳出一口冷灰，全部落在衣襟，未越过墙根、纸张或灯座", "chapter_id": "chapter-0017", "evidence": null}, {"asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.current_visible_condition", "value": "封口时胸骨猛然收缩，旧血口再次张开并沿掌纹流至腕内；身体代价继续存在", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.eye_pattern_burn", "value": "右眼持续重影并在纸展开后进一步发黑；左眼焦壳下继续掉落碎屑，视力未恢复", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "state_ledger_resident_lifefire_reserve", "field_path": "state_ledger.current_record_label", "value": "“住户命灯不列调用”；三户拒出仅限今日，且不记为住户欠火", "chapter_id": "chapter-0016", "evidence": null}, {"asset_id": "state_ledger_resident_lifefire_reserve", "field_path": "state_ledger.current_resident_lifefire_callability", "value": "仍未调用住户命灯，未发生命火扣减；三户同意仅限物证取出与轮守", "chapter_id": "chapter-0018", "evidence": null}, {"asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "value": "顾婶仅同意核对顾家余火仍在；记录明确未点、未认归属、未作调用", "chapter_id": "chapter-0019", "evidence": null}, {"asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_inference_limit", "value": "仅能确定纸靠近和展开伴随火低、上点移动及血口再开；不能确定因果、来源、同源、归属或接触事实", "chapter_id": "chapter-0015", "evidence": null}, {"asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_procedure_result", "value": "雨痕、门帘边界、陶沿结构和一次回火被分列记录；旧追缴仍不撤，未形成灰之来处、用途或归属结论", "chapter_id": "chapter-0017", "evidence": null}, {"asset_id": "technique_ledger_recognition", "field_path": "technique.current_local_ash_trace_observation", "value": "确认陆沉渊在场认痕对应的纸上暗线分成两段，其中一段绕过印角牵向残页下方，中间存在干净纸色断口；结论止于不能认定碰过残页", "chapter_id": "chapter-0010", "evidence": null}, {"asset_id": "technique_ledger_recognition", "field_path": "technique.current_use_status", "value": "仍未施展识账；仅以模糊肉眼观察灰流、刻痕和回火，不形成来源、用途或归属判断", "chapter_id": "chapter-0017", "evidence": null}], "recent_chapters": [{"chapter_id": "chapter-0018", "accepted_revision_sha256": "a6d3b891d64d57120a90e5b3baa61dfd3330c19572ee0b6c9d7f313662a7a1e1", "changes": [{"asset_id": "character_lu_chenyuan", "field_path": "character.current_observed_choice", "after": "放弃个人持有残命灯盏，接受三户轮流保管与随时退出规则"}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "after": "在住户监督下完成取盏，并将见证范围限定为各自亲见内容"}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_custody_of_artifact", "after": "负责第一回交接，将残命灯盏交给第一户轮守"}, {"asset_id": "npc_su_wan", "field_path": "npc.current_procedural_limit", "after": "与陆沉渊共同遮住仇慎袖口冷金印光一息，未越泥圈且未代他承担全部重量"}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.local_review_decision", "after": "暂停带回封存，改记原位取出、三户轮守、随时退还，并登记未点火、未认主、住户命灯不列调用"}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_protection_array_condition", "after": "取盏后灯座失去一处旧撑，裂口向下塌了半指，暗红火星断开一处，仅剩两截微弱红痕"}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "after": "三户在公开监督下允许取盏，但分别保留拒绝、撤回见证和退出保管的权利，未提供命火"}, {"asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "after": "一项带回封存程序被暂停，改为明日申前先验第一户保管意愿与盏底泥痕；异物、阵裂和拒绝单独封存被上报"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_acquisition_status", "after": "残命灯盏已从灯座基部取出并完成可追溯取得"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.lifecycle_state", "after": "dormant"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_naming_status", "after": "莫井兰以“残命灯盏”称呼它，但仍不认用途、认主或已唤醒"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_visible_trace", "after": "浅盏灰黑冰冷，外壁有灰黑斑痕，盏底带泥痕；内壁仅映出顾家一线余火"}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_custody_rule", "after": "建立三户轮流保管、交接只记亲见、任一户可退出并公开退回的共同保管规则"}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_collective_emotion", "after": "在共同监督下形成有限的物证协作，但仍拒绝把共同体变成命火或无条件见证资源"}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_procedural_boundary", "after": "与陆沉渊共同承担一息遮印的行动代价，同时未替他答复持有选择"}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_witness_commitment", "after": "见证被拆分为各户亲见范围；第三户撤回未看清的第二步，三户分别保留后续撤回或退出权"}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visible_support", "after": "苏晚在陆沉渊几乎跪下时仍抓住帘角并未把责任转给旁人，随后抱回湿帘"}, {"asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "after": "新增可追溯取得记录：残命灯盏从灯座基部取出，盏底泥痕与裂线由在场者分面复述；用途、来处和认主仍未确认"}, {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "after": "盏内只映出顾家错压旁注对应的一线余火，其他位置无第二点光；该线暂不认定为归属结论"}, {"asset_id": "state_ledger_poorcity_returnfire", "field_path": "state_ledger.current_return_transaction", "after": "本章未发生新的归火或住户命火转移，既有返还状态保持"}, {"asset_id": "state_ledger_resident_lifefire_reserve", "field_path": "state_ledger.current_resident_lifefire_callability", "after": "仍未调用住户命灯，未发生命火扣减；三户同意仅限物证取出与轮守"}, {"asset_id": "faction_life_registry_office", "field_path": "faction.next_local_notice", "after": "明日申前先验第一户是否仍愿保管、再验盏底泥痕；任一户退出即在圈内交还，离开三户轮守则旧追缴续行"}, {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.next_review_hook", "after": "下一次复核集中于残命灯盏为何只映出顾家一笔错压，且该映照尚未被认定为归属"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_chapter_step", "after": "雨停后在三户公开监督圈内取出残命灯盏，并转入三户轮守"}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_visible_condition", "after": "遮印后胸骨剧烈抽痛，右眼压成漆黑，咳出冷灰并短时无法站立"}, {"asset_id": "npc_su_wan", "field_path": "npc.current_visible_lamp_consequence", "after": "共同遮印后暗冷光仍贴近腕骨，五指抖到抓不住布，命灯未显示恢复"}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_visible_injury", "after": "取盏时手背被旧砖粗边磨开一道口子，流血但未让血落入泥中"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.reader_facing_name", "after": "正文首次出现“残命灯盏”这一登记资产名，但未发生认主或唤醒"}]}, {"chapter_id": "chapter-0019", "accepted_revision_sha256": "cae97de0053c2b76c51b03d9479818f22a7459fc2be831ccdaae94bd65600555", "changes": [{"asset_id": "character_lu_chenyuan", "field_path": "character.current_observed_choice", "after": "亲手封住灯盏点火口，并规定重新开启必须召集三户重新询问同意"}, {"asset_id": "character_lu_chenyuan", "field_path": "character.current_action_limit", "after": "接受本轮无法继续借守火显现更多灰痕"}, {"asset_id": "npc_mo_jinglan", "field_path": "npc.current_witness_participation", "after": "逐项记录三户拒绝守火，并确认封口完整作为后续交接依据"}, {"asset_id": "npc_registrar_qiu_shen", "field_path": "npc.next_local_notice", "after": "发布本地最后一次封存令：残命灯盏不得点火、移出泥灯巷或毁去封口，明日申前复核顾家余火口述及三户拒绝是否维持"}, {"asset_id": "npc_su_wan", "field_path": "npc.current_visible_lamp_consequence", "after": "冷金印出现时暗冷光向腕骨下缩，五指攥紧桌沿；未显示命灯恢复"}, {"asset_id": "faction_mudlamp_lane", "field_path": "faction.current_communal_response", "after": "三户逐一公开拒绝守火，但仍接受器物轮守；共同体把器物保管与命火提供明确分开"}, {"asset_id": "faction_life_registry_office", "field_path": "faction.current_local_enforcement_phase", "after": "旧追缴暂停至复核结束但不撤销，仇慎将异常上报州府"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_awakening_status", "after": "三户拒绝提供守火，残命灯盏继续保持未唤醒状态"}, {"asset_id": "artifact_ashlight_cup", "field_path": "artifact.current_seal_status", "after": "点火口被湿泥与轮守纸角封死，封口完整成为交接记录条件"}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_refusal_boundary", "after": "共同体公开形成“接物、不接火”的拒绝边界，并要求未来开启重新征询三户"}, {"asset_id": "bond_mother_su_wan", "field_path": "emotional_bond.current_visible_support", "after": "苏晚只压稳桌面阻止陆沉渊继续取泥，未扶他本人，也未让自己的命火承担点火代价"}, {"asset_id": "bond_mudlamp_lane_trust", "field_path": "emotional_bond.current_collective_emotion", "after": "住户将对守火的拒绝公开化，陆沉渊因守住拒绝权而失去继续追查的兴奋"}, {"asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.current_local_evidence_status", "after": "顾婶仅同意核对顾家余火仍在；记录明确未点、未认归属、未作调用"}, {"asset_id": "state_ledger_poorcity_returnfire", "field_path": "state_ledger.current_return_transaction", "after": "仍未发生命火转移；顾家余火只被确认尚存，未被调用或归还"}, {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.current_manifestation", "after": "暮光中余火线彻底隐没但未熄灭，且未向任何住户墙根延伸"}, {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.next_review_hook", "after": "下一次程序复核扩展为顾家余火口述、三户拒绝是否维持及封口完整性"}, {"asset_id": "faction_life_registry_office", "field_path": "faction.current_scene_sequence", "after": "黄昏轮值桌公开询问守火；三户拒绝后顾婶限定核火；陆沉渊封口；仇慎发布最后一次本地封存令"}, {"asset_id": "state_ledger_protagonist_strain", "field_path": "state_ledger.current_visible_condition", "after": "封口时胸骨猛然收缩，旧血口再次张开并沿掌纹流至腕内；身体代价继续存在"}, {"asset_id": "state_ledger_mudlamp_array_integrity", "field_path": "state_ledger.current_visible_integrity_consequence", "after": "裂口处两截暗红火痕继续时明时灭，未因本章行动获得修复"}]}]}}

## Rule Stack
{"version": "0.22", "chapter_id": "chapter-0020", "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "priority_order": ["safety_and_originality", "canonical_story_bible", "volume_outline", "accepted_state_settlements", "creation_asset_constraints", "chapter_must_keep_and_must_avoid", "anti_ai_style_evidence"], "hard_rules": ["no source-work names, scenes, signature systems, or prose imitation", "no untracked power, relationship, location, item, or timeline changes", "all benefits carry an embodied, relational, or systemic cost", "reader-facing prose contains no runtime or database vocabulary", "不得引入未登记人物、势力、器物、地点、能力或地图结论。", "不得将审查建议、推测或叙事解释写成已经发生的状态变化。", "不得以越级胜利、永久清偿、无代价升级或共同体牺牲解决冲突。", "不得复制语料作品的名称、场景、签名系统、情节或语言风格。"], "chapter_rules": ["陆沉渊仍只能在已验证的本地权限内识账；任何收益都必须付出身体、关系、身份或程序代价。", "苏晚、街坊与见证者均有拒绝权，不得把共同体信任、住户命火或第三方寿火作为资源。", "监督下仅允许一次有行动代价的有限遮掩；共同体可拒绝。", "每项可写状态变化必须能由正文观察绑定到既有资产、返还对象、承担方与可观察后果。"], "scene_constraints": ["本章只推进第 11-20 章窗口“护阵、住户与共同体证据”中的一个可观察步骤。", "至少呈现一项具体动作、感官后果或关系选择；禁止用设定说明替代场景。", "结尾必须留下下一次程序追缴、见证选择或证据复核，不得跳过窗口节奏。"]}

## Compilation Trace
{"version": "0.22", "chapter_id": "chapter-0020", "selected_asset_ids": ["artifact_ashlight_cup", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "character_lu_chenyuan", "faction_life_registry_office", "faction_mudlamp_lane", "foreshadowing_cinder_seal_rain", "npc_mo_jinglan", "npc_registrar_qiu_shen", "npc_su_wan", "state_ledger_faction_pressure", "state_ledger_half_life_registry_exposure", "state_ledger_map_unlock_status", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_poorcity_returnfire", "state_ledger_protagonist_strain", "state_ledger_public_reputation", "state_ledger_resident_lifefire_reserve", "state_ledger_revealed_account_errors", "state_ledger_unresolved_mysteries", "technique_backlash_guard", "technique_ledger_recognition"], "explicit_asset_ids": ["artifact_ashlight_cup", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "character_lu_chenyuan", "faction_life_registry_office", "faction_mudlamp_lane", "foreshadowing_cinder_seal_rain", "npc_mo_jinglan", "npc_registrar_qiu_shen", "npc_su_wan", "state_ledger_faction_pressure", "state_ledger_half_life_registry_exposure", "state_ledger_map_unlock_status", "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity", "state_ledger_poorcity_returnfire", "state_ledger_protagonist_strain", "state_ledger_public_reputation", "state_ledger_resident_lifefire_reserve", "state_ledger_revealed_account_errors", "state_ledger_unresolved_mysteries", "technique_backlash_guard", "technique_ledger_recognition"], "dependency_asset_ids": [], "excluded_asset_count": 20, "selection_reason": "explicit chapter intent requirements plus atomic transaction peers", "canonical_hashes": {"borrowed_heaven_life_account_bible": "81575478a441852f18d451e9967245bbfce11d60cddd3af24e9b6565955e0604", "borrowed_heaven_volume1_outline_tree": "1f12fe8ad3262876eb533d40c94ad02abb90b95b38de387d339917fce9184648", "project_assets.v0.2": "90dbcf17d769e8a985fc87880a4382018c30133a2a53f82c3826636c8ed1dc61"}, "canonical_baseline": {"path": "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json", "version": "0.22", "sha256": "402c923d3dbc19bcccc353856a605388170ab3d1410550b8fb2620e48fa8ea27"}, "prior_settlement_count": 19, "rolling_state_field_count": 68, "story_window_contract": "system/production_runtime/story_windows/window-011-020.v1.json"}

## Observed Facts
Initial audit: no final-text observations exist yet.

## Prose
清晨的雾还压在泥灯巷口，封存桌已经摆开。

桌脚垫着昨夜湿透的砖，木面一高一低。十张薄纸压在桌上，纸角被雾气泡软，墨线却分得清楚：三张记三户轮守，三张记昨日拒出守火，三张留给今日复验，最后一张空着，只在上端写了“封存”。

残命灯盏没有摆到桌心。

它被放在三户围出的泥圈里，点火口上的湿泥已经发白，嵌在泥里的轮守纸角没有翘起。灰黑盏壁冷得不沾晨光，盏底那圈旧泥痕朝外，谁走近都能看见。灯座裂口就在后方，两截暗红火痕隔着塌下的半指空隙，时亮时暗。

莫井兰先蹲下去，手背那道未合的擦口绷得发红。她没有碰灯盏，只把昨夜交接时折下的纸角举到封口旁。

“纹路对得上。”她说，“我只认纸角没换，湿泥没断。盏里有没有东西，我没看。”

仇慎站在封存桌后，左手藏在袖中，右手把第一张纸推到桌边。

“第一户，验保管。”

第一户的人没有进泥圈，只隔着一臂远看了看封口。

“昨夜接来时，口上有泥，纸角在泥里。今早送回也是这样。旁的我不验。”

仇慎蘸墨：“可愿继续保管？”

“今日不愿。”

巷里响起一阵衣料摩擦声。没人往前挤，也没人劝。

仇慎笔尖停在纸上：“退出轮守，灯盏须交回封存桌。”

“交回泥圈。”那人盯着他，“昨日写的是圈内交还。封存桌在圈外。”

仇慎抬眼。桌与泥圈之间只隔三步，桌沿冷金小印的光却正好压过第一道泥线。

他把纸拖回来，划去“封存桌”，补成“原圈”。

第一户这才按下指印。指腹离纸时，墨印缺了一小块，仇慎没有让人重按，在旁边记了“指腹旧裂，亲见缺口”。

第二户也退出。

第三户仍愿保管器物，却拒绝验盏底泥痕。

“昨夜轮到我时，盏底朝里。我没搬动，看不全。你今日把它转过来，我也不能替昨夜补看。”

仇慎将第三张纸摊平：“只验今日所见。”

“今日所见，是它在圈里，封口没破。盏底我不认。”

第三枚指印落下。十张纸里，已有三张留下各不相同的拒绝：不续守，不续守，不验盏底。

陆沉渊站在苏晚身侧，右掌缠着旧布。血从昨夜裂开的掌纹里慢慢洇出来，尚未透过最外一层。他的右眼仍压着重影，仇慎每挪一张纸，纸边便在他视野里拖出一层银灰虚线。

他没有动用识账术。

桌上能看的，只是纸角、墨迹、指印和仇慎袖口偶尔露出的冷金微光。多看一刻，胸骨里那道裂处便跟着呼吸磨一下。他把视线移到泥圈上，重影才淡了些。

仇慎抽出第四张纸。

“昨日拒出守火，今日复验。第一户，是否维持？”

“维持。”

“理由。”

“昨日没写理由。”

“今日封存，须记明拒绝是否受人逼迫。”

第一户的人把手收进袖中：“我只答没人替我应，也没人替我拒。我的命火不交。你要多写，写你问过，我没答。”

仇慎颊边绷了一下。他照写。

第二户说：“维持。灯盏可以守，命火不出。”

第三户说得更慢：“维持。以后若再问，须重新问我，不能拿今日这张纸作长久应允。”

莫井兰把三句话逐一念回。念到“不能作长久应允”时，仇慎让她停下，自己在句尾添了两个小字：限今。

冷金的光从他袖中透出来，桌上三张纸的墨色同时浅了一层。苏晚掌背皮下那点暗冷光也随之一缩，贴向腕骨。她五指扣住桌角，指节泛白，却没有退。

陆沉渊侧过身，挡住了她与封存桌之间最直的一线。

苏晚抬臂，把他推开半步。

“我站哪里，我自己选。”

她的掌背已经失温，碰到他手腕时像一块浸过冷水的石头。陆沉渊没有再挡，只将自己脚尖撤出她前方，让她能看见桌上的每一笔。

仇慎看见了，却没说话。他把第七张纸铺开。

“苏晚，验封存条件。”

“我可以拒验。”

“可以。”

“那我只验一件。”苏晚望向泥圈里的灯盏，“住户命灯没有列入调用。”

仇慎指向昨日旁注。纸上那一句被单独圈出，冷金印痕贴着圈线，颜色比别处更淡。

苏晚没有碰纸：“念。”

莫井兰念道：“未点火，未认主，住户命灯不列调用。”

“再念今日三户的话。”

莫井兰又念了一遍。每念一句，巷口便有人在纸上按下一枚指印。有人按在句后，有人按在页角，也有人拒绝按印，只让莫井兰记下“在场听见，不验全纸”。

第七张纸很快挤满了零碎的墨痕。

仇慎把第八张推给陆沉渊：“验残命灯盏。”

“验哪一项？”

“封口，盏底，是否藏火。”

“我能看封口。盏底昨夜没有全程在我眼前，不能补验。藏火须开口或借守火照见，两样都没有同意。”

“你昨日见过顾家一线余火。”

“见过映在内壁的一线光。没认归属，没认来处，也没认灯盏已醒。”

仇慎的右手按住纸，袖中传出一声轻磕，像半枚硬物撞上腕骨。

“若今日封存，命籍衙须验明所封何物。”

陆沉渊看着他：“你能封未明物，还是能命三户出火替你验明？”

巷口静了。

护阵裂口里，一截暗红火痕忽然缩短，砖缝中落下一撮干灰。没有人去扶灯座。谁都看得出，若再挪动泥圈里的灯盏，那处失去旧撑的裂口还会往下塌。

仇慎把第八张纸转了半圈，朝向三户。

“命籍衙现行封存令：封物须核名、核痕、核持有。你们拒验盏底，拒出守火，第一、第二户又退出轮守。封存条件不全。灯盏若留原圈，保管链中断；若带回，须越圈取物。”

第三户开口：“我的保管没有中断。我只不替别人补看。”

第一户跟着说：“我退出后的那一步，我不认。”

第二户将自己那张纸拿起，指着交还处：“我把灯盏交回原圈，莫井兰在场。你若说中断，写清从哪一步断。”

仇慎没有接纸。

十张拒验纸原先各压在桌的一处，此时被一只只手推到中间。谁也没有夺灯盏，谁也没有碰仇慎的封存印。纸页高低错落，指印有深有浅，连句子都不齐整，却把灯盏从昨夜第一户接手、交到第二户、再交第三户、清晨回到原圈的次序围了出来。

空缺也露在里面。

第一户不认退出后的事；第二户只认自己交还；第三户不认盏底；莫井兰只认封口与交接；苏晚只验住户命灯未被调用；陆沉渊只认现下可见的泥封，不认藏火。

仇慎若要把“全程无缺”写上去，十张纸里没有一张肯承接这四个字。若写“无人保管”，第三户的指印正压在“仍愿守物”下面。

他从袖中取出半枚印。

冷金印面只有半边，缺角处参差发暗。印一离袖，桌上几盏命灯的焰色同时褪白。苏晚腕骨下的暗冷光猛地一跳，她吸了口气，肩头没有弯。陆沉渊掌中旧血口骤然收紧，布条下渗出一线热意，胸骨也随之钝响。

仇慎将半印悬在第十张纸上。

纸上只有“封存”二字。

陆沉渊右眼里的重影层层叠起。他看不清印文，只看见缺角投下的影子没有覆住纸上预留的见证线。那是眼前便能辨出的形状，不需识账。

“缺角压不到见证位。”他说。

仇慎手腕一僵。

陆沉渊用未伤的指节轻点桌边，没有越过纸角：“你若落印，只能证明半枚印到过。证明不了十张拒验已经被一并收进封存。”

“住口。”

“我只说看见的缺口。”

仇慎盯了他片刻，半印仍悬着。冷金光把陆沉渊右眼照得发黑，银灰火屑在视野边缘不断往下掉。他闭上右眼，不再追看印痕。

莫井兰忽然把第十张纸往回抽了半寸。

仇慎喝道：“谁许你动？”

“这张还没人验。”她松开手，“你可以把它放回去。我拒绝替空纸作见证。”

纸停在半印够不着、仇慎又能自行取回的位置。

第三户把自己的纸压在第十张下方：“若要收走，一张张念。念错一句，我撤回今日的指印。”

第一户也伸手压住页角：“我的退出只到交回原圈。”

第二户没有碰纸，只站到了灯盏与封存桌之间，给泥圈留出一条能看见、不能顺手跨过的窄道。

巷中其余人仍站在原处。有的手藏在袖中，有的握着自家命灯，灯焰被半印照得苍白。没人献火，也没人上前抢印。

仇慎额角的汗落在第八张纸边，晕开一个小黑点。

他终于收回半印。

命灯的颜色缓慢回暖，苏晚掌背的暗冷光却没有退回去，仍贴着腕骨明灭。护阵裂口里的两截红痕也没有接上。

仇慎把第十张纸翻过来，在背面写字。写到第三行，左手在袖中抖了一下，他用右腕压住纸，继续往下。

莫井兰站在侧面逐字看。

“本地封存暂停。”仇慎写完，自己念出声，“残命灯盏留原圈，由现愿保管户继续守物。不得点火，不得移出泥灯巷，不得毁封。十张纸分记亲见与拒绝，不并作全验。”

第一户问：“暂停到何时？”

仇慎笔尖顿住，补上一句：“候州府复核。”

“旧追缴呢？”

“未撤。”

这两个字落下，巷里没有人应声。

陆沉渊把掌心压在胸前。那里每一次呼吸都像有碎骨互相擦过。他看了一眼残命灯盏。封口还在，灰黑盏壁仍冷，今日之后也不能拿来照那一线余火，更不能用来继续识账。

他把目光移开。

“我接受不启灯。”他说，“这一句记在我的纸上，不记到三户名下。”

仇慎另起一行。陆沉渊按指印时，旧布终于被血浸透。暗红沿着指腹落在印边，没有盖住字。仇慎看了一眼，在旁注明“血来自原伤”，没有替他抹去。

苏晚把他的手从纸上托开。她掌心冰冷，力气却稳，只托到他站直便松手。

十张纸依次穿线。每穿过一张，莫井兰便念一次页首和拒绝处。有人当场撤回一句“封口自昨夜未变”，改成“清晨看时未破”；有人拒绝核对仇慎写下的“保管完整”，逼他改成“交接各自可述”；还有一枚指印只压在“命火不出”四字下面，其余空处全被一道斜墨划去。

仇慎没有再取印。

他将穿好的纸束放在桌心，又抽出一张上报纸。半印缺角朝上搁在右侧，没有落下。纸首写命籍衙本地封存权限不足，中段列残命灯盏封口、轮守次序、拒验范围与护阵裂口，末尾留着一处方正空白。

空白上方，印着极淡的五个字：

州府命库回执。

雾气从巷口退开一点，那处印位白得刺眼。

仇慎将纸折到回执位之前，停住，重新展开。他把十张拒验纸连同上报纸一起装入封套，封套口仍空着，只压上那枚缺角半印比了比。

半印抬起时，回执位上什么也没留下。

## Required JSON
```json
{
  "chapter_id": "chapter-0020",
  "artifact_kind": "draft",
  "artifact_sha256": "12abf720130f664ff48f2ae7dee23e7597cbd37c40162df0465544450d87dc60",
  "context_sha256": "8061a5be409bf40a86d42802f9b7495e3fc50290ebb731eb0fa84432583df1a0",
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
