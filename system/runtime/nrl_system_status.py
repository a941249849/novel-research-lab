from __future__ import annotations

import json
from typing import Any

from nrl_antigravity_bridge import (
    build_antigravity_bridge_status,
    build_antigravity_execution_status,
)
from nrl_hermes_bridge import build_hermes_execution_status
from nrl_deep_read import build_deep_read_status
from nrl_paths import runtime_path
from nrl_story_window import build_story_window_status


ACTIVE_BLUEPRINT_PATH = runtime_path(
    "system/production_runtime/active_story_blueprint.v0.24.json"
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
    hermes_execution = build_hermes_execution_status(adapters.get("hermes", {}))
    deep_read = build_deep_read_status()
    blueprint = (
        json.loads(ACTIVE_BLUEPRINT_PATH.read_text(encoding="utf-8"))
        if ACTIVE_BLUEPRINT_PATH.exists()
        else {}
    )
    story_windows = build_story_window_status()
    production_checks = {
        "deep_read_verified": bool(deep_read["deep_read_verified"]),
        "owner_authorization_active": not state.get("owner_gate_required", False),
        "prose_not_globally_blocked": "write novel prose" not in state.get("blocked_actions", []),
        "active_blueprint_allows_governed_prose": bool(blueprint.get("prose_allowed")),
        "story_window_contract_valid": bool(story_windows["valid"]),
    }
    production_blockers = [name for name, passed in production_checks.items() if not passed]
    hard_rules = [
        "generate prose only inside the Owner-authorized chapter range",
        "require a validated ten-chapter story window before chapter compilation",
        "settle chapter state before the next chapter can start",
        "keep raw novel_training_set outside the chapter production runtime",
        "do not publish before the Volume 1 release gate passes",
        "use Antigravity for bounded literary review, not as the production state owner",
        "Hermes remains optional and cannot bypass runtime gates",
    ]
    if state.get("owner_gate_required", False):
        hard_rules.insert(0, "do not advance story phase")
    return {
        "operating_mode": operating_mode_for(state),
        "content_progression": content_progression_for(state),
        "current_phase": state.get("current_phase"),
        "phase_status": state.get("phase_status"),
        "owner_gate_required": state.get("owner_gate_required", False),
        "owner_gate_status": state.get("owner_gate_status"),
        "hermes_role": "later_writer_or_literary_enrichment",
        "hermes_execution_status": hermes_execution["effective_state"],
        "agent_roles": {
            "codex": "runtime_engineering_validation_orchestration",
            "antigravity": "cli_collaborative_literary_review",
            "hermes": "cli_controlled_literary_enrichment_after_explicit_authorization",
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
        "hermes_execution": hermes_execution,
        "verifiable_deep_reading": deep_read,
        "production_ready": not production_blockers,
        "production_checks": production_checks,
        "production_blockers": production_blockers,
        "story_windows": story_windows,
        "hard_rules": hard_rules,
    }
