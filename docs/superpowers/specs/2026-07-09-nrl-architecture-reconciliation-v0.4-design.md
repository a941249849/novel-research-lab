# NRL Architecture Reconciliation v0.4 Design Spec

## Accepted Source Context

This spec is based on the Owner-approved reread of the ChatGPT conversation
`中文玄幻小说汇总` on 2026-07-09. The source conversation establishes that
Novel Research Lab was never meant to be a generic writing dashboard, an InkOS
clone, or a document pipeline.

The fixed identity is:

```text
Novel Research Lab =
基于中文热门长篇小说语料研究蒸馏的原创长篇小说创作引擎
```

The fixed top-level chain is:

```text
training corpus
  -> single-book decomposition
  -> cross-book mechanism distillation
  -> narrative law / mechanism library
  -> original project synthesis
  -> Story Bible
  -> long-form creation asset system
  -> outline / chapter planning
  -> draft
  -> review
  -> state ledger
  -> continuous long-form production
```

The InkOS-like inspiration is only the workbench shape: state, memory, agent
coordination, and project visibility. NRL's first-principle difference is
Corpus-to-Creation: research distilled from proven long-form novels must drive
original creation.

## Problem

The current repository is not empty. It already contains Phase 1 research
assets, Core7 promoted candidates, Phase 2 story assets, Runtime commands,
Owner Gate guardrails, and Studio v0.2/v0.3 UI work.

The failure mode is different:

```text
runtime/product/control-plane work advanced before the final source architecture
was reconciled and locked.
```

This created three visible problems:

- The Owner cannot tell whether the system architecture is final.
- `Studio`, `Runtime`, `Creation Assets`, and `Corpus Pipeline` read like
  adjacent layers rather than one coherent product architecture.
- v0.3 correctly introduced a Corpus-to-Creation pipeline contract, but it
  risks being mistaken for the whole architecture instead of one downstream
  implementation layer.

## Core Decision

v0.4 is an architecture reconciliation release, not a content phase.

It must make the source design explicit and machine-readable:

1. `Core7` small-batch experimentation is accepted as the calibration basis,
   not as final full-corpus completion.
2. The system is frozen in `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE` until the
   reconciled architecture is visible in Studio and runtime data.
3. v0.3 `Corpus-to-Creation Pipeline` remains valid, but is repositioned as one
   executable planning layer beneath the architecture.
4. The next production direction is not Phase 2F, not prose, and not Hermes.
   It is the long-form creation asset operating system backed by research
   evidence.

## Product Architecture Layers

The architecture is divided into ten layers. Each layer has an explicit owner,
status, and dependency boundary.

1. **Corpus Layer**
   - Raw `novel_training_set/` remains a protected input.
   - Studio and runtime commands must not freely read raw prose.
   - Only structured derivatives are available to normal operations.

2. **Single-Book Decomposition Layer**
   - Book DNA, Narrative DNA, and State Ledger derivatives represent per-book
     analysis.
   - Current state: Core7 has promoted assets; the remaining corpus includes
     stub or incomplete assets.

3. **Cross-Book Distillation Layer**
   - Mechanism notes, categories, feature matrices, and synthesis reports
     abstract repeatable craft mechanisms.
   - Current state: valuable research exists, but it is not yet a complete
     queryable mechanism engine.

4. **Research Asset Engine**
   - Indexes structured research assets with source paths, provenance, review
     status, and mechanism categories.
   - This is the bridge from reports to runtime-useful evidence.

5. **Original Project Synthesis Layer**
   - Turns distilled mechanisms into original project concepts, Story Bible,
     project premise, world logic, and thematic constraints.
   - Current project: `《借天改命账》`.

6. **Long-Form Creation Asset OS**
   - Productizes the asset families required for continuous long-form writing:
     characters, NPCs, factions, artifacts, techniques, naming, emotional
     bonds, foreshadowing, and state ledger.
   - This layer is currently the largest gap.

7. **Planning Pipeline**
   - Uses structured research evidence and creation schemas to plan one asset
     family at a time.
   - v0.3 belongs here. It may output schema-bound plans, not final creative
     assets.

8. **Agent Review and Production Layer**
   - Codex validates and orchestrates locally.
   - Antigravity provides manual external literary review.
   - Hermes remains paused, not removed; it is a later writer/literary
     enrichment module after explicit authorization.

9. **Runtime / Control Plane Layer**
   - Owns state reading, safe action calculation, validation, adapter modes,
     handoff contracts, and local APIs.
   - It does not replace source-of-truth state files.

10. **Studio Layer**
    - The visible system cockpit.
    - It must show architecture, current state, evidence, asset gaps, agent
      boundaries, safe actions, and Owner Gate without requiring chat
      explanation.

## Agent Role Contract

`Codex`

- Local system host.
- Engineering, runtime, validation, artifact indexing, Studio build, Git, and
  orchestration.
- Must not pretend to call external agents without a real adapter.

`Antigravity`

- Manual external literary review.
- Evaluates long-form vitality, originality, reader pull, structure, and
  whether the work has become process prose.
- Should not be the main execution driver.

`Hermes`

- Paused but retained.
- Later writer / literary enrichment / controlled creative generation module.
- Must not be called while architecture reconciliation and Owner Gate are
  active.

`Web GPT`

- Architecture review and source-context adjudication.
- Not a task dispatcher.

`Owner`

- Gate authority.
- Authorizes phase transitions, external agent use, and content production.

## v0.4 Runtime Data Contract

`studio-data` must add a backward-compatible `architecture_reconciliation`
section:

```json
{
  "architecture_reconciliation": {
    "version": "0.4",
    "source_context": {},
    "fixed_identity": {},
    "architecture_layers": [],
    "experiment_calibration": {},
    "implementation_alignment": {},
    "agent_role_contract": [],
    "current_mismatch_report": [],
    "production_readiness": {},
    "next_architecture_action": {}
  }
}
```

The section must be deterministic and read-only. It must derive current
runtime facts from existing files and hard-coded architecture constants from
this spec. It must not introduce a database.

## Studio v0.4 Requirements

Studio must expose architecture reconciliation as a first-class view in
Simplified Chinese.

Add or revise a view named:

```text
系统架构
```

The view must show:

- NRL fixed identity.
- Corpus-to-Creation chain.
- The ten architecture layers and their current status.
- Core7 small-batch experiment conclusion.
- The mismatch report explaining why current v0.3 is useful but insufficient.
- Agent role boundaries.
- Next architecture action.

The existing `生成管线` view may remain, but it must be visually and textually
clear that it is the Planning Pipeline layer, not the entire system.

## Runtime Interfaces

Add:

```bash
python3 system/runtime/nrl.py architecture-status
```

The command emits the same `architecture_reconciliation` object used by Studio.

`system-check` must include an `architecture_reconciliation` check that verifies:

- architecture status is version `0.4`;
- all ten architecture layers exist;
- v0.3 pipeline is classified as `planning_pipeline`, not as full architecture;
- Owner Gate remains active;
- Hermes remains `paused_not_removed`;
- no `novel_training_set/` path appears in the architecture payload.

## Guardrails

- No Phase 2F transition.
- No prose.
- No chapter draft.
- No final character cards, technique trees, naming dictionaries, item catalogs,
  or full asset dossiers.
- No Hermes execution.
- No Antigravity execution button.
- No raw `novel_training_set/` reads.
- No removal of v0.3 pipeline; it must be repositioned under the architecture.

## Acceptance

- `python3 system/runtime/nrl.py architecture-status` returns version `0.4`.
- `studio-data` includes `architecture_reconciliation`.
- `architecture_reconciliation.architecture_layers` contains exactly ten
  ordered layers.
- The `planning_pipeline` layer references v0.3 as a child implementation, not
  the whole architecture.
- The mismatch report explicitly states that the previous risk was
  runtime/pipeline work advancing ahead of source architecture reconciliation.
- Studio contains Chinese text for `系统架构`, `Corpus-to-Creation`,
  `Core7 小批量试验`, `Hermes: paused_not_removed`, and `Owner Gate`.
- `system-status` remains `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.
- `advance` remains blocked at Owner Gate.
- Existing v0.2/v0.3 runtime and frontend checks remain green.
