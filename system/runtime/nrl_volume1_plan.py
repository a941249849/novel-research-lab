from __future__ import annotations

"""Non-prose production contract for Volume 1 of Borrowed Heaven Life Account."""

import json
from pathlib import Path
from typing import Any

import jsonschema

from nrl_creation_schemas import validate_creation_asset_store
from nrl_paths import ROOT, runtime_path


PLAN_VERSION = "0.1"
PLAN_PATH = runtime_path("system/production_runtime/plans/volume1_chapter_intent_manifest.v0.1.json")
LEDGER_PATH = runtime_path("system/production_runtime/state/volume1_initial_state.v0.1.json")

LEDGER_IDS = (
    "state_ledger_protagonist_strain",
    "state_ledger_half_life_registry_exposure",
    "state_ledger_mother_life_lamp_countdown",
    "state_ledger_mudlamp_array_integrity",
    "state_ledger_resident_lifefire_reserve",
    "state_ledger_poorcity_returnfire",
    "state_ledger_revealed_account_errors",
    "state_ledger_faction_pressure",
    "state_ledger_public_reputation",
    "state_ledger_unresolved_mysteries",
    "state_ledger_map_unlock_status",
)

CLUSTERS = (
    (1, "半寿残页与母亲命灯", "建立本地错账、母亲寿债与程序盯防", "不得取得或使用残命灯盏；不得开启州府地图"),
    (2, "护阵寿裂与贫城互保", "把个人压力转为可撤回的共同体证据", "不得公开审判；不得证明完整转运链"),
    (3, "收债者追缴", "让有限取证承受第一次追缴对抗", "不得越级胜利；不得高阶改账"),
    (4, "命审台反转", "完成一次局部公开反打并保留代价", "不得解释古债全貌；不得解除母亲寿债"),
    (5, "寿库封档与州府边缘", "让本地胜利承受封档与更高法权反压", "不得展开州府全貌；不得解决最终敌人"),
    (6, "贫城不交人与换图压力", "完成有限局部改账并打开下一地图压力", "不得彻底解除母亲寿债；不得解释天庭总账"),
)

BEATS = (
    "压力落地", "行动准备", "可见证据", "关系选择", "局部受挫",
    "代价推进", "线索重组", "小反转", "后果结算", "下一段压力",
)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_volume1_manifest() -> dict[str, Any]:
    chapters = []
    for cluster, title, objective, forbidden in CLUSTERS:
        for offset, beat in enumerate(BEATS, start=1):
            ordinal = (cluster - 1) * 10 + offset
            required = [
                "character_lu_chenyuan", "npc_su_wan", "bond_mother_su_wan",
                "bond_mudlamp_lane_trust", "faction_mudlamp_lane",
                "faction_life_registry_office", "technique_ledger_recognition",
                *LEDGER_IDS,
            ]
            if cluster >= 2:
                required.append("artifact_ashlight_cup")
            if cluster >= 3:
                required.append("npc_debt_collector_gu_xun")
            if cluster >= 5:
                required.extend(["npc_cluster5_black_market_transaction_role", "artifact_prefecture_transit_registry_seal"])
            if cluster == 6:
                required.append("npc_prefecture_shadow_envoy")
            chapters.append({
                "chapter_id": f"chapter-{ordinal:04d}",
                "cluster": cluster,
                "cluster_title": title,
                "beat": beat,
                "dramatic_function": objective,
                "required_asset_ids": sorted(set(required)),
                "state_domains": list(LEDGER_IDS),
                "must_not_activate": [forbidden],
                "non_prose_only": True,
            })
    return {
        "version": PLAN_VERSION,
        "project": "《借天改命账》",
        "scope": "Volume 1 only; non-prose chapter-intent manifest",
        "chapter_count": 60,
        "chapters": chapters,
    }


def build_initial_state_contract() -> dict[str, Any]:
    # Values are semantic baselines only. They do not invent a numeric debt balance or scene event.
    states = {
        "state_ledger_protagonist_strain": {"initial": "half_life_unstable", "allowed": ["worsen_with_observed_cost", "recover_with_rest_and_care"], "evidence": ["visible_bodily_or_cognitive_consequence"], "peers": ["state_ledger_half_life_registry_exposure", "state_ledger_mother_life_lamp_countdown"]},
        "state_ledger_half_life_registry_exposure": {"initial": 0, "bounds": [0, 100], "allowed": ["increase_with_observed_trace", "decrease_only_with_verified_concealment_or_legal_change"], "evidence": ["trigger_asset", "perceivable_lock_or_trace"], "peers": ["state_ledger_faction_pressure", "state_ledger_public_reputation"]},
        "state_ledger_mother_life_lamp_countdown": {"initial": "countdown_active", "allowed": ["worsen_with_observed_spillover", "buffer_without_debt_erasure"], "evidence": ["visible_lamp_effect", "trigger_reference"], "peers": ["state_ledger_protagonist_strain", "state_ledger_poorcity_returnfire"]},
        "state_ledger_mudlamp_array_integrity": {"initial": "fractured_but_functioning", "allowed": ["worsen_with_observed_crack", "repair_with_consented_watchfire_and_repair"], "evidence": ["array_mark_or_repair_observation"], "peers": ["state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire"]},
        "state_ledger_resident_lifefire_reserve": {"initial": "uncommitted", "allowed": ["change_only_with_named_consent_and_withdrawal_record"], "evidence": ["named_consent", "actual_transfer_or_refusal"], "peers": ["state_ledger_mudlamp_array_integrity"]},
        "state_ledger_poorcity_returnfire": {"initial": "none_verified", "allowed": ["increase_only_with_witnessed_source_and_return"], "evidence": ["recognizable_ash_trace", "affected_resident_witness"], "peers": ["state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure", "state_ledger_mudlamp_array_integrity", "state_ledger_resident_lifefire_reserve"]},
        "state_ledger_revealed_account_errors": {"initial": "none_verified", "allowed": ["add_only_with_verified_record_and_consequence"], "evidence": ["verified_existing_record", "pressure_or_public_consequence"], "peers": ["state_ledger_faction_pressure", "state_ledger_public_reputation", "state_ledger_unresolved_mysteries"]},
        "state_ledger_faction_pressure": {"initial": "local_registry_pressure", "allowed": ["change_only_with_named_existing_faction_and_consequence"], "evidence": ["existing_faction_asset", "trigger_and_outcome"], "peers": ["state_ledger_half_life_registry_exposure", "state_ledger_public_reputation"]},
        "state_ledger_public_reputation": {"initial": "unknown_to_public", "allowed": ["change_only_with_witness_scope_and_consequence"], "evidence": ["witness_scope", "verified_public_event"], "peers": ["state_ledger_revealed_account_errors", "state_ledger_faction_pressure"]},
        "state_ledger_unresolved_mysteries": {"initial": ["mother_debt_source", "poor_city_old_account", "half_life_anomaly"], "allowed": ["reclassify_only_with_outline_question_and_peer_transaction"], "evidence": ["canonical_outline_question", "verified_peer_change"], "peers": ["state_ledger_revealed_account_errors", "state_ledger_map_unlock_status"]},
        "state_ledger_map_unlock_status": {"initial": "poor_city_only", "allowed": ["advance_only_along_outline_boundaries"], "evidence": ["canonical_boundary_credential", "mystery_or_exposure_peer"], "peers": ["state_ledger_unresolved_mysteries", "state_ledger_half_life_registry_exposure"]},
    }
    return {"version": PLAN_VERSION, "project": "《借天改命账》", "mode": "non-prose operational state contract", "states": states}


def validate_volume1_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = []
    chapters = manifest.get("chapters", [])
    if manifest.get("chapter_count") != 60 or len(chapters) != 60:
        errors.append("manifest must contain exactly 60 chapters")
    expected_ids = [f"chapter-{index:04d}" for index in range(1, 61)]
    if [item.get("chapter_id") for item in chapters] != expected_ids:
        errors.append("chapter IDs must be sequential chapter-0001 through chapter-0060")
    for cluster in range(1, 7):
        entries = [item for item in chapters if item.get("cluster") == cluster]
        if len(entries) != 10:
            errors.append(f"cluster {cluster} must contain exactly 10 chapters")
    known_assets = {item["asset_id"] for item in _read_json(runtime_path("system/creation_assets/project_assets.v0.2.json")).get("assets", [])}
    for item in chapters:
        unknown = set(item.get("required_asset_ids", [])) - known_assets
        if unknown:
            errors.append(f"{item.get('chapter_id')} references unknown assets: {', '.join(sorted(unknown))}")
        if not item.get("non_prose_only"):
            errors.append(f"{item.get('chapter_id')} is not marked non_prose_only")
        if set(item.get("state_domains", [])) != set(LEDGER_IDS):
            errors.append(f"{item.get('chapter_id')} does not cover the canonical state domains")
    return {"valid": not errors, "errors": errors, "chapter_count": len(chapters)}


def validate_initial_state_contract(contract: dict[str, Any]) -> dict[str, Any]:
    errors = []
    states = contract.get("states", {})
    if set(states) != set(LEDGER_IDS):
        errors.append("state contract must cover every canonical Volume 1 ledger")
    for ledger_id in LEDGER_IDS:
        state = states.get(ledger_id, {})
        if "initial" not in state:
            errors.append(f"{ledger_id} is missing initial")
        for key in ("allowed", "evidence", "peers"):
            if not state.get(key):
                errors.append(f"{ledger_id} is missing {key}")
        if ledger_id in states and any(peer not in LEDGER_IDS for peer in state.get("peers", [])):
            errors.append(f"{ledger_id} has non-canonical peer ledger")
    return {"valid": not errors, "errors": errors, "ledger_count": len(states)}


def build_volume1_dry_run() -> dict[str, Any]:
    manifest = _read_json(PLAN_PATH) if PLAN_PATH.exists() else {}
    contract = _read_json(LEDGER_PATH) if LEDGER_PATH.exists() else {}
    manifest_result = validate_volume1_manifest(manifest)
    state_result = validate_initial_state_contract(contract)
    asset_result = validate_creation_asset_store()
    checks = {"manifest_valid": manifest_result["valid"], "state_contract_valid": state_result["valid"], "creation_assets_valid": asset_result["valid"]}
    return {"valid": all(checks.values()), "checks": checks, "manifest": manifest_result, "state_contract": state_result, "mode": "no prose, no model invocation, no chapter runtime mutation"}


def write_volume1_production_contracts() -> dict[str, Any]:
    _write_json(PLAN_PATH, build_volume1_manifest())
    _write_json(LEDGER_PATH, build_initial_state_contract())
    return build_volume1_dry_run()
