from __future__ import annotations

import json
from typing import Any

import jsonschema

from nrl_capabilities import build_hardening_status
from nrl_creation_schemas import (
    build_creation_schema_registry,
    validate_creation_asset_store,
)
from nrl_corpus_pipeline import build_pipeline_status
from nrl_paths import runtime_path
from nrl_research_assets import build_research_asset_catalog


STATE_PATH = runtime_path("system/mission_controller/current_phase_state.json")
STATE_SCHEMA_PATH = runtime_path("system/mission_controller/phase_state.schema.json")
ADAPTERS_PATH = runtime_path("system/runtime/agent_adapters.json")


def _load_json(path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_runtime_state() -> dict[str, Any]:
    state = _load_json(STATE_PATH)
    schema = _load_json(STATE_SCHEMA_PATH)
    try:
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(state, schema)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as error:
        return {"valid": False, "errors": [error.message]}


def run_system_check() -> dict[str, Any]:
    state = _load_json(STATE_PATH)
    adapters = _load_json(ADAPTERS_PATH)
    runtime_state = validate_runtime_state()
    hardening = build_hardening_status(state, adapters)
    research = build_research_asset_catalog()
    schemas = build_creation_schema_registry()
    store = validate_creation_asset_store()
    pipeline = build_pipeline_status(state, adapters)

    checks = [
        {
            "check_id": "runtime_state",
            "passed": runtime_state["valid"],
            "detail": runtime_state,
        },
        {
            "check_id": "capability_roadmap",
            "passed": len(hardening["capabilities"]) == 8,
            "detail": hardening["next_safe_action"],
        },
        {
            "check_id": "research_asset_catalog",
            "passed": all(
                "novel_training_set/" not in item["source_path"]
                for item in research["items"]
            ),
            "detail": research["summary"],
        },
        {
            "check_id": "creation_schemas",
            "passed": schemas["summary"]["all_schemas_valid"],
            "detail": schemas["summary"],
        },
        {
            "check_id": "creation_asset_store",
            "passed": store["valid"],
            "detail": store["summary"],
        },
        {
            "check_id": "corpus_pipeline",
            "passed": (
                pipeline["next_family"]["family"]
                in {family["family"] for family in pipeline["families"]}
            ),
            "detail": {
                "pipeline_id": pipeline["pipeline_id"],
                "next_family": pipeline["next_family"]["family"],
                "stage_count": len(pipeline["stages"]),
            },
        },
    ]
    return {
        "system": "Novel Research Lab",
        "control_plane_version": "0.2",
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
