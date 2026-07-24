from __future__ import annotations

import json
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, active_project_id

import jsonschema


REGISTRY_PATH = ROOT / "system/projects/registry.v1.json"
PROJECT_SCHEMA_PATH = ROOT / "system/projects/project.schema.json"
PROJECT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_project_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.is_file():
        return {"version": "1.0", "default_project_id": None, "projects": []}
    return _read_json(REGISTRY_PATH)


def project_config_path(project_id: str) -> Path:
    return ROOT / "system/projects" / project_id / "project.json"


def _legacy_borrowed_heaven_project() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "project_id": "borrowed-heaven",
        "title": "《借天改命账》",
        "genre": "中文玄幻长篇",
        "status": "active_production",
        "workspace": "projects/borrowed-heaven",
        "storage_mode": "legacy_v0",
        "created_at": "legacy-fixture",
        "engine": "nrl-corpus-to-creation",
        "shared_research_catalog": "system/research_assets",
        "model_team": "codex-three-model-team-v0.27",
        "planning_profile": "borrowed_heaven_v1",
        "content_authorized": True,
        "legacy_paths": {
            "creation_assets": "system/creation_assets/project_assets.v0.2.json",
            "production_runtime": "system/production_runtime",
            "release_root": "system/releases/fanqie/borrowed-heaven-volume1",
        },
    }


def load_project(project_id: str | None = None) -> dict[str, Any]:
    selected = project_id or active_project_id()
    path = project_config_path(selected)
    if not path.is_file():
        if selected == "borrowed-heaven":
            return _legacy_borrowed_heaven_project()
        raise RuntimeError(f"unknown project_id: {selected}")
    project = _read_json(path)
    if PROJECT_SCHEMA_PATH.is_file():
        jsonschema.validate(project, _read_json(PROJECT_SCHEMA_PATH))
    if project.get("project_id") != selected:
        raise RuntimeError(f"project manifest identity mismatch: {selected}")
    return project


def active_project() -> dict[str, Any]:
    return load_project(active_project_id())


def active_project_title() -> str:
    return str(active_project()["title"])


def active_project_scope() -> str:
    return f"project:{active_project_id()}:prose"


def require_planning_profile(profile: str) -> None:
    current = str(active_project().get("planning_profile", "generic_v1"))
    if current != profile:
        raise RuntimeError(
            f"command belongs to planning_profile={profile}; active project uses {current}"
        )


def list_projects() -> dict[str, Any]:
    registry = load_project_registry()
    rows = []
    for item in registry.get("projects", []):
        project_id = str(item.get("project_id", ""))
        path = project_config_path(project_id)
        rows.append({**item, "manifest_exists": path.is_file()})
    return {
        "version": registry.get("version", "1.0"),
        "default_project_id": registry.get("default_project_id"),
        "active_project_id": active_project_id(),
        "projects": rows,
    }


def initialize_project(project_id: str, title: str, genre: str = "") -> dict[str, Any]:
    project_id = project_id.strip()
    title = title.strip()
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError("project_id must be lowercase kebab-case")
    if not title:
        raise ValueError("project title is required")
    registry = load_project_registry()
    if any(item.get("project_id") == project_id for item in registry.get("projects", [])):
        raise RuntimeError(f"project already exists: {project_id}")
    workspace_rel = f"projects/{project_id}"
    workspace = ROOT / workspace_rel
    if workspace.exists():
        raise RuntimeError(f"project workspace already exists: {workspace_rel}")
    for relative in (
        "creation_assets",
        "design",
        "production_runtime/chapters",
        "production_runtime/intents",
        "production_runtime/plans",
        "production_runtime/quarantine",
        "production_runtime/release_edits",
        "production_runtime/state",
        "production_runtime/story_windows",
        "production_runtime/window_reviews",
        "releases/fanqie/volume1",
        "releases/review",
        "validation",
    ):
        (workspace / relative).mkdir(parents=True, exist_ok=True)
    created_at = _now()
    project = {
        "schema_version": "1.0",
        "project_id": project_id,
        "title": title,
        "genre": genre.strip(),
        "status": "initialized",
        "workspace": workspace_rel,
        "created_at": created_at,
        "engine": "nrl-corpus-to-creation",
        "shared_research_catalog": "system/research_assets",
        "model_team": "codex-three-model-team-v0.27",
        "planning_profile": "generic_v1",
        "content_authorized": False,
    }
    _write_json(ROOT / "system/projects" / project_id / "project.json", project)
    _write_json(
        workspace / "creation_assets/project_assets.json",
        {"version": "1.0", "project_id": project_id, "project": title, "assets": []},
    )
    _write_json(
        workspace / "production_runtime/chapter_registry.v0.20.json",
        {"version": "0.20", "project_id": project_id, "project": title, "chapters": []},
    )
    _write_json(
        workspace / "project_state.json",
        {
            "version": "1.0",
            "project_id": project_id,
            "stage": "concept_selection",
            "artifacts": {
                "concept_decision": None,
                "story_bible": None,
                "creation_assets": "creation_assets/project_assets.json",
                "longform_contract": None,
                "volume_plan": None,
            },
            "owner_gate": "required_before_prose",
        },
    )
    (workspace / "design/story_bible.md").write_text(f"# {title} Story Bible\n\n状态：待生成与审核。\n", encoding="utf-8")
    (workspace / "design/outline_tree.md").write_text(f"# {title} 大纲树\n\n状态：待生成与审核。\n", encoding="utf-8")
    (workspace / "design/production_blueprint.md").write_text(f"# {title} 生产蓝图\n\n状态：待 Owner 授权。\n", encoding="utf-8")
    registry.setdefault("projects", []).append(
        {"project_id": project_id, "title": title, "status": "initialized", "workspace": workspace_rel}
    )
    if not registry.get("default_project_id"):
        registry["default_project_id"] = project_id
    _write_json(REGISTRY_PATH, registry)
    return {"created": True, "project": project, "workspace": workspace_rel}


def build_project_status(project_id: str | None = None) -> dict[str, Any]:
    project = load_project(project_id)
    workspace = ROOT / str(project["workspace"])
    asset_path = workspace / "creation_assets/project_assets.json"
    registry_path = workspace / "production_runtime/chapter_registry.v0.20.json"
    if project.get("storage_mode") == "legacy_v0":
        asset_path = ROOT / "system/creation_assets/project_assets.v0.2.json"
        registry_path = ROOT / "system/production_runtime/chapter_registry.v0.20.json"
    assets = _read_json(asset_path).get("assets", []) if asset_path.is_file() else []
    chapters = _read_json(registry_path).get("chapters", []) if registry_path.is_file() else []
    accepted = [item for item in chapters if item.get("stage") == "chapter_accepted"]
    required_design = ["story_bible.md", "outline_tree.md", "production_blueprint.md"]
    if project.get("storage_mode") == "legacy_v0":
        design_ready = all(
            path.is_file()
            for path in (
                ROOT / "phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md",
                ROOT / "phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md",
                ROOT / "docs/production/borrowed-heaven-production-blueprint-v0.1.md",
            )
        )
    else:
        design_paths = [workspace / "design" / name for name in required_design]
        design_ready = all(
            path.is_file() and "待生成" not in path.read_text(encoding="utf-8")
            for path in design_paths
        )
    preprose_review_path = workspace / "validation/preprose_independent_review.v0.1.json"
    preprose_review = _read_json(preprose_review_path) if preprose_review_path.is_file() else {}
    controlled_sample_ready = bool(
        assets
        and design_ready
        and preprose_review.get("valid") is True
        and preprose_review.get("verdict") == "ACCEPT_FOR_CONTROLLED_SAMPLE_TEST"
    )
    expected_sample_scopes = {
        f"{project['project_id']}:volume1:sample-window-008-010",
        f"{project['project_id']}:volume1:sample-window-024-026",
        f"{project['project_id']}:volume1:sample-window-049-051",
    }
    expected_forbidden = {
        f"{project['project_id']}:continuous-prose",
        f"{project['project_id']}:chapter-outside-approved-samples",
        f"{project['project_id']}:publish",
    }
    decisions_path = ROOT / "system/runtime/owner_gate_decisions.json"
    decisions: list[dict[str, Any]] = []
    if decisions_path.is_file():
        raw_decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
        decisions = raw_decisions if isinstance(raw_decisions, list) else []
    review_response_path = ROOT / str(preprose_review.get("response_path", ""))
    review_sha = (
        hashlib.sha256(review_response_path.read_bytes()).hexdigest()
        if review_response_path.is_file()
        else ""
    )
    matching_sample_decision = next(
        (
            item
            for item in reversed(decisions)
            if item.get("decision_type") == "authorize_controlled_prose_test"
            and set(item.get("authorized_scope", [])) == expected_sample_scopes
            and expected_forbidden <= set(item.get("forbidden_scope", []))
            and item.get("expires_after_mission") == "hundred-crafts-volume1-controlled-sample-v0.1"
            and item.get("bound_response_sha256") == review_sha
        ),
        None,
    )
    sample_test_authorized = bool(
        project.get("sample_test_authorized")
        and controlled_sample_ready
        and matching_sample_decision
    )
    sample_run_path = workspace / "production_runtime/plans/controlled_sample_run.v0.1.json"
    sample_run = _read_json(sample_run_path) if sample_run_path.is_file() else {}
    controlled_sample_status = str(sample_run.get("status", "not_started"))
    sample_test_passed = bool(
        sample_test_authorized
        and controlled_sample_status == "sample_test_passed"
        and sample_run.get("continuous_prose_authorized") is False
        and sample_run.get("publish_authorized") is False
    )
    continuity_path = workspace / "production_runtime/plans/continuity_validation.v0.1.json"
    continuity_contract = _read_json(continuity_path) if continuity_path.is_file() else {}
    continuity_status = str(continuity_contract.get("status", "not_started"))
    continuity_validation: dict[str, Any] = {"valid": False}
    if continuity_path.is_file():
        from nrl_continuity_validation import validate_continuity_contract

        continuity_validation = validate_continuity_contract(str(project["project_id"]))
    continuity_test_authorized = bool(
        sample_test_passed
        and continuity_status in {"authorized", "continuity_test_passed"}
        and continuity_validation.get("valid") is True
    )
    continuity_test_passed = bool(
        continuity_test_authorized
        and continuity_status == "continuity_test_passed"
        and continuity_validation.get("review_verdict") == "ACCEPT_CONTINUITY_TEST"
        and continuity_contract.get("continuous_prose_authorized") is False
        and continuity_contract.get("publish_authorized") is False
    )
    return {
        "project_id": project["project_id"],
        "title": project["title"],
        "status": project.get("status"),
        "workspace": project["workspace"],
        "storage_mode": project.get("storage_mode", "isolated_v1"),
        "content_authorized": bool(project.get("content_authorized")),
        "sample_test_authorized": sample_test_authorized,
        "sample_test_passed": sample_test_passed,
        "controlled_sample_status": controlled_sample_status,
        "controlled_sample_ready": controlled_sample_ready,
        "sample_owner_decision_id": (
            matching_sample_decision.get("decision_id")
            if matching_sample_decision
            else None
        ),
        "continuity_test_authorized": continuity_test_authorized,
        "continuity_test_passed": continuity_test_passed,
        "continuity_status": continuity_status,
        "continuity_owner_decision_id": continuity_contract.get("owner_decision_id"),
        "assets": len(assets),
        "chapters": len(chapters),
        "accepted_chapters": len(accepted),
        "design_contracts_present": design_ready,
        "ready_for_prose": bool(project.get("content_authorized")) and bool(assets) and design_ready,
        "next_action": (
            "continue governed production"
            if bool(project.get("content_authorized")) and bool(assets) and design_ready
            else "await explicit production readiness decision"
            if continuity_test_passed
            else "await explicit controlled continuity validation authorization"
            if sample_test_passed
            else "run authorized controlled sample test"
            if controlled_sample_ready and sample_test_authorized
            else "await explicit controlled sample authorization"
            if controlled_sample_ready
            else "await explicit prose authorization"
            if bool(assets) and design_ready
            else "build project-specific creation assets"
            if design_ready
            else "produce project-specific design contracts"
        ),
    }


def validate_project_isolation(project_id: str | None = None) -> dict[str, Any]:
    project = load_project(project_id)
    selected = str(project["project_id"])
    errors: list[str] = []
    checks: dict[str, Any] = {}
    workspace = (ROOT / str(project["workspace"])).resolve()
    expected_root = (ROOT / "projects" / selected).resolve()
    if workspace != expected_root:
        errors.append("workspace must equal projects/<project_id>")
    if project.get("storage_mode") == "legacy_v0":
        if selected != "borrowed-heaven":
            errors.append("legacy_v0 is reserved for the migrated first project")
    else:
        asset_path = workspace / "creation_assets/project_assets.json"
        registry_path = workspace / "production_runtime/chapter_registry.v0.20.json"
        if not asset_path.is_file() or not registry_path.is_file():
            errors.append("isolated asset store or chapter registry is missing")
        else:
            assets = _read_json(asset_path)
            chapters = _read_json(registry_path)
            for label, payload in (("asset store", assets), ("chapter registry", chapters)):
                if payload.get("project_id") != selected:
                    errors.append(f"{label} project_id mismatch")
                if payload.get("project") != project.get("title"):
                    errors.append(f"{label} title mismatch")
            from nrl_creation_schemas import validate_creation_asset_store

            asset_validation = validate_creation_asset_store(assets)
            checks["creation_assets"] = asset_validation
            if not asset_validation["valid"]:
                errors.append("project creation assets failed schema validation")

            volume_plan_path = workspace / "production_runtime/plans/volume1_outline.v1.json"
            if volume_plan_path.is_file():
                import jsonschema

                schema_path = ROOT / "system/production_runtime/schemas/volume_outline.schema.json"
                try:
                    outline = _read_json(volume_plan_path)
                    schema = _read_json(schema_path)
                    jsonschema.Draft7Validator.check_schema(schema)
                    jsonschema.validate(outline, schema)
                    chapter_numbers = [row.get("chapter") for row in outline.get("chapters", [])]
                    plan_errors = []
                    if chapter_numbers != list(range(1, len(chapter_numbers) + 1)):
                        plan_errors.append("chapter numbers must be contiguous from 1")
                    known_asset_ids = {str(row.get("asset_id")) for row in assets.get("assets", [])}
                    unresolved = sorted({
                        ref
                        for row in outline.get("chapters", [])
                        for ref in row.get("asset_refs", [])
                        if ref not in known_asset_ids
                    })
                    if unresolved:
                        plan_errors.append(f"unresolved volume plan asset refs: {unresolved}")
                    checks["volume_plan"] = {
                        "valid": not plan_errors,
                        "status": "validated" if not plan_errors else "invalid",
                        "chapter_count": len(chapter_numbers),
                        "errors": plan_errors,
                    }
                    errors.extend(plan_errors)
                except (jsonschema.SchemaError, jsonschema.ValidationError) as exc:
                    checks["volume_plan"] = {
                        "valid": False,
                        "status": "invalid",
                        "chapter_count": 0,
                        "errors": [exc.message],
                    }
                    errors.append("project volume plan failed schema validation")
            else:
                checks["volume_plan"] = {
                    "valid": True,
                    "status": "not_present",
                    "chapter_count": 0,
                    "errors": [],
                }

            continuity_path = workspace / "production_runtime/plans/continuity_validation.v0.1.json"
            if continuity_path.is_file():
                from nrl_continuity_validation import validate_continuity_contract

                continuity_validation = validate_continuity_contract(selected)
                checks["continuity_validation"] = {
                    key: value
                    for key, value in continuity_validation.items()
                    if key != "prose_chapters"
                }
                checks["continuity_validation"]["generated_prose_count"] = len(
                    continuity_validation.get("prose_chapters", [])
                )
                if not continuity_validation["valid"]:
                    errors.append("project continuity validation failed")
        forbidden = ("《借天改命账》", "borrowed-heaven")
        canonical_roots = (
            workspace / "design",
            workspace / "creation_assets",
            workspace / "production_runtime/intents",
            workspace / "production_runtime/plans",
            workspace / "production_runtime/state",
            workspace / "production_runtime/story_windows",
        )
        canonical_paths = (
            path
            for root in canonical_roots
            if root.is_dir()
            for path in root.rglob("*")
        )
        for path in canonical_paths:
            if path.is_file() and path.suffix in {".json", ".md", ".txt"}:
                text = path.read_text(encoding="utf-8")
                if any(marker in text for marker in forbidden):
                    errors.append(f"cross-project marker found: {path.relative_to(ROOT)}")
    return {
        "valid": not errors,
        "project_id": selected,
        "workspace": str(workspace.relative_to(ROOT)) if workspace.is_relative_to(ROOT) else str(workspace),
        "storage_mode": project.get("storage_mode", "isolated_v1"),
        "checks": checks,
        "errors": errors,
    }
