#!/usr/bin/env python3
"""Novel Research Lab Mission Runtime MVP.

This runtime is intentionally small: it routes missions, prepares bounded
handoffs, dispatches registered Antigravity review jobs through the local CLI
bridge, ingests outputs, and validates phase state. It never calls Hermes.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_compiler import compile_packet
from nrl_architecture import build_architecture_reconciliation
from nrl_agent_ops import (
    build_production_runtime_status,
    dispatch_agent_job,
    ingest_agent_output,
    load_job_queue,
    plan_agent_job,
    validate_agent_job,
    write_agent_packet,
)
from nrl_antigravity_bridge import ask_antigravity, build_antigravity_bridge_status
from nrl_asset_producers import (
    build_producer_status,
    produce_artifact_seed,
    produce_npc_seed,
    produce_naming_seed,
    produce_emotional_bond_seed,
    produce_foreshadowing_seed,
    produce_character_seed,
    produce_faction_seed,
    produce_state_ledger_seed,
    produce_technique_candidates,
)
from nrl_capabilities import build_hardening_status
from nrl_creation_assets import (
    build_creation_asset_graph_status,
    load_creation_asset_registry,
)
from nrl_creation_schemas import (
    build_creation_schema_registry,
    validate_creation_asset_store,
)
from nrl_corpus_pipeline import (
    build_evidence_pack,
    build_evidence_pack_matrix,
    build_pipeline_plan,
    build_pipeline_status,
    load_evidence_pack,
    validate_all_evidence_packs,
    validate_evidence_pack,
    write_evidence_pack,
    write_evidence_pack_matrix,
)
from nrl_corpus_ingestion import write_promoted_review_assets
from nrl_dna_registry import load_or_build_dna_registry, write_dna_registry
from nrl_deep_read import (
    build_promotion_attestation,
    build_deep_read_plan,
    build_deep_read_status,
    build_book_synthesis_packets,
    build_cross_book_packet,
    dispatch_pending_chunks,
    dispatch_book_syntheses,
    dispatch_cross_book_distillation,
    validate_all_chunks,
    validate_book_syntheses,
    validate_cross_book_distillation,
    validate_chunk_response,
)
from nrl_doctor import run_doctor
from nrl_full_corpus_handoff import (
    build_full_corpus_status,
    ingest_full_corpus_output,
    validate_full_corpus_output,
    write_full_corpus_packet,
)
from nrl_full_corpus_proof import (
    build_proof_status,
    merge_proof_receipts,
    promote_verified_proof,
    validate_proof_file,
    write_proof_packets,
)
from nrl_final_assets import promote_final_asset_bundle, validate_final_asset_bundle
from nrl_handoff_packet import write_antigravity_packet
from nrl_hermes_bridge import build_hermes_execution_status
from nrl_hermes_controlled_prose import (
    AUDIT_PATH,
    OUTPUT_PATH as CONTROLLED_PROSE_OUTPUT_PATH,
    build_controlled_prose_prompt,
    build_controlled_prose_readiness,
    dispatch_controlled_prose_test,
    validate_controlled_prose_text,
)
from nrl_hermes_gate import build_hermes_readiness
from nrl_paths import ROOT, runtime_path
from nrl_owner_gate import DECISION_TYPES, load_decisions, record_owner_decision
from nrl_phase2e import (
    latest_phase2e_acceptance,
    prepare_phase2e_controlled_planning_output,
    prepare_phase2e_controlled_planning_validation,
    prepare_phase2e_entry,
    prepare_phase2e_planning_package,
)
from nrl_project_reconciliation import (
    apply_project_reconciliation,
    build_project_reconciliation_packet,
    dispatch_project_reconciliation,
    validate_project_reconciliation,
)
from nrl_production_runtime import (
    accept_chapter,
    analyze_prose_metrics,
    build_production_readiness,
    build_production_preflight,
    compile_chapter_context,
    dispatch_chapter_audit,
    dispatch_chapter_draft,
    dispatch_chapter_observation,
    dispatch_chapter_revision,
    ingest_chapter_observation,
    ingest_chapter_audit,
    ingest_chapter_revision,
    initialize_chapter,
    load_chapter_runtime_status,
    quarantine_unaccepted_chapter,
    settle_chapter_state,
    build_observed_settlement_candidate,
    run_controlled_chapter_pipeline,
)
from nrl_artifact_retention import build_compaction_plan, compact_accepted_chapters
from nrl_production_operator import build_operator_status
from nrl_volume1_plan import (
    build_volume1_dry_run,
    validate_initial_state_contract,
    validate_volume1_manifest,
    write_volume1_production_contracts,
)
from nrl_agent_canaries import run_agent_protocol_canaries, validate_agent_protocol_canaries
from nrl_model_router import build_model_routing_status
from nrl_production_calibration import (
    build_blind_review_packet,
    build_calibration_routing_decision_packet,
    build_direct_writer_calibration_status,
    record_external_review_blocked,
    record_calibration_routing_decision,
    run_direct_writer_calibration,
    run_internal_calibration_screen,
)
from nrl_longform_plan import (
    write_longform_candidate_contracts,
    build_longform_contract,
    build_first100_manifest,
    validate_longform_contract,
    validate_first100_manifest,
    build_first100_guard_config,
    validate_first100_guard_config,
    build_longform_readiness,
    promote_longform_blueprint,
    build_longform_first100_dry_run,
)
from nrl_longform_cluster1 import write_cluster1_intents
from nrl_volume1_longform import write_volume1_intents, build_volume1_manifest, validate_volume1_manifest
from nrl_volume1_release import build_release_readiness, build_fanqie_upload_package, build_review_manuscript, build_window_review_packet, record_window_review, dispatch_window_review, dispatch_release_edit, record_external_release_edit
from nrl_story_window import (
    build_story_window_status,
    generate_story_window,
    story_beat_for,
    validate_story_window,
)
from nrl_registry import (
    find_active_attempt,
    load_registry,
    mark_attempt_status,
    record_handoff_attempt,
    save_registry,
    upsert_registry_mission,
)
from nrl_rag_index import (
    load_or_build_creation_context_index,
    load_or_build_rag_index,
    write_creation_context_index,
    write_rag_index,
)
from nrl_research_assets import build_research_asset_catalog
from nrl_studio import render_studio
from nrl_studio_data import build_studio_data
from nrl_studio_server import create_studio_server
from nrl_system_check import run_system_check
from nrl_system_status import build_system_status

STATE_PATH = runtime_path("system/mission_controller/current_phase_state.json")
SCHEMA_PATH = runtime_path("system/mission_controller/phase_state.schema.json")
RULES_PATH = runtime_path("system/mission_controller/next_mission_rules.md")
CONTRACT_PATH = runtime_path("system/mission_controller/agent_task_contract.md")
ADAPTERS_PATH = runtime_path("system/runtime/agent_adapters.json")
REGISTRY_PATH = runtime_path("system/runtime/mission_registry.json")
PRODUCTION_REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")

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
    mission_id = mission_id_for(mission_name)
    if agent == "antigravity":
        if mission_id == "phase2d_antigravity_outline_tree_review":
            return ["handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"]
        return [f"handoff/antigravity/outputs/{mission_id}.md"]
    if agent == "hermes":
        return ["handoff/hermes/outputs/external_hermes_output.md"]
    return [f"system/runtime/{mission_id}_codex_output.md"]


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


def cmd_system_status(_: argparse.Namespace) -> int:
    state = load_state()
    adapters = load_adapters()
    print_json(build_system_status(state, adapters))
    return 0


def cmd_studio_data(_: argparse.Namespace) -> int:
    state = load_state()
    adapters = load_adapters()
    registry = load_registry()
    print_json(build_studio_data(state, registry, adapters))
    return 0


def cmd_creation_assets(_: argparse.Namespace) -> int:
    state = load_state()
    system_status = build_system_status(state, load_adapters())
    print_json(
        load_creation_asset_registry(
            str(state.get("selected_project", "UNKNOWN_PROJECT")),
            str(system_status.get("operating_mode", "UNKNOWN_MODE")),
        )
    )
    return 0


def cmd_asset_graph_status(_: argparse.Namespace) -> int:
    result = build_creation_asset_graph_status()
    print_json(result)
    return 0 if result["graph_valid"] else 1


def cmd_hardening_status(_: argparse.Namespace) -> int:
    print_json(build_hardening_status(load_state(), load_adapters()))
    return 0


def cmd_research_assets(args: argparse.Namespace) -> int:
    print_json(
        build_research_asset_catalog(
            {
                "title": args.title,
                "asset_type": args.asset_type,
                "category": args.category,
                "review_state": args.review_state,
            }
        )
    )
    return 0


def cmd_creation_schemas(_: argparse.Namespace) -> int:
    print_json(build_creation_schema_registry())
    return 0


def cmd_validate_creation_assets(_: argparse.Namespace) -> int:
    result = validate_creation_asset_store()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_final_assets_validate(args: argparse.Namespace) -> int:
    result = validate_final_asset_bundle(args.file)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_final_assets_promote(args: argparse.Namespace) -> int:
    result = promote_final_asset_bundle(args.file)
    print_json(result)
    return 0 if result["promotion_allowed"] else 1


def cmd_hermes_bridge_status(_: argparse.Namespace) -> int:
    print_json(build_hermes_execution_status(load_adapters().get("hermes", {})))
    return 0


def cmd_controlled_prose_status(_: argparse.Namespace) -> int:
    audit_text = AUDIT_PATH.read_text(encoding="utf-8") if AUDIT_PATH.exists() else ""
    print_json(build_controlled_prose_readiness(load_decisions(), audit_text))
    return 0


def cmd_controlled_prose_test(_: argparse.Namespace) -> int:
    adapter_status = build_hermes_execution_status(load_adapters().get("hermes", {}))
    if not adapter_status["can_execute_controlled_prose_test"]:
        print_json({"valid": False, "error": adapter_status["blocked_reason"]})
        return 1
    audit_text = AUDIT_PATH.read_text(encoding="utf-8") if AUDIT_PATH.exists() else ""
    result = dispatch_controlled_prose_test(
        build_controlled_prose_prompt(),
        load_decisions(),
        audit_text,
        CONTROLLED_PROSE_OUTPUT_PATH,
    )
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_controlled_prose_validate(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print_json({"valid": False, "errors": [{"code": "missing_output", "message": str(path)}]})
        return 1
    result = validate_controlled_prose_text(path.read_text(encoding="utf-8"))
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_system_check(_: argparse.Namespace) -> int:
    result = run_system_check()
    print_json(result)
    return 0 if result["passed"] else 1


def cmd_pipeline_status(_: argparse.Namespace) -> int:
    print_json(build_pipeline_status(load_state(), load_adapters()))
    return 0


def cmd_pipeline_plan(args: argparse.Namespace) -> int:
    print_json(
        build_pipeline_plan(
            load_state(),
            load_adapters(),
            family=args.family,
            next_only=args.next,
        )
    )
    return 0


def cmd_evidence_pack(args: argparse.Namespace) -> int:
    pack = build_evidence_pack(
        load_state(),
        load_adapters(),
        family=args.family,
        next_only=args.next,
    )
    if args.write:
        pack = write_evidence_pack(pack)
    print_json(pack)
    return 0


def cmd_evidence_pack_validate(args: argparse.Namespace) -> int:
    if args.all:
        validation = validate_all_evidence_packs(load_state(), load_adapters())
        print_json(validation)
        return 0 if validation["valid"] else 1
    if args.file:
        pack = load_evidence_pack(args.file)
    else:
        pack = build_evidence_pack(
            load_state(),
            load_adapters(),
            family=args.family,
            next_only=args.next,
        )
    validation = validate_evidence_pack(pack)
    print_json(validation)
    return 0 if validation["valid"] else 1


def cmd_evidence_pack_matrix(args: argparse.Namespace) -> int:
    state = load_state()
    adapters = load_adapters()
    matrix = build_evidence_pack_matrix(state, adapters)
    if args.write:
        matrix = write_evidence_pack_matrix(matrix, state, adapters)
    print_json(matrix)
    return 0 if matrix["valid_family_count"] == matrix["family_count"] else 1


def cmd_architecture_status(_: argparse.Namespace) -> int:
    print_json(build_architecture_reconciliation(load_state(), load_adapters()))
    return 0


def cmd_dna_registry_build(_: argparse.Namespace) -> int:
    print_json(write_dna_registry(load_state()))
    return 0


def cmd_dna_registry(_: argparse.Namespace) -> int:
    print_json(load_or_build_dna_registry(load_state()))
    return 0


def cmd_rag_index_build(_: argparse.Namespace) -> int:
    print_json(write_rag_index(load_state()))
    return 0


def cmd_rag_index(_: argparse.Namespace) -> int:
    print_json(load_or_build_rag_index(load_state()))
    return 0


def cmd_creation_context_index_build(_: argparse.Namespace) -> int:
    print_json(write_creation_context_index(load_state(), load_adapters()))
    return 0


def cmd_creation_context_index(_: argparse.Namespace) -> int:
    print_json(load_or_build_creation_context_index(load_state(), load_adapters()))
    return 0


def cmd_agent_jobs(_: argparse.Namespace) -> int:
    print_json(load_job_queue())
    return 0


def cmd_agent_job_plan(args: argparse.Namespace) -> int:
    print_json(plan_agent_job(load_state(), load_adapters(), args.family))
    return 0


def cmd_agent_pack(args: argparse.Namespace) -> int:
    print_json(write_agent_packet(args.job_id))
    return 0


def cmd_agent_ingest(args: argparse.Namespace) -> int:
    print_json(ingest_agent_output(args.job_id, args.file))
    return 0


def cmd_agent_validate(args: argparse.Namespace) -> int:
    result = validate_agent_job(args.job_id)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_agent_dispatch(args: argparse.Namespace) -> int:
    result = dispatch_agent_job(
        args.job_id,
        load_adapters(),
        print_timeout=args.print_timeout,
    )
    print_json(result)
    return 0 if result["state"] == "output_received" else 1


def cmd_production_runtime_status(_: argparse.Namespace) -> int:
    print_json(build_production_runtime_status(load_state(), load_adapters()))
    return 0


def cmd_producer_status(_: argparse.Namespace) -> int:
    print_json(build_producer_status(load_state(), load_adapters()))
    return 0


def cmd_produce_techniques(args: argparse.Namespace) -> int:
    result = produce_technique_candidates(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_naming_seed(args: argparse.Namespace) -> int:
    result = produce_naming_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_npc_seed(args: argparse.Namespace) -> int:
    result = produce_npc_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_artifact_seed(args: argparse.Namespace) -> int:
    result = produce_artifact_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_state_ledger_seed(args: argparse.Namespace) -> int:
    result = produce_state_ledger_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_emotional_bond_seed(args: argparse.Namespace) -> int:
    result = produce_emotional_bond_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_foreshadowing_seed(args: argparse.Namespace) -> int:
    result = produce_foreshadowing_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_character_seed(args: argparse.Namespace) -> int:
    result = produce_character_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_produce_faction_seed(args: argparse.Namespace) -> int:
    result = produce_faction_seed(load_state(), args.job_id)
    print_json(result)
    return 0 if result["store_validation"]["valid"] else 1


def cmd_hermes_readiness(_: argparse.Namespace) -> int:
    result = build_hermes_readiness(load_state(), load_adapters())
    print_json(result)
    return 0


def cmd_antigravity_full_corpus_pack(_: argparse.Namespace) -> int:
    print_json(write_full_corpus_packet(load_state(), load_adapters()))
    return 0


def cmd_antigravity_full_corpus_status(_: argparse.Namespace) -> int:
    print_json(build_full_corpus_status(load_state(), load_adapters()))
    return 0


def cmd_antigravity_full_corpus_ingest(args: argparse.Namespace) -> int:
    print_json(ingest_full_corpus_output(args.file))
    return 0


def cmd_antigravity_full_corpus_validate(_: argparse.Namespace) -> int:
    result = validate_full_corpus_output()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_full_corpus_proof_status(_: argparse.Namespace) -> int:
    print_json(build_proof_status())
    return 0


def cmd_full_corpus_proof_pack(args: argparse.Namespace) -> int:
    print_json(write_proof_packets(all_books=args.all, book_title=args.book_title))
    return 0


def cmd_full_corpus_proof_validate(args: argparse.Namespace) -> int:
    result = validate_proof_file(args.file)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_full_corpus_proof_merge(args: argparse.Namespace) -> int:
    print_json(merge_proof_receipts(args.input_dir, args.output_file))
    return 0


def cmd_full_corpus_proof_promote(_: argparse.Namespace) -> int:
    result = promote_verified_proof()
    print_json(result)
    return 0 if result["status"] == "promoted_research_asset" else 1


def cmd_full_corpus_review_ingest(_: argparse.Namespace) -> int:
    result = write_promoted_review_assets()
    print_json(result)
    return 0


def cmd_deep_read_plan(args: argparse.Namespace) -> int:
    print_json(build_deep_read_plan(args.target_bytes))
    return 0


def cmd_deep_read_status(_: argparse.Namespace) -> int:
    print_json(build_deep_read_status())
    return 0


def cmd_deep_read_attest(_: argparse.Namespace) -> int:
    print_json(build_promotion_attestation())
    return 0


def cmd_deep_read_validate_chunk(args: argparse.Namespace) -> int:
    result = validate_chunk_response(args.chunk_id)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_deep_read_validate_all(_: argparse.Namespace) -> int:
    result = validate_all_chunks()
    print_json(result)
    return 0 if result["status"] == "chunk_coverage_verified" else 1


def cmd_deep_read_dispatch(args: argparse.Namespace) -> int:
    result = dispatch_pending_chunks(
        limit=args.limit,
        workers=args.workers,
        model=args.model,
        print_timeout=args.print_timeout,
        runner=args.runner,
        skip_chunk_ids=tuple(args.skip_chunk_id),
    )
    print_json(result)
    return 0 if not result["failed"] else 1


def cmd_deep_read_synthesis_pack(_: argparse.Namespace) -> int:
    print_json(build_book_synthesis_packets())
    return 0


def cmd_deep_read_synthesis_dispatch(args: argparse.Namespace) -> int:
    result = dispatch_book_syntheses(workers=args.workers, model=args.model, print_timeout=args.print_timeout)
    print_json(result)
    return 0 if result["validation"]["valid"] else 1


def cmd_deep_read_synthesis_validate(_: argparse.Namespace) -> int:
    result = validate_book_syntheses()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_deep_read_cross_pack(_: argparse.Namespace) -> int:
    print_json(build_cross_book_packet())
    return 0


def cmd_deep_read_cross_dispatch(args: argparse.Namespace) -> int:
    result = dispatch_cross_book_distillation(model=args.model, print_timeout=args.print_timeout)
    print_json(result)
    return 0 if result["validation"]["valid"] else 1


def cmd_deep_read_cross_validate(_: argparse.Namespace) -> int:
    result = validate_cross_book_distillation()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_project_reconciliation_pack(_: argparse.Namespace) -> int:
    print_json(build_project_reconciliation_packet())
    return 0


def cmd_project_reconciliation_dispatch(args: argparse.Namespace) -> int:
    result = dispatch_project_reconciliation(model=args.model, print_timeout=args.print_timeout)
    print_json(result)
    return 0 if result["validation"]["valid"] else 1


def cmd_project_reconciliation_validate(_: argparse.Namespace) -> int:
    result = validate_project_reconciliation()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_project_reconciliation_apply(_: argparse.Namespace) -> int:
    print_json(apply_project_reconciliation())
    return 0


def cmd_production_readiness(_: argparse.Namespace) -> int:
    result = build_production_readiness()
    print_json(result)
    return 0 if result["ready"] else 1


def cmd_chapter_runtime_status(_: argparse.Namespace) -> int:
    print_json(load_chapter_runtime_status())
    return 0


def cmd_production_preflight(_: argparse.Namespace) -> int:
    result = build_production_preflight(load_adapters())
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_chapter_quarantine(args: argparse.Namespace) -> int:
    print_json(quarantine_unaccepted_chapter(args.chapter_id, args.reason))
    return 0


def cmd_volume1_plan_build(_: argparse.Namespace) -> int:
    result = write_volume1_production_contracts()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_plan_validate(_: argparse.Namespace) -> int:
    from nrl_volume1_plan import LEDGER_PATH, PLAN_PATH, _read_json
    result = {"manifest": validate_volume1_manifest(_read_json(PLAN_PATH) if PLAN_PATH.exists() else {}), "state_contract": validate_initial_state_contract(_read_json(LEDGER_PATH) if LEDGER_PATH.exists() else {})}
    result["valid"] = result["manifest"]["valid"] and result["state_contract"]["valid"]
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_dry_run(_: argparse.Namespace) -> int:
    result = build_volume1_dry_run()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_agent_canaries_run(args: argparse.Namespace) -> int:
    case_ids = tuple(f"protocol-{index:02d}" for index in range(args.from_index, args.to_index + 1))
    result = run_agent_protocol_canaries(agent=args.agent, case_ids=case_ids)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_agent_canaries_validate(_: argparse.Namespace) -> int:
    result = validate_agent_protocol_canaries()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_longform_candidate_build(_: argparse.Namespace) -> int:
    result = write_longform_candidate_contracts()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_longform_candidate_validate(_: argparse.Namespace) -> int:
    result = {"contract": validate_longform_contract(build_longform_contract()), "first100": validate_first100_manifest(build_first100_manifest()), "guards": validate_first100_guard_config(build_first100_guard_config())}
    result["valid"] = result["contract"]["valid"] and result["first100"]["valid"] and result["guards"]["valid"]
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_longform_readiness(_: argparse.Namespace) -> int:
    result = build_longform_readiness()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_longform_promote(_: argparse.Namespace) -> int:
    print_json(promote_longform_blueprint())
    return 0


def cmd_longform_first100_dry_run(_: argparse.Namespace) -> int:
    result = build_longform_first100_dry_run()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_story_window_status(_: argparse.Namespace) -> int:
    result = build_story_window_status()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_story_window_validate(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_absolute():
        path = ROOT / path
    result = validate_story_window(json.loads(path.read_text(encoding="utf-8")))
    result["path"] = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_story_window_build(args: argparse.Namespace) -> int:
    print_json(generate_story_window(args.start, timeout_seconds=args.timeout_seconds))
    return 0


def cmd_longform_cluster1_intents_build(_: argparse.Namespace) -> int:
    print_json(write_cluster1_intents())
    return 0


def cmd_volume1_longform_intents_build(_: argparse.Namespace) -> int:
    result = write_volume1_intents()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_longform_intents_validate(_: argparse.Namespace) -> int:
    result = validate_volume1_manifest(build_volume1_manifest())
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_release_status(_: argparse.Namespace) -> int:
    result = build_release_readiness()
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_window_review_packet(args: argparse.Namespace) -> int:
    result = build_window_review_packet(args.start, args.end)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_window_review_record(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_absolute():
        path = ROOT / path
    print_json(record_window_review(json.loads(path.read_text(encoding="utf-8"))))
    return 0


def cmd_volume1_window_review(args: argparse.Namespace) -> int:
    result = dispatch_window_review(args.start, args.end, model=args.model)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_volume1_release_edit(args: argparse.Namespace) -> int:
    print_json(dispatch_release_edit(args.chapter_id, args.repair_direction))
    return 0


def cmd_volume1_release_edit_record(args: argparse.Namespace) -> int:
    source_file = Path(args.file)
    if not source_file.is_absolute():
        source_file = ROOT / source_file
    print_json(record_external_release_edit(args.chapter_id, source_file, args.repair_direction, args.provider))
    return 0


def cmd_volume1_batch_run(args: argparse.Namespace) -> int:
    if not 12 <= args.start <= args.end <= 100:
        raise RuntimeError("Volume 1 batch range must be within chapters 12-100")
    completed = []
    for ordinal in range(args.start, args.end + 1):
        chapter_id = f"chapter-{ordinal:04d}"
        if ordinal >= 21 and story_beat_for(chapter_id) is None:
            generated = generate_story_window(((ordinal - 1) // 10) * 10 + 1)
            completed.append({"story_window": generated})
        intent = f"system/production_runtime/intents/longform_volume1_v025/chapter-{ordinal:04d}.v0.25.json"
        result = run_controlled_chapter_pipeline(intent, audit_model=args.audit_model)
        completed.append(result)
        if not result["valid"]:
            print_json({"valid": False, "completed": completed, "failed_chapter": f"chapter-{ordinal:04d}"})
            return 1
        # Accepted chapters immediately leave the working set. This keeps
        # prompts, draft packets and compiled context from accumulating across
        # a long volume while preserving every release and state artifact.
        compact_accepted_chapters(ROOT, PRODUCTION_REGISTRY_PATH)
        if ordinal % 10 == 0:
            review = dispatch_window_review(ordinal - 9, ordinal, model=args.audit_model)
            completed.append({"window_review": review})
            if not review["valid"]:
                print_json({"valid": False, "completed": completed, "window_review": review})
                return 1
    print_json({"valid": True, "completed": completed})
    return 0


def cmd_production_status(args: argparse.Namespace) -> int:
    result = build_operator_status(PRODUCTION_REGISTRY_PATH, target=args.until)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_production_compact(args: argparse.Namespace) -> int:
    result = (
        compact_accepted_chapters(ROOT, PRODUCTION_REGISTRY_PATH)
        if args.apply
        else build_compaction_plan(ROOT, PRODUCTION_REGISTRY_PATH)
    )
    print_json({key: value for key, value in result.items() if key != "compact_artifacts"})
    return 0 if result["valid"] else 1


def cmd_produce(args: argparse.Namespace) -> int:
    if not 1 <= args.until <= 100:
        raise RuntimeError("produce target must be within Volume 1 chapters 1-100")
    status = build_operator_status(PRODUCTION_REGISTRY_PATH, target=args.until)
    if not status["valid"]:
        print_json(status)
        return 1
    if status["next_chapter"] is None:
        print_json({"valid": True, "status": status, "completed": []})
        return 0
    preflight = build_production_preflight(
        load_adapters(), allowed_pending_chapter_id=status["next_chapter"]
    )
    if not preflight["valid"]:
        print_json({"valid": False, "status": status, "preflight": preflight})
        return 1
    start = int(status["next_chapter"].removeprefix("chapter-"))
    batch_args = argparse.Namespace(start=start, end=args.until, audit_model=args.audit_model)
    return cmd_volume1_batch_run(batch_args)


def cmd_volume1_fanqie_package(_: argparse.Namespace) -> int:
    print_json(build_fanqie_upload_package())
    return 0


def cmd_volume1_review_package(args: argparse.Namespace) -> int:
    print_json(build_review_manuscript(args.end))
    return 0


def cmd_prose_metrics(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise RuntimeError(f"prose file does not exist: {args.file}")
    print_json(analyze_prose_metrics(path.read_text(encoding="utf-8")))
    return 0


def cmd_chapter_init(args: argparse.Namespace) -> int:
    print_json(initialize_chapter(args.intent_file))
    return 0


def cmd_chapter_compile(args: argparse.Namespace) -> int:
    print_json(compile_chapter_context(args.chapter_id))
    return 0


def cmd_chapter_draft(args: argparse.Namespace) -> int:
    result = dispatch_chapter_draft(args.chapter_id)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_chapter_observe_ingest(args: argparse.Namespace) -> int:
    print_json(ingest_chapter_observation(args.chapter_id, args.file))
    return 0


def cmd_chapter_observe(args: argparse.Namespace) -> int:
    print_json(dispatch_chapter_observation(args.chapter_id))
    return 0


def cmd_chapter_audit(args: argparse.Namespace) -> int:
    result = dispatch_chapter_audit(args.chapter_id, model=args.model)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_chapter_audit_ingest(args: argparse.Namespace) -> int:
    print_json(ingest_chapter_audit(args.chapter_id, args.file))
    return 0


def cmd_chapter_revision_ingest(args: argparse.Namespace) -> int:
    print_json(ingest_chapter_revision(args.chapter_id, args.file))
    return 0


def cmd_chapter_revision(args: argparse.Namespace) -> int:
    result = dispatch_chapter_revision(args.chapter_id)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_chapter_settle(args: argparse.Namespace) -> int:
    print_json(settle_chapter_state(args.chapter_id, args.file))
    return 0


def cmd_chapter_settlement_candidate(args: argparse.Namespace) -> int:
    print_json(build_observed_settlement_candidate(args.chapter_id))
    return 0


def cmd_chapter_run(args: argparse.Namespace) -> int:
    result = run_controlled_chapter_pipeline(args.intent_file, audit_model=args.audit_model)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_model_routing_status(_: argparse.Namespace) -> int:
    print_json(build_model_routing_status())
    return 0


def cmd_direct_writer_calibration_status(_: argparse.Namespace) -> int:
    print_json(build_direct_writer_calibration_status())
    return 0


def cmd_direct_writer_calibration_run(args: argparse.Namespace) -> int:
    result = run_direct_writer_calibration(timeout_seconds=args.timeout_seconds)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_direct_writer_calibration_review_packet(_: argparse.Namespace) -> int:
    print_json(build_blind_review_packet())
    return 0


def cmd_direct_writer_calibration_internal_screen(args: argparse.Namespace) -> int:
    print_json(run_internal_calibration_screen(timeout_seconds=args.timeout_seconds))
    return 0


def cmd_direct_writer_calibration_external_blocked(args: argparse.Namespace) -> int:
    print_json(record_external_review_blocked(args.reason))
    return 0


def cmd_direct_writer_calibration_decision_packet(_: argparse.Namespace) -> int:
    print_json(build_calibration_routing_decision_packet())
    return 0


def cmd_direct_writer_calibration_decision_record(args: argparse.Namespace) -> int:
    result = record_calibration_routing_decision(args.file)
    print_json(result)
    return 0 if result["valid"] else 1


def cmd_chapter_accept(args: argparse.Namespace) -> int:
    print_json(accept_chapter(args.chapter_id))
    return 0


def cmd_antigravity_bridge_status(_: argparse.Namespace) -> int:
    print_json(build_antigravity_bridge_status())
    return 0


def cmd_antigravity_bridge_ask(args: argparse.Namespace) -> int:
    result = ask_antigravity(
        args.request_file,
        output_file=args.output_file,
        print_timeout=args.print_timeout,
        model=args.model,
    )
    print_json(result)
    return 0


def cmd_studio_serve(args: argparse.Namespace) -> int:
    server = create_studio_server(args.host, args.port)
    print_json(
        {
            "studio_url": f"http://{args.host}:{server.server_port}",
            "mode": "live_control_plane",
        }
    )
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
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
    if args.bound_response_sha256:
        decision["bound_response_sha256"] = args.bound_response_sha256
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

## Single Input Packet

Use this packet as the single Antigravity input surface:

```text
handoff/{mission["responsible_agent"]}/current_packet.md
```

## Blocked Actions

{blocked_actions}

## Runtime Instruction

This handoff is for manual external-agent execution. The runtime has not called the agent. Place the completed external output in the expected output directory, then run:

```text
python3 system/runtime/nrl.py advance
```
"""


def prepare_handoff(agent: str) -> dict[str, Any]:
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
    packet_path = write_antigravity_packet(mission, handoff_dir) if agent == "antigravity" else None
    attempt = record_handoff_attempt(mission, str(adapter.get("mode")), now_iso())
    result = {
        "handoff_path": str(handoff_path.relative_to(ROOT)),
        "status": "awaiting_external_output",
        "handoff_attempt_id": attempt["handoff_attempt_id"],
    }
    if packet_path is not None:
        result["handoff_packet_path"] = str(packet_path.relative_to(ROOT))
    return result


def cmd_prepare_handoff(args: argparse.Namespace) -> int:
    print_json(prepare_handoff(args.agent.lower()))
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


def ingest_file(agent: str, file_arg: str) -> dict[str, Any]:
    if agent not in {"hermes", "antigravity"}:
        raise RuntimeError("ingest supports only hermes or antigravity")
    file_path = Path(file_arg)
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
    return {"ingested": rel_file, "agent": agent, "registry_status": status}


def cmd_ingest(args: argparse.Namespace) -> int:
    print_json(ingest_file(args.agent.lower(), args.file))
    return 0


def cmd_advance(_: argparse.Namespace) -> int:
    state = load_state()
    mission = current_mission(state)
    agent = mission["responsible_agent"]
    mission_id = mission["mission_id"]

    if (
        state.get("current_phase") == "Phase 2E"
        and state.get("phase_status") == "PHASE2E_CONTROLLED_PLANNING_OUTPUT_READY"
    ):
        result = prepare_phase2e_controlled_planning_validation(state, now_iso())
        write_json(STATE_PATH, state)
        print_json(
            {
                "action": "phase2e_controlled_planning_validated",
                "status": "ready_for_antigravity_controlled_planning_review",
                "mission_id": mission_id,
                "responsible_agent": agent,
                **result,
            }
        )
        return 0

    if (
        state.get("current_phase") == "Phase 2E"
        and state.get("phase_status") == "PHASE2E_PLANNING_PACKAGE_READY"
    ):
        result = prepare_phase2e_controlled_planning_output(state, now_iso())
        write_json(STATE_PATH, state)
        print_json(
            {
                "action": "phase2e_controlled_planning_output_prepared",
                "status": "phase2e_controlled_planning_output_ready",
                "mission_id": mission_id,
                "responsible_agent": agent,
                **result,
            }
        )
        return 0

    if (
        state.get("current_phase") == "Phase 2E"
        and state.get("phase_status") == "PHASE2E_ENTRY_PREPARATION_AUTHORIZED"
    ):
        result = prepare_phase2e_planning_package(state, now_iso())
        write_json(STATE_PATH, state)
        print_json(
            {
                "action": "phase2e_planning_package_prepared",
                "status": "phase2e_planning_package_ready",
                "mission_id": mission_id,
                "responsible_agent": agent,
                **result,
            }
        )
        return 0

    if state.get("owner_gate_required", False):
        decision = latest_phase2e_acceptance(load_decisions())
        can_apply_phase2e_entry_acceptance = (
            state.get("current_phase") == "Phase 2D"
            and mission_id == "phase2d_antigravity_outline_tree_review"
            and decision is not None
        )
        if can_apply_phase2e_entry_acceptance:
            result = prepare_phase2e_entry(state, decision, now_iso())
            write_json(STATE_PATH, state)
            print_json(
                {
                    "action": "phase2e_entry_prepared",
                    "status": "ready_for_phase2e_planning",
                    "mission_id": mission_id,
                    "responsible_agent": "codex",
                    **result,
                }
            )
            return 0
        print_json(
            {
                "action": "owner_gate_required",
                "status": "manual_owner_decision_required",
                "mission_id": mission_id,
                "responsible_agent": agent,
                "owner_gate_status": state.get("owner_gate_status"),
            }
        )
        return 0

    if agent not in {"hermes", "antigravity"}:
        print_json(
            {
                "action": "unsupported_local_advance",
                "status": "manual_runtime_decision_required",
                "mission_id": mission_id,
                "responsible_agent": agent,
            }
        )
        return 0

    expected_output = mission["expected_outputs"][0]
    active_attempt = find_active_attempt(mission_id, expected_output)
    expected_path = ROOT / expected_output

    if active_attempt is None:
        result = prepare_handoff(agent)
        print_json(
            {
                "action": "prepared_handoff",
                "mission_id": mission_id,
                "responsible_agent": agent,
                **result,
            }
        )
        return 0

    if not expected_path.exists():
        print_json(
            {
                "action": "awaiting_external_output",
                "status": "blocked_on_external_agent",
                "mission_id": mission_id,
                "responsible_agent": agent,
                "handoff_attempt_id": active_attempt["handoff_attempt_id"],
                "expected_output": expected_output,
                "next_required_external_step": f"Produce {expected_output} with {agent}.",
            }
        )
        return 0

    result = ingest_file(agent, expected_output)
    next_status = "owner_gate_required" if agent == "antigravity" else "validation_required"
    print_json(
        {
            "action": "ingested_external_output",
            "status": next_status,
            "mission_id": mission_id,
            "responsible_agent": agent,
            **result,
        }
    )
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
    sub.add_parser("system-status").set_defaults(func=cmd_system_status)
    sub.add_parser("studio-data").set_defaults(func=cmd_studio_data)
    sub.add_parser("creation-assets").set_defaults(func=cmd_creation_assets)
    sub.add_parser("asset-graph-status").set_defaults(func=cmd_asset_graph_status)
    sub.add_parser("hardening-status").set_defaults(func=cmd_hardening_status)
    research = sub.add_parser("research-assets")
    research.add_argument("--title")
    research.add_argument("--asset-type")
    research.add_argument("--category")
    research.add_argument("--review-state")
    research.set_defaults(func=cmd_research_assets)
    sub.add_parser("creation-schemas").set_defaults(func=cmd_creation_schemas)
    sub.add_parser("validate-creation-assets").set_defaults(
        func=cmd_validate_creation_assets
    )
    final_assets_validate = sub.add_parser("final-assets-validate")
    final_assets_validate.add_argument("--file", required=True)
    final_assets_validate.set_defaults(func=cmd_final_assets_validate)
    final_assets_promote = sub.add_parser("final-assets-promote")
    final_assets_promote.add_argument("--file", required=True)
    final_assets_promote.set_defaults(func=cmd_final_assets_promote)
    sub.add_parser("hermes-bridge-status").set_defaults(func=cmd_hermes_bridge_status)
    sub.add_parser("controlled-prose-status").set_defaults(func=cmd_controlled_prose_status)
    sub.add_parser("controlled-prose-test").set_defaults(func=cmd_controlled_prose_test)
    controlled_prose_validate = sub.add_parser("controlled-prose-validate")
    controlled_prose_validate.add_argument("--file", required=True)
    controlled_prose_validate.set_defaults(func=cmd_controlled_prose_validate)
    sub.add_parser("system-check").set_defaults(func=cmd_system_check)
    sub.add_parser("pipeline-status").set_defaults(func=cmd_pipeline_status)
    pipeline_plan = sub.add_parser("pipeline-plan")
    pipeline_target = pipeline_plan.add_mutually_exclusive_group(required=True)
    pipeline_target.add_argument("--family")
    pipeline_target.add_argument("--next", action="store_true")
    pipeline_plan.set_defaults(func=cmd_pipeline_plan)
    evidence_pack = sub.add_parser("evidence-pack")
    evidence_target = evidence_pack.add_mutually_exclusive_group(required=True)
    evidence_target.add_argument("--family")
    evidence_target.add_argument("--next", action="store_true")
    evidence_pack.add_argument("--write", action="store_true")
    evidence_pack.set_defaults(func=cmd_evidence_pack)
    evidence_pack_validate = sub.add_parser("evidence-pack-validate")
    evidence_pack_validate_target = evidence_pack_validate.add_mutually_exclusive_group(required=True)
    evidence_pack_validate_target.add_argument("--family")
    evidence_pack_validate_target.add_argument("--next", action="store_true")
    evidence_pack_validate_target.add_argument("--file")
    evidence_pack_validate_target.add_argument("--all", action="store_true")
    evidence_pack_validate.set_defaults(func=cmd_evidence_pack_validate)
    evidence_pack_matrix = sub.add_parser("evidence-pack-matrix")
    evidence_pack_matrix.add_argument("--write", action="store_true")
    evidence_pack_matrix.set_defaults(func=cmd_evidence_pack_matrix)
    sub.add_parser("architecture-status").set_defaults(func=cmd_architecture_status)
    sub.add_parser("dna-registry-build").set_defaults(func=cmd_dna_registry_build)
    sub.add_parser("dna-registry").set_defaults(func=cmd_dna_registry)
    sub.add_parser("rag-index-build").set_defaults(func=cmd_rag_index_build)
    sub.add_parser("rag-index").set_defaults(func=cmd_rag_index)
    sub.add_parser("creation-context-index-build").set_defaults(
        func=cmd_creation_context_index_build
    )
    sub.add_parser("creation-context-index").set_defaults(
        func=cmd_creation_context_index
    )
    sub.add_parser("agent-jobs").set_defaults(func=cmd_agent_jobs)
    agent_job_plan = sub.add_parser("agent-job-plan")
    agent_job_plan.add_argument("--family", required=True)
    agent_job_plan.set_defaults(func=cmd_agent_job_plan)
    agent_pack = sub.add_parser("agent-pack")
    agent_pack.add_argument("--job-id", required=True)
    agent_pack.set_defaults(func=cmd_agent_pack)
    agent_ingest = sub.add_parser("agent-ingest")
    agent_ingest.add_argument("--job-id", required=True)
    agent_ingest.add_argument("--file", required=True)
    agent_ingest.set_defaults(func=cmd_agent_ingest)
    agent_validate = sub.add_parser("agent-validate")
    agent_validate.add_argument("--job-id", required=True)
    agent_validate.set_defaults(func=cmd_agent_validate)
    agent_dispatch = sub.add_parser("agent-dispatch")
    agent_dispatch.add_argument("--job-id", required=True)
    agent_dispatch.add_argument("--print-timeout", default="5m0s")
    agent_dispatch.set_defaults(func=cmd_agent_dispatch)
    sub.add_parser("production-runtime-status").set_defaults(
        func=cmd_production_runtime_status
    )
    sub.add_parser("producer-status").set_defaults(func=cmd_producer_status)
    produce_techniques = sub.add_parser("produce-techniques")
    produce_techniques.add_argument("--job-id", required=True)
    produce_techniques.set_defaults(func=cmd_produce_techniques)
    produce_naming = sub.add_parser("produce-naming-seed")
    produce_naming.add_argument("--job-id", required=True)
    produce_naming.set_defaults(func=cmd_produce_naming_seed)
    produce_npc = sub.add_parser("produce-npc-seed")
    produce_npc.add_argument("--job-id", required=True)
    produce_npc.set_defaults(func=cmd_produce_npc_seed)
    produce_artifact = sub.add_parser("produce-artifact-seed")
    produce_artifact.add_argument("--job-id", required=True)
    produce_artifact.set_defaults(func=cmd_produce_artifact_seed)
    produce_state = sub.add_parser("produce-state-ledger-seed")
    produce_state.add_argument("--job-id", required=True)
    produce_state.set_defaults(func=cmd_produce_state_ledger_seed)
    produce_bond = sub.add_parser("produce-emotional-bond-seed")
    produce_bond.add_argument("--job-id", required=True)
    produce_bond.set_defaults(func=cmd_produce_emotional_bond_seed)
    produce_foreshadowing = sub.add_parser("produce-foreshadowing-seed")
    produce_foreshadowing.add_argument("--job-id", required=True)
    produce_foreshadowing.set_defaults(func=cmd_produce_foreshadowing_seed)
    produce_character = sub.add_parser("produce-character-seed")
    produce_character.add_argument("--job-id", required=True)
    produce_character.set_defaults(func=cmd_produce_character_seed)
    produce_faction = sub.add_parser("produce-faction-seed")
    produce_faction.add_argument("--job-id", required=True)
    produce_faction.set_defaults(func=cmd_produce_faction_seed)
    sub.add_parser("hermes-readiness").set_defaults(func=cmd_hermes_readiness)
    sub.add_parser("antigravity-full-corpus-pack").set_defaults(
        func=cmd_antigravity_full_corpus_pack
    )
    sub.add_parser("antigravity-full-corpus-status").set_defaults(
        func=cmd_antigravity_full_corpus_status
    )
    full_corpus_ingest = sub.add_parser("antigravity-full-corpus-ingest")
    full_corpus_ingest.add_argument("--file", required=True)
    full_corpus_ingest.set_defaults(func=cmd_antigravity_full_corpus_ingest)
    sub.add_parser("antigravity-full-corpus-validate").set_defaults(
        func=cmd_antigravity_full_corpus_validate
    )
    sub.add_parser("full-corpus-proof-status").set_defaults(
        func=cmd_full_corpus_proof_status
    )
    full_corpus_proof_pack = sub.add_parser("full-corpus-proof-pack")
    full_corpus_proof_target = full_corpus_proof_pack.add_mutually_exclusive_group(required=True)
    full_corpus_proof_target.add_argument("--all", action="store_true")
    full_corpus_proof_target.add_argument("--book-title")
    full_corpus_proof_pack.set_defaults(func=cmd_full_corpus_proof_pack)
    full_corpus_proof_validate = sub.add_parser("full-corpus-proof-validate")
    full_corpus_proof_validate.add_argument("--file", required=True)
    full_corpus_proof_validate.set_defaults(func=cmd_full_corpus_proof_validate)
    full_corpus_proof_merge = sub.add_parser("full-corpus-proof-merge")
    full_corpus_proof_merge.add_argument("--input-dir", required=True)
    full_corpus_proof_merge.add_argument("--output-file", required=True)
    full_corpus_proof_merge.set_defaults(func=cmd_full_corpus_proof_merge)
    sub.add_parser("full-corpus-proof-promote").set_defaults(
        func=cmd_full_corpus_proof_promote
    )
    sub.add_parser("full-corpus-review-ingest").set_defaults(
        func=cmd_full_corpus_review_ingest
    )
    deep_read_plan = sub.add_parser("deep-read-plan")
    deep_read_plan.add_argument("--target-bytes", type=int, default=1_500_000)
    deep_read_plan.set_defaults(func=cmd_deep_read_plan)
    sub.add_parser("deep-read-status").set_defaults(func=cmd_deep_read_status)
    sub.add_parser("deep-read-attest").set_defaults(func=cmd_deep_read_attest)
    deep_read_chunk = sub.add_parser("deep-read-validate-chunk")
    deep_read_chunk.add_argument("--chunk-id", required=True)
    deep_read_chunk.set_defaults(func=cmd_deep_read_validate_chunk)
    sub.add_parser("deep-read-validate-all").set_defaults(
        func=cmd_deep_read_validate_all
    )
    deep_read_dispatch = sub.add_parser("deep-read-dispatch")
    deep_read_dispatch.add_argument("--limit", type=int, default=0)
    deep_read_dispatch.add_argument("--workers", type=int, default=2)
    deep_read_dispatch.add_argument("--model", default="Gemini 3.5 Flash (High)")
    deep_read_dispatch.add_argument("--print-timeout", default="10m0s")
    deep_read_dispatch.add_argument("--runner", choices=("agy", "opencode-go", "ccdan-anthropic"), default="agy")
    deep_read_dispatch.add_argument("--skip-chunk-id", action="append", default=[])
    deep_read_dispatch.set_defaults(func=cmd_deep_read_dispatch)
    sub.add_parser("deep-read-synthesis-pack").set_defaults(func=cmd_deep_read_synthesis_pack)
    deep_read_synth_dispatch = sub.add_parser("deep-read-synthesis-dispatch")
    deep_read_synth_dispatch.add_argument("--workers", type=int, default=2)
    deep_read_synth_dispatch.add_argument("--model", default="Gemini 3.5 Flash (High)")
    deep_read_synth_dispatch.add_argument("--print-timeout", default="10m0s")
    deep_read_synth_dispatch.set_defaults(func=cmd_deep_read_synthesis_dispatch)
    sub.add_parser("deep-read-synthesis-validate").set_defaults(func=cmd_deep_read_synthesis_validate)
    sub.add_parser("deep-read-cross-pack").set_defaults(func=cmd_deep_read_cross_pack)
    deep_read_cross_dispatch = sub.add_parser("deep-read-cross-dispatch")
    deep_read_cross_dispatch.add_argument("--model", default="Gemini 3.5 Flash (High)")
    deep_read_cross_dispatch.add_argument("--print-timeout", default="15m0s")
    deep_read_cross_dispatch.set_defaults(func=cmd_deep_read_cross_dispatch)
    sub.add_parser("deep-read-cross-validate").set_defaults(func=cmd_deep_read_cross_validate)
    sub.add_parser("project-reconciliation-pack").set_defaults(func=cmd_project_reconciliation_pack)
    project_reconciliation_dispatch = sub.add_parser("project-reconciliation-dispatch")
    project_reconciliation_dispatch.add_argument("--model", default="Gemini 3.5 Flash (High)")
    project_reconciliation_dispatch.add_argument("--print-timeout", default="15m0s")
    project_reconciliation_dispatch.set_defaults(func=cmd_project_reconciliation_dispatch)
    sub.add_parser("project-reconciliation-validate").set_defaults(func=cmd_project_reconciliation_validate)
    sub.add_parser("project-reconciliation-apply").set_defaults(func=cmd_project_reconciliation_apply)
    sub.add_parser("production-readiness").set_defaults(func=cmd_production_readiness)
    sub.add_parser("chapter-runtime-status").set_defaults(func=cmd_chapter_runtime_status)
    sub.add_parser("production-preflight").set_defaults(func=cmd_production_preflight)
    sub.add_parser("volume1-plan-build").set_defaults(func=cmd_volume1_plan_build)
    sub.add_parser("volume1-plan-validate").set_defaults(func=cmd_volume1_plan_validate)
    sub.add_parser("volume1-dry-run").set_defaults(func=cmd_volume1_dry_run)
    agent_canaries_run = sub.add_parser("agent-canaries-run")
    agent_canaries_run.add_argument("--agent", choices=("hermes", "antigravity"))
    agent_canaries_run.add_argument("--from-index", type=int, default=1)
    agent_canaries_run.add_argument("--to-index", type=int, default=10)
    agent_canaries_run.set_defaults(func=cmd_agent_canaries_run)
    sub.add_parser("agent-canaries-validate").set_defaults(func=cmd_agent_canaries_validate)
    sub.add_parser("longform-candidate-build").set_defaults(func=cmd_longform_candidate_build)
    sub.add_parser("longform-candidate-validate").set_defaults(func=cmd_longform_candidate_validate)
    sub.add_parser("longform-readiness").set_defaults(func=cmd_longform_readiness)
    sub.add_parser("longform-promote").set_defaults(func=cmd_longform_promote)
    sub.add_parser("longform-first100-dry-run").set_defaults(func=cmd_longform_first100_dry_run)
    sub.add_parser("story-window-status").set_defaults(func=cmd_story_window_status)
    story_window_validate = sub.add_parser("story-window-validate")
    story_window_validate.add_argument("--file", required=True)
    story_window_validate.set_defaults(func=cmd_story_window_validate)
    story_window_build = sub.add_parser("story-window-build")
    story_window_build.add_argument("--start", type=int, required=True)
    story_window_build.add_argument("--timeout-seconds", type=int, default=600)
    story_window_build.set_defaults(func=cmd_story_window_build)
    sub.add_parser("longform-cluster1-intents-build").set_defaults(func=cmd_longform_cluster1_intents_build)
    sub.add_parser("volume1-longform-intents-build").set_defaults(func=cmd_volume1_longform_intents_build)
    sub.add_parser("volume1-longform-intents-validate").set_defaults(func=cmd_volume1_longform_intents_validate)
    sub.add_parser("volume1-release-status").set_defaults(func=cmd_volume1_release_status)
    window_packet = sub.add_parser("volume1-window-review-packet")
    window_packet.add_argument("--start", type=int, required=True)
    window_packet.add_argument("--end", type=int, required=True)
    window_packet.set_defaults(func=cmd_volume1_window_review_packet)
    window_record = sub.add_parser("volume1-window-review-record")
    window_record.add_argument("--file", required=True)
    window_record.set_defaults(func=cmd_volume1_window_review_record)
    window_review = sub.add_parser("volume1-window-review")
    window_review.add_argument("--start", type=int, required=True)
    window_review.add_argument("--end", type=int, required=True)
    window_review.add_argument("--model", default="Gemini 3.5 Flash (High)")
    window_review.set_defaults(func=cmd_volume1_window_review)
    release_edit = sub.add_parser("volume1-release-edit")
    release_edit.add_argument("--chapter-id", required=True)
    release_edit.add_argument("--repair-direction", required=True)
    release_edit.set_defaults(func=cmd_volume1_release_edit)
    release_edit_record = sub.add_parser("volume1-release-edit-record")
    release_edit_record.add_argument("--chapter-id", required=True)
    release_edit_record.add_argument("--file", required=True)
    release_edit_record.add_argument("--repair-direction", required=True)
    release_edit_record.add_argument("--provider", required=True)
    release_edit_record.set_defaults(func=cmd_volume1_release_edit_record)
    batch_run = sub.add_parser("volume1-batch-run")
    batch_run.add_argument("--start", type=int, required=True)
    batch_run.add_argument("--end", type=int, required=True)
    batch_run.add_argument("--audit-model", default="Gemini 3.5 Flash (High)")
    batch_run.set_defaults(func=cmd_volume1_batch_run)
    production_status = sub.add_parser("production-status")
    production_status.add_argument("--until", type=int, default=100)
    production_status.set_defaults(func=cmd_production_status)
    production_compact = sub.add_parser("production-compact")
    production_compact.add_argument("--apply", action="store_true")
    production_compact.set_defaults(func=cmd_production_compact)
    produce = sub.add_parser("produce")
    produce.add_argument("--until", type=int, default=100)
    produce.add_argument("--audit-model", default="Gemini 3.5 Flash (High)")
    produce.set_defaults(func=cmd_produce)
    sub.add_parser("volume1-fanqie-package").set_defaults(func=cmd_volume1_fanqie_package)
    review_package = sub.add_parser("volume1-review-package")
    review_package.add_argument("--end", type=int, default=20)
    review_package.set_defaults(func=cmd_volume1_review_package)
    chapter_quarantine = sub.add_parser("chapter-quarantine")
    chapter_quarantine.add_argument("--chapter-id", required=True)
    chapter_quarantine.add_argument("--reason", required=True)
    chapter_quarantine.set_defaults(func=cmd_chapter_quarantine)
    prose_metrics = sub.add_parser("prose-metrics")
    prose_metrics.add_argument("--file", required=True)
    prose_metrics.set_defaults(func=cmd_prose_metrics)
    chapter_init = sub.add_parser("chapter-init")
    chapter_init.add_argument("--intent-file", required=True)
    chapter_init.set_defaults(func=cmd_chapter_init)
    chapter_compile = sub.add_parser("chapter-compile")
    chapter_compile.add_argument("--chapter-id", required=True)
    chapter_compile.set_defaults(func=cmd_chapter_compile)
    chapter_draft = sub.add_parser("chapter-draft")
    chapter_draft.add_argument("--chapter-id", required=True)
    chapter_draft.set_defaults(func=cmd_chapter_draft)
    chapter_observe = sub.add_parser("chapter-observation-ingest")
    chapter_observe.add_argument("--chapter-id", required=True)
    chapter_observe.add_argument("--file", required=True)
    chapter_observe.set_defaults(func=cmd_chapter_observe_ingest)
    chapter_observe_dispatch = sub.add_parser("chapter-observe")
    chapter_observe_dispatch.add_argument("--chapter-id", required=True)
    chapter_observe_dispatch.set_defaults(func=cmd_chapter_observe)
    chapter_audit = sub.add_parser("chapter-audit")
    chapter_audit.add_argument("--chapter-id", required=True)
    chapter_audit.add_argument("--model", default="Gemini 3.5 Flash (High)")
    chapter_audit.set_defaults(func=cmd_chapter_audit)
    chapter_audit_ingest = sub.add_parser("chapter-audit-ingest")
    chapter_audit_ingest.add_argument("--chapter-id", required=True)
    chapter_audit_ingest.add_argument("--file", required=True)
    chapter_audit_ingest.set_defaults(func=cmd_chapter_audit_ingest)
    chapter_revision = sub.add_parser("chapter-revision-ingest")
    chapter_revision.add_argument("--chapter-id", required=True)
    chapter_revision.add_argument("--file", required=True)
    chapter_revision.set_defaults(func=cmd_chapter_revision_ingest)
    chapter_revision_dispatch = sub.add_parser("chapter-revise")
    chapter_revision_dispatch.add_argument("--chapter-id", required=True)
    chapter_revision_dispatch.set_defaults(func=cmd_chapter_revision)
    chapter_settle = sub.add_parser("chapter-settle")
    chapter_settle.add_argument("--chapter-id", required=True)
    chapter_settle.add_argument("--file", required=True)
    chapter_settle.set_defaults(func=cmd_chapter_settle)
    chapter_settlement_candidate = sub.add_parser("chapter-settlement-candidate")
    chapter_settlement_candidate.add_argument("--chapter-id", required=True)
    chapter_settlement_candidate.set_defaults(func=cmd_chapter_settlement_candidate)
    chapter_run = sub.add_parser("chapter-run")
    chapter_run.add_argument("--intent-file", required=True)
    chapter_run.add_argument("--audit-model", default="Gemini 3.5 Flash (High)")
    chapter_run.set_defaults(func=cmd_chapter_run)
    sub.add_parser("model-routing-status").set_defaults(func=cmd_model_routing_status)
    sub.add_parser("direct-writer-calibration-status").set_defaults(func=cmd_direct_writer_calibration_status)
    direct_calibration = sub.add_parser("direct-writer-calibration-run")
    direct_calibration.add_argument("--timeout-seconds", type=int, default=240)
    direct_calibration.set_defaults(func=cmd_direct_writer_calibration_run)
    sub.add_parser("direct-writer-calibration-review-packet").set_defaults(
        func=cmd_direct_writer_calibration_review_packet
    )
    direct_internal_screen = sub.add_parser("direct-writer-calibration-internal-screen")
    direct_internal_screen.add_argument("--timeout-seconds", type=int, default=240)
    direct_internal_screen.set_defaults(func=cmd_direct_writer_calibration_internal_screen)
    direct_external_blocked = sub.add_parser("direct-writer-calibration-external-blocked")
    direct_external_blocked.add_argument("--reason", required=True)
    direct_external_blocked.set_defaults(func=cmd_direct_writer_calibration_external_blocked)
    sub.add_parser("direct-writer-calibration-decision-packet").set_defaults(
        func=cmd_direct_writer_calibration_decision_packet
    )
    direct_decision_record = sub.add_parser("direct-writer-calibration-decision-record")
    direct_decision_record.add_argument("--file", required=True)
    direct_decision_record.set_defaults(func=cmd_direct_writer_calibration_decision_record)
    chapter_accept = sub.add_parser("chapter-accept")
    chapter_accept.add_argument("--chapter-id", required=True)
    chapter_accept.set_defaults(func=cmd_chapter_accept)
    sub.add_parser("antigravity-bridge-status").set_defaults(
        func=cmd_antigravity_bridge_status
    )
    antigravity_bridge_ask = sub.add_parser("antigravity-bridge-ask")
    antigravity_bridge_ask.add_argument("--request-file", required=True)
    antigravity_bridge_ask.add_argument("--output-file")
    antigravity_bridge_ask.add_argument("--print-timeout", default="5m0s")
    antigravity_bridge_ask.add_argument("--model")
    antigravity_bridge_ask.set_defaults(func=cmd_antigravity_bridge_ask)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)
    sub.add_parser("advance").set_defaults(func=cmd_advance)
    owner = sub.add_parser("owner-gate")
    owner_sub = owner.add_subparsers(dest="owner_gate_command", required=True)
    owner_record = owner_sub.add_parser("record")
    owner_record.add_argument("--decision-id", required=True)
    owner_record.add_argument(
        "--decision-type",
        required=True,
        choices=sorted(DECISION_TYPES),
    )
    owner_record.add_argument("--authorized-scope", action="append", required=True)
    owner_record.add_argument("--forbidden-scope", action="append", required=True)
    owner_record.add_argument("--expires-after-mission", required=True)
    owner_record.add_argument("--owner-note", default="")
    owner_record.add_argument("--bound-response-sha256")
    owner_record.set_defaults(func=cmd_owner_gate_record)
    owner_sub.add_parser("list").set_defaults(func=cmd_owner_gate_list)
    compile_context = sub.add_parser("compile-context")
    compile_context.add_argument("--agent", required=True, choices=["hermes", "antigravity"])
    compile_context.set_defaults(func=cmd_compile_context)
    sub.add_parser("studio-build").set_defaults(func=cmd_studio_build)
    studio_serve = sub.add_parser("studio-serve")
    studio_serve.add_argument("--host", default="127.0.0.1")
    studio_serve.add_argument("--port", type=int, default=4173)
    studio_serve.set_defaults(func=cmd_studio_serve)
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
