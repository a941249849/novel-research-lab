from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_agent_ops import load_job_queue
from nrl_creation_schemas import validate_creation_asset_store
from nrl_paths import ROOT, runtime_path
from nrl_rag_index import load_or_build_rag_index
from nrl_system_status import build_system_status


VERSION = "0.6"
TECHNIQUES_JOB_ID = "job-v05-techniques-antigravity-review"
TECHNIQUES_OUTBOX_PATH = "system/agent_ops/outbox/job-v05-techniques-antigravity-review_validated.md"
PROJECT_ASSET_STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
SUPPORTED_FAMILIES = ("techniques",)
OWNED_TECHNIQUE_IDS = (
    "technique_costed_advancement",
    "technique_backlash_guard",
    "technique_state_reversal",
)
FORBIDDEN_TEXT = ("novel_training_set/", "正文", "第一章", "Chapter 1")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _project_store() -> dict[str, Any]:
    if not PROJECT_ASSET_STORE_PATH.exists():
        return {"version": "0.2", "project": "UNKNOWN_PROJECT", "assets": []}
    return _read_json(PROJECT_ASSET_STORE_PATH)


def _technique_assets(store: dict[str, Any]) -> list[dict[str, Any]]:
    return [asset for asset in store.get("assets", []) if asset.get("family") == "techniques"]


def _job_by_id(job_id: str) -> dict[str, Any] | None:
    for job in load_job_queue().get("jobs", []):
        if job.get("job_id") == job_id:
            return job
    return None


def _positive_evidence_count(state: dict[str, Any]) -> int:
    index = load_or_build_rag_index(state)
    return len([item for item in index.get("items", []) if int(item.get("evidence_weight", 0)) > 0])


def _store_validation(store: dict[str, Any]) -> dict[str, Any]:
    return validate_creation_asset_store(store)


def build_producer_status(
    state: dict[str, Any],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    store = _project_store()
    job = _job_by_id(TECHNIQUES_JOB_ID) or {}
    outbox_exists = (ROOT / TECHNIQUES_OUTBOX_PATH).exists()
    technique_assets = _technique_assets(store)
    family_counts = Counter(asset.get("family", "unknown") for asset in store.get("assets", []))
    return {
        "version": VERSION,
        "system_mode": system_status["operating_mode"],
        "content_progression": system_status["content_progression"],
        "supported_families": list(SUPPORTED_FAMILIES),
        "hermes_allowed": False,
        "owner_gate": {
            "required": system_status["owner_gate_required"],
            "status": system_status["owner_gate_status"],
        },
        "techniques": {
            "job_id": TECHNIQUES_JOB_ID,
            "job_state": job.get("state", "missing"),
            "job_validated": job.get("state") == "validated",
            "validated_outbox_path": TECHNIQUES_OUTBOX_PATH,
            "validated_outbox_exists": outbox_exists,
            "candidate_count": len(technique_assets),
            "owned_candidate_count": len(
                [asset for asset in technique_assets if asset.get("asset_id") in OWNED_TECHNIQUE_IDS]
            ),
            "positive_evidence_count": _positive_evidence_count(state),
        },
        "project_asset_store": {
            "path": "system/creation_assets/project_assets.v0.2.json",
            "family_counts": dict(sorted(family_counts.items())),
            "validation": _store_validation(store),
        },
        "blocked_actions": [
            "write novel prose",
            "write combat scenes",
            "generate final technique tree",
            "execute-hermes",
            "execute-antigravity",
            "read novel_training_set/",
        ],
        "next_safe_action": (
            "Run produce-techniques after the techniques job is validated."
            if job.get("state") != "validated"
            else "Produce or inspect seed-level technique candidates."
        ),
    }
