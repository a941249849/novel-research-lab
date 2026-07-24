from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from nrl_paths import runtime_path
from nrl_system_status import build_system_status


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
ROADMAP_PATH = runtime_path("system/control_plane/capability_roadmap.v0.2.json")
PACKAGE_ROADMAP_PATH = (
    PACKAGE_ROOT / "system/control_plane/capability_roadmap.v0.2.json"
)
ALLOWED_STATES = {"missing", "contract_ready", "data_ready", "runnable", "blocked"}
ACTIONABLE_STATES = {"missing", "contract_ready"}
DEPENDENCY_READY_STATES = {"contract_ready", "data_ready", "runnable"}


def _load_roadmap(path: Path = ROADMAP_PATH) -> dict[str, Any]:
    if not path.exists():
        path = PACKAGE_ROADMAP_PATH
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_hardening_status(
    state: dict[str, Any],
    adapters: dict[str, Any],
    *,
    roadmap: dict[str, Any] | None = None,
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    live_runtime = roadmap is None and evidence_root is None
    roadmap = deepcopy(roadmap) if roadmap is not None else _load_roadmap()
    deep_read = None
    literary_semantics = None
    if live_runtime:
        from nrl_deep_read import build_deep_read_status
        from nrl_literary_semantics import validate_literary_semantic_assets

        deep_read = build_deep_read_status()
        literary_semantics = validate_literary_semantic_assets()
    capabilities = roadmap.get("capabilities", [])
    seen: set[str] = set()
    dependency_ready: set[str] = set()
    next_id: str | None = None

    for capability in capabilities:
        capability_id = str(capability["capability_id"])
        declared_status = str(capability["status"])
        if declared_status not in ALLOWED_STATES:
            raise RuntimeError(
                f"invalid capability status: {capability_id}={declared_status}"
            )
        unordered_dependencies = [
            dependency
            for dependency in capability.get("dependencies", [])
            if dependency not in seen
        ]
        if unordered_dependencies:
            raise RuntimeError(
                f"capability dependency order invalid for {capability_id}: {unordered_dependencies}"
            )
        blocked_dependencies = [
            dependency
            for dependency in capability.get("dependencies", [])
            if dependency not in dependency_ready
        ]
        evidence = []
        for relative_path in capability.get("evidence", []):
            evidence_path = (
                (evidence_root / relative_path)
                if evidence_root is not None
                else runtime_path(relative_path)
            )
            evidence.append(
                {
                    "path": relative_path,
                    "exists": evidence_path.exists(),
                }
            )
        capability["evidence"] = evidence
        capability["evidence_complete"] = all(item["exists"] for item in evidence)
        if blocked_dependencies:
            status = "blocked"
        elif declared_status != "blocked" and evidence and not capability["evidence_complete"]:
            status = "missing"
        else:
            status = declared_status
        if live_runtime and deep_read is not None:
            if capability_id == "single_book_decomposition" and not (
                (deep_read.get("synthesis_validation") or {}).get("valid")
            ):
                status = "missing"
            elif capability_id == "cross_book_mechanism_distillation" and not deep_read.get(
                "deep_read_verified"
            ):
                status = "missing" if not blocked_dependencies else "blocked"
            elif (
                capability_id == "cross_book_mechanism_distillation"
                and not literary_semantics.get("valid")
            ):
                status = "missing" if not blocked_dependencies else "blocked"
        capability["declared_status"] = declared_status
        capability["status"] = status
        capability["blocked_dependencies"] = blocked_dependencies
        capability["is_next_safe_action"] = False
        if next_id is None and status in ACTIONABLE_STATES:
            next_id = capability_id
        seen.add(capability_id)
        if status in DEPENDENCY_READY_STATES:
            dependency_ready.add(capability_id)

    if next_id is None:
        next_id = "prose_production"
    if live_runtime:
        from nrl_production_operator import build_operator_status, describe_next_production_action

        operator = build_operator_status(
            runtime_path("system/production_runtime/chapter_registry.v0.20.json")
        )
        action = describe_next_production_action(operator)
        for capability in capabilities:
            if capability["capability_id"] == "prose_production":
                capability["next_action"] = action["label_zh"]
    for capability in capabilities:
        capability["is_next_safe_action"] = capability["capability_id"] == next_id

    next_capability = next(
        capability for capability in capabilities if capability["is_next_safe_action"]
    )
    system_status = build_system_status(state, adapters)
    return {
        "version": str(roadmap.get("version", "0.2")),
        "mode": system_status["operating_mode"],
        "content_progression": system_status["content_progression"],
        "capabilities": capabilities,
        "next_safe_action": {
            "capability_id": next_capability["capability_id"],
            "label_zh": next_capability["label_zh"],
            "action": next_capability["next_action"],
        },
    }
