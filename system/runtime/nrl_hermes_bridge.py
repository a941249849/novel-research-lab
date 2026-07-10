from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


MODEL = "gpt-5.6-terra"
PROVIDER = "openai-codex"


def find_hermes_binary() -> str | None:
    override = os.environ.get("NRL_HERMES_BIN")
    if override:
        return override if Path(override).exists() else None
    return shutil.which("hermes") or shutil.which(str(Path.home() / ".local/bin/hermes"))


def build_hermes_execution_status(adapter: dict[str, Any]) -> dict[str, Any]:
    binary = find_hermes_binary()
    if not binary:
        return {
            "declared_mode": adapter.get("mode", "manual_handoff"),
            "available": False,
            "binary_path": None,
            "model": MODEL,
            "effective_state": "blocked_bridge_unavailable",
            "can_execute_controlled_prose_test": False,
            "blocked_reason": "hermes binary not found",
        }
    probe = subprocess.run(
        [binary, "--version"], text=True, capture_output=True, check=False
    )
    configured = adapter.get("mode") == "cli_bridge"
    available = probe.returncode == 0
    ready = configured and available
    return {
        "declared_mode": adapter.get("mode", "manual_handoff"),
        "available": available,
        "binary_path": binary,
        "model": MODEL,
        "version_output": (probe.stdout or probe.stderr).strip(),
        "effective_state": "ready" if ready else "manual_handoff",
        "can_execute_controlled_prose_test": ready,
        "blocked_reason": None if ready else "Hermes adapter is not configured for cli_bridge",
    }


def ask_hermes(prompt: str) -> str:
    binary = find_hermes_binary()
    if not binary:
        raise RuntimeError("hermes binary not found")
    result = subprocess.run(
        [binary, "--provider", PROVIDER, "--model", MODEL, "--oneshot", prompt],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Hermes CLI failed with exit code {result.returncode}: {result.stderr}")
    return result.stdout.strip()
