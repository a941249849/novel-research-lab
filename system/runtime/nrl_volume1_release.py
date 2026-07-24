from __future__ import annotations

"""Release gates and an upload-ready Fanqie package for Volume 1."""

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path
from nrl_codex_writer import ask_antigravity_writer, ask_codex_writer, codex_usage_limited, extract_json_object
from nrl_model_router import route_model
from nrl_projects import active_project_id, active_project_title
from nrl_project_production import volume1_chapter_count, volume1_windows


VERSION = "0.26"
MIN_RELEASE_CHINESE_CHARS = 3000
MAX_RELEASE_CHINESE_CHARS = 4200
def _chapter_ids() -> tuple[str, ...]:
    return tuple(
        f"chapter-{number:04d}" for number in range(1, volume1_chapter_count() + 1)
    )


def _windows() -> tuple[tuple[int, int], ...]:
    return volume1_windows()


# Compatibility snapshots for callers that import the active project module once.
# Runtime functions still derive these values dynamically for project-scoped CLI use.
CHAPTER_IDS = _chapter_ids()
WINDOWS = _windows()


REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")
REVIEW_ROOT = runtime_path("system/production_runtime/window_reviews")
RELEASE_ROOT = runtime_path(f"system/releases/fanqie/{active_project_id()}-volume1")
MANUSCRIPT_REVIEW_ROOT = runtime_path("system/releases/review")
EDIT_ROOT = runtime_path("system/production_runtime/release_edits")
TITLE_REGISTRY_PATH = runtime_path("system/production_runtime/chapter_titles.volume1.json")


def _latin_token_markers(text: str) -> list[str]:
    return re.findall(r"(?<![A-Za-z])[A-Za-z]{2,}(?![A-Za-z])", text)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _formal_execution_errors(
    record: dict[str, Any], role: str, artifact_path: Path
) -> list[str]:
    ref = record.get("artifacts", {}).get(f"{role}_execution", "")
    path = runtime_path(ref)
    if not path.is_file():
        return [f"missing {role} execution"]
    payload = _read_json(path)
    expected_model = {
        "writer": "gpt-5.6-terra",
        "observer": "gpt-5.6-luna",
        "reviewer": "gpt-5.6-sol",
    }[role]
    errors = []
    if payload.get("chapter_id") != record.get("chapter_id") or payload.get("role") != role:
        errors.append(f"invalid {role} execution identity")
    if payload.get("provider") != "codex" or payload.get("model") != expected_model:
        errors.append(f"{role} execution must use Codex {expected_model}")
    if payload.get("artifact") != str(artifact_path.relative_to(ROOT)) or payload.get("artifact_sha256") != _sha256(artifact_path):
        errors.append(f"stale {role} execution artifact")
    revision = runtime_path(record.get("artifacts", {}).get("revision", ""))
    if role in {"observer", "reviewer"} and (
        not revision.is_file() or payload.get("revision_sha256") != _sha256(revision)
    ):
        errors.append(f"stale {role} revision binding")
    if role == "reviewer" and payload.get("audit_artifact_sha256") != _sha256(artifact_path):
        errors.append("stale reviewer audit binding")
    return errors


def load_volume1_titles() -> dict[str, str]:
    payload = _read_json(TITLE_REGISTRY_PATH)
    entries = payload.get("chapters", [])
    titles = {str(item.get("chapter_id", "")): str(item.get("title", "")).strip() for item in entries}
    chapter_ids = _chapter_ids()
    if set(titles) != set(chapter_ids) or len(entries) != len(chapter_ids):
        raise RuntimeError("Volume 1 title registry must contain each chapter exactly once")
    if len(set(titles.values())) != len(chapter_ids):
        raise RuntimeError("Volume 1 chapter titles must be unique")
    invalid = [chapter_id for chapter_id, title in titles.items() if not 2 <= len(title) <= 16 or re.search(r"第\s*\d+\s*章", title)]
    if invalid:
        raise RuntimeError("invalid Volume 1 chapter titles: " + ", ".join(invalid))
    return titles


def _window_id(start: int, end: int) -> str:
    return f"{start:03d}-{end:03d}"


def _window_path(start: int, end: int) -> Path:
    return REVIEW_ROOT / f"window-{_window_id(start, end)}.json"


def _independent_window_path(start: int, end: int) -> Path:
    return REVIEW_ROOT / f"window-{_window_id(start, end)}.independent.json"


def _window_execution_path(start: int, end: int, *, independent: bool = False) -> Path:
    suffix = ".independent.execution.json" if independent else ".execution.json"
    return REVIEW_ROOT / f"window-{_window_id(start, end)}{suffix}"


def _payload_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    ).hexdigest()


def _window_execution_valid(
    start: int,
    end: int,
    review: dict[str, Any],
    expected_ids: list[str],
    expected_hashes: dict[str, str],
    *,
    independent: bool = False,
) -> bool:
    review_path = _independent_window_path(start, end) if independent else _window_path(start, end)
    execution_path = _window_execution_path(start, end, independent=independent)
    if not review_path.is_file() or not execution_path.is_file():
        return False
    execution = _read_json(execution_path)
    expected_provider = "antigravity" if independent else "codex"
    expected_model = None if independent else "gpt-5.6-sol"
    return bool(
        execution.get("window") == _window_id(start, end)
        and execution.get("role") == (
            "independent_window_reviewer" if independent else "primary_window_reviewer"
        )
        and execution.get("review_artifact") == str(review_path.relative_to(ROOT))
        and execution.get("review_artifact_sha256") == _sha256(review_path)
        and execution.get("review_payload_sha256") == _payload_sha256(review)
        and execution.get("chapter_ids") == expected_ids
        and execution.get("revision_hashes") == expected_hashes
        and execution.get("provider") == expected_provider
        and (independent or execution.get("model") == expected_model)
        and (not independent or bool(execution.get("model")))
        and review.get("review_provider") == expected_provider
        and (independent or review.get("review_model") == expected_model)
        and (not independent or review.get("review_model") == execution.get("model"))
        and (independent or review.get("fallback_used") is False)
    )


def _window_requires_independent_review(start: int, end: int) -> bool:
    if active_project_id() == "borrowed-heaven":
        return False
    contract = runtime_path(
        f"system/production_runtime/story_windows/window-{start:03d}-{end:03d}.v1.json"
    )
    return bool(
        contract.is_file()
        and _read_json(contract).get("review_policy", {}).get("independent_antigravity_required")
    )


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
    if (start, end) not in _windows():
        raise ValueError("window must be one of the canonical Volume 1 windows")
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
        metrics_path = runtime_path(record["artifacts"].get("revision_metrics", ""))
        execution_path = runtime_path(record["artifacts"].get("final_audit_execution", ""))
        if active_project_id() != "borrowed-heaven" and (not metrics_path.is_file() or not execution_path.is_file()):
            return {"valid": False, "errors": [f"window quality evidence is incomplete: {chapter_id}"]}
        metrics = _read_json(metrics_path) if metrics_path.is_file() else {}
        final_audit = _read_json(audit)
        if active_project_id() != "borrowed-heaven":
            execution_errors = []
            execution_errors.extend(_formal_execution_errors(record, "writer", revision))
            observation_path = runtime_path(record["artifacts"].get("observation", ""))
            if not observation_path.is_file():
                execution_errors.append("missing observation artifact")
            else:
                execution_errors.extend(_formal_execution_errors(record, "observer", observation_path))
            execution_errors.extend(_formal_execution_errors(record, "reviewer", audit))
            if execution_errors:
                return {"valid": False, "errors": [f"window quality execution failed: {chapter_id}: " + "; ".join(execution_errors)]}
        if active_project_id() != "borrowed-heaven" and (
            not MIN_RELEASE_CHINESE_CHARS <= int(metrics.get("chinese_character_count", 0)) <= MAX_RELEASE_CHINESE_CHARS
            or any(item.get("severity") in {"blocking", "major"} for item in final_audit.get("issues", []))
        ):
            return {"valid": False, "errors": [f"window quality gate failed: {chapter_id}"]}
        entries.append({
            "chapter_id": chapter_id,
            "revision": str(revision.relative_to(ROOT)),
            "source_kind": source_kind,
            "revision_sha256": _sha256(revision),
            "final_audit": str(audit.relative_to(ROOT)),
            "final_verdict": final_audit.get("verdict"),
            "quality_metrics": metrics,
            "final_audit_execution": str(execution_path.relative_to(ROOT)) if execution_path.is_file() else None,
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
        f"你是{active_project_title()}的发布版责任编辑。只输出重修后的完整章节正文，不要标题、说明或元评论。",
        "这是一项发布版编辑修订：必须保持本章已经发生的状态结果、人物身份、已登记资产和结尾压力，不得新增能力、人物、地点、解决方案或状态变化。",
        "重点修复方向：" + repair_direction,
        "目标 3200-3800 个中文字符。用不同于相邻章节的场景动作、冲突手段和感官落点，避免模板化的识账/咳灰/口述闭环。",
        "原始章节：", original,
    ])
    editor = route_model("editor")
    provider = "codex"
    model = editor["model"]
    try:
        if codex_usage_limited():
            raise RuntimeError("Codex usage limit already detected in this batch")
        text = ask_codex_writer(prompt, model=model)
    except RuntimeError:
        provider = "antigravity"
        model = editor["fallback_model"]
        text = ask_antigravity_writer(prompt, model=model)
    text = re.sub(
        r"^\s*(?:#{1,6}\s*)?第[零〇一二三四五六七八九十百0-9]{1,8}章(?:\s+[^\n]*)?\s*\n+",
        "",
        text.strip(),
        count=1,
    )
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    candidates = [(text, chinese_count, provider, model)]
    if (
        not MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS
        or _latin_token_markers(text)
    ):
        retry_prompt = prompt + (
            f"\n\n上一版只有 {chinese_count} 个中文字符，不合格。请从头输出完整修订稿，"
            "不得续写或解释，正文必须达到 3200-3800 个中文字符。"
        )
        provider = "antigravity"
        model = editor["fallback_model"]
        text = ask_antigravity_writer(retry_prompt, model=model)
        text = re.sub(
            r"^\s*(?:#{1,6}\s*)?第[零〇一二三四五六七八九十百0-9]{1,8}章(?:\s+[^\n]*)?\s*\n+",
            "", text.strip(), count=1,
        )
        chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
        candidates.append((text, chinese_count, provider, model))
    if (
        not MIN_RELEASE_CHINESE_CHARS <= chinese_count <= MAX_RELEASE_CHINESE_CHARS
        or _latin_token_markers(text)
    ):
        def distance(candidate: tuple[str, int, str, str]) -> int:
            count = candidate[1]
            if count < MIN_RELEASE_CHINESE_CHARS:
                return MIN_RELEASE_CHINESE_CHARS - count
            if count > MAX_RELEASE_CHINESE_CHARS:
                return count - MAX_RELEASE_CHINESE_CHARS
            return 0

        text, chinese_count, provider, model = min(candidates, key=distance)
        recovery = EDIT_ROOT / f"{chapter_id}.recovery_candidate.md"
        recovery.parent.mkdir(parents=True, exist_ok=True)
        recovery.write_text(text.strip() + "\n", encoding="utf-8")
        raise RuntimeError(
            "release edit must contain 3000-4200 Chinese characters and no leaked Latin tokens; "
            f"best candidate has {chinese_count} and was saved to "
            f"{recovery.relative_to(ROOT)}"
        )
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
    latin_tokens = _latin_token_markers(text)
    if latin_tokens:
        raise RuntimeError(
            "external release edit contains leaked Latin tokens: "
            + ", ".join(latin_tokens[:10])
        )
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


def record_window_review(
    payload: dict[str, Any], execution: dict[str, Any] | None = None
) -> dict[str, Any]:
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
    if active_project_id() != "borrowed-heaven" and (
        payload.get("review_provider") != "codex"
        or payload.get("review_model") != "gpt-5.6-sol"
        or payload.get("fallback_used") is not False
    ):
        raise RuntimeError("formal primary window review must be executed by Codex gpt-5.6-sol")
    if active_project_id() != "borrowed-heaven" and (
        not execution
        or execution.get("role") != "primary_window_reviewer"
        or execution.get("window") != _window_id(start, end)
        or execution.get("chapter_ids") != packet["chapter_ids"]
        or execution.get("revision_hashes") != expected_hashes
        or execution.get("provider") != "codex"
        or execution.get("model") != "gpt-5.6-sol"
    ):
        raise RuntimeError("formal primary window review requires runtime-bound Sol execution evidence")
    target = _window_path(start, end)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    execution_target = _window_execution_path(start, end)
    if execution is not None:
        execution_payload = {
            "version": "0.28",
            **execution,
            "review_artifact": str(target.relative_to(ROOT)),
            "review_artifact_sha256": _sha256(target),
            "review_payload_sha256": _payload_sha256(payload),
        }
        execution_target.write_text(
            json.dumps(execution_payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    for chapter in packet["chapters"]:
        if chapter["source_kind"] != "release_edit":
            continue
        manifest_path = _edit_manifest_path(chapter["chapter_id"])
        manifest = _read_json(manifest_path)
        manifest.update({
            "status": (
                "approved_by_window_review"
                if payload["verdict"] == "ACCEPT"
                else "rework_required_by_window_review"
            ),
            "window_review": str(target.relative_to(ROOT)),
            "reviewed_release_edit_sha256": chapter["revision_sha256"],
        })
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {
        "valid": payload["verdict"] == "ACCEPT",
        "path": str(target.relative_to(ROOT)),
        "execution": str(execution_target.relative_to(ROOT)) if execution is not None else None,
        "verdict": payload["verdict"],
    }


def record_independent_window_review(
    payload: dict[str, Any], execution: dict[str, Any] | None = None
) -> dict[str, Any]:
    window = str(payload.get("window", ""))
    try:
        start, end = (int(part) for part in window.split("-"))
    except ValueError as error:
        raise RuntimeError("independent review must use a canonical window ID") from error
    packet_result = build_window_review_packet(start, end)
    if not packet_result["valid"]:
        raise RuntimeError("; ".join(packet_result["errors"]))
    packet = packet_result["packet"]
    expected_hashes = {item["chapter_id"]: item["revision_sha256"] for item in packet["chapters"]}
    if payload.get("review_provider") != "antigravity":
        raise RuntimeError("independent window review must be produced by Antigravity")
    if payload.get("chapter_ids") != packet["chapter_ids"] or payload.get("revision_hashes") != expected_hashes:
        raise RuntimeError("independent window review is stale or bound to different revisions")
    if payload.get("verdict") not in {"ACCEPT", "REWORK_REQUIRED"} or not isinstance(payload.get("findings"), list):
        raise RuntimeError("independent window review verdict or findings are invalid")
    if not payload.get("review_model"):
        raise RuntimeError("independent window review must declare its review model")
    if execution is not None and payload.get("review_model") != execution.get("model"):
        raise RuntimeError("independent window review model does not match execution evidence")
    if active_project_id() != "borrowed-heaven" and (
        not execution
        or execution.get("role") != "independent_window_reviewer"
        or execution.get("window") != _window_id(start, end)
        or execution.get("chapter_ids") != packet["chapter_ids"]
        or execution.get("revision_hashes") != expected_hashes
        or execution.get("provider") != "antigravity"
        or not execution.get("model")
    ):
        raise RuntimeError("formal independent window review requires runtime-bound Antigravity execution evidence")
    target = _independent_window_path(start, end)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    execution_target = _window_execution_path(start, end, independent=True)
    if execution is not None:
        execution_payload = {
            "version": "0.28",
            **execution,
            "review_artifact": str(target.relative_to(ROOT)),
            "review_artifact_sha256": _sha256(target),
            "review_payload_sha256": _payload_sha256(payload),
        }
        execution_target.write_text(
            json.dumps(execution_payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {
        "valid": payload["verdict"] == "ACCEPT",
        "path": str(target.relative_to(ROOT)),
        "execution": str(execution_target.relative_to(ROOT)) if execution is not None else None,
        "verdict": payload["verdict"],
    }


def dispatch_independent_window_review(start: int, end: int, model: str | None = None) -> dict[str, Any]:
    packet_result = build_window_review_packet(start, end)
    if not packet_result["valid"]:
        return packet_result
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
        "review_provider": "antigravity",
        "review_model": model or route_model("reviewer")["fallback_model"],
    }
    prompt = "\n".join([
        "你是独立于 Codex Sol 的 Antigravity 卷内终审者。只返回一个 JSON 对象，不改写正文。",
        "独立判断连续因果、人物生命力、文化边界、AI 味和状态一致性；任何实质问题必须 REWORK_REQUIRED。",
        "窗口契约：", json.dumps(packet, ensure_ascii=False), "章节终稿：", "\n".join(prose),
        "输出模板：", json.dumps(template, ensure_ascii=False),
    ])
    used_model = model or route_model("reviewer")["fallback_model"]
    try:
        payload = extract_json_object(ask_antigravity_writer(prompt, model=used_model, timeout_seconds=900))
        payload.update({"review_provider": "antigravity", "review_model": used_model})
        return record_independent_window_review(
            payload,
            execution={
                "role": "independent_window_reviewer",
                "window": packet["window"],
                "chapter_ids": packet["chapter_ids"],
                "revision_hashes": template["revision_hashes"],
                "provider": "antigravity",
                "model": used_model,
            },
        )
    except RuntimeError as error:
        return {"valid": False, "errors": [str(error)], "review_provider": "antigravity", "review_model": used_model}


def dispatch_window_review(start: int, end: int, model: str | None = None) -> dict[str, Any]:
    packet_result = build_window_review_packet(start, end)
    if not packet_result["valid"]:
        return packet_result
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
    reviewer = route_model("reviewer")
    provider = "codex"
    used_model = reviewer["model"]
    try:
        response = ask_codex_writer(prompt, model=used_model, timeout_seconds=600)
        payload = extract_json_object(response)
    except RuntimeError as primary_error:
        if active_project_id() != "borrowed-heaven":
            return {
                "valid": False,
                "errors": [str(primary_error)],
                "review_provider": "codex",
                "review_model": used_model,
            }
        provider = "antigravity"
        used_model = model or reviewer["fallback_model"]
        try:
            response = ask_antigravity_writer(prompt, model=used_model, timeout_seconds=780)
            payload = extract_json_object(response)
        except RuntimeError as fallback_error:
            return {
                "valid": False,
                "errors": [str(primary_error), str(fallback_error)],
                "review_provider": provider,
                "review_model": used_model,
            }
    try:
        payload = {
            **payload,
            "review_provider": provider,
            "review_model": used_model,
            "fallback_used": provider == "antigravity",
        }
        result = record_window_review(
            payload,
            execution={
                "role": "primary_window_reviewer",
                "window": packet["window"],
                "chapter_ids": packet["chapter_ids"],
                "revision_hashes": template["revision_hashes"],
                "provider": provider,
                "model": used_model,
            },
        )
        return {**result, "review_provider": provider, "review_model": used_model}
    except RuntimeError as error:
        return {"valid": False, "errors": [str(error)]}


def prior_window_review_required(chapter_id: str) -> bool:
    try:
        ordinal = int(chapter_id.removeprefix("chapter-"))
    except ValueError:
        return False
    chapter_count = volume1_chapter_count()
    minimum_gated = 20 if active_project_id() == "borrowed-heaven" else 10
    if ordinal <= minimum_gated or ordinal > chapter_count or (ordinal - 1) % 10:
        return False
    start, end = ordinal - 10, ordinal - 1
    path = _window_path(start, end)
    if not path.is_file():
        return True
    packet = build_window_review_packet(start, end)
    if not packet["valid"]:
        return True
    expected_hashes = {
        item["chapter_id"]: item["revision_sha256"]
        for item in packet["packet"]["chapters"]
    }
    review = _read_json(path)
    sol_blocked = (
        review.get("verdict") != "ACCEPT"
        or review.get("chapter_ids") != packet["packet"]["chapter_ids"]
        or review.get("revision_hashes") != expected_hashes
        or (
            active_project_id() != "borrowed-heaven"
            and not _window_execution_valid(
                start, end, review, packet["packet"]["chapter_ids"], expected_hashes
            )
        )
    )
    if sol_blocked:
        return True
    if _window_requires_independent_review(start, end):
        independent_path = _independent_window_path(start, end)
        if not independent_path.is_file():
            return True
        independent = _read_json(independent_path)
        return (
            independent.get("verdict") != "ACCEPT"
            or independent.get("review_provider") != "antigravity"
            or independent.get("chapter_ids") != packet["packet"]["chapter_ids"]
            or independent.get("revision_hashes") != expected_hashes
            or not _window_execution_valid(
                start,
                end,
                independent,
                packet["packet"]["chapter_ids"],
                expected_hashes,
                independent=True,
            )
        )
    return False


def build_release_readiness() -> dict[str, Any]:
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry.get("chapters", [])}
    chapter_errors: list[str] = []
    chapter_ids = _chapter_ids()
    windows = _windows()
    accepted_registry_count = sum(
        1 for chapter_id in chapter_ids if records.get(chapter_id, {}).get("stage") == "chapter_accepted"
    )
    character_total = 0
    accepted_character_total = 0
    for chapter_id in chapter_ids:
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
    independent_window_errors = []
    for start, end in windows:
        path = _window_path(start, end)
        if not path.is_file():
            window_errors.append(_window_id(start, end))
            if _window_requires_independent_review(start, end):
                independent_window_errors.append(_window_id(start, end))
            continue
        review = _read_json(path)
        expected_ids = [f"chapter-{number:04d}" for number in range(start, end + 1)]
        expected_hashes = {}
        for chapter_id in expected_ids:
            record = records.get(chapter_id)
            if (
                not record
                or record.get("stage") != "chapter_accepted"
                or "revision" not in record.get("artifacts", {})
            ):
                continue
            revision, _ = _effective_revision(record)
            expected_hashes[chapter_id] = _sha256(revision)
        if (
            review.get("verdict") != "ACCEPT"
            or review.get("chapter_ids") != expected_ids
            or review.get("revision_hashes") != expected_hashes
            or (
                active_project_id() != "borrowed-heaven"
                and not _window_execution_valid(start, end, review, expected_ids, expected_hashes)
            )
        ):
            window_errors.append(_window_id(start, end))
        if _window_requires_independent_review(start, end):
            independent_path = _independent_window_path(start, end)
            independent = _read_json(independent_path) if independent_path.is_file() else {}
            if (
                independent.get("verdict") != "ACCEPT"
                or independent.get("review_provider") != "antigravity"
                or independent.get("chapter_ids") != expected_ids
                or independent.get("revision_hashes") != expected_hashes
                or not _window_execution_valid(
                    start,
                    end,
                    independent,
                    expected_ids,
                    expected_hashes,
                    independent=True,
                )
            ):
                independent_window_errors.append(_window_id(start, end))
    try:
        titles = load_volume1_titles()
        titles_complete = len(titles) == len(chapter_ids)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError):
        titles_complete = False
    accepted_key = "all_100_chapters_accepted" if active_project_id() == "borrowed-heaven" else "all_volume_chapters_accepted"
    checks = {
        accepted_key: not chapter_errors,
        "all_window_reviews_accepted": not window_errors,
        "all_required_independent_window_reviews_accepted": not independent_window_errors,
        "volume_character_count_plausible": len(chapter_ids) * 3000 <= character_total <= len(chapter_ids) * 4200 if not chapter_errors else False,
        "chapter_titles_complete": titles_complete,
    }
    return {
        "version": VERSION,
        "valid": all(checks.values()),
        "checks": checks,
        "accepted_chapter_count": accepted_registry_count,
        "release_ready_chapter_count": len(chapter_ids) - len(chapter_errors),
        "character_total": accepted_character_total,
        "release_ready_character_total": character_total,
        "missing_or_invalid_chapters": chapter_errors,
        "missing_or_rejected_windows": window_errors,
        "missing_or_rejected_independent_windows": independent_window_errors,
        "release_root": str(RELEASE_ROOT.relative_to(ROOT)),
    }


def build_review_manuscript(end: int = 20) -> dict[str, Any]:
    """Materialize accepted chapters for human reading without claiming release readiness."""
    chapter_count = volume1_chapter_count()
    if not 1 <= end <= chapter_count:
        raise ValueError(f"review manuscript end must be within 1-{chapter_count}")
    registry = _read_json(REGISTRY_PATH)
    records = {item["chapter_id"]: item for item in registry.get("chapters", [])}
    sections = [f"# {active_project_title()}第 1-{end} 章审阅稿", ""]
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
    manuscript = MANUSCRIPT_REVIEW_ROOT / f"{active_project_id()}-chapters-001-{end:03d}.md"
    manuscript.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    manifest = MANUSCRIPT_REVIEW_ROOT / f"{active_project_id()}-chapters-001-{end:03d}.json"
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
    titles = load_volume1_titles()
    combined: list[str] = []
    manifest_chapters = []
    for ordinal, chapter_id in enumerate(_chapter_ids(), start=1):
        revision, _ = _effective_revision(records[chapter_id])
        text = revision.read_text(encoding="utf-8").strip()
        title = titles[chapter_id]
        heading = f"第{ordinal}章 {title}"
        filename = f"{ordinal:03d}_{title}.txt"
        output_path = chapters_root / filename
        output_path.write_text(f"{heading}\n\n{text}\n", encoding="utf-8")
        combined.extend([heading, "", text, ""])
        manifest_chapters.append({
            "ordinal": ordinal,
            "chapter_id": chapter_id,
            "title": title,
            "file": f"chapters/{filename}",
            "body_sha256": _sha256(revision),
            "file_sha256": _sha256(output_path),
        })
    manuscript_path = RELEASE_ROOT / "01_volume1_full.txt"
    manuscript_path.write_text("\n".join(combined).strip() + "\n", encoding="utf-8")
    manifest = {
        "version": VERSION,
        "project_id": active_project_id(),
        "project": active_project_title(),
        "volume": 1,
        "readiness": readiness,
        "full_manuscript": "01_volume1_full.txt",
        "full_manuscript_sha256": _sha256(manuscript_path),
        "chapters": manifest_chapters,
    }
    (RELEASE_ROOT / "00_submission_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"valid": True, "release_root": str(RELEASE_ROOT.relative_to(ROOT)), "chapter_count": len(manifest_chapters)}
