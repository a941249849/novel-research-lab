from __future__ import annotations

import json
from typing import Any

from nrl_creation_schemas import validate_creation_asset_store
from nrl_corpus_pipeline import validate_all_evidence_packs
from nrl_corpus_ingestion import load_promoted_review_assets
from nrl_owner_gate import load_decisions
from nrl_paths import runtime_path


FAMILIES = (
    "characters",
    "npcs",
    "factions",
    "artifacts",
    "techniques",
    "naming",
    "emotional_bonds",
    "foreshadowing",
    "state_ledger",
)
FINAL_ASSET_DECISION_TYPE = "authorize_final_asset_generation"
FINAL_ASSET_SCOPE = "generate_final_creation_assets"
FINAL_ASSET_MISSION = "phase2f_final_asset_generation"
FINAL_ASSET_PROMOTION_PATH = runtime_path(
    "system/creation_assets/promotions/hermes_final_asset_bundle_v0.15.json"
)


def _load_store() -> dict[str, Any]:
    path = runtime_path("system/creation_assets/project_assets.v0.2.json")
    if not path.exists():
        return {"assets": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _final_assets_promoted() -> bool:
    if not FINAL_ASSET_PROMOTION_PATH.exists():
        return False
    try:
        manifest = json.loads(FINAL_ASSET_PROMOTION_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return manifest.get("promotion_state") == "promoted_final_creation_assets"


def latest_final_asset_generation_decision(
    decisions: list[dict[str, Any]],
) -> dict[str, Any] | None:
    for decision in reversed(decisions):
        if decision.get("decision_type") != FINAL_ASSET_DECISION_TYPE:
            continue
        if FINAL_ASSET_SCOPE not in set(decision.get("authorized_scope", [])):
            continue
        if decision.get("expires_after_mission") != FINAL_ASSET_MISSION:
            continue
        return decision
    return None


def build_hermes_readiness(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    promoted = load_promoted_review_assets()
    store = _load_store()
    store_validation = validate_creation_asset_store(store)
    family_counts = {family: 0 for family in FAMILIES}
    for asset in store.get("assets", []):
        if isinstance(asset, dict) and asset.get("family") in family_counts:
            family_counts[str(asset["family"])] += 1
    evidence = validate_all_evidence_packs(state, adapters)
    hermes = adapters.get("hermes", {})
    owner_gate_required = bool(state.get("owner_gate_required", True))
    authorization = latest_final_asset_generation_decision(load_decisions())
    final_assets_promoted = _final_assets_promoted()
    prerequisites_ready = all(
        (
            bool(
                promoted
                and promoted.get("book_review_count") == 18
                and promoted.get("cross_book_mechanism_count", 0) >= 3
                and promoted.get("family_count") == 9
            ),
            bool(store_validation["valid"]),
            all(count > 0 for count in family_counts.values()),
            bool(evidence["valid"] and evidence["valid_family_count"] == len(FAMILIES)),
        )
    )
    final_asset_generation_ready = (
        prerequisites_ready and authorization is not None and not final_assets_promoted
    )
    checks = {
        "research_review_promoted": bool(promoted) and promoted.get("book_review_count") == 18,
        "creation_store_valid": bool(store_validation["valid"]),
        "all_creation_families_seeded": all(count > 0 for count in family_counts.values()),
        "evidence_packs_valid": bool(
            evidence["valid"] and evidence["valid_family_count"] == len(FAMILIES)
        ),
        "final_asset_generation_authorized": authorization is not None,
        "final_assets_promoted": final_assets_promoted,
        "content_generation_authorized": False,
        "owner_gate_required": owner_gate_required,
        "hermes_paused": not final_asset_generation_ready,
    }
    return {
        "version": "0.1",
        "status": (
            "final_assets_promoted_awaiting_prose_owner_gate"
            if final_assets_promoted
            else (
                "ready_for_final_asset_generation"
                if final_asset_generation_ready
                else "blocked_on_final_asset_owner_gate"
            )
        ),
        "ready_to_call_hermes": final_asset_generation_ready,
        "project": state.get("selected_project", "UNKNOWN_PROJECT"),
        "checks": checks,
        "owner_authorization": {
            "decision_id": authorization.get("decision_id") if authorization else None,
            "authorized_scope": list(authorization.get("authorized_scope", []))
            if authorization
            else [],
            "prose_authorized": False,
        },
        "research_review": {
            "book_review_count": promoted.get("book_review_count", 0) if promoted else 0,
            "cross_book_mechanism_count": promoted.get("cross_book_mechanism_count", 0)
            if promoted
            else 0,
            "family_count": promoted.get("family_count", 0) if promoted else 0,
        },
        "creation_families": family_counts,
        "hermes": {
            "declared_mode": hermes.get("mode", "manual_handoff"),
            "status": (
                "final_asset_generation_authorized"
                if final_asset_generation_ready
                else (
                    "paused_awaiting_prose_owner_gate"
                    if final_assets_promoted
                    else "paused_not_removed"
                )
            ),
            "allowed": final_asset_generation_ready,
            "allowed_actions": (
                [FINAL_ASSET_SCOPE] if final_asset_generation_ready else []
            ),
        },
        "next_required_action": (
            "Owner must explicitly authorize a bounded controlled prose test."
            if final_assets_promoted
            else (
                "Generate and validate the nine final creation asset families before any prose test."
                if final_asset_generation_ready
                else "Owner must explicitly authorize final creative asset generation."
            )
        ),
        "forbidden_actions": [
            "generate_novel_prose",
            "bypass_owner_gate",
            "read_raw_novel_training_set",
        ]
        + (
            []
            if final_asset_generation_ready
            else ["execute_hermes", "generate_final_creation_assets"]
        ),
    }
