from __future__ import annotations

from typing import Any

from nrl_creation_assets import load_creation_asset_registry
from nrl_system_status import build_system_status


DASHBOARD_SECTION_KEYS = (
    "system_identity",
    "current_project",
    "agent_panel",
    "artifact_map",
    "creation_coverage_matrix",
    "runtime_status",
    "next_safe_action",
    "owner_gate",
    "creation_asset_registry",
)


def _adapter_mode(adapters: dict[str, Any], name: str) -> str:
    adapter = adapters.get(name, {})
    return str(adapter.get("mode", "unknown"))


def _adapter_can_execute(adapters: dict[str, Any], name: str) -> bool:
    adapter = adapters.get(name, {})
    return bool(adapter.get("can_execute", False))


def _latest_registry_mission(registry: list[dict[str, Any]]) -> dict[str, Any]:
    if not registry:
        return {}
    return registry[-1]


def _artifact_status(state: dict[str, Any], name: str) -> str:
    for artifact in state.get("key_artifacts", []):
        artifact_name = str(artifact.get("name", ""))
        if name.lower() in artifact_name.lower():
            return str(artifact.get("status", "present"))
    return "not_registered"


def _coverage_items_from_registry(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "asset": family["label"],
            "status": family["status"],
            "gap": family["why_not_complete"],
            "asset_id": family["asset_id"],
            "readiness_score": family["readiness_score"],
        }
        for family in registry["asset_families"]
    ]


def build_studio_data(
    state: dict[str, Any],
    registry: list[dict[str, Any]],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    latest_mission = _latest_registry_mission(registry)
    current_mission_name = state.get("next_recommended_mission", "UNKNOWN_MISSION")
    current_agent = str(state.get("allowed_next_agents", ["codex"])[0]).lower()
    expected_outputs = latest_mission.get("output_artifacts") or []
    active_attempts = latest_mission.get("handoff_attempts") or []
    creation_asset_registry = load_creation_asset_registry(
        str(state.get("selected_project", "UNKNOWN_PROJECT")),
        str(system_status["operating_mode"]),
    )

    return {
        "system_identity": {
            "name": "Novel Research Lab",
            "positioning": "Corpus-to-Creation engine for Chinese long-form web novel creation.",
            "not_a": [
                "generic AI writing app",
                "InkOS clone",
                "document pipeline",
            ],
            "core_chain": [
                "corpus reading",
                "single-book decomposition",
                "cross-book mechanism distillation",
                "narrative law library",
                "original project synthesis",
                "story bible",
                "outline and chapter planning",
                "draft",
                "review",
                "state ledger",
            ],
        },
        "current_project": {
            "project_name": state.get("project_name", "Novel Research Lab"),
            "selected_project": state.get("selected_project", "UNKNOWN_PROJECT"),
            "current_phase": state.get("current_phase", "UNKNOWN_PHASE"),
            "current_subphase": state.get("current_subphase", "UNKNOWN_SUBPHASE"),
            "phase_status": state.get("phase_status", "UNKNOWN_STATUS"),
            "system_mode": system_status["operating_mode"],
            "content_progression": system_status["content_progression"],
            "last_completed_mission": state.get("last_completed_mission", ""),
        },
        "agent_panel": {
            "items": [
                {
                    "agent": "Codex",
                    "status": "local_runtime_host",
                    "mode": _adapter_mode(adapters, "codex"),
                    "can_execute": _adapter_can_execute(adapters, "codex"),
                    "role": "local runtime host / engineering / validation / orchestration",
                },
                {
                    "agent": "Antigravity",
                    "status": "manual_external_literary_review",
                    "mode": _adapter_mode(adapters, "antigravity"),
                    "can_execute": _adapter_can_execute(adapters, "antigravity"),
                    "role": "manual external literary review",
                },
                {
                    "agent": "Hermes",
                    "status": system_status["hermes_execution_status"],
                    "display_status": f"Hermes: {system_status['hermes_execution_status']}",
                    "mode": _adapter_mode(adapters, "hermes"),
                    "can_execute": _adapter_can_execute(adapters, "hermes"),
                    "role": "paused, not removed; later writer / literary enrichment after explicit authorization",
                },
                {
                    "agent": "Web GPT",
                    "status": "architecture_review_only",
                    "mode": "external_conversation",
                    "can_execute": False,
                    "role": "architecture review only, not task dispatcher",
                },
                {
                    "agent": "Owner",
                    "status": "gate_authority",
                    "mode": "manual_gate",
                    "can_execute": True,
                    "role": "final authorization for phase and capability changes",
                },
            ],
        },
        "artifact_map": {
            "items": [
                {"area": "Corpus", "status": "asset_layer_present", "note": "raw corpus remains off-limits for Studio v0.1"},
                {"area": "Mechanisms", "status": "partial_engine", "note": "mechanism library exists but is not yet a queryable engine"},
                {"area": "Grand Synthesis", "status": "research_asset", "note": "research synthesis supports Corpus-to-Creation positioning"},
                {"area": "Story Bible", "status": _artifact_status(state, "Bible"), "note": "current project bible asset"},
                {"area": "Outline Tree", "status": _artifact_status(state, "Outline Tree"), "note": "Phase 2D outline tree asset"},
                {"area": "Planning Pack", "status": _artifact_status(state, "Planning"), "note": "Phase 2E planning control asset"},
                {"area": "Validation Reports", "status": state.get("validation_status", "UNKNOWN"), "note": "Codex validation status"},
                {"area": "Review Reports", "status": state.get("review_status", "UNKNOWN"), "note": "Antigravity review status"},
                {"area": "State Ledger", "status": "seed", "note": "state tracking exists but is not yet a full long-form ledger"},
            ],
        },
        "creation_coverage_matrix": {
            "assessment": "Long-form asset coverage is not complete; Studio v0.1 exposes the gaps instead of hiding them.",
            "items": _coverage_items_from_registry(creation_asset_registry),
        },
        "creation_asset_registry": creation_asset_registry,
        "runtime_status": {
            "health_commands": [
                "python3 system/runtime/nrl.py doctor",
                "python3 system/runtime/nrl.py system-status",
                "python3 system/runtime/nrl.py studio-data",
                "python3 system/runtime/nrl.py advance",
                "python3 system/runtime/nrl.py check-inputs",
                "python3 system/runtime/nrl.py validate-state",
            ],
            "state_validity_command": "python3 system/runtime/nrl.py validate-state",
            "status_command": "python3 system/runtime/nrl.py system-status",
            "studio_data_command": "python3 system/runtime/nrl.py studio-data",
            "current_mission": current_mission_name,
            "responsible_agent": current_agent,
            "registry_status": latest_mission.get("status", "no_registered_mission"),
            "adapter_modes": system_status["adapter_modes"],
            "handoff_attempts": active_attempts,
            "expected_outputs": expected_outputs,
            "blocked_actions": state.get("blocked_actions", []),
        },
        "next_safe_action": {
            "recommended": "Keep content progression frozen and continue Studio/system hardening.",
            "runtime_command": "python3 system/runtime/nrl.py system-status",
            "blocked_next_action": "Do not advance story content while Owner Gate is pending.",
            "safe_commands": [
                "python3 system/runtime/nrl.py system-status",
                "python3 system/runtime/nrl.py studio-data",
                "python3 system/runtime/nrl.py studio-build",
                "python3 system/runtime/nrl.py validate-state",
            ],
        },
        "owner_gate": {
            "required": bool(state.get("owner_gate_required", False)),
            "status": state.get("owner_gate_status", "UNKNOWN"),
            "review_status": state.get("review_status", "UNKNOWN"),
            "authorization_scope": ["status read", "studio build", "runtime validation", "system hardening"],
            "forbidden_scope": state.get("blocked_actions", []),
            "decision_boundary": "No stale Owner Gate decision may authorize a later gate.",
            "expires_after_mission": "current Owner Gate only",
        },
    }
