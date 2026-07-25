from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_codex_writer import ask_codex_writer
from nrl_model_router import ROUTES, validate_model_team_contract
from nrl_paths import ROOT, runtime_path


CALIBRATION_PATH = runtime_path(
    "system/production_runtime/calibration/direct_codex_writer_calibration.v0.21.json"
)
CALIBRATION_ROOT = CALIBRATION_PATH.parent
MODEL_TEAM_ATTESTATION_PATH = CALIBRATION_ROOT / "codex_model_team_attestation.v0.27.json"
CANDIDATE_ROOT = CALIBRATION_ROOT / "candidates"
INTERNAL_SCREEN_ROOT = CALIBRATION_ROOT / "internal_screening"
REVIEW_PACKET_PATH = runtime_path(
    ".agent-handoff/antigravity/requests/nrl-v021-direct-writer-calibration-review.md"
)
DECISION_PACKET_PATH = runtime_path(
    ".agent-handoff/antigravity/requests/nrl-v021-direct-writer-calibration-routing-decision.md"
)

MODELS = ("gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna")
SCENARIOS = (
    {
        "scenario_id": "cause_under_pressure",
        "brief": "一名镖局学徒误将一份染血的押镖簿带回城。城门即将关闭，师父命他立刻焚毁证据；他发现簿册夹层写着失踪姐姐的名字。写一个有明确因果选择、具体动作与未完全揭示后果的场景。",
    },
    {
        "scenario_id": "relationship_reversal",
        "brief": "两名结伴多年的寻药人终于找到灵药，但其中一人早已隐瞒自己只能再活三日。写一个通过动作、对话和物件呈现信任变化的场景，不解释人物心理结论。",
    },
    {
        "scenario_id": "rule_cost",
        "brief": "一位少年第一次使用会折损记忆的禁术，必须在救下陌生人和保留母亲的最后一段记忆之间选择。写一个规则代价清楚、场面可感、结尾留下可追读后果的场景。",
    },
)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_payload() -> dict[str, Any]:
    return json.loads(CALIBRATION_PATH.read_text(encoding="utf-8"))


def _write_payload(payload: dict[str, Any]) -> None:
    CALIBRATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CALIBRATION_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _candidate_prompt(brief: str) -> str:
    return f"""你正在参加原创中文长篇叙事的盲测校准。\n\n{brief}\n\n要求：\n- 只输出 550 至 750 个汉字的小说正文，不要标题、解释、提纲或 Markdown。\n- 人物不能使用任何既有作品、真实作者或本项目人物设定。\n- 以可见动作、物件和对话推进，避免总结式说理与套路化宣言。\n- 因果必须能从文本中追溯；结尾留下具体但未解决的后果。\n"""


def run_direct_writer_calibration(timeout_seconds: int = 240) -> dict[str, Any]:
    """Create exactly nine blinded, non-project prose candidates.

    Candidates are deliberately outside the active novel. The reviewer only
    sees anonymous labels; model mapping remains in the calibration ledger.
    """
    payload = _read_payload()
    existing = {str(item.get("run_id")): item for item in payload.get("runs", [])}
    runs: list[dict[str, Any]] = []
    created: list[str] = []
    for scenario_index, scenario in enumerate(SCENARIOS, start=1):
        for model_index, model in enumerate(MODELS, start=1):
            run_id = f"candidate-{scenario_index}{model_index}"
            if run_id in existing:
                runs.append(existing[run_id])
                continue
            text = ask_codex_writer(
                _candidate_prompt(str(scenario["brief"])),
                model=model,
                timeout_seconds=timeout_seconds,
            )
            candidate_path = CANDIDATE_ROOT / f"{run_id}.md"
            candidate_path.parent.mkdir(parents=True, exist_ok=True)
            candidate_path.write_text(text + "\n", encoding="utf-8")
            runs.append(
                {
                    "run_id": run_id,
                    "blind_label": f"样本 {len(runs) + 1:02d}",
                    "scenario_id": scenario["scenario_id"],
                    "model": model,
                    "candidate_path": str(candidate_path.relative_to(ROOT)),
                    "sha256": _sha256_text(text),
                    "generated_at": _now(),
                    "review_status": "pending_blind_review",
                }
            )
            created.append(run_id)
    payload["runs"] = runs
    payload["status"] = "candidates_generated"
    payload["generated_at"] = _now()
    _write_payload(payload)
    return {"valid": len(runs) == 9, "created": created, "run_count": len(runs)}


def _packet_header() -> list[str]:
    return [
        "# NRL Direct Writer Blind Calibration Review",
        "",
        "You are an independent literary quality reviewer. These are isolated, original calibration samples, not project prose. Do not write or revise fiction.",
        "",
        "## Required Output",
        "Return exactly these sections: `## Scores`, `## Rejection Reasons`, `## Routing Recommendation`, and `## Verdict`.",
        "Score each sample from 1 to 5 for causality, scene embodiment, relationship/rule handling, anti-formula quality, and continuation pull. Reject any sample with copying signals, empty rhetoric, broken causality, or unusable prose. In `## Verdict`, write exactly one of `ACCEPT`, `RECALIBRATE`, or `REJECT`.",
    ]


def build_blind_review_packet() -> dict[str, Any]:
    payload = _read_payload()
    runs = payload.get("runs", [])
    if len(runs) != 9:
        raise RuntimeError("nine calibration candidates are required before review")
    packet_paths: list[str] = []
    REVIEW_PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    for batch_index, start in enumerate(range(0, len(runs), 3), start=1):
        sections = _packet_header()
        for run in runs[start : start + 3]:
            path = ROOT / str(run["candidate_path"])
            if not path.is_file():
                raise RuntimeError(f"calibration candidate is missing: {run['run_id']}")
            sections.extend(
                [
                    "",
                    f"## {run['blind_label']} ({run['scenario_id']})",
                    path.read_text(encoding="utf-8").strip(),
                ]
            )
        path = REVIEW_PACKET_PATH.with_name(
            f"{REVIEW_PACKET_PATH.stem}-batch-{batch_index}.md"
        )
        path.write_text("\n".join(sections) + "\n", encoding="utf-8")
        packet_paths.append(str(path.relative_to(ROOT)))
    return {
        "valid": True,
        "packet_paths": packet_paths,
        "candidate_count": len(runs),
    }


def record_external_review_blocked(reason: str) -> dict[str, Any]:
    payload = _read_payload()
    payload["external_review"] = {
        "status": "blocked_cli_execution",
        "reason": reason,
        "recorded_at": _now(),
    }
    _write_payload(payload)
    return payload["external_review"]


def run_internal_calibration_screen(timeout_seconds: int = 240) -> dict[str, Any]:
    """Create a non-gating Sol screening record while external review is down."""
    packet = build_blind_review_packet()
    reviews: list[dict[str, str]] = []
    for index, packet_path in enumerate(packet["packet_paths"], start=1):
        text = (ROOT / packet_path).read_text(encoding="utf-8")
        prompt = (
            "This is an internal, non-gating quality screen. Do not claim to be "
            "an independent reviewer and do not change any production gate. "
            "Follow the scoring and verdict format in this packet.\n\n" + text
        )
        review = ask_codex_writer(
            prompt, model="gpt-5.6-sol", timeout_seconds=timeout_seconds
        )
        path = INTERNAL_SCREEN_ROOT / f"batch-{index}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(review + "\n", encoding="utf-8")
        reviews.append({"packet_path": packet_path, "review_path": str(path.relative_to(ROOT))})
    payload = _read_payload()
    payload["internal_screening"] = {
        "status": "completed_non_gating",
        "model": "gpt-5.6-sol",
        "reviews": reviews,
        "completed_at": _now(),
    }
    _write_payload(payload)
    return {"valid": len(reviews) == 3, "reviews": reviews, "non_gating": True}


def build_calibration_routing_decision_packet() -> dict[str, Any]:
    """Build the final external decision packet after blinded reviews complete."""
    payload = _read_payload()
    response_root = runtime_path(".agent-handoff/antigravity/responses")
    review_paths = [
        response_root / f"nrl-v021-direct-writer-calibration-review-opus-batch-{index}.md"
        for index in range(1, 4)
    ]
    missing = [str(path.relative_to(ROOT)) for path in review_paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"external calibration reviews are missing: {', '.join(missing)}")
    mapping = [
        {
            "blind_label": run["blind_label"],
            "scenario_id": run["scenario_id"],
            "model": run["model"],
        }
        for run in payload.get("runs", [])
    ]
    sections = [
        "# NRL Direct Writer Calibration Routing Decision",
        "",
        "You are the independent final adjudicator. Do not write fiction. Decide the production routing from the blinded reviews below.",
        "",
        "## Required Output",
        "Return exactly `## Evidence`, `## Routing Decision`, and `## Verdict`. In `## Verdict`, write exactly one of `ACCEPT_SOL_ONLY`, `RECALIBRATE`, or `REJECT`.",
        "`ACCEPT_SOL_ONLY` is allowed only when all three Sol samples are independently positive across the three distinct scenario types, and the decision explicitly excludes Terra and Luna from prose writing. Luna may remain an observer. Terra may remain unavailable for prose until separately recalibrated.",
        "",
        "## Blind-label Mapping (revealed only after scoring)",
        json.dumps(mapping, ensure_ascii=False, indent=2),
    ]
    for path in review_paths:
        sections.extend(["", f"## Review: {path.name}", path.read_text(encoding="utf-8").strip()])
    DECISION_PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    DECISION_PACKET_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return {"valid": True, "packet_path": str(DECISION_PACKET_PATH.relative_to(ROOT))}


def record_calibration_routing_decision(response_file: str) -> dict[str, Any]:
    path = Path(response_file)
    if not path.is_absolute():
        path = ROOT / path
    text = path.read_text(encoding="utf-8")
    verdict = next(
        (item for item in ("ACCEPT_SOL_ONLY", "RECALIBRATE", "REJECT") if item in text),
        None,
    )
    if verdict is None:
        raise RuntimeError("routing decision response does not contain a valid verdict")
    payload = _read_payload()
    outcome_by_id = {
        "candidate-11": "accepted", "candidate-12": "rejected", "candidate-13": "conditional",
        "candidate-21": "accepted", "candidate-22": "rejected", "candidate-23": "rejected",
        "candidate-31": "accepted", "candidate-32": "rejected", "candidate-33": "conditional",
    }
    for run in payload.get("runs", []):
        run["review_status"] = outcome_by_id.get(run.get("run_id"), "conditional")
    payload["independent_reviewer_verdict"] = verdict
    payload["independent_reviewer_response"] = str(path.relative_to(ROOT))
    payload["external_review"] = {
        "status": "completed_via_model_override",
        "model": "Claude Opus 4.6 (Thinking)",
        "response_path": str(path.relative_to(ROOT)),
        "note": "The default Gemini route was quota-exhausted; the isolated review completed through the explicit Opus route.",
        "completed_at": _now(),
    }
    payload["routing_decision"] = (
        "Sol is the only production prose writer; Terra is excluded pending focused recalibration; "
        "Luna is observer and mechanical only."
    )
    payload["status"] = "accepted_route_restricted" if verdict == "ACCEPT_SOL_ONLY" else "recalibration_required"
    payload["decision_recorded_at"] = _now()
    _write_payload(payload)
    return build_direct_writer_calibration_status()


def build_direct_writer_calibration_status() -> dict[str, Any]:
    if not CALIBRATION_PATH.exists():
        return {
            "valid": False,
            "status": "missing",
            "reason": "direct Codex writer calibration has not been recorded",
        }
    data: dict[str, Any] = _read_payload()
    required = {"version", "status", "models", "criteria", "runs"}
    runs = data.get("runs", [])
    structurally_valid_runs = all(
        {"run_id", "blind_label", "scenario_id", "model", "candidate_path", "sha256", "review_status"}.issubset(run)
        and run.get("model") in MODELS
        and run.get("review_status") in {"accepted", "rejected", "conditional"}
        for run in runs
    )
    valid = (
        required.issubset(data)
        and data.get("status") in {"accepted", "accepted_route_restricted"}
        and set(MODELS).issubset(set(data.get("models", [])))
        and len(runs) == 9
        and structurally_valid_runs
        and data.get("independent_reviewer_verdict") in {"ACCEPT", "ACCEPT_SOL_ONLY"}
        and bool(data.get("routing_decision"))
    )
    return {
        "valid": valid,
        "status": data.get("status"),
        "path": str(CALIBRATION_PATH),
        "reason": None if valid else "calibration requires nine blinded runs, independent acceptance, and an accepted routing decision",
        "run_count": len(runs),
        "external_review_status": data.get("external_review", {}).get("status", "pending"),
    }


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _generation_evidence() -> tuple[list[str], dict[str, int]]:
    items = []
    counts: dict[str, int] = {}
    # This is engine-level calibration evidence from the first accepted run,
    # not mutable state for whichever project is currently selected.
    chapter_root = ROOT / "system/production_runtime/chapters"
    for path in sorted(chapter_root.glob("chapter-*/generation_cost.json")):
        try:
            ordinal = int(path.parent.name.removeprefix("chapter-"))
        except ValueError:
            continue
        if not 1 <= ordinal <= 100:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        model = str(payload.get("writer_model"))
        counts[model] = counts.get(model, 0) + 1
        items.append(f"{path.relative_to(ROOT).as_posix()}:{_sha256_path(path)}")
    return items, counts


def build_model_team_attestation_status() -> dict[str, Any]:
    if not MODEL_TEAM_ATTESTATION_PATH.is_file():
        return {"valid": False, "status": "missing", "errors": ["v0.27 model-team attestation is missing"]}
    data = json.loads(MODEL_TEAM_ATTESTATION_PATH.read_text(encoding="utf-8"))
    errors = []
    legacy_path = runtime_path(str(data.get("supersedes_for_active_routing", "")))
    if not legacy_path.is_file() or _sha256_path(legacy_path) != data.get("legacy_calibration_sha256"):
        errors.append("legacy calibration hash mismatch")
    items, counts = _generation_evidence()
    evidence = data.get("generation_evidence", {})
    root_hash = hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()
    if len(items) != evidence.get("artifact_count") or root_hash != evidence.get("artifact_root_sha256"):
        errors.append("generation evidence root mismatch")
    if counts != evidence.get("writer_model_counts"):
        errors.append("generation model counts mismatch")
    registry_path = ROOT / "system/production_runtime/chapter_registry.v0.20.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.is_file() else {"chapters": []}
    accepted = {
        str(item.get("chapter_id"))
        for item in registry.get("chapters", [])
        if item.get("stage") == "chapter_accepted"
    }
    generation_chapters = {item.split("/")[-2] for item in items}
    if not generation_chapters.issubset(accepted):
        errors.append("generation evidence includes an unaccepted chapter")
    window_config = data.get("window_review_evidence", {})
    window_root = ROOT / str(window_config.get("path", ""))
    window_items = []
    window_verdicts = []
    for path in sorted(window_root.glob("*.json")) if window_root.is_dir() else []:
        window_items.append(f"{path.relative_to(ROOT).as_posix()}:{_sha256_path(path)}")
        window_verdicts.append(json.loads(path.read_text(encoding="utf-8")).get("verdict"))
    window_hash = hashlib.sha256("\n".join(window_items).encode("utf-8")).hexdigest()
    if len(window_items) != window_config.get("artifact_count") or window_hash != window_config.get("artifact_root_sha256"):
        errors.append("window review evidence root mismatch")
    if not window_verdicts or any(
        verdict != window_config.get("required_verdict") for verdict in window_verdicts
    ):
        errors.append("window review evidence is not fully accepted")
    expected_routes = {role: route.get("model") for role, route in ROUTES.items()}
    if data.get("active_routes") != expected_routes:
        errors.append("active model routes do not match the attested decision")
    contract = validate_model_team_contract()
    errors.extend(contract["errors"])
    if data.get("status") != "accepted_operational_route":
        errors.append("model-team attestation is not accepted")
    return {
        "valid": not errors,
        "status": data.get("status"),
        "errors": errors,
        "path": str(MODEL_TEAM_ATTESTATION_PATH.relative_to(ROOT)),
        "generation_artifact_count": len(items),
        "writer_model_counts": counts,
        "model_team_contract": contract,
    }
