from __future__ import annotations

"""Release gates and an upload-ready Fanqie package for Volume 1."""

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path


VERSION = "0.25"
CHAPTER_IDS = tuple(f"chapter-{number:04d}" for number in range(1, 101))
WINDOWS = tuple((start, start + 9) for start in range(1, 101, 10))
REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")
REVIEW_ROOT = runtime_path("system/production_runtime/window_reviews")
RELEASE_ROOT = runtime_path("system/releases/fanqie/borrowed-heaven-volume1")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _window_id(start: int, end: int) -> str:
    return f"{start:03d}-{end:03d}"


def _window_path(start: int, end: int) -> Path:
    return REVIEW_ROOT / f"window-{_window_id(start, end)}.json"


def build_window_review_packet(start: int, end: int) -> dict[str, Any]:
    if (start, end) not in WINDOWS:
        raise ValueError("window must be one of the canonical ten-chapter Volume 1 windows")
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry.get("chapters", [])}
    chapter_ids = [f"chapter-{number:04d}" for number in range(start, end + 1)]
    missing = [chapter_id for chapter_id in chapter_ids if records.get(chapter_id, {}).get("stage") != "chapter_accepted"]
    if missing:
        return {"valid": False, "errors": ["window has unaccepted chapters: " + ", ".join(missing)]}
    entries = []
    for chapter_id in chapter_ids:
        record = records[chapter_id]
        revision = runtime_path(record["artifacts"]["revision"])
        audit = runtime_path(record["artifacts"]["final_audit"])
        entries.append({
            "chapter_id": chapter_id,
            "revision": str(revision.relative_to(ROOT)),
            "revision_sha256": _sha256(revision),
            "final_audit": str(audit.relative_to(ROOT)),
            "final_verdict": _read_json(audit).get("verdict"),
        })
    packet = {
        "version": VERSION,
        "window": _window_id(start, end),
        "chapter_ids": chapter_ids,
        "chapters": entries,
        "required_checks": [
            "continuous causality and character agency",
            "no unresolved blocking state contradiction",
            "reader-facing scene variation and no repetitive AI-style pattern",
            "window payoff is visible without resolving the volume premise",
        ],
        "allowed_verdicts": ["ACCEPT", "REWORK_REQUIRED"],
    }
    return {"valid": True, "packet": packet}


def record_window_review(payload: dict[str, Any]) -> dict[str, Any]:
    window = str(payload.get("window", ""))
    try:
        start, end = (int(part) for part in window.split("-"))
    except ValueError as error:
        raise RuntimeError("window review must use a canonical window ID") from error
    packet_result = build_window_review_packet(start, end)
    if not packet_result["valid"]:
        raise RuntimeError("; ".join(packet_result["errors"]))
    packet = packet_result["packet"]
    if payload.get("chapter_ids") != packet["chapter_ids"]:
        raise RuntimeError("window review chapter IDs do not match the accepted window")
    expected_hashes = {item["chapter_id"]: item["revision_sha256"] for item in packet["chapters"]}
    if payload.get("revision_hashes") != expected_hashes:
        raise RuntimeError("window review is stale or bound to different revisions")
    if payload.get("verdict") not in {"ACCEPT", "REWORK_REQUIRED"}:
        raise RuntimeError("window review verdict is invalid")
    if not isinstance(payload.get("findings"), list):
        raise RuntimeError("window review findings must be a list")
    target = _window_path(start, end)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"valid": payload["verdict"] == "ACCEPT", "path": str(target.relative_to(ROOT)), "verdict": payload["verdict"]}


def build_release_readiness() -> dict[str, Any]:
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry.get("chapters", [])}
    chapter_errors: list[str] = []
    character_total = 0
    for chapter_id in CHAPTER_IDS:
        record = records.get(chapter_id, {})
        artifacts = record.get("artifacts", {})
        required = ("revision", "revision_metrics", "observation", "settlement", "acceptance")
        audit_key = "final_audit" if "final_audit" in artifacts else "revision_audit"
        if record.get("stage") != "chapter_accepted" or any(key not in artifacts for key in required) or audit_key not in artifacts:
            chapter_errors.append(chapter_id)
            continue
        audit = _read_json(runtime_path(artifacts[audit_key]))
        if audit.get("verdict") not in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}:
            chapter_errors.append(chapter_id)
            continue
        metrics = _read_json(runtime_path(artifacts["revision_metrics"]))
        count = int(metrics.get("chinese_character_count", 0))
        if not 2600 <= count <= 4200:
            chapter_errors.append(chapter_id)
            continue
        character_total += count
    window_errors = []
    for start, end in WINDOWS:
        path = _window_path(start, end)
        if not path.is_file():
            window_errors.append(_window_id(start, end))
            continue
        review = _read_json(path)
        if review.get("verdict") != "ACCEPT":
            window_errors.append(_window_id(start, end))
    checks = {
        "all_100_chapters_accepted": not chapter_errors,
        "all_window_reviews_accepted": not window_errors,
        "volume_character_count_plausible": 260000 <= character_total <= 420000 if not chapter_errors else False,
    }
    return {
        "version": VERSION,
        "valid": all(checks.values()),
        "checks": checks,
        "accepted_chapter_count": 100 - len(chapter_errors),
        "character_total": character_total,
        "missing_or_invalid_chapters": chapter_errors,
        "missing_or_rejected_windows": window_errors,
        "release_root": str(RELEASE_ROOT.relative_to(ROOT)),
    }


def build_fanqie_upload_package() -> dict[str, Any]:
    readiness = build_release_readiness()
    if not readiness["valid"]:
        raise RuntimeError("Fanqie package is blocked: " + json.dumps(readiness["checks"], ensure_ascii=False))
    if RELEASE_ROOT.exists():
        shutil.rmtree(RELEASE_ROOT)
    chapters_root = RELEASE_ROOT / "chapters"
    chapters_root.mkdir(parents=True, exist_ok=True)
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry["chapters"]}
    combined: list[str] = []
    manifest_chapters = []
    for ordinal, chapter_id in enumerate(CHAPTER_IDS, start=1):
        revision = runtime_path(records[chapter_id]["artifacts"]["revision"])
        text = revision.read_text(encoding="utf-8").strip()
        filename = f"{ordinal:03d}_{chapter_id}.txt"
        (chapters_root / filename).write_text(text + "\n", encoding="utf-8")
        combined.extend([f"第{ordinal}章", "", text, ""])
        manifest_chapters.append({"ordinal": ordinal, "chapter_id": chapter_id, "file": f"chapters/{filename}", "sha256": _sha256(revision)})
    (RELEASE_ROOT / "01_volume1_full.txt").write_text("\n".join(combined).strip() + "\n", encoding="utf-8")
    manifest = {"version": VERSION, "project": "《借天改命账》", "volume": 1, "readiness": readiness, "chapters": manifest_chapters}
    (RELEASE_ROOT / "00_submission_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"valid": True, "release_root": str(RELEASE_ROOT.relative_to(ROOT)), "chapter_count": len(manifest_chapters)}
