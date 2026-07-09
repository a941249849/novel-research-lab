from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_dna_registry import load_or_build_dna_registry
from nrl_paths import runtime_path


VERSION = "0.5"
INDEX_PATH = runtime_path("system/research_index/research_rag_index.v0.5.json")
WEIGHT_BY_PROMOTION_STATE = {
    "promoted": 3,
    "candidate": 2,
    "stub": 1,
    "blocked": 0,
}


def _retrieval_text(entry: dict[str, Any]) -> str:
    tags = ", ".join(str(tag) for tag in entry.get("evidence_tags", []))
    return " | ".join(
        [
            str(entry["family"]),
            str(entry["title"]),
            str(entry["review_state"]),
            str(entry["promotion_state"]),
            tags,
        ]
    )


def _index_item(entry: dict[str, Any]) -> dict[str, Any]:
    source_path = str(entry["source_path"])
    if "novel_training_set/" in source_path:
        raise RuntimeError(f"raw corpus path is forbidden in RAG Index: {source_path}")
    promotion_state = str(entry.get("promotion_state", "stub"))
    return {
        "index_id": f"rag-v05-{entry['dna_id']}",
        "source_dna_id": str(entry["dna_id"]),
        "source_path": source_path,
        "title": str(entry["title"]),
        "asset_type": str(entry["family"]),
        "mechanism_categories": [
            str(tag)
            for tag in entry.get("evidence_tags", [])
            if str(tag) not in {entry.get("review_state"), entry.get("provenance")}
        ],
        "retrieval_text": _retrieval_text(entry),
        "evidence_weight": WEIGHT_BY_PROMOTION_STATE.get(promotion_state, 1),
    }


def _summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    by_asset_type = Counter(str(item["asset_type"]) for item in items)
    weights = Counter(str(item["evidence_weight"]) for item in items)
    return {
        "total_items": len(items),
        "by_asset_type": dict(sorted(by_asset_type.items())),
        "by_evidence_weight": dict(sorted(weights.items())),
    }


def build_rag_index(state: dict[str, Any]) -> dict[str, Any]:
    registry = load_or_build_dna_registry(state)
    items = [
        _index_item(entry)
        for entry in registry["entries"]
        if str(entry.get("family")) != "project_dna"
    ]
    items = sorted(items, key=lambda item: item["index_id"])
    encoded = json.dumps(items, ensure_ascii=False)
    if "novel_training_set/" in encoded:
        raise RuntimeError("RAG Index includes forbidden raw corpus path")
    return {
        "index_name": "NRL Research RAG Index",
        "version": VERSION,
        "source_of_truth": ["system/dna_registry/dna_registry.v0.5.json"],
        "items": items,
        "summary": _summary(items),
        "guardrails": [
            "Structured DNA metadata only",
            "No raw novel prose",
            "Evidence weights derive from DNA promotion state",
        ],
    }


def write_rag_index(state: dict[str, Any]) -> dict[str, Any]:
    index = build_rag_index(state)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return index


def load_or_build_rag_index(state: dict[str, Any]) -> dict[str, Any]:
    if INDEX_PATH.exists():
        with INDEX_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("version") == VERSION:
            return data
    return write_rag_index(state)


def rag_index_path() -> Path:
    return INDEX_PATH
