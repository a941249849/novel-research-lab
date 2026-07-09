from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from nrl_agent_ops import load_job_queue
from nrl_creation_schemas import validate_creation_asset_store
from nrl_paths import ROOT, runtime_path
from nrl_rag_index import load_or_build_rag_index
from nrl_system_status import build_system_status


VERSION = "0.6"
TECHNIQUES_JOB_ID = "job-v05-techniques-antigravity-review"
NAMING_JOB_ID = "job-v05-naming-antigravity-review"
TECHNIQUES_OUTBOX_PATH = "system/agent_ops/outbox/job-v05-techniques-antigravity-review_validated.md"
NAMING_OUTBOX_PATH = "system/agent_ops/outbox/job-v05-naming-antigravity-review_validated.md"
PROJECT_ASSET_STORE_PATH = runtime_path("system/creation_assets/project_assets.v0.2.json")
SUPPORTED_FAMILIES = ("techniques", "naming")
OWNED_TECHNIQUE_IDS = (
    "technique_costed_advancement",
    "technique_backlash_guard",
    "technique_state_reversal",
)
OWNED_NAMING_IDS = ("naming_project_contract_seed",)
OWNED_NPC_IDS = ("npcs_project_contract_seed",)
OWNED_ARTIFACT_IDS = ("artifacts_project_contract_seed",)
OWNED_STATE_LEDGER_IDS = ("state_ledger_project_contract_seed",)
OWNED_BOND_IDS = ("emotional_bonds_project_contract_seed",)
OWNED_FORESHADOWING_IDS = ("foreshadowing_project_contract_seed",)
OWNED_CHARACTER_IDS = ("characters_project_contract_seed",)
OWNED_FACTION_IDS = ("factions_project_contract_seed",)
FORBIDDEN_TEXT = ("novel_training_set/", "正文", "第一章", "Chapter 1")
TECHNIQUE_CANDIDATES = (
    {
        "asset_id": "technique_costed_advancement",
        "display_name": "Costed Advancement Candidate",
        "cost": "Every advancement action must spend a visible resource, reputation position, or bodily state.",
        "constraints": [
            "seed candidate only",
            "not a final in-world technique name",
            "do not use for prose generation",
            "do not treat as final technique tree",
        ],
    },
    {
        "asset_id": "technique_backlash_guard",
        "display_name": "Backlash Guard Candidate",
        "cost": "Every defensive or stabilizing action must leave a delayed backlash, debt marker, or opportunity cost.",
        "constraints": [
            "seed candidate only",
            "not a final in-world technique name",
            "do not use for combat scene drafting",
            "must preserve a cost or counter path",
        ],
    },
    {
        "asset_id": "technique_state_reversal",
        "display_name": "State Reversal Candidate",
        "cost": "Every reversal action must convert one tracked state into another rather than erasing consequences.",
        "constraints": [
            "seed candidate only",
            "not a final in-world technique name",
            "do not generate final naming dictionary",
            "must cite DNA evidence before promotion",
        ],
    },
)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _project_store() -> dict[str, Any]:
    if not PROJECT_ASSET_STORE_PATH.exists():
        return {"version": "0.2", "project": "UNKNOWN_PROJECT", "assets": []}
    return _read_json(PROJECT_ASSET_STORE_PATH)


def _technique_assets(store: dict[str, Any]) -> list[dict[str, Any]]:
    return [asset for asset in store.get("assets", []) if asset.get("family") == "techniques"]


def _job_by_id(job_id: str) -> dict[str, Any] | None:
    for job in load_job_queue().get("jobs", []):
        if job.get("job_id") == job_id:
            return job
    return None


def _positive_evidence_count(state: dict[str, Any]) -> int:
    index = load_or_build_rag_index(state)
    return len([item for item in index.get("items", []) if int(item.get("evidence_weight", 0)) > 0])


def _positive_evidence_ids(state: dict[str, Any]) -> list[str]:
    index = load_or_build_rag_index(state)
    return [
        str(item["source_dna_id"])
        for item in index.get("items", [])
        if int(item.get("evidence_weight", 0)) > 0
    ]


def _store_validation(store: dict[str, Any]) -> dict[str, Any]:
    return validate_creation_asset_store(store)


def build_producer_status(
    state: dict[str, Any],
    adapters: dict[str, Any],
) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    store = _project_store()
    job = _job_by_id(TECHNIQUES_JOB_ID) or {}
    naming_job = _job_by_id(NAMING_JOB_ID) or {}
    outbox_exists = (ROOT / TECHNIQUES_OUTBOX_PATH).exists()
    naming_outbox_exists = (ROOT / NAMING_OUTBOX_PATH).exists()
    technique_assets = _technique_assets(store)
    naming_seed_count = len(
        [asset for asset in store.get("assets", []) if asset.get("asset_id") in OWNED_NAMING_IDS]
    )
    family_counts = Counter(asset.get("family", "unknown") for asset in store.get("assets", []))
    return {
        "version": VERSION,
        "system_mode": system_status["operating_mode"],
        "content_progression": system_status["content_progression"],
        "supported_families": list(SUPPORTED_FAMILIES),
        "hermes_allowed": False,
        "owner_gate": {
            "required": system_status["owner_gate_required"],
            "status": system_status["owner_gate_status"],
        },
        "techniques": {
            "job_id": TECHNIQUES_JOB_ID,
            "job_state": job.get("state", "missing"),
            "job_validated": job.get("state") == "validated",
            "validated_outbox_path": TECHNIQUES_OUTBOX_PATH,
            "validated_outbox_exists": outbox_exists,
            "candidate_count": len(technique_assets),
            "owned_candidate_count": len(
                [asset for asset in technique_assets if asset.get("asset_id") in OWNED_TECHNIQUE_IDS]
            ),
            "positive_evidence_count": _positive_evidence_count(state),
        },
        "naming": {
            "job_id": NAMING_JOB_ID,
            "job_state": naming_job.get("state", "missing"),
            "job_validated": naming_job.get("state") == "validated",
            "validated_outbox_path": NAMING_OUTBOX_PATH,
            "validated_outbox_exists": naming_outbox_exists,
            "seed_count": naming_seed_count,
        },
        "project_asset_store": {
            "path": "system/creation_assets/project_assets.v0.2.json",
            "family_counts": dict(sorted(family_counts.items())),
            "validation": _store_validation(store),
        },
        "blocked_actions": [
            "write novel prose",
            "write combat scenes",
            "generate final technique tree",
            "execute-hermes",
            "execute-antigravity",
            "read novel_training_set/",
        ],
        "next_safe_action": (
            "Run produce-techniques after the techniques job is validated."
            if job.get("state") != "validated"
            else "Produce or inspect seed-level technique candidates."
        ),
    }


def _assert_no_forbidden_text(data: dict[str, Any]) -> None:
    encoded = json.dumps(data, ensure_ascii=False)
    for value in FORBIDDEN_TEXT:
        if value in encoded:
            raise RuntimeError(f"producer output contains forbidden text: {value}")


def _technique_candidate_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": candidate["asset_id"],
            "family": "techniques",
            "display_name": candidate["display_name"],
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": list(candidate["constraints"]),
            "technique": {
                "cost": candidate["cost"],
                "counter_ids": [],
                "ledger_state_cost_key": "lifespan_debt_balance",
                "measurable_decrement": 1,
                "backlash_state_modifier": "increase protagonist_exposure_rate or delayed debt",
                "required_auditing_role": "auditor_role_pending",
                "relic_exposure_coefficient": 0,
                "lifecycle_policy": {
                    "evolution": "evolve only after a validated ledger transition and evidence-backed function change",
                    "decay": "decay when cost, role, or map prerequisites are unmet",
                    "retirement": "retire when its counter path or debt function is resolved",
                },
                "originality_policy": "abstract function and cost; never copy source technique names, realms, or proprietary jargon",
            },
        }
        for candidate in TECHNIQUE_CANDIDATES
    ]


def _naming_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "naming_project_contract_seed",
            "family": "naming",
            "display_name": "Project Naming Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final naming dictionary",
                "do not use as prose generation output",
                "every derived name requires collision validation",
            ],
            "naming": {
                "semantic_field": "寿命、债务、账册、税序、火、秤的审计语义",
                "naming_roots": ["命", "账", "债", "算", "簿", "漏", "劫"],
                "form_rules": [
                    "角色与势力名称优先使用制度、职业或地域语义",
                    "道具与招式名称必须体现账务动作、代价或状态变化",
                    "境界与能力名称不得复用训练集的现成等级词或专名结构",
                    "每个名称必须保留来源机制与原创转译说明",
                ],
                "forbidden_collisions": ["至尊骨", "重瞳", "九秘", "掌天瓶", "春秋蝉", "魂殿"],
                "forbidden_terms": ["测名院", "无名者航路", "群岛无名碑", "海图擦除", "旧名碑逻辑"],
                "originality_policy": "只迁移抽象功能与叙事作用，不复制原作专名、词法模板或境界序列。",
            },
        }
    ]


def _npc_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "npcs_project_contract_seed",
            "family": "npcs",
            "display_name": "NPC Role Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final NPC roster",
                "no final names or dialogue",
                "every recurrence change requires state-ledger validation",
            ],
            "npc": {
                "role_class": "debt-auditing role taxonomy seed",
                "recurrence_policy": {
                    "map_transition": "re-enter only when the current map exposes a new ledger consequence",
                    "power_scaling": "scale by information, authority, and debt exposure before combat power",
                    "retirement_condition": "retire when the role's debt, witness, or trust function is resolved",
                },
                "faction_id": "faction_registry_pending",
                "information_state": "role-level information boundary only",
                "ledger_debt_balance": 0,
                "trust_metric": 0,
                "originality_policy": "Use systemic functions and state transitions, never copied identities, titles, or dialogue patterns.",
            },
        }
    ]


def _artifact_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "artifacts_project_contract_seed",
            "family": "artifacts",
            "display_name": "Artifact Lifecycle Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final item catalog",
                "no final physical description",
                "every benefit must map to a tracked cost or exposure state",
            ],
            "artifact": {
                "cost": "Every activation consumes a tracked life, debt, exposure, or trust state.",
                "upgrade_stage": "contract_seed",
                "lifecycle_policy": {
                    "acquisition": "enter the registry only with source evidence and a bounded acquisition condition",
                    "activation": "activate only when the linked state transition is explicit",
                    "dormancy": "become dormant when cost, exposure, or map conditions are unmet",
                    "retirement": "retire when its narrative function is resolved or its debt is unrecoverable",
                },
                "cost_and_limitation_rules": {
                    "usage_cost": "must name a ledger state key and a measurable decrement or debt increase",
                    "backlash": "must define delayed backlash or exposure, never cost-free progression",
                    "exposure_state_key": "artifact_exposure_rate",
                },
                "upgrade_path": {
                    "criteria": "upgrade only after a validated state transition and evidence-backed function change",
                    "materials": "tracked resources or obligations, not arbitrary treasure accumulation",
                    "state_transition": "seed -> active -> dormant or retired",
                },
                "visual_symbol_ledger": "visual symbol must reinforce ledger, debt, audit, fire, or scale semantics without copying source-object imagery",
                "originality_policy": "translate function and narrative pressure; never copy names, shapes, scenes, or exact abilities from source works",
            },
        }
    ]


def _upsert_assets(store: dict[str, Any], produced: list[dict[str, Any]]) -> dict[str, Any]:
    owned = {asset["asset_id"] for asset in produced}
    preserved = [
        asset
        for asset in store.get("assets", [])
        if asset.get("asset_id") not in owned
    ]
    updated = {**store, "assets": sorted([*preserved, *produced], key=lambda item: item["asset_id"])}
    return updated


def produce_technique_candidates(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    if job_id != TECHNIQUES_JOB_ID:
        raise RuntimeError(f"unsupported technique producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"techniques job must be validated before production: {job_id}")
    outbox_path = ROOT / TECHNIQUES_OUTBOX_PATH
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {TECHNIQUES_OUTBOX_PATH}")

    evidence_ids = _positive_evidence_ids(state)
    if len(evidence_ids) < 3:
        raise RuntimeError("technique producer requires at least three positive evidence items")
    source_refs = [
        TECHNIQUES_OUTBOX_PATH,
        *evidence_ids[:3],
    ]
    produced = _technique_candidate_assets(source_refs)
    candidate_payload = {"assets": produced}
    _assert_no_forbidden_text(candidate_payload)

    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _assert_no_forbidden_text(updated_store)
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "technique_asset_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def produce_naming_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    if job_id != NAMING_JOB_ID:
        raise RuntimeError(f"unsupported naming producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"naming job must be validated before production: {job_id}")
    outbox_path = ROOT / NAMING_OUTBOX_PATH
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {NAMING_OUTBOX_PATH}")
    source_refs = [NAMING_OUTBOX_PATH, *job.get("source_evidence_ids", [])[:3]]
    produced = _naming_seed_assets(source_refs)
    _assert_no_forbidden_text({"assets": produced})
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "naming_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def produce_npc_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    if job_id != NAMING_JOB_ID.replace("naming", "npcs"):
        raise RuntimeError(f"unsupported NPC producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"NPC job must be validated before production: {job_id}")
    outbox_path = ROOT / NAMING_OUTBOX_PATH.replace("naming", "npcs")
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _npc_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "npc_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def produce_artifact_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    expected_job_id = "job-v05-artifacts-antigravity-review"
    if job_id != expected_job_id:
        raise RuntimeError(f"unsupported artifact producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"artifact job must be validated before production: {job_id}")
    outbox_path = ROOT / "system/agent_ops/outbox/job-v05-artifacts-antigravity-review_validated.md"
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _artifact_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "artifact_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def _state_ledger_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "state_ledger_project_contract_seed",
            "family": "state_ledger",
            "display_name": "State Ledger Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a chapter-by-chapter event log",
                "no invented unreleased plot events",
                "every update must balance a tracked debit and credit",
            ],
            "state_ledger": {
                "state_key": "project_audit_balance",
                "value_type": "bounded_numeric_with_transition_reason",
                "audit_policy": {
                    "validation_rule": "every state change requires source, reason, delta, and affected asset IDs",
                    "transaction_boundary": "a state transaction closes only after downstream references resolve",
                    "balance_rule": "life, debt, reputation, exposure, and trust deltas must reconcile before promotion",
                },
                "retribution_triggers": [
                    "debt threshold crossing",
                    "exposure threshold crossing",
                    "unbalanced transaction",
                ],
                "tracking_metrics": [
                    "lifespan_debt_balance",
                    "protagonist_exposure_rate",
                    "community_trust_level",
                    "reincarnation_lifespan_count",
                ],
                "decay_policy": {
                    "decay_condition": "unresolved debt and exposure increase when a promised settlement is skipped",
                    "restoration_condition": "restoration requires a validated repayment, sacrifice, or trust repair transition",
                },
                "originality_policy": "abstract state mechanics only; never copy named meters, progression labels, or numeric systems from source works",
            },
        }
    ]


def produce_state_ledger_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    expected_job_id = "job-v05-state_ledger-antigravity-review"
    if job_id != expected_job_id:
        raise RuntimeError(f"unsupported state ledger producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"state ledger job must be validated before production: {job_id}")
    outbox_path = ROOT / "system/agent_ops/outbox/job-v05-state_ledger-antigravity-review_validated.md"
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _state_ledger_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "state_ledger_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def _emotional_bond_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "emotional_bonds_project_contract_seed",
            "family": "emotional_bonds",
            "display_name": "Emotional Bond Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final relationship arc",
                "no final dialogue or sacrifice scene",
                "trust changes require state-ledger evidence",
            ],
            "emotional_bond": {
                "bond_type": "trust-debt transition contract",
                "trust_state": "unresolved",
                "persona_trust_map": ["primary_persona:unresolved", "masked_persona:unresolved"],
                "lifespan_decay_rate": 0,
                "preservation_deadline": "requires explicit deadline state before activation",
                "karmic_debt_modifier": 0,
                "exposure_backlash_coefficient": 0,
                "transition_policy": "devoted, suspicious, and adversarial states must alter downstream role and faction behavior through validated transitions",
                "originality_policy": "translate relationship pressure into trust, debt, risk, and repair states; never copy iconic identities or backstory configurations",
            },
        }
    ]


def produce_emotional_bond_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    expected_job_id = "job-v05-emotional_bonds-antigravity-review"
    if job_id != expected_job_id:
        raise RuntimeError(f"unsupported emotional bond producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"emotional bond job must be validated before production: {job_id}")
    outbox_path = ROOT / "system/agent_ops/outbox/job-v05-emotional_bonds-antigravity-review_validated.md"
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _emotional_bond_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "emotional_bond_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def _foreshadowing_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "foreshadowing_project_contract_seed",
            "family": "foreshadowing",
            "display_name": "Foreshadowing Lifecycle Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final clue dictionary",
                "no new plot promises",
                "every payoff requires state-ledger evidence",
            ],
            "foreshadowing": {
                "surface_explanation": "initial clue presents a bounded ledger anomaly without confirming its cause",
                "payoff_stage": "contract_seed",
                "hidden_logic_key": "unresolved_audit_liability",
                "payoff_condition_ledger_state": "protagonist_exposure_rate and community_trust_level must satisfy the registered transition",
                "clue_exposure_risk": 0,
                "lifecycle_policy": {
                    "setup": "register one observable anomaly with source and state impact",
                    "misdirection": "allow only evidence-backed alternative explanations",
                    "reveal": "reveal only after the linked ledger condition is met",
                    "retirement": "retire after payoff and downstream references are reconciled",
                },
                "originality_policy": "abstract clue function and payoff pressure; never copy iconic objects, setups, names, or resolution scenes",
            },
        }
    ]


def produce_foreshadowing_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    expected_job_id = "job-v05-foreshadowing-antigravity-review"
    if job_id != expected_job_id:
        raise RuntimeError(f"unsupported foreshadowing producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"foreshadowing job must be validated before production: {job_id}")
    outbox_path = ROOT / "system/agent_ops/outbox/job-v05-foreshadowing-antigravity-review_validated.md"
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _foreshadowing_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "foreshadowing_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def _character_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "characters_project_contract_seed",
            "family": "characters",
            "display_name": "Character Growth Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final character card",
                "no final names or dialogue",
                "growth cannot be represented as a level-only ladder",
            ],
            "character": {
                "role": "ledger-bound protagonist growth contract",
                "growth_stage": "contract_seed",
                "debt_balance": 0,
                "exposure_rate": 0,
                "sanity_level": 0,
                "identity_masks": {
                    "max_active_masks": 0,
                    "exposure_parameter": "protagonist_exposure_rate",
                },
                "growth_policy": {
                    "transition_condition": "growth requires a validated debt-clearing or audit-resolution state transition",
                    "forbidden_shortcut": "no free power-up, copied realm ladder, or untracked inheritance jump",
                    "audit_resolution": "each growth stage must reconcile cost, trust, exposure, and consequence references",
                },
                "originality_policy": "abstract growth pressure and role function only; never copy names, identities, relationships, or progression titles from source works",
            },
        }
    ]


def produce_character_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    expected_job_id = "job-v05-characters-antigravity-review"
    if job_id != expected_job_id:
        raise RuntimeError(f"unsupported character producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"character job must be validated before production: {job_id}")
    outbox_path = ROOT / "system/agent_ops/outbox/job-v05-characters-antigravity-review_validated.md"
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _character_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "character_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }


def _faction_seed_assets(source_refs: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": "factions_project_contract_seed",
            "family": "factions",
            "display_name": "Faction Pressure Contract Seed",
            "lifecycle_state": "seed",
            "source_refs": source_refs,
            "relationships": [],
            "constraints": [
                "seed contract only",
                "not a final faction roster",
                "no named institutions or plot dossiers",
                "faction pressure must be ledger-backed",
            ],
            "faction": {
                "interest": "manage survival, debt collection, public legitimacy, and access to life resources",
                "pressure_level": 0,
                "tax_enforcement_role": "role contract pending original faction naming",
                "associated_ledger_states": ["protagonist_exposure_rate", "community_trust_level", "lifespan_debt_balance"],
                "cohort_capacity": 0,
                "threat_exposure_coefficient": 0,
                "lifecycle_policy": {
                    "establishment": "establish only when an interest, resource, authority, and ledger state are registered",
                    "alliance_shift": "shift alliance only after an interest or debt transition is validated",
                    "territorial_expansion": "expand with map evidence and increased exposure cost",
                    "retirement": "retire or dissolve when its pressure function and outstanding obligations are reconciled",
                },
                "originality_policy": "translate systemic interests and pressure functions; never copy faction names, institutions, or plot structures from source works",
            },
        }
    ]


def produce_faction_seed(state: dict[str, Any], job_id: str) -> dict[str, Any]:
    expected_job_id = "job-v05-factions-antigravity-review"
    if job_id != expected_job_id:
        raise RuntimeError(f"unsupported faction producer job: {job_id}")
    job = _job_by_id(job_id)
    if not job or job.get("state") != "validated":
        raise RuntimeError(f"faction job must be validated before production: {job_id}")
    outbox_path = ROOT / "system/agent_ops/outbox/job-v05-factions-antigravity-review_validated.md"
    if not outbox_path.exists():
        raise RuntimeError(f"validated Antigravity outbox is missing: {outbox_path}")
    source_refs = [str(outbox_path.relative_to(ROOT)), *job.get("source_evidence_ids", [])[:3]]
    produced = _faction_seed_assets(source_refs)
    store = _project_store()
    updated_store = _upsert_assets(store, produced)
    validation = validate_creation_asset_store(updated_store)
    if not validation["valid"]:
        return {
            "produced_count": 0,
            "asset_ids": [asset["asset_id"] for asset in produced],
            "store_validation": validation,
            "store_path": "system/creation_assets/project_assets.v0.2.json",
        }
    _write_json(PROJECT_ASSET_STORE_PATH, updated_store)
    return {
        "producer": "faction_contract_seed_producer",
        "version": VERSION,
        "job_id": job_id,
        "produced_count": len(produced),
        "asset_ids": [asset["asset_id"] for asset in produced],
        "store_validation": validation,
        "store_path": "system/creation_assets/project_assets.v0.2.json",
        "content_generation_allowed": False,
    }
