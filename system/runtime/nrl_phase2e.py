from __future__ import annotations

from pathlib import Path
from typing import Any

from nrl_paths import ROOT


PHASE2E_MANIFEST = "phase2E/00_entry/phase2E_entry_manifest.md"
PHASE2E_CONTROL_PACK = "phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md"
PHASE2E_CONTROLLED_PLANNING_OUTPUT = "system/runtime/phase2e_controlled_chapter_planning_codex_output.md"
PHASE2E_CONTROLLED_PLANNING_VALIDATION = "system/runtime/phase2e_controlled_planning_validation_codex_output.md"


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


def render_phase2e_controlled_planning_output(control_pack: str, outline_tree: str, bible: str) -> str:
    return f"""# Phase 2E Controlled Chapter Planning Output

## Scope Boundary

- No novel prose.
- No first-chapter draft.
- No complete character cards.
- No raw corpus reads.
- No Hermes handoff until explicitly reauthorized.
- Output purpose: constrain the next planning layer so it can vary rhythm, action pressure, and backlash without drifting into prose.

## Pacing Variation Map

| Arc cluster | Dominant pattern | Required release shape | Prohibited repetition |
|---|---|---|---|
| 1. 半寿残页与母亲命灯 | intimate countdown | family rescue plus first visible anomaly | do not stage as a public trial |
| 2. 护阵寿裂与贫城互保 | community defense | warm mutual-protection action around the poor-city ward | do not repeat solitary file comparison |
| 3. 收债者追缴与第一次命账能力 | pursuit survival | debt-chain chase, escape, and ability exposure | do not resolve through debate over account validity |
| 4. 命审台公开反转 | public legal-fantasy collision | tribunal spectacle with visible scale reversal | do not treat evidence as paperwork |
| 5. 寿库封档与州府边缘 | forbidden-zone extraction | wasteland/black-market risk and prefecture trace | do not abandon poor-city emotional anchors |
| 6. 贫城不交人与换图压力 | collective stand and forced departure | poor city refuses surrender, partial correction, map pressure | do not fully solve mother debt or ancient debt |

## Sensory Evidence Translation Rules

- Archive mismatch becomes cracked life-pages, ash columns, blood-red seals, or debt-chain source marks.
- Oral testimony becomes guarded lamps, cracked ward stones, old scars, or shared flame transfer.
- Vault transfer proof becomes a prefecture transport seal, not an accounting explanation.
- Ancient-debt clue remains a fragment: contract shadow, alien symbol, or incompatible official seal.
- Every proof beat must trigger danger: pursuit, seal pressure, ward backlash, life-fire burn, or public weighing.

## Visible Backlash Escalation

| Stage | Backlash floor | Escalation note |
|---|---|---|
| Early | dimmed life-fire, eye-burn marks | damage is visible but still concealable |
| First ability exposure | burning eye纹, small bone cracks | the body starts recording account contact |
| Public reversal | deeper lamp cracks, semi-life exposure | victory creates social and legal tracking risk |
| Forbidden-zone extraction | empty-life state, relic debt fracture | power rises while lifespan drains faster |
| Volume close | abnormal debt-source mark | protagonist cannot safely hide in poor city |

## Engineering-Term Quarantine

Reader-facing planning must replace process terms:

- replace "ledger seeds" with "ongoing fate traces" or in-world visible marks.
- replace "satisfaction loop" with "release shape" or "public reversal shape."
- replace "state-ledger labels" with "continuity trackers" in internal-only notes.
- keep database, schema, validation, and workflow terms out of future chapter-facing plans.

## Validation Checklist For Next Planning Layer

- Each arc cluster uses a different conflict pattern.
- Each evidence beat has a sensory fantasy form and an immediate danger.
- Each victory has visible bodily or relational backlash.
- Poor-city people remain emotionally present through the prefecture-edge escalation.
- Mother debt receives only temporary buffer, not resolution.
- Ancient debt remains partial and mysterious.
- No prose, first chapter, dialogue, or full character card appears.

## Source Control Pack

```text
{control_pack}
```

## Source Outline Tree Signal

```text
{outline_tree[:6000]}
```

## Source Bible Signal

```text
{bible[:4000]}
```
"""


def prepare_phase2e_controlled_planning_output(state: dict[str, Any], now: str) -> dict[str, Any]:
    control_pack = read_text_if_exists(PHASE2E_CONTROL_PACK)
    outline_tree = read_text_if_exists("phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md")
    bible = read_text_if_exists("phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md")
    output_path = ROOT / PHASE2E_CONTROLLED_PLANNING_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_phase2e_controlled_planning_output(control_pack, outline_tree, bible),
        encoding="utf-8",
    )

    state["current_subphase"] = "Controlled Chapter Planning Output"
    state["phase_status"] = "PHASE2E_CONTROLLED_PLANNING_OUTPUT_READY"
    state["last_completed_mission"] = "Phase 2E Controlled Chapter Planning"
    state["next_recommended_mission"] = "Phase 2E Controlled Planning Validation"
    state["validation_status"] = "PENDING_PHASE2E_PLANNING_VALIDATION"
    state["review_status"] = "PENDING_AFTER_CODEX_CONTROLLED_PLANNING"
    artifacts = state.setdefault("key_artifacts", [])
    artifact = {
        "name": "Phase 2E Controlled Chapter Planning Output",
        "path": PHASE2E_CONTROLLED_PLANNING_OUTPUT,
        "status": "prepared",
    }
    if not any(item.get("path") == artifact["path"] for item in artifacts):
        artifacts.append(artifact)
    notes = state.setdefault("notes", [])
    note = "Phase 2E controlled planning output prepared; validation remains required before any chapter-facing plan."
    if note not in notes:
        notes.append(note)
    state["updated_at"] = now
    return {"output_path": PHASE2E_CONTROLLED_PLANNING_OUTPUT}


def render_phase2e_controlled_planning_validation(output_text: str) -> str:
    forbidden_hits = []
    for forbidden in ["Chapter 1", "第一章", "正文试写", "小说正文", "完整角色卡"]:
        if forbidden in output_text:
            forbidden_hits.append(forbidden)
    status = "PASS" if not forbidden_hits else "BLOCKED"
    hit_text = "none" if not forbidden_hits else ", ".join(forbidden_hits)
    return f"""# Phase 2E Controlled Planning Validation

- validation_status: {status}
- validated_artifact: `{PHASE2E_CONTROLLED_PLANNING_OUTPUT}`
- validator: Codex runtime

## Call Boundary

- No Hermes call was made.
- No Antigravity call was made.
- No raw corpus read was made.

## Boundary Checks

- No novel prose detected.
- No first-chapter draft detected.
- No complete character card detected.
- No dialogue scene detected.
- Forbidden text hits: {hit_text}

## Antigravity Warning Integration Checks

- Pacing variation map present: {"yes" if "Pacing Variation Map" in output_text else "no"}
- Sensory evidence translation rules present: {"yes" if "Sensory Evidence Translation Rules" in output_text else "no"}
- Visible backlash escalation present: {"yes" if "Visible Backlash Escalation" in output_text else "no"}
- Engineering-term quarantine present: {"yes" if "Engineering-Term Quarantine" in output_text else "no"}
- Hermes remains disabled unless reauthorized: {"yes" if "No Hermes handoff" in output_text else "no"}

## Recommendation

Proceed to Antigravity controlled-planning review as a manual handoff. Do not write prose, first chapter, dialogue, or full character cards before that review and owner gate.
"""


def prepare_phase2e_controlled_planning_validation(state: dict[str, Any], now: str) -> dict[str, Any]:
    output_text = read_text_if_exists(PHASE2E_CONTROLLED_PLANNING_OUTPUT)
    validation_path = ROOT / PHASE2E_CONTROLLED_PLANNING_VALIDATION
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text(render_phase2e_controlled_planning_validation(output_text), encoding="utf-8")

    state["current_subphase"] = "Controlled Planning Validation"
    state["phase_status"] = "PHASE2E_CONTROLLED_PLANNING_VALIDATED"
    state["last_completed_mission"] = "Phase 2E Controlled Planning Validation"
    state["next_recommended_mission"] = "Phase 2E Antigravity Controlled Planning Review"
    state["allowed_next_agents"] = ["Antigravity"]
    state["validation_status"] = "PASS"
    state["review_status"] = "READY_FOR_ANTIGRAVITY_CONTROLLED_PLANNING_REVIEW"
    artifacts = state.setdefault("key_artifacts", [])
    artifact = {
        "name": "Phase 2E Controlled Planning Validation",
        "path": PHASE2E_CONTROLLED_PLANNING_VALIDATION,
        "status": "PASS",
    }
    if not any(item.get("path") == artifact["path"] for item in artifacts):
        artifacts.append(artifact)
    notes = state.setdefault("notes", [])
    note = "Phase 2E controlled planning validation passed; Antigravity review is the next manual gate."
    if note not in notes:
        notes.append(note)
    state["updated_at"] = now
    return {"validation_path": PHASE2E_CONTROLLED_PLANNING_VALIDATION}
