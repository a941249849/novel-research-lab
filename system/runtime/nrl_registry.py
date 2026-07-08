from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any

from nrl_models import require_mission_status
from nrl_paths import runtime_path


REGISTRY_PATH = runtime_path("system/runtime/mission_registry.json")


def load_json(path: Path) -> Any:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_registry() -> list[dict[str, Any]]:
    data = load_json(REGISTRY_PATH)
    if isinstance(data, list):
        return data
    raise RuntimeError("mission_registry.json must be a JSON array")


def save_registry(registry: list[dict[str, Any]]) -> None:
    write_json(REGISTRY_PATH, registry)


def upsert_registry_mission(mission: dict[str, Any], status: str, notes: list[str], now: str) -> None:
    require_mission_status(status)
    registry = load_registry()
    mission_id = mission["mission_id"]
    existing = next((m for m in registry if m.get("mission_id") == mission_id), None)
    if existing is None:
        registry.append(
            {
                "mission_id": mission_id,
                "mission_name": mission["mission_name"],
                "phase": mission["phase"],
                "responsible_agent": mission["responsible_agent"],
                "status": status,
                "input_artifacts": mission["required_inputs"],
                "output_artifacts": mission["expected_outputs"],
                "created_at": now,
                "updated_at": now,
                "gate_status": "owner_gate_required" if mission["whether_owner_gate_required"] else "owner_gate_not_required",
                "notes": notes,
            }
        )
    else:
        existing["mission_name"] = mission["mission_name"]
        existing["phase"] = mission["phase"]
        existing["responsible_agent"] = mission["responsible_agent"]
        existing["status"] = status
        existing["input_artifacts"] = mission["required_inputs"]
        existing["output_artifacts"] = sorted(dict.fromkeys(existing.get("output_artifacts", []) + mission["expected_outputs"]))
        existing["updated_at"] = now
        existing["gate_status"] = "owner_gate_required" if mission["whether_owner_gate_required"] else "owner_gate_not_required"
        existing["notes"] = sorted(dict.fromkeys(existing.get("notes", []) + notes))
    save_registry(registry)


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_hashes(paths: list[str]) -> dict[str, str]:
    hashes = {}
    for rel in paths:
        hashes[rel] = sha256_file(runtime_path(rel))
    return hashes


def record_handoff_attempt(mission: dict[str, Any], adapter_mode: str, now: str) -> dict[str, Any]:
    upsert_registry_mission(mission, "awaiting_external_output", [f"adapter_mode={adapter_mode}"], now)
    registry = load_registry()
    item = next(m for m in registry if m.get("mission_id") == mission["mission_id"])
    attempts = item.setdefault("handoff_attempts", [])
    expected_output_path = mission["expected_outputs"][0]
    for attempt in reversed(attempts):
        if attempt.get("expected_output_path") == expected_output_path and attempt.get("status") == "awaiting_external_output":
            attempt["adapter_mode"] = adapter_mode
            attempt["input_artifact_hashes"] = input_hashes(mission["required_inputs"])
            attempt["ingest_command"] = (
                f"python3 system/runtime/nrl.py ingest --agent {mission['responsible_agent']} --file {expected_output_path}"
            )
            attempt["updated_at"] = now
            item["updated_at"] = now
            save_registry(registry)
            return attempt
    attempt_id = f"{mission['mission_id']}_attempt_{len(attempts) + 1:03d}"
    attempt = {
        "handoff_attempt_id": attempt_id,
        "mission_id": mission["mission_id"],
        "target_agent": mission["responsible_agent"],
        "adapter_mode": adapter_mode,
        "input_artifact_hashes": input_hashes(mission["required_inputs"]),
        "expected_output_path": expected_output_path,
        "created_at": now,
        "stale_after": "",
        "ingest_command": f"python3 system/runtime/nrl.py ingest --agent {mission['responsible_agent']} --file {expected_output_path}",
        "validation_contract": "Codex validation or Owner Gate required by mission contract",
        "status": "awaiting_external_output",
    }
    attempts.append(attempt)
    item["updated_at"] = now
    save_registry(registry)
    return attempt


def find_active_attempt(mission_id: str, output_path: str) -> dict[str, Any] | None:
    registry = load_registry()
    item = next((m for m in registry if m.get("mission_id") == mission_id), None)
    if item is None:
        return None
    for attempt in reversed(item.get("handoff_attempts", [])):
        if attempt.get("expected_output_path") == output_path and attempt.get("status") == "awaiting_external_output":
            return attempt
    return None


def mark_attempt_status(mission_id: str, attempt_id: str, status: str, now: str) -> None:
    registry = load_registry()
    item = next(m for m in registry if m.get("mission_id") == mission_id)
    for attempt in item.get("handoff_attempts", []):
        if attempt.get("handoff_attempt_id") == attempt_id:
            attempt["status"] = status
            attempt["updated_at"] = now
    item["updated_at"] = now
    save_registry(registry)
