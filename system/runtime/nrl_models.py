from __future__ import annotations


MISSION_STATUSES = {
    "planned",
    "package_generated",
    "client_staged",
    "awaiting_user_confirmation",
    "awaiting_external_output",
    "output_detected",
    "ingest_started",
    "ingest_failed",
    "validation_passed",
    "validation_failed",
    "review_required",
    "owner_gate_pending",
    "completed",
    "blocked",
}

ADAPTER_MODES = {"local", "manual_handoff", "client_handoff", "api", "cli", "cli_bridge"}


def require_mission_status(status: str) -> str:
    if status not in MISSION_STATUSES:
        raise RuntimeError(f"unsupported mission status: {status}")
    return status
