from __future__ import annotations

import json
import os
import shutil
import subprocess
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
    version = subprocess.run(
        [binary, "--version"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "version": VERSION,
        "available": version.returncode == 0,
        "mode": "cli",
        "binary_path": binary,
        "version_output": (version.stdout or version.stderr).strip(),
        "blocked_reason": None if version.returncode == 0 else "agy --version failed",
        "request_dir": DEFAULT_REQUEST_DIR,
        "response_dir": DEFAULT_RESPONSE_DIR,
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
    if output_file:
        response_path = _resolve_repo_path(output_file)
    else:
        response_path = runtime_path(
            f"{DEFAULT_RESPONSE_DIR}/{request_path.stem}_response.md"
        )
    response_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = now_iso()
    result = subprocess.run(
        [binary, "--print-timeout", print_timeout, "-p", prompt],
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
        "started_at": started_at,
        "finished_at": now_iso(),
    }
    _write_json(BRIDGE_LOG_PATH, payload)
    if result.returncode != 0:
        raise RuntimeError(f"agy bridge call failed with exit code {result.returncode}; response written to {payload['output_file']}")
    return payload

