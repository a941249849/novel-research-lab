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
TECHNIQUE_CANDIDATES = (
    {
        "asset_id": "technique_costed_advancement",
        "display_name": "Costed Advancement Candidate",
        "cost": "Every advancement action must spend a visible resource, reputation position, or bodily state.",
        "constraints": [
            "seed candidate only",
            "not a final in-world technique name",
            "do not use for prose generation",
            "do not treat as final technique tree",
        ],
    },
    {
        "asset_id": "technique_backlash_guard",
        "display_name": "Backlash Guard Candidate",
        "cost": "Every defensive or stabilizing action must leave a delayed backlash, debt marker, or opportunity cost.",
        "constraints": [
            "seed candidate only",
            "not a final in-world technique name",
            "do not use for combat scene drafting",
            "must preserve a cost or counter path",
        ],
    },
    {
        "asset_id": "technique_state_reversal",
        "display_name": "State Reversal Candidate",
        "cost": "Every reversal action must convert one tracked state into another rather than erasing consequences.",
        "constraints": [
            "seed candidate only",
            "not a final in-world technique name",
            "do not generate final naming dictionary",
            "must cite DNA evidence before promotion",
        ],
    },
)


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


def _positive_evidence_ids(state: dict[str, Any]) -> list[str]:
    index = load_or_build_rag_index(state)
    return [
        str(item["source_dna_id"])
        for item in index.get("items", [])
        if int(item.get("evidence_weight", 0)) > 0
    ]


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


def _assert_no_forbidden_text(data: dict[str, Any]) -> None:
    encoded = json.dumps(data, ensure_ascii=False)
    for value in FORBIDDEN_TEXT:
        if value in encoded:
            raise RuntimeError(f"producer output contains forbidden text: {value}")


def _technique_candidate_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": candidate["asset_id"],
            "family": "techniques",
            "display_name": candidate["display_name"],
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": list(candidate["constraints"]),
            "technique": {
                "cost": candidate["cost"],
                "counter_ids": [],
            },
        }
        for candidate in TECHNIQUE_CANDIDATES
    ]


def _upsert_assets(store: dict[str, Any], produced: list[dict[str, Any]]) -> dict[str, Any]:
    owned = {asset["asset_id"] for asset in produced}
    preserved = [
        asset
        for asset in store.get("assets", [])
        if asset.get("asset_id") not in owned
    ]
    updated = {**store, "assets": sorted([*preserved, *produced], key=lambda item: item["asset_id"])}
    return updated


def produce_technique_candidates(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    if job_id != TECHNIQUES_JOB_ID:
        raise RuntimeError(f"unsupported technique producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"techniques job must be validated before production: {job_id}")
    outbox_path = ROOT / TECHNIQUES_OUTBOX_PATH
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {TECHNIQUES_OUTBOX_PATH}")

    evidence_ids = _positive_evidence_ids(state)
    if len(evidence_ids) < 3:
        raise RuntimeError("technique producer requires at least three positive evidence items")
    source_refs = [
        TECHNIQUES_OUTBOX_PATH,
        *evidence_ids[:3],
    ]
    produced = _technique_candidate_assets(source_refs)
    candidate_payload = {"assets": produced}
    _assert_no_forbidden_text(candidate_payload)

    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _assert_no_forbidden_text(updated_store)
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "technique_asset_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }
