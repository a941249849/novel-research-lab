from __future__ import annotations

import hashlib
import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from nrl_creation_schemas import validate_creation_asset_store
from nrl_deep_read import build_deep_read_status
from nrl_paths import ROOT, runtime_path


VERSION = "0.20"
STAGES = (
    "chapter_intent",
    "context_compiled",
    "draft_generated",
    "facts_observed",
    "continuity_audited",
    "revision_generated",
    "state_settled",
    "chapter_accepted",
)
REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")
PROJECT_RECONCILIATION_VALIDATION = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json"
)
CANONICAL_INPUTS = (
    "phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md",
    "phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md",
    "system/creation_assets/project_assets.v0.2.json",
)
RUNTIME_SCHEMAS = (
    "system/production_runtime/schemas/chapter_intent.schema.json",
    "system/production_runtime/schemas/chapter_observation.schema.json",
    "system/production_runtime/schemas/chapter_settlement.schema.json",
    "system/production_runtime/schemas/chapter_registry.schema.json",
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


def analyze_prose_metrics(text: str) -> dict[str, Any]:
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    sentences = [item.strip() for item in re.split(r"[。！？!?]", text) if item.strip()]
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    sentence_lengths = [len(re.findall(r"[\u4e00-\u9fff]", item)) for item in sentences]
    paragraph_lengths = [len(re.findall(r"[\u4e00-\u9fff]", item)) for item in paragraphs]
    starters = [sentence[:2] for sentence in sentences if len(sentence) >= 2]
    starter_counts = Counter(starters)
    repeated_starters = [
        {"starter": starter, "count": count}
        for starter, count in starter_counts.most_common()
        if count >= 3
    ]
    transition_hits = sum(text.count(word) for word in TRANSITION_WORDS)
    rhetorical_hits = sum(len(pattern.findall(text)) for pattern in RHETORICAL_PATTERNS)
    abstract_hits = sum(text.count(word) for word in ABSTRACT_WORDS)
    sensory_hits = sum(text.count(word) for word in SENSORY_WORDS)
    quote_chars = sum(len(match) for match in re.findall(r"[“\"](.*?)[”\"]", text, re.DOTALL))
    count = len(chinese_chars)
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
        "flags": flags,
        "policy": "metrics_are_audit_evidence_not_a_literary_verdict",
    }


def compile_chapter_context_payload(
    intent: dict[str, Any],
    assets: list[dict[str, Any]],
    canonical_hashes: dict[str, str],
    prior_settlements: list[dict[str, Any]],
) -> dict[str, Any]:
    asset_map = {
        str(asset.get("asset_id")): asset
        for asset in assets
        if isinstance(asset, dict) and asset.get("asset_id")
    }
    requested = [str(item) for item in intent.get("required_asset_ids", [])]
    missing = [asset_id for asset_id in requested if asset_id not in asset_map]
    if missing:
        return {"valid": False, "errors": [f"missing required assets: {', '.join(missing)}"]}
    selected = [asset_map[asset_id] for asset_id in requested]
    context = {
        "version": VERSION,
        "chapter_id": intent.get("chapter_id"),
        "dramatic_purpose": intent.get("dramatic_purpose"),
        "must_keep": list(intent.get("must_keep", [])),
        "must_avoid": list(intent.get("must_avoid", [])),
        "scene_constraints": list(intent.get("scene_constraints", [])),
        "active_hook_ids": list(intent.get("active_hook_ids", [])),
        "assets": selected,
        "prior_settlements": prior_settlements,
        "canonical_hashes": canonical_hashes,
    }
    trace = {
        "version": VERSION,
        "chapter_id": intent.get("chapter_id"),
        "selected_asset_ids": requested,
        "excluded_asset_count": len(asset_map) - len(selected),
        "selection_reason": "explicit chapter intent requirements",
        "canonical_hashes": canonical_hashes,
        "prior_settlement_count": len(prior_settlements),
    }
    rule_stack = {
        "version": VERSION,
        "chapter_id": intent.get("chapter_id"),
        "priority_order": [
            "safety_and_originality",
            "canonical_story_bible",
            "volume_outline",
            "accepted_state_settlements",
            "creation_asset_constraints",
            "chapter_must_keep_and_must_avoid",
            "anti_ai_style_evidence",
        ],
        "hard_rules": [
            "no source-work names, scenes, signature systems, or prose imitation",
            "no untracked power, relationship, location, item, or timeline changes",
            "all benefits carry an embodied, relational, or systemic cost",
            "reader-facing prose contains no runtime or database vocabulary",
            *[str(item) for item in intent.get("must_avoid", [])],
        ],
        "chapter_rules": [str(item) for item in intent.get("must_keep", [])],
        "scene_constraints": [str(item) for item in intent.get("scene_constraints", [])],
    }
    return {"valid": True, "errors": [], "context": context, "trace": trace, "rule_stack": rule_stack}


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_registry() -> dict[str, Any]:
    return _read_json(REGISTRY_PATH) if REGISTRY_PATH.exists() else {
        "version": VERSION, "project": "《借天改命账》", "chapters": []
    }


def _save_registry(registry: dict[str, Any]) -> None:
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_registry.schema.json"))
    jsonschema.validate(registry, schema)
    _write_json(REGISTRY_PATH, registry)


def initialize_chapter(intent_file: str) -> dict[str, Any]:
    readiness = build_production_readiness()
    if not readiness["ready"]:
        raise RuntimeError("production readiness gate is blocked")
    source = Path(intent_file)
    if not source.is_absolute():
        source = ROOT / source
    intent = _read_json(source)
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_intent.schema.json"))
    jsonschema.validate(intent, schema)
    registry = _load_registry()
    chapter_id = str(intent["chapter_id"])
    if any(item.get("chapter_id") == chapter_id for item in registry["chapters"]):
        raise RuntimeError(f"chapter already exists: {chapter_id}")
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
    transition = validate_stage_transition(record, "context_compiled", "context.json")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    intent = _read_json(runtime_path(record["artifacts"]["intent"]))
    store = _read_json(runtime_path("system/creation_assets/project_assets.v0.2.json"))
    prior = []
    for item in registry["chapters"]:
        settlement_path = item.get("artifacts", {}).get("settlement")
        if settlement_path:
            prior.append(_read_json(runtime_path(settlement_path)))
    compiled = compile_chapter_context_payload(intent, store.get("assets", []), record["source_hashes"], prior)
    if not compiled["valid"]:
        raise RuntimeError("; ".join(compiled["errors"]))
    chapter_dir = runtime_path(f"system/production_runtime/chapters/{chapter_id}")
    paths = {
        "context": chapter_dir / "context.json",
        "rule_stack": chapter_dir / "rule_stack.json",
        "trace": chapter_dir / "trace.json",
    }
    for key, path in paths.items():
        _write_json(path, compiled[key])
        record["artifacts"][key] = str(path.relative_to(ROOT))
    record["stage"] = "context_compiled"
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "artifacts": record["artifacts"]}


def build_production_readiness() -> dict[str, Any]:
    deep_read = build_deep_read_status()
    if PROJECT_RECONCILIATION_VALIDATION.exists():
        reconciliation = _read_json(PROJECT_RECONCILIATION_VALIDATION)
    else:
        reconciliation = {"valid": False, "verdict": None}
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
    checks = {
        "deep_read_verified": bool(deep_read["deep_read_verified"]),
        "project_reconciliation_accepted": bool(
            reconciliation.get("valid")
            and reconciliation.get("verdict") in {"ACCEPT", "ACCEPT_WITH_WARNINGS"}
        ),
        "creation_assets_valid": bool(store["valid"]),
        "canonical_inputs_locked": all(item["exists"] and item["sha256"] for item in canonical),
        "chapter_runtime_contract_ready": all(item["valid"] for item in schema_checks),
    }
    ready = all(checks.values())
    return {
        "version": VERSION,
        "status": "ready_for_bounded_chapter_runtime" if ready else "blocked_before_prose",
        "ready": ready,
        "checks": checks,
        "canonical_inputs": canonical,
        "schema_checks": schema_checks,
        "stage_order": list(STAGES),
        "blocked_actions": [] if ready else ["generate_chapter_draft", "run_hermes_writer", "bulk_prose"],
        "next_action": (
            "Create a bounded Chapter 1 intent."
            if ready
            else "Complete v0.18 deep reading and v0.19 project reconciliation."
        ),
    }


def load_chapter_runtime_status() -> dict[str, Any]:
    if REGISTRY_PATH.exists():
        registry = _read_json(REGISTRY_PATH)
    else:
        registry = {"version": VERSION, "project": "《借天改命账》", "chapters": []}
    return {
        "version": VERSION,
        "readiness": build_production_readiness(),
        "registry_path": str(REGISTRY_PATH.relative_to(ROOT)),
        "chapter_count": len(registry.get("chapters", [])),
        "chapters": registry.get("chapters", []),
        "stage_order": list(STAGES),
    }
