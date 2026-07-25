from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from nrl_hermes_bridge import ask_hermes
from nrl_paths import runtime_path


DECISION_TYPE = "authorize_controlled_prose_test"
DECISION_SCOPE = "generate_controlled_prose_test"
MISSION_ID = "phase2g_controlled_prose_test"
FORBIDDEN_READER_TERMS = ("schema", "ledger", "database", "metric", "transaction", "audit")
REQUIRED_ANCHOR_GROUPS = (
    ("母亲", "寿债"),
    ("泥灯巷", "街坊"),
    ("灰", "命火"),
    ("白发", "裂", "咳", "冷灰"),
)
FINAL_ASSET_PATH = runtime_path("system/agent_ops/inbox/hermes-final-asset-bundle-v015.json")
AUDIT_PATH = runtime_path("system/agent_ops/inbox/antigravity-final-assets-audit-v016.md")
BIBLE_PATH = runtime_path("phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md")
PLANNING_PATH = runtime_path("phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md")
OUTPUT_PATH = runtime_path("system/agent_ops/inbox/hermes-controlled-prose-test-v016.md")


def latest_controlled_prose_decision(
    decisions: list[dict[str, Any]],
) -> dict[str, Any] | None:
    for decision in reversed(decisions):
        if decision.get("decision_type") != DECISION_TYPE:
            continue
        if DECISION_SCOPE not in set(decision.get("authorized_scope", [])):
            continue
        if decision.get("expires_after_mission") != MISSION_ID:
            continue
        return decision
    return None


def _audit_verdict(audit_text: str) -> str | None:
    match = re.search(r"## Verdict\s*\n\s*(ACCEPT(?:_WITH_WARNINGS)?|REWORK_REQUIRED)", audit_text)
    return match.group(1) if match else None


def build_controlled_prose_readiness(
    decisions: list[dict[str, Any]], audit_text: str
) -> dict[str, Any]:
    decision = latest_controlled_prose_decision(decisions)
    verdict = _audit_verdict(audit_text)
    accepted = verdict in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
    allowed = bool(decision and accepted)
    return {
        "status": "ready_for_controlled_prose_test" if allowed else "blocked_controlled_prose_test",
        "allowed": allowed,
        "owner_decision_id": decision.get("decision_id") if decision else None,
        "antigravity_verdict": verdict,
        "content_production_allowed": False,
        "forbidden_actions": ["generate_full_chapter", "generate_serial_prose", "publish_prose"],
    }


def _approved_context_excerpt(path: Path, limit: int) -> str:
    text = path.read_text(encoding="utf-8")
    if "novel_training_set/" in text:
        raise RuntimeError(f"approved context contains raw corpus path: {path}")
    return text[:limit]


def build_controlled_prose_prompt() -> str:
    final_assets = _approved_context_excerpt(FINAL_ASSET_PATH, 24000)
    audit = _approved_context_excerpt(AUDIT_PATH, 6000)
    bible = _approved_context_excerpt(BIBLE_PATH, 12000)
    planning = _approved_context_excerpt(PLANNING_PATH, 8000)
    return f"""你是 Novel Research Lab 的受控中文玄幻写作 Agent。只生成一段独立的开场场景测试，不是章节，不加标题，不解释过程，也不写任何文件。输出仅为最终中文正文。

硬性范围：800 至 1400 个中文字符；必须出现陆沉渊、母亲或寿债、泥灯巷或街坊、灰或命火，以及白发/裂/咳/冷灰之一。必须将代价写成可见肉身或共同体后果。不得出现 schema、ledger、database、metric、transaction、audit 等技术词，也不得出现章节标题、项目说明、训练语料或来源作品内容。

Antigravity 独立审查结论与限制：
{audit}

已晋升的最终创作资产：
{final_assets}

Story Bible 摘要上下文：
{bible}

Phase 2E 节奏约束：
{planning}
"""


def validate_controlled_prose_text(text: str) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    chinese_character_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    if not 800 <= chinese_character_count <= 1400:
        errors.append(
            {
                "code": "character_count",
                "message": "controlled prose test must contain 800-1400 Chinese characters",
            }
        )
    if re.search(r"(?m)^\s*#|第.{0,8}章", text):
        errors.append({"code": "chapter_boundary", "message": "chapter headings are forbidden"})
    jargon_hits = [term for term in FORBIDDEN_READER_TERMS if term.casefold() in text.casefold()]
    if jargon_hits:
        errors.append(
            {
                "code": "reader_facing_jargon",
                "message": "reader-facing schema or audit jargon is forbidden",
                "terms": jargon_hits,
            }
        )
    if "novel_training_set/" in text:
        errors.append({"code": "raw_corpus_boundary", "message": "raw corpus paths are forbidden"})
    missing_groups = [list(group) for group in REQUIRED_ANCHOR_GROUPS if not any(term in text for term in group)]
    if missing_groups:
        errors.append(
            {
                "code": "missing_story_anchor",
                "message": "controlled prose test is missing required story anchors",
                "missing_groups": missing_groups,
            }
        )
    return {
        "valid": not errors,
        "errors": errors,
        "chinese_character_count": chinese_character_count,
        "content_production_allowed": False,
    }


def dispatch_controlled_prose_test(
    prompt: str,
    decisions: list[dict[str, Any]],
    audit_text: str,
    output_path: Path,
    *,
    invoke=ask_hermes,
) -> dict[str, Any]:
    readiness = build_controlled_prose_readiness(decisions, audit_text)
    if not readiness["allowed"]:
        return {
            "valid": False,
            "errors": [
                {
                    "code": "controlled_prose_gate",
                    "message": "Owner decision and accepted Antigravity audit are required",
                }
            ],
            "readiness": readiness,
            "content_production_allowed": False,
        }
    text = invoke(prompt)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    validation = validate_controlled_prose_text(text)
    return {
        **validation,
        "readiness": readiness,
        "output_path": str(output_path),
        "content_production_allowed": False,
    }
