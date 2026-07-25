from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path
from nrl_system_status import build_system_status


VERSION = "0.7"
ARCHITECTURE_VERSION = "0.4"
JOB_ID = "job-v07-full-corpus-antigravity-review"
JOB_PATH = runtime_path("system/agent_ops/full_corpus_job.v0.7.json")
PACKET_PATH = runtime_path(f"system/agent_ops/packets/{JOB_ID}.md")
COMMAND_PATH = runtime_path(f"system/agent_ops/packets/{JOB_ID}-command.md")
EXPECTED_OUTPUT_PATH = f"system/agent_ops/inbox/{JOB_ID}.md"
VALIDATION_PATH = runtime_path(f"system/agent_ops/validation/{JOB_ID}_validation.json")
VALIDATED_OUTBOX_PATH = runtime_path(f"system/agent_ops/outbox/{JOB_ID}_validated.md")
CREATION_ASSET_FAMILIES = (
    "characters",
    "npcs",
    "factions",
    "artifacts",
    "techniques",
    "naming",
    "emotional_bonds",
    "foreshadowing",
    "state_ledger",
)
REQUIRED_HEADINGS = (
    "## Job ID",
    "## Scope",
    "## Corpus Coverage",
    "## Cross-Book Mechanisms",
    "## Creation Asset Evidence",
    "## Originality Risk",
    "## Recommended Next Ingestion",
    "## JSON Manifest",
)
FORBIDDEN_MARKERS = (
    "novel_training_set/",
    "第一章",
    "正文",
    "Chapter 1",
    "Hermes 已执行",
    "最终正文",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _empty_job() -> dict[str, Any]:
    return {
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "architecture_version": ARCHITECTURE_VERSION,
        "job_type": "antigravity_full_corpus_review",
        "review_scope": "full_remaining_corpus",
        "owner_agent": "antigravity",
        "state": "not_prepared",
        "packet_path": str(PACKET_PATH.relative_to(ROOT)),
        "command_path": str(COMMAND_PATH.relative_to(ROOT)),
        "expected_output_path": EXPECTED_OUTPUT_PATH,
        "actual_output_path": None,
        "validation_report_path": None,
        "validated_outbox_path": None,
        "created_at": None,
        "updated_at": None,
        "blocked_reason": None,
    }


def load_full_corpus_job() -> dict[str, Any]:
    if not JOB_PATH.exists():
        return _empty_job()
    data = _read_json(JOB_PATH)
    if data.get("contract_version") != VERSION or data.get("job_id") != JOB_ID:
        return _empty_job()
    return data


def save_full_corpus_job(job: dict[str, Any]) -> dict[str, Any]:
    _write_json(JOB_PATH, job)
    return job


def _architecture_summary() -> str:
    return "\n".join(
        [
            "1. corpus_layer / 语料层",
            "2. single_book_decomposition / 单书拆解层",
            "3. cross_book_distillation / 跨书蒸馏层",
            "4. research_asset_engine / 研究资产引擎",
            "5. original_project_synthesis / 原创项目综合层",
            "6. long_form_creation_asset_os / 长篇创作资产系统",
            "7. planning_pipeline / 规划管线层",
            "8. agent_review_and_production / Agent 审查与生产层",
            "9. runtime_control_plane / Runtime / Control Plane 层",
            "10. studio_cockpit / Studio 驾驶舱层",
        ]
    )


def _family_lines() -> str:
    return "\n".join(f"- `{family}`" for family in CREATION_ASSET_FAMILIES)


def _packet_text() -> str:
    headings = "\n".join(f"- `{heading}`" for heading in REQUIRED_HEADINGS)
    return f"""# NRL Antigravity Full Corpus Review Packet v0.7

## Job

- job_id: {JOB_ID}
- contract_version: {VERSION}
- architecture_version: {ARCHITECTURE_VERSION}
- review_scope: full_remaining_corpus
- owner_agent: antigravity
- expected_output_path: {EXPECTED_OUTPUT_PATH}

## Purpose

Run a full-corpus literary and structural review for Novel Research Lab after the v0.4 architecture freeze.
The output must be structured for Codex ingestion, not written as a freeform essay.

## Architecture Baseline

{_architecture_summary()}

## Required Asset Families

{_family_lines()}

## Required Markdown Headings

{headings}

## JSON Manifest Contract

Return a fenced JSON block under `## JSON Manifest` with:

- job_id
- contract_version
- review_scope
- architecture_version
- corpus_policy
- book_reviews
- cross_book_mechanisms
- asset_family_evidence
- originality_risks
- recommended_next_ingestion

## Forbidden Actions

- Do not write novel prose.
- Do not produce Chapter 1.
- Do not generate final character sheets, final naming dictionaries, final technique trees, or final outline trees.
- Do not claim Hermes execution.
- Do not quote raw source prose.
- Do not include `novel_training_set/` paths in the returned artifact.

## Return Instruction

Save the completed review to:

```text
{EXPECTED_OUTPUT_PATH}
```
"""


def _command_text(state: dict[str, Any]) -> str:
    project = state.get("selected_project", "《借天改命账》")
    return f"""# 交给 Antigravity 的命令包：NRL 全量小说集重读 v0.7

你现在在本机共享项目目录 `Novel Research Lab` 中工作。请执行一次中文玄幻小说全量重读与结构化审查，目标不是写正文，而是为 Novel Research Lab 的 Corpus-to-Creation 系统补全可摄取的研究资产。

## 固定系统身份

- 系统名：Novel Research Lab
- 当前原创项目：{project}
- 架构基线：v0.4 十层架构
- 当前运行模式：SYSTEM_HARDENING
- 内容推进状态：FROZEN_AT_OWNER_GATE
- Hermes：paused_not_removed，不要调用，不要代替 Hermes 写作
- Codex：本地 runtime / 工程 / 校验 / 编排
- Antigravity：CLI 协作文学审查 / 全量小说集重读 / 长篇生命力评估

## v0.4 十层架构

{_architecture_summary()}

## 你的任务

请基于本机项目中已有的小说集与 Phase 1 结构化资产，做全量重读、重分析、重规划。输出必须服务于这条链路：

小说集阅读拆解 -> 单书 DNA -> 跨书机制蒸馏 -> 创作母库 -> 新书生成

你需要重点提炼：

- 长篇追更机制
- 升级与压力循环
- 人物成长与关系推进
- NPC / 群像 / 小人物可复用结构
- 势力扩张、利益冲突和裂缝
- 道具、招式、境界、代价、反制
- 命名体系和避免撞名的规则
- 情感羁绊、牺牲、背叛、偿还
- 伏笔、误导、揭示、回收
- 状态账本需要记录的变量

## 九类创作资产必须全部覆盖

{_family_lines()}

如果某一类证据不足，请标记为 `missing` 并说明原因，不要编造。

## 输出边界

禁止：

- 写小说正文
- 写第一章
- 写章节大纲
- 生成最终人物卡
- 生成最终招式树
- 生成最终命名词典
- 声称 Hermes 已经运行或完成写作
- 复制或引用原文大段内容

允许：

- 抽象机制
- 结构化证据
- 风险判断
- 可原创迁移建议
- 缺口说明
- 后续 Codex 摄取建议

## 必须输出的 Markdown 标题

{chr(10).join(REQUIRED_HEADINGS)}

## JSON Manifest 要求

在 `## JSON Manifest` 下输出一个 fenced `json` 代码块，字段必须包含：

```json
{{
  "job_id": "{JOB_ID}",
  "contract_version": "{VERSION}",
  "review_scope": "full_remaining_corpus",
  "architecture_version": "{ARCHITECTURE_VERSION}",
  "corpus_policy": {{
    "raw_prose_quoted": false,
    "abstract_mechanisms_only": true
  }},
  "book_reviews": [],
  "cross_book_mechanisms": [],
  "asset_family_evidence": {{
    "characters": {{}},
    "npcs": {{}},
    "factions": {{}},
    "artifacts": {{}},
    "techniques": {{}},
    "naming": {{}},
    "emotional_bonds": {{}},
    "foreshadowing": {{}},
    "state_ledger": {{}}
  }},
  "originality_risks": [],
  "recommended_next_ingestion": {{}}
}}
```

请把最终结果保存到：

```text
{EXPECTED_OUTPUT_PATH}
```

注意：这不是作文任务，不是章节任务，不是 Hermes 写作任务。你的产物必须能被 Codex 校验和摄取。
"""


def write_full_corpus_packet(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    created = now_iso()
    job = load_full_corpus_job()
    if job["state"] not in {"validated", "promoted"}:
        job["state"] = "ready_for_antigravity"
        job["blocked_reason"] = None
        job["actual_output_path"] = None
        job["validation_report_path"] = None
        job["validated_outbox_path"] = None
    job["created_at"] = job.get("created_at") or created
    job["updated_at"] = created
    job["system_mode"] = system_status["operating_mode"]
    job["content_progression"] = system_status["content_progression"]
    PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKET_PATH.write_text(_packet_text(), encoding="utf-8")
    COMMAND_PATH.write_text(_command_text(state), encoding="utf-8")
    save_full_corpus_job(job)
    return {
        "job_id": JOB_ID,
        "state": job["state"],
        "packet_path": str(PACKET_PATH.relative_to(ROOT)),
        "command_path": str(COMMAND_PATH.relative_to(ROOT)),
        "expected_output_path": EXPECTED_OUTPUT_PATH,
    }


def build_full_corpus_status(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    job = load_full_corpus_job()
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "architecture_version": ARCHITECTURE_VERSION,
        "state": job["state"],
        "packet_path": job["packet_path"],
        "command_path": job["command_path"],
        "expected_output_path": job["expected_output_path"],
        "actual_output_path": job.get("actual_output_path"),
        "validation_report_path": job.get("validation_report_path"),
        "validated_outbox_path": job.get("validated_outbox_path"),
        "antigravity_mode": (
            "cli_bridge_owner_gated_full_corpus_review"
            if system_status["antigravity_execution"]["effective_state"] == "ready"
            else f"{system_status['antigravity_execution']['effective_state']}_full_corpus_review"
        ),
        "hermes_allowed": False,
        "system_mode": system_status["operating_mode"],
        "content_progression": system_status["content_progression"],
        "owner_gate": {
            "required": system_status["owner_gate_required"],
            "status": system_status["owner_gate_status"],
        },
        "asset_families": list(CREATION_ASSET_FAMILIES),
    }


def _resolve_repo_path(file_arg: str) -> Path:
    path = Path(file_arg)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def ingest_full_corpus_output(file_arg: str) -> dict[str, Any]:
    job = load_full_corpus_job()
    if job["state"] == "not_prepared":
        raise RuntimeError("full corpus packet has not been prepared")
    file_path = _resolve_repo_path(file_arg)
    inbox = runtime_path("system/agent_ops/inbox").resolve()
    if not _is_relative_to(file_path, inbox):
        raise RuntimeError(f"full corpus output must be placed under system/agent_ops/inbox: {file_arg}")
    if not file_path.exists():
        raise RuntimeError(f"full corpus output file does not exist: {file_arg}")
    rel_path = str(file_path.relative_to(ROOT))
    job["actual_output_path"] = rel_path
    if job["state"] not in {"validated", "promoted"}:
        job["state"] = "output_received"
    job["updated_at"] = now_iso()
    save_full_corpus_job(job)
    return {"job": job, "ingested": rel_path}


def _extract_manifest(text: str) -> tuple[dict[str, Any] | None, str | None]:
    pattern = r"## JSON Manifest\s*```json\s*(.*?)\s*```"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        return None, "missing JSON Manifest fenced json block"
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        return None, f"invalid JSON Manifest: {error}"
    if not isinstance(data, dict):
        return None, "JSON Manifest must be an object"
    return data, None


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_pairs = {
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "review_scope": "full_remaining_corpus",
        "architecture_version": ARCHITECTURE_VERSION,
    }
    for key, expected in expected_pairs.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must be {expected}")
    if not isinstance(manifest.get("book_reviews"), list) or not manifest["book_reviews"]:
        errors.append("book_reviews must be a non-empty list")
    if not isinstance(manifest.get("cross_book_mechanisms"), list) or not manifest["cross_book_mechanisms"]:
        errors.append("cross_book_mechanisms must be a non-empty list")
    families = manifest.get("asset_family_evidence")
    if not isinstance(families, dict):
        errors.append("asset_family_evidence must be an object")
    else:
        missing = sorted(set(CREATION_ASSET_FAMILIES) - set(families))
        extra = sorted(set(families) - set(CREATION_ASSET_FAMILIES))
        if missing:
            errors.append(f"missing asset families: {', '.join(missing)}")
        if extra:
            errors.append(f"unknown asset families: {', '.join(extra)}")
    corpus_policy = manifest.get("corpus_policy")
    if not isinstance(corpus_policy, dict):
        errors.append("corpus_policy must be an object")
    elif corpus_policy.get("raw_prose_quoted") is not False:
        errors.append("corpus_policy.raw_prose_quoted must be false")
    return errors


def validate_full_corpus_output() -> dict[str, Any]:
    job = load_full_corpus_job()
    actual = job.get("actual_output_path")
    if not actual:
        raise RuntimeError("full corpus job has no ingested output")
    output_path = runtime_path(str(actual))
    text = output_path.read_text(encoding="utf-8")
    missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    forbidden_hits = [marker for marker in FORBIDDEN_MARKERS if marker in text]
    manifest, manifest_error = _extract_manifest(text)
    manifest_errors = [manifest_error] if manifest_error else _validate_manifest(manifest or {})
    valid = not missing_headings and not forbidden_hits and not manifest_errors
    report = {
        "job_id": JOB_ID,
        "valid": valid,
        "missing_headings": missing_headings,
        "forbidden_hits": forbidden_hits,
        "manifest_errors": manifest_errors,
        "validated_at": now_iso(),
    }
    _write_json(VALIDATION_PATH, report)
    job["validation_report_path"] = str(VALIDATION_PATH.relative_to(ROOT))
    if valid:
        VALIDATED_OUTBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(output_path, VALIDATED_OUTBOX_PATH)
        job["state"] = "validated"
        job["validated_outbox_path"] = str(VALIDATED_OUTBOX_PATH.relative_to(ROOT))
        job["blocked_reason"] = None
    else:
        job["state"] = "rejected"
        job["blocked_reason"] = "validation_failed"
    job["updated_at"] = now_iso()
    save_full_corpus_job(job)
    return {
        "valid": valid,
        "job": job,
        "report": report,
        "manifest": manifest if manifest is not None else {},
    }
