from __future__ import annotations

import json
from typing import Any

import jsonschema

from nrl_architecture import build_architecture_reconciliation
from nrl_capabilities import build_hardening_status
from nrl_creation_schemas import (
    build_creation_schema_registry,
    validate_creation_asset_store,
)
from nrl_corpus_pipeline import build_evidence_pack_matrix, build_pipeline_status
from nrl_deep_read import build_deep_read_status
from nrl_paths import runtime_path
from nrl_production_runtime import build_production_readiness
from nrl_production_calibration import build_model_team_attestation_status
from nrl_production_operator import build_operator_status
from nrl_story_window import build_story_window_status
from nrl_system_status import build_system_status
from nrl_rag_index import load_or_build_creation_context_index
from nrl_research_assets import build_research_asset_catalog


STATE_PATH = runtime_path("system/mission_controller/current_phase_state.json")
STATE_SCHEMA_PATH = runtime_path("system/mission_controller/phase_state.schema.json")
ADAPTERS_PATH = runtime_path("system/runtime/agent_adapters.json")
SOURCE_OWNERSHIP_PATH = runtime_path("system/control_plane/source_ownership.v0.20.json")


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
    evidence_matrix = build_evidence_pack_matrix(state, adapters)
    # The evidence-pack matrix is rebuilt above; the context index itself is a
    # materialized read-only artifact and should not be regenerated on every
    # health request. This keeps the allowlisted Studio action responsive.
    creation_context = load_or_build_creation_context_index(state, adapters)
    architecture = build_architecture_reconciliation(
        state,
        adapters,
        pipeline_status=pipeline,
    )
    deep_read = build_deep_read_status()
    production_runtime = build_production_readiness()
    model_team_attestation = build_model_team_attestation_status()
    system_status = build_system_status(state, adapters)
    story_windows = build_story_window_status()
    source_ownership = _load_json(SOURCE_OWNERSHIP_PATH)
    operator = build_operator_status(
        runtime_path("system/production_runtime/chapter_registry.v0.20.json")
    )
    ownership_domains = [item.get("domain") for item in source_ownership.get("domains", [])]
    architecture_payload = json.dumps(architecture, ensure_ascii=False)
    architecture_passed = (
        architecture["version"] == "0.4"
        and len(architecture["architecture_layers"]) == 10
        and architecture["architecture_layers"][6]["layer_id"] == "planning_pipeline"
        and architecture["architecture_layers"][6]["child_implementation"]
        == "corpus_pipeline_v0.3"
        and not architecture["production_readiness"]["owner_gate_required"]
        and architecture["production_readiness"]["content_generation_allowed"]
        and architecture["production_readiness"]["codex_model_team_contract_valid"]
        and "novel_training_set/" not in architecture_payload
    )

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
        {
            "check_id": "evidence_pack_matrix",
            "passed": (
                evidence_matrix["family_count"] == 9
                and evidence_matrix["valid_family_count"] == 9
                and not evidence_matrix["content_generation_allowed"]
                and not evidence_matrix["external_agent_execution_allowed"]
            ),
            "detail": {
                "matrix_id": evidence_matrix["matrix_id"],
                "family_count": evidence_matrix["family_count"],
                "valid_family_count": evidence_matrix["valid_family_count"],
                "invalid_families": evidence_matrix["invalid_families"],
            },
        },
        {
            "check_id": "creation_context_index",
            "passed": (
                creation_context["summary"]["family_count"] == 9
                and creation_context["summary"]["total_items"] >= 27
                and not creation_context["content_generation_allowed"]
                and not creation_context["external_agent_execution_allowed"]
            ),
            "detail": creation_context["summary"],
        },
        {
            "check_id": "source_ownership",
            "passed": (
                source_ownership.get("version") == "1.0"
                and len(ownership_domains) == len(set(ownership_domains)) == 9
            ),
            "detail": {
                "version": source_ownership.get("version"),
                "domain_count": len(ownership_domains),
                "duplicate_domains": sorted(
                    domain for domain in set(ownership_domains) if ownership_domains.count(domain) > 1
                ),
            },
        },
        {
            "check_id": "production_chapter_runtime",
            "passed": (
                production_runtime["checks"]["chapter_runtime_contract_ready"]
                and story_windows["valid"]
            ),
            "detail": {
                "status": production_runtime["status"],
                "ready": production_runtime["ready"],
                "stage_count": len(production_runtime["stage_order"]),
                "story_windows": story_windows,
            },
        },
        {
            "check_id": "codex_model_team_attestation",
            "passed": model_team_attestation["valid"],
            "blocking_scope": "production_readiness",
            "detail": model_team_attestation,
        },
        {
            "check_id": "production_output_gate",
            "passed": operator["valid"] and not operator.get("blocking_window_review"),
            "blocking_scope": "production_readiness",
            "detail": {
                "accepted_contiguous": operator["accepted_contiguous"],
                "blocking_window_review": operator.get("blocking_window_review"),
                "blocking_window_verdict": operator.get("blocking_window_verdict"),
                "accepted_release_ready_count": operator["accepted_release_ready_count"],
            },
        },
        {
            "check_id": "cross_domain_invariants",
            "passed": (
                system_status["production_ready"]
                and not system_status["production_blockers"]
                and state.get("owner_gate_required") is False
                and "write novel prose" not in state.get("blocked_actions", [])
                and story_windows["valid"]
            ),
            "detail": {
                "production_checks": system_status["production_checks"],
                "production_blockers": system_status["production_blockers"],
                "story_window_count": story_windows["window_count"],
            },
        },
        {
            "check_id": "verifiable_deep_reading",
            "passed": deep_read["deep_read_verified"],
            "blocking_scope": "production_readiness",
            "detail": {
                "status": deep_read["status"],
                "deep_read_verified": deep_read["deep_read_verified"],
                "legacy_v08_effective_status": deep_read["legacy_v08_effective_status"],
                "required_chunk_count": deep_read["required_chunk_count"],
            },
        },
        {
            "check_id": "architecture_reconciliation",
            "passed": architecture_passed,
            "detail": {
                "version": architecture["version"],
                "layer_count": len(architecture["architecture_layers"]),
                "pipeline_layer": architecture["implementation_alignment"][
                    "pipeline_layer"
                ],
            },
        },
    ]
    integrity_checks = [
        check for check in checks if check.get("blocking_scope") != "production_readiness"
    ]
    return {
        "system": "Novel Research Lab",
        "control_plane_version": "0.2",
        "passed": all(check["passed"] for check in integrity_checks),
        "production_ready": all(check["passed"] for check in checks),
        "checks": checks,
    }
