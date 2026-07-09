# NRL Evidence Pack Matrix v0.11 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full nine-family Corpus-to-Creation evidence-pack matrix so the system has a validated input layer for every creation asset family before any Hermes writing stage.

**Architecture:** Extend the existing `nrl_corpus_pipeline` runtime from single-family evidence packs to an aggregate manifest. Keep Phase 1 structured research assets and `current_phase_state.json` as upstream truth, generate read-only evidence packages under `system/research_assets/evidence_packs/`, validate them with active gates, and expose the aggregate through CLI, Studio data, system check, and static Studio.

**Tech Stack:** Python runtime CLI, `unittest`, Draft-07 `jsonschema`, Vite + React + Astryx Studio.

## Global Constraints

- Do not generate novel prose, chapter plans, final character cards, final naming dictionaries, or final creative assets.
- Do not copy raw `novel_training_set/` content into evidence packs or committed artifacts.
- Hermes remains `paused_not_removed`.
- Antigravity remains external review / CLI bridge only; no automatic content execution.
- Owner Gate remains active; full-corpus proof promotion remains blocked without explicit Owner decision.
- Use TDD: failing test first, then minimal implementation.

---

### Task 1: Full Evidence-Pack Matrix CLI

**Files:**
- Modify: `tests/test_corpus_pipeline_v03.py`
- Modify: `system/runtime/nrl_corpus_pipeline.py`
- Modify: `system/runtime/nrl.py`

**Interfaces:**
- Consumes: `build_evidence_pack(state, adapters, family=...) -> dict`, `validate_evidence_pack(pack) -> dict`
- Produces: `build_evidence_pack_matrix(state, adapters) -> dict`, `write_evidence_pack_matrix(matrix) -> dict`, CLI `evidence-pack-matrix [--write]`, CLI `evidence-pack-validate --all`

- [ ] **Step 1: Write failing tests**

Add tests that assert `evidence-pack-matrix --write` emits nine packs, writes `manifest.v0.11.json`, excludes `novel_training_set/`, keeps `content_generation_allowed=false`, and that `evidence-pack-validate --all` validates all nine packs.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_corpus_pipeline_v03.CorpusPipelineCliTests -v`

Expected: fail because `evidence-pack-matrix` and `--all` are not implemented.

- [ ] **Step 3: Implement matrix builder and validator**

Add `EVIDENCE_PACK_MATRIX_VERSION = "0.11"`, build one pack per `FAMILY_PRIORITY`, write each pack plus a manifest, and validate all packs through existing active gates.

- [ ] **Step 4: Run target tests**

Run: `python3 -m unittest tests.test_corpus_pipeline_v03.CorpusPipelineCliTests -v`

Expected: pass.

### Task 2: System Check and Studio Exposure

**Files:**
- Modify: `system/runtime/nrl_system_check.py`
- Modify: `system/runtime/nrl_studio_data.py`
- Modify: `system/runtime/nrl_studio_server.py`
- Modify: `apps/studio/src/types.ts`
- Modify: `apps/studio/src/App.tsx`
- Modify: `system/runtime/README.md`

**Interfaces:**
- Consumes: `build_evidence_pack_matrix(state, adapters) -> dict`
- Produces: `studio-data.corpus_pipeline.evidence_pack_matrix`, API route `GET /api/evidence-pack-matrix`, system-check check id `evidence_pack_matrix`

- [ ] **Step 1: Write failing tests**

Add assertions that `system-check` includes `evidence_pack_matrix`, `studio-data` includes matrix summary, and `/api/evidence-pack-matrix` returns nine family entries.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_corpus_pipeline_v03 -v`

Expected: fail because matrix is not exposed.

- [ ] **Step 3: Implement exposure**

Wire matrix into Studio data, server route, system-check, and the Pipeline view with compact matrix summary.

- [ ] **Step 4: Run tests and build**

Run:

```bash
python3 -m unittest tests.test_corpus_pipeline_v03 -v
npm run build
npx astryx doctor
```

Expected: all pass.

### Task 3: Verification and Commit

**Files:**
- Modify: generated `apps/studio/public/nrl-studio-data.json`
- Modify: generated `system/runtime/studio/*`
- Create: generated evidence packs under `system/research_assets/evidence_packs/`

- [ ] **Step 1: Run full verification**

Run:

```bash
python3 -m unittest tests.test_corpus_pipeline_v03 tests.test_full_corpus_proof_gate_v08 tests.test_control_plane_v02 tests.test_sys3_runtime -v
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py validate-state
python3 system/runtime/nrl.py evidence-pack-validate --all
python3 system/runtime/nrl.py studio-build
git diff --check
```

- [ ] **Step 2: Commit only durable engineering artifacts**

Stage code, tests, docs, Studio build output, and evidence-pack matrix artifacts. Do not stage `.agent-handoff/`, raw Antigravity responses, or unrelated `system/agent_ops/full_corpus_job.v0.7.json`.

- [ ] **Step 3: Push**

Run:

```bash
git commit -m "feat: add evidence pack matrix"
git push
```
