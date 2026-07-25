from __future__ import annotations

"""Isolated model adapters. They have no filesystem authority over NRL."""

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_TIMEOUT_SECONDS = 300
DEFAULT_ANTIGRAVITY_TIMEOUT_SECONDS = 600
DEFAULT_OPENCODE_TIMEOUT_SECONDS = 600
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


def _provider_error_detail(stderr: str, stdout: str = "") -> str:
    """Keep actionable provider errors without persisting prompts or warning floods."""
    raw = (stderr or stdout).strip()
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    actionable = [
        line for line in lines
        if re.search(r"(?:^|\s)(?:ERROR|FATAL):|usage limit|rate limit|timed out|quota", line, re.IGNORECASE)
    ]
    selected = actionable[-3:] if actionable else lines[-3:]
    detail = " | ".join(selected)
    return detail[:1600] or "provider returned no diagnostic"


def _codex_response_schema(value: Any) -> Any:
    """Remove Draft-07 keywords unsupported by Codex response schemas.

    The untouched source schema is still used for local validation after the
    model returns, so provider compatibility does not weaken NRL's contract.
    """
    if isinstance(value, dict):
        compatible = {
            key: _codex_response_schema(item)
            for key, item in value.items()
            if key != "uniqueItems"
        }
        properties = compatible.get("properties")
        if compatible.get("type") == "object" and isinstance(properties, dict):
            compatible["required"] = list(properties)
        return compatible
    if isinstance(value, list):
        return [_codex_response_schema(item) for item in value]
    return value


def ask_codex_writer(prompt: str, *, model: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    global _CODEX_USAGE_LIMITED
    binary = find_codex_binary()
    if not binary:
        raise RuntimeError("codex CLI is missing")
    with tempfile.TemporaryDirectory(prefix="nrl-codex-writer-") as temp_dir:
        output = Path(temp_dir) / "writer-output.md"
        try:
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
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(f"Codex writer timed out after {timeout_seconds} seconds") from error
        if result.returncode != 0 or not output.is_file():
            detail = _provider_error_detail(result.stderr, result.stdout)
            error = f"Codex writer failed with exit code {result.returncode}: {detail}"
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
        provider_schema = schema_path
        if schema_path.is_file():
            provider_schema = Path(temp_dir) / "provider-schema.json"
            provider_schema.write_text(
                json.dumps(
                    _codex_response_schema(json.loads(schema_path.read_text(encoding="utf-8"))),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        try:
            result = subprocess.run(
                [
                    binary, "--ask-for-approval", "never", "exec", "--ephemeral",
                    "--skip-git-repo-check", "--sandbox", "read-only", "-m", model,
                    "--output-schema", str(provider_schema), "-o", str(output), prompt,
                ],
                cwd=temp_dir,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(f"Codex structured call timed out after {timeout_seconds} seconds") from error
        if result.returncode != 0 or not output.is_file():
            detail = _provider_error_detail(result.stderr, result.stdout)
            error = f"Codex structured call failed with exit code {result.returncode}: {detail}"
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
        detail = _provider_error_detail(result.stderr, result.stdout)
        raise RuntimeError(f"Antigravity writer failed with exit code {result.returncode}: {detail}")
    text = result.stdout.strip()
    if not text:
        raise RuntimeError("Antigravity writer returned empty output")
    return text


def ask_opencode_writer(
    prompt: str,
    *,
    model: str = "qwen3.7-max",
    timeout_seconds: int = DEFAULT_OPENCODE_TIMEOUT_SECONDS,
) -> str:
    """Run an isolated OpenCode Go call through the repository's no-tools adapter."""
    node = shutil.which("node")
    script = Path(__file__).with_name("opencode_direct.mjs")
    if not node or not script.is_file():
        raise RuntimeError("OpenCode direct runtime is unavailable")
    with tempfile.TemporaryDirectory(prefix="nrl-opencode-writer-") as temp_dir:
        request = Path(temp_dir) / "request.md"
        source = Path(temp_dir) / "source.md"
        request.write_text(prompt, encoding="utf-8")
        source.write_text("", encoding="utf-8")
        try:
            result = subprocess.run(
                [node, str(script), str(request), str(source), model],
                cwd=temp_dir,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(
                f"OpenCode writer timed out after {timeout_seconds} seconds"
            ) from error
    if result.returncode != 0:
        detail = _provider_error_detail(result.stderr, result.stdout)
        raise RuntimeError(
            f"OpenCode writer failed with exit code {result.returncode}: {detail}"
        )
    text = result.stdout.strip()
    if not text:
        raise RuntimeError("OpenCode writer returned empty output")
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
