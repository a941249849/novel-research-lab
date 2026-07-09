from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_paths import runtime_path
from nrl_research_assets import build_research_asset_catalog


VERSION = "0.5"
REGISTRY_PATH = runtime_path("system/dna_registry/dna_registry.v0.5.json")
FAMILY_BY_ASSET_TYPE = {
    "book_dna": "book_dna",
    "narrative_dna": "narrative_dna",
    "mechanism": "mechanism_dna",
    "mechanism_notes": "mechanism_dna",
    "state_ledger": "state_dna",
}


def _promotion_state(item: dict[str, Any]) -> str:
    provenance = str(item.get("provenance", ""))
    review_state = str(item.get("review_state", ""))
    if provenance == "promoted" or review_state == "formal":
        return "promoted"
    if provenance == "candidate" or "candidate" in review_state:
        return "candidate"
    if not item.get("exists", True):
        return "blocked"
    return "stub"


def _dna_id(item: dict[str, Any], family: str) -> str:
    source_id = str(item.get("asset_id", "")).replace("_", "-")
    return f"dna-v05-{family}-{source_id}"


def _entry_from_research_item(item: dict[str, Any]) -> dict[str, Any]:
    asset_type = str(item["asset_type"])
    family = FAMILY_BY_ASSET_TYPE[asset_type]
    source_path = str(item["source_path"])
    if "novel_training_set/" in source_path:
        raise RuntimeError(f"raw corpus path is forbidden in DNA Registry: {source_path}")
    categories = [str(category) for category in item.get("categories", [])]
    evidence_tags = sorted(
        {
            asset_type,
            *categories,
            str(item.get("review_state", "unknown")),
            str(item.get("provenance", "unknown")),
        }
    )
    return {
        "dna_id": _dna_id(item, family),
        "family": family,
        "title": str(item.get("title", "UNKNOWN_TITLE")),
        "source_path": source_path,
        "review_state": str(item.get("review_state", "unknown")),
        "provenance": str(item.get("provenance", "unknown")),
        "promotion_state": _promotion_state(item),
        "evidence_tags": evidence_tags,
        "blocked_for_generation": True,
    }


def _project_entry(state: dict[str, Any]) -> dict[str, Any]:
    project = str(state.get("selected_project", "UNKNOWN_PROJECT"))
    return {
        "dna_id": "dna-v05-project-current",
        "family": "project_dna",
        "title": project,
        "source_path": "system/mission_controller/current_phase_state.json",
        "review_state": str(state.get("phase_status", "unknown")),
        "provenance": "runtime_state",
        "promotion_state": "blocked",
        "evidence_tags": [
            "current_project",
            str(state.get("current_phase", "unknown")),
            str(state.get("content_progression", state.get("phase_status", "unknown"))),
        ],
        "blocked_for_generation": True,
    }


def _summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    by_family = Counter(str(entry["family"]) for entry in entries)
    by_promotion_state = Counter(str(entry["promotion_state"]) for entry in entries)
    return {
        "total_entries": len(entries),
        "by_family": dict(sorted(by_family.items())),
        "by_promotion_state": dict(sorted(by_promotion_state.items())),
    }


def build_dna_registry(state: dict[str, Any]) -> dict[str, Any]:
    catalog = build_research_asset_catalog()
    entries = [
        _entry_from_research_item(item)
        for item in catalog["items"]
        if str(item.get("asset_type")) in FAMILY_BY_ASSET_TYPE
    ]
    entries.append(_project_entry(state))
    entries = sorted(entries, key=lambda entry: entry["dna_id"])
    encoded = json.dumps(entries, ensure_ascii=False)
    if "novel_training_set/" in encoded:
        raise RuntimeError("DNA Registry includes forbidden raw corpus path")
    return {
        "registry_name": "NRL DNA Registry",
        "version": VERSION,
        "source_of_truth": [
            "phase1/05_review/phase1C_asset_manifest.json",
            "phase1/04_mechanism_library/category_manifest.json",
            "system/mission_controller/current_phase_state.json",
        ],
        "entries": entries,
        "summary": _summary(entries),
        "guardrails": [
            "Structured derivatives only",
            "No raw corpus reads",
            "All entries blocked for generation until promotion workflow authorizes use",
        ],
    }


def write_dna_registry(state: dict[str, Any]) -> dict[str, Any]:
    registry = build_dna_registry(state)
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return registry


def load_or_build_dna_registry(state: dict[str, Any]) -> dict[str, Any]:
    if REGISTRY_PATH.exists():
        with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("version") == VERSION:
            return data
    return write_dna_registry(state)


def registry_path() -> Path:
    return REGISTRY_PATH
