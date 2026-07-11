from __future__ import annotations

import hashlib
import json
import re
import shutil
import statistics
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from nrl_creation_schemas import validate_creation_asset_store
from nrl_antigravity_bridge import find_agy_binary
from nrl_deep_read import build_deep_read_status
from nrl_hermes_bridge import ask_hermes
from nrl_paths import ROOT, runtime_path


VERSION = "0.20"
STAGES = (
    "chapter_intent",
    "context_compiled",
    "draft_generated",
    "facts_observed",
    "continuity_audited",
    "revision_generated",
    "revision_audited",
    "state_settled",
    "chapter_accepted",
)
REGISTRY_PATH = runtime_path("system/production_runtime/chapter_registry.v0.20.json")
PROJECT_RECONCILIATION_VALIDATION = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_v0.19.json"
)
PROJECT_RECONCILIATION_APPLICATION = runtime_path(
    "system/agent_ops/validation/borrowed_heaven_project_reconciliation_application_v0.19.json"
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
        if issue.get("severity") == "blocking"
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
        for delta in settlement.get("state_deltas", []):
            fact = observed.get(str(delta.get("fact_id")))
            comparable = ("asset_id", "field_path", "before", "after")
            if not fact or any(delta.get(key) != fact.get(key) for key in comparable):
                errors.append(f"state delta does not match observed fact: {delta.get('fact_id')}")
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
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


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
    transition = validate_stage_transition(record, "context_compiled", "context.json")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    intent = _read_json(runtime_path(record["artifacts"]["intent"]))
    store = _read_json(runtime_path("system/creation_assets/project_assets.v0.2.json"))
    prior = []
    chapter_ordinal = int(chapter_id.removeprefix("chapter-"))
    for item in registry["chapters"]:
        settlement_path = item.get("artifacts", {}).get("settlement")
        item_ordinal = int(str(item["chapter_id"]).removeprefix("chapter-"))
        if settlement_path and item.get("stage") == "chapter_accepted" and item_ordinal < chapter_ordinal:
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


def _chapter_record(registry: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    record = next((item for item in registry["chapters"] if item["chapter_id"] == chapter_id), None)
    if not record:
        raise RuntimeError(f"unknown chapter: {chapter_id}")
    return record


def build_chapter_writer_prompt(chapter_id: str) -> str:
    readiness = build_production_readiness()
    if not readiness["ready"]:
        raise RuntimeError("production readiness gate is blocked")
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "context_compiled":
        raise RuntimeError("chapter must be context_compiled before writing")
    context = _read_json(runtime_path(record["artifacts"]["context"]))
    rules = _read_json(runtime_path(record["artifacts"]["rule_stack"]))
    return "\n".join(
        [
            "你是 Novel Research Lab 的 Hermes 正文写手。只输出本章正文，不加标题和说明。",
            "目标 2600-4200 个中文字符。严格服从上下文与规则栈；不得引入未登记资产或状态变化。",
            "避免工整段落、总结句、抽象议论堆叠、重复转折词和‘不是因为…而是因为…’模板。",
            "抽象机制必须落成动作、感官、物件、关系选择和后果。",
            "",
            "上下文：",
            json.dumps(context, ensure_ascii=False),
            "",
            "规则栈：",
            json.dumps(rules, ensure_ascii=False),
        ]
    )


def dispatch_chapter_draft(chapter_id: str) -> dict[str, Any]:
    prompt = build_chapter_writer_prompt(chapter_id)
    text = ask_hermes(prompt)
    metrics = analyze_prose_metrics(text)
    errors = []
    if not 2600 <= metrics["chinese_character_count"] <= 4200:
        errors.append("draft must contain 2600-4200 Chinese characters")
    if re.search(r"(?m)^\s*#|第.{0,8}章", text):
        errors.append("draft must not contain a chapter heading")
    if errors:
        return {"valid": False, "errors": errors, "metrics": metrics}
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "draft_generated", "draft.md")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    chapter_dir = runtime_path(f"system/production_runtime/chapters/{chapter_id}")
    draft_path = chapter_dir / "draft.md"
    metrics_path = chapter_dir / "draft.metrics.json"
    draft_path.write_text(text, encoding="utf-8")
    _write_json(metrics_path, metrics)
    record["artifacts"].update({"draft": str(draft_path.relative_to(ROOT)), "draft_metrics": str(metrics_path.relative_to(ROOT))})
    record["stage"] = "draft_generated"
    _save_registry(registry)
    return {"valid": True, "chapter_id": chapter_id, "stage": record["stage"], "metrics": metrics}


def ingest_chapter_observation(chapter_id: str, file_arg: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "facts_observed", file_arg)
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    source = Path(file_arg)
    if not source.is_absolute():
        source = ROOT / source
    observation = _read_json(source)
    schema = _read_json(runtime_path("system/production_runtime/schemas/chapter_observation.schema.json"))
    jsonschema.validate(observation, schema)
    draft_path = runtime_path(record["artifacts"]["draft"])
    if observation["chapter_id"] != chapter_id or observation["draft_sha256"] != _sha256(draft_path):
        raise RuntimeError("observation is stale or bound to another draft")
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/observation.json")
    _write_json(target, observation)
    record["artifacts"]["observation"] = str(target.relative_to(ROOT))
    record["stage"] = "facts_observed"
    _save_registry(registry)
    return {"chapter_id": chapter_id, "stage": record["stage"], "observation": record["artifacts"]["observation"]}


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


def dispatch_chapter_observation(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "draft_generated":
        raise RuntimeError("chapter must be draft_generated before observation")
    binary = shutil.which("codex")
    if not binary:
        raise RuntimeError("codex CLI is missing")
    draft = runtime_path(record["artifacts"]["draft"])
    context = _read_json(runtime_path(record["artifacts"]["context"]))
    prompt = build_observer_prompt_payload(
        chapter_id, _sha256(draft), draft.read_text(encoding="utf-8"), context
    )
    output = runtime_path(f"system/production_runtime/chapters/{chapter_id}/observation.candidate.json")
    schema = runtime_path("system/production_runtime/schemas/chapter_observation.schema.json")
    result = subprocess.run(
        [
            binary, "--ask-for-approval", "never", "exec", "--ephemeral",
            "--sandbox", "read-only", "-m", "gpt-5.6-terra",
            "--output-schema", str(schema), "-o", str(output), prompt,
        ],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0 or not output.is_file():
        output.unlink(missing_ok=True)
        raise RuntimeError(f"Codex observer failed: {result.stderr.strip()}")
    ingested = ingest_chapter_observation(chapter_id, str(output))
    output.unlink(missing_ok=True)
    return {**ingested, "observer_model": "gpt-5.6-terra"}


def build_chapter_audit_packet(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] == "facts_observed":
        artifact_kind = "draft"
    elif record["stage"] == "revision_generated":
        artifact_kind = "revision"
    else:
        raise RuntimeError("chapter must be facts_observed or revision_generated before audit")
    prose_path = runtime_path(record["artifacts"][artifact_kind])
    context_path = runtime_path(record["artifacts"]["context"])
    template = {
        "chapter_id": chapter_id,
        "artifact_kind": artifact_kind,
        "artifact_sha256": _sha256(prose_path),
        "context_sha256": _sha256(context_path),
        "verdict": "ACCEPT_WITH_WARNINGS",
        "dimensions": {key: [] for key in ("canon", "character", "state", "causality", "pacing", "life_force", "anti_ai_taste", "originality")},
        "issues": [],
    }
    paths = [record["artifacts"][key] for key in ("context", "rule_stack", "trace", artifact_kind, "observation")]
    packet = runtime_path(f"system/production_runtime/chapters/{chapter_id}/{artifact_kind}_audit_packet.md")
    packet.write_text(
        "\n".join([
            "# NRL Antigravity Chapter Audit v0.20", "",
            "Read all artifacts. Judge continuity, causality, long-form vitality and AI-taste independently.",
            "Do not rewrite prose. Return one JSON object only using the exact binding hashes.", "",
            *[f"- `{path}`" for path in paths], "", "```json",
            json.dumps(template, ensure_ascii=False, indent=2), "```", "",
        ]), encoding="utf-8"
    )
    return {"chapter_id": chapter_id, "packet_path": str(packet.relative_to(ROOT)), "template": template}


def dispatch_chapter_audit(chapter_id: str, model: str = "Gemini 3.5 Flash (High)") -> dict[str, Any]:
    packet = build_chapter_audit_packet(chapter_id)
    binary = find_agy_binary()
    if not binary:
        raise RuntimeError("agy binary is missing")
    packet_path = runtime_path(packet["packet_path"])
    result = subprocess.run(
        [binary, "--add-dir", str(ROOT), "--model", model, "--mode", "plan", "--sandbox", "--print-timeout", "12m0s", "-p", packet_path.read_text(encoding="utf-8")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    try:
        data = json.loads(result.stdout.strip().removeprefix("```json").removesuffix("```").strip())
        schema = _read_json(runtime_path("system/production_runtime/schemas/continuity_audit.schema.json"))
        jsonschema.validate(data, schema)
    except (json.JSONDecodeError, jsonschema.ValidationError) as error:
        return {"valid": False, "errors": [str(error)], "returncode": result.returncode, "stderr": result.stderr.strip()}
    expected = packet["template"]
    if data["artifact_kind"] != expected["artifact_kind"] or data["artifact_sha256"] != expected["artifact_sha256"] or data["context_sha256"] != expected["context_sha256"]:
        return {"valid": False, "errors": ["audit binding hash mismatch"]}
    if data["verdict"] == "REWORK_REQUIRED":
        return {"valid": False, "errors": ["audit requires rework and cannot advance chapter state"], "verdict": data["verdict"]}
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    is_revision = expected["artifact_kind"] == "revision"
    artifact_key = "revision_audit" if is_revision else "continuity_audit"
    target_stage = "revision_audited" if is_revision else "continuity_audited"
    transition = validate_stage_transition(record, target_stage, f"{artifact_key}.json")
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
    target = runtime_path(f"system/production_runtime/chapters/{chapter_id}/{artifact_key}.json")
    _write_json(target, data)
    record["artifacts"][artifact_key] = str(target.relative_to(ROOT))
    record["stage"] = target_stage
    _save_registry(registry)
    return {"valid": True, "chapter_id": chapter_id, "stage": record["stage"], "verdict": data["verdict"]}


def ingest_chapter_revision(chapter_id: str, file_arg: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    transition = validate_stage_transition(record, "revision_generated", file_arg)
    if not transition["valid"]:
        raise RuntimeError("; ".join(transition["errors"]))
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


def dispatch_chapter_revision(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    if record["stage"] != "continuity_audited":
        raise RuntimeError("chapter must be continuity_audited before revision")
    draft = runtime_path(record["artifacts"]["draft"])
    audit = _read_json(runtime_path(record["artifacts"]["continuity_audit"]))
    context = _read_json(runtime_path(record["artifacts"]["context"]))
    prompt = "\n".join(
        [
            "你是 Novel Research Lab 的 Hermes 修订写手。只输出修订后的完整正文，不加标题或说明。",
            "解决审查问题但不得改变章节意图、引入未登记资产或无观察依据的状态变化。",
            "保持 2600-4200 个中文字符，并减少模板化转折、抽象总结和 AI 腔。",
            "审查：", json.dumps(audit, ensure_ascii=False),
            "上下文：", json.dumps(context, ensure_ascii=False),
            "原稿：", draft.read_text(encoding="utf-8"),
        ]
    )
    text = ask_hermes(prompt)
    metrics = analyze_prose_metrics(text)
    if not 2600 <= metrics["chinese_character_count"] <= 4200:
        return {"valid": False, "errors": ["revision must contain 2600-4200 Chinese characters"], "metrics": metrics}
    candidate = runtime_path(f"system/production_runtime/chapters/{chapter_id}/revision.candidate.md")
    candidate.write_text(text, encoding="utf-8")
    result = ingest_chapter_revision(chapter_id, str(candidate))
    candidate.unlink(missing_ok=True)
    return {"valid": True, **result, "metrics": metrics}


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
    audit = _read_json(runtime_path(record["artifacts"]["revision_audit"]))
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


def accept_chapter(chapter_id: str) -> dict[str, Any]:
    registry = _load_registry()
    record = _chapter_record(registry, chapter_id)
    revision = runtime_path(record.get("artifacts", {}).get("revision", ""))
    settlement_path = runtime_path(record.get("artifacts", {}).get("settlement", ""))
    settlement = _read_json(settlement_path) if settlement_path.is_file() else {}
    validation = validate_acceptance(record, settlement, _sha256(revision) if revision.is_file() else "")
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


def build_production_readiness() -> dict[str, Any]:
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
        "project_reconciliation_applied": bool(
            application.get("status") == "applied"
            and application.get("resulting_asset_store_sha256")
            == _sha256(runtime_path("system/creation_assets/project_assets.v0.2.json"))
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
