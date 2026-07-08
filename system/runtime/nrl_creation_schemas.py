from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from nrl_paths import runtime_path


SCHEMA_DIR = runtime_path("system/creation_assets/schemas")
STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
PACKAGE_SCHEMA_DIR = Path(__file__).resolve().parents[2] / "system/creation_assets/schemas"
PACKAGE_STORE_PATH = (
    Path(__file__).resolve().parents[2]
    / "system/creation_assets/project_assets.v0.2.json"
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


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists() and path.parent == SCHEMA_DIR:
        path = PACKAGE_SCHEMA_DIR / path.name
    elif not path.exists() and path == STORE_PATH:
        path = PACKAGE_STORE_PATH
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_creation_schema_registry() -> dict[str, Any]:
    schemas = []
    all_valid = True
    for family in FAMILIES:
        path = SCHEMA_DIR / f"{family}.schema.json"
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
                "path": f"system/creation_assets/schemas/{path.name}",
                "valid": valid,
                "payload_key": PAYLOAD_KEYS[family],
            }
        )
    common = _load_json(SCHEMA_DIR / "common.schema.json")
    jsonschema.Draft7Validator.check_schema(common)
    return {
        "registry_name": "NRL Creation Schema Registry",
        "version": "0.2",
        "draft": "http://json-schema.org/draft-07/schema#",
        "common_schema": "system/creation_assets/schemas/common.schema.json",
        "families": schemas,
        "summary": {
            "family_count": len(schemas),
            "all_schemas_valid": all_valid,
        },
    }


def _normalize_name(value: str) -> str:
    return re.sub(r"[\s\-_]+", "", value).casefold()


def validate_creation_asset_store(
    store: dict[str, Any] | None = None,
) -> dict[str, Any]:
    store = store if store is not None else _load_json(STORE_PATH)
    assets = store.get("assets", [])
    errors: list[dict[str, Any]] = []
    if not isinstance(assets, list):
        return {
            "valid": False,
            "errors": [{"code": "schema_validation", "message": "assets must be a list"}],
            "summary": {"asset_count": 0, "family_counts": {}},
        }

    common_validator = jsonschema.Draft7Validator(
        _load_json(SCHEMA_DIR / "common.schema.json")
    )
    ids: set[str] = set()
    names: dict[str, str] = {}

    for index, asset in enumerate(assets):
        for error in common_validator.iter_errors(asset):
            errors.append(
                {
                    "code": "schema_validation",
                    "asset_index": index,
                    "message": error.message,
                }
            )
        asset_id = str(asset.get("asset_id", ""))
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
        if expected_payload is None or any(
            payload != expected_payload for payload in present_payloads
        ):
            errors.append(
                {
                    "code": "schema_validation",
                    "asset_id": asset_id,
                    "message": f"payload does not match family: {family}",
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
        asset_id = str(asset.get("asset_id", ""))
        reference_ids = [
            relationship.get("target_id")
            for relationship in asset.get("relationships", [])
            if isinstance(relationship, dict)
        ]
        technique = asset.get("technique")
        if isinstance(technique, dict):
            reference_ids.extend(technique.get("counter_ids", []))
        for target_id in reference_ids:
            if target_id not in ids:
                errors.append(
                    {
                        "code": "unresolved_reference",
                        "asset_id": asset_id,
                        "target_id": target_id,
                        "message": f"unresolved reference: {target_id}",
                    }
                )

    family_counts = Counter(str(asset.get("family", "unknown")) for asset in assets)
    return {
        "valid": not errors,
        "errors": errors,
        "summary": {
            "asset_count": len(assets),
            "family_counts": dict(sorted(family_counts.items())),
        },
        "store_path": "system/creation_assets/project_assets.v0.2.json",
    }
