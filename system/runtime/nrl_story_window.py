from __future__ import annotations

"""Ten-chapter story compilation contracts for production prose."""

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import jsonschema

from nrl_paths import ROOT, runtime_path
from nrl_model_router import route_model


VERSION = "1.0"
MAX_CHAPTER_ASSETS = 12
MAX_STORY_WINDOW_PROMPT_BYTES = 36000
SCHEMA_PATH = runtime_path("system/production_runtime/schemas/story_window.schema.json")
WINDOW_ROOT = runtime_path("system/production_runtime/story_windows")
ASSET_STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
LONGFORM_CONTRACT_PATH = runtime_path(
    "system/production_runtime/plans/borrowed_heaven_longform_contract.v0.1.json"
)
FIRST100_MANIFEST_PATH = runtime_path(
    "system/production_runtime/plans/borrowed_heaven_first100_manifest.v0.1.json"
)
CHAPTER_ROOT = runtime_path("system/production_runtime/chapters")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _latest_asset_state(asset_ids: set[str] | None = None) -> dict[str, dict[str, Any]]:
    """Project accepted settlements into a compact, deterministic current state."""
    latest: dict[str, dict[str, Any]] = {}
    for path in sorted(CHAPTER_ROOT.glob("chapter-*/settlement.json")):
        settlement = _read_json(path)
        chapter_id = str(settlement.get("chapter_id", path.parent.name))
        for delta in settlement.get("state_deltas", []):
            if not isinstance(delta, dict):
                continue
            asset_id = str(delta.get("asset_id", ""))
            field_path = str(delta.get("field_path", ""))
            if not asset_id or not field_path or (asset_ids is not None and asset_id not in asset_ids):
                continue
            latest.setdefault(asset_id, {})[field_path] = {
                "value": delta.get("after"),
                "chapter_id": chapter_id,
            }
    return latest


def _compact_story_state(
    latest: dict[str, dict[str, Any]], recent_fields_per_asset: int = 3
) -> dict[str, dict[str, Any]]:
    """Keep continuity-critical lifecycle fields plus each asset's recent state."""
    critical_suffixes = (
        "acquisition_status",
        "awakening_status",
        "custody_status",
        "lifecycle_state",
    )
    compact: dict[str, dict[str, Any]] = {}
    for asset_id, fields in latest.items():
        selected = {
            key: value
            for key, value in fields.items()
            if key.endswith(critical_suffixes)
        }
        for key in list(fields)[-recent_fields_per_asset:]:
            selected[key] = fields[key]
        compact[asset_id] = selected
    return compact


def validate_story_window(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    try:
        jsonschema.validate(payload, _read_json(SCHEMA_PATH))
    except jsonschema.ValidationError as error:
        errors.append(error.message)
        return {"valid": False, "errors": errors}
    start = int(payload["window"]["start"])
    end = int(payload["window"]["end"])
    if end - start != 9:
        errors.append("story window must contain exactly ten consecutive chapters")
    chapters = payload["chapters"]
    expected_ids = [f"chapter-{number:04d}" for number in range(start, end + 1)]
    if [item["chapter_id"] for item in chapters] != expected_ids:
        errors.append("story window chapter IDs must be consecutive and ordered")
    for field in ("working_title", "event", "scene_anchor", "conflict", "character_choice", "irreversible_change", "hook_out"):
        values = [str(item[field]).strip() for item in chapters]
        if len(values) != len(set(values)):
            errors.append(f"story window requires unique {field} values")
    duplicate_asset_chapters = [
        item["chapter_id"]
        for item in chapters
        if len(item.get("required_asset_ids", [])) != len(set(item.get("required_asset_ids", [])))
    ]
    if duplicate_asset_chapters:
        errors.append("required_asset_ids must be unique within chapters: " + ", ".join(duplicate_asset_chapters))
    if start >= 51:
        overwide = [
            item["chapter_id"] for item in chapters
            if len(item.get("required_asset_ids", [])) > MAX_CHAPTER_ASSETS
        ]
        if overwide:
            errors.append(
                "future story-window chapters may use at most 12 writer assets: "
                + ", ".join(overwide)
            )
    if len({item["scene_anchor"].split("，")[0] for item in chapters}) < 5:
        errors.append("story window requires at least five distinct scene anchors")
    known_assets = {
        item.get("asset_id") for item in _read_json(ASSET_STORE_PATH).get("assets", [])
    }
    unknown_assets = sorted(
        {
            asset_id
            for chapter in chapters
            for asset_id in chapter.get("required_asset_ids", [])
            if asset_id not in known_assets
        }
    )
    if unknown_assets:
        errors.append("story window references unknown assets: " + ", ".join(unknown_assets))
    asset_rows = {
        str(item.get("asset_id")): item
        for item in _read_json(ASSET_STORE_PATH).get("assets", [])
        if item.get("asset_id")
    }
    canonical_state = _latest_asset_state(set(asset_rows))
    start_snapshot = "\n".join(str(item) for item in payload.get("start_snapshot", []))
    for asset_id, fields in canonical_state.items():
        acquisition = fields.get("artifact.current_acquisition_status", {}).get("value")
        display_name = str(asset_rows[asset_id].get("display_name", ""))
        if (
            acquisition
            and display_name
            and display_name in start_snapshot
            and ("已" in str(acquisition) or "完成" in str(acquisition))
            and re.search(
                rf"{re.escape(display_name)}[^。；\n]*未取得(?=[、，；。\n])",
                start_snapshot,
            )
        ):
            errors.append(
                f"start_snapshot contradicts accepted acquisition state for {asset_id}"
            )
    if any(
        item.get("source_status") != ("accepted_calibration" if int(item["chapter_id"][-4:]) <= 15 else "planned")
        for item in chapters
    ):
        errors.append("source_status must distinguish accepted calibration from planned chapters")
    return {
        "valid": not errors,
        "errors": errors,
        "window": f"{start:03d}-{end:03d}",
        "chapter_count": len(chapters),
    }


def load_story_window(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    validation = validate_story_window(payload)
    if not validation["valid"]:
        raise RuntimeError("; ".join(validation["errors"]))
    return payload


def story_beat_for(chapter_id: str) -> dict[str, Any] | None:
    for path in sorted(WINDOW_ROOT.glob("window-*.json")):
        payload = load_story_window(path)
        for beat in payload["chapters"]:
            if beat["chapter_id"] == chapter_id:
                return {
                    **beat,
                    "window": payload["window"],
                    "window_name": payload["window"]["name"],
                    "window_end_target": payload["end_target"],
                    "contract_path": str(path.relative_to(ROOT)),
                }
    return None


def build_story_window_status() -> dict[str, Any]:
    windows = []
    for path in sorted(WINDOW_ROOT.glob("window-*.json")):
        payload = _read_json(path)
        validation = validate_story_window(payload)
        windows.append({
            "path": str(path.relative_to(ROOT)),
            "status": payload.get("status"),
            **validation,
        })
    return {
        "version": VERSION,
        "valid": bool(windows) and all(item["valid"] for item in windows),
        "window_count": len(windows),
        "windows": windows,
    }


def build_story_window_prompt(start: int) -> str:
    if start not in range(21, 92, 10):
        raise RuntimeError("generated story windows must start at 21, 31, ..., or 91")
    previous_path = WINDOW_ROOT / f"window-{start - 10:03d}-{start - 1:03d}.v1.json"
    if not previous_path.exists():
        raise RuntimeError(f"previous story window is missing: {previous_path.name}")
    previous = load_story_window(previous_path)
    if previous.get("status") != "production_ready":
        raise RuntimeError("previous story window must be production_ready")
    end = start + 9
    previous_summary = {
        "window": previous.get("window"),
        "end_target": previous.get("end_target", []),
        "chapters": [
            {
                "chapter_id": item.get("chapter_id"),
                "working_title": item.get("working_title"),
                "irreversible_change": item.get("irreversible_change"),
                "hook_out": item.get("hook_out"),
            }
            for item in previous.get("chapters", [])
        ],
    }
    assets = _read_json(ASSET_STORE_PATH).get("assets", [])
    compact_assets = [
        {
            "asset_id": item.get("asset_id"),
            "display_name": item.get("display_name"),
            "family": item.get("family"),
            "lifecycle_state": item.get("lifecycle_state"),
            "constraints": item.get("constraints", []),
        }
        for item in assets
    ]
    manifest = _read_json(FIRST100_MANIFEST_PATH)
    chapter_contracts = [
        item
        for item in manifest.get("chapters", [])
        if start <= int(item["chapter_id"][-4:]) <= end
    ]
    compact_chapter_contracts = [
        {
            key: item.get(key)
            for key in (
                "chapter_id", "beat", "objective", "required_payoff",
                "structural_reversal_window", "payoff_contract", "survival_constraint",
            )
        }
        for item in chapter_contracts
    ]
    allowed_asset_ids = {
        asset_id
        for item in chapter_contracts
        for asset_id in item.get("required_asset_ids", [])
    }
    known_asset_ids = {
        str(item.get("asset_id")) for item in assets if item.get("asset_id")
    }
    for item in chapter_contracts:
        for constraint in item.get("lifecycle_constraints", []):
            referenced_id = re.split(r"[:\s]", str(constraint), maxsplit=1)[0]
            if referenced_id in known_asset_ids:
                allowed_asset_ids.add(referenced_id)
    compact_assets = [
        item for item in compact_assets if item.get("asset_id") in allowed_asset_ids
    ]
    canonical_state = _compact_story_state(_latest_asset_state(allowed_asset_ids))
    contract = _read_json(LONGFORM_CONTRACT_PATH)
    prompt = "\n".join(
        [
            "你是 Novel Research Lab 的长篇故事编译器。只输出符合 JSON Schema 的一个对象，不写正文。",
            f"为《借天改命账》第一卷编译第 {start}-{end} 章的十章故事窗口。",
            "十章必须形成一条不可逆因果链，每章必须有不同事件、场景、冲突、人物选择、不可逆变化和尾钩。",
            "不得把同一争执、查账、见证、追兵换词重复；不得凭空新增资产；不得读取或模仿原始语料。",
            "每章至少推进一个人物关系、程序压力或物质后果。第十章必须完成局部兑现，同时打开下一层压力。",
            "每章 required_asset_ids 最多 12 项，只选本章真正出场或发生状态变化的资产；不得把窗口全部资产重复塞进每章。",
            "status 输出 candidate；source_status 全部输出 planned。",
            "上一窗口：",
            json.dumps(previous_summary, ensure_ascii=False),
            "长篇第一卷契约：",
            json.dumps(contract.get("volumes", [])[0], ensure_ascii=False),
            "本窗口旧约束（只能作为边界，不得沿用其循环节拍生成内容）：",
            json.dumps(compact_chapter_contracts, ensure_ascii=False),
            "可用创作资产：",
            json.dumps(compact_assets, ensure_ascii=False),
            "已接受章节的当前状态（这是事实源；start_snapshot 与后续事件不得回滚、重复取得或覆盖这些状态）：",
            json.dumps(canonical_state, ensure_ascii=False),
        ]
    )
    if len(prompt.encode("utf-8")) > MAX_STORY_WINDOW_PROMPT_BYTES:
        raise RuntimeError(
            f"story-window prompt exceeds {MAX_STORY_WINDOW_PROMPT_BYTES} bytes; narrow the state projection"
        )
    return prompt


def generate_story_window(start: int, timeout_seconds: int = 600) -> dict[str, Any]:
    prompt = build_story_window_prompt(start)
    binary = shutil.which("codex")
    if not binary:
        raise RuntimeError("codex CLI is missing")
    end = start + 9
    with tempfile.TemporaryDirectory(prefix="nrl-story-window-") as temp_dir:
        candidate = Path(temp_dir) / "story-window.json"
        result = subprocess.run(
            [
                binary,
                "--ask-for-approval", "never",
                "exec", "--ephemeral", "--skip-git-repo-check",
                "--sandbox", "read-only",
                "-m", route_model("showrunner")["model"],
                "--output-schema", str(SCHEMA_PATH),
                "-o", str(candidate),
                prompt,
            ],
            cwd=temp_dir,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        if result.returncode != 0 or not candidate.exists():
            raise RuntimeError(f"story-window compiler failed: {result.stderr.strip()}")
        payload = _read_json(candidate)
    if payload.get("window", {}).get("start") != start or payload.get("window", {}).get("end") != end:
        raise RuntimeError("story-window compiler returned the wrong chapter range")
    validation = validate_story_window(payload)
    if not validation["valid"]:
        raise RuntimeError("; ".join(validation["errors"]))
    payload["status"] = "production_ready"
    target = WINDOW_ROOT / f"window-{start:03d}-{end:03d}.v1.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "valid": True,
        "path": str(target.relative_to(ROOT)),
        "window": f"{start:03d}-{end:03d}",
        "model": route_model("showrunner")["model"],
    }
