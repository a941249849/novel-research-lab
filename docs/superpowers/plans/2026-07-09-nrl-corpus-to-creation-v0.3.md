# NRL Corpus-to-Creation v0.3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first deterministic Corpus-to-Creation pipeline layer that turns reviewed research assets into read-only creation asset plans.

**Architecture:** Add a focused Python pipeline module that consumes the existing research catalog, creation schema registry, creation coverage matrix, and runtime state. Expose the pipeline through CLI, Studio data, live Studio API, and a sixth Chinese Astryx view while preserving all Owner Gate and no-content-production boundaries.

**Tech Stack:** Python 3 standard library, jsonschema Draft-07, unittest, React 19, TypeScript, Vite, Astryx 0.1.4.

## Global Constraints

- Keep Phase 2E frozen at Owner Gate.
- Do not read `novel_training_set/`.
- Do not generate prose or final creative assets.
- Do not call Hermes or Antigravity.
- Keep current runtime state files as sources of truth.
- Use TDD for every behavior change.

---

### Task 1: Pipeline Contract Runtime

**Files:**
- Create: `system/runtime/nrl_corpus_pipeline.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_corpus_pipeline_v03.py`

**Interfaces:**
- Produces: `build_pipeline_status(state: dict, adapters: dict) -> dict`
- Produces: `build_pipeline_plan(state: dict, adapters: dict, family: str | None = None, next_only: bool = False) -> dict`
- Produces CLI: `pipeline-status`
- Produces CLI: `pipeline-plan --family <asset_family>`
- Produces CLI: `pipeline-plan --next`

- [ ] Write failing tests that `pipeline-status` returns deterministic stages, one next family, and no raw corpus paths.
- [ ] Write failing tests that every creation family can produce a plan with schema, research query, evidence requirements, validation gates, agent review policy, and Owner Gate.
- [ ] Run: `python3 -m unittest tests.test_corpus_pipeline_v03 -v`
- [ ] Implement `nrl_corpus_pipeline.py` using existing research and creation registries.
- [ ] Wire the two CLI commands into `nrl.py`.
- [ ] Run focused tests and existing v0.2 runtime tests.
- [ ] Commit the runtime slice.

### Task 2: Studio Data And Live API

**Files:**
- Modify: `system/runtime/nrl_studio_data.py`
- Modify: `system/runtime/nrl_studio_server.py`
- Test: `tests/test_corpus_pipeline_v03.py`

**Interfaces:**
- Extends `studio-data` with `corpus_pipeline`.
- Produces GET route: `/api/pipeline-status`
- Produces GET route: `/api/pipeline-plan?family=<asset_family>`
- Produces GET route: `/api/pipeline-plan?next=true`

- [ ] Write failing tests that `studio-data` contains `corpus_pipeline`.
- [ ] Write failing server tests for the three pipeline GET paths.
- [ ] Write failing server tests that invalid families return a structured error.
- [ ] Implement Studio data aggregation and GET route parsing.
- [ ] Run focused tests and existing runtime tests.
- [ ] Commit the API slice.

### Task 3: Chinese Astryx Pipeline View

**Files:**
- Modify: `apps/studio/src/types.ts`
- Modify: `apps/studio/src/App.tsx`
- Modify: `system/runtime/nrl_studio.py`
- Test: `tests/test_sys3_runtime.py`

**Interfaces:**
- Consumes `StudioData["corpus_pipeline"]`.
- Adds SideNav view id `pipeline` with label `生成管线`.
- Shows no creative execution buttons.

- [ ] Query Astryx component docs for every new component or changed pattern.
- [ ] Add TypeScript types for pipeline status and plans.
- [ ] Add a sixth SideNav view with stage table, next family summary, evidence requirements, validation gates, and forbidden actions.
- [ ] Extend Studio build labels so static output contains `生成管线` and `Corpus-to-Creation Pipeline`.
- [ ] Run frontend build and `npx astryx doctor`.
- [ ] Inspect desktop and mobile layout.
- [ ] Commit the Studio slice.

### Task 4: Documentation And Full Verification

**Files:**
- Modify: `system/runtime/README.md`
- Modify: `docs/superpowers/specs/2026-07-09-nrl-corpus-to-creation-v0.3-design.md` only if implementation reveals a contract correction.

**Interfaces:**
- Documents:
  - `python3 system/runtime/nrl.py pipeline-status`
  - `python3 system/runtime/nrl.py pipeline-plan --next`
  - `python3 system/runtime/nrl.py pipeline-plan --family characters`

- [ ] Update runtime README with v0.3 commands and boundaries.
- [ ] Run `python3 -m unittest tests.test_corpus_pipeline_v03 tests.test_control_plane_v02 tests.test_sys3_runtime -v`.
- [ ] Run `python3 system/runtime/nrl.py validate-state`.
- [ ] Run `python3 system/runtime/nrl.py system-check`.
- [ ] Run `python3 system/runtime/nrl.py studio-build`.
- [ ] Run `npm run build` in `apps/studio`.
- [ ] Run `npx astryx doctor` in `apps/studio`.
- [ ] Run `git diff --check`.
- [ ] Commit final docs and fixes.
