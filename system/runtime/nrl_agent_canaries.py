from __future__ import annotations

"""No-prose provider protocol canaries. Evidence is kept separate from fiction runtime."""

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_antigravity_bridge import find_agy_binary
from nrl_hermes_bridge import ask_hermes
from nrl_paths import ROOT, runtime_path


VERSION = "0.1"
EVIDENCE_PATH = runtime_path("system/production_runtime/canaries/agent_protocol_evidence.v0.1.json")
CASE_IDS = tuple(f"protocol-{index:02d}" for index in range(1, 11))
HERMES_MODELS = ("gpt-5.6-terra", "gpt-5.6-sol", "gpt-5.6-luna")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _parse_protocol_output(text: str, agent: str, case_id: str) -> dict[str, Any]:
    candidate = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", candidate, re.DOTALL)
    if fenced:
        candidate = fenced.group(1)
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as error:
        return {"valid": False, "error": f"non_json_output: {error.msg}", "raw_preview": text[:300]}
    expected = {
        "protocol_version": VERSION,
        "agent": agent,
        "case_id": case_id,
        "status": "ok",
        "no_prose": True,
    }
    if payload != expected:
        return {"valid": False, "error": "protocol_payload_mismatch", "payload": payload}
    return {"valid": True, "payload": payload}


def _prompt(agent: str, case_id: str) -> str:
    return (
        "This is an NRL infrastructure protocol canary, not a literary task. "
        "Do not write fiction, analysis, markdown, or code fences. Return exactly one JSON object and nothing else: "
        + json.dumps({"protocol_version": VERSION, "agent": agent, "case_id": case_id, "status": "ok", "no_prose": True})
    )


def _run_hermes_case(case_id: str) -> dict[str, Any]:
    attempts = []
    for model in HERMES_MODELS:
        try:
            output = ask_hermes(_prompt("hermes", case_id), model=model, timeout_seconds=45)
        except RuntimeError as error:
            attempts.append({"model": model, "valid": False, "error": str(error)})
            continue
        parsed = _parse_protocol_output(output, "hermes", case_id)
        attempts.append({"model": model, **parsed})
        if parsed["valid"]:
            return {"case_id": case_id, "valid": True, "selected_model": model, "attempts": attempts}
    return {"case_id": case_id, "valid": False, "attempts": attempts}


def _run_antigravity_case(case_id: str) -> dict[str, Any]:
    binary = find_agy_binary()
    if not binary:
        return {"case_id": case_id, "valid": False, "error": "agy binary not found"}
    try:
        result = subprocess.run(
            [binary, "--mode", "plan", "--sandbox", "--print-timeout", "1m0s", "-p", _prompt("antigravity", case_id)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=90,
        )
    except subprocess.TimeoutExpired:
        return {"case_id": case_id, "valid": False, "error": "agy timeout after 90s"}
    text = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    if result.returncode != 0:
        return {"case_id": case_id, "valid": False, "error": f"agy exit {result.returncode}", "raw_preview": text[:300]}
    return {"case_id": case_id, **_parse_protocol_output(text, "antigravity", case_id)}


def run_agent_protocol_canaries(agent: str | None = None, case_ids: tuple[str, ...] = CASE_IDS) -> dict[str, Any]:
    """Run a resumable subset and persist each completed call before the next one."""
    if agent not in {None, "hermes", "antigravity"}:
        raise ValueError("agent must be hermes or antigravity")
    if EVIDENCE_PATH.exists():
        evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    else:
        evidence = {"version": VERSION, "mode": "no-prose protocol verification", "started_at": _now(), "hermes": [], "antigravity": []}
    agents = (agent,) if agent else ("hermes", "antigravity")
    for agent_name in agents:
        existing = {item.get("case_id"): item for item in evidence.get(agent_name, [])}
        runner = _run_hermes_case if agent_name == "hermes" else _run_antigravity_case
        for case_id in case_ids:
            existing[case_id] = runner(case_id)
            evidence[agent_name] = [existing[key] for key in CASE_IDS if key in existing]
            evidence["finished_at"] = _now()
            evidence["valid"] = False
            _write_json(EVIDENCE_PATH, evidence)
    evidence["finished_at"] = _now()
    evidence["valid"] = validate_agent_protocol_canaries_from_evidence(evidence)["valid"]
    _write_json(EVIDENCE_PATH, evidence)
    return evidence


def validate_agent_protocol_canaries_from_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    errors = []
    for agent in ("hermes", "antigravity"):
        cases = evidence.get(agent, [])
        if [item.get("case_id") for item in cases] != list(CASE_IDS):
            errors.append(f"{agent} must record all ten ordered protocol cases")
        if not all(item.get("valid") for item in cases):
            errors.append(f"{agent} has failed protocol cases")
    if evidence.get("mode") != "no-prose protocol verification":
        errors.append("canary evidence mode is invalid")
    return {"valid": not errors, "errors": errors, "evidence_path": str(EVIDENCE_PATH.relative_to(ROOT))}


def validate_agent_protocol_canaries() -> dict[str, Any]:
    if not EVIDENCE_PATH.exists():
        return {"valid": False, "errors": ["agent protocol evidence is missing"]}
    return validate_agent_protocol_canaries_from_evidence(json.loads(EVIDENCE_PATH.read_text(encoding="utf-8")))
