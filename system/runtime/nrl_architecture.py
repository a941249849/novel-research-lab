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
        "Codex validates locally; Antigravity is manual review; Hermes is paused",
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


def _layers() -> list[dict[str, Any]]:
    return [
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


def _agent_roles(system_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "agent": "Codex",
            "status": "local_runtime_host",
            "role": "本地系统宿主 / Runtime / 工程 / 校验 / 编排",
            "execution_boundary": "may execute local runtime and validation only",
        },
        {
            "agent": "Antigravity",
            "status": "manual_external_literary_review",
            "role": "人工外部文学审查 / 长篇生命力评估",
            "execution_boundary": "manual handoff only",
        },
        {
            "agent": "Hermes",
            "status": system_status["hermes_execution_status"],
            "display_status": f"Hermes: {system_status['hermes_execution_status']}",
            "role": "后期写手 / 文学增强 / 受控创意生成",
            "execution_boundary": "paused until explicit Owner authorization",
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
        "architecture_layers": _layers(),
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
        },
        "agent_role_contract": _agent_roles(system_status),
        "current_mismatch_report": [
            {
                "mismatch_id": "runtime_pipeline_ahead_of_architecture",
                "severity": "high",
                "summary": "Runtime and pipeline work advanced before source architecture reconciliation was locked.",
                "correction": "Classify v0.3 as planning_pipeline and expose the ten-layer architecture in runtime and Studio.",
            },
            {
                "mismatch_id": "product_visibility_gap",
                "severity": "high",
                "summary": "The Owner could not see how research assets, agents, runtime, and creation assets form one system.",
                "correction": "Studio must expose architecture layers, Core7 calibration, mismatch report, and next architecture action.",
            },
        ],
        "production_readiness": {
            "system_mode": system_status["operating_mode"],
            "content_progression": system_status["content_progression"],
            "owner_gate_required": system_status["owner_gate_required"],
            "owner_gate_status": system_status["owner_gate_status"],
            "content_generation_allowed": False,
            "hermes_execution_status": system_status["hermes_execution_status"],
        },
        "next_architecture_action": {
            "action_id": "architecture_reconciliation_v0_4",
            "label_zh": "锁定系统架构并把 v0.3 归位为规划管线层",
            "safe_command": "python3 system/runtime/nrl.py architecture-status",
            "blocked_actions": pipeline["forbidden_actions"],
        },
    }
