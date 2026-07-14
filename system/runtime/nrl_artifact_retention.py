from __future__ import annotations

"""Retention policy for accepted chapter bundles.

Working artifacts are useful while a chapter is in flight. Once accepted, the
revision, audits, observed facts, settlement and acceptance record are the
durable product; prompts, drafts and compiled context are reproducible cache.
"""

import json
from pathlib import Path
from typing import Any


POLICY_VERSION = "1.0"
RETAINED_ARTIFACT_KEYS = frozenset({
    "intent",
    "revision",
    "revision_metrics",
    "observation",
    "final_audit",
    "revision_audit",
    "settlement",
    "acceptance",
    "generation_cost",
})
REQUIRED_ARTIFACT_KEYS = frozenset({
    "intent",
    "revision",
    "revision_metrics",
    "observation",
    "settlement",
    "acceptance",
})


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_compaction_plan(root: Path, registry_path: Path) -> dict[str, Any]:
    registry = _load(registry_path)
    errors: list[str] = []
    removable: list[Path] = []
    accepted = 0
    compact_artifacts: dict[str, dict[str, str]] = {}

    for record in registry.get("chapters", []):
        if record.get("stage") != "chapter_accepted":
            continue
        accepted += 1
        chapter_id = str(record.get("chapter_id"))
        artifacts = record.get("artifacts", {})
        missing_keys = sorted(REQUIRED_ARTIFACT_KEYS - artifacts.keys())
        if not ({"final_audit", "revision_audit"} & artifacts.keys()):
            missing_keys.append("final_audit_or_revision_audit")
        if missing_keys:
            errors.append(f"{chapter_id}: missing durable artifacts: {', '.join(missing_keys)}")
            continue
        retained = {key: value for key, value in artifacts.items() if key in RETAINED_ARTIFACT_KEYS}
        missing_files = [value for value in retained.values() if not (root / value).is_file()]
        if missing_files:
            errors.append(f"{chapter_id}: missing durable files: {', '.join(missing_files)}")
            continue
        compact_artifacts[chapter_id] = retained
        chapter_dir = root / "system/production_runtime/chapters" / chapter_id
        retained_paths = {(root / value).resolve() for value in retained.values()}
        removable.extend(path for path in chapter_dir.iterdir() if path.is_file() and path.resolve() not in retained_paths)

    return {
        "valid": not errors,
        "policy_version": POLICY_VERSION,
        "accepted_chapters": accepted,
        "remove_files": [str(path.relative_to(root)) for path in sorted(removable)],
        "reclaimable_bytes": sum(path.stat().st_size for path in removable),
        "compact_artifacts": compact_artifacts,
        "errors": errors,
    }


def compact_accepted_chapters(root: Path, registry_path: Path) -> dict[str, Any]:
    plan = build_compaction_plan(root, registry_path)
    if not plan["valid"]:
        return plan

    registry = _load(registry_path)
    for record in registry.get("chapters", []):
        chapter_id = record.get("chapter_id")
        if chapter_id in plan["compact_artifacts"]:
            record["artifacts"] = plan["compact_artifacts"][chapter_id]
    temporary = registry_path.with_suffix(registry_path.suffix + ".tmp")
    temporary.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(registry_path)

    for relative in plan["remove_files"]:
        (root / relative).unlink(missing_ok=True)
    return {
        "valid": True,
        "policy_version": POLICY_VERSION,
        "accepted_chapters": plan["accepted_chapters"],
        "removed_file_count": len(plan["remove_files"]),
        "reclaimed_bytes": plan["reclaimable_bytes"],
        "errors": [],
    }
