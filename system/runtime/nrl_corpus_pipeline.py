from __future__ import annotations

from typing import Any

from nrl_creation_assets import load_creation_asset_registry
from nrl_creation_schemas import build_creation_schema_registry
from nrl_research_assets import build_research_asset_catalog
from nrl_system_status import build_system_status


VERSION = "0.3"
FAMILY_PRIORITY = (
    "characters",
    "npcs",
    "factions",
    "artifacts",
    "techniques",
    "naming",
    "emotional_bonds",
    "foreshadowing",
    "state_ledger",
)
FAMILY_RESEARCH_NEEDS: dict[str, dict[str, list[str]]] = {
    "characters": {
        "asset_types": ["book_dna", "narrative_dna", "state_ledger"],
        "categories": ["宿命/情绪/哲学机制", "压迫与释放机制"],
    },
    "npcs": {
        "asset_types": ["narrative_dna", "state_ledger"],
        "categories": ["压迫与释放机制", "隐藏实力与信息差机制"],
    },
    "factions": {
        "asset_types": ["book_dna", "narrative_dna"],
        "categories": ["组织/阵营/声望机制"],
    },
    "artifacts": {
        "asset_types": ["state_ledger"],
        "categories": ["资源与资产机制", "反噬/代价/污染机制"],
    },
    "techniques": {
        "asset_types": ["state_ledger"],
        "categories": ["升级与境界机制", "反噬/代价/污染机制"],
    },
    "naming": {
        "asset_types": ["book_dna", "narrative_dna"],
        "categories": ["升级与境界机制", "宿命/情绪/哲学机制"],
    },
    "emotional_bonds": {
        "asset_types": ["narrative_dna", "state_ledger"],
        "categories": ["宿命/情绪/哲学机制"],
    },
    "foreshadowing": {
        "asset_types": ["narrative_dna", "state_ledger"],
        "categories": ["探索/谜团/知识机制", "隐藏实力与信息差机制"],
    },
    "state_ledger": {
        "asset_types": ["state_ledger", "book_dna", "narrative_dna"],
        "categories": ["反噬/代价/污染机制", "资源与资产机制"],
    },
}
VALIDATION_GATES = (
    ("schema_validation", "Draft-07 family schema must validate the asset envelope and payload."),
    ("source_evidence", "Plan must retain structured research evidence and source paths."),
    ("reference_integrity", "Cross-asset references must resolve before any asset can be promoted."),
    ("naming_collision", "Normalized names must not collide across the project asset store."),
    ("lifecycle_transition", "Lifecycle transitions must follow the creation asset contract."),
    ("owner_gate", "Owner Gate must remain active before prose or final asset generation."),
)


def _families(state: dict[str, Any], adapters: dict[str, Any]) -> list[dict[str, Any]]:
    system_status = build_system_status(state, adapters)
    registry = load_creation_asset_registry(
        str(state.get("selected_project", "UNKNOWN_PROJECT")),
        str(system_status["operating_mode"]),
    )
    order = {family: index for index, family in enumerate(FAMILY_PRIORITY)}
    families = []
    for family in registry["asset_families"]:
        family_id = str(family["asset_id"])
        families.append(
            {
                "family": family_id,
                "label": str(family["label"]),
                "status": str(family["status"]),
                "readiness_score": int(family["readiness_score"]),
                "gap": str(family["why_not_complete"]),
                "next_safe_action": str(family["next_safe_action"]),
                "blocked_actions": list(family["blocked_actions"]),
                "priority": order[family_id],
                "is_next": False,
            }
        )
    return sorted(families, key=lambda item: (item["readiness_score"], item["priority"]))


def _stages(system_status: dict[str, Any]) -> list[dict[str, Any]]:
    owner_gate_active = bool(system_status["owner_gate_required"])
    return [
        {
            "stage_id": "research_asset_retrieval",
            "label_zh": "研究资产检索",
            "status": "runnable",
            "description": "从结构化 Phase 1 资产中筛选证据，不读取原文语料。",
        },
        {
            "stage_id": "evidence_pack_assembly",
            "label_zh": "证据包装配",
            "status": "runnable",
            "description": "按目标资产家族组合来源、机制分类和审核状态。",
        },
        {
            "stage_id": "creation_asset_contract_planning",
            "label_zh": "创作资产契约计划",
            "status": "runnable",
            "description": "输出 schema-bound plan，而不是最终创作资产。",
        },
        {
            "stage_id": "consistency_validation",
            "label_zh": "一致性校验",
            "status": "runnable",
            "description": "检查 schema、引用、命名、生命周期和来源证据。",
        },
        {
            "stage_id": "agent_review_policy",
            "label_zh": "Agent 审查策略",
            "status": "contract_ready",
            "description": "Codex 本地验证；Antigravity/Hermes 保持人工或暂停边界。",
        },
        {
            "stage_id": "owner_gate",
            "label_zh": "Owner Gate",
            "status": "blocked" if owner_gate_active else "contract_ready",
            "description": "Owner Gate 未解除前禁止内容推进。",
        },
        {
            "stage_id": "prose_generation",
            "label_zh": "正文生产",
            "status": "blocked",
            "description": "v0.3 不生成正文、章节或最终创作资产。",
        },
    ]


def _schema_for_family(family: str) -> dict[str, Any]:
    schemas = build_creation_schema_registry()
    by_family = {item["family"]: item for item in schemas["families"]}
    if family not in by_family:
        raise RuntimeError(f"unsupported creation asset family: {family}")
    schema = by_family[family]
    return {
        "family": family,
        "draft": schemas["draft"],
        "path": schema["path"],
        "payload_key": schema["payload_key"],
        "valid": schema["valid"],
    }


def _validation_gates() -> list[dict[str, str]]:
    return [{"gate_id": gate_id, "description": description} for gate_id, description in VALIDATION_GATES]


def _evidence_for_family(family: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    needs = FAMILY_RESEARCH_NEEDS[family]
    catalog = build_research_asset_catalog()
    evidence = [
        item
        for item in catalog["items"]
        if item["asset_type"] in needs["asset_types"]
        or any(category in item["categories"] for category in needs["categories"])
    ]
    evidence = sorted(evidence, key=lambda item: item["asset_id"])[:18]
    return (
        {
            "asset_types": needs["asset_types"],
            "categories": needs["categories"],
            "review_state": "formal_or_reviewed",
        },
        evidence,
    )


def build_pipeline_status(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    families = _families(state, adapters)
    if not families:
        raise RuntimeError("creation asset families are empty")
    families[0]["is_next"] = True
    forbidden = sorted(
        {
            *[str(item) for item in state.get("blocked_actions", [])],
            "generate final creative assets",
            "execute-hermes",
            "execute-antigravity",
        }
    )
    return {
        "version": VERSION,
        "pipeline_id": "corpus-to-creation",
        "mode": system_status["operating_mode"],
        "content_progression": system_status["content_progression"],
        "project": state.get("selected_project", "UNKNOWN_PROJECT"),
        "stages": _stages(system_status),
        "families": families,
        "next_family": families[0],
        "forbidden_actions": forbidden,
    }


def build_pipeline_plan(
    state: dict[str, Any],
    adapters: dict[str, Any],
    *,
    family: str | None = None,
    next_only: bool = False,
) -> dict[str, Any]:
    status = build_pipeline_status(state, adapters)
    target_family = status["next_family"]["family"] if next_only or family is None else family
    families_by_id = {item["family"]: item for item in status["families"]}
    if target_family not in families_by_id:
        raise RuntimeError(f"unsupported creation asset family: {target_family}")
    research_query, evidence = _evidence_for_family(target_family)
    adapters_policy = build_system_status(state, adapters)
    return {
        "version": VERSION,
        "pipeline_id": f"corpus-to-creation-{target_family}",
        "project": status["project"],
        "mode": status["mode"],
        "content_progression": status["content_progression"],
        "target_family": families_by_id[target_family],
        "stage_statuses": status["stages"],
        "research_query": research_query,
        "evidence_requirements": {
            "minimum_items": 3,
            "structured_only": True,
            "raw_corpus_allowed": False,
            "evidence_status": "ready" if evidence else "insufficient",
        },
        "research_evidence": evidence,
        "schema_contract": _schema_for_family(target_family),
        "validation_gates": _validation_gates(),
        "agent_review_policy": {
            "codex": "local_validation_orchestration",
            "antigravity": adapters_policy["adapter_modes"]["antigravity"]["mode"],
            "hermes": adapters_policy["hermes_execution_status"],
            "web_gpt": "architecture_review_only",
        },
        "owner_gate": {
            "required": adapters_policy["owner_gate_required"],
            "status": adapters_policy["owner_gate_status"],
        },
        "forbidden_actions": status["forbidden_actions"],
        "content_generation_allowed": False,
    }
