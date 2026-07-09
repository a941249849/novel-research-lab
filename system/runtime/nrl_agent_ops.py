from __future__ import annotations

import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_corpus_pipeline import build_pipeline_plan
from nrl_dna_registry import load_or_build_dna_registry
from nrl_paths import ROOT, runtime_path
from nrl_rag_index import load_or_build_rag_index, write_rag_index
from nrl_system_status import build_system_status


VERSION = "0.5"
QUEUE_PATH = runtime_path("system/agent_ops/job_queue.v0.5.json")
PACKET_DIR = runtime_path("system/agent_ops/packets")
INBOX_DIR = runtime_path("system/agent_ops/inbox")
OUTBOX_DIR = runtime_path("system/agent_ops/outbox")
VALIDATION_DIR = runtime_path("system/agent_ops/validation")
JOB_STATES = {
    "planned",
    "ready_for_codex",
    "ready_for_antigravity",
    "external_running",
    "output_received",
    "validated",
    "promoted",
    "rejected",
    "blocked",
}
REQUIRED_REVIEW_SECTIONS = (
    "## Job ID",
    "## Structural Review",
    "## Evidence Use",
    "## Originality Risk",
    "## Required Fixes",
    "## Promotion Recommendation",
)
FORBIDDEN_OUTPUT_TEXT = ("Chapter 1", "正文", "第一章")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _empty_queue() -> dict[str, Any]:
    return {
        "queue_name": "NRL Agent Job Queue",
        "version": VERSION,
        "jobs": [],
        "summary": {"total_jobs": 0, "by_state": {}, "by_family": {}},
    }


def _summarize_jobs(jobs: list[dict[str, Any]]) -> dict[str, Any]:
    by_state = Counter(str(job["state"]) for job in jobs)
    by_family = Counter(str(job["target_family"]) for job in jobs)
    return {
        "total_jobs": len(jobs),
        "by_state": dict(sorted(by_state.items())),
        "by_family": dict(sorted(by_family.items())),
    }


def _queue_payload(jobs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "queue_name": "NRL Agent Job Queue",
        "version": VERSION,
        "jobs": sorted(jobs, key=lambda job: job["job_id"]),
        "summary": _summarize_jobs(jobs),
        "guardrails": [
            "File-backed queue only",
            "Manual external agent execution only",
            "No prose generation jobs",
        ],
    }


def load_job_queue() -> dict[str, Any]:
    if not QUEUE_PATH.exists():
        return _empty_queue()
    data = _read_json(QUEUE_PATH)
    if data.get("version") != VERSION:
        return _empty_queue()
    return data


def save_job_queue(queue: dict[str, Any]) -> dict[str, Any]:
    payload = _queue_payload(list(queue.get("jobs", [])))
    _write_json(QUEUE_PATH, payload)
    return payload


def _find_job(queue: dict[str, Any], job_id: str) -> dict[str, Any]:
    for job in queue.get("jobs", []):
        if job.get("job_id") == job_id:
            return job
    raise RuntimeError(f"agent job not found: {job_id}")


def _source_dna_ids(state: dict[str, Any], family: str) -> list[str]:
    index = load_or_build_rag_index(state)
    family_terms = {family, "state_dna", "mechanism_dna"}
    selected = [
        item["source_dna_id"]
        for item in index["items"]
        if str(item.get("asset_type")) in family_terms or family in str(item.get("retrieval_text", ""))
    ]
    if len(selected) < 3:
        registry = load_or_build_dna_registry(state)
        selected.extend(entry["dna_id"] for entry in registry["entries"] if entry["family"] != "project_dna")
    return sorted(dict.fromkeys(str(item) for item in selected))[:18]


def _job_id(family: str) -> str:
    return f"job-v05-{family}-antigravity-review"


def _expected_output_path(job_id: str) -> str:
    return f"system/agent_ops/inbox/{job_id}.md"


def plan_agent_job(
    state: dict[str, Any],
    adapters: dict[str, Any],
    family: str,
) -> dict[str, Any]:
    build_pipeline_plan(state, adapters, family=family)
    write_rag_index(state)
    queue = load_job_queue()
    jobs = list(queue.get("jobs", []))
    job_id = _job_id(family)
    created = now_iso()
    existing = next((item for item in jobs if item.get("job_id") == job_id), None)
    preserved_state = str(existing.get("state")) if existing else "ready_for_antigravity"
    if preserved_state not in {"validated", "promoted"}:
        preserved_state = "ready_for_antigravity"
    updated_at = existing.get("updated_at") if existing and preserved_state in {"validated", "promoted"} else created
    job = {
        "job_id": job_id,
        "job_type": "antigravity_structural_review",
        "target_family": family,
        "owner_agent": "antigravity",
        "state": preserved_state,
        "source_dna_ids": _source_dna_ids(state, family),
        "input_packet_path": f"system/agent_ops/packets/{job_id}.md",
        "expected_output_path": _expected_output_path(job_id),
        "actual_output_path": existing.get("actual_output_path") if existing else None,
        "validation_report_path": existing.get("validation_report_path") if existing else None,
        "promotion_target": f"system/creation_assets/project_assets.v0.2.json::{family}",
        "created_at": existing.get("created_at") if existing else created,
        "updated_at": updated_at,
        "blocked_reason": None,
    }
    jobs = [item for item in jobs if item.get("job_id") != job_id]
    jobs.append(job)
    queue = save_job_queue({"jobs": jobs})
    return {"job": _find_job(queue, job_id), "queue_path": str(QUEUE_PATH.relative_to(ROOT))}


def _packet_text(job: dict[str, Any]) -> str:
    dna_lines = "\n".join(f"- {dna_id}" for dna_id in job["source_dna_ids"])
    required_sections = "\n".join(f"- {section}" for section in REQUIRED_REVIEW_SECTIONS)
    return f"""# NRL Antigravity Manual Review Packet

## JOB

- job_id: {job["job_id"]}
- target_family: {job["target_family"]}
- owner_agent: antigravity
- expected_output_path: {job["expected_output_path"]}

## PURPOSE

Review whether the current DNA evidence is sufficient to plan the `{job["target_family"]}` creation asset family.
Focus on long-form vitality, structural usefulness, originality risk, and missing evidence.

## SOURCE DNA IDS

{dna_lines}

## REQUIRED OUTPUT SECTIONS

{required_sections}

## FORBIDDEN ACTIONS

- Do not write prose.
- Do not draft Chapter 1.
- Do not create final character sheets, technique trees, naming dictionaries, or NPC dossiers.
- Do not claim Hermes execution.
- Do not read or quote raw `novel_training_set/` prose.

## RETURN INSTRUCTION

Save the completed review to:

```text
{job["expected_output_path"]}
```
"""


def write_agent_packet(job_id: str) -> dict[str, Any]:
    queue = load_job_queue()
    job = _find_job(queue, job_id)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    packet_path = ROOT / job["input_packet_path"]
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(_packet_text(job), encoding="utf-8")
    job["state"] = "ready_for_antigravity"
    job["updated_at"] = now_iso()
    save_job_queue(queue)
    return {
        "job_id": job_id,
        "packet_path": str(packet_path.relative_to(ROOT)),
        "expected_output_path": job["expected_output_path"],
    }


def _resolve_repo_path(file_arg: str) -> Path:
    path = Path(file_arg)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def ingest_agent_output(job_id: str, file_arg: str) -> dict[str, Any]:
    queue = load_job_queue()
    job = _find_job(queue, job_id)
    file_path = _resolve_repo_path(file_arg)
    inbox = INBOX_DIR.resolve()
    if not _is_relative_to(file_path, inbox):
        raise RuntimeError(f"agent output must be placed under system/agent_ops/inbox: {file_arg}")
    if not file_path.exists():
        raise RuntimeError(f"agent output file does not exist: {file_arg}")
    rel_path = str(file_path.relative_to(ROOT))
    if job.get("state") in {"validated", "promoted"} and job.get("actual_output_path") == rel_path:
        return {"job": job, "ingested": rel_path}
    job["actual_output_path"] = rel_path
    job["state"] = "output_received"
    job["updated_at"] = now_iso()
    save_job_queue(queue)
    return {"job": job, "ingested": job["actual_output_path"]}


def validate_agent_job(job_id: str) -> dict[str, Any]:
    queue = load_job_queue()
    job = _find_job(queue, job_id)
    actual = job.get("actual_output_path")
    if not actual:
        raise RuntimeError(f"agent job has no ingested output: {job_id}")
    output_path = ROOT / str(actual)
    text = output_path.read_text(encoding="utf-8")
    missing_sections = [section for section in REQUIRED_REVIEW_SECTIONS if section not in text]
    forbidden_hits = [value for value in FORBIDDEN_OUTPUT_TEXT if value in text]
    valid = not missing_sections and not forbidden_hits and job_id in text
    report_path = VALIDATION_DIR / f"{job_id}_validation.json"
    if valid and job.get("state") == "validated" and report_path.exists():
        return {"valid": True, "job": job, "report": _read_json(report_path)}
    report = {
        "job_id": job_id,
        "valid": valid,
        "missing_sections": missing_sections,
        "forbidden_hits": forbidden_hits,
        "validated_at": now_iso(),
    }
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    _write_json(report_path, report)
    job["validation_report_path"] = str(report_path.relative_to(ROOT))
    if valid:
        OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
        outbox_path = OUTBOX_DIR / f"{job_id}_validated.md"
        shutil.copyfile(output_path, outbox_path)
        job["state"] = "validated"
        job["blocked_reason"] = None
    else:
        job["state"] = "rejected"
        job["blocked_reason"] = "validation_failed"
    job["updated_at"] = now_iso()
    queue = save_job_queue(queue)
    return {"valid": valid, "job": _find_job(queue, job_id), "report": report}


def build_production_runtime_status(
    state: dict[str, Any],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    registry = load_or_build_dna_registry(state)
    index = load_or_build_rag_index(state)
    queue = load_job_queue()
    packet_paths = (
        sorted(str(path.relative_to(ROOT)) for path in PACKET_DIR.glob("*.md"))
        if PACKET_DIR.exists()
        else []
    )
    inbox_count = len([path for path in INBOX_DIR.glob("*") if path.is_file()]) if INBOX_DIR.exists() else 0
    outbox_count = len([path for path in OUTBOX_DIR.glob("*") if path.is_file()]) if OUTBOX_DIR.exists() else 0
    antigravity = adapters.get("antigravity", {})
    return {
        "version": VERSION,
        "system_mode": system_status["operating_mode"],
        "content_progression": system_status["content_progression"],
        "owner_gate": {
            "required": system_status["owner_gate_required"],
            "status": system_status["owner_gate_status"],
        },
        "dna_registry": registry["summary"],
        "rag_index": index["summary"],
        "agent_jobs": queue["summary"],
        "current_packets": packet_paths,
        "agent_io": {
            "inbox_dir": "system/agent_ops/inbox",
            "outbox_dir": "system/agent_ops/outbox",
            "inbox_count": inbox_count,
            "outbox_count": outbox_count,
        },
        "antigravity": {
            "mode": antigravity.get("mode", "manual_handoff"),
            "status": "manual_external_review",
        },
        "hermes": {
            "status": system_status["hermes_execution_status"],
            "allowed": False,
        },
    }
