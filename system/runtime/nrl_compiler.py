from __future__ import annotations

import json
from typing import Any

from nrl_paths import runtime_path


FORBIDDEN_INPUT_MARKERS = {"novel_training_set/", "data/raw/", "full_corpus/"}


def reject_forbidden_inputs(paths: list[str]) -> None:
    for path in paths:
        normalized = path.replace("\\", "/")
        for marker in FORBIDDEN_INPUT_MARKERS:
            if marker in normalized:
                raise RuntimeError(f"forbidden raw research input for runtime packet: {path}")


def compile_packet(mission: dict[str, Any], packet_type: str, now: str) -> dict[str, Any]:
    reject_forbidden_inputs(mission["required_inputs"])
    packet = {
        "schema_version": "1.0",
        "packet_type": packet_type,
        "mission_id": mission["mission_id"],
        "mission_name": mission["mission_name"],
        "target_agent": mission["responsible_agent"],
        "created_at": now,
        "allowed_input_paths": mission["required_inputs"],
        "source_artifact_list": mission["required_inputs"],
        "protected_state_reads": [
            "system/mission_controller/current_phase_state.json",
            "system/mission_controller/next_mission_rules.md",
            "system/mission_controller/agent_task_contract.md",
        ],
        "must_keep_beats": [
            "Review the current mission artifact only",
            "Respect the current phase and selected project",
            "Return findings in the expected output contract",
        ],
        "must_avoid_elements": mission["blocked_actions"],
        "originality_red_lines": [
            "Do not copy source novel character paths",
            "Do not reproduce proprietary setting combinations",
            "Do not convert type tropes into recognizable source-plot replicas",
        ],
        "review_criteria": [
            "mechanism-pileup risk",
            "long-form potential",
            "protagonist fate-arc traction",
            "reader follow-through",
            "structural originality",
        ],
        "expected_output_contract": mission["expected_outputs"],
    }
    out_dir = runtime_path("system/runtime/constraint_packets")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{mission['mission_id']}_{mission['responsible_agent']}_packet.json"
    out_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    packet["packet_path"] = str(out_path.relative_to(runtime_path("")))
    return packet
