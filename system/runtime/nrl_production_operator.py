from __future__ import annotations

"""Small operator-facing status for the long-form production loop."""

import json
import hashlib
import re
from pathlib import Path
from typing import Any


def describe_next_production_action(status: dict[str, Any]) -> dict[str, str]:
    if status.get("accepted_contiguous", 0) >= status.get("target_chapters", 100):
        return {
            "action_id": "volume_release_review",
            "label_zh": "执行第一卷全卷发布审查与遗留章节发布编辑",
            "safe_command": "python3 system/runtime/nrl.py volume1-release-status",
        }
    window = str(status.get("active_window") or "")
    chapter_id = str(status.get("next_chapter") or "")
    chapter = int(chapter_id.removeprefix("chapter-")) if chapter_id else 1
    return {
        "action_id": f"story_window_{window.replace('-', '_')}",
        "label_zh": f"编译 {window} 故事窗口并从第 {chapter} 章恢复受控生产",
        "safe_command": status.get("resume_command") or "python3 system/runtime/nrl.py production-status",
    }


def build_operator_status(registry_path: Path, target: int = 100) -> dict[str, Any]:
    if not registry_path.is_file():
        return {
            "valid": True,
            "project": "借天改命账",
            "volume": 1,
            "target_chapters": target,
            "accepted_contiguous": 0,
            "remaining_chapters": target,
            "next_chapter": "chapter-0001",
            "active_window": "001-010",
            "release_ready": False,
            "accepted_chapters_requiring_release_edit": [],
            "accepted_release_ready_count": 0,
            "resume_command": f"python3 system/runtime/nrl.py produce --until {target}",
            "errors": [],
        }
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    root = registry_path.parents[2]
    accepted = {
        int(item["chapter_id"].removeprefix("chapter-"))
        for item in registry.get("chapters", [])
        if item.get("stage") == "chapter_accepted"
    }
    contiguous = 0
    while contiguous + 1 in accepted:
        contiguous += 1
    later = sorted(number for number in accepted if number > contiguous + 1)
    errors = []
    if later:
        errors.append(f"chapter registry has a gap at chapter-{contiguous + 1:04d}")
    release_repairs = []
    for item in registry.get("chapters", []):
        if item.get("stage") != "chapter_accepted":
            continue
        revision = root / item.get("artifacts", {}).get("revision", "")
        if not revision.is_file():
            release_repairs.append(item["chapter_id"])
            continue
        effective = revision
        edit_manifest = root / "system/production_runtime/release_edits" / f"{item['chapter_id']}.json"
        if edit_manifest.is_file():
            edit = json.loads(edit_manifest.read_text(encoding="utf-8"))
            source_hash = hashlib.sha256(revision.read_bytes()).hexdigest()
            candidate = root / edit.get("release_edit", "")
            if edit.get("source_sha256") == source_hash and candidate.is_file():
                effective = candidate
        chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", effective.read_text(encoding="utf-8")))
        if not 3000 <= chinese_chars <= 4200:
            release_repairs.append(item["chapter_id"])
    next_ordinal = contiguous + 1 if contiguous < target else None
    window_start = ((next_ordinal - 1) // 10) * 10 + 1 if next_ordinal else None
    return {
        "valid": not errors,
        "project": "借天改命账",
        "volume": 1,
        "target_chapters": target,
        "accepted_contiguous": contiguous,
        "remaining_chapters": max(target - contiguous, 0),
        "next_chapter": f"chapter-{next_ordinal:04d}" if next_ordinal else None,
        "active_window": f"{window_start:03d}-{window_start + 9:03d}" if window_start else None,
        "release_ready": contiguous >= target and not release_repairs,
        "accepted_chapters_requiring_release_edit": release_repairs,
        "accepted_release_ready_count": contiguous - len(release_repairs),
        "resume_command": f"python3 system/runtime/nrl.py produce --until {target}" if next_ordinal else None,
        "errors": errors,
    }
