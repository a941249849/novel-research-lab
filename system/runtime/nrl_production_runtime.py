from __future__ import annotations

import hashlib
import json
import re
import shutil
import statistics
import subprocess
import math
import unicodedata
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from nrl_creation_schemas import validate_creation_asset_store
from nrl_antigravity_bridge import build_antigravity_bridge_status
from nrl_deep_read import build_deep_read_status
from nrl_codex_writer import (
    ask_antigravity_writer,
    ask_codex_structured,
    ask_codex_writer,
    codex_usage_limited,
    extract_json_object,
    find_codex_binary,
)
from nrl_model_router import route_model, validate_model_team_contract
from nrl_production_calibration import build_direct_writer_calibration_status, build_model_team_attestation_status
from nrl_owner_gate import load_decisions
from nrl_paths import ROOT, runtime_path
from nrl_projects import active_project, active_project_id, active_project_scope, active_project_title
from nrl_project_production import (
    project_workspace,
    resolve_independent_review_binding,
    validate_project_production,
    volume1_chapter_count,
    volume1_windows,
)
from nrl_volume1_plan import build_volume1_dry_run
from nrl_volume1_longform import build_volume1_manifest as build_longform_volume1_manifest, validate_volume1_manifest as validate_longform_volume1_manifest
from nrl_volume1_release import prior_window_review_required
from nrl_story_window import story_beat_for
from nrl_longform_plan import ACTIVE_BLUEPRINT_PATH, build_longform_first100_dry_run, build_longform_readiness
from nrl_literary_semantics import validate_project_semantic_contracts


VERSION = "0.23"
CONTEXT_PACKET_VERSION = "0.23"
MIN_CHAPTER_CHINESE_CHARS = 3000
MAX_CHAPTER_CHINESE_CHARS = 4200
MAX_WRITER_PROMPT_BYTES = 40000
STAGES = (
    "chapter_intent",
    "context_compiled",
    "draft_generated",
    "continuity_audited",
    "revision_generated",
    "final_observed",
    "final_audited",
    "state_settled",
    "chapter_accepted",
)
REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")
QUARANTINE_ROOT = runtime_path("system/production_runtime/quarantine")
PRODUCTION_BLUEPRINT_PATH = runtime_path("docs/production/borrowed-heaven-production-blueprint-v0.1.md")
PROJECT_RECONCILIATION_VALIDATION = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json"
)
PROJECT_RECONCILIATION_APPLICATION = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_application_v0.19.json"
)
CANONICAL_BASELINE_PATH = runtime_path(
    "system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.22.json"
)
CANONICAL_INPUTS = (
    "phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md",
    "phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md",
    "system/creation_assets/project_assets.v0.2.json",
)
RUNTIME_SCHEMAS = (
    "system/production_runtime/schemas/chapter_intent.schema.json",
    "system/production_runtime/schemas/chapter_observation.schema.json",
    "system/production_runtime/schemas/chapter_generation.schema.json",
    "system/production_runtime/schemas/chapter_settlement.schema.json",
    "system/production_runtime/schemas/chapter_registry.schema.json",
    "system/production_runtime/schemas/continuity_audit.schema.json",
)
TRANSITION_WORDS = (
    "然而", "此外", "与此同时", "因此", "于是", "不过", "随即", "紧接着", "更重要的是",
)
RHETORICAL_PATTERNS = (
    re.compile(r"不是因为.{0,40}而是因为"),
    re.compile(r"不(?:仅|只)是.{0,40}(?:更|而且|还)是"),
    re.compile(r"这一刻.{0,30}(?:终于|才)"),
    re.compile(r"他知道.{0,50}(?:意味着|明白)"),
)
ABSTRACT_WORDS = ("命运", "意义", "本质", "信念", "责任", "选择", "希望", "绝望", "力量")
SENSORY_WORDS = ("冷", "热", "痛", "血", "灰", "火", "光", "声", "气味", "手", "眼", "骨", "皮")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_role_execution(
    chapter_id: str,
    role: str,
    artifact_path: Path,
    *,
    provider: str,
    model: str,
    bindings: dict[str, Any] | None = None,
) -> str:
    target = runtime_path(
        f"system/production_runtime/chapters/{chapter_id}/{role}.execution.json"
    )
    payload = {
        "version": "0.28",
        "chapter_id": chapter_id,
        "role": role,
        "artifact": str(artifact_path.relative_to(ROOT)),
        "artifact_sha256": _sha256(artifact_path),
        "provider": provider,
        "model": model,
        **(bindings or {}),
    }
    _write_json(target, payload)
    return str(target.relative_to(ROOT))


def validate_role_execution(
    record: dict[str, Any], role: str, artifact_path: Path
) -> dict[str, Any]:
    errors: list[str] = []
    execution_ref = record.get("artifacts", {}).get(f"{role}_execution", "")
    execution_path = runtime_path(execution_ref)
    if not execution_path.is_file():
        return {"valid": False, "errors": [f"missing {role} execution evidence"]}
    execution = _read_json(execution_path)
    expected_models = {
        "writer": "gpt-5.6-terra",
        "observer": "gpt-5.6-luna",
        "reviewer": "gpt-5.6-sol",
    }
    if execution.get("chapter_id") != record.get("chapter_id"):
        errors.append(f"{role} execution chapter mismatch")
    if execution.get("role") != role:
        errors.append(f"{role} execution role mismatch")
    if execution.get("artifact") != str(artifact_path.relative_to(ROOT)):
        errors.append(f"{role} execution artifact path mismatch")
    if execution.get("artifact_sha256") != _sha256(artifact_path):
        errors.append(f"{role} execution artifact hash mismatch")
    if active_project_id() != "borrowed-heaven" and (
        execution.get("provider") != "codex"
        or execution.get("model") != expected_models[role]
    ):
        errors.append(f"{role} execution must use Codex {expected_models[role]}")
    if role == "observer":
        revision = runtime_path(record.get("artifacts", {}).get("revision", ""))
        if not revision.is_file() or execution.get("revision_sha256") != _sha256(revision):
            errors.append("observer execution revision hash mismatch")
    if role == "reviewer":
        audit = _read_json(artifact_path)
        revision = runtime_path(record.get("artifacts", {}).get("revision", ""))
        if execution.get("audit_artifact_sha256") != _sha256(artifact_path):
            errors.append("reviewer execution audit hash mismatch")
        if not revision.is_file() or execution.get("revision_sha256") != _sha256(revision):
            errors.append("reviewer execution revision hash mismatch")
        if audit.get("artifact_sha256") != execution.get("revision_sha256"):
            errors.append("reviewer execution is not bound to audited revision")
    return {"valid": not errors, "errors": errors, "execution": execution}


def validate_stage_transition(
    record: dict[str, Any], target_stage: str, artifact_path: str
) -> dict[str, Any]:
    errors = []
    current = str(record.get("stage", ""))
    if current == STAGES[-1]:
        errors.append("accepted chapter is immutable")
    elif current not in STAGES:
        errors.append("current stage is invalid")
    else:
        expected_index = STAGES.index(current) + 1
        if expected_index >= len(STAGES) or target_stage != STAGES[expected_index]:
            errors.append("target stage must be the exact next stage")
    if not artifact_path:
        errors.append("transition artifact path is required")
    return {"valid": not errors, "errors": errors, "current_stage": current, "target_stage": target_stage}


def validate_settlement_payload(
    settlement: dict[str, Any],
    chapter_id: str,
    revision_sha256: str,
    audit: dict[str, Any],
    observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    errors = []
    if audit.get("verdict") == "REWORK_REQUIRED":
        errors.append("REWORK_REQUIRED audit must be replaced by an accepted revision audit")
    if settlement.get("chapter_id") != chapter_id:
        errors.append("settlement chapter_id mismatch")
    if settlement.get("accepted_revision_sha256") != revision_sha256:
        errors.append("settlement is stale or bound to another revision")
    resolved = set(settlement.get("resolved_audit_ids", []))
    blocking = {
        str(issue.get("issue_id"))
        for issue in audit.get("issues", [])
        if issue.get("severity") in {"blocking", "major"}
    }
    missing = sorted(blocking - resolved)
    if missing:
        errors.append(f"unresolved blocking audit issues: {', '.join(missing)}")
    if observation is not None:
        observed = {}
        for facts in observation.get("facts", {}).values():
            if isinstance(facts, list):
                for fact in facts:
                    if isinstance(fact, dict) and fact.get("fact_id"):
                        observed[str(fact["fact_id"])] = fact
        settlement_keys: set[tuple[str, str]] = set()
        for delta in settlement.get("state_deltas", []):
            key = (str(delta.get("asset_id")), str(delta.get("field_path")))
            if key in settlement_keys:
                errors.append(
                    f"duplicate settlement state key: {key[0]}:{key[1]}"
                )
            settlement_keys.add(key)
            fact = observed.get(str(delta.get("fact_id")))
            comparable = ("asset_id", "field_path", "before", "after")
            if not fact or any(delta.get(key) != fact.get(key) for key in comparable):
                errors.append(f"state delta does not match observed fact: {delta.get('fact_id')}")
    if active_project_id() != "borrowed-heaven":
        workspace = project_workspace()
        store_path = workspace / "creation_assets/project_assets.json"
        initial_path = workspace / "production_runtime/state/canonical_initial_state.v1.json"
        assets = {
            str(item.get("asset_id")): item
            for item in _read_json(store_path).get("assets", [])
            if item.get("asset_id")
        }
        current = {
            (str(item.get("asset_id")), str(item.get("field_path"))): item.get("value")
            for item in _read_json(initial_path).get("fields", [])
            if item.get("asset_id") and item.get("field_path")
        } if initial_path.is_file() else {}
        registry = _load_registry()
        ordinal = int(chapter_id.removeprefix("chapter-"))
        for record in registry.get("chapters", []):
            if int(str(record.get("chapter_id", "chapter-0000"))[-4:]) >= ordinal:
                continue
            settlement_path = record.get("artifacts", {}).get("settlement")
            if settlement_path and record.get("stage") == "chapter_accepted":
                for delta in _read_json(runtime_path(settlement_path)).get("state_deltas", []):
                    current[(str(delta.get("asset_id")), str(delta.get("field_path")))] = delta.get("after")
        allowed_fields = {key for key in current}
        expected: dict[tuple[str, str], dict[str, Any]] = {}
        chapter_record = next(
            (item for item in registry.get("chapters", []) if item.get("chapter_id") == chapter_id),
            None,
        )
        if chapter_record and chapter_record.get("artifacts", {}).get("intent"):
            intent = _read_json(runtime_path(chapter_record["artifacts"]["intent"]))
            expected = {
                (str(item.get("asset_id")), str(item.get("field_path"))): item
                for item in intent.get("expected_state_deltas", [])
            }
        for delta in settlement.get("state_deltas", []):
            asset_id = str(delta.get("asset_id", ""))
            field_path = str(delta.get("field_path", ""))
            key = (asset_id, field_path)
            if asset_id not in assets:
                errors.append(f"unknown settlement asset: {asset_id}")
                continue
            if key not in allowed_fields:
                errors.append(f"unregistered settlement field: {asset_id}:{field_path}")
                continue
            contract = expected.get(key)
            if not contract:
                errors.append(f"state delta is not declared by chapter intent: {asset_id}:{field_path}")
                continue
            if delta.get("before") != current.get(key):
                errors.append(f"stale settlement before value: {asset_id}:{field_path}")
            if contract.get("before") != current.get(key) or delta.get("after") != contract.get("after"):
                errors.append(f"state delta violates frozen intent: {asset_id}:{field_path}")
            if delta.get("after") == current.get(key):
                errors.append(f"state delta repeats the current value: {asset_id}:{field_path}")
            if field_path == "lifecycle_state":
                before, after = delta.get("before"), delta.get("after")
                allowed = (before, after) == (contract.get("before"), contract.get("after"))
                if not allowed:
                    errors.append(f"illegal lifecycle transition: {asset_id}:{before}->{after}")
                if asset_id == "faction_maintenance_team" and after == "active" and chapter_id != "chapter-0033":
                    errors.append("maintenance team may become active only in chapter-0033")
        observed_keys = {
            (str(item.get("asset_id", "")), str(item.get("field_path", "")))
            for item in settlement.get("state_deltas", [])
        }
        for asset_id, field_path in sorted(set(expected) - observed_keys):
            errors.append(f"missing frozen intent state delta: {asset_id}:{field_path}")
    return {"valid": not errors, "errors": errors}


def validate_acceptance(
    record: dict[str, Any], settlement: dict[str, Any], revision_sha256: str
) -> dict[str, Any]:
    errors = []
    if record.get("stage") != "state_settled":
        errors.append("chapter must be state_settled before acceptance")
    if not record.get("artifacts", {}).get("revision") or not record.get("artifacts", {}).get("settlement"):
        errors.append("revision and settlement artifacts are required")
    if settlement.get("accepted_revision_sha256") != revision_sha256:
        errors.append("settlement is stale or bound to another revision")
    return {"valid": not errors, "errors": errors}


def validate_chapter_sequence(chapters: list[dict[str, Any]], chapter_id: str) -> dict[str, Any]:
    errors = []
    try:
        ordinal = int(chapter_id.removeprefix("chapter-"))
    except ValueError:
        return {"valid": False, "errors": ["chapter_id has invalid ordinal"]}
    if ordinal == 1:
        if chapters:
            errors.append("chapter-0001 requires an empty registry")
    else:
        predecessor_id = f"chapter-{ordinal - 1:04d}"
        predecessor = next((item for item in chapters if item.get("chapter_id") == predecessor_id), None)
        if not predecessor or predecessor.get("stage") != "chapter_accepted":
            errors.append(f"immediate predecessor must be accepted: {predecessor_id}")
        if any(int(str(item.get("chapter_id", "chapter-0000")).removeprefix("chapter-")) >= ordinal for item in chapters):
            errors.append("chapter initialization must be strictly sequential")
    return {"valid": not errors, "errors": errors}


def analyze_prose_metrics(text: str) -> dict[str, Any]:
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    sentences = [item.strip() for item in re.split(r"[。！？!?]", text) if item.strip()]
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    sentence_lengths = [len(re.findall(r"[\u4e00-\u9fff]", item)) for item in sentences]
    paragraph_lengths = [len(re.findall(r"[\u4e00-\u9fff]", item)) for item in paragraphs]
    normalized_text = re.sub(r"\s+", "", text)
    repeated_span = None
    seen_spans: dict[str, int] = {}
    for index in range(max(0, len(normalized_text) - 119)):
        span = normalized_text[index:index + 120]
        previous = seen_spans.get(span)
        if previous is not None and index - previous >= 120:
            repeated_span = span[:40]
            break
        seen_spans.setdefault(span, index)
    tail_paragraphs = paragraphs[-30:]
    tail_lengths = [len(re.findall(r"[\u4e00-\u9fff]", item)) for item in tail_paragraphs]
    tail_short_ratio = (
        sum(length <= 20 for length in tail_lengths) / len(tail_lengths)
        if tail_lengths else 0
    )
    tail_dialogue_ratio = (
        sum(item.lstrip().startswith(("“", '"')) for item in tail_paragraphs)
        / len(tail_paragraphs)
        if tail_paragraphs else 0
    )
    starters = []
    for sentence in sentences:
        han = re.findall(r"[\u4e00-\u9fff]", sentence)
        if len(han) >= 3:
            starters.append("".join(han[:3]))
    starter_counts = Counter(starters)
    starter_threshold = max(4, math.ceil(len(starters) * 0.08))
    repeated_starters = [
        {"starter": starter, "count": count}
        for starter, count in starter_counts.most_common()
        if count >= starter_threshold
    ]
    transition_hits = sum(text.count(word) for word in TRANSITION_WORDS)
    rhetorical_hits = sum(len(pattern.findall(text)) for pattern in RHETORICAL_PATTERNS)
    abstract_hits = sum(text.count(word) for word in ABSTRACT_WORDS)
    sensory_hits = sum(text.count(word) for word in SENSORY_WORDS)
    quote_chars = sum(len(match) for match in re.findall(r"[“\"](.*?)[”\"]", text, re.DOTALL))
    count = len(chinese_chars)
    prompt_leak_markers = [
        marker for marker in (
            '"contract_path"', '"scene_constraints"', '"must_keep"',
            '"required_asset_ids"', '"canonical_baseline"', '"writer_asset_ids"',
        )
        if marker in text
    ]
    generation_meta_markers = [
        marker for marker in (
            "源代码提交确认", "测试通过", "最终状态已更新", "所有规则符合",
            "正文结束", "停止生成", "字数完成", "请继续下一章", "凑字数",
            "以上都不算正文", "请忽略", "工程元数据", "测试测试测试",
        )
        if marker in text
    ]
    latin_token_markers = re.findall(r"(?<![A-Za-z])[A-Za-z]{2,}(?![A-Za-z])", text)
    termination_word_hits = sum(text.count(marker) for marker in ("结束", "停止", "收束", "完。", "终。"))
    flags = []
    if transition_hits >= max(3, len(paragraphs) // 2):
        flags.append("transition_word_repetition")
    if rhetorical_hits >= 3:
        flags.append("rhetorical_template_repetition")
    if repeated_starters:
        flags.append("sentence_opening_repetition")
    if abstract_hits > sensory_hits * 2 and abstract_hits >= 6:
        flags.append("abstract_exposition_density")
    if text.count("——") > max(3, count // 500):
        flags.append("dash_overuse")
    if (
        len(tail_paragraphs) >= 20
        and tail_short_ratio >= 0.7
        and statistics.mean(tail_lengths) <= 28
        and tail_dialogue_ratio < 0.35
    ):
        flags.append("tail_fragmentation_loop")
    if prompt_leak_markers:
        flags.append("prompt_context_leak")
    if generation_meta_markers:
        flags.append("generation_meta_leak")
    if latin_token_markers:
        flags.append("latin_token_leak")
    if termination_word_hits >= 10:
        flags.append("termination_token_loop")
    if paragraph_lengths and max(paragraph_lengths) > 500:
        flags.append("oversized_paragraph_loop")
    if repeated_span:
        flags.append("duplicate_text_span")
    return {
        "chinese_character_count": count,
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "average_sentence_length": round(statistics.mean(sentence_lengths), 2) if sentence_lengths else 0,
        "sentence_length_stddev": round(statistics.pstdev(sentence_lengths), 2) if sentence_lengths else 0,
        "average_paragraph_length": round(statistics.mean(paragraph_lengths), 2) if paragraph_lengths else 0,
        "paragraph_length_stddev": round(statistics.pstdev(paragraph_lengths), 2) if paragraph_lengths else 0,
        "dialogue_ratio": round(quote_chars / count, 4) if count else 0,
        "transition_word_hits": transition_hits,
        "rhetorical_template_hits": rhetorical_hits,
        "abstract_word_hits": abstract_hits,
        "sensory_word_hits": sensory_hits,
        "repeated_sentence_starters": repeated_starters,
        "tail_short_paragraph_ratio": round(tail_short_ratio, 4),
        "tail_dialogue_paragraph_ratio": round(tail_dialogue_ratio, 4),
        "prompt_leak_markers": prompt_leak_markers,
        "generation_meta_markers": generation_meta_markers,
        "latin_token_markers": latin_token_markers,
        "termination_word_hits": termination_word_hits,
        "max_paragraph_length": max(paragraph_lengths) if paragraph_lengths else 0,
        "repeated_text_span_preview": repeated_span,
        "flags": flags,
        "policy": "metrics_are_audit_evidence_not_a_literary_verdict",
    }


def compile_chapter_context_payload(
    intent: dict[str, Any],
    assets: list[dict[str, Any]],
    canonical_hashes: dict[str, str],
    prior_settlements: list[dict[str, Any]],
    canonical_baseline: dict[str, str] | None = None,
    story_beat: dict[str, Any] | None = None,
    initial_state: dict[str, Any] | None = None,
    literary_semantic_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if active_project_id() != "borrowed-heaven" and not literary_semantic_contract:
        return {
            "valid": False,
            "errors": ["project chapter context requires a literary semantic contract"],
        }
    asset_map = {
        str(asset.get("asset_id")): asset
        for asset in assets
        if isinstance(asset, dict) and asset.get("asset_id")
    }
    legacy_requested = [str(item) for item in intent.get("required_asset_ids", [])]
    if story_beat and story_beat.get("required_asset_ids"):
        requested = [str(item) for item in story_beat.get("required_asset_ids", [])]
        requested.extend(str(item) for item in intent.get("active_hook_ids", []))
        requested = list(dict.fromkeys(requested))
    else:
        requested = legacy_requested
    missing = [asset_id for asset_id in requested if asset_id not in asset_map]
    if missing:
        return {"valid": False, "errors": [f"missing required assets: {', '.join(missing)}"]}

    selected_ids = list(requested)
    selected_set = set(selected_ids)
    dependency_ids = []
    cursor = 0
    while cursor < len(selected_ids):
        asset = asset_map[selected_ids[cursor]]
        cursor += 1
        for relationship in asset.get("relationships", []):
            if not str(relationship.get("relation_type", "")).startswith("atomic_transaction_peer"):
                continue
            target_id = str(relationship.get("target_id", ""))
            if target_id not in asset_map:
                return {
                    "valid": False,
                    "errors": [f"missing atomic transaction peer: {target_id}"],
                }
            if target_id not in selected_set:
                selected_ids.append(target_id)
                selected_set.add(target_id)
                dependency_ids.append(target_id)

    selected = [asset_map[asset_id] for asset_id in selected_ids]
    baseline_metadata = dict(canonical_baseline or {})
    packet_version = baseline_metadata.get("version", CONTEXT_PACKET_VERSION)
    rolling_state = build_rolling_state_snapshot(prior_settlements, initial_state=initial_state)
    context = {
        "version": packet_version,
        "chapter_id": intent.get("chapter_id"),
        "dramatic_purpose": intent.get("dramatic_purpose"),
        "must_keep": list(intent.get("must_keep", [])),
        "must_avoid": list(intent.get("must_avoid", [])),
        "scene_constraints": list(intent.get("scene_constraints", [])),
        "active_hook_ids": list(intent.get("active_hook_ids", [])),
        "expected_state_deltas": list(intent.get("expected_state_deltas", [])),
        "assets": selected,
        "writer_asset_ids": requested,
        "story_beat": story_beat,
        "rolling_state": rolling_state,
        "canonical_hashes": canonical_hashes,
        "canonical_baseline": baseline_metadata,
        "literary_semantic_contract": literary_semantic_contract,
    }
    trace = {
        "version": packet_version,
        "chapter_id": intent.get("chapter_id"),
        "selected_asset_ids": selected_ids,
        "explicit_asset_ids": requested,
        "legacy_intent_asset_count": len(legacy_requested),
        "dependency_asset_ids": dependency_ids,
        "excluded_asset_count": len(asset_map) - len(selected),
        "selection_reason": "explicit chapter intent requirements plus atomic transaction peers",
        "canonical_hashes": canonical_hashes,
        "canonical_baseline": baseline_metadata,
        "prior_settlement_count": len(prior_settlements),
        "rolling_state_field_count": len(rolling_state["latest_fields"]),
        "story_window_contract": story_beat.get("contract_path") if story_beat else None,
        "literary_semantic_sources": (
            literary_semantic_contract.get("source_bindings", [])
            if literary_semantic_contract
            else []
        ),
    }
    rule_stack = {
        "version": packet_version,
        "chapter_id": intent.get("chapter_id"),
        "canonical_baseline": baseline_metadata,
        "priority_order": [
            "safety_and_originality",
            "canonical_story_bible",
            "volume_outline",
            "accepted_state_settlements",
            "creation_asset_constraints",
            "literary_semantic_contract",
            "chapter_must_keep_and_must_avoid",
            "anti_ai_style_evidence",
        ],
        "hard_rules": [
            "no source-work names, scenes, signature systems, or prose imitation",
            "no untracked power, relationship, location, item, or timeline changes",
            "all benefits carry an embodied, relational, or systemic cost",
            "reader-facing prose contains no runtime or database vocabulary",
            *(
                [str(item) for item in literary_semantic_contract.get("enforced_rules", [])]
                if literary_semantic_contract
                else []
            ),
            *[str(item) for item in intent.get("must_avoid", [])],
        ],
        "chapter_rules": [str(item) for item in intent.get("must_keep", [])],
        "scene_constraints": [str(item) for item in intent.get("scene_constraints", [])],
    }
    return {"valid": True, "errors": [], "context": context, "trace": trace, "rule_stack": rule_stack}


def build_chapter_literary_semantic_contract(
    chapter_id: str, canonical_baseline: dict[str, Any]
) -> dict[str, Any] | None:
    """Compile project semantics into chapter-sized, hash-bound writing constraints."""
    if active_project_id() == "borrowed-heaven":
        return None
    project_id = active_project_id()
    validation = validate_project_semantic_contracts(project_id)
    if not validation.get("valid"):
        raise RuntimeError(
            "literary semantic contract is blocked: "
            + "; ".join(validation.get("errors", []))
        )
    workspace = project_workspace(project_id)
    sources = {
        "character_highlights": workspace / "design/character_highlight_matrix.v1.json",
        "world_progression": workspace / "design/world_progression_atlas.v1.json",
        "embedded_history": workspace / "design/embedded_history_engine.v1.json",
        "chapter_semantic_beats": workspace / "production_runtime/plans/volume1_semantic_beat_contract.v1.json",
        "semantic_application": workspace / "validation/literary_semantic_application.v1.json",
    }
    baseline_hashes = {
        str(item.get("path")): str(item.get("sha256"))
        for item in canonical_baseline.get("canonical_inputs", [])
    }
    bindings = []
    for label, path in sources.items():
        relative = str(path.relative_to(ROOT))
        digest = _sha256(path)
        if baseline_hashes.get(relative) != digest:
            raise RuntimeError(f"semantic source is not current in canonical baseline: {relative}")
        bindings.append({"kind": label, "path": relative, "sha256": digest})
    chapter_number = int(chapter_id.removeprefix("chapter-"))
    if not 1 <= chapter_number <= 66:
        raise RuntimeError(f"Volume 1 semantic contract does not cover {chapter_id}")
    highlights = _read_json(sources["character_highlights"])
    atlas = _read_json(sources["world_progression"])
    history = _read_json(sources["embedded_history"])
    beats = _read_json(sources["chapter_semantic_beats"])
    application = _read_json(sources["semantic_application"])
    volume_highlight = next(
        item for item in highlights["volumes"] if item.get("volume") == 1
    )
    volume_atlas = next(item for item in atlas["volumes"] if item.get("volume") == 1)
    history_dossier = next(
        item for item in history["dossiers"] if item.get("volume") == 1
    )
    chapter_beat = next(
        (
            item
            for item in beats["chapters"]
            if item.get("chapter_id") == chapter_id
        ),
        None,
    )
    if not chapter_beat:
        raise RuntimeError(f"missing literary semantic beat for {chapter_id}")
    character_id_by_name = {
        item["name"]: item["character_id"] for item in highlights["characters"]
    }
    pov_character_id = character_id_by_name.get(chapter_beat.get("pov"))
    current_pov_agency = (
        volume_highlight["agency"].get(pov_character_id)
        if pov_character_id
        else None
    )
    return {
        "version": "0.29",
        "project_id": project_id,
        "chapter_id": chapter_id,
        "source_bindings": bindings,
        "chapter_beat": chapter_beat,
        "volume_character_contract": {
            "primary_spotlight": volume_highlight["primary_spotlight"],
            "pov_character_id": pov_character_id,
            "pov_agency": current_pov_agency,
            "signature_highlights": [
                item
                for item in volume_highlight["signature_highlights"]
                if item.get("character_id") == pov_character_id
            ],
        },
        "volume_progression_contract": {
            "progression_rule": atlas["progression_rule"],
            "competency_names": [item["name"] for item in atlas["competencies"]],
            "authority_rank_names": [item["rank"] for item in atlas["authority_ranks"]],
            "volume_scope": volume_atlas,
        },
        "embedded_history_contract": {
            "engine_name": history["engine_name"],
            "narrative_rule": history["narrative_rule"],
            "form_rule": history["form_rule"],
            "dossier": history_dossier,
        },
        "application_summary": {
            "semantic_dimensions_decided": len(application["dimension_decisions"]),
            "source_books_decided": len(
                {
                    item["source_book"]
                    for item in application["signature_dimension_dispositions"]
                }
            ),
            "allowed_operation": "functional transformation only",
        },
        "dimension_contracts": application["dimension_decisions"],
        "protected_function_transforms": [
            {
                "source_dimension": item["source_dimension"],
                "decision": item["decision"],
                "functional_rationale": item["rationale"],
                "originality_transformation": item["originality_transformation"],
            }
            for item in application["signature_decisions"]
            if item["decision"] != "defer"
        ],
        "enforced_rules": [
            "the chapter semantic beat must affect an on-page choice and consequence",
            "the POV character must exercise independent professional agency",
            "progression changes permissions and liability, never grants cost-free dominance",
            "embedded history must alter present judgment or action, never become decorative exposition",
            "source-book material may only survive as transformed narrative function",
        ],
    }


def validate_compiled_literary_semantic_payload(
    context: dict[str, Any],
    rules: dict[str, Any],
    trace: dict[str, Any],
    expected: dict[str, Any],
    chapter_id: str,
    baseline_metadata: dict[str, str],
) -> dict[str, Any]:
    errors: list[str] = []
    if context.get("chapter_id") != chapter_id:
        errors.append("compiled context chapter identity mismatch")
    if context.get("canonical_baseline") != baseline_metadata:
        errors.append("compiled context canonical baseline binding mismatch")
    if context.get("literary_semantic_contract") != expected:
        errors.append("compiled literary semantic contract is stale or mutated")
    if trace.get("literary_semantic_sources") != expected.get("source_bindings"):
        errors.append("compiled semantic trace bindings are stale or mutated")
    if "literary_semantic_contract" not in rules.get("priority_order", []):
        errors.append("literary semantic priority rule is missing")
    hard_rules = set(str(item) for item in rules.get("hard_rules", []))
    required_rules = set(str(item) for item in expected.get("enforced_rules", []))
    if not required_rules <= hard_rules:
        errors.append("compiled literary semantic hard rules are incomplete")
    return {"valid": not errors, "errors": errors}


def validate_compiled_literary_semantic_context(
    record: dict[str, Any], chapter_id: str
) -> dict[str, Any]:
    if active_project_id() == "borrowed-heaven":
        return {"valid": True, "errors": []}
    artifacts = record.get("artifacts", {})
    required = {
        name: runtime_path(artifacts.get(name, ""))
        for name in ("context", "rule_stack", "trace")
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    if missing:
        return {
            "valid": False,
            "errors": ["missing compiled semantic artifacts: " + ", ".join(missing)],
        }
    baseline = _read_json(CANONICAL_BASELINE_PATH)
    baseline_metadata = {
        "path": str(CANONICAL_BASELINE_PATH.relative_to(ROOT)),
        "version": str(baseline["version"]),
        "sha256": _sha256(CANONICAL_BASELINE_PATH),
    }
    expected = build_chapter_literary_semantic_contract(chapter_id, baseline)
    return validate_compiled_literary_semantic_payload(
        _read_json(required["context"]),
        _read_json(required["rule_stack"]),
        _read_json(required["trace"]),
        expected,
        chapter_id,
        baseline_metadata,
    )


def build_rolling_state_snapshot(
    settlements: list[dict[str, Any]], recent_limit: int = 2,
    initial_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Reduce immutable history to current fields plus a short causal tail."""
    latest: dict[str, dict[str, Any]] = {}
    for field in (initial_state or {}).get("fields", []):
        if not isinstance(field, dict):
            continue
        asset_id = str(field.get("asset_id", ""))
        field_path = str(field.get("field_path", ""))
        if asset_id and field_path:
            latest[f"{asset_id}:{field_path}"] = {
                "asset_id": asset_id,
                "field_path": field_path,
                "value": field.get("value"),
                "chapter_id": "canonical-initial-state",
                "evidence": field.get("source"),
            }
    for settlement in settlements:
        chapter_id = str(settlement.get("chapter_id", "unknown"))
        for delta in settlement.get("state_deltas", []):
            if not isinstance(delta, dict):
                continue
            asset_id = str(delta.get("asset_id", ""))
            field_path = str(delta.get("field_path", ""))
            if not asset_id or not field_path:
                continue
            latest[f"{asset_id}:{field_path}"] = {
                "asset_id": asset_id,
                "field_path": field_path,
                "value": delta.get("after"),
                "chapter_id": chapter_id,
                "evidence": delta.get("evidence"),
            }
    recent = []
    for settlement in settlements[-recent_limit:]:
        recent.append({
            "chapter_id": settlement.get("chapter_id"),
            "accepted_revision_sha256": settlement.get("accepted_revision_sha256"),
            "changes": [
                {
                    "asset_id": item.get("asset_id"),
                    "field_path": item.get("field_path"),
                    "after": item.get("after"),
                }
                for item in settlement.get("state_deltas", [])
                if isinstance(item, dict)
            ],
        })
    return {
        "source_chapter_count": len(settlements),
        "latest_fields": [latest[key] for key in sorted(latest)],
        "recent_chapters": recent,
    }


def validate_context_compile_stage(
    record: dict[str, Any], chapter_dir: Path
) -> dict[str, Any]:
    if record.get("stage") == "context_compiled":
        has_draft_artifact = bool(record.get("artifacts", {}).get("draft"))
        has_draft_file = (chapter_dir / "draft.md").exists()
        errors = []
        if has_draft_artifact or has_draft_file:
            errors.append("context cannot be recompiled after a draft exists")
        return {"valid": not errors, "errors": errors, "recompile": True}
    transition = validate_stage_transition(record, "context_compiled", "context.json")
    return {**transition, "recompile": False}


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _load_registry() -> dict[str, Any]:
    return _read_json(REGISTRY_PATH) if REGISTRY_PATH.exists() else {
        "version": "0.20",
        "project_id": active_project_id(),
        "project": active_project_title(),
        "chapters": [],
    }


def _save_registry(registry: dict[str, Any]) -> None:
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_registry.schema.json"))
    jsonschema.validate(registry, schema)
    _write_json(REGISTRY_PATH, registry)


def quarantine_unaccepted_chapter(chapter_id: str, reason: str) -> dict[str, Any]:
    """Remove an unaccepted test sample from the active sequence without deleting it."""
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] == "chapter_accepted":
        raise RuntimeError("accepted chapters cannot be quarantined")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    source_dir = runtime_path(f"system/production_runtime/chapters/{chapter_id}")
    target_dir = QUARANTINE_ROOT / f"{chapter_id}-{stamp}"
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if source_dir.exists():
        shutil.move(str(source_dir), str(target_dir))
    manifest = {"chapter_id": chapter_id, "prior_stage": record["stage"], "reason": reason, "quarantined_at": stamp, "source_hashes": record["source_hashes"]}
    _write_json(target_dir / "quarantine_manifest.json", manifest)
    registry["chapters"] = [item for item in registry["chapters"] if item["chapter_id"] != chapter_id]
    _save_registry(registry)
    return {"chapter_id": chapter_id, "quarantine_path": str(target_dir.relative_to(ROOT)), "reason": reason}


def build_production_preflight(
    adapters: dict[str, Any], allowed_pending_chapter_id: str | None = None
) -> dict[str, Any]:
    registry = _load_registry()
    readiness = build_production_readiness(allowed_pending_chapter_id)
    pending = [item["chapter_id"] for item in registry["chapters"] if item["stage"] != "chapter_accepted"]
    blocking_pending = [item for item in pending if item != allowed_pending_chapter_id]
    project = active_project()
    authorized_scopes = {
        active_project_scope(),
        f"{active_project_id()}-production-blueprint-v01",
    }
    if active_project_id() == "borrowed-heaven":
        authorized_scopes.add("borrowed-heaven-production-blueprint-v01")
    blueprint_accepted = bool(project.get("content_authorized")) and any(
        item.get("decision_type") == "accept_review"
        and authorized_scopes.intersection(item.get("authorized_scope", []))
        for item in load_decisions()
    )
    longform_active = ACTIVE_BLUEPRINT_PATH.exists()
    legacy_volume1_dry_run = build_volume1_dry_run()
    longform_volume1_manifest = (
        validate_longform_volume1_manifest(build_longform_volume1_manifest())
        if longform_active
        else None
    )
    longform_readiness = build_longform_readiness() if longform_active else None
    longform_dry_run = build_longform_first100_dry_run() if longform_active else None
    calibration = build_direct_writer_calibration_status()
    model_team_attestation = build_model_team_attestation_status()
    model_team = validate_model_team_contract()
    antigravity = adapters.get("antigravity", {})
    if active_project_id() != "borrowed-heaven":
        checks = {
            "project_production_contract_valid": readiness["checks"].get("project_production_contract_valid", False),
            "canonical_runtime_ready": readiness["ready"],
            "bounded_owner_authorization_current": readiness["checks"].get("bounded_prose_authorized", False),
            "no_unaccepted_chapters": not blocking_pending,
            "creation_assets_valid": validate_creation_asset_store()["valid"],
            "codex_direct_writer_available": bool(adapters.get("codex", {}).get("can_execute")) and bool(find_codex_binary()),
            "antigravity_backup_configured": antigravity.get("execution_policy") == "independent_review_and_provider_fallback_only",
        }
        return {
            "valid": all(checks.values()),
            "project_id": active_project_id(),
            "checks": checks,
            "project_production": validate_project_production(),
            "legacy_volume1_dry_run": {"deprecated": True, "reason": "project-isolated production contract is active"},
            "pending_chapters": pending,
            "allowed_pending_chapter_id": allowed_pending_chapter_id,
            "accepted_chapters": [item["chapter_id"] for item in registry["chapters"] if item["stage"] == "chapter_accepted"],
        }
    checks = {
        "canonical_runtime_ready": readiness["ready"],
        "codex_model_team_contract_valid": model_team["valid"],
        "codex_model_team_attestation_valid": model_team_attestation["valid"],
        "no_unaccepted_chapters": not blocking_pending,
        "creation_assets_valid": validate_creation_asset_store()["valid"],
        "codex_direct_writer_available": bool(adapters.get("codex", {}).get("can_execute")) and bool(find_codex_binary()),
        "antigravity_backup_configured": (
            antigravity.get("execution_policy")
            == "independent_review_and_provider_fallback_only"
        ),
    }
    if longform_active:
        checks.update({
            "active_longform_blueprint_ready": bool(longform_readiness and longform_readiness["valid"]),
            "longform_first100_non_prose_dry_run_valid": bool(longform_dry_run and longform_dry_run["valid"]),
            "longform_volume1_intents_valid": bool(longform_volume1_manifest and longform_volume1_manifest["valid"]),
        })
    else:
        checks.update({
            "production_blueprint_present": PRODUCTION_BLUEPRINT_PATH.exists(),
            "production_blueprint_owner_accepted": blueprint_accepted,
            "volume1_non_prose_dry_run_valid": legacy_volume1_dry_run["valid"],
        })
    return {"valid": all(checks.values()), "checks": checks, "legacy_volume1_dry_run": legacy_volume1_dry_run if not longform_active else {"deprecated": True, "reason": "The active 6M-character route uses the 100-chapter Volume 1 contract."}, "longform_volume1_manifest": longform_volume1_manifest if longform_active else None, "longform_readiness": longform_readiness, "longform_dry_run": longform_dry_run, "codex_model_team": model_team, "model_team_attestation": model_team_attestation, "legacy_direct_codex_calibration": calibration, "antigravity_runtime_available": build_antigravity_bridge_status()["available"], "pending_chapters": pending, "allowed_pending_chapter_id": allowed_pending_chapter_id, "accepted_chapters": [item["chapter_id"] for item in registry["chapters"] if item["stage"] == "chapter_accepted"]}


def initialize_chapter(intent_file: str) -> dict[str, Any]:
    source = Path(intent_file)
    if not source.is_absolute():
        source = ROOT / source
    intent = _read_json(source)
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_intent.schema.json"))
    jsonschema.validate(intent, schema)
    chapter_id = str(intent["chapter_id"])
    if not has_bounded_intent_authorization(load_decisions(), chapter_id):
        raise RuntimeError(f"bounded chapter intent gate is blocked for {chapter_id}")
    readiness = build_production_readiness(chapter_id)
    registry = _load_registry()
    if any(item.get("chapter_id") == chapter_id for item in registry["chapters"]):
        raise RuntimeError(f"chapter already exists: {chapter_id}")
    sequence = validate_chapter_sequence(registry["chapters"], chapter_id)
    if not sequence["valid"]:
        raise RuntimeError("; ".join(sequence["errors"]))
    chapter_dir = runtime_path(f"system/production_runtime/chapters/{chapter_id}")
    intent_path = chapter_dir / "intent.json"
    _write_json(intent_path, intent)
    source_hashes = {
        Path(item["path"]).stem: str(item["sha256"])
        for item in readiness["canonical_inputs"]
    }
    record = {
        "chapter_id": chapter_id,
        "stage": "chapter_intent",
        "artifacts": {"intent": str(intent_path.relative_to(ROOT))},
        "source_hashes": source_hashes,
    }
    registry["chapters"].append(record)
    _save_registry(registry)
    return record


def compile_chapter_context(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = next((item for item in registry["chapters"] if item["chapter_id"] == chapter_id), None)
    if not record:
        raise RuntimeError(f"unknown chapter: {chapter_id}")
    chapter_dir = runtime_path(f"system/production_runtime/chapters/{chapter_id}")
    compile_stage = validate_context_compile_stage(record, chapter_dir)
    if not compile_stage["valid"]:
        raise RuntimeError("; ".join(compile_stage["errors"]))
    intent = _read_json(runtime_path(record["artifacts"]["intent"]))
    store = _read_json(runtime_path("system/creation_assets/project_assets.v0.2.json"))
    prior = []
    chapter_ordinal = int(chapter_id.removeprefix("chapter-"))
    for item in registry["chapters"]:
        settlement_path = item.get("artifacts", {}).get("settlement")
        item_ordinal = int(str(item["chapter_id"]).removeprefix("chapter-"))
        if settlement_path and item.get("stage") == "chapter_accepted" and item_ordinal < chapter_ordinal:
            prior.append(_read_json(runtime_path(settlement_path)))
    baseline = _read_json(CANONICAL_BASELINE_PATH)
    baseline_metadata = {
        "path": str(CANONICAL_BASELINE_PATH.relative_to(ROOT)),
        "version": str(baseline["version"]),
        "sha256": _sha256(CANONICAL_BASELINE_PATH),
    }
    literary_semantic_contract = build_chapter_literary_semantic_contract(
        chapter_id, baseline
    )
    story_beat = story_beat_for(chapter_id)
    if chapter_ordinal >= 11 and not story_beat:
        raise RuntimeError(f"story window contract is missing for {chapter_id}")
    initial_state_path = runtime_path("system/production_runtime/state/canonical_initial_state.v1.json")
    initial_state = _read_json(initial_state_path) if initial_state_path.is_file() else None
    compiled = compile_chapter_context_payload(
        intent,
        store.get("assets", []),
        record["source_hashes"],
        prior,
        baseline_metadata,
        story_beat,
        initial_state,
        literary_semantic_contract,
    )
    if not compiled["valid"]:
        raise RuntimeError("; ".join(compiled["errors"]))
    paths = {
        "context": chapter_dir / "context.json",
        "rule_stack": chapter_dir / "rule_stack.json",
        "trace": chapter_dir / "trace.json",
    }
    for key, path in paths.items():
        _write_json(path, compiled[key])
        record["artifacts"][key] = str(path.relative_to(ROOT))
    record["stage"] = "context_compiled"
    if not compile_stage["recompile"]:
        _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "artifacts": record["artifacts"]}


def _chapter_record(registry: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    record = next((item for item in registry["chapters"] if item["chapter_id"] == chapter_id), None)
    if not record:
        raise RuntimeError(f"unknown chapter: {chapter_id}")
    return record


def build_chapter_writer_prompt(chapter_id: str) -> str:
    adapters = _read_json(runtime_path("system/runtime/agent_adapters.json"))
    preflight = build_production_preflight(adapters, allowed_pending_chapter_id=chapter_id)
    if not preflight["valid"]:
        blocked = [name for name, passed in preflight["checks"].items() if not passed]
        raise RuntimeError("production preflight is blocked: " + ", ".join(blocked))
    readiness = build_production_readiness(chapter_id)
    if not readiness["ready"]:
        raise RuntimeError("production readiness gate is blocked")
    if not has_bounded_prose_authorization(load_decisions(), chapter_id):
        raise RuntimeError(f"controlled prose authorization is blocked for {chapter_id}")
    if prior_window_review_required(chapter_id):
        raise RuntimeError(f"prior ten-chapter window review is required before {chapter_id}")
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "context_compiled":
        raise RuntimeError("chapter must be context_compiled before writing")
    semantic_integrity = validate_compiled_literary_semantic_context(
        record, chapter_id
    )
    if not semantic_integrity["valid"]:
        raise RuntimeError(
            "compiled literary semantic context is blocked: "
            + "; ".join(semantic_integrity["errors"])
        )
    context = _read_json(runtime_path(record["artifacts"]["context"]))
    rules = _read_json(runtime_path(record["artifacts"]["rule_stack"]))
    writer_context = _compact_chapter_context(context)
    writer_rules = {
        **rules,
        "hard_rules": [
            rule
            for rule in rules.get("hard_rules", [])
            if "不得生成章节正文、场景草稿或对话" not in str(rule)
            and "intent metadata only" not in str(rule)
        ],
    }
    prompt = "\n".join(
        [
            f"你已获得 Owner Gate 对 {chapter_id} 的一次性受控正文测试授权。",
            "你是 Novel Research Lab 的受控正文写手。只输出完整小说正文，不要 JSON、标题、说明或确认。",
            "本次授权仅覆盖非正文意图阶段留下的临时正文禁令；其余规则栈全部保持生效。",
            "prose 目标 3200-3500 个中文字符，必须完整写到结尾钩子，不得用摘要压缩。严格服从上下文与规则栈；不得引入未登记资产或状态变化。",
            "避免工整段落、总结句、抽象议论堆叠、重复转折词和‘不是因为…而是因为…’模板。",
            "不得把残印、封布、胸前冷感作为每章固定反应；同一章‘残印’和‘封布’各不超过三次，优先用规则变化、空间、物证和人物选择推进。",
            "严格继承伤病与肢体状态：失明眼、失能肢体和既有伤势不得在无明确治疗事件时恢复动作、触觉或精细发力。",
            "结尾钩子成立后立即收束；禁止用连续短段、倒计时、同义复述或反复亮格拖长悬念，不得连续出现六个以上不足二十字的非对话段落。",
            "prose 只能包含读者可见的小说正文，严禁复制上下文 JSON、字段名、规则栈、asset_id、contract_path 或任何工程元数据。",
            "抽象机制必须落成动作、感官、物件、关系选择和后果。",
            "",
            "上下文：",
            json.dumps(writer_context, ensure_ascii=False),
            "",
            "规则栈：",
            json.dumps(writer_rules, ensure_ascii=False),
        ]
    )
    if len(prompt.encode("utf-8")) > MAX_WRITER_PROMPT_BYTES:
        raise RuntimeError(
            f"writer prompt exceeds {MAX_WRITER_PROMPT_BYTES} bytes; narrow story-window assets before generation"
        )
    return prompt


def validate_prose_entry_gate(chapter_id: str) -> dict[str, Any]:
    """Recheck live authorization before every route that creates or ingests prose."""
    adapters = _read_json(runtime_path("system/runtime/agent_adapters.json"))
    preflight = build_production_preflight(
        adapters, allowed_pending_chapter_id=chapter_id
    )
    readiness = build_production_readiness(chapter_id)
    checks = {
        "production_preflight": preflight.get("valid") is True,
        "production_readiness": readiness.get("ready") is True,
        "bounded_prose_authorization": has_bounded_prose_authorization(
            load_decisions(), chapter_id
        ),
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "errors": [name for name, passed in checks.items() if not passed],
    }


def _compact_chapter_context(context: dict[str, Any]) -> dict[str, Any]:
    """Keep model prompts bounded while retaining every enforceable asset constraint."""
    writer_asset_ids = {
        str(item) for item in context.get("writer_asset_ids", [])
    } or {str(item.get("asset_id")) for item in context.get("assets", [])}
    compact_assets = []
    for asset in context.get("assets", []):
        if str(asset.get("asset_id")) not in writer_asset_ids:
            continue
        compact_assets.append(dict(asset))
    selected_ids = {str(item.get("asset_id")) for item in compact_assets}
    rolling = context.get("rolling_state", {})
    latest_by_asset: dict[str, list[dict[str, Any]]] = {}
    for item in rolling.get("latest_fields", []):
        asset_id = str(item.get("asset_id"))
        if asset_id not in selected_ids:
            continue
        latest_by_asset.setdefault(asset_id, []).append(item)
    compact_latest = []
    for asset_id in sorted(latest_by_asset):
        items = latest_by_asset[asset_id]
        items.sort(
            key=lambda item: (
                str(item.get("chapter_id", "")),
                str(item.get("field_path", "")),
            )
        )
        compact_latest.extend(
            {
                "asset_id": item.get("asset_id"),
                "field_path": item.get("field_path"),
                "value": item.get("value"),
                "chapter_id": item.get("chapter_id"),
            }
            for item in items[-8:]
        )
    compact_rolling = {
        "source_chapter_count": rolling.get("source_chapter_count", 0),
        "latest_fields": compact_latest,
        "recent_chapters": [],
    }
    # Latest fields already carry the canonical current value. Keep only a bounded
    # immediate-transition digest so long-running projects cannot grow prompts
    # without limit by repeating the same state in settlement history.
    recent_chapters = rolling.get("recent_chapters", [])[-1:]
    for chapter in recent_chapters:
        changes = [
            {
                "asset_id": item.get("asset_id"),
                "field_path": item.get("field_path"),
                "after": item.get("after"),
            }
            for item in chapter.get("changes", [])
            if str(item.get("asset_id")) in selected_ids
        ][-12:]
        if changes:
            compact_rolling["recent_chapters"].append(
                {"chapter_id": chapter.get("chapter_id"), "changes": changes}
            )
    return {
        "chapter_id": context.get("chapter_id"),
        "dramatic_purpose": context.get("dramatic_purpose"),
        "story_beat": context.get("story_beat"),
        "literary_semantic_contract": context.get("literary_semantic_contract"),
        "must_keep": context.get("must_keep", []),
        "must_avoid": context.get("must_avoid", []),
        "scene_constraints": context.get("scene_constraints", []),
        "expected_state_deltas": context.get("expected_state_deltas", []),
        "assets": compact_assets,
        "rolling_state": compact_rolling,
    }


def _compact_observer_context(context: dict[str, Any]) -> dict[str, Any]:
    """Give the fact observer IDs and current values without literary constraints."""
    compact = _compact_chapter_context(context)
    latest_by_asset: dict[str, list[dict[str, Any]]] = {}
    for item in compact.get("rolling_state", {}).get("latest_fields", []):
        latest_by_asset.setdefault(str(item.get("asset_id", "")), []).append(item)
    recent_latest = []
    for items in latest_by_asset.values():
        items.sort(key=lambda item: (str(item.get("chapter_id", "")), str(item.get("field_path", ""))))
        recent_latest.extend(items[-3:])
    return {
        "chapter_id": compact.get("chapter_id"),
        "story_beat": compact.get("story_beat"),
        "expected_state_deltas": compact.get("expected_state_deltas", []),
        "assets": [
            {
                "asset_id": item.get("asset_id"),
                "display_name": item.get("display_name"),
                "family": item.get("family"),
            }
            for item in compact.get("assets", [])
        ],
        "rolling_state": {
            "latest_fields": recent_latest,
            "recent_chapters": compact.get("rolling_state", {}).get("recent_chapters", []),
        },
    }


def build_bundled_observation(
    chapter_id: str, prose: str, facts: list[dict[str, Any]]
) -> dict[str, Any]:
    """Bind writer-emitted facts to the exact prose without a second model call."""
    payload = normalize_observation_payload(
        {"chapter_id": chapter_id, "draft_sha256": _sha256_text(prose), "facts": facts}
    )
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_observation.schema.json"))
    jsonschema.validate(payload, schema)
    return payload


def _ask_chapter_bundle(prompt: str, model: str) -> tuple[dict[str, Any], str, str]:
    schema = runtime_path("system/production_runtime/schemas/chapter_generation.schema.json")
    errors = []
    if not codex_usage_limited():
        try:
            return ask_codex_structured(prompt, model=model, schema_path=schema), "codex", model
        except RuntimeError as error:
            errors.append(f"{model}: {error}")
    route = route_model("writer")
    for fallback_model in filter(None, (route["fallback_model"], route.get("secondary_fallback_model"))):
        try:
            response = ask_antigravity_writer(
                prompt + "\n只返回 JSON 对象，字段必须为 prose 和 facts。", model=fallback_model
            )
            payload = extract_json_object(response)
            jsonschema.validate(payload, _read_json(schema))
            return payload, "antigravity", fallback_model
        except (RuntimeError, jsonschema.ValidationError) as error:
            errors.append(f"{fallback_model}: {error}")
    raise RuntimeError("all bundled chapter providers failed: " + "; ".join(errors))


def _record_writer_attempt(chapter_id: str, payload: dict[str, Any]) -> str:
    """Keep failed direct-writer attempts inspectable without advancing chapter state."""
    target = runtime_path(
        f"system/production_runtime/chapters/{chapter_id}/draft.attempt.json"
    )
    _write_json(target, payload)
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "chapter_accepted":
        record["artifacts"]["draft_attempt"] = str(target.relative_to(ROOT))
        _save_registry(registry)
    return str(target.relative_to(ROOT))


def _insert_length_recovery(draft: str, insert: str) -> str:
    """Place a short bridge before the closing beat without changing its payoff."""
    paragraphs = [part for part in draft.strip().split("\n\n") if part.strip()]
    if len(paragraphs) < 3:
        return draft.strip() + "\n\n" + insert.strip()
    closing = paragraphs[-2:]
    return "\n\n".join([*paragraphs[:-2], insert.strip(), *closing])


def _reflow_oversized_paragraphs(text: str, max_chars: int = 500) -> str:
    """Add paragraph boundaries at sentence endings without changing prose."""
    output = []
    for paragraph in (part.strip() for part in text.split("\n\n")):
        if not paragraph or len(paragraph) <= max_chars:
            if paragraph:
                output.append(paragraph)
            continue
        sentences = [part for part in re.split(r"(?<=[。！？])", paragraph) if part]
        if len(sentences) == 1:
            output.append(paragraph)
            continue
        chunk = ""
        for sentence in sentences:
            if chunk and len(chunk) + len(sentence) > max_chars:
                output.append(chunk)
                chunk = sentence
            else:
                chunk += sentence
        if chunk:
            output.append(chunk)
    return "\n\n".join(output)


CHAPTER_HEADING_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:第[零〇一二三四五六七八九十百0-9]{1,8}章(?:\s+.*)?|chapter\s+[0-9]+(?:\s+.*)?)\s*$",
    re.IGNORECASE,
)


def _strip_leading_chapter_heading(text: str) -> str:
    """Remove a provider-added title line without touching narrative prose."""
    lines = text.strip().splitlines()
    first_content = next((index for index, line in enumerate(lines) if line.strip()), None)
    if first_content is not None and CHAPTER_HEADING_RE.fullmatch(lines[first_content]):
        del lines[first_content]
    return "\n".join(lines).strip()


def _contains_chapter_heading(text: str) -> bool:
    return any(CHAPTER_HEADING_RE.fullmatch(line) for line in text.splitlines())


def _ask_prose_writer(prompt: str, model: str) -> tuple[str, str, str]:
    """Use Codex first, then an isolated literary provider when Codex is quota-bound."""
    primary_error = None
    if not codex_usage_limited():
        try:
            return ask_codex_writer(prompt, model=model), "codex", model
        except RuntimeError as error:
            primary_error = str(error)
    route = route_model("writer")
    fallback_models = (
        route["fallback_model"],
        route.get("secondary_fallback_model"),
        route.get("tertiary_fallback_model"),
    )
    fallback_errors = []
    for fallback_model in filter(None, fallback_models):
        try:
            return (
                ask_antigravity_writer(prompt, model=fallback_model),
                "antigravity",
                fallback_model,
            )
        except RuntimeError as error:
            fallback_errors.append(f"{fallback_model}: {error}")
    details = "; ".join(filter(None, (primary_error, *fallback_errors)))
    raise RuntimeError(f"all prose providers failed: {details}")


def _ask_prose_editor(prompt: str) -> tuple[str, str, str]:
    """Use the bounded editor route without spending a literary fallback call."""
    route = route_model("editor")
    primary_error = None
    if not codex_usage_limited():
        try:
            return ask_codex_writer(prompt, model=route["model"]), "codex", route["model"]
        except RuntimeError as error:
            primary_error = str(error)
    try:
        model = route["fallback_model"]
        return ask_antigravity_writer(prompt, model=model), "antigravity", model
    except RuntimeError as error:
        details = "; ".join(filter(None, (primary_error, str(error))))
        raise RuntimeError(f"all prose editors failed: {details}") from error


def _recover_short_draft(chapter_id: str, prompt: str, draft: str) -> tuple[str, dict[str, Any] | None]:
    """Request a bounded bridge when a valid scene is cut short by provider output limits."""
    metrics = analyze_prose_metrics(draft)
    if metrics["chinese_character_count"] >= MIN_CHAPTER_CHINESE_CHARS:
        return draft, None
    deficit = MIN_CHAPTER_CHINESE_CHARS - metrics["chinese_character_count"]
    requested_min = min(max(deficit + 150, 300), 900)
    requested_max = min(requested_min + 400, 1200)
    closing = "\n\n".join(part for part in draft.strip().split("\n\n")[-3:] if part.strip())
    recovery_prompt = "\n".join([
        f"你是{active_project_title()}{chapter_id} 的受控编辑。只输出一段 {requested_min}-{requested_max} 个中文字符的场景桥段，不要标题、解释或总结。",
        "这段将插入既有正文的结尾前，必须保持人物、资产、时间和状态约束；用尚未发生的动作、感官和选择补足冲突，不能解决结尾悬念或新增事实。",
        "不得复述既有结尾中的发现、物件交接、人物站位、对白、判断或收束动作；桥段最后必须自然接回既有结尾第一句。",
        "原有写作规则：", prompt[-5000:],
        "既有结尾前的片段：", closing,
    ])
    try:
        insert, provider, model = _ask_prose_editor(recovery_prompt)
    except RuntimeError as error:
        return draft, {"valid": False, "error": str(error)}
    insert = _reflow_oversized_paragraphs(insert)
    insert_metrics = analyze_prose_metrics(insert)
    if not 180 <= insert_metrics["chinese_character_count"] <= 1400:
        return draft, {"valid": False, "metrics": insert_metrics, "error": "length recovery bridge out of range"}
    recovered = _insert_length_recovery(draft, insert)
    return recovered, {"valid": True, "metrics": insert_metrics, "provider": provider, "model": model}


def _generated_prose_errors(text: str, metrics: dict[str, Any]) -> list[str]:
    errors = []
    if not MIN_CHAPTER_CHINESE_CHARS <= metrics.get("chinese_character_count", 0) <= MAX_CHAPTER_CHINESE_CHARS:
        errors.append("prose must contain 3000-4200 Chinese characters")
    if _contains_chapter_heading(text):
        errors.append("prose must not contain a chapter heading")
    flags = set(metrics.get("flags", []))
    if "tail_fragmentation_loop" in flags:
        errors.append("prose ending contains a fragmented repetition loop")
    if "prompt_context_leak" in flags:
        errors.append("prose contains leaked prompt or runtime context")
    if "generation_meta_leak" in flags:
        errors.append("prose contains generation or completion metadata")
    if "latin_token_leak" in flags:
        errors.append("prose contains leaked Latin-language tokens")
    if flags & {"termination_token_loop", "oversized_paragraph_loop", "duplicate_text_span"}:
        errors.append("prose contains repeated or malformed prose blocks")
    return errors


def _best_short_recovery_candidate(current: str, candidate: str) -> str:
    """Keep the longest structurally clean short draft for bounded recovery."""
    metrics = analyze_prose_metrics(candidate)
    count = metrics.get("chinese_character_count", 0)
    blocking_flags = {
        "tail_fragmentation_loop", "prompt_context_leak", "generation_meta_leak",
        "termination_token_loop", "oversized_paragraph_loop", "duplicate_text_span",
    }
    if not 1 <= count < MIN_CHAPTER_CHINESE_CHARS:
        return current
    if _contains_chapter_heading(candidate) or set(metrics.get("flags", [])) & blocking_flags:
        return current
    if not current:
        return candidate
    current_count = analyze_prose_metrics(current).get("chinese_character_count", 0)
    return candidate if count > current_count else current


def dispatch_chapter_draft(chapter_id: str) -> dict[str, Any]:
    prompt = build_chapter_writer_prompt(chapter_id)
    attempts = []
    text = ""
    metrics: dict[str, Any] = {}
    errors: list[str] = []
    selected_model = None
    bundled_observation: dict[str, Any] | None = None
    bundled_facts: list[dict[str, Any]] = []
    repair_candidate = ""
    short_recovery_candidate = ""
    chapter_dir = runtime_path(f"system/production_runtime/chapters/{chapter_id}")
    candidate_path = chapter_dir / "draft.recovery_candidate.md"
    if candidate_path.is_file():
        cached = candidate_path.read_text(encoding="utf-8")
        cached_metrics = analyze_prose_metrics(cached)
        text = cached
        metrics = cached_metrics
        errors = _generated_prose_errors(cached, cached_metrics)
        if cached_metrics.get("chinese_character_count", 0) < MIN_CHAPTER_CHINESE_CHARS:
            short_recovery_candidate = _best_short_recovery_candidate("", cached)
        else:
            repair_candidate = cached
    # Drafting stays on the sustained-production route. Sol adjudicates windows;
    # using it as an implicit per-chapter retry multiplies cost without adding a gate.
    for model in (() if (repair_candidate or short_recovery_candidate) else (route_model("writer")["model"],)):
        for generation in range(1, 3):
            retry_prompt = prompt
            if generation == 2:
                retry_prompt += "\n\n上一版未通过长度或结尾节奏门禁。请从头完整重写，不要续写；必须交付 3100-3500 个中文字符，并在结尾钩子成立后立即收束，禁止连续短段同义复述。"
            try:
                raw_text, provider, used_model = _ask_prose_writer(retry_prompt, model)
                text = _strip_leading_chapter_heading(raw_text)
                bundled_facts = []
                bundled_observation = None
            except RuntimeError as error:
                attempts.append({"model": model, "generation": generation, "valid": False, "error": str(error)})
                errors = ["writer provider failed"]
                continue
            metrics = analyze_prose_metrics(text)
            errors = _generated_prose_errors(text, metrics)
            attempts.append(
                {
                    "model": used_model,
                    "provider": provider,
                    "generation": generation,
                    "valid": not errors,
                    "metrics": metrics,
                    "response_preview": text[:500],
                }
            )
            if not errors:
                selected_model = used_model
                break
            short_recovery_candidate = _best_short_recovery_candidate(
                short_recovery_candidate, text
            )
            count = metrics.get("chinese_character_count", 0)
            if (
                MIN_CHAPTER_CHINESE_CHARS <= count <= 6000
                and not _contains_chapter_heading(text)
                and not set(metrics.get("flags", [])) & {
                    "prompt_context_leak", "generation_meta_leak", "termination_token_loop",
                    "duplicate_text_span",
                }
            ):
                repair_candidate = text
                candidate_path.write_text(text, encoding="utf-8")
                break
            if short_recovery_candidate:
                candidate_path.write_text(short_recovery_candidate, encoding="utf-8")
                break
        if repair_candidate:
            break
        if short_recovery_candidate:
            break
        if selected_model:
            break
    if not selected_model and not repair_candidate and short_recovery_candidate:
        text = short_recovery_candidate
        metrics = analyze_prose_metrics(text)
        errors = _generated_prose_errors(text, metrics)
    if repair_candidate and errors:
        cleanup_prompt = "\n".join([
            f"你是{active_project_title()}{chapter_id} 的受控清稿编辑。只输出清理后的完整小说正文，不要标题、解释或确认。",
            "保留候选稿已经发生的情节、人物选择、物证流转、状态结果和结尾钩子，不得新增事实。",
            "删除重复文本、超长粘连段、提示词、工程字段、完成日志、凑字内容和结束词循环；段落适合移动端阅读。",
            "正文必须为 3100-3500 个中文字符。若候选稿尾部损坏，在最后一个完整叙事钩子处结束。",
            "原写作约束：", prompt,
            "候选稿：", repair_candidate,
        ])
        for cleanup_generation in range(1, 3):
            current_prompt = cleanup_prompt
            if cleanup_generation == 2:
                current_prompt += "\n\n上一版清稿长度不足或仍有格式故障。请完整重写为 3200-3500 个中文字符，分成自然段并只输出正文。"
            try:
                cleaned, provider, used_model = _ask_prose_editor(current_prompt)
                text = _strip_leading_chapter_heading(cleaned)
                metrics = analyze_prose_metrics(text)
                errors = _generated_prose_errors(text, metrics)
                attempts.append({
                    "model": used_model, "provider": provider,
                    "generation": f"quality_repair_{cleanup_generation}",
                    "valid": not errors, "errors": errors, "metrics": metrics,
                    "response_preview": text[:500],
                })
                if not errors:
                    selected_model = used_model
                    bundled_observation = None
                    bundled_facts = []
                    break
            except RuntimeError as error:
                errors = ["quality repair provider failed"]
                attempts.append({
                    "model": route_model("writer")["model"],
                    "generation": f"quality_repair_{cleanup_generation}",
                    "valid": False, "error": str(error),
                })
    recoveries = []
    if (
        errors
        and text
        and analyze_prose_metrics(text)["chinese_character_count"] < MIN_CHAPTER_CHINESE_CHARS
    ):
        for _ in range(3):
            if analyze_prose_metrics(text)["chinese_character_count"] >= MIN_CHAPTER_CHINESE_CHARS:
                break
            text, recovery = _recover_short_draft(chapter_id, prompt, text)
            recoveries.append(recovery)
            if not recovery or not recovery.get("valid"):
                break
        metrics = analyze_prose_metrics(text)
        errors = _generated_prose_errors(text, metrics)
        successful_recovery = next(
            (item for item in reversed(recoveries) if item.get("valid")), {}
        )
        attempts.append({
            "model": successful_recovery.get("model", route_model("writer")["model"]),
            "provider": successful_recovery.get("provider"),
            "generation": "length_recovery",
            "valid": not errors,
            "metrics": metrics,
            "recoveries": recoveries,
        })
        if not errors:
            selected_model = route_model("writer")["model"]
    if errors:
        if text and not set(analyze_prose_metrics(text).get("flags", [])) & {
            "prompt_context_leak", "generation_meta_leak", "termination_token_loop",
        }:
            candidate_path.write_text(text, encoding="utf-8")
        attempt_path = _record_writer_attempt(
            chapter_id,
            {
                "chapter_id": chapter_id,
                "status": "writer_failed",
                "errors": errors,
                "attempts": attempts,
            },
        )
        return {"valid": False, "errors": errors, "metrics": metrics, "attempts": attempts, "attempt_path": attempt_path}
    valid_attempt = next(
        (
            item for item in reversed(attempts)
            if item.get("valid") and item.get("provider") and item.get("model")
        ),
        None,
    )
    if active_project_id() != "borrowed-heaven" and (
        valid_attempt is None
        or valid_attempt.get("provider") != "codex"
        or valid_attempt.get("model") != "gpt-5.6-terra"
    ):
        attempt_path = _record_writer_attempt(
            chapter_id,
            {
                "chapter_id": chapter_id,
                "status": "formal_terra_execution_required",
                "errors": ["formal draft must be executed by Codex gpt-5.6-terra"],
                "attempts": attempts,
            },
        )
        return {
            "valid": False,
            "errors": ["formal draft must be executed by Codex gpt-5.6-terra"],
            "metrics": metrics,
            "attempts": attempts,
            "attempt_path": attempt_path,
        }
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "draft_generated", "draft.md")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    draft_path = chapter_dir / "draft.md"
    metrics_path = chapter_dir / "draft.metrics.json"
    draft_path.write_text(text, encoding="utf-8")
    candidate_path.unlink(missing_ok=True)
    _write_json(metrics_path, metrics)
    cost_path = chapter_dir / "generation_cost.json"
    _write_json(cost_path, {
        "version": VERSION,
        "chapter_id": chapter_id,
        "prompt_bytes": len(prompt.encode("utf-8")),
        "writer_asset_count": len(_compact_chapter_context(_read_json(runtime_path(record["artifacts"]["context"]))).get("assets", [])),
        "provider_calls": len(attempts),
        "used_length_recovery": bool(recoveries),
        "writer_model": selected_model,
    })
    record["artifacts"].update({
        "draft": str(draft_path.relative_to(ROOT)),
        "draft_metrics": str(metrics_path.relative_to(ROOT)),
        "generation_cost": str(cost_path.relative_to(ROOT)),
    })
    if valid_attempt is not None:
        record["artifacts"]["draft_writer_execution"] = _write_role_execution(
            chapter_id,
            "draft_writer",
            draft_path,
            provider=str(valid_attempt["provider"]),
            model=str(valid_attempt["model"]),
        )
    record["stage"] = "draft_generated"
    _save_registry(registry)
    return {
        "valid": True,
        "chapter_id": chapter_id,
        "stage": record["stage"],
        "metrics": metrics,
        "writer_model": selected_model,
        "attempts": attempts,
    }


def ingest_chapter_observation(chapter_id: str, file_arg: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "final_observed", file_arg)
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    source = Path(file_arg)
    if not source.is_absolute():
        source = ROOT / source
    observation = _read_json(source)
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_observation.schema.json"))
    jsonschema.validate(observation, schema)
    final_path = runtime_path(record["artifacts"]["revision"])
    if observation["chapter_id"] != chapter_id or observation["draft_sha256"] != _sha256(final_path):
        raise RuntimeError("observation is stale or bound to another final text")
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/observation.json")
    _write_json(target, observation)
    record["artifacts"]["observation"] = str(target.relative_to(ROOT))
    record["stage"] = "final_observed"
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "observation": record["artifacts"]["observation"]}


def ingest_bundled_observation(chapter_id: str) -> dict[str, Any]:
    """Reuse the writer sidecar when revision content is byte-identical to the draft."""
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    candidate = record.get("artifacts", {}).get("bundled_observation")
    if not candidate:
        return {"valid": False, "reason": "bundled observation is missing"}
    candidate_path = runtime_path(candidate)
    revision_path = runtime_path(record["artifacts"]["revision"])
    if not candidate_path.is_file():
        return {"valid": False, "reason": "bundled observation file is missing"}
    payload = _read_json(candidate_path)
    if payload.get("draft_sha256") != _sha256(revision_path):
        return {"valid": False, "reason": "revision changed after bundled observation"}
    result = ingest_chapter_observation(chapter_id, str(candidate_path))
    return {"valid": True, **result}


def build_observer_prompt_payload(
    chapter_id: str, draft_sha256: str, draft_text: str, context: dict[str, Any]
) -> str:
    return "\n".join(
        [
            "你是 Novel Research Lab 的 Codex 事实观察器。只输出符合指定 JSON Schema 的对象。",
            "逐项记录正文实际发生的状态变化，不补写剧情，不推测未发生事实。",
            "每个事实必须有唯一 fact_id、已登记 asset_id、字段路径、before、after 和正文证据摘要。",
            f"chapter_id: {chapter_id}",
            f"draft_sha256: {draft_sha256}",
            "上下文：",
            json.dumps(context, ensure_ascii=False),
            "正文：",
            draft_text,
        ]
    )


OBSERVATION_FACT_CATEGORIES = (
    "characters", "npcs", "locations", "factions", "artifacts", "techniques",
    "relationships", "emotions", "information", "hooks", "timeline",
    "physical_state", "naming",
)


def normalize_observation_payload(
    payload: dict[str, Any], *, chapter_id: str | None = None, draft_sha256: str | None = None
) -> dict[str, Any]:
    """Normalize an equivalent flat fact list without weakening the stored contract."""
    normalized = {
        key: value for key, value in payload.items()
        if key in {"chapter_id", "draft_sha256", "facts"}
    }
    if chapter_id is not None:
        normalized["chapter_id"] = chapter_id
    if draft_sha256 is not None:
        normalized["draft_sha256"] = draft_sha256
    if isinstance(payload.get("facts"), dict):
        return normalized
    facts = payload.get("facts", payload.get("changes", payload.get("fact_deltas")))
    if not isinstance(facts, list):
        return normalized
    grouped: dict[str, list[dict[str, Any]]] = {key: [] for key in OBSERVATION_FACT_CATEGORIES}
    prefix_categories = (
        ("character_", "characters"),
        ("npc_", "npcs"),
        ("location_", "locations"),
        ("faction_", "factions"),
        ("artifact_", "artifacts"),
        ("technique_", "techniques"),
        ("bond_", "relationships"),
        ("foreshadowing_", "hooks"),
        ("naming_", "naming"),
    )
    for fact in facts:
        asset_id = str(fact.get("asset_id", "")) if isinstance(fact, dict) else ""
        field_path = str(fact.get("field_path", "")) if isinstance(fact, dict) else ""
        category = next((value for prefix, value in prefix_categories if asset_id.startswith(prefix)), None)
        if category is None and asset_id.startswith("state_ledger_"):
            if any(token in field_path for token in ("emotion", "trust", "bond")):
                category = "emotions"
            elif any(token in field_path for token in ("timeline", "deadline", "countdown")):
                category = "timeline"
            elif any(token in field_path for token in ("physical", "condition", "strain", "injury", "wound")):
                category = "physical_state"
            else:
                category = "information"
        grouped[category or "information"].append(fact)
    return {**normalized, "facts": grouped}


def dispatch_chapter_observation(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "revision_generated":
        raise RuntimeError("chapter must be revision_generated before final observation")
    final_text = runtime_path(record["artifacts"]["revision"])
    context = _compact_observer_context(
        _read_json(runtime_path(record["artifacts"]["context"]))
    )
    prompt = build_observer_prompt_payload(
        chapter_id, _sha256(final_text), final_text.read_text(encoding="utf-8"), context
    )
    output = runtime_path(f"system/production_runtime/chapters/{chapter_id}/observation.candidate.json")
    schema = runtime_path("system/production_runtime/schemas/chapter_observation.schema.json")
    observer = route_model("observer")
    provider = "codex"
    if not codex_usage_limited() and (binary := shutil.which("codex")):
        try:
            result = subprocess.run(
                [
                    binary, "--ask-for-approval", "never", "exec", "--ephemeral",
                    "--sandbox", "read-only", "-m", observer["model"],
                    "--output-schema", str(schema), "-o", str(output), prompt,
                ],
                cwd=ROOT, text=True, capture_output=True, check=False, timeout=300,
            )
        except subprocess.TimeoutExpired:
            output.unlink(missing_ok=True)
            result = None
        if result is not None and (result.returncode != 0 or not output.is_file()):
            output.unlink(missing_ok=True)
            if "usage limit" not in result.stderr.lower() and "hit your usage" not in result.stderr.lower():
                raise RuntimeError(f"Codex observer failed: {result.stderr.strip()}")
    if not output.is_file():
        if active_project_id() != "borrowed-heaven":
            raise RuntimeError("formal observation requires an independent Codex Luna execution")
        provider = "antigravity"
        response = ask_antigravity_writer(
            prompt + "\n只返回一个 JSON 对象，所有 required 字段都必须存在，空类别使用空数组。",
            model=observer["fallback_model"],
        )
        payload = normalize_observation_payload(
            extract_json_object(response), chapter_id=chapter_id,
            draft_sha256=_sha256(final_text),
        )
        jsonschema.validate(payload, _read_json(schema))
        _write_json(output, payload)
    else:
        payload = normalize_observation_payload(
            _read_json(output),
            chapter_id=chapter_id,
            draft_sha256=_sha256(final_text),
        )
        jsonschema.validate(payload, _read_json(schema))
        _write_json(output, payload)
    ingested = ingest_chapter_observation(chapter_id, str(output))
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    observation_path = runtime_path(record["artifacts"]["observation"])
    observer_model = observer["model"] if provider == "codex" else observer["fallback_model"]
    record["artifacts"]["observer_execution"] = _write_role_execution(
        chapter_id,
        "observer",
        observation_path,
        provider=provider,
        model=observer_model,
        bindings={"revision_sha256": _sha256(final_text)},
    )
    _save_registry(registry)
    output.unlink(missing_ok=True)
    return {
        **ingested,
        "observer_provider": provider,
        "observer_model": observer_model,
    }


def build_chapter_audit_packet(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] == "draft_generated":
        artifact_kind = "draft"
        observation = None
        audit_kind = "initial"
    elif record["stage"] == "final_observed":
        artifact_kind = "revision"
        observation = _read_json(runtime_path(record["artifacts"]["observation"]))
        audit_kind = "final"
    else:
        raise RuntimeError("chapter must be draft_generated or final_observed before audit")
    prose_path = runtime_path(record["artifacts"][artifact_kind])
    context_path = runtime_path(record["artifacts"]["context"])
    template = {
        "chapter_id": chapter_id,
        "artifact_kind": artifact_kind,
        "artifact_sha256": _sha256(prose_path),
        "context_sha256": _sha256(context_path),
        "verdict": "ACCEPT_WITH_WARNINGS",
        "dimensions": {
            key: [f"必须替换为针对 {key} 的正文或上下文具体证据"]
            for key in (
                "canon",
                "character",
                "state",
                "causality",
                "pacing",
                "life_force",
                "anti_ai_taste",
                "originality",
                "semantic_realization",
                "progression_permissions",
                "history_coherence",
            )
        },
        "issues": [],
        "resolved_prior_issue_ids": [],
    }
    context = _read_json(context_path)
    rules = _read_json(runtime_path(record["artifacts"]["rule_stack"]))
    trace = _read_json(runtime_path(record["artifacts"]["trace"]))
    prose = prose_path.read_text(encoding="utf-8")
    prior_audit = None
    if audit_kind == "final" and record.get("artifacts", {}).get("continuity_audit"):
        prior_audit = _read_json(runtime_path(record["artifacts"]["continuity_audit"]))
        template["resolved_prior_issue_ids"] = [
            str(item.get("issue_id"))
            for item in prior_audit.get("issues", [])
            if item.get("severity") in {"blocking", "major"}
        ]
    audit_context = _compact_chapter_context(context)
    packet = runtime_path(f"system/production_runtime/chapters/{chapter_id}/{artifact_kind}_audit_packet.md")
    packet.write_text(
        "\n".join([
            "# NRL Chapter Audit v0.27", "",
            "Judge continuity, causality, long-form vitality and AI-taste independently from the inline, hash-bound artifacts below.",
            "Explicitly verify that the prose realizes its chapter semantic beat, keeps every action within current progression permissions and liabilities, and uses only historical evidence available in this chapter.",
            "Do not use terminal tools, inspect files, run tests, make a plan, or wait for background work. The complete review packet is inline.",
            "Do not rewrite prose. Return one JSON object only using the exact binding hashes, with no Markdown fence or surrounding text.", "",
            "Every array under dimensions must contain at least one specific evidence sentence grounded in the supplied prose/context. Empty arrays, generic placeholders, and copied instructions are invalid.", "",
            "## Compact Context", json.dumps(audit_context, ensure_ascii=False), "",
            "## Rule Stack", json.dumps(rules, ensure_ascii=False), "",
            "## Compilation Trace", json.dumps(trace, ensure_ascii=False), "",
            "## Observed Facts", json.dumps(observation, ensure_ascii=False) if observation else "Initial audit: no final-text observations exist yet.", "",
            "## Initial Audit To Close", json.dumps(prior_audit, ensure_ascii=False) if prior_audit else "Not applicable.", "",
            "For a final audit, verify every prior blocking or major issue is actually absent from the revision. If any remains, return REWORK_REQUIRED and repeat its issue_id.", "",
            "## Prose", prose, "", "## Required JSON", "```json",
            json.dumps(template, ensure_ascii=False, indent=2), "```", "",
        ]), encoding="utf-8"
    )
    return {"chapter_id": chapter_id, "packet_path": str(packet.relative_to(ROOT)), "template": template, "audit_kind": audit_kind}


def normalize_continuity_audit_payload(data: dict[str, Any]) -> dict[str, Any]:
    """Adapt equivalent review-agent issue labels without loosening the audit schema."""
    normalized = dict(data)
    issues = []
    severity_map = {
        "MINOR": "minor",
        "WARN": "minor",
        "WARNING": "minor",
        "MAJOR": "major",
        "BLOCKING": "blocking",
        "FATAL": "blocking",
        "CRITICAL": "blocking",
    }
    verdict_map = {
        "REJECT": "REWORK_REQUIRED",
        "REJECTED": "REWORK_REQUIRED",
        "FAIL": "REWORK_REQUIRED",
    }
    normalized["verdict"] = verdict_map.get(
        str(data.get("verdict", "")).upper(), data.get("verdict")
    )
    for index, issue in enumerate(data.get("issues", []), start=1):
        if not isinstance(issue, dict):
            issues.append(
                {
                    "issue_id": f"agent-issue-{index:03d}",
                    "severity": "major",
                    "evidence": str(issue),
                    "required_fix": "Correct the reviewer-described issue while preserving established state.",
                }
            )
            continue
        severity = issue.get("severity")
        normalized_severity = severity_map.get(str(severity).upper())
        if normalized_severity is None:
            normalized_severity = severity if severity in {"blocking", "major", "minor"} else "blocking"
        issues.append(
            {
                "issue_id": issue.get("issue_id") or issue.get("id") or f"agent-issue-{index:03d}",
                "severity": normalized_severity,
                "evidence": issue.get("evidence") or issue.get("description") or "No evidence supplied by review agent.",
                "required_fix": issue.get("required_fix") or issue.get("recommendation") or "No corrective action supplied; retain as a non-blocking review note.",
            }
        )
    normalized["issues"] = issues
    return normalized


AUDIT_EVIDENCE_DIMENSIONS = (
    "canon",
    "character",
    "state",
    "causality",
    "pacing",
    "life_force",
    "anti_ai_taste",
    "originality",
    "semantic_realization",
    "progression_permissions",
    "history_coherence",
)


def validate_literary_audit_evidence(data: dict[str, Any]) -> dict[str, Any]:
    """Require visible evidence on every literary audit dimension."""
    dimensions = data.get("dimensions", {})

    def visible(value: Any) -> bool:
        if not isinstance(value, str):
            return False
        normalized = unicodedata.normalize("NFKC", value)
        return any(
            unicodedata.category(character)[0] in {"L", "N"}
            for character in normalized
        )

    missing = [
        key
        for key in AUDIT_EVIDENCE_DIMENSIONS
        if not isinstance(dimensions.get(key), list)
        or not dimensions.get(key)
        or any(not visible(item) for item in dimensions.get(key, []))
    ]
    return {
        "valid": not missing,
        "errors": (
            []
            if not missing
            else ["literary audit omitted substantive evidence: " + ", ".join(missing)]
        ),
    }


def validate_grounded_literary_audit_evidence(
    data: dict[str, Any], grounding_text: str | None = None
) -> dict[str, Any]:
    dimensions = data.get("dimensions", {})
    base = validate_literary_audit_evidence(data)

    def evidence_tokens(value: str) -> set[str]:
        normalized = unicodedata.normalize("NFKC", value)
        tokens: set[str] = set()
        for run in re.findall(r"[\u4e00-\u9fff]{2,}", normalized):
            for size in (2, 3, 4):
                tokens.update(
                    run[index : index + size]
                    for index in range(max(len(run) - size + 1, 0))
                )
        tokens.update(
            token.lower()
            for token in re.findall(r"[A-Za-z0-9_]{4,}", normalized)
        )
        return tokens

    placeholder_markers = (
        "必须替换",
        "具体证据",
        "checked",
        "check passed",
        "无问题",
        "未发现问题",
        "符合要求",
        "通过审查",
        "hash-bound context retained",
        "state observation remains mandatory",
    )
    grounding_tokens = evidence_tokens(grounding_text or "") if grounding_text else set()
    seen_evidence: set[str] = set()
    missing = [
        key
        for key in AUDIT_EVIDENCE_DIMENSIONS
        if not isinstance(dimensions.get(key), list)
        or not dimensions.get(key)
        or any(
            len(unicodedata.normalize("NFKC", str(item)).strip()) < 8
            or any(
                marker in unicodedata.normalize("NFKC", str(item)).lower()
                for marker in placeholder_markers
            )
            or (
                grounding_text is not None
                and not (evidence_tokens(str(item)) & grounding_tokens)
            )
            for item in dimensions.get(key, [])
        )
    ]
    duplicates = []
    for key in AUDIT_EVIDENCE_DIMENSIONS:
        for item in dimensions.get(key, []) if isinstance(dimensions.get(key), list) else []:
            normalized = unicodedata.normalize("NFKC", str(item)).strip()
            if normalized in seen_evidence:
                duplicates.append(key)
            seen_evidence.add(normalized)
    return {
        "valid": base["valid"] and not missing and not duplicates,
        "errors": (
            []
            if base["valid"] and not missing and not duplicates
            else [
                *base["errors"],
                *(
                    ["literary audit omitted substantive grounded evidence: " + ", ".join(missing)]
                    if missing
                    else []
                ),
                *(
                    ["literary audit repeated evidence across dimensions: " + ", ".join(duplicates)]
                    if duplicates
                    else []
                ),
            ]
        ),
    }


def validate_final_audit_issue_closure(
    data: dict[str, Any], prior_audit: dict[str, Any]
) -> dict[str, Any]:
    """Require substantive closures while allowing known minor closures."""
    severity_rank = {"minor": 1, "major": 2, "blocking": 3}
    prior_issues: dict[str, str] = {}
    for item in prior_audit.get("issues", []):
        issue_id = str(item.get("issue_id", ""))
        severity = str(item.get("severity", ""))
        if not issue_id:
            continue
        previous = prior_issues.get(issue_id, "")
        if severity_rank.get(severity, 0) > severity_rank.get(previous, 0):
            prior_issues[issue_id] = severity
    resolved = {str(item) for item in data.get("resolved_prior_issue_ids", [])}
    required = {
        issue_id
        for issue_id, severity in prior_issues.items()
        if severity in {"blocking", "major"}
    }
    missing = sorted(required - resolved)
    unknown = sorted(resolved - set(prior_issues))
    errors = []
    if missing:
        errors.append(
            "final audit did not explicitly close required prior issues: "
            + ", ".join(missing)
        )
    if unknown:
        errors.append(
            "final audit claimed unknown prior issue closures: " + ", ".join(unknown)
        )
    return {"valid": not errors, "errors": errors}


def _chapter_audit_grounding_text(
    record: dict[str, Any], artifact_kind: str
) -> str:
    artifacts = record.get("artifacts", {})
    parts = []
    prose_path = runtime_path(artifacts.get(artifact_kind, ""))
    if prose_path.is_file():
        parts.append(prose_path.read_text(encoding="utf-8"))
    for key in ("context", "rule_stack", "trace"):
        path = runtime_path(artifacts.get(key, ""))
        if not path.is_file():
            continue
        payload = _read_json(path)
        if key == "context":
            payload = _compact_chapter_context(payload)
        parts.append(json.dumps(payload, ensure_ascii=False))
    observation = record.get("artifacts", {}).get("observation")
    if observation:
        parts.append(
            json.dumps(_read_json(runtime_path(observation)), ensure_ascii=False)
        )
    return "\n".join(parts)


def requires_external_chapter_audit(chapter_id: str, audit_kind: str) -> bool:
    """Every formal project chapter gets a model literary audit."""
    ordinal = int(chapter_id.removeprefix("chapter-"))
    if active_project_id() != "borrowed-heaven":
        return audit_kind in {"initial", "final"}
    return audit_kind == "initial" and ordinal % 5 == 0


def _metric_audit_issues(metrics: dict[str, Any]) -> list[dict[str, str]]:
    issues = []
    severity_by_flag = {
        "transition_word_repetition": "major",
        "rhetorical_template_repetition": "major",
        "sentence_opening_repetition": "minor",
        "abstract_exposition_density": "minor",
        "dash_overuse": "minor",
        "tail_fragmentation_loop": "major",
        "prompt_context_leak": "blocking",
        "generation_meta_leak": "blocking",
        "latin_token_leak": "blocking",
        "termination_token_loop": "blocking",
        "oversized_paragraph_loop": "major",
        "duplicate_text_span": "major",
    }
    fixes = {
        "transition_word_repetition": "Replace explicit transitions with action, spatial change, or consequence.",
        "rhetorical_template_repetition": "Rewrite repeated rhetorical templates as concrete action and choice.",
        "sentence_opening_repetition": "Vary sentence subjects and entry points without changing facts.",
        "abstract_exposition_density": "Ground abstractions in sensory detail, objects, and observable consequence.",
        "dash_overuse": "Replace decorative dashes with sentence rhythm or concrete interruption.",
        "tail_fragmentation_loop": "Collapse the ending into one decisive escalation and stop immediately after the hook.",
        "prompt_context_leak": "Remove all prompt, JSON, asset IDs, rules, and runtime metadata from reader-facing prose.",
        "generation_meta_leak": "Remove completion logs, generation instructions, and model-facing termination text from prose.",
        "latin_token_leak": "Remove accidental Latin-language tokens from Chinese reader-facing prose.",
        "termination_token_loop": "Delete repeated ending tokens and stop at the first complete narrative hook.",
        "oversized_paragraph_loop": "Split or remove the malformed long paragraph while preserving only one causal sequence.",
        "duplicate_text_span": "Remove the duplicated prose span and keep the first coherent occurrence only.",
    }
    for index, flag in enumerate(metrics.get("flags", []), start=1):
        issues.append({
            "issue_id": f"metric-{index:02d}-{flag}",
            "severity": severity_by_flag.get(flag, "minor"),
            "evidence": f"deterministic prose metric flagged {flag}",
            "required_fix": fixes.get(flag, "Review and correct the flagged prose pattern."),
        })
    return issues


def record_deterministic_chapter_audit(chapter_id: str) -> dict[str, Any]:
    """Advance a hash-bound audit using local checks, without an external model call."""
    if active_project_id() != "borrowed-heaven":
        raise RuntimeError(
            "deterministic chapter audit is legacy-only; project chapters require model review"
        )
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] == "draft_generated":
        artifact_kind = "draft"
        is_final = False
    elif record["stage"] == "final_observed":
        artifact_kind = "revision"
        is_final = True
    else:
        raise RuntimeError("chapter must be draft_generated or final_observed before audit")
    prose_path = runtime_path(record["artifacts"][artifact_kind])
    context_path = runtime_path(record["artifacts"]["context"])
    expected = {
        "chapter_id": chapter_id,
        "artifact_kind": artifact_kind,
        "artifact_sha256": _sha256(prose_path),
        "context_sha256": _sha256(context_path),
    }
    metrics = analyze_prose_metrics(prose_path.read_text(encoding="utf-8"))
    issues = _metric_audit_issues(metrics)
    major_issues = [item for item in issues if item["severity"] in {"major", "blocking"}]
    verdict = "REWORK_REQUIRED" if major_issues else "ACCEPT_WITH_WARNINGS" if issues else "ACCEPT"
    payload = {
        **expected,
        "verdict": verdict,
        "dimensions": {
            "canon": ["hash-bound context retained"],
            "character": ["state observation remains mandatory"],
            "state": ["final observation and settlement remain mandatory"],
            "causality": ["story-window irreversible change is bound in context"],
            "pacing": [f"paragraphs={metrics['paragraph_count']}"],
            "life_force": [f"sensory_hits={metrics['sensory_word_hits']}"],
            "anti_ai_taste": list(metrics.get("flags", [])),
            "originality": ["no raw corpus is available to the chapter writer"],
            "semantic_realization": [
                "deterministic audit cannot establish literary realization"
            ],
            "progression_permissions": [
                "deterministic audit cannot establish permission compliance"
            ],
            "history_coherence": [
                "deterministic audit cannot establish historical access timing"
            ],
        },
        "issues": issues,
    }
    if is_final and verdict == "REWORK_REQUIRED":
        return {"valid": False, "errors": ["final deterministic audit requires rework"], "verdict": verdict}
    artifact_key = "final_audit" if is_final else "continuity_audit"
    target_stage = "final_audited" if is_final else "continuity_audited"
    transition = validate_stage_transition(record, target_stage, f"{artifact_key}.json")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/{artifact_key}.json")
    _write_json(target, payload)
    record["artifacts"][artifact_key] = str(target.relative_to(ROOT))
    record["stage"] = target_stage
    _save_registry(registry)
    return {
        "valid": True,
        "chapter_id": chapter_id,
        "stage": target_stage,
        "verdict": verdict,
        "audit_tier": "deterministic",
    }


def _record_audit_attempt(
    chapter_id: str, artifact_key: str, payload: dict[str, Any]
) -> str:
    """Persist non-gating reviewer evidence so a failed external call is diagnosable."""
    target = runtime_path(
        f"system/production_runtime/chapters/{chapter_id}/{artifact_key}.attempt.json"
    )
    _write_json(target, payload)
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "chapter_accepted":
        record["artifacts"][f"{artifact_key}_attempt"] = str(target.relative_to(ROOT))
        _save_registry(registry)
    return str(target.relative_to(ROOT))


def dispatch_chapter_audit(chapter_id: str, model: str | None = None) -> dict[str, Any]:
    packet = build_chapter_audit_packet(chapter_id)
    packet_path = runtime_path(packet["packet_path"])
    artifact_key = "final_audit" if packet.get("audit_kind", "initial") == "final" else "continuity_audit"
    schema_path = runtime_path("system/production_runtime/schemas/continuity_audit.schema.json")
    is_final = packet.get("audit_kind", "initial") == "final"
    reviewer = route_model("reviewer" if is_final else "editor")
    provider = "codex"
    used_model = reviewer["model"]
    errors = []
    try:
        data = ask_codex_structured(
            packet_path.read_text(encoding="utf-8"),
            model=used_model,
            schema_path=schema_path,
            timeout_seconds=600,
        )
    except RuntimeError as error:
        errors.append(f"{used_model}: {error}")
        if is_final and active_project_id() != "borrowed-heaven":
            attempt_path = _record_audit_attempt(
                chapter_id,
                artifact_key,
                {
                    "chapter_id": chapter_id,
                    "audit_kind": "final",
                    "provider": "codex",
                    "model": used_model,
                    "status": "required_sol_provider_failed",
                    "errors": errors,
                },
            )
            return {"valid": False, "errors": errors, "attempt_path": attempt_path}
        provider = "antigravity"
        used_model = model or reviewer["fallback_model"]
        try:
            response_text = ask_antigravity_writer(
                packet_path.read_text(encoding="utf-8"), model=used_model, timeout_seconds=780
            )
            data = extract_json_object(response_text)
        except RuntimeError as fallback_error:
            errors.append(f"{used_model}: {fallback_error}")
            attempt_path = _record_audit_attempt(
                chapter_id,
                artifact_key,
                {
                    "chapter_id": chapter_id,
                    "audit_kind": packet.get("audit_kind", "initial"),
                    "provider": provider,
                    "model": used_model,
                    "status": "provider_failed",
                    "errors": errors,
                },
            )
            return {"valid": False, "errors": errors, "attempt_path": attempt_path}
    try:
        data = normalize_continuity_audit_payload(data)
        jsonschema.validate(data, _read_json(schema_path))
    except jsonschema.ValidationError as error:
        attempt_path = _record_audit_attempt(
            chapter_id,
            artifact_key,
            {
                "chapter_id": chapter_id,
                "audit_kind": packet.get("audit_kind", "initial"),
                "provider": provider,
                "model": used_model,
                "status": "invalid_response",
                "error": str(error),
            },
        )
        return {"valid": False, "errors": [str(error)], "attempt_path": attempt_path}
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    expected = packet["template"]
    evidence = validate_grounded_literary_audit_evidence(
        data,
        _chapter_audit_grounding_text(record, expected["artifact_kind"]),
    )
    if not evidence["valid"]:
        return evidence
    if data["artifact_kind"] != expected["artifact_kind"] or data["artifact_sha256"] != expected["artifact_sha256"] or data["context_sha256"] != expected["context_sha256"]:
        return {"valid": False, "errors": ["audit binding hash mismatch"]}
    if is_final:
        prior_path = runtime_path(
            record.get("artifacts", {}).get("continuity_audit", "")
        )
        prior_audit = _read_json(prior_path) if prior_path.is_file() else {"issues": []}
        closure = validate_final_audit_issue_closure(data, prior_audit)
        if not closure["valid"]:
            return closure
        if any(item.get("severity") in {"blocking", "major"} for item in data.get("issues", [])):
            return {"valid": False, "errors": ["final audit contains unresolved blocking or major issues"], "verdict": data.get("verdict")}
    if is_final and data["verdict"] == "REWORK_REQUIRED":
        return {"valid": False, "errors": ["audit requires rework and cannot advance chapter state"], "verdict": data["verdict"]}
    artifact_key = "final_audit" if is_final else "continuity_audit"
    target_stage = "final_audited" if is_final else "continuity_audited"
    transition = validate_stage_transition(record, target_stage, f"{artifact_key}.json")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/{artifact_key}.json")
    _write_json(target, data)
    audit_sha256 = _sha256_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    execution_target = runtime_path(
        f"system/production_runtime/chapters/{chapter_id}/{artifact_key}.execution.json"
    )
    revision_path = runtime_path(record.get("artifacts", {}).get("revision", ""))
    _write_json(execution_target, {
        "version": "0.27",
        "chapter_id": chapter_id,
        "role": "reviewer" if is_final else "initial_reviewer",
        "artifact": str(target.relative_to(ROOT)),
        "artifact_sha256": audit_sha256,
        "audit_artifact_sha256": audit_sha256,
        "revision_sha256": _sha256(revision_path) if is_final and revision_path.is_file() else None,
        "provider": provider,
        "model": used_model,
        "fallback_used": provider == "antigravity",
    })
    record["artifacts"][artifact_key] = str(target.relative_to(ROOT))
    record["artifacts"][f"{artifact_key}_execution"] = str(execution_target.relative_to(ROOT))
    if is_final:
        record["artifacts"]["reviewer_execution"] = str(execution_target.relative_to(ROOT))
    record["stage"] = target_stage
    _save_registry(registry)
    return {"valid": True, "chapter_id": chapter_id, "stage": record["stage"], "verdict": data["verdict"], "review_provider": provider, "review_model": used_model}


def ingest_chapter_audit(chapter_id: str, file_arg: str) -> dict[str, Any]:
    """Ingest a hash-bound Antigravity audit produced through the CLI bridge."""
    packet = build_chapter_audit_packet(chapter_id)
    source = Path(file_arg)
    if not source.is_absolute():
        source = ROOT / source
    data = normalize_continuity_audit_payload(_read_json(source))
    schema = _read_json(runtime_path("system/production_runtime/schemas/continuity_audit.schema.json"))
    jsonschema.validate(data, schema)
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    evidence = validate_grounded_literary_audit_evidence(
        data,
        _chapter_audit_grounding_text(record, packet["template"]["artifact_kind"]),
    )
    if not evidence["valid"]:
        raise RuntimeError("; ".join(evidence["errors"]))
    expected = packet["template"]
    if (
        data["artifact_kind"] != expected["artifact_kind"]
        or data["artifact_sha256"] != expected["artifact_sha256"]
        or data["context_sha256"] != expected["context_sha256"]
    ):
        raise RuntimeError("audit binding hash mismatch")
    is_final = packet.get("audit_kind", "initial") == "final"
    if is_final:
        prior_path = runtime_path(
            record.get("artifacts", {}).get("continuity_audit", "")
        )
        prior_audit = _read_json(prior_path) if prior_path.is_file() else {"issues": []}
        closure = validate_final_audit_issue_closure(data, prior_audit)
        if not closure["valid"]:
            raise RuntimeError("; ".join(closure["errors"]))
        if any(item.get("severity") in {"blocking", "major"} for item in data.get("issues", [])):
            raise RuntimeError("final audit contains unresolved blocking or major issues")
    if is_final and data["verdict"] == "REWORK_REQUIRED":
        raise RuntimeError("audit requires rework and cannot advance chapter state")
    artifact_key = "final_audit" if is_final else "continuity_audit"
    target_stage = "final_audited" if is_final else "continuity_audited"
    transition = validate_stage_transition(record, target_stage, f"{artifact_key}.json")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/{artifact_key}.json")
    _write_json(target, data)
    record["artifacts"][artifact_key] = str(target.relative_to(ROOT))
    record["stage"] = target_stage
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "verdict": data["verdict"]}


def ingest_chapter_revision(chapter_id: str, file_arg: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "revision_generated", file_arg)
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    prose_gate = validate_prose_entry_gate(chapter_id)
    if not prose_gate["valid"]:
        raise RuntimeError(
            "revision ingest prose gate is blocked: "
            + ", ".join(prose_gate["errors"])
        )
    semantic_integrity = validate_compiled_literary_semantic_context(
        record, chapter_id
    )
    if not semantic_integrity["valid"]:
        raise RuntimeError(
            "compiled literary semantic context is blocked before revision ingest: "
            + "; ".join(semantic_integrity["errors"])
        )
    source = Path(file_arg)
    if not source.is_absolute():
        source = ROOT / source
    if not source.is_file() or not source.read_text(encoding="utf-8").strip():
        raise RuntimeError("revision file is missing or empty")
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/revision.md")
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    metrics_path = target.with_suffix(".metrics.json")
    _write_json(metrics_path, analyze_prose_metrics(target.read_text(encoding="utf-8")))
    record["artifacts"].update(
        {"revision": str(target.relative_to(ROOT)), "revision_metrics": str(metrics_path.relative_to(ROOT))}
    )
    record["stage"] = "revision_generated"
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "revision_sha256": _sha256(target)}


def _audit_requires_revision(audit: dict[str, Any]) -> bool:
    return any(isinstance(issue, dict) for issue in audit.get("issues", []))


def _remove_repeated_suffix_paragraph_block(text: str, *, max_block: int = 6) -> str:
    paragraphs = text.split("\n\n")
    changed = True
    while changed:
        changed = False
        for size in range(min(max_block, len(paragraphs) // 2), 0, -1):
            if paragraphs[-2 * size : -size] == paragraphs[-size:]:
                del paragraphs[-size:]
                changed = True
                break
    return "\n\n".join(paragraphs)


def _issues_are_exact_repetition_only(audit: dict[str, Any]) -> bool:
    issues = [item for item in audit.get("issues", []) if isinstance(item, dict)]
    if not issues:
        return False
    repetition_markers = ("重复", "复述", "duplicate", "repeat")
    removal_markers = ("删除", "去重", "合并", "remove", "delete", "deduplic")
    mixed_semantic_markers = (
        "因果", "动机", "状态", "补足", "新增", "重构", "causal", "motivation",
        "state", "add", "expand", "rewrite",
    )
    return all(
        any(marker in str(issue.get("evidence", "")).lower() for marker in repetition_markers)
        and any(marker in str(issue.get("required_fix", "")).lower() for marker in removal_markers)
        and not any(
            marker in str(issue.get("required_fix", "")).lower()
            for marker in mixed_semantic_markers
        )
        for issue in issues
    )


def _build_revision_generation_prompt(
    base_prompt: str,
    generation: int,
    previous_text: str,
    previous_metrics: dict[str, Any],
) -> str:
    if generation <= 1:
        return base_prompt
    previous_count = int(previous_metrics.get("chinese_character_count", 0))
    return (
        base_prompt
        + "\n\n上一版修订只有 "
        + str(previous_count)
        + " 个中文字符，未达到门禁。请从头完整重写为 3800-4000 个中文字符，"
        "只保留小说正文。必须保留上一版已经修正的单一事件链，并用新的中段行动、"
        "现场阻力、人物反应和可验证后果扩展；不得用追加尾段补字数，必须实际删除或"
        "合并审查指出的重复场景。以下上一版仅作为重写素材，不得原样拼接到原稿末尾：\n"
        + previous_text
    )


def dispatch_chapter_revision(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "continuity_audited":
        raise RuntimeError("chapter must be continuity_audited before revision")
    prose_gate = validate_prose_entry_gate(chapter_id)
    if not prose_gate["valid"]:
        raise RuntimeError(
            "revision prose gate is blocked: " + ", ".join(prose_gate["errors"])
        )
    semantic_integrity = validate_compiled_literary_semantic_context(
        record, chapter_id
    )
    if not semantic_integrity["valid"]:
        raise RuntimeError(
            "compiled literary semantic context is blocked before revision: "
            + "; ".join(semantic_integrity["errors"])
        )
    draft = runtime_path(record["artifacts"]["draft"])
    audit = _read_json(runtime_path(record["artifacts"]["continuity_audit"]))
    if _issues_are_exact_repetition_only(audit):
        draft_text = draft.read_text(encoding="utf-8")
        deduplicated = _remove_repeated_suffix_paragraph_block(draft_text)
        metrics = analyze_prose_metrics(deduplicated)
        if deduplicated != draft_text and not _generated_prose_errors(
            deduplicated, metrics
        ):
            draft_execution_path = runtime_path(
                record.get("artifacts", {}).get("draft_writer_execution", "")
            )
            draft_execution = (
                _read_json(draft_execution_path)
                if draft_execution_path.is_file()
                else {}
            )
            if (
                draft_execution.get("provider") != "codex"
                or draft_execution.get("model") != "gpt-5.6-terra"
            ):
                return {
                    "valid": False,
                    "errors": [
                        "deterministic revision lacks Codex gpt-5.6-terra source execution"
                    ],
                }
            candidate = runtime_path(
                f"system/production_runtime/chapters/{chapter_id}/revision.candidate.md"
            )
            candidate.write_text(deduplicated, encoding="utf-8")
            result = ingest_chapter_revision(chapter_id, str(candidate))
            registry = _load_registry()
            record = _chapter_record(registry, chapter_id)
            revision_path = runtime_path(record["artifacts"]["revision"])
            record["artifacts"]["writer_execution"] = _write_role_execution(
                chapter_id,
                "writer",
                revision_path,
                provider="codex",
                model="gpt-5.6-terra",
                bindings={
                    "source_draft_sha256": _sha256(draft),
                    "deterministic_transform": "remove_repeated_suffix_paragraph_block",
                },
            )
            _save_registry(registry)
            candidate.unlink(missing_ok=True)
            return {
                "valid": True,
                **result,
                "metrics": metrics,
                "writer_model": "gpt-5.6-terra",
                "attempts": [],
                "deterministic_transform": "remove_repeated_suffix_paragraph_block",
            }
    if not _audit_requires_revision(audit):
        draft_execution_path = runtime_path(record.get("artifacts", {}).get("draft_writer_execution", ""))
        draft_execution = _read_json(draft_execution_path) if draft_execution_path.is_file() else {}
        if active_project_id() != "borrowed-heaven" and (
            draft_execution.get("provider") != "codex"
            or draft_execution.get("model") != "gpt-5.6-terra"
        ):
            return {
                "valid": False,
                "errors": ["reused formal draft lacks Codex gpt-5.6-terra writer execution"],
            }
        candidate = runtime_path(f"system/production_runtime/chapters/{chapter_id}/revision.candidate.md")
        candidate.write_text(draft.read_text(encoding="utf-8"), encoding="utf-8")
        result = ingest_chapter_revision(chapter_id, str(candidate))
        candidate.unlink(missing_ok=True)
        registry = _load_registry()
        record = _chapter_record(registry, chapter_id)
        if draft_execution_path.is_file():
            revision_path = runtime_path(record["artifacts"]["revision"])
            record["artifacts"]["writer_execution"] = _write_role_execution(
                chapter_id,
                "writer",
                revision_path,
                provider=str(draft_execution.get("provider", "")),
                model=str(draft_execution.get("model", "")),
                bindings={"source_draft_sha256": draft_execution.get("artifact_sha256")},
            )
            _save_registry(registry)
        return {"valid": True, **result, "reused_draft": True, "writer_model": None, "attempts": []}
    context = _read_json(runtime_path(record["artifacts"]["context"]))
    writer_context = {
        **_compact_chapter_context(context),
        "must_avoid": [
            rule
            for rule in context.get("must_avoid", [])
            if "不得生成章节正文、场景草稿或对话" not in str(rule)
        ],
    }
    prompt = "\n".join(
        [
            f"你已获得 Owner Gate 对 {chapter_id} 的一次性受控正文测试授权。",
            "你是 Novel Research Lab 的 Codex 受控修订写手。直接输出修订后的完整正文，不加标题、确认或说明。",
            "本次授权仅覆盖非正文意图阶段留下的临时正文禁令；其余约束保持生效。",
            "解决审查问题但不得改变章节意图、引入未登记资产或无观察依据的状态变化。",
            "逐项执行审查 issues 中的 required_fix。若问题涉及重复、顺序覆盖或尾段重写，必须先删除或合并原有问题段，再重建一条连续事件链；禁止在原稿末尾追加另一版同义场景来声称修复。",
            "输出前逐项核对每个 issue 的 evidence 已从正文中消失；正文中同一发现、物件交接、人物站位、对白和收束动作只能发生一次。",
            "目标 3600-4000 个中文字符，硬性范围为 3000-4200；不要为求简洁压缩关键行动、感官与后果。减少模板化转折、抽象总结和 AI 腔。",
            "只输出读者正文；禁止工程字段、完成日志、凑字提示、重复结束词、超长粘连段或重复文本块。",
            "审查：", json.dumps(audit, ensure_ascii=False),
            "上下文：", json.dumps(writer_context, ensure_ascii=False),
            "原稿：", draft.read_text(encoding="utf-8"),
        ]
    )
    attempts = []
    text = ""
    metrics: dict[str, Any] = {}
    revision_errors = ["revision was not generated"]
    recovery_path = runtime_path(
        f"system/production_runtime/chapters/{chapter_id}/revision.recovery_candidate.md"
    )
    if recovery_path.is_file():
        text = recovery_path.read_text(encoding="utf-8")
        metrics = analyze_prose_metrics(text)
        revision_errors = _generated_prose_errors(text, metrics)
    for model in (route_model("writer")["model"],):
        for generation in (() if not revision_errors else range(1, 4)):
            revision_prompt = _build_revision_generation_prompt(
                prompt, generation, text, metrics
            )
            try:
                raw_text, provider, used_model = _ask_prose_writer(revision_prompt, model)
                text = _strip_leading_chapter_heading(raw_text)
            except RuntimeError as error:
                attempts.append({"model": model, "generation": generation, "valid": False, "error": str(error)})
                continue
            metrics = analyze_prose_metrics(text)
            revision_errors = _generated_prose_errors(text, metrics)
            attempts.append({
                "model": used_model, "provider": provider, "generation": generation,
                "valid": not revision_errors, "errors": revision_errors,
                "metrics": metrics, "response_preview": text[:500],
            })
            if not revision_errors:
                break
        if not revision_errors:
            break
    if revision_errors:
        if text and not set(metrics.get("flags", [])) & {
            "prompt_context_leak", "generation_meta_leak", "termination_token_loop",
        }:
            recovery_path.write_text(text, encoding="utf-8")
        return {"valid": False, "errors": revision_errors, "metrics": metrics, "attempts": attempts}
    valid_attempt = next(
        (
            item for item in reversed(attempts)
            if item.get("valid") and item.get("provider") and item.get("model")
        ),
        None,
    )
    if active_project_id() != "borrowed-heaven" and (
        valid_attempt is None
        or valid_attempt.get("provider") != "codex"
        or valid_attempt.get("model") != "gpt-5.6-terra"
    ):
        return {
            "valid": False,
            "errors": ["formal revision must be executed by Codex gpt-5.6-terra"],
            "metrics": metrics,
            "attempts": attempts,
        }
    candidate = runtime_path(f"system/production_runtime/chapters/{chapter_id}/revision.candidate.md")
    candidate.write_text(text, encoding="utf-8")
    result = ingest_chapter_revision(chapter_id, str(candidate))
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if valid_attempt is not None:
        revision_path = runtime_path(record["artifacts"]["revision"])
        record["artifacts"]["writer_execution"] = _write_role_execution(
            chapter_id,
            "writer",
            revision_path,
            provider=str(valid_attempt["provider"]),
            model=str(valid_attempt["model"]),
        )
        _save_registry(registry)
    candidate.unlink(missing_ok=True)
    recovery_path.unlink(missing_ok=True)
    return {"valid": True, **result, "metrics": metrics, "writer_model": attempts[-1]["model"], "attempts": attempts}


def settle_chapter_state(chapter_id: str, file_arg: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "state_settled", file_arg)
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    source = Path(file_arg)
    if not source.is_absolute():
        source = ROOT / source
    settlement = _read_json(source)
    jsonschema.validate(
        settlement,
        _read_json(runtime_path("system/production_runtime/schemas/chapter_settlement.schema.json")),
    )
    revision = runtime_path(record["artifacts"]["revision"])
    audit = _read_json(runtime_path(record["artifacts"]["final_audit"]))
    observation = _read_json(runtime_path(record["artifacts"]["observation"]))
    validation = validate_settlement_payload(
        settlement, chapter_id, _sha256(revision), audit, observation=observation
    )
    if not validation["valid"]:
        raise RuntimeError("; ".join(validation["errors"]))
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/settlement.json")
    _write_json(target, settlement)
    record["artifacts"]["settlement"] = str(target.relative_to(ROOT))
    record["stage"] = "state_settled"
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "settlement": record["artifacts"]["settlement"]}


def build_observed_settlement_candidate(chapter_id: str) -> dict[str, Any]:
    """Generate a reviewable settlement using only facts already bound to the draft."""
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "final_audited":
        raise RuntimeError("chapter must be final_audited before settlement candidate generation")
    observation = _read_json(runtime_path(record["artifacts"]["observation"]))
    revision = runtime_path(record["artifacts"]["revision"])
    final_audit = (
        _read_json(runtime_path(record["artifacts"]["final_audit"]))
        if record.get("artifacts", {}).get("final_audit")
        else {"verdict": None}
    )
    initial_audit = (
        _read_json(runtime_path(record["artifacts"]["continuity_audit"]))
        if record.get("artifacts", {}).get("continuity_audit")
        else {"issues": []}
    )
    intent_ref = record.get("artifacts", {}).get("intent")
    expected: dict[tuple[str, str], dict[str, Any]] | None = None
    if intent_ref:
        intent = _read_json(runtime_path(intent_ref))
        expected = {
            (str(item.get("asset_id")), str(item.get("field_path"))): item
            for item in intent.get("expected_state_deltas", [])
            if item.get("asset_id") and item.get("field_path")
        }
    deltas = []
    selected_keys: set[tuple[str, str]] = set()
    for facts in observation.get("facts", {}).values():
        if not isinstance(facts, list):
            continue
        for fact in facts:
            if not isinstance(fact, dict):
                continue
            key = (str(fact.get("asset_id")), str(fact.get("field_path")))
            if expected is not None:
                contract = expected.get(key)
                if (
                    contract is None
                    or fact.get("before") != contract.get("before")
                    or fact.get("after") != contract.get("after")
                    or key in selected_keys
                ):
                    continue
                selected_keys.add(key)
            deltas.append(
                {
                    "fact_id": fact["fact_id"],
                    "asset_id": fact["asset_id"],
                    "field_path": fact["field_path"],
                    "operation": "set",
                    "before": fact.get("before"),
                    "after": fact.get("after"),
                }
            )
    candidate = {
        "chapter_id": chapter_id,
        "accepted_revision_sha256": _sha256(revision),
        "state_deltas": deltas,
        "resolved_audit_ids": list(final_audit.get("resolved_prior_issue_ids", []))
        if final_audit.get("verdict") in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
        else [],
    }
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/settlement.candidate.json")
    _write_json(target, candidate)
    return {"chapter_id": chapter_id, "candidate": str(target.relative_to(ROOT)), "state_delta_count": len(deltas)}


def run_controlled_chapter_pipeline(
    intent_file: str, *, audit_model: str | None = None
) -> dict[str, Any]:
    """Advance exactly one authorized chapter through every recoverable gate."""
    source = Path(intent_file)
    if not source.is_absolute():
        source = ROOT / source
    intent = _read_json(source)
    chapter_id = str(intent["chapter_id"])
    completed: list[str] = []

    registry = _load_registry()
    record = next((item for item in registry["chapters"] if item["chapter_id"] == chapter_id), None)
    if record is None:
        initialize_chapter(str(source))
        completed.append("chapter_intent")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "chapter_intent":
        compile_chapter_context(chapter_id)
        completed.append("context_compiled")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "context_compiled":
        result = dispatch_chapter_draft(chapter_id)
        if not result["valid"]:
            return {"valid": False, "chapter_id": chapter_id, "completed": completed, "errors": result.get("errors", [])}
        completed.append("draft_generated")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "draft_generated":
        result = (
            dispatch_chapter_audit(chapter_id, model=audit_model)
            if requires_external_chapter_audit(chapter_id, "initial")
            else record_deterministic_chapter_audit(chapter_id)
        )
        if not result["valid"]:
            return {"valid": False, "chapter_id": chapter_id, "completed": completed, "errors": result.get("errors", [])}
        completed.append("continuity_audited")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "continuity_audited":
        result = dispatch_chapter_revision(chapter_id)
        if not result["valid"]:
            return {"valid": False, "chapter_id": chapter_id, "completed": completed, "errors": result.get("errors", [])}
        completed.append("revision_generated")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "revision_generated":
        if active_project_id() != "borrowed-heaven":
            dispatch_chapter_observation(chapter_id)
        else:
            bundled = ingest_bundled_observation(chapter_id)
            if not bundled["valid"]:
                dispatch_chapter_observation(chapter_id)
        completed.append("final_observed")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "final_observed":
        result = (
            dispatch_chapter_audit(chapter_id, model=audit_model)
            if requires_external_chapter_audit(chapter_id, "final")
            else record_deterministic_chapter_audit(chapter_id)
        )
        if not result["valid"]:
            return {"valid": False, "chapter_id": chapter_id, "completed": completed, "errors": result.get("errors", [])}
        completed.append("final_audited")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "final_audited":
        candidate = build_observed_settlement_candidate(chapter_id)
        settle_chapter_state(chapter_id, candidate["candidate"])
        completed.append("state_settled")
        record = _chapter_record(_load_registry(), chapter_id)
    if record["stage"] == "state_settled":
        accept_chapter(chapter_id)
        completed.append("chapter_accepted")
        record = _chapter_record(_load_registry(), chapter_id)
    return {
        "valid": record["stage"] == "chapter_accepted",
        "chapter_id": chapter_id,
        "stage": record["stage"],
        "completed": completed,
    }


def accept_chapter(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    prose_gate = validate_prose_entry_gate(chapter_id)
    if not prose_gate["valid"]:
        raise RuntimeError(
            "acceptance prose gate is blocked: "
            + ", ".join(prose_gate["errors"])
        )
    semantic_integrity = validate_compiled_literary_semantic_context(
        record, chapter_id
    )
    if not semantic_integrity["valid"]:
        raise RuntimeError(
            "compiled literary semantic context is blocked before acceptance: "
            + "; ".join(semantic_integrity["errors"])
        )
    revision = runtime_path(record.get("artifacts", {}).get("revision", ""))
    settlement_path = runtime_path(record.get("artifacts", {}).get("settlement", ""))
    settlement = _read_json(settlement_path) if settlement_path.is_file() else {}
    validation = validate_acceptance(record, settlement, _sha256(revision) if revision.is_file() else "")
    if active_project_id() != "borrowed-heaven":
        final_audit_path = runtime_path(record.get("artifacts", {}).get("final_audit", ""))
        execution_path = runtime_path(record.get("artifacts", {}).get("final_audit_execution", ""))
        if not final_audit_path.is_file() or not execution_path.is_file():
            validation["errors"].append("project acceptance requires semantic final audit and execution evidence")
        else:
            final_audit = _read_json(final_audit_path)
            evidence = validate_grounded_literary_audit_evidence(
                final_audit,
                _chapter_audit_grounding_text(record, "revision"),
            )
            validation["errors"].extend(evidence["errors"])
            if (
                final_audit.get("artifact_kind") != "revision"
                or final_audit.get("artifact_sha256") != _sha256(revision)
                or final_audit.get("verdict") not in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
                or any(item.get("severity") in {"blocking", "major"} for item in final_audit.get("issues", []))
            ):
                validation["errors"].append("semantic final audit is stale or contains unresolved substantive issues")
            for role, path in (
                ("writer", revision),
                ("observer", runtime_path(record.get("artifacts", {}).get("observation", ""))),
                ("reviewer", final_audit_path),
            ):
                evidence = validate_role_execution(record, role, path)
                validation["errors"].extend(evidence["errors"])
        validation["valid"] = not validation["errors"]
    if not validation["valid"]:
        raise RuntimeError("; ".join(validation["errors"]))
    manifest = {
        "version": VERSION,
        "chapter_id": chapter_id,
        "revision_sha256": _sha256(revision),
        "settlement_sha256": _sha256(settlement_path),
        "source_hashes": record["source_hashes"],
    }
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/acceptance.json")
    _write_json(target, manifest)
    record["artifacts"]["acceptance"] = str(target.relative_to(ROOT))
    record["stage"] = "chapter_accepted"
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "acceptance": record["artifacts"]["acceptance"]}


def _has_bounded_chapter_scope(
    decisions: list[dict[str, Any]], decision_type: str, scope_prefix: str, chapter_id: str
) -> bool:
    """Authorize a concrete chapter only; legacy generic scopes remain Chapter 1-only."""
    chapter_scope = f"{scope_prefix}:{chapter_id}"
    return any(
        item.get("decision_type") == decision_type
        and _legacy_authorization_binding_valid(item)
        and (
            chapter_scope in item.get("authorized_scope", [])
            or (
                chapter_id == "chapter-0001"
                and scope_prefix in item.get("authorized_scope", [])
            )
        )
        for item in decisions
    )


def has_bounded_prose_authorization(
    decisions: list[dict[str, Any]], chapter_id: str = "chapter-0001"
) -> bool:
    """Keep the prose gate independent from asset and reconciliation approvals."""
    if active_project_id() != "borrowed-heaven":
        return _has_project_volume1_scope(
            decisions, "authorize_controlled_prose_test", chapter_id
        )
    return _has_bounded_chapter_scope(
        decisions, "authorize_controlled_prose_test", "bounded_chapter_runtime_v0.20", chapter_id
    ) or _has_longform_cluster1_scope(decisions, "authorize_controlled_prose_test", chapter_id)


def has_bounded_intent_authorization(
    decisions: list[dict[str, Any]], chapter_id: str = "chapter-0001"
) -> bool:
    """Intent creation is non-prose and has its own chapter-bound Owner scope."""
    if active_project_id() != "borrowed-heaven":
        return _has_project_volume1_scope(decisions, "authorize_next_phase", chapter_id)
    return _has_bounded_chapter_scope(
        decisions, "authorize_next_phase", "bounded_chapter_intent_v0.20", chapter_id
    ) or _has_longform_cluster1_scope(decisions, "authorize_next_phase", chapter_id)


def _has_longform_cluster1_scope(
    decisions: list[dict[str, Any]], decision_type: str, chapter_id: str
) -> bool:
    try:
        ordinal = int(chapter_id.removeprefix("chapter-"))
    except ValueError:
        return False
    scope_ranges = (
        ("longform_cluster1_v024", 1, 10),
        ("longform_volume1_v025", 1, 100),
    )
    return any(
        start <= ordinal <= end
        and item.get("decision_type") == decision_type
        and _legacy_authorization_binding_valid(item)
        and f"{prefix}:{chapter_id}" in item.get("authorized_scope", [])
        for prefix, start, end in scope_ranges
        for item in decisions
    )


def _legacy_authorization_binding_valid(decision: dict[str, Any]) -> bool:
    """Retire pre-v0.29 unbound Borrowed Heaven authorizations."""
    if not CANONICAL_BASELINE_PATH.is_file():
        return False
    return (
        decision.get("project_id") == "borrowed-heaven"
        and decision.get("authorization_contract_version") == "0.29"
        and decision.get("bound_baseline_sha256")
        == _sha256(CANONICAL_BASELINE_PATH)
        and {
            "borrowed-heaven:raw-corpus-read",
            "borrowed-heaven:publish",
        }
        <= set(decision.get("forbidden_scope", []))
    )


def _has_project_volume1_scope(
    decisions: list[dict[str, Any]], decision_type: str, chapter_id: str
) -> bool:
    """Require project identity, current baseline, dual review, and one chapter scope."""
    try:
        ordinal = int(chapter_id.removeprefix("chapter-"))
    except ValueError:
        return False
    window = next(
        (
            (start, end)
            for start, end in volume1_windows(active_project_id())
            if start <= ordinal <= end
        ),
        None,
    )
    if window is None:
        return False
    start, end = window
    project_id = active_project_id()
    baseline_path = project_workspace(project_id) / "creation_assets/canonical_baseline.json"
    if not baseline_path.is_file():
        return False
    baseline_sha = _sha256(baseline_path)
    review_index_path = project_workspace(project_id) / "production_runtime/production_readiness/final-review-index.v0.1.json"
    if not review_index_path.is_file():
        return False
    review_index = _read_json(review_index_path)
    if (
        review_index.get("valid") is not True
        or review_index.get("bound_baseline_sha256") != baseline_sha
        or review_index.get("sol_verdict") != "ACCEPT"
    ):
        return False
    sol_path = ROOT / str(review_index.get("sol_review_path", ""))
    independent = resolve_independent_review_binding(review_index, baseline_sha)
    if not sol_path.is_file() or independent is None:
        return False
    sol_sha = _sha256(sol_path)
    if (
        review_index.get("sol_review_sha256") != sol_sha
    ):
        return False
    required_forbidden = {
        f"{project_id}:outside-window-{start:03d}-{end:03d}",
        f"{project_id}:bulk-or-continuous-production",
        f"{project_id}:raw-corpus-read",
        f"{project_id}:publish",
    }
    scope = f"project_volume1_v1:{project_id}:{chapter_id}"
    return any(
        item.get("decision_type") == decision_type
        and item.get("project_id") == project_id
        and scope in item.get("authorized_scope", [])
        and required_forbidden <= set(item.get("forbidden_scope", []))
        and item.get("expires_after_mission")
        == f"{project_id}-volume1-window-{start:03d}-{end:03d}-v1"
        and item.get("bound_baseline_sha256") == baseline_sha
        and item.get("bound_sol_review_sha256") == sol_sha
        and item.get("bound_independent_review_sha256")
        == independent["sha256"]
        and item.get("bound_independent_review_provider")
        == independent["provider"]
        and item.get("bound_independent_review_model")
        == independent["model"]
        for item in decisions
    )


def _next_project_production_chapter_id() -> str:
    workspace = project_workspace()
    registry_path = workspace / "production_runtime/chapter_registry.v0.20.json"
    registry = _read_json(registry_path) if registry_path.is_file() else {"chapters": []}
    records = {
        str(item.get("chapter_id")): item
        for item in registry.get("chapters", [])
    }
    count = volume1_chapter_count(active_project_id())
    for ordinal in range(1, count + 1):
        chapter_id = f"chapter-{ordinal:04d}"
        record = records.get(chapter_id)
        if record is None or record.get("stage") != "chapter_accepted":
            return chapter_id
    return f"chapter-{count:04d}"


def build_production_readiness(chapter_id: str | None = None) -> dict[str, Any]:
    if active_project_id() != "borrowed-heaven":
        target_chapter_id = chapter_id or _next_project_production_chapter_id()
        target_ordinal = int(target_chapter_id.removeprefix("chapter-"))
        target_window = next(
            (
                (start, end)
                for start, end in volume1_windows(active_project_id())
                if start <= target_ordinal <= end
            ),
            None,
        )
        project = active_project()
        validation = validate_project_production()
        workspace = project_workspace()
        review_index_path = workspace / "production_runtime/production_readiness/final-review-index.v0.1.json"
        review_index = _read_json(review_index_path) if review_index_path.is_file() else {}
        baseline_path = workspace / "creation_assets/canonical_baseline.json"
        baseline_sha = _sha256(baseline_path) if baseline_path.is_file() else None
        sol_path = ROOT / str(review_index.get("sol_review_path", ""))
        independent = (
            resolve_independent_review_binding(review_index, baseline_sha)
            if baseline_sha
            else None
        )
        dual_review = bool(
            review_index.get("valid") is True
            and review_index.get("sol_verdict") == "ACCEPT"
            and review_index.get("bound_baseline_sha256") == baseline_sha
            and sol_path.is_file()
            and review_index.get("sol_review_sha256") == _sha256(sol_path)
            and independent is not None
        )
        decisions = load_decisions()
        checks = {
            "project_production_contract_valid": validation.get("valid") is True,
            "dual_final_review_accepted": dual_review,
            "project_content_authorized": bool(project.get("content_authorized")),
            "bounded_intent_authorized": has_bounded_intent_authorization(
                decisions, target_chapter_id
            ),
            "bounded_prose_authorized": has_bounded_prose_authorization(
                decisions, target_chapter_id
            ),
        }
        ready = all(checks.values())
        window_label = (
            f"{target_window[0]:03d}_{target_window[1]:03d}"
            if target_window
            else "outside_volume"
        )
        return {
            "version": VERSION,
            "project_id": active_project_id(),
            "target_chapter_id": target_chapter_id,
            "target_window": list(target_window) if target_window else None,
            "status": (
                f"ready_for_formal_window_{window_label}"
                if ready
                else "blocked_before_formal_prose"
            ),
            "ready": ready,
            "bounded_intent_ready": validation.get("valid") is True and dual_review,
            "checks": checks,
            "canonical_inputs": validation.get("canonical_inputs", []),
            "schema_checks": [],
            "stage_order": list(STAGES),
            "blocked_actions": [] if ready else ["generate_chapter_draft", "bulk_prose", "publish"],
            "next_action": (
                f"Initialize formal {target_chapter_id} intent."
                if ready
                else (
                    "Complete project-isolated final review and bounded Owner "
                    f"authorization for {target_chapter_id}."
                )
            ),
            "validation_errors": validation.get("errors", []),
        }
    deep_read = build_deep_read_status()
    if PROJECT_RECONCILIATION_VALIDATION.exists():
        reconciliation = _read_json(PROJECT_RECONCILIATION_VALIDATION)
    else:
        reconciliation = {"valid": False, "verdict": None}
    application = (
        _read_json(PROJECT_RECONCILIATION_APPLICATION)
        if PROJECT_RECONCILIATION_APPLICATION.exists()
        else {}
    )
    canonical_baseline = _read_json(CANONICAL_BASELINE_PATH) if CANONICAL_BASELINE_PATH.exists() else {}
    store = validate_creation_asset_store()
    canonical = []
    for relative in CANONICAL_INPUTS:
        path = runtime_path(relative)
        canonical.append(
            {
                "path": relative,
                "exists": path.exists(),
                "sha256": _sha256(path) if path.exists() else None,
            }
        )
    schema_checks = []
    for relative in RUNTIME_SCHEMAS:
        path = runtime_path(relative)
        valid = False
        error = None
        if path.exists():
            try:
                jsonschema.Draft7Validator.check_schema(_read_json(path))
                valid = True
            except jsonschema.SchemaError as exc:
                error = exc.message
        schema_checks.append({"path": relative, "valid": valid, "error": error})
    decisions = load_decisions()
    asset_store_path = runtime_path("system/creation_assets/project_assets.v0.2.json")
    current_asset_sha = _sha256(asset_store_path) if asset_store_path.exists() else None
    baseline_asset_sha = next(
        (
            item.get("sha256")
            for item in canonical_baseline.get("canonical_inputs", [])
            if item.get("path") == "system/creation_assets/project_assets.v0.2.json"
        ),
        None,
    )
    reconciliation_chain_continues = bool(
        application.get("status") == "applied"
        and (
            current_asset_sha is not None
            and (
                application.get("resulting_asset_store_sha256") == current_asset_sha
                or baseline_asset_sha == current_asset_sha
            )
        )
    )
    checks = {
        "deep_read_verified": bool(deep_read["deep_read_verified"]),
        "project_reconciliation_accepted": bool(
            reconciliation.get("valid")
            and reconciliation.get("verdict") in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
        ),
        "project_reconciliation_applied": reconciliation_chain_continues,
        "creation_assets_valid": bool(store["valid"]),
        "canonical_inputs_locked": all(item["exists"] and item["sha256"] for item in canonical),
        "chapter_runtime_contract_ready": all(item["valid"] for item in schema_checks),
        "bounded_intent_authorized": has_bounded_intent_authorization(decisions),
        "bounded_prose_authorized": has_bounded_prose_authorization(decisions),
    }
    ready = all(checks.values())
    bounded_intent_ready = all(
        value for key, value in checks.items() if key != "bounded_prose_authorized"
    )
    return {
        "version": VERSION,
        "status": (
            "ready_for_bounded_chapter_runtime"
            if ready
            else "ready_for_bounded_intent"
            if bounded_intent_ready
            else "blocked_before_prose"
        ),
        "ready": ready,
        "bounded_intent_ready": bounded_intent_ready,
        "checks": checks,
        "canonical_inputs": canonical,
        "schema_checks": schema_checks,
        "stage_order": list(STAGES),
        "blocked_actions": [] if ready else ["generate_chapter_draft", "run_codex_direct_writer", "bulk_prose"],
        "next_action": (
            "Create a bounded Chapter 1 intent."
            if ready
            else (
                "Create and validate a non-prose Chapter 1 intent."
                if bounded_intent_ready
                else "Record an Owner authorization for bounded Chapter 1 intent."
                if all(
                    value
                    for key, value in checks.items()
                    if key not in {"bounded_intent_authorized", "bounded_prose_authorized"}
                )
                else "Complete v0.18 deep reading and v0.19 project reconciliation."
            )
        ),
    }


def load_chapter_runtime_status() -> dict[str, Any]:
    if REGISTRY_PATH.exists():
        registry = _read_json(REGISTRY_PATH)
    else:
        registry = {
            "version": "0.20",
            "project_id": active_project_id(),
            "project": active_project_title(),
            "chapters": [],
        }
    return {
        "version": VERSION,
        "readiness": build_production_readiness(),
        "registry_path": str(REGISTRY_PATH.relative_to(ROOT)),
        "chapter_count": len(registry.get("chapters", [])),
        "chapters": registry.get("chapters", []),
        "stage_order": list(STAGES),
    }
