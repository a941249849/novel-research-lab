from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_creation_schemas import FAMILIES, validate_creation_asset_store
from nrl_paths import runtime_path

REGISTRY_PATH = runtime_path("system/creation_assets/creation_asset_registry.v0.1.json")
PROJECT_ASSET_STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
ALLOWED_STATUSES = {"missing", "seed", "partial"}
EXPECTED_ASSET_IDS = {
    "characters",
    "npcs",
    "factions",
    "artifacts",
    "techniques",
    "naming",
    "emotional_bonds",
    "foreshadowing",
    "state_ledger",
}

DEEP_READ_VALIDATION_PATH = runtime_path(
    "system/research_assets/deep_read/v0.18/validation.json"
)
DEEP_READ_SYNTHESIS_VALIDATION_PATH = runtime_path(
    "system/research_assets/deep_read/v0.18/synthesis_validation.json"
)
DEEP_READ_CROSS_VALIDATION_PATH = runtime_path(
    "system/research_assets/deep_read/v0.18/cross_validation.json"
)
RECONCILIATION_VALIDATION_PATH = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json"
)
RECONCILIATION_APPLICATION_PATH = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_application_v0.19.json"
)
OWNER_DECISIONS_PATH = runtime_path("system/runtime/owner_gate_decisions.json")
ADVISORY_REVIEW_PATH = runtime_path(
    ".agent-handoff/antigravity/responses/nrl-v020-asset-graph-review.md"
)
ADVISORY_REREVIEW_PATH = runtime_path(
    ".agent-handoff/antigravity/responses/nrl-v020-asset-graph-rereview.md"
)


def _load_registry_artifact(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate_family(family: dict[str, Any]) -> None:
    asset_id = family.get("asset_id")
    status = family.get("status")
    if asset_id not in EXPECTED_ASSET_IDS:
        raise RuntimeError(f"unexpected creation asset family: {asset_id}")
    if status not in ALLOWED_STATUSES:
        raise RuntimeError(f"invalid creation asset status for {asset_id}: {status}")
    score = family.get("readiness_score")
    if not isinstance(score, int) or score < 0 or score > 100:
        raise RuntimeError(f"invalid readiness_score for {asset_id}: {score}")


def _coverage_summary(families: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(family["status"]) for family in families)
    return {
        "total": len(families),
        "by_status": dict(sorted(counts.items())),
        "complete": 0,
        "lowest_readiness": min(int(family["readiness_score"]) for family in families),
        "highest_readiness": max(int(family["readiness_score"]) for family in families),
    }


def load_creation_asset_registry(project: str, mode: str) -> dict[str, Any]:
    artifact = _load_registry_artifact()
    families = artifact.get("asset_families", [])
    if not isinstance(families, list):
        raise RuntimeError("creation asset registry asset_families must be a list")
    project_asset_counts: Counter[str] = Counter()
    if PROJECT_ASSET_STORE_PATH.exists():
        with PROJECT_ASSET_STORE_PATH.open("r", encoding="utf-8") as handle:
            store = json.load(handle)
        for asset in store.get("assets", []):
            if isinstance(asset, dict):
                project_asset_counts[str(asset.get("family", "unknown"))] += 1
    for family in families:
        _validate_family(family)
        family_id = str(family["asset_id"])
        asset_count = project_asset_counts.get(family_id, 0)
        if asset_count and family["status"] == "missing":
            family["status"] = "seed"
            family["readiness_score"] = max(int(family["readiness_score"]), 20)
            family["known_support"] = list(family.get("known_support", [])) + [
                f"Project asset store contains {asset_count} schema-bound seed asset(s)."
            ]
        family["project_asset_count"] = asset_count
    family_ids = {str(family["asset_id"]) for family in families}
    if family_ids != EXPECTED_ASSET_IDS:
        missing = sorted(EXPECTED_ASSET_IDS - family_ids)
        extra = sorted(family_ids - EXPECTED_ASSET_IDS)
        raise RuntimeError(f"creation asset registry family mismatch: missing={missing}, extra={extra}")
    return {
        "registry_name": "Creation Asset Registry",
        "version": str(artifact.get("version", "0.1")),
        "project": project,
        "mode": mode,
        "source_of_truth": [
            "system/creation_assets/creation_asset_registry.v0.1.json",
            "system/mission_controller/current_phase_state.json",
            "system/runtime/mission_registry.json",
        ],
        "asset_families": families,
        "coverage_summary": _coverage_summary(families),
        "guardrails": [
            "No family is complete in v0.1",
            "Do not generate novel prose",
            "Do not generate full character cards",
            "Do not generate final NPC sheets, faction dossiers, technique trees, naming dictionaries, or item catalogs",
            "Do not read raw novel_training_set/",
            "Do not call Hermes or dispatch Antigravity outside registered CLI review jobs",
        ],
        "next_safe_action": "Use the registry to design schemas and validation before any content progression.",
    }


def _load_json_if_present(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def _load_decisions() -> list[dict[str, Any]]:
    if not OWNER_DECISIONS_PATH.exists():
        return []
    with OWNER_DECISIONS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []


def _reference_rows(assets: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for asset in assets:
        source_id = str(asset.get("asset_id", ""))
        family = str(asset.get("family", ""))
        for relationship in asset.get("relationships", []):
            if isinstance(relationship, dict):
                rows.append(
                    {
                        "source_id": source_id,
                        "source_family": family,
                        "target_id": str(relationship.get("target_id", "")),
                        "reference_kind": "relationship",
                        "relation_type": str(relationship.get("relation_type", "")),
                    }
                )
        technique = asset.get("technique")
        if isinstance(technique, dict):
            for target_id in technique.get("counter_ids", []):
                rows.append(
                    {
                        "source_id": source_id,
                        "source_family": family,
                        "target_id": str(target_id),
                        "reference_kind": "technique_counter",
                        "relation_type": "counter",
                    }
                )
    return rows


def _reference_summary(
    references: list[dict[str, str]], asset_ids: set[str]
) -> dict[str, Any]:
    resolved = [row for row in references if row["target_id"] in asset_ids]
    unresolved = [row for row in references if row["target_id"] not in asset_ids]
    return {
        "total": len(references),
        "resolved_count": len(resolved),
        "unresolved_count": len(unresolved),
        "resolved": resolved,
        "unresolved": unresolved,
    }


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+(?:\d+\.\s+)?{re.escape(heading)}\s*$\n(.*?)(?=^##\s+(?:\d+\.\s+)?|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def _parse_advisory_review(text: str | None = None) -> dict[str, Any]:
    path = ADVISORY_REVIEW_PATH
    if text is None:
        if ADVISORY_REREVIEW_PATH.exists():
            path = ADVISORY_REREVIEW_PATH
        text = path.read_text(encoding="utf-8") if path.exists() else ""
    verdict_section = _section(text, "VERDICT")
    verdict_match = re.search(r"\b(ACCEPT_WITH_WARNINGS|REWORK_REQUIRED|ACCEPT)\b", verdict_section)
    integrity_section = _section(text, "CROSS_ASSET_INTEGRITY")
    findings = []
    for line in integrity_section.splitlines():
        match = re.match(r"^-\s+\*\*(.+?)\*\*:\s*(.+)$", line.strip())
        if match:
            findings.append({"name": match.group(1), "details": match.group(2)})
    remaining_blockers = []
    for line in _section(text, "REMAINING_BLOCKERS").splitlines():
        cleaned = line.strip().lstrip("-").strip()
        if cleaned and not re.match(r"^none(?:\.|$)", cleaned, re.IGNORECASE):
            remaining_blockers.append(cleaned)
    remediations = []
    for line in _section(text, "REQUIRED_REMEDIATIONS").splitlines():
        match = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if match:
            remediations.append(match.group(1))
    return {
        "path": str(path.relative_to(runtime_path("."))),
        "available": bool(text.strip()),
        "verdict": verdict_match.group(1) if verdict_match else "MISSING",
        "named_unresolved_risks": remaining_blockers or findings,
        "required_remediations": remediations,
        "serial_prose_blockers": _section(text, "SERIAL_PROSE_BLOCKERS"),
        "prose_gate_recommendation": _section(text, "PROSE_GATE_RECOMMENDATION"),
    }


def _readiness_evidence() -> dict[str, Any]:
    chunks = _load_json_if_present(DEEP_READ_VALIDATION_PATH)
    synthesis = _load_json_if_present(DEEP_READ_SYNTHESIS_VALIDATION_PATH)
    cross = _load_json_if_present(DEEP_READ_CROSS_VALIDATION_PATH)
    chunk_ready = bool(
        chunks.get("status") == "chunk_coverage_verified"
        and chunks.get("validated_chunk_count") == chunks.get("required_chunk_count")
        and chunks.get("validated_byte_ratio") == 1.0
    )
    synthesis_ready = bool(
        synthesis.get("valid") is True
        and synthesis.get("validated_book_count") == synthesis.get("required_book_count")
    )
    cross_ready = cross.get("valid") is True

    reconciliation = _load_json_if_present(RECONCILIATION_VALIDATION_PATH)
    application = _load_json_if_present(RECONCILIATION_APPLICATION_PATH)
    validation_ready = bool(
        reconciliation.get("valid") is True
        and reconciliation.get("verdict") in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
    )
    application_ready = application.get("status") == "applied"
    return {
        "v0.18": {
            "ready": chunk_ready and synthesis_ready and cross_ready,
            "chunk_coverage": {
                "ready": chunk_ready,
                "status": chunks.get("status", "missing"),
                "validated_chunk_count": chunks.get("validated_chunk_count", 0),
                "required_chunk_count": chunks.get("required_chunk_count", 0),
                "validated_byte_ratio": chunks.get("validated_byte_ratio", 0),
                "path": "system/research_assets/deep_read/v0.18/validation.json",
            },
            "book_synthesis": {
                "ready": synthesis_ready,
                "valid": synthesis.get("valid", False),
                "validated_book_count": synthesis.get("validated_book_count", 0),
                "required_book_count": synthesis.get("required_book_count", 0),
                "path": "system/research_assets/deep_read/v0.18/synthesis_validation.json",
            },
            "cross_book_distillation": {
                "ready": cross_ready,
                "valid": cross.get("valid", False),
                "path": "system/research_assets/deep_read/v0.18/cross_validation.json",
            },
        },
        "v0.19": {
            "ready": validation_ready and application_ready,
            "reconciliation_validation": {
                "ready": validation_ready,
                "valid": reconciliation.get("valid", False),
                "verdict": reconciliation.get("verdict", "missing"),
                "path": "system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json",
            },
            "reconciliation_application": {
                "ready": application_ready,
                "status": application.get("status", "missing"),
                "owner_decision_id": application.get("owner_decision_id"),
                "applied_asset_ids": application.get("applied_asset_ids", []),
                "path": "system/agent_ops/validation/borrowed_heaven_project_reconciliation_application_v0.19.json",
            },
        },
    }


def build_creation_asset_graph_status(
    store: dict[str, Any] | None = None,
    *,
    decisions: list[dict[str, Any]] | None = None,
    advisory_review_text: str | None = None,
) -> dict[str, Any]:
    """Build a read-only status view of the current creation asset graph."""
    store = store if store is not None else _load_json_if_present(PROJECT_ASSET_STORE_PATH)
    assets = [item for item in store.get("assets", []) if isinstance(item, dict)]
    validation = validate_creation_asset_store(store)
    asset_ids = {str(asset.get("asset_id", "")) for asset in assets}
    references = _reference_rows(assets)
    reference_summary = _reference_summary(references, asset_ids)
    family_ids = {str(asset.get("family", "")) for asset in assets}
    exact_family_coverage = family_ids == set(FAMILIES)

    families = []
    for family in FAMILIES:
        family_assets = [asset for asset in assets if asset.get("family") == family]
        states = Counter(str(asset.get("lifecycle_state", "unknown")) for asset in family_assets)
        family_references = [row for row in references if row["source_family"] == family]
        families.append(
            {
                "family": family,
                "total": len(family_assets),
                "active": states.get("active", 0),
                "seed": states.get("seed", 0),
                "lifecycle_states": dict(sorted(states.items())),
                "cross_asset_references": _reference_summary(family_references, asset_ids),
            }
        )

    evidence = _readiness_evidence()
    advisory = _parse_advisory_review(advisory_review_text)
    decisions = decisions if decisions is not None else _load_decisions()
    asset_authorizations = [
        item
        for item in decisions
        if item.get("decision_type") == "authorize_final_asset_generation"
    ]
    prose_authorizations = [
        item
        for item in decisions
        if item.get("decision_type") == "authorize_controlled_prose_test"
    ]

    graph_valid = bool(
        validation.get("valid")
        and exact_family_coverage
        and reference_summary["unresolved_count"] == 0
    )
    blockers = []
    if not validation.get("valid"):
        blockers.append("creation_schema_validation_failed")
    if not exact_family_coverage:
        blockers.append("exact_nine_family_coverage_missing")
    if reference_summary["unresolved_count"]:
        blockers.append("unresolved_cross_asset_references")
    if not evidence["v0.18"]["ready"]:
        blockers.append("v0.18_readiness_unverified")
    if not evidence["v0.19"]["ready"]:
        blockers.append("v0.19_readiness_unverified")
    if not advisory["available"]:
        blockers.append("antigravity_advisory_review_missing")
    if advisory["verdict"] == "REWORK_REQUIRED":
        blockers.append("antigravity_review_requires_rework")
    elif advisory["verdict"] not in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}:
        blockers.append("antigravity_review_not_accepted")
    if advisory["named_unresolved_risks"]:
        blockers.append("named_advisory_risks_unresolved")

    production_ready = not blockers
    return {
        "graph_name": "NRL Creation Asset Graph Status",
        "version": "0.20",
        "project": store.get("project", "UNKNOWN_PROJECT"),
        "read_only": True,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "graph_valid": graph_valid,
        "schema_validation": validation,
        "exact_family_coverage": exact_family_coverage,
        "family_count": len(families),
        "families": families,
        "summary": {
            "total": len(assets),
            "active": sum(1 for asset in assets if asset.get("lifecycle_state") == "active"),
            "seed": sum(1 for asset in assets if asset.get("lifecycle_state") == "seed"),
            "lifecycle_states": dict(
                sorted(Counter(str(asset.get("lifecycle_state", "unknown")) for asset in assets).items())
            ),
            "cross_asset_references": reference_summary,
        },
        "readiness_evidence": evidence,
        "advisory_review": advisory,
        "authorization": {
            "asset_authorization_present": bool(asset_authorizations),
            "asset_authorization_decision_ids": [item.get("decision_id") for item in asset_authorizations],
            "controlled_prose_authorization_present": bool(prose_authorizations),
            "controlled_prose_authorization_decision_ids": [item.get("decision_id") for item in prose_authorizations],
            "prose_generation_allowed": False,
            "reason": "Asset graph status is read-only and never grants prose authorization.",
        },
        "readiness": {
            "status": "asset_baseline_ready" if production_ready else "rework_required",
            "production_ready": production_ready,
            "blockers": blockers,
            "prose_generation_allowed": False,
            "asset_mutation_allowed": False,
            "next_action": (
                "Freeze the reviewed asset baseline. A separate prose gate is still required."
                if production_ready
                else "Create a separate hash-bound remediation task; do not mutate project assets from status inspection."
            ),
        },
    }
