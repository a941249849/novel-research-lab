from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from nrl_antigravity_bridge import find_agy_binary
from nrl_deep_read import build_deep_read_status
from nrl_paths import ROOT, runtime_path


VERSION = "0.19"
JOB_ID = "job-v019-borrowed-heaven-project-reconciliation"
PACKET_PATH = runtime_path("system/agent_ops/packets/borrowed_heaven_project_reconciliation_v0.19.md")
RESPONSE_PATH = runtime_path("system/agent_ops/inbox/borrowed_heaven_project_reconciliation_v0.19.json")
VALIDATION_PATH = runtime_path("system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json")
INPUTS = (
    "system/agent_ops/inbox/deep_read_v0.18/cross_book_distillation.json",
    "phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md",
    "phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md",
    "system/creation_assets/project_assets.v0.2.json",
    "system/agent_ops/inbox/hermes-controlled-prose-test-v016.md",
    "system/agent_ops/inbox/antigravity-controlled-prose-audit-v016.md",
    "system/agent_ops/inbox/antigravity-volume1-assets-audit-v017.md",
)


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_project_reconciliation_packet() -> dict[str, Any]:
    deep_read = build_deep_read_status()
    if not deep_read["deep_read_verified"]:
        raise RuntimeError("v0.18 deep reading must be verified before project reconciliation")
    inputs = []
    for relative in INPUTS:
        path = runtime_path(relative)
        if not path.exists():
            raise RuntimeError(f"project reconciliation input is missing: {relative}")
        inputs.append({"path": relative, "sha256": _sha256(path)})
    template = {
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "project": "《借天改命账》",
        "input_hashes": inputs,
        "verdict": "ACCEPT_WITH_WARNINGS",
        "assessments": {
            "long_form_vitality": [],
            "plot_logic": [],
            "character_and_emotional_life": [],
            "anti_ai_prose": [],
            "asset_and_state_consistency": [],
            "originality": [],
        },
        "keep": [],
        "required_changes": [],
        "rejected_source_influences": [],
        "asset_patch_candidates": [],
        "volume1_production_recommendation": "",
    }
    PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKET_PATH.write_text(
        "\n".join(
            [
                "# NRL Project Reconciliation v0.19", "",
                "Independently review the current project against the newly verified full-corpus distillation.",
                "Read every input below. Preserve original project identity; do not maximize the number of borrowed mechanisms.",
                "Assess long-form vitality, plot causality, character life, AI-taste risk, asset/state consistency, and originality separately.",
                "Do not write novel prose. Return one JSON object only.", "",
                *[f"- `{item['path']}` sha256 `{item['sha256']}`" for item in inputs], "",
                "Copy all binding fields exactly and fill every array with evidence-backed findings:", "```json",
                json.dumps(template, ensure_ascii=False, indent=2), "```", "",
            ]
        ),
        encoding="utf-8",
    )
    return {"version": VERSION, "job_id": JOB_ID, "packet_path": _relative(PACKET_PATH), "response_path": _relative(RESPONSE_PATH), "input_hashes": inputs}


def validate_project_reconciliation_response(
    data: dict[str, Any], expected_inputs: list[dict[str, str]]
) -> dict[str, Any]:
    errors = []
    if data.get("job_id") != JOB_ID:
        errors.append("job_id mismatch")
    if data.get("contract_version") != VERSION:
        errors.append("contract_version mismatch")
    if data.get("project") != "《借天改命账》":
        errors.append("project mismatch")
    if data.get("input_hashes") != expected_inputs:
        errors.append("input_hashes mismatch")
    if data.get("verdict") not in {"ACCEPT", "ACCEPT_WITH_WARNINGS", "REWORK_REQUIRED"}:
        errors.append("verdict is invalid")
    assessments = data.get("assessments")
    required_assessments = {
        "long_form_vitality", "plot_logic", "character_and_emotional_life",
        "anti_ai_prose", "asset_and_state_consistency", "originality",
    }
    if not isinstance(assessments, dict) or set(assessments) != required_assessments:
        errors.append("assessments must contain all six quality dimensions")
    elif any(not isinstance(value, list) or not value for value in assessments.values()):
        errors.append("every quality assessment must be non-empty")
    for field in ("keep", "required_changes", "rejected_source_influences", "asset_patch_candidates"):
        if not isinstance(data.get(field), list):
            errors.append(f"{field} must be an array")
    if not data.get("volume1_production_recommendation"):
        errors.append("volume1_production_recommendation is required")
    return {"valid": not errors, "errors": errors, "verdict": data.get("verdict")}


def validate_project_reconciliation() -> dict[str, Any]:
    packet = build_project_reconciliation_packet()
    if not RESPONSE_PATH.exists():
        result = {"valid": False, "errors": ["project reconciliation response is missing"]}
    else:
        try:
            data = json.loads(RESPONSE_PATH.read_text(encoding="utf-8").strip().removeprefix("```json").removesuffix("```").strip())
        except json.JSONDecodeError as error:
            result = {"valid": False, "errors": [f"invalid response JSON: {error}"]}
        else:
            result = validate_project_reconciliation_response(data, packet["input_hashes"])
    result = {"version": VERSION, "job_id": JOB_ID, **result}
    _write_json(VALIDATION_PATH, result)
    return result


def dispatch_project_reconciliation(
    model: str = "Gemini 3.5 Flash (High)", print_timeout: str = "15m0s"
) -> dict[str, Any]:
    packet = build_project_reconciliation_packet()
    binary = find_agy_binary()
    if not binary:
        raise RuntimeError("agy binary is missing")
    result = subprocess.run(
        [binary, "--model", model, "--mode", "plan", "--sandbox", "--print-timeout", print_timeout, "-p", PACKET_PATH.read_text(encoding="utf-8")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    RESPONSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESPONSE_PATH.write_text(result.stdout, encoding="utf-8")
    validation = validate_project_reconciliation()
    return {"returncode": result.returncode, "stderr": result.stderr.strip(), "validation": validation, **packet}
