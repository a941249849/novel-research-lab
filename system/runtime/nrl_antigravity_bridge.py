from __future__ import annotations

import json
import os
import shutil
import subprocess
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path


VERSION = "0.8"
DEFAULT_REQUEST_DIR = ".agent-handoff/antigravity/requests"
DEFAULT_RESPONSE_DIR = ".agent-handoff/antigravity/responses"
BRIDGE_LOG_PATH = runtime_path("system/agent_ops/antigravity_bridge_last_run.v0.8.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_agy_binary() -> str | None:
    override = os.environ.get("NRL_AGY_BIN")
    if override:
        return override if Path(override).exists() else None
    return shutil.which("agy") or shutil.which(str(Path.home() / ".local/bin/agy"))


@lru_cache(maxsize=1)
def build_antigravity_bridge_status() -> dict[str, Any]:
    binary = find_agy_binary()
    if not binary:
        return {
            "version": VERSION,
            "available": False,
            "mode": "cli",
            "binary_path": None,
            "version_output": None,
            "blocked_reason": "agy binary not found",
            "request_dir": DEFAULT_REQUEST_DIR,
            "response_dir": DEFAULT_RESPONSE_DIR,
        }
    try:
        version = subprocess.run(
            [binary, "--version"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=2,
        )
        version_output = (version.stdout or version.stderr).strip()
        blocked_reason = None if version.returncode == 0 else "agy --version failed"
    except subprocess.TimeoutExpired:
        # A running long-context job can hold the CLI state lock. Binary
        # presence still proves the bridge is installed; do not block Studio.
        version_output = "version check deferred while CLI is busy"
        blocked_reason = None
    return {
        "version": VERSION,
        "available": True,
        "mode": "cli",
        "binary_path": binary,
        "version_output": version_output,
        "blocked_reason": blocked_reason,
        "request_dir": DEFAULT_REQUEST_DIR,
        "response_dir": DEFAULT_RESPONSE_DIR,
    }


def build_antigravity_execution_status(adapters: dict[str, Any]) -> dict[str, Any]:
    declared_mode = str(adapters.get("antigravity", {}).get("mode", "manual_handoff"))
    bridge = build_antigravity_bridge_status()
    if declared_mode == "cli_bridge" and bridge["available"]:
        effective_state = "ready"
        can_dispatch = True
        blocked_reason = None
    elif declared_mode == "cli_bridge":
        effective_state = "blocked_bridge_unavailable"
        can_dispatch = False
        blocked_reason = bridge["blocked_reason"]
    else:
        effective_state = "manual_handoff"
        can_dispatch = False
        blocked_reason = "antigravity adapter is not configured for cli_bridge"
    return {
        "declared_mode": declared_mode,
        "bridge_available": bool(bridge["available"]),
        "effective_state": effective_state,
        "can_dispatch_registered_reviews": can_dispatch,
        "blocked_reason": blocked_reason,
        "allowed_job_types": ["antigravity_structural_review"] if can_dispatch else [],
    }


def _resolve_repo_path(file_arg: str) -> Path:
    path = Path(file_arg)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def _relative_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def ask_antigravity(
    request_file: str,
    output_file: str | None = None,
    print_timeout: str = "5m0s",
    model: str | None = None,
) -> dict[str, Any]:
    binary = find_agy_binary()
    if not binary:
        raise RuntimeError("agy binary not found; install Antigravity CLI before using bridge")
    request_path = _resolve_repo_path(request_file)
    if not request_path.exists():
        raise RuntimeError(f"request file does not exist: {request_file}")
    prompt = request_path.read_text(encoding="utf-8")
    if not prompt.strip():
        raise RuntimeError(f"request file is empty: {request_file}")
    bridge_contract = """\
NRL bridge contract: this is a non-interactive structural review call. Do not
write files, run shell commands, create scratch scripts, or narrate tool use.
Return only the final Markdown review body. The first line must be a Markdown
heading and the response must use the exact section headings requested by the
packet. Do not include a preamble, plan, progress log, file links, or postscript.

"""
    if output_file:
        response_path = _resolve_repo_path(output_file)
    else:
        response_path = runtime_path(
            f"{DEFAULT_RESPONSE_DIR}/{request_path.stem}_response.md"
        )
    response_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = now_iso()
    command = [
        binary,
        "--dangerously-skip-permissions",
        "--mode",
        "plan",
        "--sandbox",
        "--print-timeout",
        print_timeout,
    ]
    if model:
        command.extend(["--model", model])
    command.extend(["-p", bridge_contract + prompt])
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    response_text = result.stdout
    if result.stderr:
        response_text = response_text + ("\n" if response_text else "") + result.stderr
    response_path.write_text(response_text, encoding="utf-8")
    payload = {
        "version": VERSION,
        "mode": "cli",
        "binary_path": binary,
        "request_file": _relative_to_root(request_path),
        "output_file": _relative_to_root(response_path),
        "returncode": result.returncode,
        "model": model,
        "started_at": started_at,
        "finished_at": now_iso(),
        "bridge_log_path": str(BRIDGE_LOG_PATH.relative_to(ROOT)),
    }
    _write_json(BRIDGE_LOG_PATH, payload)
    permission_denied_markers = (
        "no output produced",
        "read_file permission",
        "auto-denied",
    )
    bridge_failed = result.returncode != 0 or any(
        marker in response_text.lower() for marker in permission_denied_markers
    )
    if bridge_failed:
        raise RuntimeError(f"agy bridge call failed with exit code {result.returncode}; response written to {payload['output_file']}")
    return payload
