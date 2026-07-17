from __future__ import annotations

import os
import json
from pathlib import Path


def resolve_root() -> Path:
    override = os.environ.get("NRL_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[2]


ROOT = resolve_root()


def active_project_id() -> str:
    return os.environ.get("NRL_PROJECT_ID", "borrowed-heaven").strip() or "borrowed-heaven"


def _project_config(project_id: str) -> dict:
    path = ROOT / "system" / "projects" / project_id / "project.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _project_relative_path(relative: str) -> str | None:
    project_id = active_project_id()
    if project_id == "borrowed-heaven":
        return None
    config = _project_config(project_id)
    workspace = str(config.get("workspace", f"projects/{project_id}")).rstrip("/")
    exact = {
        "system/creation_assets/project_assets.v0.2.json": f"{workspace}/creation_assets/project_assets.json",
        "phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md": f"{workspace}/design/story_bible.md",
        "phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md": f"{workspace}/design/outline_tree.md",
        "docs/production/borrowed-heaven-production-blueprint-v0.1.md": f"{workspace}/design/production_blueprint.md",
        "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json": f"{workspace}/creation_assets/canonical_baseline.json",
        "system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json": f"{workspace}/validation/project_reconciliation.json",
        "system/agent_ops/validation/borrowed_heaven_project_reconciliation_application_v0.19.json": f"{workspace}/validation/project_reconciliation_application.json",
        "system/releases/fanqie/borrowed-heaven-volume1": f"{workspace}/releases/fanqie/volume1",
        "system/releases/review": f"{workspace}/releases/review",
        "system/production_runtime/plans/borrowed_heaven_longform_contract.v0.1.json": f"{workspace}/production_runtime/plans/longform_contract.json",
        "system/production_runtime/plans/borrowed_heaven_first100_manifest.v0.1.json": f"{workspace}/production_runtime/plans/first100_manifest.json",
        "system/production_runtime/plans/borrowed_heaven_volume1_production_manifest.v0.25.json": f"{workspace}/production_runtime/plans/volume1_production_manifest.json",
    }
    if relative in exact:
        return exact[relative]
    if relative.startswith("system/production_runtime/"):
        suffix = relative.removeprefix("system/production_runtime/")
        if suffix.startswith(("schemas/", "calibration/", "canaries/")):
            return None
        return f"{workspace}/production_runtime/{suffix}"
    return None


def runtime_path(relative: str) -> Path:
    mapped = _project_relative_path(relative)
    return ROOT / (mapped or relative)
