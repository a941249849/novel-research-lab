from __future__ import annotations

from typing import Any

from nrl_corpus_pipeline import build_pipeline_status
from nrl_system_status import build_system_status


VERSION = "0.4"

ARCHITECTURE_LAYERS = [
    (
        "corpus_layer",
        "语料层",
        "protected_input",
        "raw corpus is protected; normal runtime uses structured derivatives",
        None,
    ),
    (
        "single_book_decomposition",
        "单书拆解层",
        "partial_data",
        "Book DNA / Narrative DNA / State Ledger derivatives exist with Core7 promoted assets",
        None,
    ),
    (
        "cross_book_distillation",
        "跨书蒸馏层",
        "partial_engine",
        "mechanism notes and synthesis exist but are not a full mechanism engine",
        None,
    ),
    (
        "research_asset_engine",
        "研究资产引擎",
        "runnable",
        "structured Phase 1 assets are indexed for runtime evidence",
        None,
    ),
    (
        "original_project_synthesis",
        "原创项目综合层",
        "data_ready",
        "current project is synthesized into Story Bible and related phase assets",
        None,
    ),
    (
        "long_form_creation_asset_os",
        "长篇创作资产系统",
        "contract_ready",
        "nine asset families exist as contracts; operating registries are incomplete",
        None,
    ),
    (
        "planning_pipeline",
        "规划管线层",
        "runnable",
        "v0.3 plans one asset family from research evidence without generating final assets",
        "corpus_pipeline_v0.3",
    ),
    (
        "agent_review_and_production",
        "Agent 审查与生产层",
        "blocked",
        "Codex validates locally; Antigravity uses guarded CLI review; Hermes is paused",
        None,
    ),
    (
        "runtime_control_plane",
        "Runtime / Control Plane 层",
        "runnable",
        "runtime reads state, validates, exposes safe actions, and serves local APIs",
        None,
    ),
    (
        "studio_cockpit",
        "Studio 驾驶舱层",
        "partial",
        "Studio exposes system state and must now expose architecture reconciliation",
        None,
    ),
]


def _layers(system_status: dict[str, Any]) -> list[dict[str, Any]]:
    layers = [
        {
            "order": index + 1,
            "layer_id": layer_id,
            "label_zh": label_zh,
            "status": status,
            "purpose": purpose,
            "child_implementation": child,
        }
        for index, (layer_id, label_zh, status, purpose, child) in enumerate(
            ARCHITECTURE_LAYERS
        )
    ]
    deep_status = system_status["verifiable_deep_reading"]["status"]
    layers[0]["status"] = "deep_read_verified" if system_status["production_ready"] else deep_status
    layers[1]["status"] = "data_ready" if system_status["production_ready"] else "revalidation_in_progress"
    layers[2]["status"] = "data_ready" if system_status["production_ready"] else "blocked_on_deep_read"
    layers[5]["status"] = "data_ready"
    layers[7]["status"] = "runnable" if system_status["production_ready"] else "blocked_before_prose"
    layers[7]["child_implementation"] = "production_chapter_runtime_v0.20"
    layers[9]["status"] = "runnable"
    return layers


def _agent_roles(system_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "agent": "Codex",
            "status": "local_runtime_host",
            "role": "本地系统宿主 / 直连写手 / Runtime / 工程 / 校验 / 编排",
            "execution_boundary": "supervisor, direct writer, compiler, validator, observer, and state settler",
        },
        {
            "agent": "Antigravity",
            "status": system_status["antigravity_execution"]["effective_state"],
            "role": "CLI 协作文学审查 / 长篇生命力评估",
            "execution_boundary": "registered deep-reading, continuity, and literary-review jobs only",
        },
        {
            "agent": "Hermes",
            "status": "optional_enrichment",
            "display_status": f"Hermes: {system_status['hermes_execution_status']}",
            "role": "可选后期文学增强，不参与主生产链",
            "execution_boundary": "never required for drafting, observation, or state settlement",
        },
        {
            "agent": "Web GPT",
            "status": "architecture_review_only",
            "role": "架构互审和源上下文裁决",
            "execution_boundary": "not a task dispatcher",
        },
        {
            "agent": "Owner",
            "status": "gate_authority",
            "role": "阶段、外部 Agent、内容生产授权",
            "execution_boundary": "manual decision authority",
        },
    ]


def build_architecture_reconciliation(
    state: dict[str, Any],
    adapters: dict[str, Any],
    pipeline_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    pipeline = pipeline_status or build_pipeline_status(state, adapters)
    return {
        "version": VERSION,
        "implementation_revision": "0.20",
        "source_context": {
            "conversation_title": "中文玄幻小说汇总",
            "accepted_on": "2026-07-09",
            "source_role": "architecture_review_baseline",
        },
        "fixed_identity": {
            "short_name": "Novel Research Lab",
            "principle": "Corpus-to-Creation",
            "positioning_zh": "基于中文热门长篇小说语料研究蒸馏的原创长篇小说创作引擎",
            "not_a": ["generic writing app", "InkOS clone", "document pipeline"],
            "core_chain": [
                "training corpus",
                "single-book decomposition",
                "cross-book mechanism distillation",
                "narrative law / mechanism library",
                "original project synthesis",
                "Story Bible",
                "long-form creation asset system",
                "outline / chapter planning",
                "draft",
                "review",
                "state ledger",
                "continuous long-form production",
            ],
        },
        "architecture_layers": _layers(system_status),
        "experiment_calibration": {
            "label_zh": "Core7 小批量试验",
            "status": "accepted_as_calibration_basis",
            "scope": "Core7 promoted assets are real calibration data; remaining corpus is not assumed complete.",
            "production_meaning": "small-batch validation supports architecture convergence before full production execution",
        },
        "implementation_alignment": {
            "pipeline_version": pipeline["version"],
            "pipeline_id": pipeline["pipeline_id"],
            "pipeline_layer": "planning_pipeline",
            "classification": "child_implementation_not_full_architecture",
            "next_family": pipeline["next_family"]["family"],
            "deep_read_runtime": "verifiable_deep_reading_v0.18",
            "project_reconciliation": "borrowed_heaven_project_reconciliation_v0.19",
            "chapter_runtime": "production_chapter_runtime_v0.20",
        },
        "agent_role_contract": _agent_roles(system_status),
        "current_mismatch_report": [
            {
                "mismatch_id": "runtime_pipeline_ahead_of_architecture",
                "severity": "high",
                "summary": "Resolved: v0.3 is classified as the planning child layer and the ten-layer architecture remains canonical.",
                "correction": "No further architecture fork; new runtimes remain child implementations.",
            },
            {
                "mismatch_id": "product_visibility_gap",
                "severity": "high",
                "summary": "Resolved: Studio reads the same runtime status and now exposes truthful deep-reading and production gates.",
                "correction": "Keep Studio generated and read-only; do not create UI-owned state.",
            },
            {
                "mismatch_id": "legacy_proof_overclaim",
                "severity": "high",
                "summary": "v0.8 sampled-access evidence was previously presented as full deep reading.",
                "correction": "v0.18 requires contiguous byte coverage, per-book synthesis, and cross-book distillation.",
            },
            {
                "mismatch_id": "missing_chapter_runtime",
                "severity": "high",
                "summary": "Research and asset layers existed without a traceable chapter production lifecycle.",
                "correction": "v0.20 adds intent, compiled context, rule stack, draft, observation, audit, revision, and settlement stages.",
            },
        ],
        "production_readiness": {
            "system_mode": system_status["operating_mode"],
            "content_progression": system_status["content_progression"],
            "owner_gate_required": system_status["owner_gate_required"],
            "owner_gate_status": system_status["owner_gate_status"],
            "content_generation_allowed": False,
            "hermes_execution_status": system_status["hermes_execution_status"],
            "deep_read_status": system_status["verifiable_deep_reading"]["status"],
            "production_ready": system_status["production_ready"],
        },
        "next_architecture_action": {
            "action_id": "verifiable_deep_reading_v0_18",
            "label_zh": "完成连续深读、项目重审与正文运行门禁",
            "safe_command": "python3 system/runtime/nrl.py deep-read-status",
            "blocked_actions": [
                "generate chapter prose before production readiness",
                "call Hermes writer before v0.18 and v0.19 gates",
                "promote unvalidated Agent output",
                "treat historical v0.8 proof as full deep reading",
            ],
        },
    }
