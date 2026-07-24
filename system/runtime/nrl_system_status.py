from __future__ import annotations

import json
from typing import Any

from nrl_antigravity_bridge import (
    build_antigravity_bridge_status,
    build_antigravity_execution_status,
)
from nrl_deep_read import build_deep_read_status
from nrl_model_router import build_model_routing_status, validate_model_team_contract
from nrl_paths import runtime_path
from nrl_story_window import build_story_window_status
from nrl_projects import build_project_status, list_projects, validate_project_isolation


ACTIVE_BLUEPRINT_PATH = runtime_path(
    "system/production_runtime/active_story_blueprint.v0.24.json"
)


def content_progression_for(state: dict[str, Any]) -> str:
    project = build_project_status()
    if (
        state.get("owner_gate_required", False)
        or project.get("status") == "owner_gate"
    ):
        return "FROZEN_AT_OWNER_GATE"
    if not project["ready_for_prose"]:
        return "BLOCKED_AT_PROJECT_SETUP"
    if "write novel prose" in state.get("blocked_actions", []):
        return "BLOCKED_FROM_PROSE"
    return "RUNTIME_CONTROLLED"


def operating_mode_for(state: dict[str, Any]) -> str:
    progression = content_progression_for(state)
    if progression == "FROZEN_AT_OWNER_GATE":
        return "SYSTEM_HARDENING"
    if progression == "BLOCKED_AT_PROJECT_SETUP":
        return "PROJECT_DESIGN"
    return "CONTROLLED_RUNTIME"


def build_system_status(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    antigravity_execution = build_antigravity_execution_status(adapters)
    deep_read = build_deep_read_status()
    model_routing = build_model_routing_status()
    model_team_contract = validate_model_team_contract()
    blueprint = (
        json.loads(ACTIVE_BLUEPRINT_PATH.read_text(encoding="utf-8"))
        if ACTIVE_BLUEPRINT_PATH.exists()
        else {}
    )
    story_windows = build_story_window_status()
    project_status = build_project_status()
    project_isolation = validate_project_isolation()
    production_checks = {
        "deep_read_verified": bool(deep_read["deep_read_verified"]),
        "owner_authorization_active": (
            project_status["content_authorized"]
            and not state.get("owner_gate_required", False)
        ),
        "prose_not_globally_blocked": (
            project_status["content_authorized"]
            and "write novel prose" not in state.get("blocked_actions", [])
        ),
        "active_blueprint_allows_governed_prose": bool(blueprint.get("prose_allowed")),
        "story_window_contract_valid": bool(story_windows["valid"]),
        "codex_model_team_contract_valid": model_team_contract["valid"],
        "project_isolation_valid": project_isolation["valid"],
        "active_project_ready_for_prose": project_status["ready_for_prose"],
    }
    production_blockers = [name for name, passed in production_checks.items() if not passed]
    hard_rules = [
        "generate prose only inside the Owner-authorized chapter range",
        "require a validated ten-chapter story window before chapter compilation",
        "settle chapter state before the next chapter can start",
        "keep raw novel_training_set outside the chapter production runtime",
        "do not publish before the Volume 1 release gate passes",
        "use Antigravity only for independent review or provider fallback, never as production state owner",
        "route planning/review to Sol, prose/editing to Terra, and observation/mechanical work to Luna",
    ]
    if state.get("owner_gate_required", False):
        hard_rules.insert(0, "do not advance story phase")
    return {
        "operating_mode": operating_mode_for(state),
        "content_progression": content_progression_for(state),
        "current_phase": state.get("current_phase"),
        "project_stage": project_status["status"],
        "active_project": project_status,
        "project_registry": list_projects(),
        "project_isolation": project_isolation,
        "phase_status": state.get("phase_status"),
        "owner_gate_required": (
            state.get("owner_gate_required", False)
            or not project_status["content_authorized"]
        ),
        "owner_gate_status": (
            state.get("owner_gate_status")
            if project_status["content_authorized"]
            else (
                "OWNER_REVIEW_REQUIRED"
                if project_status.get("status") == "owner_gate"
                else "PROJECT_SETUP_REQUIRED"
            )
        ),
        "agent_roles": {
            "codex": "three_model_runtime_planning_writing_review_observation",
            "antigravity": "backup_review_and_provider_fallback",
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
        "antigravity_role": "backup_review_and_provider_fallback",
        "codex_model_team": model_routing["routes"],
        "model_team_contract": model_team_contract,
        "verifiable_deep_reading": deep_read,
        "production_ready": not production_blockers,
        "production_checks": production_checks,
        "production_blockers": production_blockers,
        "story_windows": story_windows,
        "hard_rules": hard_rules,
    }
