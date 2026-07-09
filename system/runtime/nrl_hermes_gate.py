from __future__ import annotations

import json
from typing import Any

from nrl_creation_schemas import validate_creation_asset_store
from nrl_corpus_pipeline import validate_all_evidence_packs
from nrl_corpus_ingestion import load_promoted_review_assets
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


def _load_store() -> dict[str, Any]:
    path = runtime_path("system/creation_assets/project_assets.v0.2.json")
    if not path.exists():
        return {"assets": []}
    return json.loads(path.read_text(encoding="utf-8"))


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
    checks = {
        "research_review_promoted": bool(
            promoted
            and promoted.get("book_review_count") == 18
            and promoted.get("cross_book_mechanism_count", 0) >= 3
            and promoted.get("family_count") == 9
        ),
        "creation_store_valid": bool(store_validation["valid"]),
        "all_creation_families_seeded": all(count > 0 for count in family_counts.values()),
        "evidence_packs_valid": bool(
            evidence["valid"] and evidence["valid_family_count"] == len(FAMILIES)
        ),
        "content_generation_authorized": False,
        "owner_gate_required": owner_gate_required,
        "hermes_paused": True,
    }
    ready = all(
        checks[key]
        for key in (
            "research_review_promoted",
            "creation_store_valid",
            "all_creation_families_seeded",
            "evidence_packs_valid",
        )
    ) and not checks["content_generation_authorized"] and not owner_gate_required
    return {
        "version": "0.1",
        "status": "ready_for_hermes_authorization" if ready else "blocked_on_final_asset_owner_gate",
        "ready_to_call_hermes": ready,
        "project": state.get("selected_project", "UNKNOWN_PROJECT"),
        "checks": checks,
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
            "status": "paused_not_removed",
            "allowed": False,
        },
        "next_required_action": (
            "Owner must explicitly authorize final creative asset generation and Hermes writing."
            if not ready
            else "Prepare the Hermes writing handoff packet; do not bypass the final content contract."
        ),
        "forbidden_actions": [
            "execute_hermes",
            "generate_novel_prose",
            "generate_final_creation_assets",
            "bypass_owner_gate",
            "read_raw_novel_training_set",
        ],
    }
