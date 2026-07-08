# NRL Studio v0.1 Design Spec

## Baseline

The accepted product baseline is the web-GPT diagnosis supplied by the Owner on 2026-07-09:

- Novel Research Lab is not an InkOS clone and not a generic AI writing tool.
- Novel Research Lab is a Corpus-to-Creation engine: corpus reading, single-book decomposition, cross-book mechanism distillation, narrative law library, original project synthesis, story bible, outline, chapter planning, draft, review, and state ledger.
- The current repository has research assets, phase governance, and a runtime MVP, but it lacks a visible product control surface.
- The immediate deliverable is a read-only local dashboard: `Novel Research Lab Studio v0.1`.

## Goal

Build a first visible product shell that lets the Owner understand the system identity, current state, agent roles, artifact map, creative coverage gaps, runtime state, next safe action, and Owner Gate within five minutes.

## Hard Non-Goals

- Do not progress to Phase 2F.
- Do not write novel prose.
- Do not write a chapter plan as a content deliverable.
- Do not generate full character cards.
- Do not call Hermes.
- Do not call Antigravity.
- Do not read raw `novel_training_set/` files.
- Do not add an independent database or replace `current_phase_state.json` / `mission_registry.json` as source of truth.

## Product Shape

Studio v0.1 is a dense operational dashboard, not a landing page. It is read-only. It may show command strings and status guidance, but it must not mutate runtime state or call external agents.

The dashboard must include eight sections:

1. System Identity
   - Show `Novel Research Lab`.
   - Show the Corpus-to-Creation identity.
   - Make clear that this is not a generic writing app, not an InkOS clone, and not a document pipeline.
2. Current Project
   - Show selected project, current phase, subphase, phase status, system mode, and content progression state.
   - Use the current Phase 2E Owner Gate pending state as the sample state.
3. Agent Panel
   - Codex: local runtime host, engineering, validation, orchestration.
   - Antigravity: manual external literary review.
   - Hermes: `paused_not_removed`, later writer or literary enrichment only after explicit authorization.
   - Web GPT: architecture review only, not task dispatcher.
   - Owner: gate authority.
4. Artifact Map
   - Show Corpus, Mechanisms, Grand Synthesis, Story Bible, Outline Tree, Planning Pack, Validation Reports, Review Reports, and State Ledger.
   - Derive artifact status from the runtime state and known phase assets where possible.
5. Creation Coverage Matrix
   - Show long-form asset coverage honestly for characters, NPCs, factions, artifacts, techniques, naming, emotional bonds, foreshadowing, and state ledger.
   - Initial statuses must include missing, seed, or partial; do not mark the long-form asset system complete.
6. Runtime Status
   - Show state validity command, mission registry status, adapter modes, handoff state, expected output, and blocked actions.
7. Next Safe Action
   - Show that content progression is frozen at Owner Gate.
   - Recommend Studio/system hardening instead of content progression while the Owner Gate is pending.
8. Owner Gate
   - Show whether Owner Gate is required, current gate status, authorization scope, forbidden scope, and expiry/decision boundaries.

## Runtime Data Contract

Add a read-only `studio-data` runtime command that emits one JSON object with these top-level keys:

- `system_identity`
- `current_project`
- `agent_panel`
- `artifact_map`
- `creation_coverage_matrix`
- `runtime_status`
- `next_safe_action`
- `owner_gate`

The command must assemble data from:

- `system/mission_controller/current_phase_state.json`
- `system/runtime/mission_registry.json`
- `system/runtime/agent_adapters.json`
- derived `system-status` logic

The data contract should be simple and stable enough for a React dashboard to render without creative interpretation.

## Frontend Requirements

- Create the only frontend package under `apps/studio/`.
- Use Vite + React + Astryx.
- Install and initialize Astryx only inside `apps/studio/`.
- Use Astryx tokens/components for the dashboard surface.
- Render a dense product dashboard, not a marketing hero.
- Read Studio data from a generated JSON asset.
- Build output must be copied to `system/runtime/studio/` by `studio-build`.

## Runtime Integration

`python3 system/runtime/nrl.py studio-build` must:

1. Generate current Studio data.
2. Provide it to `apps/studio/`.
3. Build the React app.
4. Copy the built output into `system/runtime/studio/`.

A static fallback is allowed only when the frontend build is genuinely unavailable during development. Once `apps/studio/` exists and dependencies are installed, frontend build failure must be surfaced instead of hidden.

## Guardrails

- `advance` remains blocked at Owner Gate.
- No stale Owner Gate decision reuse.
- Studio must not create novel content artifacts.
- Studio must not directly execute Hermes or Antigravity.
- Studio must not read raw corpus files.

## Acceptance Checks

- `python3 system/runtime/nrl.py studio-data` returns all eight required sections.
- `python3 system/runtime/nrl.py system-status` still reports `SYSTEM_HARDENING` and `FROZEN_AT_OWNER_GATE` for the current Owner Gate pending state.
- `python3 system/runtime/nrl.py advance` still stops at Owner Gate.
- `python3 system/runtime/nrl.py studio-build` produces a built Studio under `system/runtime/studio/`.
- Built Studio contains `Novel Research Lab`, `Corpus-to-Creation`, `SYSTEM_HARDENING`, `Hermes: paused_not_removed`, `Creation Coverage Matrix`, and `Owner Gate`.
