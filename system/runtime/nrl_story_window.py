from __future__ import annotations

"""Ten-chapter story compilation contracts for production prose."""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import jsonschema

from nrl_paths import ROOT, runtime_path
from nrl_model_router import route_model


VERSION = "1.0"
SCHEMA_PATH = runtime_path("system/production_runtime/schemas/story_window.schema.json")
WINDOW_ROOT = runtime_path("system/production_runtime/story_windows")
ASSET_STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
LONGFORM_CONTRACT_PATH = runtime_path(
    "system/production_runtime/plans/borrowed_heaven_longform_contract.v0.1.json"
)
FIRST100_MANIFEST_PATH = runtime_path(
    "system/production_runtime/plans/borrowed_heaven_first100_manifest.v0.1.json"
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    contract = _read_json(LONGFORM_CONTRACT_PATH)
    return "\n".join(
        [
            "你是 Novel Research Lab 的长篇故事编译器。只输出符合 JSON Schema 的一个对象，不写正文。",
            f"为《借天改命账》第一卷编译第 {start}-{end} 章的十章故事窗口。",
            "十章必须形成一条不可逆因果链，每章必须有不同事件、场景、冲突、人物选择、不可逆变化和尾钩。",
            "不得把同一争执、查账、见证、追兵换词重复；不得凭空新增资产；不得读取或模仿原始语料。",
            "每章至少推进一个人物关系、程序压力或物质后果。第十章必须完成局部兑现，同时打开下一层压力。",
            "status 输出 candidate；source_status 全部输出 planned。",
            "上一窗口：",
            json.dumps(previous, ensure_ascii=False),
            "长篇第一卷契约：",
            json.dumps(contract.get("volumes", [])[0], ensure_ascii=False),
            "本窗口旧约束（只能作为边界，不得沿用其循环节拍生成内容）：",
            json.dumps(chapter_contracts, ensure_ascii=False),
            "可用创作资产：",
            json.dumps(compact_assets, ensure_ascii=False),
        ]
    )


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
