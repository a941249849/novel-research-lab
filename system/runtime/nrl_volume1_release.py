from __future__ import annotations

"""Release gates and an upload-ready Fanqie package for Volume 1."""

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path
from nrl_antigravity_bridge import find_agy_binary
from nrl_codex_writer import ask_antigravity_writer, ask_codex_writer
from nrl_model_router import route_model


VERSION = "0.25"
MIN_RELEASE_CHINESE_CHARS = 3000
MAX_RELEASE_CHINESE_CHARS = 4200
CHAPTER_IDS = tuple(f"chapter-{number:04d}" for number in range(1, 101))
WINDOWS = tuple((start, start + 9) for start in range(1, 101, 10))
REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")
REVIEW_ROOT = runtime_path("system/production_runtime/window_reviews")
RELEASE_ROOT = runtime_path("system/releases/fanqie/borrowed-heaven-volume1")
MANUSCRIPT_REVIEW_ROOT = runtime_path("system/releases/review")
EDIT_ROOT = runtime_path("system/production_runtime/release_edits")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _window_id(start: int, end: int) -> str:
    return f"{start:03d}-{end:03d}"


def _window_path(start: int, end: int) -> Path:
    return REVIEW_ROOT / f"window-{_window_id(start, end)}.json"


def _edit_manifest_path(chapter_id: str) -> Path:
    return EDIT_ROOT / f"{chapter_id}.json"


def _effective_revision(record: dict[str, Any]) -> tuple[Path, str]:
    source = runtime_path(record["artifacts"]["revision"])
    chapter_id = record["chapter_id"]
    manifest_path = _edit_manifest_path(chapter_id)
    if not manifest_path.is_file():
        return source, "accepted_revision"
    edit = _read_json(manifest_path)
    if edit.get("source_sha256") == _sha256(source):
        candidate = runtime_path(edit.get("release_edit", ""))
        if candidate.is_file():
            return candidate, "release_edit"
    return source, "accepted_revision"


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
        revision, source_kind = _effective_revision(record)
        audit_key = "final_audit" if "final_audit" in record["artifacts"] else "revision_audit"
        audit = runtime_path(record["artifacts"][audit_key])
        entries.append({
            "chapter_id": chapter_id,
            "revision": str(revision.relative_to(ROOT)),
            "source_kind": source_kind,
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


def dispatch_release_edit(chapter_id: str, repair_direction: str) -> dict[str, Any]:
    """Create a release-only editorial revision; accepted runtime history remains immutable."""
    registry = _read_json(REGISTRY_PATH)
    record = next((item for item in registry.get("chapters", []) if item.get("chapter_id") == chapter_id), None)
    if not record or record.get("stage") != "chapter_accepted":
        raise RuntimeError("release edits require an accepted chapter")
    source = runtime_path(record["artifacts"]["revision"])
    original = source.read_text(encoding="utf-8").strip()
    prompt = "\n".join([
        "你是《借天改命账》的发布版责任编辑。只输出重修后的完整章节正文，不要标题、说明或元评论。",
        "这是一项发布版编辑修订：必须保持本章已经发生的状态结果、人物身份、已登记资产和结尾压力，不得新增能力、人物、地点、解决方案或状态变化。",
        "重点修复方向：" + repair_direction,
        "目标 3200-3800 个中文字符。用不同于相邻章节的场景动作、冲突手段和感官落点，避免模板化的识账/咳灰/口述闭环。",
        "原始章节：", original,
    ])
    provider = "codex"
    model = "gpt-5.6-sol"
    try:
        text = ask_codex_writer(prompt, model=model)
    except RuntimeError:
        provider = "antigravity"
        model = route_model("writer")["fallback_model"]
        text = ask_antigravity_writer(prompt, model=model)
    text = re.sub(
        r"^\s*(?:#{1,6}\s*)?第[零〇一二三四五六七八九十百0-9]{1,8}章(?:\s+[^\n]*)?\s*\n+",
        "",
        text.strip(),
        count=1,
    )
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    if not MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS:
        retry_prompt = prompt + (
            f"\n\n上一版只有 {chinese_count} 个中文字符，不合格。请从头输出完整修订稿，"
            "不得续写或解释，正文必须达到 3200-3800 个中文字符。"
        )
        try:
            text = ask_codex_writer(retry_prompt, model="gpt-5.6-sol")
            provider = "codex"
            model = "gpt-5.6-sol"
            text = re.sub(
                r"^\s*(?:#{1,6}\s*)?第[零〇一二三四五六七八九十百0-9]{1,8}章(?:\s+[^\n]*)?\s*\n+",
                "",
                text.strip(),
                count=1,
            )
            chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
        except RuntimeError:
            pass
    if not MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS:
        provider = "antigravity"
        retry_prompt = prompt + (
            f"\n\n此前版本只有 {chinese_count} 个中文字符，不合格。请从头输出完整修订稿，"
            "不得续写或解释，正文必须达到 3200-3800 个中文字符。"
        )
        route = route_model("writer")
        fallback_errors = []
        for model in (route["fallback_model"], route.get("secondary_fallback_model")):
            if not model:
                continue
            try:
                text = ask_antigravity_writer(retry_prompt, model=model)
            except RuntimeError as error:
                fallback_errors.append(str(error))
                continue
            text = re.sub(
                r"^\s*(?:#{1,6}\s*)?第[零〇一二三四五六七八九十百0-9]{1,8}章(?:\s+[^\n]*)?\s*\n+",
                "",
                text.strip(),
                count=1,
            )
            chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
            if MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS:
                break
        else:
            if fallback_errors:
                raise RuntimeError("release edit fallback providers failed: " + "; ".join(fallback_errors))
    if not MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS:
        raise RuntimeError("release edit must contain 3000-4200 Chinese characters")
    target = EDIT_ROOT / f"{chapter_id}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8")
    manifest = {
        "version": VERSION,
        "chapter_id": chapter_id,
        "source_revision": str(source.relative_to(ROOT)),
        "source_sha256": _sha256(source),
        "release_edit": str(target.relative_to(ROOT)),
        "release_edit_sha256": _sha256(target),
        "repair_direction": repair_direction,
        "provider": provider,
        "model": model,
        "status": "pending_window_re_review",
    }
    _edit_manifest_path(chapter_id).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "valid": True,
        "chapter_id": chapter_id,
        "release_edit": manifest["release_edit"],
        "chinese_character_count": chinese_count,
        "provider": provider,
        "model": model,
    }


def record_external_release_edit(
    chapter_id: str,
    source_file: Path,
    repair_direction: str,
    provider: str,
) -> dict[str, Any]:
    """Register an external editor result without altering accepted runtime history."""
    registry = _read_json(REGISTRY_PATH)
    record = next((item for item in registry.get("chapters", []) if item.get("chapter_id") == chapter_id), None)
    if not record or record.get("stage") != "chapter_accepted":
        raise RuntimeError("release edits require an accepted chapter")
    if not source_file.is_file():
        raise RuntimeError("external release edit file is missing")
    text = source_file.read_text(encoding="utf-8").strip()
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    if not MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS:
        raise RuntimeError("external release edit must contain 3000-4200 Chinese characters")
    source = runtime_path(record["artifacts"]["revision"])
    target = EDIT_ROOT / f"{chapter_id}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text + "\n", encoding="utf-8")
    manifest = {
        "version": VERSION,
        "chapter_id": chapter_id,
        "source_revision": str(source.relative_to(ROOT)),
        "source_sha256": _sha256(source),
        "release_edit": str(target.relative_to(ROOT)),
        "release_edit_sha256": _sha256(target),
        "repair_direction": repair_direction,
        "provider": provider,
        "status": "pending_window_re_review",
    }
    _edit_manifest_path(chapter_id).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"valid": True, "chapter_id": chapter_id, "release_edit": manifest["release_edit"], "chinese_character_count": chinese_count, "provider": provider}


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


def dispatch_window_review(start: int, end: int, model: str = "Gemini 3.5 Flash (High)") -> dict[str, Any]:
    packet_result = build_window_review_packet(start, end)
    if not packet_result["valid"]:
        return packet_result
    binary = find_agy_binary()
    if not binary:
        return {"valid": False, "errors": ["agy binary is missing"]}
    packet = packet_result["packet"]
    prose = []
    for chapter in packet["chapters"]:
        prose.extend([f"## {chapter['chapter_id']}", (ROOT / chapter["revision"]).read_text(encoding="utf-8").strip(), ""])
    template = {
        "window": packet["window"],
        "chapter_ids": packet["chapter_ids"],
        "revision_hashes": {item["chapter_id"]: item["revision_sha256"] for item in packet["chapters"]},
        "verdict": "ACCEPT",
        "findings": [],
    }
    prompt = "\n".join([
        "你是 Novel Research Lab 的独立卷内审查者。只返回一个 JSON 对象，不要 Markdown、计划或正文。",
        "审查连续因果、人物能动性、状态一致性、节奏兑现和重复 AI 味。不得用未出现事实补写剧情。",
        "若存在阻断问题，verdict 必须为 REWORK_REQUIRED；否则 ACCEPT。findings 中逐项给证据与修复方向。",
        "窗口元数据：", json.dumps(packet, ensure_ascii=False), "", "章节终稿：", "\n".join(prose),
        "", "输出模板：", json.dumps(template, ensure_ascii=False),
    ])
    try:
        with tempfile.TemporaryDirectory(prefix="nrl-volume1-window-review-") as cwd:
            result = subprocess.run(
                [binary, "--model", model, "--mode", "plan", "--sandbox", "--print-timeout", "12m0s", "-p", prompt],
                cwd=cwd, text=True, capture_output=True, check=False, timeout=780,
            )
    except subprocess.TimeoutExpired:
        return {"valid": False, "errors": ["window review timed out after 780s"]}
    if result.returncode != 0:
        return {"valid": False, "errors": [f"window review provider failed with exit code {result.returncode}"], "stderr": result.stderr.strip()[:1000]}
    response = (result.stdout or result.stderr).strip()
    try:
        match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
        payload = json.loads(match.group(1) if match else response)
    except json.JSONDecodeError as error:
        return {"valid": False, "errors": [f"window review returned invalid JSON: {error}"], "response_preview": response[:1000]}
    try:
        return record_window_review(payload)
    except RuntimeError as error:
        return {"valid": False, "errors": [str(error)]}


def prior_window_review_required(chapter_id: str) -> bool:
    try:
        ordinal = int(chapter_id.removeprefix("chapter-"))
    except ValueError:
        return False
    if ordinal <= 20 or ordinal > 100 or (ordinal - 1) % 10:
        return False
    path = _window_path(ordinal - 10, ordinal - 1)
    return not path.is_file() or _read_json(path).get("verdict") != "ACCEPT"


def build_release_readiness() -> dict[str, Any]:
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry.get("chapters", [])}
    chapter_errors: list[str] = []
    accepted_registry_count = sum(
        1 for chapter_id in CHAPTER_IDS if records.get(chapter_id, {}).get("stage") == "chapter_accepted"
    )
    character_total = 0
    accepted_character_total = 0
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
        effective, _ = _effective_revision(record)
        if effective == runtime_path(artifacts["revision"]):
            metrics = _read_json(runtime_path(artifacts["revision_metrics"]))
            count = int(metrics.get("chinese_character_count", 0))
        else:
            count = len(re.findall(r"[\u4e00-\u9fff]", effective.read_text(encoding="utf-8")))
        accepted_character_total += count
        if not MIN_RELEASE_CHINESE_CHARS <= count <= MAX_RELEASE_CHINESE_CHARS:
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
        "volume_character_count_plausible": 300000 <= character_total <= 420000 if not chapter_errors else False,
    }
    return {
        "version": VERSION,
        "valid": all(checks.values()),
        "checks": checks,
        "accepted_chapter_count": accepted_registry_count,
        "release_ready_chapter_count": 100 - len(chapter_errors),
        "character_total": accepted_character_total,
        "release_ready_character_total": character_total,
        "missing_or_invalid_chapters": chapter_errors,
        "missing_or_rejected_windows": window_errors,
        "release_root": str(RELEASE_ROOT.relative_to(ROOT)),
    }


def build_review_manuscript(end: int = 20) -> dict[str, Any]:
    """Materialize accepted chapters for human reading without claiming release readiness."""
    if not 1 <= end <= 100:
        raise ValueError("review manuscript end must be within 1-100")
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry.get("chapters", [])}
    sections = [f"# 《借天改命账》第 1-{end} 章审阅稿", ""]
    hashes = {}
    character_total = 0
    for ordinal in range(1, end + 1):
        chapter_id = f"chapter-{ordinal:04d}"
        record = records.get(chapter_id)
        if not record or record.get("stage") != "chapter_accepted":
            raise RuntimeError(f"review manuscript requires accepted chapter: {chapter_id}")
        revision, source_kind = _effective_revision(record)
        text = revision.read_text(encoding="utf-8").strip()
        character_total += len(re.findall(r"[\u4e00-\u9fff]", text))
        hashes[chapter_id] = {"sha256": _sha256(revision), "source_kind": source_kind}
        sections.extend([f"## 第 {ordinal} 章", "", text, ""])
    MANUSCRIPT_REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    manuscript = MANUSCRIPT_REVIEW_ROOT / f"borrowed-heaven-chapters-001-{end:03d}.md"
    manuscript.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    manifest = MANUSCRIPT_REVIEW_ROOT / f"borrowed-heaven-chapters-001-{end:03d}.json"
    payload = {
        "version": VERSION,
        "status": "human_review_only_not_release_ready",
        "chapter_range": [1, end],
        "chapter_count": end,
        "chinese_character_total": character_total,
        "manuscript": str(manuscript.relative_to(ROOT)),
        "manuscript_sha256": _sha256(manuscript),
        "chapters": hashes,
    }
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**payload, "manifest": str(manifest.relative_to(ROOT))}


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
        revision, _ = _effective_revision(records[chapter_id])
        text = revision.read_text(encoding="utf-8").strip()
        filename = f"{ordinal:03d}_{chapter_id}.txt"
        (chapters_root / filename).write_text(text + "\n", encoding="utf-8")
        combined.extend([f"第{ordinal}章", "", text, ""])
        manifest_chapters.append({"ordinal": ordinal, "chapter_id": chapter_id, "file": f"chapters/{filename}", "sha256": _sha256(revision)})
    (RELEASE_ROOT / "01_volume1_full.txt").write_text("\n".join(combined).strip() + "\n", encoding="utf-8")
    manifest = {"version": VERSION, "project": "《借天改命账》", "volume": 1, "readiness": readiness, "chapters": manifest_chapters}
    (RELEASE_ROOT / "00_submission_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"valid": True, "release_root": str(RELEASE_ROOT.relative_to(ROOT)), "chapter_count": len(manifest_chapters)}
