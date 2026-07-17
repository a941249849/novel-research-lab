from __future__ import annotations

import json
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
    return {
        "project_id": project["project_id"],
        "title": project["title"],
        "status": project.get("status"),
        "workspace": project["workspace"],
        "storage_mode": project.get("storage_mode", "isolated_v1"),
        "content_authorized": bool(project.get("content_authorized")),
        "assets": len(assets),
        "chapters": len(chapters),
        "accepted_chapters": len(accepted),
        "design_contracts_present": design_ready,
        "ready_for_prose": bool(project.get("content_authorized")) and bool(assets) and design_ready,
        "next_action": (
            "continue governed production"
            if bool(project.get("content_authorized")) and bool(assets) and design_ready
            else "select an original concept and produce project-specific design contracts"
        ),
    }


def validate_project_isolation(project_id: str | None = None) -> dict[str, Any]:
    project = load_project(project_id)
    selected = str(project["project_id"])
    errors: list[str] = []
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
        forbidden = ("《借天改命账》", "borrowed-heaven")
        for path in workspace.rglob("*") if workspace.is_dir() else []:
            if path.is_file() and path.suffix in {".json", ".md", ".txt"}:
                text = path.read_text(encoding="utf-8")
                if any(marker in text for marker in forbidden):
                    errors.append(f"cross-project marker found: {path.relative_to(ROOT)}")
    return {
        "valid": not errors,
        "project_id": selected,
        "workspace": str(workspace.relative_to(ROOT)) if workspace.is_relative_to(ROOT) else str(workspace),
        "storage_mode": project.get("storage_mode", "isolated_v1"),
        "errors": errors,
    }
