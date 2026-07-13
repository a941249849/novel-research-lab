from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from nrl_paths import runtime_path


INTENT_ROOT = runtime_path("system/production_runtime/intents/longform_cluster1_v024")
SCHEMA_PATH = runtime_path("system/production_runtime/schemas/chapter_intent.schema.json")
ASSETS = [
    "character_lu_chenyuan", "npc_su_wan", "npc_registrar_qiu_shen", "npc_mo_jinglan",
    "bond_mother_su_wan", "bond_mudlamp_lane_trust", "faction_mudlamp_lane",
    "faction_life_registry_office", "technique_ledger_recognition", "foreshadowing_cinder_seal_rain",
    "state_ledger_protagonist_strain", "state_ledger_half_life_registry_exposure",
    "state_ledger_mother_life_lamp_countdown", "state_ledger_mudlamp_array_integrity",
    "state_ledger_resident_lifefire_reserve", "state_ledger_poorcity_returnfire",
    "state_ledger_revealed_account_errors", "state_ledger_faction_pressure",
    "state_ledger_public_reputation", "state_ledger_unresolved_mysteries", "state_ledger_map_unlock_status",
]

BEATS = {
    3: ("让午后复核留下可被第三方否认也可被追查的局部痕迹，陆沉渊必须选择保住母亲命灯还是保住证据。", "可见灰痕与口述必须互相校验；识账只可辨认本地错位。"),
    4: ("把一户人的命灯压力扩展为泥灯巷的共同风险，让陆沉渊接受街坊有拒绝见证的权利。", "共同体不被当作资源；任何帮助都保留退出与拒绝。"),
    5: ("命籍衙以程序理由收紧复核，主角用残页时间差证明一项局部记录无法自洽。", "不能把程序漏洞直接等同于完整真相；必须留下追查后果。"),
    6: ("母亲的命灯余波迫使主角放弃一次安全选择，换取不伤及邻里的有限证据保全。", "亲缘选择不许以第三方寿火代偿。"),
    7: ("让本地执行者与街坊各自暴露恐惧和利益，主角取得一条可复核但不完整的错账链。", "不得把敌人写成无理由恶意；证据只覆盖本地一段。"),
    8: ("复核压力转化为实际追缴前兆，主角必须承受一次识账反噬来确定错误归属。", "反噬要体现在身体、暴露或家庭压力；不得升级战力。"),
    9: ("让共同体见证形成初步因果锚，同时令命籍衙获得更准确的异常残籍线索。", "见证不是胜利；锚定不能解决母亲寿债或贫城全账。"),
    10: ("完成一次合法、有限、可见的错征返还：母亲得短缓冲，主角获得一次续存窗口，双方暴露同步上升。", "返还必须绑定受益者、承担方与可观察后果；不得解除核心寿债。"),
}


def _intent(number: int) -> dict[str, Any]:
    purpose, constraint = BEATS[number]
    return {
        "chapter_id": f"chapter-{number:04d}",
        "dramatic_purpose": purpose,
        "must_keep": [
            "陆沉渊仍处于燃命境初成，只能使用普通识账与本地灰痕辨认。",
            "残命灯盏不得取得、唤醒、持有、激活或使用。",
            "州府命库只可作为远端压力，不得出现全貌、人物交锋或地图展开。",
            constraint,
        ],
        "must_avoid": [
            "不得引入未登记人物、势力、器物、地点或能力。",
            "不得以共同体信任、孩童命火、住户命火或第三方寿火作为可消耗资源。",
            "不得进行公开审判、高阶斗法、永久清偿或越级胜利。",
            "不得把审查建议、推测或未观察事实写成状态变化。",
        ],
        "expected_state_deltas": [],
        "required_asset_ids": ASSETS,
        "active_hook_ids": ["foreshadowing_cinder_seal_rain"],
        "scene_constraints": [
            "舞台限于贫城、泥灯巷与命籍衙的本地压力范围。",
            "每项收益都必须能在后续观察中绑定返还对象、承担方与可观察后果。",
            "每次识账都必须带来可见代价或程序性暴露。",
            "结尾只推进到下一次本地程序追缴或监督，不得换图。",
        ],
    }


def write_cluster1_intents() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    files = []
    for number in sorted(BEATS):
        intent = _intent(number)
        jsonschema.validate(intent, schema)
        path = INTENT_ROOT / f"chapter-{number:04d}.v0.24.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(intent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files.append(str(path))
    return {"valid": True, "chapter_ids": [f"chapter-{number:04d}" for number in sorted(BEATS)], "files": files}
