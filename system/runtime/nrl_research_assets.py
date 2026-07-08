from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path


ASSET_MANIFEST = runtime_path("phase1/05_review/phase1C_asset_manifest.json")
MECHANISM_CATEGORIES = runtime_path(
    "phase1/04_mechanism_library/category_manifest.json"
)
ALLOWED_ASSET_TYPES = {
    "book_dna",
    "narrative_dna",
    "state_ledger",
    "mechanism_notes",
}


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _provenance(status: str, path: str) -> str:
    if "candidate" in path or status == "candidate_retained":
        return "candidate"
    if status == "formal":
        return "promoted"
    return "stub"


def _manifest_items() -> list[dict[str, Any]]:
    if not ASSET_MANIFEST.exists():
        return []
    manifest = _read_json(ASSET_MANIFEST)
    items = []
    for index, asset in enumerate(manifest.get("assets", []), start=1):
        path = str(asset.get("path", ""))
        asset_type = str(asset.get("asset_type", ""))
        if asset_type not in ALLOWED_ASSET_TYPES:
            continue
        if "novel_training_set/" in path:
            raise RuntimeError(f"raw corpus path is forbidden in research catalog: {path}")
        items.append(
            {
                "asset_id": f"phase1-{asset_type}-{index:03d}",
                "title": str(asset.get("book") or "跨书机制库"),
                "asset_type": asset_type,
                "source_path": path,
                "review_state": str(asset.get("status", "unknown")),
                "provenance": _provenance(str(asset.get("status", "")), path),
                "categories": [],
                "exists": (ROOT / path).exists(),
            }
        )
    return items


def _mechanism_items() -> list[dict[str, Any]]:
    if not MECHANISM_CATEGORIES.exists():
        return []
    category_manifest = _read_json(MECHANISM_CATEGORIES)
    categories_by_id: dict[str, list[str]] = defaultdict(list)
    mechanism_by_id: dict[str, dict[str, Any]] = {}
    for category in category_manifest.get("categories", []):
        category_name = str(category.get("category", ""))
        for mechanism in category.get("items", []):
            mechanism_id = str(mechanism["mechanism_id"])
            categories_by_id[mechanism_id].append(category_name)
            mechanism_by_id[mechanism_id] = mechanism

    source_path = str(category_manifest.get("source", ""))
    return [
        {
            "asset_id": f"mechanism-{mechanism_id.lower()}",
            "title": str(mechanism["source_book"]),
            "asset_type": "mechanism",
            "source_path": source_path,
            "review_state": "formal",
            "provenance": "promoted",
            "categories": sorted(categories_by_id[mechanism_id]),
            "mechanism_id": mechanism_id,
            "mechanism_name": str(mechanism["mechanism_name"]),
            "exists": (ROOT / source_path).exists(),
        }
        for mechanism_id, mechanism in sorted(mechanism_by_id.items())
    ]


def build_research_asset_catalog(
    filters: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    filters = filters or {}
    all_items = _manifest_items() + _mechanism_items()
    if any(not item["exists"] for item in all_items):
        missing = [item["source_path"] for item in all_items if not item["exists"]]
        raise RuntimeError(f"research catalog source paths missing: {sorted(set(missing))}")

    items = all_items
    title = filters.get("title")
    asset_type = filters.get("asset_type")
    category = filters.get("category")
    review_state = filters.get("review_state")
    if title:
        items = [item for item in items if item["title"] == title]
    if asset_type:
        items = [item for item in items if item["asset_type"] == asset_type]
    if category:
        items = [item for item in items if category in item["categories"]]
    if review_state:
        items = [item for item in items if item["review_state"] == review_state]

    items = sorted(items, key=lambda item: item["asset_id"])
    counts = Counter(item["asset_type"] for item in items)
    return {
        "catalog_name": "NRL Research Asset Catalog",
        "version": "0.2",
        "source_of_truth": [
            "phase1/05_review/phase1C_asset_manifest.json",
            "phase1/04_mechanism_library/category_manifest.json",
        ],
        "filters": {key: value for key, value in filters.items() if value},
        "items": items,
        "summary": {
            "total_indexed": len(all_items),
            "returned": len(items),
            "by_type": dict(sorted(counts.items())),
        },
        "guardrails": [
            "Structured Phase 1 derivatives only",
            "No raw corpus reads",
            "Every item retains source provenance",
        ],
    }
