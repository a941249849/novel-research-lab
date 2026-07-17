from __future__ import annotations

from typing import Any

from nrl_corpus_pipeline import build_pipeline_status
from nrl_paths import runtime_path
from nrl_production_operator import build_operator_status, describe_next_production_action
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
    operator = build_operator_status(
        runtime_path("system/production_runtime/chapter_registry.v0.20.json")
    )
    production_action = describe_next_production_action(operator)
    production_ready = (
        system_status["production_ready"]
        and operator["valid"]
        and not operator.get("blocking_window_review")
    )
    return {
        "version": VERSION,
        "implementation_revision": "1.0",
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
            "scope": "Core7 established the calibration method; v0.18 then verified all 18 books, 143 contiguous chunks, 18 syntheses, and cross-book distillation.",
            "production_meaning": "the small-batch architecture was retained and the full corpus was materialized through the same evidence contract",
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
            "story_compiler": "ten_chapter_story_window_v1",
            "context_memory": "bounded_rolling_state_v1",
            "audit_policy": "deterministic_each_chapter_external_each_five_window_each_ten",
        },
        "agent_role_contract": _agent_roles(system_status),
        "current_mismatch_report": [
            {
                "mismatch_id": "control_plane_split_brain",
                "severity": "high",
                "summary": "Resolved: historical Phase 2E freeze no longer contradicts the later Volume 1 Owner authorization.",
                "correction": "The current phase, active blueprint, capability roadmap, and chapter registry now resolve to one production state.",
            },
            {
                "mismatch_id": "generic_intent_repetition",
                "severity": "high",
                "summary": "Resolved for active production: chapters 11-20 are compiled from unique event, conflict, choice, state delta, and hook contracts.",
                "correction": "No chapter from 11 onward can compile without a validated ten-chapter story window.",
            },
            {
                "mismatch_id": "unbounded_context_growth",
                "severity": "high",
                "summary": "Resolved: chapter prompts no longer embed the complete settlement history.",
                "correction": "A rolling state snapshot plus the latest two settlements bounds prompt size while retaining active facts.",
            },
            {
                "mismatch_id": "audit_cost_and_false_acceptance",
                "severity": "high",
                "summary": "Resolved: deterministic anti-template checks run every chapter and external literary review is reserved for five-chapter checkpoints.",
                "correction": "Final metric failures block settlement; ten-chapter window review and full-volume release review remain mandatory.",
            },
        ],
        "production_readiness": {
            "system_mode": system_status["operating_mode"],
            "content_progression": system_status["content_progression"],
            "owner_gate_required": system_status["owner_gate_required"],
            "owner_gate_status": system_status["owner_gate_status"],
            "content_generation_allowed": system_status["production_ready"],
            "hermes_execution_status": system_status["hermes_execution_status"],
            "deep_read_status": system_status["verifiable_deep_reading"]["status"],
            "production_ready": production_ready,
            "release_ready": operator["release_ready"],
            "blocking_window_review": operator.get("blocking_window_review"),
            "blocking_window_verdict": operator.get("blocking_window_verdict"),
            "accepted_contiguous": operator["accepted_contiguous"],
            "accepted_release_ready_count": operator["accepted_release_ready_count"],
        },
        "next_architecture_action": {
            **production_action,
            "blocked_actions": [
                "generate chapter prose without a validated story window",
                "publish before Volume 1 release acceptance",
                "promote unvalidated Agent output",
                "treat historical Phase 2E state as the active production gate",
            ],
        },
    }
