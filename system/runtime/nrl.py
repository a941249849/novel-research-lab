#!/usr/bin/env python3
"""Novel Research Lab Mission Runtime MVP.

This runtime is intentionally small: it routes missions, prepares manual
handoffs, ingests external outputs, and validates phase state. It does not call
Hermes or Antigravity directly.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_compiler import compile_packet
from nrl_doctor import run_doctor
from nrl_paths import ROOT, runtime_path
from nrl_owner_gate import load_decisions, record_owner_decision
from nrl_registry import (
    find_active_attempt,
    load_registry,
    mark_attempt_status,
    record_handoff_attempt,
    save_registry,
    upsert_registry_mission,
)
from nrl_studio import render_studio

STATE_PATH = runtime_path("system/mission_controller/current_phase_state.json")
SCHEMA_PATH = runtime_path("system/mission_controller/phase_state.schema.json")
RULES_PATH = runtime_path("system/mission_controller/next_mission_rules.md")
CONTRACT_PATH = runtime_path("system/mission_controller/agent_task_contract.md")
ADAPTERS_PATH = runtime_path("system/runtime/agent_adapters.json")
REGISTRY_PATH = runtime_path("system/runtime/mission_registry.json")

SUPPORTED_AGENTS = {"codex", "hermes", "antigravity"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_state() -> dict[str, Any]:
    return load_json(STATE_PATH)


def load_adapters() -> dict[str, Any]:
    return load_json(ADAPTERS_PATH)


def mission_id_for(name: str) -> str:
    slug = name.lower().replace("《", "").replace("》", "")
    for old, new in [
        ("phase ", "phase"),
        (" ", "_"),
        ("/", "_"),
        ("-", "_"),
        (":", ""),
    ]:
        slug = slug.replace(old, new)
    return "".join(ch for ch in slug if ch.isalnum() or ch in {"_"})


def responsible_agent_for(state: dict[str, Any], requested_agent: str | None = None) -> str:
    if requested_agent:
        agent = requested_agent.lower()
        if agent not in SUPPORTED_AGENTS:
            raise RuntimeError(f"unsupported agent: {requested_agent}")
        return agent
    allowed = [str(a).lower() for a in state.get("allowed_next_agents", [])]
    if allowed:
        return allowed[0]
    mission = state.get("next_recommended_mission", "").lower()
    if "antigravity" in mission:
        return "antigravity"
    if "hermes" in mission:
        return "hermes"
    return "codex"


def required_inputs_for(state: dict[str, Any]) -> list[str]:
    inputs = []
    for artifact in state.get("key_artifacts", []):
        path = artifact.get("path")
        if path:
            inputs.append(path)
    inputs.extend(
        [
            "system/mission_controller/current_phase_state.json",
            "system/mission_controller/next_mission_rules.md",
            "system/mission_controller/agent_task_contract.md",
        ]
    )
    return sorted(dict.fromkeys(inputs))


def expected_outputs_for(agent: str, mission_name: str) -> list[str]:
    if agent == "antigravity":
        return ["handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"]
    if agent == "hermes":
        return ["handoff/hermes/outputs/external_hermes_output.md"]
    return [f"system/runtime/{mission_id_for(mission_name)}_codex_output.md"]


def current_mission(state: dict[str, Any], agent: str | None = None) -> dict[str, Any]:
    mission_name = state.get("next_recommended_mission", "UNKNOWN_MISSION")
    responsible_agent = responsible_agent_for(state, agent)
    return {
        "mission_id": mission_id_for(mission_name),
        "mission_name": mission_name,
        "phase": state.get("current_phase", "UNKNOWN_PHASE"),
        "responsible_agent": responsible_agent,
        "required_inputs": required_inputs_for(state),
        "expected_outputs": expected_outputs_for(responsible_agent, mission_name),
        "blocked_actions": state.get("blocked_actions", []),
        "whether_owner_gate_required": state.get("owner_gate_required", False),
    }


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_status(_: argparse.Namespace) -> int:
    state = load_state()
    print_json(
        {
            "current_phase": state.get("current_phase"),
            "current_subphase": state.get("current_subphase"),
            "phase_status": state.get("phase_status"),
            "next_recommended_mission": state.get("next_recommended_mission"),
            "allowed_next_agents": state.get("allowed_next_agents", []),
            "blocked_actions": state.get("blocked_actions", []),
        }
    )
    return 0


def cmd_next(_: argparse.Namespace) -> int:
    state = load_state()
    print_json(current_mission(state))
    return 0


def cmd_missions(_: argparse.Namespace) -> int:
    print_json({"missions": load_registry()})
    return 0


def cmd_check_inputs(_: argparse.Namespace) -> int:
    state = load_state()
    mission = current_mission(state)
    rows = []
    for rel in mission["required_inputs"]:
        path = ROOT / rel
        rows.append({"path": rel, "exists": path.exists()})
    print_json({"mission_id": mission["mission_id"], "inputs": rows})
    return 0 if all(row["exists"] for row in rows) else 1


def cmd_gate_status(_: argparse.Namespace) -> int:
    state = load_state()
    print_json(
        {
            "phase_status": state.get("phase_status"),
            "validation_status": state.get("validation_status"),
            "review_status": state.get("review_status"),
            "owner_gate_required": state.get("owner_gate_required", False),
            "owner_gate_status": state.get("owner_gate_status"),
        }
    )
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    state = load_state()
    adapters = load_adapters()
    mission = current_mission(state)
    print_json(run_doctor(state, adapters, mission))
    return 0


def cmd_owner_gate_record(args: argparse.Namespace) -> int:
    decision = {
        "decision_id": args.decision_id,
        "decision_type": args.decision_type,
        "authorized_scope": args.authorized_scope,
        "forbidden_scope": args.forbidden_scope,
        "expires_after_mission": args.expires_after_mission,
        "owner_note": args.owner_note,
    }
    print_json(record_owner_decision(decision, now_iso()))
    return 0


def cmd_owner_gate_list(_: argparse.Namespace) -> int:
    print_json({"decisions": load_decisions()})
    return 0


def cmd_compile_context(args: argparse.Namespace) -> int:
    state = load_state()
    mission = current_mission(state, args.agent)
    packet = compile_packet(mission, "review" if args.agent == "antigravity" else "creative", now_iso())
    print_json(
        {
            "packet_path": packet["packet_path"],
            "mission_id": mission["mission_id"],
            "target_agent": mission["responsible_agent"],
        }
    )
    return 0


def cmd_studio_build(_: argparse.Namespace) -> int:
    path = render_studio()
    print_json({"studio_path": str(path.relative_to(ROOT))})
    return 0


def make_handoff_markdown(mission: dict[str, Any], adapter: dict[str, Any]) -> str:
    can_execute = str(adapter.get("can_execute", False)).lower()
    required_inputs = "\n".join(f"- {x}" for x in mission["required_inputs"])
    expected_outputs = "\n".join(f"- {x}" for x in mission["expected_outputs"])
    blocked_actions = "\n".join(f"- {x}" for x in mission["blocked_actions"])
    return f"""# Novel Research Lab Agent Handoff

## Mission

- mission_id: {mission["mission_id"]}
- mission_name: {mission["mission_name"]}
- phase: {mission["phase"]}
- responsible_agent: {mission["responsible_agent"]}
- adapter_mode: {adapter.get("mode")}
- adapter_can_execute: {can_execute}
- owner_gate_required: {mission["whether_owner_gate_required"]}

## Required Inputs

{required_inputs}

## Expected Outputs

{expected_outputs}

## Blocked Actions

{blocked_actions}

## Runtime Instruction

This handoff is for manual external-agent execution. The runtime has not called the agent. Place the completed external output in the expected output directory, then run:

```text
python3 system/runtime/nrl.py ingest --agent {mission["responsible_agent"]} --file <path>
```
"""


def cmd_prepare_handoff(args: argparse.Namespace) -> int:
    agent = args.agent.lower()
    state = load_state()
    adapters = load_adapters()
    if agent not in adapters:
        raise RuntimeError(f"agent not configured: {agent}")
    mission = current_mission(state, agent)
    adapter = adapters[agent]
    handoff_dir = ROOT / adapter.get("handoff_dir", f"handoff/{agent}")
    output_dir = ROOT / adapter.get("expected_output_dir", f"handoff/{agent}/outputs")
    handoff_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = handoff_dir / "current_task.md"
    handoff_path.write_text(make_handoff_markdown(mission, adapter), encoding="utf-8")
    attempt = record_handoff_attempt(mission, str(adapter.get("mode")), now_iso())
    print_json(
        {
            "handoff_path": str(handoff_path.relative_to(ROOT)),
            "status": "awaiting_external_output",
            "handoff_attempt_id": attempt["handoff_attempt_id"],
        }
    )
    return 0


def update_state_for_ingest(agent: str, output_path: str) -> None:
    state = load_state()
    if agent == "hermes":
        state["phase_status"] = "output_received_pending_validation"
        state["validation_status"] = "PENDING"
    elif agent == "antigravity":
        state["phase_status"] = "review_received_pending_owner_gate"
        state["review_status"] = "REVIEW_RECEIVED_PENDING_OWNER_GATE"
        state["owner_gate_required"] = True
        state["owner_gate_status"] = "REQUIRED_PENDING_ACKNOWLEDGEMENT"
    notes = state.setdefault("notes", [])
    note = f"Runtime ingest: {agent} external output registered at {output_path}."
    if note not in notes:
        notes.append(note)
    state["updated_at"] = now_iso()
    write_json(STATE_PATH, state)


def cmd_ingest(args: argparse.Namespace) -> int:
    agent = args.agent.lower()
    if agent not in {"hermes", "antigravity"}:
        raise RuntimeError("ingest supports only hermes or antigravity")
    file_path = Path(args.file)
    if not file_path.is_absolute():
        file_path = (ROOT / file_path).resolve()
    else:
        file_path = file_path.resolve()
    if not file_path.exists():
        raise RuntimeError(f"ingest file does not exist: {file_path}")
    state = load_state()
    mission = current_mission(state, agent)
    rel_file = str(file_path.relative_to(ROOT)) if file_path.is_relative_to(ROOT) else str(file_path)
    expected_outputs = set(mission["expected_outputs"])
    if rel_file not in expected_outputs:
        raise RuntimeError(f"ingest file is not an expected output for this mission: {rel_file}")
    attempt = find_active_attempt(mission["mission_id"], rel_file)
    if attempt is None:
        raise RuntimeError(f"no active handoff attempt for expected output: {rel_file}")
    mark_attempt_status(mission["mission_id"], attempt["handoff_attempt_id"], "output_detected", now_iso())
    status = "output_detected"
    upsert_registry_mission(mission, status, [f"{agent} output ingested from {rel_file}"], now_iso())
    registry = load_registry()
    for item in registry:
        if item.get("mission_id") == mission["mission_id"] and rel_file not in item["output_artifacts"]:
            item["output_artifacts"].append(rel_file)
            item["updated_at"] = now_iso()
    save_registry(registry)
    update_state_for_ingest(agent, rel_file)
    print_json({"ingested": rel_file, "agent": agent, "registry_status": status})
    return 0


def cmd_validate_state(_: argparse.Namespace) -> int:
    schema = load_json(SCHEMA_PATH)
    state = load_state()
    try:
        import jsonschema  # type: ignore

        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(state, schema)
        print_json({"state_valid_against_schema": True, "validator": "jsonschema"})
        return 0
    except ModuleNotFoundError:
        missing = [key for key in schema.get("required", []) if key not in state]
        ok = not missing
        print_json({"state_valid_against_schema": ok, "validator": "required-fields-fallback", "missing": missing})
        return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Novel Research Lab Mission Runtime MVP")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("next").set_defaults(func=cmd_next)
    sub.add_parser("missions").set_defaults(func=cmd_missions)
    sub.add_parser("check-inputs").set_defaults(func=cmd_check_inputs)
    sub.add_parser("gate-status").set_defaults(func=cmd_gate_status)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)
    owner = sub.add_parser("owner-gate")
    owner_sub = owner.add_subparsers(dest="owner_gate_command", required=True)
    owner_record = owner_sub.add_parser("record")
    owner_record.add_argument("--decision-id", required=True)
    owner_record.add_argument(
        "--decision-type",
        required=True,
        choices=["accept_review", "request_rework", "authorize_next_phase", "authorize_adapter_upgrade"],
    )
    owner_record.add_argument("--authorized-scope", action="append", required=True)
    owner_record.add_argument("--forbidden-scope", action="append", required=True)
    owner_record.add_argument("--expires-after-mission", required=True)
    owner_record.add_argument("--owner-note", default="")
    owner_record.set_defaults(func=cmd_owner_gate_record)
    owner_sub.add_parser("list").set_defaults(func=cmd_owner_gate_list)
    compile_context = sub.add_parser("compile-context")
    compile_context.add_argument("--agent", required=True, choices=["hermes", "antigravity"])
    compile_context.set_defaults(func=cmd_compile_context)
    sub.add_parser("studio-build").set_defaults(func=cmd_studio_build)
    prepare = sub.add_parser("prepare-handoff")
    prepare.add_argument("--agent", required=True, choices=["hermes", "antigravity"])
    prepare.set_defaults(func=cmd_prepare_handoff)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("--agent", required=True, choices=["hermes", "antigravity"])
    ingest.add_argument("--file", required=True)
    ingest.set_defaults(func=cmd_ingest)
    sub.add_parser("validate-state").set_defaults(func=cmd_validate_state)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
