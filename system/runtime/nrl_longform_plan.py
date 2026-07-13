from __future__ import annotations

"""Candidate-only contracts for the 6M-character version of Borrowed Heaven."""

import json
from pathlib import Path
from typing import Any

from nrl_paths import runtime_path
from nrl_owner_gate import load_decisions


VERSION = "0.1"
CONTRACT_PATH = runtime_path("system/production_runtime/plans/borrowed_heaven_longform_contract.v0.1.json")
FIRST100_PATH = runtime_path("system/production_runtime/plans/borrowed_heaven_first100_manifest.v0.1.json")
FINAL_REVIEW_PATH = runtime_path(".agent-handoff/antigravity/responses/nrl-v024-600w-longform-final-review.md")
ACTIVE_BLUEPRINT_PATH = runtime_path("system/production_runtime/active_story_blueprint.v0.24.json")
GUARD_CONFIG_PATH = runtime_path("system/production_runtime/state/longform_first100_guard_config.v0.1.json")

STATE_LEDGER_IDS = (
    "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure",
    "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity",
    "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire",
    "state_ledger_revealed_account_errors", "state_ledger_faction_pressure",
    "state_ledger_public_reputation", "state_ledger_unresolved_mysteries",
    "state_ledger_map_unlock_status",
)

VOLUMES = (
    (1, "贫城错账", "母亲寿债与贫城重复征收", "首笔局部改账，贫城拒绝交人"),
    (2, "州府命库", "转运账路如何把地方错误合法化", "取得可复核的转运证据"),
    (3, "迁籍长夜", "被注销者与迁徙人群如何活下来", "建立跨城见证网络"),
    (4, "寿库封国", "州府用封档制造无证即有罪", "打开州级档库公开缺口"),
    (5, "废命地", "被抹除的人能否成为证人", "找到古债的第一位活证人"),
    (6, "命审九城", "九城互保能否承受联合追缴", "形成有限共同裁决规则"),
    (7, "仙朝命卷", "上层豁免如何转嫁到底层", "证实命税结构性例外"),
    (8, "诸侯借寿", "战争、宗门与商路如何争夺寿命财政", "撕开跨域借寿链"),
    (9, "灯海叛证", "见证者如何不被收买或灭口", "见证网络反向保护主角"),
    (10, "禁区残账", "古债残页为何不断生成新债", "确认债源并非单一帝国错误"),
    (11, "天秤裂谷", "公共裁决能否抵抗超凡暴力", "建立可复制但脆弱的地方新法"),
    (12, "无命之城", "无命籍者能否拥有权利", "新法承认无籍者证词"),
    (13, "借寿井外", "域外债源与天庭中层的利益", "找到总账可改边界与代价"),
    (14, "旧界还账", "旧世界为何把债留给后来者", "拒绝个人登顶捷径"),
    (15, "万民持账", "新法如何成为可运作制度", "多地接入见证账网"),
    (16, "断账之战", "旧秩序如何清零证人与记录", "切断一层重复征收总链"),
    (17, "天庭复核", "谁拥有重写法权的资格", "把审判权夺回公共程序"),
    (18, "立命新法", "改账会否制造新的剥夺者", "完成可申诉、可复核、可约束的新法"),
)
FIRST100_BEATS = (
    "压迫落地", "生存选择", "证据显形", "关系代价", "程序反压",
    "局部取证", "共同体分歧", "小反转", "后果结算", "更高压力",
)


def _write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_longform_contract() -> dict[str, Any]:
    volumes = []
    for number, name, question, outcome in VOLUMES:
        volumes.append({
            "volume": number,
            "name": name,
            "chapter_target": 100,
            "core_question": question,
            "irreversible_outcome": outcome,
            "required_payoff_cadence": {"local_payoff_every_chapters": 10, "structural_reversal_every_chapters": [25, 35]},
        })
    return {
        "version": VERSION,
        "status": "owner_accepted_active",
        "project": "《借天改命账》",
        "target_chapters": 1800,
        "target_chinese_characters": [6000000, 6800000],
        "chapter_character_target": [3200, 3800],
        "volumes": volumes,
        "cross_volume_hooks": ["mother_life_debt", "community_legal_witness", "ancient_debt_origin"],
        "price_engine": "cost_conserved_with_verified_liability_migration",
        "witness_network_evolution": ["local_causal_anchor", "cross_city_reviewability", "public_right_of_appeal"],
        "power_law_constraint": "high_rank_power_depends_on_recognized_life_rights_and_cannot_erase_anchored_facts_without_backlash",
        "mother_debt_stages": ["interest_period_volumes_1_2", "principal_period_volumes_7_9", "origin_period_volumes_14_18"],
        "administrative_lens": "structural_laundering_and_exemptions_not_incompetence",
        "causality_settlement": "beneficiary_liability_consequence_all_required",
        "cross_city_witness_medium": ["local_trace", "independent_relay", "destination_review_seal"],
        "high_rank_backlash": "removes_at_least_one_of_jurisdiction_supply_or_subordinate_contract",
        "mother_debt_echo_windows": ["volumes_3_6", "volumes_10_13"],
        "production_boundary": "Owner-authorized controlled prose is limited to Volume 1 chapters 11-100 and remains subject to story-window, chapter-state, and release gates.",
    }


def build_first100_manifest() -> dict[str, Any]:
    windows = (
        (1, 10, "开局命灯危机与异常残籍"),
        (11, 30, "护阵、住户与共同体证据"),
        (31, 60, "收债追缴与第一次公开反打"),
        (61, 80, "封档、迁籍与本地胜利后果"),
        (81, 100, "共同见证、离城压力与州府入口"),
    )
    chapters = []
    for start, end, objective in windows:
        for number in range(start, end + 1):
            assets = ["character_lu_chenyuan", "npc_su_wan", "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane", "faction_life_registry_office", "technique_ledger_recognition", *STATE_LEDGER_IDS]
            guards = ["benefit_triad_required", "community_trust_not_resource"]
            lifecycle = ["artifact_ashlight_cup:chapter_0001_dormant"] if number == 1 else []
            if 2 <= number <= 80:
                lifecycle.append("artifact_ashlight_cup:canonical_acquisition_and_consent_transaction_required")
            if 11 <= number <= 20:
                guards.append("single_concealment_period_with_supervision_and_action_cost")
            if 21 <= number <= 60:
                assets.append("npc_debt_collector_gu_xun")
            if 61 <= number <= 80:
                guards.extend(["registry_office_lockstep_for_seal_or_migration", "ledger_write_topology"])
            if 81 <= number <= 100:
                assets.extend(["npc_prefecture_shadow_envoy", "artifact_prefecture_transit_registry_seal"])
                guards.append("prefecture_seal_edge_clue_only")
            chapters.append({
                "chapter_id": f"chapter-{number:04d}",
                "window": f"{start:03d}-{end:03d}",
                "beat": FIRST100_BEATS[(number - 1) % len(FIRST100_BEATS)],
                "objective": objective,
                "required_payoff": number % 10 == 0,
                "structural_reversal_window": number in {30, 60, 90, 100},
                "payoff_contract": (
                    "verified_limited_restitution_with_protagonist_survival_window_and_exposure" if number == 10
                    else "local_payoff_required" if number % 10 == 0 else "none"
                ),
                "survival_constraint": "registry_concealment_period_with_supervision_and_delayed_pursuit" if 11 <= number <= 20 else "none",
                "required_asset_ids": sorted(set(assets)),
                "required_guard_ids": guards,
                "lifecycle_constraints": lifecycle,
                "non_prose_only": True,
            })
    return {"version": VERSION, "status": "owner_accepted_active", "chapter_count": 100, "chapters": chapters}


def build_first100_guard_config() -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": "owner_accepted_active",
        "benefit_triad": ["return_recipient", "liable_party", "observable_consequence"],
        "community_trust": {"resource_pool_forbidden": True},
        "concealment_period": {"chapter_range": [11, 20], "max_uses": 1, "requires": ["supervision", "action_cost"], "does_not_reduce_exposure": True},
        "artifact_ashlight_cup": {"chapter_0001_state": "dormant", "after_chapter_0001": "canonical_acquisition_and_consented_watchfire_transaction_required"},
        "prefecture_transit_seal": {"before_chapter": 81, "access": "no_full_prefecture_payload", "from_chapter_81": "edge_clue_only"},
        "ledger_write_topology": ["protagonist_strain", "registry_exposure", "mother_life_lamp", "array_integrity", "resident_reserve", "returnfire", "revealed_errors", "faction_pressure", "public_reputation", "unresolved_mysteries", "map_unlock"],
    }


def validate_longform_contract(contract: dict[str, Any]) -> dict[str, Any]:
    errors = []
    volumes = contract.get("volumes", [])
    if len(volumes) != 18:
        errors.append("longform contract must contain 18 volumes")
    if [item.get("volume") for item in volumes] != list(range(1, 19)):
        errors.append("volume IDs must be sequential 1 through 18")
    if sum(item.get("chapter_target", 0) for item in volumes) != 1800:
        errors.append("volume chapter targets must total 1800")
    if contract.get("target_chinese_characters") != [6000000, 6800000]:
        errors.append("character target must remain 6.0M-6.8M")
    if contract.get("status") != "owner_accepted_active":
        errors.append("active contract must record Owner acceptance")
    if contract.get("price_engine") != "cost_conserved_with_verified_liability_migration":
        errors.append("contract must preserve a cost-conserved price engine")
    if contract.get("witness_network_evolution") != ["local_causal_anchor", "cross_city_reviewability", "public_right_of_appeal"]:
        errors.append("contract must define three non-repeating witness network stages")
    if not contract.get("power_law_constraint") or not contract.get("mother_debt_stages"):
        errors.append("contract must define power-law and mother-debt constraints")
    if contract.get("causality_settlement") != "beneficiary_liability_consequence_all_required":
        errors.append("contract must define an observable causality settlement rule")
    if contract.get("cross_city_witness_medium") != ["local_trace", "independent_relay", "destination_review_seal"]:
        errors.append("contract must define a cross-city witness medium")
    if not contract.get("high_rank_backlash") or contract.get("mother_debt_echo_windows") != ["volumes_3_6", "volumes_10_13"]:
        errors.append("contract must preserve high-rank backlash and mother-debt echo windows")
    return {"valid": not errors, "errors": errors}


def validate_first100_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = []
    chapters = manifest.get("chapters", [])
    if len(chapters) != 100:
        errors.append("first100 manifest must contain exactly 100 chapters")
    if [item.get("chapter_id") for item in chapters] != [f"chapter-{number:04d}" for number in range(1, 101)]:
        errors.append("first100 chapter IDs must be sequential")
    if sum(bool(item.get("required_payoff")) for item in chapters) != 10:
        errors.append("first100 must contain ten required local payoffs")
    if any(not item.get("non_prose_only") for item in chapters):
        errors.append("first100 must remain non-prose")
    if len(chapters) >= 10 and chapters[9].get("payoff_contract") != "verified_limited_restitution_with_protagonist_survival_window_and_exposure":
        errors.append("chapter 10 must carry the bounded restitution payoff contract")
    if len(chapters) >= 20 and any(item.get("survival_constraint") != "registry_concealment_period_with_supervision_and_delayed_pursuit" for item in chapters[10:20]):
        errors.append("chapters 11-20 must preserve the bounded concealment survival constraint")
    known_assets = {item["asset_id"] for item in _read(runtime_path("system/creation_assets/project_assets.v0.2.json")).get("assets", [])}
    if any(set(item.get("required_asset_ids", [])) - known_assets for item in chapters):
        errors.append("first100 references unknown assets")
    if manifest.get("status") != "owner_accepted_active":
        errors.append("active manifest must record Owner acceptance")
    return {"valid": not errors, "errors": errors}


def validate_first100_guard_config(config: dict[str, Any]) -> dict[str, Any]:
    errors = []
    if config.get("benefit_triad") != ["return_recipient", "liable_party", "observable_consequence"]:
        errors.append("benefit triad must be exact")
    if config.get("community_trust", {}).get("resource_pool_forbidden") is not True:
        errors.append("community trust must not become a resource pool")
    concealment = config.get("concealment_period", {})
    if concealment.get("chapter_range") != [11, 20] or concealment.get("max_uses") != 1 or set(concealment.get("requires", [])) != {"supervision", "action_cost"}:
        errors.append("concealment period contract is invalid")
    lamp = config.get("artifact_ashlight_cup", {})
    if lamp.get("chapter_0001_state") != "dormant" or not lamp.get("after_chapter_0001"):
        errors.append("ashlight cup lifecycle must preserve canonical chapter 1 dormancy")
    seal = config.get("prefecture_transit_seal", {})
    if seal.get("before_chapter") != 81 or seal.get("from_chapter_81") != "edge_clue_only":
        errors.append("prefecture seal access control is invalid")
    if len(config.get("ledger_write_topology", [])) != 11:
        errors.append("ledger write topology must include eleven entries")
    return {"valid": not errors, "errors": errors}


def write_longform_candidate_contracts() -> dict[str, Any]:
    contract = build_longform_contract()
    manifest = build_first100_manifest()
    _write(CONTRACT_PATH, contract)
    _write(FIRST100_PATH, manifest)
    guards = build_first100_guard_config()
    _write(GUARD_CONFIG_PATH, guards)
    return {"valid": validate_longform_contract(contract)["valid"] and validate_first100_manifest(manifest)["valid"] and validate_first100_guard_config(guards)["valid"], "contract": validate_longform_contract(contract), "first100": validate_first100_manifest(manifest), "guards": validate_first100_guard_config(guards)}


def build_longform_readiness() -> dict[str, Any]:
    contract = _read(CONTRACT_PATH) if CONTRACT_PATH.exists() else {}
    manifest = _read(FIRST100_PATH) if FIRST100_PATH.exists() else {}
    review_text = FINAL_REVIEW_PATH.read_text(encoding="utf-8") if FINAL_REVIEW_PATH.exists() else ""
    owner_accepted = any(
        item.get("decision_type") == "accept_review"
        and "borrowed-heaven-longform-v024" in item.get("authorized_scope", [])
        for item in load_decisions()
    )
    checks = {
        "longform_contract_valid": validate_longform_contract(contract)["valid"],
        "first100_manifest_valid": validate_first100_manifest(manifest)["valid"],
        "antigravity_final_review_accepted": "## Verdict\nACCEPT" in review_text,
        "owner_accepted": owner_accepted,
    }
    return {"valid": all(checks.values()), "checks": checks, "contract_path": str(CONTRACT_PATH), "manifest_path": str(FIRST100_PATH)}


def build_longform_first100_dry_run() -> dict[str, Any]:
    manifest = _read(FIRST100_PATH) if FIRST100_PATH.exists() else {}
    guards = _read(GUARD_CONFIG_PATH) if GUARD_CONFIG_PATH.exists() else {}
    active = _read(ACTIVE_BLUEPRINT_PATH) if ACTIVE_BLUEPRINT_PATH.exists() else {}
    checks = {
        "first100_manifest_valid": validate_first100_manifest(manifest)["valid"],
        "guard_config_valid": validate_first100_guard_config(guards)["valid"],
        "active_blueprint_governed": (
            active.get("status") == "active_production_governed"
            and active.get("prose_allowed") is True
            and active.get("story_window_contract_required") is True
        ),
    }
    return {"valid": all(checks.values()), "checks": checks, "mode": "governed prose; dry run performs no model invocation or chapter mutation"}


def promote_longform_blueprint() -> dict[str, Any]:
    readiness = build_longform_readiness()
    if not readiness["valid"]:
        blocked = [name for name, value in readiness["checks"].items() if not value]
        raise RuntimeError("longform promotion is blocked: " + ", ".join(blocked))
    payload = {
        "version": "0.24",
        "project": "《借天改命账》",
        "status": "active_production_governed",
        "contract_path": str(CONTRACT_PATH.relative_to(runtime_path("."))),
        "first100_manifest_path": str(FIRST100_PATH.relative_to(runtime_path("."))),
        "owner_scope": "borrowed-heaven-longform-v024",
        "prose_allowed": True,
        "authorized_chapter_range": [11, 100],
        "accepted_calibration_range": [1, 15],
        "story_window_contract_required": True,
        "next_required_gate": "story_window_011_020_validation",
    }
    _write(ACTIVE_BLUEPRINT_PATH, payload)
    return {"valid": True, "active_blueprint_path": str(ACTIVE_BLUEPRINT_PATH), "payload": payload}
