from __future__ import annotations

"""Project-isolated, non-prose production preparation and readiness checks."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema

from nrl_paths import ROOT
from nrl_literary_semantics import validate_project_semantic_contracts
from nrl_owner_gate import load_decisions, save_decisions
from nrl_projects import (
    PROJECT_SCHEMA_PATH,
    REGISTRY_PATH,
    load_project,
    load_project_registry,
    project_config_path,
    validate_project_isolation,
)


VERSION = "1.1"
WINDOW_SIZE = 10
CANONICAL_SOURCES = (
    "project_state.json",
    "design/story_bible.md",
    "design/outline_tree.md",
    "design/production_blueprint.md",
    "design/character_highlight_matrix.v1.json",
    "design/world_progression_atlas.v1.json",
    "design/embedded_history_engine.v1.json",
    "production_runtime/plans/volume1_semantic_beat_contract.v1.json",
    "creation_assets/project_assets.json",
    "production_runtime/plans/volume1_outline.v1.json",
    "production_runtime/plans/volume1_production_manifest.v1.json",
    "production_runtime/state/canonical_initial_state.v1.json",
    "production_runtime/chapter_titles.volume1.json",
    "production_runtime/production_readiness/audit-contract.v0.1.json",
    "production_runtime/quality/first_window_quality_contract.v1.json",
    "production_runtime/quality/calibration_quality_evidence.v1.json",
    "validation/project_reconciliation.json",
    "validation/project_reconciliation_application.json",
    "validation/literary_semantic_application.v1.json",
)
CANONICAL_RUNTIME_SOURCES = tuple(
    f"system/runtime/{path.name}"
    for path in sorted((ROOT / "system/runtime").glob("*.py"))
) + (
    "system/runtime/opencode_direct.mjs",
    "system/production_runtime/schemas/chapter_generation.schema.json",
    "system/production_runtime/schemas/chapter_intent.schema.json",
    "system/production_runtime/schemas/chapter_observation.schema.json",
    "system/production_runtime/schemas/chapter_registry.schema.json",
    "system/production_runtime/schemas/chapter_settlement.schema.json",
    "system/production_runtime/schemas/continuity_audit.schema.json",
    "system/production_runtime/schemas/story_window.schema.json",
    "system/production_runtime/schemas/volume_outline.schema.json",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _review_document_accepts(
    path: Path, baseline_sha256: str, allowed_verdicts: set[str]
) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    verdicts = re.findall(r"(?m)^\s*VERDICT:\s*([A-Z_]+)\s*$", text)
    baseline_lines = re.findall(r"(?m)^\s*BASELINE:\s*([0-9a-f]{64})\s*$", text)
    return (
        len(verdicts) == 1
        and verdicts[0] in allowed_verdicts
        and baseline_lines == [baseline_sha256]
    )


def validate_provider_unavailable_evidence(
    payload: dict[str, Any], baseline_sha256: str
) -> bool:
    """Validate a baseline-bound failed attempt against the preferred provider."""
    preferred = payload.get("preferred_provider")
    attempts = payload.get("attempts")
    if (
        preferred != "antigravity"
        or payload.get("status") != "unavailable"
        or payload.get("bound_baseline_sha256") != baseline_sha256
        or not isinstance(attempts, list)
        or not attempts
    ):
        return False
    allowed_results = {
        "provider_error",
        "quota_exhausted",
        "rate_limited",
        "nonzero_exit",
        "timeout",
    }
    for attempt in attempts:
        if (
            not isinstance(attempt, dict)
            or attempt.get("provider") != preferred
            or not isinstance(attempt.get("returncode"), int)
            or attempt.get("returncode") == 0
            or attempt.get("result") not in allowed_results
            or not attempt.get("started_at")
            or not attempt.get("finished_at")
        ):
            return False
        request_path = ROOT / str(attempt.get("request_artifact", ""))
        log_path = ROOT / str(attempt.get("log_artifact", ""))
        if (
            not request_path.is_file()
            or attempt.get("request_artifact_sha256") != _sha256(request_path)
            or not log_path.is_file()
            or attempt.get("log_artifact_sha256") != _sha256(log_path)
        ):
            return False
    return True


def resolve_independent_review_binding(
    review_index: dict[str, Any], baseline_sha256: str
) -> dict[str, Any] | None:
    """Validate a provider-aware independent review and its execution evidence."""
    relative = review_index.get("independent_review_path")
    if not relative:
        return None
    provider = str(review_index.get("independent_review_provider", ""))
    model = str(review_index.get("independent_review_model", ""))
    path = ROOT / str(relative)
    execution_path = ROOT / str(
        review_index.get("independent_review_execution_path", "")
    )
    if (
        provider not in {"antigravity", "opencode-go"}
        or not model
        or review_index.get("independent_review_verdict")
        not in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
        or not path.is_file()
        or review_index.get("independent_review_sha256") != _sha256(path)
        or not _review_document_accepts(
            path, baseline_sha256, {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
        )
        or not execution_path.is_file()
        or review_index.get("independent_review_execution_sha256")
        != _sha256(execution_path)
    ):
        return None
    execution = _read_json(execution_path)
    if (
        execution.get("provider") != provider
        or execution.get("model") != model
        or execution.get("returncode") != 0
        or execution.get("bound_baseline_sha256") != baseline_sha256
        or execution.get("review_artifact") != str(path.relative_to(ROOT))
        or execution.get("review_artifact_sha256") != _sha256(path)
        or not execution.get("started_at")
        or not execution.get("finished_at")
    ):
        return None
    request_path = ROOT / str(execution.get("request_artifact", ""))
    if (
        not request_path.is_file()
        or execution.get("request_artifact_sha256") != _sha256(request_path)
    ):
        return None
    if provider == "opencode-go":
        unavailable_path = ROOT / str(
            review_index.get("preferred_provider_unavailable_evidence_path", "")
        )
        if (
            not review_index.get("degradation_reason")
            or not unavailable_path.is_file()
            or review_index.get("preferred_provider_unavailable_evidence_sha256")
            != _sha256(unavailable_path)
        ):
            return None
        unavailable = _read_json(unavailable_path)
        if not validate_provider_unavailable_evidence(
            unavailable, baseline_sha256
        ):
            return None
    return {
        "provider": provider,
        "model": model,
        "path": path,
        "sha256": _sha256(path),
        "execution_path": execution_path,
    }


def project_workspace(project_id: str | None = None) -> Path:
    project = load_project(project_id)
    return ROOT / str(project["workspace"])


def volume1_chapter_count(project_id: str | None = None) -> int:
    workspace = project_workspace(project_id)
    outline_path = workspace / "production_runtime/plans/volume1_outline.v1.json"
    if not outline_path.is_file():
        return 100 if load_project(project_id).get("storage_mode") == "legacy_v0" else 0
    outline = _read_json(outline_path)
    chapters = outline.get("chapters", [])
    declared = int(outline.get("chapter_count", len(chapters)))
    return declared if declared == len(chapters) else 0


def volume1_windows(project_id: str | None = None) -> tuple[tuple[int, int], ...]:
    count = volume1_chapter_count(project_id)
    return tuple(
        (start, min(start + WINDOW_SIZE - 1, count))
        for start in range(1, count + 1, WINDOW_SIZE)
    )


def build_production_batch_plan(
    start: int, end: int, project_id: str | None = None
) -> dict[str, Any]:
    """Resolve a bounded batch against the active project's own Volume 1."""
    project = load_project(project_id)
    selected = str(project["project_id"])
    count = volume1_chapter_count(selected)
    minimum = 12 if project.get("storage_mode") == "legacy_v0" else 1
    if not minimum <= start <= end <= count:
        raise RuntimeError(
            f"Volume 1 batch range must be within chapters {minimum}-{count}"
        )
    window = next(
        (
            (window_start, window_end)
            for window_start, window_end in volume1_windows(selected)
            if window_start <= start <= end <= window_end
        ),
        None,
    )
    if window is None:
        raise RuntimeError("production batch cannot cross a canonical story window")
    workspace = project_workspace(selected)
    intent_paths = []
    for ordinal in range(start, end + 1):
        if project.get("storage_mode") == "legacy_v0":
            path = (
                ROOT
                / "system/production_runtime/intents/longform_volume1_v025"
                / f"chapter-{ordinal:04d}.v0.25.json"
            )
        else:
            path = (
                workspace
                / "production_runtime/intents"
                / f"chapter-{ordinal:04d}.json"
            )
        if not path.is_file():
            raise RuntimeError(f"production intent is missing: {path.relative_to(ROOT)}")
        intent_paths.append(str(path.relative_to(ROOT)))
    window_start, window_end = window
    independent_required = False
    if project.get("storage_mode") != "legacy_v0":
        contract = (
            workspace
            / "production_runtime/story_windows"
            / f"window-{window_start:03d}-{window_end:03d}.v1.json"
        )
        if not contract.is_file():
            raise RuntimeError(
                f"story window contract is missing: {contract.relative_to(ROOT)}"
            )
        independent_required = bool(
            _read_json(contract)
            .get("review_policy", {})
            .get("independent_review_required")
        )
    return {
        "project_id": selected,
        "start": start,
        "end": end,
        "window": [window_start, window_end],
        "intent_paths": intent_paths,
        "review_after_batch": end == window_end,
        "independent_review_required": independent_required,
    }


def build_project_window_authorization(
    start: int,
    end: int,
    decision_id: str,
    owner_note: str,
    *,
    project_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build two hash-bound Owner decisions without mutating project state."""
    project = load_project(project_id)
    selected = str(project["project_id"])
    if project.get("storage_mode") == "legacy_v0":
        raise RuntimeError("project window authorization requires an isolated project")
    if (start, end) not in volume1_windows(selected):
        raise RuntimeError("Owner authorization must match one canonical story window")
    validation = validate_project_production(selected)
    if validation.get("valid") is not True:
        raise RuntimeError(
            "project production contract is invalid: "
            + "; ".join(validation.get("errors", []))
        )
    workspace = project_workspace(selected)
    baseline_path = workspace / "creation_assets/canonical_baseline.json"
    review_index_path = (
        workspace
        / "production_runtime/production_readiness/final-review-index.v0.1.json"
    )
    review_index = _read_json(review_index_path)
    baseline_sha = _sha256(baseline_path)
    sol_path = ROOT / str(review_index.get("sol_review_path", ""))
    independent = resolve_independent_review_binding(review_index, baseline_sha)
    if (
        review_index.get("valid") is not True
        or review_index.get("bound_baseline_sha256") != baseline_sha
        or review_index.get("sol_verdict") != "ACCEPT"
        or not sol_path.is_file()
        or not _review_document_accepts(sol_path, baseline_sha, {"ACCEPT"})
        or review_index.get("sol_review_sha256") != _sha256(sol_path)
        or independent is None
    ):
        raise RuntimeError("dual final review is missing, stale, or rejected")
    timestamp = created_at or datetime.now(timezone.utc).astimezone().replace(
        microsecond=0
    ).isoformat()
    scopes = [
        f"project_volume1_v1:{selected}:chapter-{ordinal:04d}"
        for ordinal in range(start, end + 1)
    ]
    forbidden = [
        f"{selected}:outside-window-{start:03d}-{end:03d}",
        f"{selected}:bulk-or-continuous-production",
        f"{selected}:raw-corpus-read",
        f"{selected}:publish",
    ]
    common = {
        "project_id": selected,
        "authorization_contract_version": "0.29",
        "authorized_scope": scopes,
        "forbidden_scope": forbidden,
        "expires_after_mission": (
            f"{selected}-volume1-window-{start:03d}-{end:03d}-v1"
        ),
        "bound_baseline_sha256": baseline_sha,
        "bound_sol_review_sha256": _sha256(sol_path),
        "bound_independent_review_sha256": independent["sha256"],
        "bound_independent_review_provider": independent["provider"],
        "bound_independent_review_model": independent["model"],
        "owner_note": owner_note,
        "created_at": timestamp,
    }
    return {
        "project_id": selected,
        "window": [start, end],
        "baseline_sha256": baseline_sha,
        "decisions": [
            {
                "decision_id": f"{decision_id}_intent",
                "decision_type": "authorize_next_phase",
                **common,
            },
            {
                "decision_id": f"{decision_id}_prose",
                "decision_type": "authorize_controlled_prose_test",
                **common,
            },
        ],
    }


def authorize_project_production_window(
    start: int,
    end: int,
    decision_id: str,
    owner_note: str,
    *,
    project_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Stage authorization records and make project config the activation commit."""
    authorization = build_project_window_authorization(
        start,
        end,
        decision_id,
        owner_note,
        project_id=project_id,
        created_at=created_at,
    )
    existing = load_decisions()
    new_ids = {
        str(item["decision_id"]) for item in authorization["decisions"]
    }
    if new_ids & {str(item.get("decision_id")) for item in existing}:
        raise RuntimeError("Owner production authorization decision already exists")
    selected = str(authorization["project_id"])
    project = load_project(selected)
    project["content_authorized"] = True
    project["status"] = "active_production"
    jsonschema.validate(project, _read_json(PROJECT_SCHEMA_PATH))

    registry = load_project_registry()
    matched = None
    for item in registry.get("projects", []):
        if item.get("project_id") == selected:
            item["status"] = "active_production"
            matched = item
    if matched is None:
        raise RuntimeError("project registry entry is missing")

    # Registry and decisions cannot activate prose while project.json remains
    # false. Write project.json last so any earlier failure stays fail-closed.
    _write_json(REGISTRY_PATH, registry)
    save_decisions([*existing, *authorization["decisions"]])
    _write_json(project_config_path(selected), project)
    return {
        **authorization,
        "content_authorized": True,
        "project_status": "active_production",
    }


def _family_field(asset: dict[str, Any]) -> str:
    return {
        "characters": "character.current_state",
        "npcs": "npc.current_agenda",
        "factions": "faction.status",
        "artifacts": "artifact.condition",
        "techniques": "technique.availability",
        "naming": "naming.adoption",
        "emotional_bonds": "emotional_bond.trust",
        "foreshadowing": "foreshadowing.status",
        "state_ledger": "state_ledger.value",
    }.get(str(asset.get("family")), "lifecycle_state")


def _initial_value(asset: dict[str, Any]) -> str:
    overrides = {
        "ledger_structural_load": "旧梁连接异常，未知荷载尚未验明",
        "ledger_role_residue": "角色残留未激活",
        "ledger_water_level": "风险尚未分舱",
        "ledger_public_dissent": "居民尚未成为正式异议方",
        "ledger_team_authority": "事故协作规则尚未建立",
        "ledger_maintenance_deadline": "三年维护期限尚未启动",
        "faction_maintenance_team": "候选协作关系，尚未成立",
    }
    return overrides.get(str(asset.get("asset_id")), str(asset.get("lifecycle_state", "seed")))


def _build_initial_state(assets: list[dict[str, Any]], project_id: str) -> dict[str, Any]:
    fields = []
    for asset in assets:
        fields.append(
            {
                "asset_id": asset["asset_id"],
                "field_path": _family_field(asset),
                "value": _initial_value(asset),
                "source": "canonical_project_asset",
            }
        )
        if _family_field(asset) != "lifecycle_state":
            fields.append(
                {
                    "asset_id": asset["asset_id"],
                    "field_path": "lifecycle_state",
                    "value": asset.get("lifecycle_state"),
                    "source": "canonical_project_asset",
                }
            )
    return {
        "version": VERSION,
        "project_id": project_id,
        "status": "canonical_initial_state",
        "fields": fields,
    }


def _delta_type(asset_refs: list[str], asset_map: dict[str, dict[str, Any]]) -> str:
    families = {asset_map[item]["family"] for item in asset_refs if item in asset_map}
    if families & {"artifacts", "techniques", "state_ledger"}:
        return "material_state"
    if families & {"emotional_bonds", "characters", "npcs"}:
        return "relationship_state"
    if "factions" in families:
        return "institutional_state"
    return "causal_state"


def _special_dependencies(chapter: int) -> list[str]:
    return {
        29: ["v1.ch019.outcome"],
        33: ["v1.ch010.outcome"],
        54: ["v1.ch041.outcome"],
        60: ["v1.ch029.outcome"],
    }.get(chapter, [])


def _special_deltas(
    ordinal: int, state_id: str, asset_map: dict[str, dict[str, Any]]
) -> list[dict[str, Any]] | None:
    rows: dict[int, list[tuple[str, str, str]]] = {
        19: [("char_zhou_li", "character.current_state", "周砺撤回单方无责目标，旧案转入行为与后果核查。")],
        29: [("artifact_responsibility_ledger", "artifact.condition", "未识别受影响者进入旧案核查与补偿对象范围")],
        33: [
            ("faction_maintenance_team", "lifecycle_state", "active"),
            ("faction_maintenance_team", "faction.status", "有限期夜间维护班已正式成立"),
            ("ledger_team_authority", "state_ledger.value", "双人复核、受影响者否决和退出条款已生效"),
        ],
        41: [("artifact_responsibility_ledger", "artifact.condition", "远端自动代偿旁路与可重接残件已登记")],
        54: [("artifact_responsibility_ledger", "artifact.condition", "远端旁路已物理断开，重接责任已公开")],
        60: [("artifact_responsibility_ledger", "artifact.condition", "父亲旧案成为可追索但未清偿的公共责任")],
    }
    selected = rows.get(ordinal)
    if not selected:
        return None
    return [
        {
            "state_id": state_id if index == 0 else f"{state_id}.{index + 1}",
            "asset_id": asset_id,
            "field_path": field_path,
            "after": after,
        }
        for index, (asset_id, field_path, after) in enumerate(selected)
        if asset_id in asset_map
    ]


def _build_manifest(
    outline: dict[str, Any], assets: list[dict[str, Any]], project_id: str
) -> dict[str, Any]:
    asset_map = {str(item["asset_id"]): item for item in assets}
    chapters = []
    projected = {
        (str(asset["asset_id"]), _family_field(asset)): _initial_value(asset)
        for asset in assets
    }
    projected.update({
        (str(asset["asset_id"]), "lifecycle_state"): asset.get("lifecycle_state")
        for asset in assets
    })
    for item in outline["chapters"]:
        ordinal = int(item["chapter"])
        refs = [str(asset_id) for asset_id in item.get("asset_refs", [])]
        state_id = f"v1.ch{ordinal:03d}.outcome"
        requires = ["v1.baseline"] if ordinal == 1 else [f"v1.ch{ordinal - 1:03d}.outcome"]
        requires.extend(_special_dependencies(ordinal))
        primary = asset_map[refs[0]]
        deltas = _special_deltas(ordinal, state_id, asset_map) or [
            {
                "state_id": state_id,
                "asset_id": primary["asset_id"],
                "field_path": _family_field(primary),
                "after": item["irreversible_change"],
            }
        ]
        for delta in deltas:
            key = (str(delta["asset_id"]), str(delta["field_path"]))
            delta["before"] = projected[key]
            projected[key] = delta["after"]
        chapters.append(
            {
                "chapter_id": f"chapter-{ordinal:04d}",
                "title": item["title"],
                "act": item["act"],
                "pov": item["pov"],
                "purpose": item["purpose"],
                "material_action": item["irreversible_change"],
                "required_asset_ids": refs,
                "requires_state_ids": list(dict.fromkeys(requires)),
                "establishes_state_ids": [delta["state_id"] for delta in deltas],
                "delta_type": _delta_type(refs, asset_map),
                "payoff_id": f"v1.payoff.ch{ordinal:03d}",
                "expected_state_deltas": deltas,
            }
        )
    return {
        "version": VERSION,
        "project_id": project_id,
        "volume": 1,
        "chapter_count": len(chapters),
        "canonicalization": {
            "formal_production_starts_at": "chapter-0001",
            "controlled_samples": "calibration_evidence_only",
            "sample_import_allowed": False,
        },
        "chapters": chapters,
    }


def _build_story_window(
    chapters: list[dict[str, Any]], start: int, end: int, title: str,
    asset_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    selected = chapters[start - 1 : end]
    beats = []
    for index, item in enumerate(selected):
        ordinal = int(item["chapter_id"][-4:])
        next_title = chapters[ordinal]["title"] if ordinal < len(chapters) else "第二节点退构"
        beats.append(
            {
                "chapter_id": item["chapter_id"],
                "working_title": item["title"],
                "event": f"围绕{item['title']}发生可验证事件：{item['purpose']}",
                "scene_anchor": f"第{ordinal}章的具体工艺现场与物证位置",
                "conflict": f"在《{item['title']}》现场，{item['pov']}必须在专业判断、受影响者异议与现实后果之间作出不可回避的选择。",
                "character_choice": f"面对《{item['title']}》的具体后果，{item['pov']}选择以可复核的现场行动承担代价，而不是用口头承诺绕过程序。",
                "irreversible_change": item["material_action"],
                "emotional_turn": f"本章选择改变了{item['pov']}与共同体之间的信任方向。",
                "hook_out": f"已发生的后果把下一步压力推向《{next_title}》，且不能回到本章开始状态。",
                "expected_state_deltas": [
                    f"{delta['state_id']}:{delta['asset_id']}:{delta['field_path']}"
                    for delta in item["expected_state_deltas"]
                ],
                "required_asset_ids": item["required_asset_ids"],
                "evidence_refs": list(dict.fromkeys(
                    str(ref)
                    for asset_id in item["required_asset_ids"]
                    for ref in asset_map.get(asset_id, {}).get("source_refs", [])
                )),
                "cultural_safety_checks": [
                    "只使用证据卡支持的工艺事实，不把地方知识改写为万能异术",
                    "知识所有权、署名、拒绝和退出必须保留在人物行动中",
                ],
                "source_status": "formal_plan",
            }
        )
    return {
        "version": "1.0",
        "project": title,
        "volume": 1,
        "window": {"start": start, "end": end, "name": f"正式生产窗口 {start:03d}-{end:03d}"},
        "status": "production_ready",
        "review_policy": {
            "sol_window_review_required": True,
            "independent_review_required": start in {1, 41, 61},
            "publish_authorized": False,
        },
        "start_snapshot": [
            f"第{start}章开始前只承认 canonical initial state 与已接受结算。",
            "受影响者异议、专业复核和物质后果均不得被摘要覆盖。",
            "未登记资产、能力、关系和状态变化一律禁止进入正文。",
        ],
        "end_target": [
            f"第{end}章必须完成本窗口不可逆因果链并保留卷级矛盾。",
            "所有状态变化必须由观察、终审和结算三方绑定同一修订稿。",
            "下一窗口不得在本窗口审查接受前启动正文。",
        ],
        "chapters": beats,
    }


def _build_intent(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "chapter_id": item["chapter_id"],
        "dramatic_purpose": item["purpose"],
        "must_keep": [item["material_action"], f"POV 固定为{item['pov']}"],
        "must_avoid": ["不得引入未登记资产或用旁白代替物质行动", "不得回滚已接受状态"],
        "expected_state_deltas": item["expected_state_deltas"],
        "required_asset_ids": item["required_asset_ids"],
        "active_hook_ids": [asset_id for asset_id in item["required_asset_ids"] if asset_id.startswith("foreshadow_")],
        "scene_constraints": ["冲突必须落在具体工艺现场、物证或受影响者选择上"],
    }


def _build_quality_evidence(workspace: Path, project_id: str) -> dict[str, Any]:
    validation_path = workspace / "validation/continuity_validation.v0.1.json"
    source = _read_json(validation_path) if validation_path.is_file() else {"prose_chapters": []}
    rows = []
    transitions = ("然而", "此外", "与此同时", "因此", "于是", "不过")
    abstract = ("命运", "意义", "本质", "责任", "选择")
    sensory = ("冷", "热", "痛", "血", "灰", "火", "光", "声", "气味", "手", "眼")
    for item in source.get("prose_chapters", []):
        body = str(item.get("body", ""))
        chinese_count = len(re.findall(r"[\u4e00-\u9fff]", body))
        quote_count = sum(len(value) for value in re.findall(r"“(.*?)”", body, re.DOTALL))
        rows.append({
            "chapter": item.get("chapter"),
            "title": item.get("title"),
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "reported_character_count": item.get("character_count"),
            "chinese_character_count": chinese_count,
            "dialogue_ratio": round(quote_count / chinese_count, 4) if chinese_count else 0,
            "transition_word_hits": sum(body.count(word) for word in transitions),
            "abstract_word_hits": sum(body.count(word) for word in abstract),
            "sensory_word_hits": sum(body.count(word) for word in sensory),
            "formal_quality_verdict": "NOT_APPLICABLE_CALIBRATION_ONLY",
        })
    return {
        "version": VERSION,
        "project_id": project_id,
        "status": "calibration_evidence_only_not_formal_acceptance",
        "source_validation": str(validation_path.relative_to(ROOT)) if validation_path.is_file() else None,
        "chapters": rows,
        "role_evidence": {
            "terra": "production_runtime/continuity_validation/prompts/*.terra.md",
            "luna": "production_runtime/continuity_validation/reviews/luna-state-observation.v0.1.json",
            "sol": "production_runtime/continuity_validation/reviews/sol-final-review.v0.3.md",
        },
        "limitations": [
            "historical samples do not satisfy formal 3000-character minimum",
            "formal quality evidence is generated only after authorized chapter production",
        ],
    }


def _build_quality_contract(project_id: str) -> dict[str, Any]:
    return {
        "version": VERSION,
        "project_id": project_id,
        "window": [1, 10],
        "status": "contract_ready_no_formal_prose",
        "per_chapter_required": [
            "revision_sha256", "chinese_character_count", "dialogue_ratio",
            "transition_word_hits", "rhetorical_template_hits", "abstract_word_hits",
            "sensory_word_hits", "semantic_final_audit_sha256", "writer_execution",
            "observer_execution", "reviewer_execution",
        ],
        "hard_gates": {
            "chinese_character_count": [3000, 4200],
            "blocking_or_major_final_issue_count": 0,
            "prompt_or_runtime_leak_count": 0,
            "same_model_self_certification_allowed": False,
        },
        "window_review": {
            "sol_required": True,
            "independent_review_required": True,
            "independent_review_policy": {
                "preferred_provider": "antigravity",
                "allowed_degradation_providers": ["opencode-go"],
                "owner_authorization_required": True,
                "execution_evidence_required": True,
            },
            "any_failed_chapter_blocks_window_accept": True,
        },
        "publish_authorized": False,
    }


def prepare_project_production(project_id: str | None = None) -> dict[str, Any]:
    project = load_project(project_id)
    if project.get("storage_mode") == "legacy_v0":
        raise RuntimeError("legacy_v0 uses its existing production preparation path")
    selected = str(project["project_id"])
    workspace = project_workspace(selected)
    outline_path = workspace / "production_runtime/plans/volume1_outline.v1.json"
    asset_path = workspace / "creation_assets/project_assets.json"
    outline = _read_json(outline_path)
    store = _read_json(asset_path)
    assets = store.get("assets", [])
    manifest = _build_manifest(outline, assets, selected)
    manifest_path = workspace / "production_runtime/plans/volume1_production_manifest.v1.json"
    _write_json(manifest_path, manifest)
    initial_path = workspace / "production_runtime/state/canonical_initial_state.v1.json"
    _write_json(initial_path, _build_initial_state(assets, selected))
    titles_path = workspace / "production_runtime/chapter_titles.volume1.json"
    _write_json(
        titles_path,
        {
            "version": VERSION,
            "project_id": selected,
            "chapters": [
                {"chapter_id": item["chapter_id"], "title": item["title"]}
                for item in manifest["chapters"]
            ],
        },
    )
    quality_root = workspace / "production_runtime/quality"
    _write_json(quality_root / "first_window_quality_contract.v1.json", _build_quality_contract(selected))
    _write_json(quality_root / "calibration_quality_evidence.v1.json", _build_quality_evidence(workspace, selected))
    intents_root = workspace / "production_runtime/intents"
    for item in manifest["chapters"]:
        _write_json(intents_root / f"{item['chapter_id']}.json", _build_intent(item))
    window_root = workspace / "production_runtime/story_windows"
    for old in window_root.glob("window-*.json"):
        old.unlink()
    for start, end in volume1_windows(selected):
        _write_json(
            window_root / f"window-{start:03d}-{end:03d}.v1.json",
            _build_story_window(
                manifest["chapters"], start, end, str(project["title"]),
                {str(item["asset_id"]): item for item in assets},
            ),
        )
    conflict_resolutions = [
        {
            "conflict_id": "samples-vs-formal-canon",
            "sources": ["validation/continuity_validation.v0.1.json", "design/production_blueprint.md"],
            "decision": "samples are calibration evidence only; formal production starts at chapter-0001",
            "applied_to": ["production_runtime/plans/volume1_production_manifest.v1.json", "production_runtime/chapter_registry.v0.20.json"],
        },
        {
            "conflict_id": "regional-and-medical-debt",
            "sources": ["design/story_bible.md", "design/production_blueprint.md"],
            "decision": "P1 regional evidence is sufficient for Volume 1; medical signature gate remains Volume 9 only",
            "applied_to": ["design/story_bible.md", "design/production_blueprint.md"],
        },
        {
            "conflict_id": "maintenance-team-lifecycle",
            "sources": ["creation_assets/project_assets.json", "production_runtime/plans/volume1_outline.v1.json"],
            "decision": "team remains seed until chapter-0033 records seed-to-active settlement",
            "applied_to": ["creation_assets/project_assets.json", "production_runtime/plans/volume1_production_manifest.v1.json"],
        },
    ]
    reconciliation = {
        "version": VERSION,
        "project_id": selected,
        "valid": True,
        "verdict": "ACCEPT_WITH_WARNINGS",
        "resolved": [
            "controlled samples are calibration evidence only",
            "formal production starts at chapter-0001",
            "volume1 uses 66 chapters and seven project-isolated windows",
            "maintenance team remains seed until chapter-0033",
        ],
        "remaining_warnings": ["formal prose remains blocked until final dual review and bounded Owner decision"],
        "conflict_resolutions": conflict_resolutions,
    }
    reconciliation_path = workspace / "validation/project_reconciliation.json"
    _write_json(reconciliation_path, reconciliation)
    applied_hashes = {
        str((workspace / relative).relative_to(ROOT)): _sha256(workspace / relative)
        for relative in CANONICAL_SOURCES
        if relative not in {"validation/project_reconciliation.json", "validation/project_reconciliation_application.json"}
    }
    applied_hashes[str(reconciliation_path.relative_to(ROOT))] = _sha256(reconciliation_path)
    application = {
        "version": VERSION,
        "project_id": selected,
        "status": "applied",
        "resulting_asset_store_sha256": _sha256(asset_path),
        "resulting_manifest_sha256": _sha256(manifest_path),
        "applied_input_hashes": applied_hashes,
    }
    _write_json(workspace / "validation/project_reconciliation_application.json", application)
    canonical_inputs = []
    for relative in CANONICAL_SOURCES:
        path = workspace / relative
        canonical_inputs.append(
            {"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)}
        )
    for relative in CANONICAL_RUNTIME_SOURCES:
        path = ROOT / relative
        canonical_inputs.append({"path": relative, "sha256": _sha256(path)})
    for start, end in volume1_windows(selected):
        path = window_root / f"window-{start:03d}-{end:03d}.v1.json"
        canonical_inputs.append({"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)})
    for path in sorted(intents_root.glob("chapter-*.json")):
        canonical_inputs.append({"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)})
    baseline_path = workspace / "creation_assets/canonical_baseline.json"
    _write_json(
        baseline_path,
        {
            "version": VERSION,
            "project_id": selected,
            "status": "locked_before_formal_prose",
            "canonical_inputs": canonical_inputs,
        },
    )
    return {
        "valid": True,
        "project_id": selected,
        "chapter_count": len(manifest["chapters"]),
        "window_count": len(volume1_windows(selected)),
        "manifest": str(manifest_path.relative_to(ROOT)),
        "baseline": str(baseline_path.relative_to(ROOT)),
        "prose_generated": False,
    }


def validate_project_production(project_id: str | None = None) -> dict[str, Any]:
    project = load_project(project_id)
    selected = str(project["project_id"])
    workspace = project_workspace(selected)
    errors: list[str] = []
    isolation = validate_project_isolation(selected)
    if not isolation.get("valid"):
        errors.extend(isolation.get("errors", []))
    semantic = validate_project_semantic_contracts(selected)
    if not semantic.get("valid"):
        errors.extend(f"literary semantic contract: {item}" for item in semantic.get("errors", []))
    required = {
        "manifest": workspace / "production_runtime/plans/volume1_production_manifest.v1.json",
        "initial_state": workspace / "production_runtime/state/canonical_initial_state.v1.json",
        "titles": workspace / "production_runtime/chapter_titles.volume1.json",
        "baseline": workspace / "creation_assets/canonical_baseline.json",
        "reconciliation": workspace / "validation/project_reconciliation.json",
        "application": workspace / "validation/project_reconciliation_application.json",
    }
    for label, path in required.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")
    if errors:
        return {"valid": False, "project_id": selected, "errors": errors, "checks": {}}
    manifest = _read_json(required["manifest"])
    chapters = manifest.get("chapters", [])
    chapter_count = volume1_chapter_count(selected)
    ids = [item.get("chapter_id") for item in chapters]
    expected_ids = [f"chapter-{number:04d}" for number in range(1, chapter_count + 1)]
    if ids != expected_ids:
        errors.append("production manifest must contain every volume chapter in order")
    established = {"v1.baseline"}
    payoffs: set[str] = set()
    for item in chapters:
        missing = set(item.get("requires_state_ids", [])) - established
        if missing:
            errors.append(f"{item.get('chapter_id')} requires unavailable state: {sorted(missing)}")
        payoff = str(item.get("payoff_id", ""))
        if not payoff or payoff in payoffs:
            errors.append(f"duplicate or missing payoff: {item.get('chapter_id')}")
        payoffs.add(payoff)
        for state_id in item.get("establishes_state_ids", []):
            if state_id in established:
                errors.append(f"duplicate established state: {state_id}")
            established.add(state_id)
    chapter_map = {str(item.get("chapter_id")): item for item in chapters}
    chapter33 = chapter_map.get("chapter-0033", {})
    if not any(
        delta.get("asset_id") == "faction_maintenance_team"
        and delta.get("field_path") == "lifecycle_state"
        and delta.get("before") == "seed"
        and delta.get("after") == "active"
        for delta in chapter33.get("expected_state_deltas", [])
    ):
        errors.append("chapter-0033 must establish maintenance team seed-to-active lifecycle")
    schema = _read_json(ROOT / "system/production_runtime/schemas/story_window.schema.json")
    windows = []
    for start, end in volume1_windows(selected):
        path = workspace / f"production_runtime/story_windows/window-{start:03d}-{end:03d}.v1.json"
        if not path.is_file():
            errors.append(f"missing story window {start:03d}-{end:03d}")
            continue
        payload = _read_json(path)
        try:
            jsonschema.validate(payload, schema)
        except jsonschema.ValidationError as error:
            errors.append(f"story window {start:03d}-{end:03d}: {error.message}")
        if payload.get("window") != {"start": start, "end": end, "name": f"正式生产窗口 {start:03d}-{end:03d}"}:
            errors.append(f"story window range mismatch: {start:03d}-{end:03d}")
        if [item.get("chapter_id") for item in payload.get("chapters", [])] != expected_ids[start - 1 : end]:
            errors.append(f"story window chapters mismatch: {start:03d}-{end:03d}")
        for beat in payload.get("chapters", []):
            contract = chapter_map.get(str(beat.get("chapter_id")), {})
            expected_delta_strings = [
                f"{delta['state_id']}:{delta['asset_id']}:{delta['field_path']}"
                for delta in contract.get("expected_state_deltas", [])
            ]
            if beat.get("working_title") != contract.get("title"):
                errors.append(f"story window title drift: {beat.get('chapter_id')}")
            if beat.get("required_asset_ids") != contract.get("required_asset_ids"):
                errors.append(f"story window asset drift: {beat.get('chapter_id')}")
            if beat.get("expected_state_deltas") != expected_delta_strings:
                errors.append(f"story window state delta drift: {beat.get('chapter_id')}")
            if not beat.get("evidence_refs") or not beat.get("cultural_safety_checks"):
                errors.append(f"story window evidence or cultural safety binding missing: {beat.get('chapter_id')}")
        windows.append(path)
    intent_schema = _read_json(ROOT / "system/production_runtime/schemas/chapter_intent.schema.json")
    for chapter_id in expected_ids:
        path = workspace / f"production_runtime/intents/{chapter_id}.json"
        if not path.is_file():
            errors.append(f"missing chapter intent: {chapter_id}")
            continue
        try:
            intent = _read_json(path)
            jsonschema.validate(intent, intent_schema)
        except jsonschema.ValidationError as error:
            errors.append(f"intent {chapter_id}: {error.message}")
            continue
        contract = chapter_map.get(chapter_id, {})
        if intent.get("dramatic_purpose") != contract.get("purpose"):
            errors.append(f"intent purpose drift: {chapter_id}")
        if intent.get("required_asset_ids") != contract.get("required_asset_ids"):
            errors.append(f"intent asset drift: {chapter_id}")
        if intent.get("expected_state_deltas") != contract.get("expected_state_deltas"):
            errors.append(f"intent state delta drift: {chapter_id}")
    titles = _read_json(required["titles"])
    if titles.get("chapters") != [
        {"chapter_id": item["chapter_id"], "title": item["title"]} for item in chapters
    ]:
        errors.append("chapter title registry drift")
    baseline = _read_json(required["baseline"])
    stale = []
    for item in baseline.get("canonical_inputs", []):
        path = ROOT / str(item.get("path", ""))
        if not path.is_file() or _sha256(path) != item.get("sha256"):
            stale.append(str(item.get("path")))
    if stale:
        errors.append("canonical baseline drift: " + ", ".join(stale))
    expected_canonical_paths = {
        str((workspace / relative).relative_to(ROOT)) for relative in CANONICAL_SOURCES
    }
    expected_canonical_paths.update(CANONICAL_RUNTIME_SOURCES)
    expected_canonical_paths.update(str(path.relative_to(ROOT)) for path in windows)
    expected_canonical_paths.update(
        str((workspace / f"production_runtime/intents/{chapter_id}.json").relative_to(ROOT))
        for chapter_id in expected_ids
    )
    listed_canonical_paths = {
        str(item.get("path")) for item in baseline.get("canonical_inputs", [])
    }
    if listed_canonical_paths != expected_canonical_paths:
        errors.append("canonical baseline input set is incomplete or contains unexpected paths")
    application = _read_json(required["application"])
    asset_path = workspace / "creation_assets/project_assets.json"
    if application.get("resulting_asset_store_sha256") != _sha256(asset_path):
        errors.append("reconciliation application is stale")
    for relative, expected_sha in application.get("applied_input_hashes", {}).items():
        path = ROOT / relative
        if not path.is_file() or _sha256(path) != expected_sha:
            errors.append(f"reconciliation application input drift: {relative}")
    quality_contract = _read_json(workspace / "production_runtime/quality/first_window_quality_contract.v1.json")
    if quality_contract.get("hard_gates", {}).get("blocking_or_major_final_issue_count") != 0:
        errors.append("formal quality contract must reject every final blocking or major issue")
    review_policy = quality_contract.get("window_review", {})
    if review_policy.get("independent_review_required") is not True:
        errors.append("first formal window must require independent external review")
    independent_policy = review_policy.get("independent_review_policy", {})
    if (
        independent_policy.get("preferred_provider") != "antigravity"
        or independent_policy.get("allowed_degradation_providers") != ["opencode-go"]
        or independent_policy.get("owner_authorization_required") is not True
        or independent_policy.get("execution_evidence_required") is not True
    ):
        errors.append("formal quality contract has an invalid independent review policy")
    checks = {
        "project_isolated": isolation.get("valid") is True,
        "literary_semantic_integrity": semantic.get("valid") is True,
        "volume_contract_complete": ids == expected_ids,
        "causal_state_graph_valid": not any("state:" in item for item in errors),
        "unique_payoffs": len(payoffs) == chapter_count,
        "story_windows_complete": len(windows) == len(volume1_windows(selected)),
        "canonical_baseline_current": not stale,
        "canonical_input_set_complete": listed_canonical_paths == expected_canonical_paths,
        "formal_samples_excluded": manifest.get("canonicalization", {}).get("sample_import_allowed") is False,
        "quality_gate_contract_ready": not any("quality contract" in item for item in errors),
    }
    return {
        "version": VERSION,
        "project_id": selected,
        "valid": not errors and all(checks.values()),
        "checks": checks,
        "errors": errors,
        "chapter_count": chapter_count,
        "window_count": len(windows),
        "canonical_inputs": baseline.get("canonical_inputs", []),
    }


def relock_project_baseline(project_id: str | None = None) -> dict[str, Any]:
    """Relock a prose-empty project after validated non-prose canonical changes."""
    project = load_project(project_id)
    selected = str(project["project_id"])
    workspace = project_workspace(selected)
    if project.get("content_authorized") is not False or project.get("status") != "owner_gate":
        raise RuntimeError("project must be at owner_gate with content authorization disabled")
    registry_path = workspace / "production_runtime/chapter_registry.v0.20.json"
    if not registry_path.is_file() or _read_json(registry_path).get("chapters"):
        raise RuntimeError("semantic baseline can only be relocked before formal prose exists")
    semantic = validate_project_semantic_contracts(selected)
    if not semantic.get("valid"):
        raise RuntimeError(
            "project semantic contracts are invalid: " + "; ".join(semantic.get("errors", []))
        )
    for relative in CANONICAL_SOURCES:
        if not (workspace / relative).is_file():
            raise RuntimeError(f"canonical source is missing: {relative}")
    application_path = workspace / "validation/project_reconciliation_application.json"
    application = _read_json(application_path)
    application["version"] = VERSION
    application["status"] = "applied_after_semantic_reconciliation"
    application["resulting_asset_store_sha256"] = _sha256(
        workspace / "creation_assets/project_assets.json"
    )
    application["resulting_manifest_sha256"] = _sha256(
        workspace / "production_runtime/plans/volume1_production_manifest.v1.json"
    )
    application["applied_input_hashes"] = {
        str((workspace / relative).relative_to(ROOT)): _sha256(workspace / relative)
        for relative in CANONICAL_SOURCES
        if relative != "validation/project_reconciliation_application.json"
    }
    _write_json(application_path, application)
    canonical_inputs = [
        {
            "path": str((workspace / relative).relative_to(ROOT)),
            "sha256": _sha256(workspace / relative),
        }
        for relative in CANONICAL_SOURCES
    ]
    canonical_inputs.extend(
        {"path": relative, "sha256": _sha256(ROOT / relative)}
        for relative in CANONICAL_RUNTIME_SOURCES
    )
    for start, end in volume1_windows(selected):
        path = workspace / f"production_runtime/story_windows/window-{start:03d}-{end:03d}.v1.json"
        canonical_inputs.append({"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)})
    for path in sorted((workspace / "production_runtime/intents").glob("chapter-*.json")):
        canonical_inputs.append({"path": str(path.relative_to(ROOT)), "sha256": _sha256(path)})
    baseline_path = workspace / "creation_assets/canonical_baseline.json"
    _write_json(
        baseline_path,
        {
            "version": VERSION,
            "project_id": selected,
            "status": "locked_after_literary_semantic_remediation",
            "canonical_inputs": canonical_inputs,
        },
    )
    review_index_path = (
        workspace / "production_runtime/production_readiness/final-review-index.v0.1.json"
    )
    if review_index_path.is_file():
        review_index = _read_json(review_index_path)
        review_index["valid"] = False
        review_index["superseded_reason"] = (
            "Canonical baseline changed after literary semantic remediation v0.29."
        )
        review_index["superseded_baseline_sha256"] = _sha256(baseline_path)
        _write_json(review_index_path, review_index)
    return {
        "version": VERSION,
        "project_id": selected,
        "valid": True,
        "baseline": str(baseline_path.relative_to(ROOT)),
        "baseline_sha256": _sha256(baseline_path),
        "canonical_input_count": len(canonical_inputs),
        "formal_chapter_count": 0,
        "production_authorized": False,
    }
