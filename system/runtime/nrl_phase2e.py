from __future__ import annotations

from pathlib import Path
from typing import Any

from nrl_paths import ROOT


PHASE2E_MANIFEST = "phase2E/00_entry/phase2E_entry_manifest.md"
PHASE2E_CONTROL_PACK = "phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md"


def latest_phase2e_acceptance(decisions: list[dict[str, Any]]) -> dict[str, Any] | None:
    for decision in reversed(decisions):
        if decision.get("decision_type") != "accept_review":
            continue
        scopes = set(decision.get("authorized_scope", []))
        if "prepare_phase2e_entry" in scopes:
            return decision
    return None


def read_text_if_exists(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def render_phase2e_manifest(decision: dict[str, Any], review_text: str) -> str:
    return f"""# Phase 2E Entry Manifest

## Owner Gate

- decision_id: {decision["decision_id"]}
- decision_type: {decision["decision_type"]}
- owner_note: {decision.get("owner_note", "")}
- accepted_review_condition: ACCEPT_WITH_WARNINGS

## Authorized Scope

{chr(10).join(f"- {scope}" for scope in decision.get("authorized_scope", []))}

## Forbidden Scope

{chr(10).join(f"- {scope}" for scope in decision.get("forbidden_scope", []))}

## Phase 2E Required Conditions

- Incorporate Antigravity's required fixes before prose.
- Vary pacing loops; do not repeat identical investigation-conflict-reversal structures.
- Transmute evidence into sensory supernatural images and action pressure.
- Make protagonist backlash visible and physical.
- Remove engineering/schema terminology from chapter-facing plans.
- Do not write novel prose.
- Do not write the first chapter.

## Antigravity Review Source

```text
{review_text}
```
"""


def prepare_phase2e_entry(state: dict[str, Any], decision: dict[str, Any], now: str) -> dict[str, Any]:
    review_path = "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
    review_text = read_text_if_exists(review_path)
    manifest_path = ROOT / PHASE2E_MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(render_phase2e_manifest(decision, review_text), encoding="utf-8")

    state["previous_story_phase"] = "Phase 2D"
    state["current_phase"] = "Phase 2E"
    state["current_subphase"] = "Chapter Plan Entry Preparation"
    state["phase_status"] = "PHASE2E_ENTRY_PREPARATION_AUTHORIZED"
    state["last_completed_mission"] = "Phase 2D Antigravity Outline Tree Review"
    state["next_recommended_mission"] = "Phase 2E Chapter Plan Entry Preparation"
    state["owner_gate_required"] = False
    state["owner_gate_status"] = "ACCEPTED_WITH_WARNINGS_FOR_PHASE2E_ENTRY"
    state["allowed_next_agents"] = ["Codex"]
    state["validation_status"] = "PENDING_PHASE2E_ENTRY_PREPARATION"
    state["review_status"] = "ANTIGRAVITY_REVIEW_ACCEPTED_WITH_WARNINGS"
    state["blocked_actions"] = [
        "write novel prose",
        "write first chapter",
        "generate full character cards",
        "bypass Phase 2E planning constraints",
        "ignore Antigravity required fixes",
        "freely read novel_training_set",
    ]
    artifacts = state.setdefault("key_artifacts", [])
    for artifact in [
        {
            "name": "Phase 2D Antigravity Outline Tree Review",
            "path": review_path,
            "status": "PASS_WITH_WARNINGS_ACCEPTED_BY_OWNER",
        },
        {
            "name": "Phase 2E Entry Manifest",
            "path": PHASE2E_MANIFEST,
            "status": "prepared",
        },
    ]:
        if not any(item.get("path") == artifact["path"] for item in artifacts):
            artifacts.append(artifact)
    notes = state.setdefault("notes", [])
    note = f"Owner Gate accepted Antigravity review with warnings via {decision['decision_id']}."
    if note not in notes:
        notes.append(note)
    state["updated_at"] = now
    return {
        "manifest_path": PHASE2E_MANIFEST,
        "owner_gate_decision_id": decision["decision_id"],
    }


def render_phase2e_control_pack(entry_manifest: str) -> str:
    return f"""# Phase 2E Chapter Plan Control Pack

## Purpose

Prepare controlled chapter planning for Volume 1 without writing prose,
without writing the first chapter, and without generating full character cards.

## Required Antigravity Fix Integration

- Vary pacing loops across arc clusters.
- Convert evidence into sensory supernatural pressure, not paperwork.
- Make protagonist backlash visible, physical, and escalating.
- Preserve local emotional anchors before scaling to prefecture/state scope.
- Remove engineering/schema terminology from reader-facing chapter plans.

## Planning Output Boundary

Allowed in the next planning mission:

- chapter-plan constraints
- arc-level pacing variation map
- sensory evidence translation rules
- backlash escalation rules
- validation checklist

Forbidden in the next planning mission:

- Do not write novel prose.
- Do not write the first chapter.
- Do not create full character cards.
- Do not bypass Antigravity warning integration.
- Do not read the raw source corpus freely.

## Acceptance Checklist

- Every planned arc must have a distinct conflict/release pattern.
- Evidence beats must be expressed as fantasy action or sensory images.
- Backlash must be visible on the protagonist's body or behavior.
- Engineering terms such as ledger seeds, satisfaction loops, and state-ledger labels must stay out of reader-facing chapter plans.
- Any future Hermes handoff remains disabled until explicitly reauthorized.

## Source Entry Manifest

```text
{entry_manifest}
```
"""


def prepare_phase2e_planning_package(state: dict[str, Any], now: str) -> dict[str, Any]:
    manifest_text = read_text_if_exists(PHASE2E_MANIFEST)
    package_path = ROOT / PHASE2E_CONTROL_PACK
    package_path.parent.mkdir(parents=True, exist_ok=True)
    package_path.write_text(render_phase2e_control_pack(manifest_text), encoding="utf-8")

    state["current_subphase"] = "Chapter Plan Control Package"
    state["phase_status"] = "PHASE2E_PLANNING_PACKAGE_READY"
    state["next_recommended_mission"] = "Phase 2E Controlled Chapter Planning"
    state["validation_status"] = "PENDING_PHASE2E_CONTROLLED_PLANNING"
    state["review_status"] = "ANTIGRAVITY_WARNINGS_INTEGRATED_IN_CONTROL_PACK"
    artifacts = state.setdefault("key_artifacts", [])
    artifact = {
        "name": "Phase 2E Chapter Plan Control Pack",
        "path": PHASE2E_CONTROL_PACK,
        "status": "prepared",
    }
    if not any(item.get("path") == artifact["path"] for item in artifacts):
        artifacts.append(artifact)
    notes = state.setdefault("notes", [])
    note = "Phase 2E chapter planning control pack prepared; prose remains blocked."
    if note not in notes:
        notes.append(note)
    state["updated_at"] = now
    return {"control_pack_path": PHASE2E_CONTROL_PACK}
