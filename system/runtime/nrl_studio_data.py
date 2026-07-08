from __future__ import annotations

from typing import Any

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
            "items": [
                {"asset": "Characters", "status": "partial", "gap": "core roles exist; full character engine is not complete"},
                {"asset": "NPCs", "status": "missing", "gap": "witnesses, rivals, minor officials, and reversible roles need a system"},
                {"asset": "Factions", "status": "partial", "gap": "major institutions exist; faction internals and cracks are sparse"},
                {"asset": "Artifacts", "status": "seed", "gap": "motifs exist; item lifecycle and upgrade paths are not modeled"},
                {"asset": "Techniques", "status": "missing", "gap": "ability tree, move names, costs, counters, and upgrades are missing"},
                {"asset": "Naming", "status": "missing", "gap": "no naming grammar for people, powers, places, artifacts, or realms"},
                {"asset": "Emotional Bonds", "status": "partial", "gap": "mother bond is strong; wider bond network is not complete"},
                {"asset": "Foreshadowing", "status": "partial", "gap": "ledger idea exists; retrieval and payoff lifecycle are not productized"},
                {"asset": "State Ledger", "status": "seed", "gap": "state concept exists; chapter-by-chapter operating ledger is not complete"},
            ],
        },
        "runtime_status": {
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
