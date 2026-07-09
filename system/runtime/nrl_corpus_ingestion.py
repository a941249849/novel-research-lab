from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from nrl_full_corpus_proof import build_proof_status
from nrl_paths import ROOT, runtime_path


VERSION = "0.14"
JOB_ID = "job-v07-full-corpus-antigravity-review"
SOURCE_PATH = runtime_path(
    "system/agent_ops/outbox/job-v07-full-corpus-antigravity-review_validated.md"
)
VALIDATION_PATH = runtime_path(
    "system/agent_ops/validation/job-v07-full-corpus-antigravity-review_validation.json"
)
OUTPUT_PATH = runtime_path(
    "system/research_assets/promotions/full_corpus_review_assets.v0.10.json"
)
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


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _extract_manifest(text: str) -> dict[str, Any]:
    match = re.search(r"## JSON Manifest\s*```json\s*(.*?)\s*```", text, re.DOTALL)
    if not match:
        raise RuntimeError("validated full-corpus review is missing JSON Manifest")
    try:
        manifest = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"validated full-corpus review has invalid JSON: {error}") from error
    if not isinstance(manifest, dict):
        raise RuntimeError("validated full-corpus review manifest must be an object")
    return manifest


def _load_source_manifest() -> dict[str, Any]:
    if not SOURCE_PATH.exists():
        raise RuntimeError(f"validated full-corpus review is missing: {_relative(SOURCE_PATH)}")
    if not VALIDATION_PATH.exists():
        raise RuntimeError(f"full-corpus review validation is missing: {_relative(VALIDATION_PATH)}")
    validation = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
    if validation.get("valid") is not True or validation.get("job_id") != JOB_ID:
        raise RuntimeError("full-corpus review must pass its validation contract before ingestion")
    manifest = _extract_manifest(SOURCE_PATH.read_text(encoding="utf-8"))
    expected = {
        "job_id": JOB_ID,
        "contract_version": "0.7",
        "review_scope": "full_remaining_corpus",
        "architecture_version": "0.4",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise RuntimeError(f"full-corpus review manifest {key} must be {value}")
    if len(manifest.get("book_reviews", [])) != 18:
        raise RuntimeError("full-corpus review must contain exactly 18 book reviews")
    if len(manifest.get("cross_book_mechanisms", [])) < 3:
        raise RuntimeError("full-corpus review must contain cross-book mechanisms")
    family_evidence = manifest.get("asset_family_evidence")
    if not isinstance(family_evidence, dict) or set(family_evidence) != set(FAMILIES):
        raise RuntimeError("full-corpus review must cover all nine creation families")
    encoded = json.dumps(manifest, ensure_ascii=False)
    if "novel_training_set/" in encoded:
        raise RuntimeError("validated research artifact contains a raw corpus path")
    return manifest


def build_promoted_review_assets() -> dict[str, Any]:
    manifest = _load_source_manifest()
    proof = build_proof_status()
    readiness = proof["promotion_readiness"]
    if not readiness.get("promotion_allowed"):
        raise RuntimeError("full-corpus proof promotion must be authorized before review ingestion")
    owner_decision_id = str(readiness.get("owner_decision_id", ""))
    if not owner_decision_id:
        raise RuntimeError("full-corpus review ingestion requires an owner decision")
    output = {
        "version": VERSION,
        "asset_id": "full-corpus-review-assets-v014",
        "promotion_state": "promoted_research_asset",
        "source_review_job_id": JOB_ID,
        "source_artifact": _relative(SOURCE_PATH),
        "source_artifact_sha256": _sha256(SOURCE_PATH),
        "validation_artifact": _relative(VALIDATION_PATH),
        "owner_decision_id": owner_decision_id,
        "book_reviews": manifest["book_reviews"],
        "cross_book_mechanisms": manifest["cross_book_mechanisms"],
        "asset_family_evidence": manifest["asset_family_evidence"],
        "originality_risks": manifest.get("originality_risks", []),
        "recommended_next_ingestion": manifest.get("recommended_next_ingestion", {}),
        "book_review_count": len(manifest["book_reviews"]),
        "cross_book_mechanism_count": len(manifest["cross_book_mechanisms"]),
        "family_count": len(FAMILIES),
        "content_generation_allowed": False,
        "hermes_execution_allowed": False,
        "raw_corpus_allowed": False,
        "guardrails": [
            "Structured review derivatives only",
            "No raw novel prose",
            "No final creative assets",
            "No Hermes execution",
            "Family promotion requires schema and validation gates",
        ],
    }
    encoded = json.dumps(output, ensure_ascii=False)
    if "novel_training_set/" in encoded:
        raise RuntimeError("promoted review asset contains a raw corpus path")
    return output


def write_promoted_review_assets() -> dict[str, Any]:
    output = build_promoted_review_assets()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "version": VERSION,
        "status": "promoted_research_review_ingested",
        "output_path": _relative(OUTPUT_PATH),
        "book_review_count": output["book_review_count"],
        "cross_book_mechanism_count": output["cross_book_mechanism_count"],
        "family_count": output["family_count"],
        "owner_decision_id": output["owner_decision_id"],
        "content_generation_allowed": False,
    }


def load_promoted_review_assets() -> dict[str, Any] | None:
    if not OUTPUT_PATH.exists():
        return None
    data = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    if data.get("version") != VERSION or data.get("promotion_state") != "promoted_research_asset":
        return None
    encoded = json.dumps(data, ensure_ascii=False)
    if "novel_training_set/" in encoded:
        raise RuntimeError("promoted review asset contains a raw corpus path")
    return data
