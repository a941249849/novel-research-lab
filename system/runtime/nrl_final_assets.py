from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_creation_schemas import FAMILIES, validate_creation_asset_store
from nrl_hermes_gate import latest_final_asset_generation_decision
from nrl_owner_gate import load_decisions
from nrl_paths import ROOT, runtime_path


VERSION = "0.15"
PROJECT = "《借天改命账》"
INBOX_DIR = runtime_path("system/agent_ops/inbox")
STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
VALIDATION_PATH = runtime_path("system/agent_ops/validation/final_asset_bundle_v0.15.json")
PROMOTION_MANIFEST_PATH = runtime_path(
    "system/creation_assets/promotions/hermes_final_asset_bundle_v0.15.json"
)
ALLOWED_SOURCE_REFS = {
    "phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md",
    "phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md",
    "phase2C/03_codex_validation/phase2C_bible_validation_report.md",
    "phase2C/03_codex_validation/phase2C_antigravity_bible_review_report.md",
    "system/creation_assets/project_assets.v0.2.json",
    "system/creation_assets/schemas/common.schema.json",
    "system/research_assets/evidence_packs/manifest.v0.11.json",
    "system/research_index/creation_context_index.v0.12.json",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RuntimeError(f"JSON object required: {path}")
    return data


def _write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _relative_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _resolve_candidate_path(file_arg: str, require_inbox: bool) -> Path:
    path = Path(file_arg)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve()
    if require_inbox:
        try:
            path.relative_to(INBOX_DIR.resolve())
        except ValueError as error:
            raise RuntimeError(
                "final asset bundle must be placed under system/agent_ops/inbox"
            ) from error
    return path


def _error(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **details}


def validate_final_asset_payload(
    bundle: dict[str, Any], store: dict[str, Any]
) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    assets = bundle.get("assets")
    if bundle.get("version") != VERSION:
        errors.append(_error("bundle_version", f"version must be {VERSION}"))
    if bundle.get("project") != PROJECT:
        errors.append(_error("project_mismatch", f"project must be {PROJECT}"))
    if not isinstance(assets, list):
        errors.append(_error("assets_type", "assets must be a list"))
        assets = []

    family_counts = Counter(
        str(asset.get("family", "")) for asset in assets if isinstance(asset, dict)
    )
    if len(assets) != len(FAMILIES) or set(family_counts) != set(FAMILIES) or any(
        family_counts[family] != 1 for family in FAMILIES
    ):
        errors.append(
            _error(
                "exact_family_coverage",
                "candidate must contain exactly one asset for every creation family",
                family_counts=dict(sorted(family_counts.items())),
            )
        )

    existing_ids = {
        str(asset.get("asset_id", ""))
        for asset in store.get("assets", [])
        if isinstance(asset, dict)
    }
    candidate_ids: set[str] = set()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(_error("asset_type", "asset must be an object", asset_index=index))
            continue
        asset_id = str(asset.get("asset_id", ""))
        if asset_id in candidate_ids:
            errors.append(_error("duplicate_candidate_id", "candidate asset IDs must be unique", asset_id=asset_id))
        candidate_ids.add(asset_id)
        if asset_id in existing_ids:
            errors.append(_error("existing_asset_id", "candidate asset ID already exists", asset_id=asset_id))
        if asset.get("lifecycle_state") != "active":
            errors.append(
                _error(
                    "lifecycle_state",
                    "final candidate assets must have lifecycle_state active",
                    asset_id=asset_id,
                )
            )
        for source_ref in asset.get("source_refs", []):
            if not isinstance(source_ref, str) or source_ref not in ALLOWED_SOURCE_REFS:
                errors.append(
                    _error(
                        "source_boundary",
                        "candidate source reference is outside the approved packet allowlist",
                        asset_id=asset_id,
                        source_ref=source_ref,
                    )
                )

    bundle_text = json.dumps(bundle, ensure_ascii=False)
    if "novel_training_set/" in bundle_text:
        errors.append(
            _error(
                "raw_corpus_boundary",
                "candidate must not contain raw corpus paths",
            )
        )

    combined_store = {**store, "assets": [*store.get("assets", []), *assets]}
    combined_validation = validate_creation_asset_store(combined_store)
    if not combined_validation["valid"]:
        errors.extend(
            _error("creation_schema", item["message"], detail=item)
            for item in combined_validation["errors"]
        )

    return {
        "version": VERSION,
        "valid": not errors,
        "errors": errors,
        "candidate_asset_count": len(assets),
        "candidate_family_counts": dict(sorted(family_counts.items())),
        "combined_asset_count": len(combined_store["assets"]),
        "combined_store_validation": combined_validation,
        "content_generation_allowed": False,
        "forbidden_actions": ["generate_novel_prose", "generate_full_chapter"],
    }


def validate_final_asset_bundle(
    file_arg: str,
    *,
    store_path: Path = STORE_PATH,
    validation_path: Path | None = VALIDATION_PATH,
    require_inbox: bool = True,
) -> dict[str, Any]:
    candidate_path = _resolve_candidate_path(file_arg, require_inbox)
    if not candidate_path.exists():
        result = {
            "version": VERSION,
            "valid": False,
            "errors": [_error("missing_candidate", f"candidate file does not exist: {file_arg}")],
            "content_generation_allowed": False,
        }
    else:
        try:
            bundle = _load_json(candidate_path)
            store = _load_json(store_path)
            already_promoted = _is_matching_promoted_candidate(
                bundle, candidate_path, store, PROMOTION_MANIFEST_PATH
            )
            validation_store = (
                _store_without_candidate_assets(store, bundle) if already_promoted else store
            )
            result = validate_final_asset_payload(bundle, validation_store)
            result["already_promoted"] = already_promoted
        except (json.JSONDecodeError, RuntimeError) as error:
            result = {
                "version": VERSION,
                "valid": False,
                "errors": [_error("invalid_json", str(error))],
                "content_generation_allowed": False,
            }
    result["candidate_path"] = _relative_to_root(candidate_path)
    if validation_path is not None:
        _write_json_atomic(validation_path, result)
        result["validation_path"] = _relative_to_root(validation_path)
    return result


def build_final_asset_promotion_readiness(
    bundle: dict[str, Any], store: dict[str, Any], decisions: list[dict[str, Any]]
) -> dict[str, Any]:
    validation = validate_final_asset_payload(bundle, store)
    decision = latest_final_asset_generation_decision(decisions)
    allowed = validation["valid"] and decision is not None
    return {
        "version": VERSION,
        "status": "ready_to_promote_final_creation_assets" if allowed else "blocked_final_asset_promotion",
        "candidate_valid": validation["valid"],
        "owner_decision_id": decision.get("decision_id") if decision else None,
        "promotion_allowed": allowed,
        "content_generation_allowed": False,
        "forbidden_actions": ["generate_novel_prose", "generate_full_chapter", "bypass_asset_validation"],
        "validation": validation,
    }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_matching_promoted_candidate(
    bundle: dict[str, Any], candidate_path: Path, store: dict[str, Any], manifest_path: Path
) -> bool:
    if not manifest_path.exists():
        return False
    try:
        manifest = _load_json(manifest_path)
    except (json.JSONDecodeError, RuntimeError):
        return False
    candidate_assets = bundle.get("assets")
    if not isinstance(candidate_assets, list):
        return False
    candidate_ids = [asset.get("asset_id") for asset in candidate_assets if isinstance(asset, dict)]
    if manifest.get("promotion_state") != "promoted_final_creation_assets":
        return False
    if manifest.get("candidate_sha256") != _sha256_file(candidate_path):
        return False
    if manifest.get("asset_ids") != candidate_ids:
        return False
    stored_asset_ids = {
        asset.get("asset_id")
        for asset in store.get("assets", [])
        if isinstance(asset, dict)
    }
    # Promoted assets may be enriched by later, separately validated project
    # reconciliation. The immutable promotion manifest proves origin; current
    # presence by ID proves the bundle was not removed or duplicated.
    return all(asset.get("asset_id") in stored_asset_ids for asset in candidate_assets)


def _store_without_candidate_assets(store: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    candidate_ids = {
        asset.get("asset_id") for asset in bundle.get("assets", []) if isinstance(asset, dict)
    }
    return {
        **store,
        "assets": [
            asset for asset in store.get("assets", []) if asset.get("asset_id") not in candidate_ids
        ],
    }


def promote_final_asset_bundle(
    file_arg: str,
    *,
    decisions: list[dict[str, Any]] | None = None,
    store_path: Path = STORE_PATH,
    manifest_path: Path = PROMOTION_MANIFEST_PATH,
    validation_path: Path = VALIDATION_PATH,
    require_inbox: bool = True,
) -> dict[str, Any]:
    candidate_path = _resolve_candidate_path(file_arg, require_inbox)
    bundle = _load_json(candidate_path)
    store = _load_json(store_path)
    already_promoted = _is_matching_promoted_candidate(
        bundle, candidate_path, store, manifest_path
    )
    if already_promoted:
        validation = validate_final_asset_payload(
            bundle, _store_without_candidate_assets(store, bundle)
        )
        validation.update(
            {
                "candidate_path": _relative_to_root(candidate_path),
                "already_promoted": True,
                "promotion_allowed": True,
            }
        )
        _write_json_atomic(validation_path, validation)
        return {
            "version": VERSION,
            "status": "already_promoted_final_creation_assets",
            "promotion_allowed": True,
            "store_path": _relative_to_root(store_path),
            "manifest_path": _relative_to_root(manifest_path),
            "validation_path": _relative_to_root(validation_path),
            "content_generation_allowed": False,
        }
    decision_set = load_decisions() if decisions is None else decisions
    readiness = build_final_asset_promotion_readiness(bundle, store, decision_set)
    validation = readiness["validation"]
    validation.update(
        {
            "candidate_path": _relative_to_root(candidate_path),
            "promotion_allowed": readiness["promotion_allowed"],
            "owner_decision_id": readiness["owner_decision_id"],
        }
    )
    _write_json_atomic(validation_path, validation)
    if not readiness["promotion_allowed"]:
        return {
            "version": VERSION,
            "status": readiness["status"],
            "promotion_allowed": False,
            "validation_path": _relative_to_root(validation_path),
            "next_required_action": "Resolve final asset validation or record the matching Owner decision.",
            "content_generation_allowed": False,
        }

    promoted_store = {**store, "assets": [*store.get("assets", []), *bundle["assets"]]}
    _write_json_atomic(store_path, promoted_store)
    manifest = {
        "version": VERSION,
        "promotion_state": "promoted_final_creation_assets",
        "project": PROJECT,
        "candidate_path": _relative_to_root(candidate_path),
        "candidate_sha256": _sha256_file(candidate_path),
        "validation_path": _relative_to_root(validation_path),
        "owner_decision_id": readiness["owner_decision_id"],
        "asset_ids": [asset["asset_id"] for asset in bundle["assets"]],
        "asset_family_count": len(FAMILIES),
        "content_generation_allowed": False,
        "forbidden_actions": ["generate_novel_prose", "generate_full_chapter"],
    }
    _write_json_atomic(manifest_path, manifest)
    return {
        "version": VERSION,
        "status": "promoted_final_creation_assets",
        "promotion_allowed": True,
        "store_path": _relative_to_root(store_path),
        "manifest_path": _relative_to_root(manifest_path),
        "validation_path": _relative_to_root(validation_path),
        "owner_decision_id": readiness["owner_decision_id"],
        "content_generation_allowed": False,
    }
