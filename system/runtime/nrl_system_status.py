from __future__ import annotations

from typing import Any

from nrl_antigravity_bridge import (
    build_antigravity_bridge_status,
    build_antigravity_execution_status,
)


def content_progression_for(state: dict[str, Any]) -> str:
    if state.get("owner_gate_required", False):
        return "FROZEN_AT_OWNER_GATE"
    if "write novel prose" in state.get("blocked_actions", []):
        return "BLOCKED_FROM_PROSE"
    return "RUNTIME_CONTROLLED"


def operating_mode_for(state: dict[str, Any]) -> str:
    if content_progression_for(state) == "FROZEN_AT_OWNER_GATE":
        return "SYSTEM_HARDENING"
    return "CONTROLLED_RUNTIME"


def build_system_status(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    antigravity_execution = build_antigravity_execution_status(adapters)
    return {
        "operating_mode": operating_mode_for(state),
        "content_progression": content_progression_for(state),
        "current_phase": state.get("current_phase"),
        "phase_status": state.get("phase_status"),
        "owner_gate_required": state.get("owner_gate_required", False),
        "owner_gate_status": state.get("owner_gate_status"),
        "hermes_role": "later_writer_or_literary_enrichment",
        "hermes_execution_status": "paused_not_removed",
        "agent_roles": {
            "codex": "runtime_engineering_validation_orchestration",
            "antigravity": "cli_collaborative_literary_review",
            "hermes": "later_writer_or_literary_enrichment_after_explicit_authorization",
        },
        "adapter_modes": {
            name: {
                "mode": adapter.get("mode"),
                "can_execute": bool(adapter.get("can_execute", False)),
            }
            for name, adapter in adapters.items()
        },
        "antigravity_bridge": build_antigravity_bridge_status(),
        "antigravity_execution": antigravity_execution,
        "hard_rules": [
            "do not advance story phase",
            "do not advance story phase while owner gate is pending",
            "do not write novel prose",
            "do not write first chapter",
            "do not generate full character cards",
            "do not call Hermes until explicitly reauthorized",
            "use current pending review as a system-state test sample",
        ],
    }
