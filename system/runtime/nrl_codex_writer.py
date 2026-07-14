from __future__ import annotations

"""Isolated model adapters. They have no filesystem authority over NRL."""

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_TIMEOUT_SECONDS = 180
DEFAULT_ANTIGRAVITY_TIMEOUT_SECONDS = 600
_CODEX_USAGE_LIMITED = False


def find_codex_binary() -> str | None:
    return shutil.which("codex")


def find_antigravity_binary() -> str | None:
    return shutil.which("agy") or shutil.which(str(Path.home() / ".local/bin/agy"))


def codex_usage_limited() -> bool:
    return _CODEX_USAGE_LIMITED


def _is_usage_limit_error(text: str) -> bool:
    lowered = text.lower()
    return "usage limit" in lowered or "hit your usage" in lowered


def ask_codex_writer(prompt: str, *, model: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    global _CODEX_USAGE_LIMITED
    binary = find_codex_binary()
    if not binary:
        raise RuntimeError("codex CLI is missing")
    with tempfile.TemporaryDirectory(prefix="nrl-codex-writer-") as temp_dir:
        output = Path(temp_dir) / "writer-output.md"
        result = subprocess.run(
            [
                binary, "--ask-for-approval", "never", "exec", "--ephemeral", "--skip-git-repo-check",
                "--sandbox", "read-only", "-m", model, "-o", str(output), prompt,
            ],
            cwd=temp_dir,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        if result.returncode != 0 or not output.is_file():
            error = f"Codex writer failed with exit code {result.returncode}: {result.stderr.strip()}"
            if _is_usage_limit_error(error):
                _CODEX_USAGE_LIMITED = True
            raise RuntimeError(error)
        text = output.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("Codex writer returned empty output")
    return text


def ask_codex_structured(
    prompt: str,
    *,
    model: str,
    schema_path: Path,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Run one schema-bound Codex call and return its JSON object."""
    global _CODEX_USAGE_LIMITED
    binary = find_codex_binary()
    if not binary:
        raise RuntimeError("codex CLI is missing")
    with tempfile.TemporaryDirectory(prefix="nrl-codex-structured-") as temp_dir:
        output = Path(temp_dir) / "output.json"
        result = subprocess.run(
            [
                binary, "--ask-for-approval", "never", "exec", "--ephemeral",
                "--skip-git-repo-check", "--sandbox", "read-only", "-m", model,
                "--output-schema", str(schema_path), "-o", str(output), prompt,
            ],
            cwd=temp_dir,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        if result.returncode != 0 or not output.is_file():
            error = f"Codex structured call failed with exit code {result.returncode}: {result.stderr.strip()}"
            if _is_usage_limit_error(error):
                _CODEX_USAGE_LIMITED = True
            raise RuntimeError(error)
        try:
            payload = json.loads(output.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Codex structured call returned invalid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise RuntimeError("Codex structured call must return one JSON object")
    return payload


def ask_antigravity_writer(
    prompt: str,
    *,
    model: str,
    timeout_seconds: int = DEFAULT_ANTIGRAVITY_TIMEOUT_SECONDS,
) -> str:
    binary = find_antigravity_binary()
    if not binary:
        raise RuntimeError("Antigravity CLI is missing")
    contract = (
        "你是 NRL 的隔离生产 Agent。不得使用工具、读取或写入文件、执行命令或解释过程。"
        "严格按任务要求直接返回最终内容，不要前言、Markdown 围栏或后记。\n\n"
    )
    with tempfile.TemporaryDirectory(prefix="nrl-antigravity-writer-") as temp_dir:
        result = subprocess.run(
            [
                binary,
                "--mode", "plan",
                "--sandbox",
                "--print-timeout", f"{max(1, timeout_seconds // 60)}m0s",
                "--model", model,
                "-p", contract + prompt,
            ],
            cwd=temp_dir,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds + 30,
        )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Antigravity writer failed with exit code {result.returncode}: {detail}")
    text = result.stdout.strip()
    if not text:
        raise RuntimeError("Antigravity writer returned empty output")
    return text


def extract_json_object(text: str) -> dict[str, Any]:
    candidate = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", candidate, re.DOTALL | re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start < 0 or end <= start:
            raise RuntimeError("model response does not contain a JSON object")
        try:
            payload = json.loads(candidate[start : end + 1])
        except json.JSONDecodeError as error:
            raise RuntimeError(f"model returned invalid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise RuntimeError("model response must be one JSON object")
    return payload
