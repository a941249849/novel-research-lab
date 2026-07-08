from __future__ import annotations

from pathlib import Path
from typing import Any

from nrl_paths import ROOT


FORBIDDEN_SOURCE_MARKERS = ("novel_training_set/", "data/raw/", "full_corpus/")


def _safe_text(path: Path) -> str:
    if not path.exists():
        return "[MISSING]"
    if not path.is_file():
        return "[NOT A FILE]"
    return _sanitize_for_packet(path.read_text(encoding="utf-8", errors="replace"))


def _sanitize_for_packet(text: str) -> str:
    sanitized = text
    for marker in FORBIDDEN_SOURCE_MARKERS:
        sanitized = sanitized.replace(marker, "[raw source corpus]/")
    return "\n".join(line.rstrip() for line in sanitized.splitlines())


def _assert_safe_artifact_path(relative_path: str) -> None:
    normalized = relative_path.replace("\\", "/")
    for marker in FORBIDDEN_SOURCE_MARKERS:
        if marker in normalized:
            raise RuntimeError(f"handoff packet cannot include raw source path: {relative_path}")


def render_antigravity_packet(mission: dict[str, Any]) -> str:
    for relative_path in mission["required_inputs"]:
        _assert_safe_artifact_path(relative_path)

    blocked = "\n".join(f"- {_sanitize_for_packet(str(item))}" for item in mission["blocked_actions"])
    outputs = "\n".join(f"- {item}" for item in mission["expected_outputs"])
    artifact_sections = []
    for relative_path in mission["required_inputs"]:
        text = _safe_text(ROOT / relative_path)
        artifact_sections.append(
            f"### {relative_path}\n\n"
            "```text\n"
            f"{text}\n"
            "```\n"
        )

    artifacts = "\n".join(artifact_sections)
    return f"""# Novel Research Lab Antigravity Review Packet

## Mission Contract

- mission_id: {mission["mission_id"]}
- mission_name: {mission["mission_name"]}
- phase: {mission["phase"]}
- responsible_agent: {mission["responsible_agent"]}

## Review Task

Review the current mission artifacts for {mission["mission_name"]} as an external
heterogeneous literary reviewer. Focus on structural soundness, originality risk,
pacing risk, contradiction risk, warning integration, and whether the current
plan is ready for Owner Gate. Do not write novel prose.

## Expected Output

Write one markdown report to:

{outputs}

The report must include:

- verdict: pass, pass_with_warnings, hold, or fail
- major risks
- required fixes before prose
- optional recommendations
- Owner Gate recommendation

## Blocked Actions

{blocked}

## Source Artifacts

{artifacts}
"""


def write_antigravity_packet(mission: dict[str, Any], handoff_dir: Path) -> Path:
    packet_path = handoff_dir / "current_packet.md"
    packet_path.write_text(render_antigravity_packet(mission), encoding="utf-8")
    return packet_path
