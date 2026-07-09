# NRL Corpus-to-Creation v0.3 Design Spec

## Architecture Decision

The Novel Research Lab architecture is accepted for production implementation
as a Corpus-to-Creation system. The fixed product direction is:

```text
structured corpus derivatives
  -> research asset retrieval
  -> creation asset contract planning
  -> consistency validation
  -> agent/manual review
  -> Owner Gate
  -> authorized prose production
```

This does not mean every subsystem is already implemented. It means the system
identity, boundaries, sources of truth, agent roles, and safety gates are now
the baseline architecture. Future work should implement this architecture
instead of re-litigating whether NRL is a generic writing app, an InkOS clone,
or a manual file handoff pile.

## Product Goal

v0.3 turns Control Plane v0.2 from a status dashboard into the first executable
pipeline layer. The pipeline must connect reviewed research assets to the nine
creation asset families without generating final story content.

Within five minutes, the Owner should be able to answer:

1. Which creation asset family should be built next?
2. Which research assets support that family?
3. Which schema and validation gates constrain the output?
4. Which agent or manual review step would be needed later?
5. Which actions remain forbidden while Owner Gate is active?

## Hard Boundaries

- Phase 2E remains frozen at Owner Gate.
- No Phase 2F transition.
- No novel prose, chapter draft, final character card, final NPC sheet,
  faction dossier, technique tree, naming dictionary, item catalog, or state
  ledger content is generated in v0.3.
- `novel_training_set/` remains off-limits.
- Hermes remains `paused_not_removed`.
- Antigravity remains manual external review.
- Studio can show pipeline commands and read-only plans, but it cannot call
  `advance`, Hermes, or Antigravity.

## Runtime Sources Of Truth

- `system/mission_controller/current_phase_state.json`
- `system/runtime/mission_registry.json`
- `system/runtime/agent_adapters.json`
- `system/control_plane/capability_roadmap.v0.2.json`
- `system/creation_assets/creation_asset_registry.v0.1.json`
- `system/creation_assets/schemas/*.schema.json`
- Structured Phase 1 research assets indexed through `research-assets`

No database is introduced in v0.3.

## Pipeline Contract

The v0.3 pipeline is read-only and deterministic. It produces pipeline plans,
not creative content. A pipeline plan contains:

- `pipeline_id`
- `project`
- `mode`
- `target_family`
- `stage_statuses`
- `research_query`
- `evidence_requirements`
- `schema_contract`
- `validation_gates`
- `agent_review_policy`
- `owner_gate`
- `forbidden_actions`

The pipeline must return the same output for the same runtime state and family.

## Creation Family Mapping

Each creation asset family maps to research asset needs:

- `characters`: book DNA, narrative DNA, emotional mechanisms, state ledger
- `npcs`: narrative DNA, mechanism examples, state ledger
- `factions`: book DNA, narrative DNA, organization mechanisms
- `artifacts`: mechanism examples, resource mechanisms, state ledger
- `techniques`: upgrade mechanisms, cost/counter mechanisms, state ledger
- `naming`: book DNA, narrative DNA, mechanism naming patterns
- `emotional_bonds`: narrative DNA, emotional/philosophical mechanisms
- `foreshadowing`: narrative DNA, mystery mechanisms, state ledger
- `state_ledger`: all structured family outputs and Phase 1 state ledgers

Plans should include enough evidence to support drafting later, but v0.3 does
not draft the assets.

## CLI Interfaces

Add:

```text
pipeline-status
pipeline-plan --family <asset_family>
pipeline-plan --next
```

`pipeline-status` reports the stage graph, current next family, and all blocked
production steps. `pipeline-plan` emits a single JSON plan for a requested
family or for the next recommended family.

## Studio Integration

Studio adds a sixth Chinese view:

```text
生成管线
```

The view shows:

- pipeline stage graph
- next recommended asset family
- evidence requirements
- validation gates
- forbidden production actions

It uses Astryx lists/tables/tokens in the existing AppShell. It remains
read-only and must not expose execution controls for creative generation.

## Acceptance

- `pipeline-status` is deterministic and contains one next family.
- `pipeline-plan --next` returns a plan for the same next family.
- Every family can produce a plan.
- Every plan references an existing Draft-07 schema path.
- Every plan uses only structured research asset paths and excludes
  `novel_training_set/`.
- Plans include validation gates for schema, references, naming, lifecycle,
  source evidence, and Owner Gate.
- `studio-data` includes a `corpus_pipeline` section.
- Studio shows `生成管线` and no creative execution buttons.
- Existing v0.2 checks remain green.
