from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from nrl_paths import ROOT
from nrl_registry import load_registry


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )


def inspect_git(root: Path = ROOT) -> dict[str, Any]:
    top_level = _git(["rev-parse", "--show-toplevel"], root)
    if top_level.returncode != 0:
        return {
            "is_repo": False,
            "root": None,
            "branch": None,
            "remotes": [],
            "status": "not_a_git_repository",
        }

    branch = _git(["branch", "--show-current"], root)
    remotes = _git(["remote", "-v"], root)
    remote_rows = []
    if remotes.returncode == 0:
        for line in remotes.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3:
                remote_rows.append({"name": parts[0], "url": parts[1], "kind": parts[2].strip("()")})

    return {
        "is_repo": True,
        "root": top_level.stdout.strip(),
        "branch": branch.stdout.strip() if branch.returncode == 0 else None,
        "remotes": remote_rows,
        "status": "git_repository_detected",
    }


def adapter_summary(adapters: dict[str, Any]) -> dict[str, dict[str, Any]]:
    summary = {}
    for name, adapter in adapters.items():
        summary[name] = {
            "mode": adapter.get("mode"),
            "can_execute": bool(adapter.get("can_execute", False)),
            "handoff_dir": adapter.get("handoff_dir"),
            "expected_output_dir": adapter.get("expected_output_dir"),
        }
    return summary


def handoff_summary(mission: dict[str, Any]) -> dict[str, Any]:
    expected_outputs = mission.get("expected_outputs", [])
    return {
        "expected_outputs": expected_outputs,
        "outputs_exist": [
            {
                "path": rel,
                "exists": (ROOT / rel).exists(),
            }
            for rel in expected_outputs
        ],
    }


def latest_registry_status(mission_id: str) -> dict[str, Any] | None:
    for mission in load_registry():
        if mission.get("mission_id") == mission_id:
            attempts = mission.get("handoff_attempts", [])
            return {
                "status": mission.get("status"),
                "attempt_count": len(attempts),
                "latest_attempt_status": attempts[-1].get("status") if attempts else None,
            }
    return None


def run_doctor(state: dict[str, Any], adapters: dict[str, Any], mission: dict[str, Any]) -> dict[str, Any]:
    mission_id = mission["mission_id"]
    registry_status = latest_registry_status(mission_id)

    return {
        "runtime": "Novel Research Lab",
        "root": str(ROOT),
        "git": inspect_git(ROOT),
        "mission": {
            "mission_id": mission_id,
            "mission_name": mission["mission_name"],
            "phase": mission["phase"],
            "responsible_agent": mission["responsible_agent"],
            "registry": registry_status,
        },
        "adapters": adapter_summary(adapters),
        "gates": {
            "phase_status": state.get("phase_status"),
            "validation_status": state.get("validation_status"),
            "review_status": state.get("review_status"),
            "owner_gate_required": state.get("owner_gate_required", False),
            "owner_gate_status": state.get("owner_gate_status"),
        },
        "handoff": handoff_summary(mission),
        "blocked_actions": state.get("blocked_actions", []),
        "recommended_next_command": "python3 system/runtime/nrl.py advance",
    }
