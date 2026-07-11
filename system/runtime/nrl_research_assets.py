from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from nrl_full_corpus_proof import build_proof_status
from nrl_corpus_ingestion import load_promoted_review_assets
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
    "corpus_proof",
    "full_corpus_book_review",
    "cross_book_mechanism",
    "creation_family_evidence",
    "verified_book_synthesis",
    "verified_cross_book_mechanism",
}
FULL_CORPUS_PROOF_VALIDATION = runtime_path(
    "system/agent_ops/validation/full_corpus_proof_v0.8.json"
)
FULL_CORPUS_PROOF_MASTER = runtime_path(
    "system/agent_ops/inbox/full_corpus_proof_v0.8/master.md"
)
FULL_CORPUS_REVIEW_ASSETS = runtime_path(
    "system/research_assets/promotions/full_corpus_review_assets.v0.10.json"
)
DEEP_READ_SYNTHESIS_VALIDATION = runtime_path(
    "system/research_assets/deep_read/v0.18/synthesis_validation.json"
)
DEEP_READ_CROSS_VALIDATION = runtime_path(
    "system/research_assets/deep_read/v0.18/cross_validation.json"
)
DEEP_READ_SYNTHESIS_DIR = runtime_path("system/agent_ops/inbox/deep_read_v0.18/synthesis")
DEEP_READ_CROSS_RESPONSE = runtime_path(
    "system/agent_ops/inbox/deep_read_v0.18/cross_book_distillation.json"
)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_agent_json(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").strip()
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    return json.loads(match.group(1) if match else text)


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


def _full_corpus_proof_item() -> list[dict[str, Any]]:
    if not FULL_CORPUS_PROOF_VALIDATION.exists() or not FULL_CORPUS_PROOF_MASTER.exists():
        return []
    validation = _read_json(FULL_CORPUS_PROOF_VALIDATION)
    if validation.get("status") != "proof_verified":
        return []
    proof_status = build_proof_status()
    readiness = proof_status["promotion_readiness"]
    source_path = str(FULL_CORPUS_PROOF_MASTER.relative_to(ROOT))
    validation_path = str(FULL_CORPUS_PROOF_VALIDATION.relative_to(ROOT))
    item = {
        "asset_id": "full-corpus-proof-v08",
        "title": "全量小说集抽样访问证明（历史）",
        "asset_type": "corpus_proof",
        "source_path": source_path,
        "validation_path": validation_path,
        "review_state": "proof_verified",
        "provenance": (
            "promotable_research_asset"
            if readiness["promotion_allowed"]
            else "verified_not_promoted"
        ),
        "categories": ["抽样访问证明", "语料工程", "历史证据"],
        "evidence_scope": "sampled_access_only",
        "deep_read_claim_allowed": False,
        "exists": FULL_CORPUS_PROOF_MASTER.exists(),
        "verified_receipts": int(validation.get("verified_receipts", 0)),
        "required_receipts": int(validation.get("required_receipts", 0)),
        "promotion_allowed": bool(readiness["promotion_allowed"]),
    }
    if readiness.get("owner_decision_id"):
        item["owner_decision_id"] = str(readiness["owner_decision_id"])
    return [item]


def _full_corpus_review_items() -> list[dict[str, Any]]:
    promoted = load_promoted_review_assets()
    if not promoted:
        return []
    source_path = str(promoted["source_artifact"])
    items: list[dict[str, Any]] = []
    for index, review in enumerate(promoted.get("book_reviews", []), start=1):
        if not isinstance(review, dict):
            continue
        items.append(
            {
                "asset_id": f"full-review-book-{index:02d}",
                "title": str(review.get("book_title", "")),
                "asset_type": "full_corpus_book_review",
                "source_path": source_path,
                "review_state": "legacy_unverified",
                "provenance": "legacy_candidate",
                "categories": [
                    str(item) for item in review.get("asset_family_relevance", [])
                ],
                "author": str(review.get("author", "")),
                "read_scope": "legacy_unverified_summary",
                "deep_read_claim_allowed": False,
                "reusable_mechanisms": list(review.get("reusable_mechanisms", [])),
                "exists": FULL_CORPUS_REVIEW_ASSETS.exists(),
            }
        )
    for mechanism in promoted.get("cross_book_mechanisms", []):
        if not isinstance(mechanism, dict):
            continue
        mechanism_id = str(mechanism.get("mechanism_id", ""))
        items.append(
            {
                "asset_id": f"full-review-mechanism-{mechanism_id.lower()}",
                "title": mechanism_id,
                "asset_type": "cross_book_mechanism",
                "source_path": source_path,
                "review_state": "legacy_unverified",
                "provenance": "legacy_candidate",
                "categories": ["跨书机制蒸馏"],
                "mechanism_id": mechanism_id,
                "source_books": list(mechanism.get("source_books", [])),
                "reusable_for_nrl": bool(mechanism.get("reusable_for_NRL", False)),
                "deep_read_claim_allowed": False,
                "exists": FULL_CORPUS_REVIEW_ASSETS.exists(),
            }
        )
    for family, evidence in sorted(promoted.get("asset_family_evidence", {}).items()):
        if not isinstance(evidence, dict):
            continue
        items.append(
            {
                "asset_id": f"full-review-family-{family}",
                "title": family,
                "asset_type": "creation_family_evidence",
                "source_path": source_path,
                "review_state": str(evidence.get("status", "unknown")),
                "provenance": "legacy_candidate",
                "categories": [family, "创作资产证据"],
                "evidence_count": len(evidence.get("evidence", []))
                if isinstance(evidence.get("evidence"), list)
                else 0,
                "deep_read_claim_allowed": False,
                "exists": FULL_CORPUS_REVIEW_ASSETS.exists(),
            }
        )
    return items


def _verified_deep_read_items() -> list[dict[str, Any]]:
    items = []
    synthesis_valid = (
        DEEP_READ_SYNTHESIS_VALIDATION.exists()
        and _read_json(DEEP_READ_SYNTHESIS_VALIDATION).get("valid") is True
    )
    if synthesis_valid:
        for path in sorted(DEEP_READ_SYNTHESIS_DIR.glob("*.json")):
            data = _read_agent_json(path)
            items.append(
                {
                    "asset_id": f"deep-read-{data.get('book_id')}",
                    "title": str(data.get("book_title", "")),
                    "asset_type": "verified_book_synthesis",
                    "source_path": str(path.relative_to(ROOT)),
                    "review_state": "verified",
                    "provenance": "v0.18_hash_bound",
                    "categories": ["单书深读", "九类创作资产证据"],
                    "read_scope": "contiguous_full_text_verified",
                    "deep_read_claim_allowed": True,
                    "exists": True,
                }
            )
    cross_valid = (
        DEEP_READ_CROSS_VALIDATION.exists()
        and _read_json(DEEP_READ_CROSS_VALIDATION).get("valid") is True
        and DEEP_READ_CROSS_RESPONSE.exists()
    )
    if cross_valid:
        cross = _read_agent_json(DEEP_READ_CROSS_RESPONSE)
        for mechanism in cross.get("cross_book_mechanisms", []):
            items.append(
                {
                    "asset_id": f"deep-read-{mechanism.get('mechanism_id')}",
                    "title": str(mechanism.get("name", "")),
                    "asset_type": "verified_cross_book_mechanism",
                    "source_path": str(DEEP_READ_CROSS_RESPONSE.relative_to(ROOT)),
                    "review_state": "verified",
                    "provenance": "v0.18_hash_bound",
                    "categories": ["跨书机制蒸馏"],
                    "source_book_ids": list(mechanism.get("source_book_ids", [])),
                    "deep_read_claim_allowed": True,
                    "exists": True,
                }
            )
    return items


def build_research_asset_catalog(
    filters: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    filters = filters or {}
    all_items = (
        _manifest_items()
        + _mechanism_items()
        + _full_corpus_proof_item()
        + _full_corpus_review_items()
        + _verified_deep_read_items()
    )
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
            "system/agent_ops/inbox/full_corpus_proof_v0.8/master.md",
            "system/agent_ops/validation/full_corpus_proof_v0.8.json",
            "system/research_assets/promotions/full_corpus_review_assets.v0.10.json",
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
