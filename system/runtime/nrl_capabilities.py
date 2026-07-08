from __future__ import annotations

import json
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


def _load_roadmap(path: Path = ROADMAP_PATH) -> dict[str, Any]:
    if not path.exists():
        path = PACKAGE_ROADMAP_PATH
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_hardening_status(
    state: dict[str, Any],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    roadmap = _load_roadmap()
    capabilities = roadmap.get("capabilities", [])
    seen: set[str] = set()
    next_id: str | None = None

    for capability in capabilities:
        capability_id = str(capability["capability_id"])
        status = str(capability["status"])
        if status not in ALLOWED_STATES:
            raise RuntimeError(f"invalid capability status: {capability_id}={status}")
        missing_dependencies = [
            dependency
            for dependency in capability.get("dependencies", [])
            if dependency not in seen
        ]
        if missing_dependencies:
            raise RuntimeError(
                f"capability dependency order invalid for {capability_id}: {missing_dependencies}"
            )
        evidence = []
        for relative_path in capability.get("evidence", []):
            evidence.append(
                {
                    "path": relative_path,
                    "exists": runtime_path(relative_path).exists(),
                }
            )
        capability["evidence"] = evidence
        capability["evidence_complete"] = all(item["exists"] for item in evidence)
        capability["is_next_safe_action"] = False
        if next_id is None and status in ACTIONABLE_STATES:
            next_id = capability_id
        seen.add(capability_id)

    if next_id is None:
        next_id = "prose_production"
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
