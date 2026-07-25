from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECTS_ROOT = ROOT / "projects"
DECISIONS_PATH = ROOT / "system/runtime/owner_gate_decisions.json"
CHAPTER_HEADING = re.compile(r"^## 第(\d+)章\s+(.+?)\s*$", re.MULTILINE)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_chapter_document(text: str) -> list[dict[str, Any]]:
    matches = list(CHAPTER_HEADING.finditer(text))
    chapters: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        chapters.append({
            "chapter": int(match.group(1)),
            "title": match.group(2).strip(),
            "body": body,
            "character_count": len(re.sub(r"\s+", "", body)),
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        })
    return chapters


def _owner_decision(decision_id: str) -> dict[str, Any] | None:
    payload = _read_json(DECISIONS_PATH)
    decisions = payload if isinstance(payload, list) else payload.get("decisions", [])
    return next((item for item in decisions if item.get("decision_id") == decision_id), None)


def validate_continuity_contract(project_id: str, *, require_prose: bool = True) -> dict[str, Any]:
    workspace = PROJECTS_ROOT / project_id
    contract_path = workspace / "production_runtime/plans/continuity_validation.v0.1.json"
    errors: list[str] = []
    if not contract_path.exists():
        return {"valid": False, "errors": [f"missing contract: {contract_path}"]}

    contract = _read_json(contract_path)
    start, end = contract.get("chapter_range", [0, -1])
    covered = [item.get("chapter") for item in contract.get("chapter_state_deltas", [])]
    expected_covered = list(range(start, end + 1))
    if covered != expected_covered:
        errors.append(f"chapter state coverage must be exact: {expected_covered}")

    anchors = contract.get("read_only_anchor_chapters", [])
    generated = contract.get("generated_chapters", [])
    if sorted(anchors + generated) != expected_covered:
        errors.append("anchor and generated chapters must partition the chapter range")
    if set(anchors) & set(generated):
        errors.append("anchor chapters cannot be generated")
    anchor_paths = {
        "10": workspace / "production_runtime/samples/window-008-010.md",
        "24-26": workspace / "production_runtime/samples/window-024-026.md",
    }
    for anchor_id, expected_hash in contract.get("read_only_anchor_hashes", {}).items():
        path = anchor_paths.get(anchor_id)
        if path is None or not path.exists():
            errors.append(f"missing read-only anchor: {anchor_id}")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"read-only anchor changed: {anchor_id}")
    if any(chapter >= 28 for chapter in generated):
        errors.append("continuity validation cannot generate chapter 28 or later")
    if contract.get("continuous_prose_authorized"):
        errors.append("continuous prose must remain unauthorized")
    if contract.get("publish_authorized"):
        errors.append("publication must remain unauthorized")

    review_result = contract.get("review_result", {})
    review_verdict = str(review_result.get("verdict", ""))
    if contract.get("status") == "continuity_test_passed":
        review_path_value = str(contract.get("internal_review", ""))
        review_path = workspace / review_path_value
        if not review_path_value or not review_path.is_file():
            errors.append("accepted continuity review is missing")
        elif "`ACCEPT_CONTINUITY_TEST`" not in review_path.read_text(encoding="utf-8"):
            errors.append("continuity review does not accept the test")
        if review_verdict != "ACCEPT_CONTINUITY_TEST":
            errors.append("contract review verdict does not accept the continuity test")

    decision = _owner_decision(str(contract.get("owner_decision_id", "")))
    if decision is None:
        errors.append("bounded owner decision not found")
    else:
        authorized = set(decision.get("authorized_scope", []))
        for chapter in generated:
            scope = f"{project_id}:chapter-{chapter:03d}"
            if scope not in authorized:
                errors.append(f"owner decision missing scope: {scope}")
        forbidden = set(decision.get("forbidden_scope", []))
        required_forbidden = {
            f"{project_id}:chapter-028-or-later",
            f"{project_id}:continuous-production",
            f"{project_id}:publish",
        }
        if not required_forbidden.issubset(forbidden):
            errors.append("owner decision does not preserve all production boundaries")
        if decision.get("bound_response_sha256") != contract.get("bound_review_sha256"):
            errors.append("owner decision is not bound to the accepted review")

    established: set[str] = set()
    for delta in contract.get("chapter_state_deltas", []):
        chapter = delta.get("chapter")
        missing = [key for key in delta.get("requires", []) if key not in established]
        if missing:
            errors.append(f"chapter {chapter} requires unavailable states: {missing}")
        if not delta.get("establishes"):
            errors.append(f"chapter {chapter} has no explicit state delta")
        if not delta.get("must_carry"):
            errors.append(f"chapter {chapter} has no carry-forward requirement")
        established.update(delta.get("establishes", []))

    prose_chapters: list[dict[str, Any]] = []
    for block in contract.get("blocks", []):
        output = workspace / str(block.get("output_path", ""))
        if not output.exists():
            if require_prose:
                errors.append(f"missing prose block: {output.relative_to(ROOT)}")
            continue
        parsed = split_chapter_document(output.read_text(encoding="utf-8"))
        actual = [item["chapter"] for item in parsed]
        if actual != block.get("chapters", []):
            errors.append(f"{output.name} chapter sequence {actual} != {block.get('chapters', [])}")
        prose_chapters.extend(parsed)

    if require_prose:
        actual_generated = [item["chapter"] for item in prose_chapters]
        if actual_generated != generated:
            errors.append(f"generated prose chapters {actual_generated} != authorized {generated}")
        lower, upper = contract.get("quality_contract", {}).get("chapter_character_range", [0, 10**9])
        for item in prose_chapters:
            if not lower <= item["character_count"] <= upper:
                errors.append(f"chapter {item['chapter']} character_count {item['character_count']} outside {lower}-{upper}")

    return {
        "valid": not errors,
        "project_id": project_id,
        "mission_id": contract.get("mission_id"),
        "status": contract.get("status"),
        "review_verdict": review_verdict or None,
        "covered_chapters": covered,
        "generated_chapters": generated,
        "tracked_state_keys": list(contract.get("state_tracks", {}).keys()),
        "prose_chapters": prose_chapters,
        "errors": errors,
        "warnings": [],
        "authorization": {"continuous_prose_authorized": False, "publish_authorized": False},
    }
