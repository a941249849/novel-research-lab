from __future__ import annotations

"""Canonical 100-chapter Volume 1 intent contract for the 6M-character route."""

import json
from pathlib import Path
from typing import Any

import jsonschema

from nrl_paths import runtime_path
from nrl_projects import require_planning_profile


VERSION = "0.25"
SCOPE_PREFIX = "longform_volume1_v025"
INTENT_ROOT = runtime_path("system/production_runtime/intents/longform_volume1_v025")
SCHEMA_PATH = runtime_path("system/production_runtime/schemas/chapter_intent.schema.json")
MANIFEST_PATH = runtime_path("system/production_runtime/plans/borrowed_heaven_volume1_production_manifest.v0.25.json")

BASE_ASSETS = (
    "character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan",
    "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane",
    "faction_life_registry_office", "technique_ledger_recognition", "technique_backlash_guard",
    "foreshadowing_cinder_seal_rain", "state_ledger_protagonist_strain",
    "state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown",
    "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve",
    "state_ledger_poorcity_returnfire", "state_ledger_revealed_account_errors",
    "state_ledger_faction_pressure", "state_ledger_public_reputation",
    "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status",
)

WINDOWS = (
    (11, 20, "护阵寿裂", "护阵、住户与共同体证据", "监督下仅允许一次有行动代价的有限遮掩；共同体可拒绝。", ("artifact_ashlight_cup",)),
    (21, 30, "收债追缴", "收债追缴与第一次公开反打", "每次反打只改正一段可验证的错误归属，追缴后果必须保留。", ("artifact_ashlight_cup", "npc_debt_collector_gu_xun")),
    (31, 40, "命审台反转", "命审台见证与局部公开反打", "公开见证只能锚定亲见事实，不能替代完整因果链。", ("artifact_ashlight_cup", "npc_debt_collector_gu_xun")),
    (41, 50, "寿库封档", "封档压力、证据交易与废命地线索", "高阶法权只能以边缘压力出现，不得提前展示州府全貌。", ("artifact_ashlight_cup", "npc_debt_collector_gu_xun", "npc_cluster5_black_market_transaction_role")),
    (51, 60, "贫城不交人", "共同体承担、首笔局部改账与贫城拒绝交人", "卷段成果必须可见且不可逆，但不得解除母亲核心寿债。", ("artifact_ashlight_cup", "npc_debt_collector_gu_xun", "technique_embertrace_return")),
    (61, 70, "封档余震", "胜利后果、封档与迁籍追捕", "局部胜利必须提高身份暴露与证据保全的现实成本。", ("artifact_ashlight_cup", "npc_debt_collector_gu_xun", "faction_prefecture_life_treasury")),
    (71, 80, "迁籍裂口", "迁籍压力与州府入口的可复核边缘", "只能获得可复核的边缘线索，不得获得州府完整解释。", ("artifact_ashlight_cup", "faction_prefecture_life_treasury", "artifact_prefecture_transit_registry_seal")),
    (81, 90, "共同见证", "共同见证网络、离城选择与州府入口", "见证网络是权利关系，不得转为可消耗资源。", ("artifact_ashlight_cup", "faction_prefecture_life_treasury", "artifact_prefecture_transit_registry_seal", "npc_prefecture_shadow_envoy")),
    (91, 100, "离城追缴", "贫城拒绝交人、离城压力与卷末州府入口", "卷末只打开州府入口，不揭示古债全貌或完成最终清偿。", ("artifact_ashlight_cup", "faction_prefecture_life_treasury", "artifact_prefecture_transit_registry_seal", "npc_prefecture_shadow_envoy", "foreshadowing_ancient_debt_covenant_fragment")),
)

STEP_PURPOSES = (
    "将上一章留下的代价转换为具体程序压力",
    "让一名既有角色在保护、拒绝或自保之间作出可见选择",
    "用局部证据推进一次受限识账，并留下身体或暴露代价",
    "让追缴方获得更准确但仍不完整的反制线索",
    "把个人危机扩展为共同体可退出的协商冲突",
    "保全一项可复核事实，同时失去一项安全余地",
    "暴露受益者、承担方与后果之间的一段错位",
    "完成一次不越级的小反转，并令敌方改变程序策略",
    "结算本轮关系与肉身后果，不能以解释替代伤害",
    "兑现窗口承诺并留下下一窗口的更高法权压力",
)


def _window(number: int) -> tuple[Any, ...]:
    return next(item for item in WINDOWS if item[0] <= number <= item[1])


def build_volume1_intent(number: int) -> dict[str, Any]:
    if not 11 <= number <= 100:
        raise ValueError("Volume 1 v0.25 only covers chapters 11-100")
    start, end, arc, objective, constraint, additions = _window(number)
    step = (number - start) % 10
    assets = sorted(set((*BASE_ASSETS, *additions)))
    purpose = f"{arc}：{STEP_PURPOSES[step]}，服务于“{objective}”。"
    must_keep = [
        "陆沉渊仍只能在已验证的本地权限内识账；任何收益都必须付出身体、关系、身份或程序代价。",
        "苏晚、街坊与见证者均有拒绝权，不得把共同体信任、住户命火或第三方寿火作为资源。",
        constraint,
        "每项可写状态变化必须能由正文观察绑定到既有资产、返还对象、承担方与可观察后果。",
    ]
    must_avoid = [
        "不得引入未登记人物、势力、器物、地点、能力或地图结论。",
        "不得将审查建议、推测或叙事解释写成已经发生的状态变化。",
        "不得以越级胜利、永久清偿、无代价升级或共同体牺牲解决冲突。",
        "不得复制语料作品的名称、场景、签名系统、情节或语言风格。",
    ]
    return {
        "chapter_id": f"chapter-{number:04d}",
        "dramatic_purpose": purpose,
        "must_keep": must_keep,
        "must_avoid": must_avoid,
        "expected_state_deltas": [],
        "required_asset_ids": assets,
        "active_hook_ids": ["foreshadowing_cinder_seal_rain"],
        "scene_constraints": [
            f"本章只推进第 {start}-{end} 章窗口“{objective}”中的一个可观察步骤。",
            "至少呈现一项具体动作、感官后果或关系选择；禁止用设定说明替代场景。",
            "结尾必须留下下一次程序追缴、见证选择或证据复核，不得跳过窗口节奏。",
        ],
    }


def build_volume1_manifest() -> dict[str, Any]:
    require_planning_profile("borrowed_heaven_v1")
    return {
        "version": VERSION,
        "status": "owner_authorization_required_for_prose",
        "canonical_scale": {"total_volumes": 18, "total_chapters": 1800, "target_characters": [6000000, 6800000]},
        "volume": {"number": 1, "name": "贫城错账", "chapter_count": 100, "chapter_character_target": [3200, 3800]},
        "production_scope": {"prefix": SCOPE_PREFIX, "chapter_range": [1, 100], "batch_size": 10},
        "supersedes": ["docs/production/borrowed-heaven-production-blueprint-v0.1.md"],
        "chapters": [build_volume1_intent(number) for number in range(11, 101)],
    }


def validate_volume1_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    chapters = manifest.get("chapters", [])
    expected = [f"chapter-{number:04d}" for number in range(11, 101)]
    if [item.get("chapter_id") for item in chapters] != expected:
        errors.append("Volume 1 intent manifest must contain chapters 11-100 in order")
    if manifest.get("volume", {}).get("chapter_count") != 100:
        errors.append("Volume 1 must contain 100 chapters on the active longform route")
    if manifest.get("production_scope", {}).get("chapter_range") != [1, 100]:
        errors.append("Volume 1 production scope must be bounded to chapters 1-100")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    for chapter in chapters:
        try:
            jsonschema.validate(chapter, schema)
        except jsonschema.ValidationError as error:
            errors.append(f"{chapter.get('chapter_id', 'unknown')}: {error.message}")
    return {"valid": not errors, "errors": errors, "chapter_count": len(chapters)}


def write_volume1_intents() -> dict[str, Any]:
    manifest = build_volume1_manifest()
    validation = validate_volume1_manifest(manifest)
    if not validation["valid"]:
        return validation
    for intent in manifest["chapters"]:
        path = INTENT_ROOT / f"{intent['chapter_id']}.v0.25.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(intent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"valid": True, "manifest_path": str(MANIFEST_PATH), "intent_count": len(manifest["chapters"])}
