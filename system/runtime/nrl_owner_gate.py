from __future__ import annotations

import json
from typing import Any

from nrl_paths import runtime_path


OWNER_GATE_PATH = runtime_path("system/runtime/owner_gate_decisions.json")
DECISION_TYPES = {
    "accept_review",
    "request_rework",
    "authorize_next_phase",
    "authorize_adapter_upgrade",
    "authorize_research_promotion",
    "authorize_final_asset_generation",
    "authorize_controlled_prose_test",
}


def load_decisions() -> list[dict[str, Any]]:
    if not OWNER_GATE_PATH.exists():
        return []
    with OWNER_GATE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    raise RuntimeError("owner_gate_decisions.json must be a JSON array")


def save_decisions(decisions: list[dict[str, Any]]) -> None:
    OWNER_GATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    OWNER_GATE_PATH.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def record_owner_decision(decision: dict[str, Any], now: str) -> dict[str, Any]:
    if decision["decision_type"] not in DECISION_TYPES:
        raise RuntimeError(f"unsupported owner decision type: {decision['decision_type']}")
    if not decision["authorized_scope"]:
        raise RuntimeError("owner decision requires at least one authorized scope")
    if not decision["forbidden_scope"]:
        raise RuntimeError("owner decision requires at least one forbidden scope")
    decisions = load_decisions()
    if any(item.get("decision_id") == decision["decision_id"] for item in decisions):
        raise RuntimeError(f"owner decision already exists: {decision['decision_id']}")
    decision["created_at"] = now
    decisions.append(decision)
    save_decisions(decisions)
    return decision
