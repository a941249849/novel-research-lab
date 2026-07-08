# NRL Control Plane v0.2 Design Spec

## Baseline

NRL Studio v0.1 proved that the runtime state can be rendered, but it is still
an English, read-only snapshot composed as a long stack of cards. Control Plane
v0.2 turns that shell into the Chinese operational surface for the existing
Corpus-to-Creation system while keeping Phase 2E frozen at Owner Gate.

## Goal

Deliver one coherent local control plane that answers five questions without
requiring the Owner to inspect phase directories:

1. Which NRL capabilities exist and which are blocked?
2. Which research assets are available and where did they come from?
3. Which long-form creation asset contracts are ready?
4. Which agent can act, and under which constraints?
5. What is the single next safe system action?

## System Boundaries

- `current_phase_state.json`, `mission_registry.json`, and
  `agent_adapters.json` remain runtime sources of truth.
- No database is introduced.
- Phase 1 structured assets may be indexed; raw `novel_training_set/` files
  must never be read or exposed.
- No Phase 2F transition, prose, chapter plan, final character card, NPC sheet,
  faction dossier, technique tree, naming dictionary, or item catalog is
  generated.
- Hermes remains `paused_not_removed`; Hermes and Antigravity remain
  `manual_handoff` and cannot be executed from Studio.

## Capability Roadmap

The control plane owns a machine-readable roadmap with these capabilities:
corpus engineering, single-book decomposition, cross-book mechanism
distillation, research asset retrieval, creation asset contracts, consistency
validation, agent orchestration, and prose production.

Capability states are `missing`, `contract_ready`, `data_ready`, `runnable`,
and `blocked`. Dependencies and evidence paths determine state. The first
incomplete capability whose dependencies are satisfied becomes the unique next
safe action. Prose production remains blocked while Owner Gate is pending.

## Research Asset Catalog

The catalog indexes only structured Phase 1 outputs:

- Book DNA
- Narrative DNA
- State Ledger
- Core7 promoted candidates
- Mechanism Library

Each entry records a stable ID, title, asset type, source path, review state,
promotion state, and provenance class (`stub`, `candidate`, or `promoted`).
The runtime supports filters by title, asset type, mechanism category, and
review state. Missing or malformed paths fail validation.

## Creation Asset Contracts

Draft-07 schemas cover characters, NPCs, factions, artifacts, techniques,
naming, emotional bonds, foreshadowing, and the state ledger. A shared
envelope defines ID, display name, lifecycle state, source references,
relationships, and constraints. Family schemas add only domain fields needed
for consistency checks.

An empty project registry is the canonical instance store for v0.2. Validation
rejects duplicate IDs, unresolved references, duplicate normalized names,
invalid lifecycle transitions, and family/status mismatches. Test fixtures may
contain synthetic examples; production artifacts must remain content-empty.

## Runtime Interfaces

Add these commands:

```text
hardening-status
research-assets
creation-schemas
validate-creation-assets
system-check
studio-serve --port 4173
```

`studio-data` remains backward compatible and adds `control_plane`,
`capability_roadmap`, `research_asset_catalog`, `creation_schema_registry`, and
`safe_action_catalog`.

The local Studio server exposes:

- `GET /api/studio-data`
- `GET /api/research-assets`
- `GET /api/creation-schemas`
- `POST /api/actions/system-check`
- `POST /api/actions/validate-state`

POST actions are selected from a fixed allowlist and call Python functions
directly. Arbitrary commands, `advance`, and external agent execution are not
accepted.

## Studio Information Architecture

The default language is Simplified Chinese. Technical identifiers, commands,
and paths remain unchanged. The Astryx shell uses a SideNav with five views:

1. 系统总览
2. 研究资产
3. 创作资产
4. Agent 与任务
5. 运行状态与 Owner Gate

The UI uses dense tables, lists, status tokens, banners, and a detail panel.
Cards are limited to small summary widgets. The Owner Gate warning remains
visible in every view. Astryx components and tokens are the only visual system.

`studio-build` remains the offline snapshot command. `studio-serve` is the
normal local entry point and serves live runtime data.

## Acceptance

- All existing runtime tests continue to pass.
- Roadmap calculation returns one deterministic next safe action.
- The research catalog contains no raw corpus path.
- All nine Draft-07 schemas pass meta-validation.
- Positive and negative creation asset fixtures exercise reference, duplicate,
  lifecycle, naming, and status validation.
- Studio APIs reject unknown methods, paths, and action names.
- `system-status` remains `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.
- `advance` remains blocked at Owner Gate.
- The Chinese Studio builds, passes `astryx doctor`, and has no overlap or
  overflow at 1440x900 and 390x844.
