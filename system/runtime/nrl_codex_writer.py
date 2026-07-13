from __future__ import annotations

"""Direct Codex writer adapter. It has no filesystem authority over NRL."""

import shutil
import subprocess
import tempfile
from pathlib import Path


DEFAULT_TIMEOUT_SECONDS = 180


def find_codex_binary() -> str | None:
    return shutil.which("codex")


def ask_codex_writer(prompt: str, *, model: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
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
            raise RuntimeError(f"Codex writer failed with exit code {result.returncode}: {result.stderr.strip()}")
        text = output.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("Codex writer returned empty output")
    return text
