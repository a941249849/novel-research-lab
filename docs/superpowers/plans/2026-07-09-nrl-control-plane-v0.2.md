# NRL Control Plane v0.2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a Chinese, live NRL control plane backed by capability, research asset, and creation asset contracts without advancing story content.

**Architecture:** Extend the Python runtime with three focused read/validation modules and a fixed-route local HTTP server. Aggregate their outputs through the backward-compatible Studio data contract, then replace the card stack with an Astryx SideNav console.

**Tech Stack:** Python 3 standard library, jsonschema Draft-07, unittest, React 19, TypeScript, Vite, Astryx 0.1.4.

## Global Constraints

- Keep Phase 2E frozen at Owner Gate.
- Do not read `novel_training_set/`.
- Do not generate prose or final creative assets.
- Do not call Hermes or Antigravity.
- Keep current runtime state files as sources of truth.
- Use TDD for every behavior change.

---

### Task 1: Capability Roadmap

**Files:**
- Create: `system/control_plane/capability_roadmap.v0.2.json`
- Create: `system/runtime/nrl_capabilities.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_control_plane_v02.py`

**Interfaces:**
- Produces: `build_hardening_status(state, adapters) -> dict`
- Produces CLI: `hardening-status`

- [ ] Write tests for allowed states, evidence, dependency order, and the unique next safe action.
- [ ] Run the focused tests and confirm they fail because the module and CLI are absent.
- [ ] Implement roadmap loading, evidence checks, dependency evaluation, and CLI wiring.
- [ ] Run focused and existing runtime tests.
- [ ] Commit the capability roadmap slice.

### Task 2: Research Asset Catalog

**Files:**
- Create: `system/runtime/nrl_research_assets.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_control_plane_v02.py`

**Interfaces:**
- Produces: `build_research_asset_catalog(filters=None) -> dict`
- Produces CLI: `research-assets --title --asset-type --category --review-state`

- [ ] Write failing tests for structured Phase 1 discovery, provenance, filters, and raw-corpus exclusion.
- [ ] Implement deterministic catalog discovery without reading source contents except structured manifests needed for category metadata.
- [ ] Validate every returned source path and sort output by stable ID.
- [ ] Run focused and existing runtime tests.
- [ ] Commit the research catalog slice.

### Task 3: Creation Asset Schemas

**Files:**
- Create: `system/creation_assets/schemas/*.schema.json`
- Create: `system/creation_assets/project_assets.v0.2.json`
- Create: `system/runtime/nrl_creation_schemas.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_control_plane_v02.py`

**Interfaces:**
- Produces: `build_creation_schema_registry() -> dict`
- Produces: `validate_creation_asset_store(store=None) -> dict`
- Produces CLI: `creation-schemas`, `validate-creation-assets`

- [ ] Write failing meta-schema and nine-family coverage tests.
- [ ] Write failing positive/negative validation tests for duplicates, references, normalized names, lifecycle transitions, and family/status consistency.
- [ ] Add the shared envelope, nine family schemas, and empty project store.
- [ ] Implement schema registry and cross-asset validation.
- [ ] Run focused and existing runtime tests.
- [ ] Commit the creation contract slice.

### Task 4: Control Plane Aggregation And System Check

**Files:**
- Modify: `system/runtime/nrl_studio_data.py`
- Create: `system/runtime/nrl_system_check.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_control_plane_v02.py`

**Interfaces:**
- Extends `studio-data` with five v0.2 sections.
- Produces: `run_system_check() -> dict`
- Produces CLI: `system-check`

- [ ] Write failing compatibility and aggregation tests.
- [ ] Implement the five additive sections and deterministic check summary.
- [ ] Ensure check execution cannot mutate phase state.
- [ ] Run focused and existing runtime tests.
- [ ] Commit the aggregation slice.

### Task 5: Live Studio Server

**Files:**
- Create: `system/runtime/nrl_studio_server.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_control_plane_v02.py`

**Interfaces:**
- Produces: `create_studio_server(host, port) -> ThreadingHTTPServer`
- Produces CLI: `studio-serve --host 127.0.0.1 --port 4173`

- [ ] Write failing route tests for three GET endpoints and two allowlisted POST actions.
- [ ] Write failing rejection tests for unknown actions, `advance`, arbitrary command bodies, and unsupported methods.
- [ ] Implement static serving, JSON responses, and direct function dispatch.
- [ ] Run focused and existing runtime tests.
- [ ] Commit the server slice.

### Task 6: Chinese Astryx Studio

**Files:**
- Modify: `apps/studio/src/App.tsx`
- Modify: `apps/studio/src/types.ts`
- Modify: `apps/studio/src/styles.css`
- Modify: `system/runtime/nrl_studio.py`

**Interfaces:**
- Consumes the extended `StudioData` contract and live API.
- Preserves offline data injection for `studio-build`.

- [ ] Query Astryx SideNav, AppShell, Table, Banner, Tabs, ProgressBar, and detail-panel APIs before editing.
- [ ] Replace the single long page with five Chinese SideNav views and persistent Owner Gate banner.
- [ ] Use tables/lists for research and creation assets, with local filtering and a detail panel.
- [ ] Add safe system-check and validate-state controls only when live API is available.
- [ ] Build the frontend and run `astryx doctor`.
- [ ] Commit the Studio slice.

### Task 7: Documentation And Verification

**Files:**
- Modify: `system/runtime/README.md`
- Modify: `tests/test_sys3_runtime.py` only when existing assertions need additive v0.2 compatibility coverage.

- [ ] Document the normal `studio-serve` entry point and all v0.2 commands.
- [ ] Run all Python tests, state validation, system check, frontend build, Astryx doctor, Studio build, and `git diff --check`.
- [ ] Inspect desktop and mobile screenshots and fix visual defects.
- [ ] Request an independent code review and resolve all critical or important findings.
- [ ] Commit final documentation/fixes and push `codex/nrl-control-plane-v0.2`.
