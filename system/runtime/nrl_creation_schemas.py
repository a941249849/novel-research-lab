from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema
from referencing import Registry, Resource

from nrl_paths import active_project_id, runtime_path


LEGACY_SCHEMA_DIR = runtime_path("system/creation_assets/schemas")
V1_SCHEMA_DIR = LEGACY_SCHEMA_DIR / "v1"
PACKAGE_SCHEMA_DIR = Path(__file__).resolve().parents[2] / "system/creation_assets/schemas"
PACKAGE_STORE_PATH = Path(__file__).resolve().parents[2] / "system/creation_assets/project_assets.v0.2.json"
STORE_RELATIVE_PATH = "system/creation_assets/project_assets.v0.2.json"
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
PAYLOAD_KEYS = {
    "characters": "character",
    "npcs": "npc",
    "factions": "faction",
    "artifacts": "artifact",
    "techniques": "technique",
    "naming": "naming",
    "emotional_bonds": "emotional_bond",
    "foreshadowing": "foreshadowing",
    "state_ledger": "state_ledger",
}
TRANSITIONS = {
    "seed": {"seed", "active", "dormant", "retired"},
    "active": {"active", "dormant", "retired"},
    "dormant": {"active", "dormant", "retired"},
    "retired": {"retired"},
}
FORBIDDEN_NAMING_TERMS = (
    "测名院",
    "无名者航路",
    "群岛无名碑",
    "海图擦除",
    "旧名碑逻辑",
)


def _active_store_path() -> Path:
    return runtime_path(STORE_RELATIVE_PATH)


def _display_path(path: Path) -> str:
    root = runtime_path(".").resolve()
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        if path == _active_store_path() and active_project_id() == "borrowed-heaven":
            path = PACKAGE_STORE_PATH
        else:
            try:
                relative = path.relative_to(LEGACY_SCHEMA_DIR)
            except ValueError:
                relative = None
            if relative is not None:
                fallback = PACKAGE_SCHEMA_DIR / relative
                if fallback.exists():
                    path = fallback
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _schema_lane(version: Any) -> tuple[str, Path]:
    if version == "0.2":
        return "legacy_v0.2", LEGACY_SCHEMA_DIR
    if version == "1.0":
        return "v1", V1_SCHEMA_DIR
    raise ValueError(f"unsupported creation asset store version: {version!r}")


def _schema_paths_for_store(store: dict[str, Any]) -> tuple[str, Path, Path, Path | None]:
    lane, schema_dir = _schema_lane(store.get("version"))
    store_schema = schema_dir / "project_store.schema.json" if lane == "v1" else None
    return lane, schema_dir, schema_dir / "common.schema.json", store_schema


def build_creation_schema_registry(store: dict[str, Any] | None = None) -> dict[str, Any]:
    store = store if store is not None else _load_json(_active_store_path())
    lane, schema_dir, common_path, store_schema_path = _schema_paths_for_store(store)
    schemas = []
    all_valid = True
    for family in FAMILIES:
        path = schema_dir / f"{family}.schema.json"
        schema = _load_json(path)
        try:
            jsonschema.Draft7Validator.check_schema(schema)
            valid = True
        except jsonschema.SchemaError:
            valid = False
            all_valid = False
        schemas.append(
            {
                "family": family,
                "title": str(schema.get("title", family)),
                "path": _display_path(path),
                "valid": valid,
                "payload_key": PAYLOAD_KEYS[family],
            }
        )
    common = _load_json(common_path)
    jsonschema.Draft7Validator.check_schema(common)
    if store_schema_path is not None:
        jsonschema.Draft7Validator.check_schema(_load_json(store_schema_path))
    return {
        "registry_name": "NRL Creation Schema Registry",
        "version": str(store.get("version", "")),
        "schema_lane": lane,
        "draft": "http://json-schema.org/draft-07/schema#",
        "common_schema": _display_path(common_path),
        "project_store_schema": (
            _display_path(store_schema_path) if store_schema_path is not None else None
        ),
        "families": schemas,
        "summary": {
            "family_count": len(schemas),
            "all_schemas_valid": all_valid,
        },
    }


def _normalize_name(value: str) -> str:
    return re.sub(r"[\s\-_]+", "", value).casefold()


def _append_schema_errors(
    errors: list[dict[str, Any]],
    validator: jsonschema.Draft7Validator,
    value: Any,
    *,
    asset_id: str | None = None,
    asset_index: int | None = None,
    code: str = "schema_validation",
) -> None:
    for error in validator.iter_errors(value):
        item: dict[str, Any] = {"code": code, "message": error.message}
        if asset_id is not None:
            item["asset_id"] = asset_id
        if asset_index is not None:
            item["asset_index"] = asset_index
        errors.append(item)


def _reference_ids(asset: dict[str, Any], lane: str) -> list[str]:
    reference_ids = [
        relationship.get("target_id")
        for relationship in asset.get("relationships", [])
        if isinstance(relationship, dict)
    ]
    family = str(asset.get("family", ""))
    payload_key = PAYLOAD_KEYS.get(family)
    payload = asset.get(payload_key, {}) if payload_key else {}
    if not isinstance(payload, dict):
        return reference_ids
    if lane == "v1":
        for field in ("related_asset_ids", "participant_ids", "owners"):
            values = payload.get(field, [])
            if isinstance(values, list):
                reference_ids.extend(values)
    elif family == "techniques":
        values = payload.get("counter_ids", [])
        if isinstance(values, list):
            reference_ids.extend(values)
    return reference_ids


def validate_creation_asset_store(
    store: dict[str, Any] | None = None,
) -> dict[str, Any]:
    store_path = _active_store_path()
    store = store if store is not None else _load_json(store_path)
    errors: list[dict[str, Any]] = []
    try:
        lane, schema_dir, common_path, store_schema_path = _schema_paths_for_store(store)
    except ValueError as error:
        return {
            "valid": False,
            "errors": [{"code": "unsupported_store_version", "message": str(error)}],
            "summary": {"asset_count": 0, "family_counts": {}},
            "store_path": _display_path(store_path),
        }

    if store_schema_path is not None:
        _append_schema_errors(
            errors,
            jsonschema.Draft7Validator(_load_json(store_schema_path)),
            store,
            code="store_schema_validation",
        )
    assets = store.get("assets", [])
    if not isinstance(assets, list):
        errors.append({"code": "schema_validation", "message": "assets must be a list"})
        return {
            "valid": False,
            "errors": errors,
            "schema_lane": lane,
            "summary": {"asset_count": 0, "family_counts": {}},
            "store_path": _display_path(store_path),
        }

    common_schema = _load_json(common_path)
    common_validator = jsonschema.Draft7Validator(common_schema)
    schema_registry = Registry().with_resource(
        str(common_schema["$id"]), Resource.from_contents(common_schema)
    )
    family_validators = {
        family: jsonschema.Draft7Validator(
            _load_json(schema_dir / f"{family}.schema.json"), registry=schema_registry
        )
        for family in FAMILIES
    }
    ids: set[str] = set()
    names: dict[str, str] = {}

    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(
                {
                    "code": "schema_validation",
                    "asset_index": index,
                    "message": "asset must be an object",
                }
            )
            continue
        asset_id = str(asset.get("asset_id", ""))
        _append_schema_errors(
            errors, common_validator, asset, asset_id=asset_id, asset_index=index
        )
        if asset_id in ids:
            errors.append(
                {
                    "code": "duplicate_asset_id",
                    "asset_id": asset_id,
                    "message": f"duplicate asset_id: {asset_id}",
                }
            )
        ids.add(asset_id)

        normalized_name = _normalize_name(str(asset.get("display_name", "")))
        if normalized_name and normalized_name in names:
            errors.append(
                {
                    "code": "name_collision",
                    "asset_id": asset_id,
                    "message": f"name collides with {names[normalized_name]}",
                }
            )
        elif normalized_name:
            names[normalized_name] = asset_id

        family = str(asset.get("family", ""))
        expected_payload = PAYLOAD_KEYS.get(family)
        present_payloads = set(PAYLOAD_KEYS.values()).intersection(asset)
        if expected_payload is None or expected_payload not in present_payloads or any(
            payload != expected_payload for payload in present_payloads
        ):
            errors.append(
                {
                    "code": "schema_validation",
                    "asset_id": asset_id,
                    "message": f"payload does not match family: {family}",
                }
            )
        family_validator = family_validators.get(family)
        if family_validator is not None:
            _append_schema_errors(
                errors, family_validator, asset, asset_id=asset_id, asset_index=index
            )
        if lane == "legacy_v0.2" and family == "naming":
            naming_payload = asset.get("naming", {})
            naming_content = (
                {key: value for key, value in naming_payload.items() if key != "forbidden_terms"}
                if isinstance(naming_payload, dict)
                else naming_payload
            )
            naming_text = json.dumps(
                {"display_name": asset.get("display_name"), "naming": naming_content},
                ensure_ascii=False,
            )
            forbidden_hits = [term for term in FORBIDDEN_NAMING_TERMS if term in naming_text]
            if forbidden_hits:
                errors.append(
                    {
                        "code": "naming_anti_contamination",
                        "asset_id": asset_id,
                        "forbidden_terms": forbidden_hits,
                        "message": "naming asset contains forbidden Phase 2A concepts",
                    }
                )

        previous = asset.get("previous_lifecycle_state")
        current = asset.get("lifecycle_state")
        if previous and current not in TRANSITIONS.get(str(previous), set()):
            errors.append(
                {
                    "code": "invalid_lifecycle_transition",
                    "asset_id": asset_id,
                    "message": f"invalid lifecycle transition: {previous} -> {current}",
                }
            )

    for asset in assets:
        if not isinstance(asset, dict):
            continue
        asset_id = str(asset.get("asset_id", ""))
        for target_id in _reference_ids(asset, lane):
            if target_id not in ids:
                errors.append(
                    {
                        "code": "unresolved_reference",
                        "asset_id": asset_id,
                        "target_id": target_id,
                        "message": f"unresolved reference: {target_id}",
                    }
                )

    family_counts = Counter(str(asset.get("family", "unknown")) for asset in assets if isinstance(asset, dict))
    return {
        "valid": not errors,
        "errors": errors,
        "schema_lane": lane,
        "summary": {
            "asset_count": len(assets),
            "family_counts": dict(sorted(family_counts.items())),
        },
        "store_path": _display_path(store_path),
    }
