from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nrl_creation_assets import load_creation_asset_registry
from nrl_creation_schemas import (
    build_creation_schema_registry,
    validate_creation_asset_store,
)
from nrl_full_corpus_proof import build_proof_status
from nrl_paths import ROOT, runtime_path
from nrl_research_assets import build_research_asset_catalog
from nrl_system_status import build_system_status


VERSION = "0.3"
EVIDENCE_PACK_VERSION = "0.10"
EVIDENCE_PACK_MATRIX_VERSION = "0.11"
EVIDENCE_PACK_DIR = runtime_path("system/research_assets/evidence_packs")
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


def _relative_to_root(path: Any) -> str:
    resolved = path if hasattr(path, "relative_to") else runtime_path(str(path))
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


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
            "antigravity": adapters_policy["antigravity_execution"]["effective_state"],
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


def _pack_path(family: str) -> Path:
    return EVIDENCE_PACK_DIR / f"{family}.v{EVIDENCE_PACK_VERSION}.json"


def build_evidence_pack(
    state: dict[str, Any],
    adapters: dict[str, Any],
    *,
    family: str | None = None,
    next_only: bool = False,
) -> dict[str, Any]:
    plan = build_pipeline_plan(
        state,
        adapters,
        family=family,
        next_only=next_only,
    )
    target_family = str(plan["target_family"]["family"])
    proof_status = build_proof_status()
    proof_readiness = proof_status["promotion_readiness"]
    evidence = list(plan["research_evidence"])
    blocked_actions = sorted(
        {
            *[str(item) for item in plan["forbidden_actions"]],
            *[str(item) for item in plan["target_family"]["blocked_actions"]],
            "execute_hermes",
            "execute_antigravity",
            "read_raw_novel_training_set",
            "generate_final_creation_assets",
            "generate_novel_prose",
        }
    )
    source_paths = sorted({str(item["source_path"]) for item in evidence})
    output_path = _pack_path(target_family)
    return {
        "version": EVIDENCE_PACK_VERSION,
        "evidence_pack_id": f"evidence-pack-{target_family}-v{EVIDENCE_PACK_VERSION}",
        "pipeline_id": plan["pipeline_id"],
        "project": plan["project"],
        "mode": plan["mode"],
        "content_progression": plan["content_progression"],
        "family": target_family,
        "label": plan["target_family"]["label"],
        "status": "ready_for_contract_planning"
        if plan["evidence_requirements"]["evidence_status"] == "ready"
        else "blocked_on_research_evidence",
        "output_path": _relative_to_root(output_path),
        "schema_contract": plan["schema_contract"],
        "research_query": plan["research_query"],
        "evidence_requirements": plan["evidence_requirements"],
        "evidence_summary": {
            "item_count": len(evidence),
            "source_paths": source_paths,
            "structured_only": True,
            "raw_corpus_allowed": False,
        },
        "research_evidence": evidence,
        "validation_gates": plan["validation_gates"],
        "promotion_dependencies": {
            "full_corpus_proof": {
                "job_id": proof_status["job_id"],
                "status": proof_readiness["status"],
                "proof_verified": proof_readiness["proof_verified"],
                "verified_receipts": proof_readiness["verified_receipts"],
                "required_receipts": proof_readiness["required_receipts"],
                "promotion_allowed": proof_readiness["promotion_allowed"],
                "next_required_action": proof_readiness["next_required_action"],
            }
        },
        "agent_review_policy": plan["agent_review_policy"],
        "owner_gate": plan["owner_gate"],
        "blocked_actions": blocked_actions,
        "content_generation_allowed": False,
        "external_agent_execution_allowed": False,
    }


def write_evidence_pack(pack: dict[str, Any]) -> dict[str, Any]:
    output_path = runtime_path(str(pack["output_path"]))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(pack, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return pack


def load_evidence_pack(file_arg: str) -> dict[str, Any]:
    path = Path(file_arg)
    if not path.is_absolute():
        path = ROOT / path
    return json.loads(path.read_text(encoding="utf-8"))


def _check_result(gate_id: str, passed: bool, detail: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def validate_evidence_pack(pack: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    schema_contract = pack.get("schema_contract", {})
    schema_path = runtime_path(str(schema_contract.get("path", "")))
    schema_valid = False
    schema_error = None
    if schema_path.exists():
        try:
            import jsonschema  # type: ignore

            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.Draft7Validator.check_schema(schema)
            schema_valid = bool(schema_contract.get("valid", False))
        except Exception as error:  # pragma: no cover - defensive detail path
            schema_error = str(error)
    checks.append(
        _check_result(
            "schema_validation",
            schema_valid,
            {
                "schema_path": str(schema_contract.get("path", "")),
                "schema_valid": schema_valid,
                "error": schema_error,
            },
        )
    )

    evidence = pack.get("research_evidence", [])
    requirements = pack.get("evidence_requirements", {})
    minimum_items = int(requirements.get("minimum_items", 0))
    missing_paths = []
    raw_paths = []
    source_paths = []
    if isinstance(evidence, list):
        for item in evidence:
            if not isinstance(item, dict):
                continue
            source_path = str(item.get("source_path", ""))
            source_paths.append(source_path)
            if "novel_training_set/" in source_path:
                raw_paths.append(source_path)
            if source_path and not runtime_path(source_path).exists():
                missing_paths.append(source_path)
    enough_evidence = isinstance(evidence, list) and len(evidence) >= minimum_items
    checks.append(
        _check_result(
            "source_evidence",
            enough_evidence and not missing_paths,
            {
                "item_count": len(evidence) if isinstance(evidence, list) else 0,
                "minimum_items": minimum_items,
                "missing_path_count": len(missing_paths),
            },
        )
    )

    summary_paths = pack.get("evidence_summary", {}).get("source_paths", [])
    if isinstance(summary_paths, list):
        raw_paths.extend(path for path in summary_paths if "novel_training_set/" in str(path))
    raw_boundary_passed = (
        not raw_paths
        and requirements.get("raw_corpus_allowed") is False
        and pack.get("evidence_summary", {}).get("raw_corpus_allowed") is False
    )
    checks.append(
        _check_result(
            "raw_corpus_boundary",
            raw_boundary_passed,
            {
                "raw_corpus_allowed": requirements.get("raw_corpus_allowed"),
                "raw_path_count": len(raw_paths),
            },
        )
    )

    asset_store_validation = validate_creation_asset_store()
    checks.append(
        _check_result(
            "creation_asset_store",
            bool(asset_store_validation["valid"]),
            {
                "asset_count": asset_store_validation["summary"]["asset_count"],
                "error_count": len(asset_store_validation["errors"]),
                "store_path": asset_store_validation["store_path"],
            },
        )
    )

    owner_gate = pack.get("owner_gate", {})
    proof = pack.get("promotion_dependencies", {}).get("full_corpus_proof", {})
    owner_gate_passed = (
        owner_gate.get("required") is True
        and str(owner_gate.get("status", ""))
        and pack.get("content_generation_allowed") is False
        and proof.get("promotion_allowed") is False
    )
    checks.append(
        _check_result(
            "owner_gate",
            owner_gate_passed,
            {
                "owner_gate_required": owner_gate.get("required"),
                "owner_gate_status": owner_gate.get("status"),
                "full_corpus_promotion_allowed": proof.get("promotion_allowed"),
            },
        )
    )

    blocked_actions = set(str(item) for item in pack.get("blocked_actions", []))
    required_blocked = {
        "execute_hermes",
        "execute_antigravity",
        "generate_novel_prose",
        "read_raw_novel_training_set",
    }
    execution_boundary_passed = (
        pack.get("content_generation_allowed") is False
        and pack.get("external_agent_execution_allowed") is False
        and required_blocked <= blocked_actions
    )
    checks.append(
        _check_result(
            "agent_execution_boundary",
            execution_boundary_passed,
            {
                "content_generation_allowed": pack.get("content_generation_allowed"),
                "external_agent_execution_allowed": pack.get("external_agent_execution_allowed"),
                "missing_blocked_actions": sorted(required_blocked - blocked_actions),
            },
        )
    )

    errors = [
        {
            "gate_id": check["gate_id"],
            "detail": check["detail"],
        }
        for check in checks
        if not check["passed"]
    ]
    return {
        "version": EVIDENCE_PACK_VERSION,
        "evidence_pack_id": pack.get("evidence_pack_id", "unknown"),
        "family": pack.get("family", "unknown"),
        "valid": not errors,
        "checks": checks,
        "errors": errors,
    }


def build_evidence_pack_matrix(
    state: dict[str, Any],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    family_items: dict[str, dict[str, Any]] = {}
    for family in FAMILY_PRIORITY:
        pack = build_evidence_pack(state, adapters, family=family)
        validation = validate_evidence_pack(pack)
        family_items[family] = {
            "family": family,
            "label": pack["label"],
            "status": pack["status"],
            "output_path": pack["output_path"],
            "schema_path": pack["schema_contract"]["path"],
            "evidence_item_count": pack["evidence_summary"]["item_count"],
            "validation_status": "valid" if validation["valid"] else "invalid",
            "validation_error_count": len(validation["errors"]),
            "content_generation_allowed": pack["content_generation_allowed"],
            "external_agent_execution_allowed": pack[
                "external_agent_execution_allowed"
            ],
            "full_corpus_proof_status": pack["promotion_dependencies"][
                "full_corpus_proof"
            ]["status"],
        }
    invalid_families = sorted(
        family
        for family, item in family_items.items()
        if item["validation_status"] != "valid"
    )
    return {
        "version": EVIDENCE_PACK_MATRIX_VERSION,
        "matrix_id": f"evidence-pack-matrix-v{EVIDENCE_PACK_MATRIX_VERSION}",
        "pipeline_id": "corpus-to-creation",
        "project": state.get("selected_project", "UNKNOWN_PROJECT"),
        "mode": build_system_status(state, adapters)["operating_mode"],
        "content_progression": build_system_status(state, adapters)[
            "content_progression"
        ],
        "output_path": (
            f"system/research_assets/evidence_packs/manifest.v{EVIDENCE_PACK_MATRIX_VERSION}.json"
        ),
        "family_count": len(family_items),
        "valid_family_count": len(family_items) - len(invalid_families),
        "invalid_families": invalid_families,
        "families": family_items,
        "content_generation_allowed": False,
        "external_agent_execution_allowed": False,
        "owner_gate_required": True,
    }


def write_evidence_pack_matrix(matrix: dict[str, Any], state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    for family in FAMILY_PRIORITY:
        write_evidence_pack(build_evidence_pack(state, adapters, family=family))
    output_path = runtime_path(str(matrix["output_path"]))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return matrix


def validate_all_evidence_packs(
    state: dict[str, Any],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    families: dict[str, dict[str, Any]] = {}
    for family in FAMILY_PRIORITY:
        pack = build_evidence_pack(state, adapters, family=family)
        validation = validate_evidence_pack(pack)
        families[family] = {
            "family": family,
            "valid": validation["valid"],
            "check_count": len(validation["checks"]),
            "error_count": len(validation["errors"]),
            "checks": validation["checks"],
        }
    invalid_families = sorted(
        family for family, validation in families.items() if not validation["valid"]
    )
    return {
        "version": EVIDENCE_PACK_MATRIX_VERSION,
        "mode": "all",
        "valid": not invalid_families,
        "family_count": len(families),
        "valid_family_count": len(families) - len(invalid_families),
        "invalid_families": invalid_families,
        "families": families,
    }
