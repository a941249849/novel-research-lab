from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_paths import runtime_path

REGISTRY_PATH = runtime_path("system/creation_assets/creation_asset_registry.v0.1.json")
ALLOWED_STATUSES = {"missing", "seed", "partial"}
EXPECTED_ASSET_IDS = {
    "characters",
    "npcs",
    "factions",
    "artifacts",
    "techniques",
    "naming",
    "emotional_bonds",
    "foreshadowing",
    "state_ledger",
}


def _load_registry_artifact(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate_family(family: dict[str, Any]) -> None:
    asset_id = family.get("asset_id")
    status = family.get("status")
    if asset_id not in EXPECTED_ASSET_IDS:
        raise RuntimeError(f"unexpected creation asset family: {asset_id}")
    if status not in ALLOWED_STATUSES:
        raise RuntimeError(f"invalid creation asset status for {asset_id}: {status}")
    score = family.get("readiness_score")
    if not isinstance(score, int) or score < 0 or score > 100:
        raise RuntimeError(f"invalid readiness_score for {asset_id}: {score}")


def _coverage_summary(families: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(family["status"]) for family in families)
    return {
        "total": len(families),
        "by_status": dict(sorted(counts.items())),
        "complete": 0,
        "lowest_readiness": min(int(family["readiness_score"]) for family in families),
        "highest_readiness": max(int(family["readiness_score"]) for family in families),
    }


def load_creation_asset_registry(project: str, mode: str) -> dict[str, Any]:
    artifact = _load_registry_artifact()
    families = artifact.get("asset_families", [])
    if not isinstance(families, list):
        raise RuntimeError("creation asset registry asset_families must be a list")
    for family in families:
        _validate_family(family)
    family_ids = {str(family["asset_id"]) for family in families}
    if family_ids != EXPECTED_ASSET_IDS:
        missing = sorted(EXPECTED_ASSET_IDS - family_ids)
        extra = sorted(family_ids - EXPECTED_ASSET_IDS)
        raise RuntimeError(f"creation asset registry family mismatch: missing={missing}, extra={extra}")
    return {
        "registry_name": "Creation Asset Registry",
        "version": str(artifact.get("version", "0.1")),
        "project": project,
        "mode": mode,
        "source_of_truth": [
            "system/creation_assets/creation_asset_registry.v0.1.json",
            "system/mission_controller/current_phase_state.json",
            "system/runtime/mission_registry.json",
        ],
        "asset_families": families,
        "coverage_summary": _coverage_summary(families),
        "guardrails": [
            "No family is complete in v0.1",
            "Do not generate novel prose",
            "Do not generate full character cards",
            "Do not generate final NPC sheets, faction dossiers, technique trees, naming dictionaries, or item catalogs",
            "Do not read raw novel_training_set/",
            "Do not call Hermes or dispatch Antigravity outside registered CLI review jobs",
        ],
        "next_safe_action": "Use the registry to design schemas and validation before any content progression.",
    }
