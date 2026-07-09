# NRL DNA Production Runtime v0.5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first operational DNA production runtime for Novel Research Lab: DNA Registry, Research RAG Index, Agent Job Queue, manual Antigravity packet/ingest/validation loop, and runtime status.

**Architecture:** Keep v0.5 file-backed and deterministic. Add focused runtime modules under `system/runtime/`, generated artifacts under `system/dna_registry/`, `system/research_index/`, and `system/agent_ops/`, and CLI commands in `system/runtime/nrl.py`. Existing Control Plane, Studio, Owner Gate, creation schemas, and v0.3 pipeline remain backward compatible.

**Tech Stack:** Python 3 standard library, `unittest`, JSON runtime artifacts, existing NRL runtime modules.

## Global Constraints

- No Phase 2F transition.
- No prose generation.
- No chapter drafting.
- No final character sheets, technique trees, naming dictionaries, or NPC dossiers.
- No raw `novel_training_set/` reads.
- No fake Antigravity or Hermes execution.
- No new display-only dashboard work.
- No database migration. v0.5 remains file-backed.
- `advance` remains blocked at Owner Gate.
- Hermes remains `paused_not_removed`.
- Antigravity remains `manual_handoff`.

---

## File Structure

- Create `system/runtime/nrl_dna_registry.py`: build/load DNA Registry from structured research catalog and current project state.
- Create `system/runtime/nrl_rag_index.py`: build/load structured RAG-style retrieval index from DNA Registry.
- Create `system/runtime/nrl_agent_ops.py`: own file-backed jobs, Antigravity packets, inbox ingest, validation, and runtime status.
- Modify `system/runtime/nrl.py`: add CLI commands and wire runtime modules.
- Modify `system/runtime/nrl_studio_data.py`: expose `dna_production_runtime` summary backed by real v0.5 artifacts.
- Modify `system/runtime/nrl_studio_server.py`: expose safe read routes and allowlisted action routes for v0.5.
- Modify `system/runtime/README.md`: document v0.5 commands.
- Create `tests/test_dna_production_runtime_v05.py`: CLI and module tests.
- Create fixture sample output under `tests/fixtures/agent_ops/valid_antigravity_techniques_review.md`.

### Task 1: DNA Registry

**Files:**
- Create: `system/runtime/nrl_dna_registry.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_dna_production_runtime_v05.py`

**Interfaces:**
- Consumes: `build_research_asset_catalog()`, `load_state()`
- Produces:
  - `build_dna_registry(state: dict[str, Any]) -> dict[str, Any]`
  - `write_dna_registry(state: dict[str, Any]) -> dict[str, Any]`
  - `load_or_build_dna_registry(state: dict[str, Any]) -> dict[str, Any]`
  - CLI `dna-registry-build`
  - CLI `dna-registry`

- [ ] **Step 1: Write failing tests**

```python
def test_dna_registry_builds_all_families_without_raw_corpus(self):
    result = self.run_cli("dna-registry-build")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertEqual(data["version"], "0.5")
    self.assertEqual(
        set(data["summary"]["by_family"]),
        {"book_dna", "narrative_dna", "mechanism_dna", "state_dna", "project_dna"},
    )
    self.assertTrue((REPO_ROOT / "system/dna_registry/dna_registry.v0.5.json").exists())
    self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

def test_dna_registry_cli_loads_generated_registry(self):
    self.run_cli("dna-registry-build")
    result = self.run_cli("dna-registry")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertGreater(data["summary"]["total_entries"], 0)
    self.assertIn("project_dna", data["summary"]["by_family"])
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.DnaRegistryCliTests -v
```

Expected: FAIL because CLI commands are missing.

- [ ] **Step 3: Implement minimal DNA Registry**

Create `nrl_dna_registry.py` with deterministic mapping:

```python
FAMILY_BY_ASSET_TYPE = {
    "book_dna": "book_dna",
    "narrative_dna": "narrative_dna",
    "mechanism": "mechanism_dna",
    "mechanism_notes": "mechanism_dna",
    "state_ledger": "state_dna",
}
```

Map each research item into a DNA entry with stable `dna_id`, source path,
review state, provenance, promotion state, evidence tags, and
`blocked_for_generation=True`. Add one `project_dna` entry for the selected
project from current runtime state.

Add CLI commands to `nrl.py`.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.DnaRegistryCliTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_dna_registry.py system/runtime/nrl.py tests/test_dna_production_runtime_v05.py system/dna_registry/dna_registry.v0.5.json
git commit -m "feat: add dna registry runtime"
```

### Task 2: Research RAG Index

**Files:**
- Create: `system/runtime/nrl_rag_index.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_dna_production_runtime_v05.py`

**Interfaces:**
- Consumes: `load_or_build_dna_registry(state)`
- Produces:
  - `build_rag_index(state: dict[str, Any]) -> dict[str, Any]`
  - `write_rag_index(state: dict[str, Any]) -> dict[str, Any]`
  - CLI `rag-index-build`
  - CLI `rag-index`

- [ ] **Step 1: Write failing tests**

```python
def test_rag_index_builds_structured_items_without_raw_prose(self):
    self.run_cli("dna-registry-build")
    result = self.run_cli("rag-index-build")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertEqual(data["version"], "0.5")
    self.assertGreater(data["summary"]["total_items"], 0)
    item = data["items"][0]
    self.assertIn("retrieval_text", item)
    self.assertIn("evidence_weight", item)
    self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.RagIndexCliTests -v
```

Expected: FAIL because CLI commands are missing.

- [ ] **Step 3: Implement RAG Index**

Build one item per non-project DNA entry. Use concise metadata only:

```text
<family> | <title> | <review_state> | <promotion_state> | <comma-separated evidence_tags>
```

Use `evidence_weight=3` for promoted, `2` for candidate, `1` for stub, `0` for
blocked.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.RagIndexCliTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_rag_index.py system/runtime/nrl.py tests/test_dna_production_runtime_v05.py system/research_index/research_rag_index.v0.5.json
git commit -m "feat: add research rag index runtime"
```

### Task 3: Agent Job Queue And Packets

**Files:**
- Create: `system/runtime/nrl_agent_ops.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_dna_production_runtime_v05.py`

**Interfaces:**
- Consumes: `build_pipeline_plan()`, `load_or_build_dna_registry()`, `write_rag_index()`
- Produces:
  - `load_job_queue() -> dict[str, Any]`
  - `plan_agent_job(state: dict[str, Any], adapters: dict[str, Any], family: str) -> dict[str, Any]`
  - `write_agent_packet(job_id: str) -> dict[str, Any]`
  - CLI `agent-jobs`
  - CLI `agent-job-plan --family <asset_family>`
  - CLI `agent-pack --job-id <job_id>`

- [ ] **Step 1: Write failing tests**

```python
def test_agent_job_plan_creates_techniques_job_and_packet(self):
    result = self.run_cli("agent-job-plan", "--family", "techniques")
    self.assertEqual(result.returncode, 0, result.stderr)
    job = json.loads(result.stdout)["job"]
    self.assertEqual(job["target_family"], "techniques")
    self.assertEqual(job["owner_agent"], "antigravity")
    self.assertEqual(job["state"], "ready_for_antigravity")
    self.assertTrue((REPO_ROOT / "system/agent_ops/job_queue.v0.5.json").exists())

    packet = self.run_cli("agent-pack", "--job-id", job["job_id"])
    self.assertEqual(packet.returncode, 0, packet.stderr)
    packet_data = json.loads(packet.stdout)
    packet_text = (REPO_ROOT / packet_data["packet_path"]).read_text(encoding="utf-8")
    self.assertIn("FORBIDDEN ACTIONS", packet_text)
    self.assertIn("Do not write prose", packet_text)
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.AgentOpsCliTests.test_agent_job_plan_creates_techniques_job_and_packet -v
```

Expected: FAIL because commands are missing.

- [ ] **Step 3: Implement job queue and packet writer**

Use stable job ids:

```text
job-v05-<family>-antigravity-review
```

Write queue to `system/agent_ops/job_queue.v0.5.json`. Packet path is:

```text
system/agent_ops/packets/<job_id>.md
```

Packet must include job id, target family, source DNA ids, expected output path,
required sections, and forbidden actions.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.AgentOpsCliTests.test_agent_job_plan_creates_techniques_job_and_packet -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_agent_ops.py system/runtime/nrl.py tests/test_dna_production_runtime_v05.py system/agent_ops
git commit -m "feat: add agent production job queue"
```

### Task 4: Antigravity Ingest And Validation

**Files:**
- Modify: `system/runtime/nrl_agent_ops.py`
- Modify: `system/runtime/nrl.py`
- Create: `tests/fixtures/agent_ops/valid_antigravity_techniques_review.md`
- Test: `tests/test_dna_production_runtime_v05.py`

**Interfaces:**
- Produces:
  - `ingest_agent_output(job_id: str, file_arg: str) -> dict[str, Any]`
  - `validate_agent_job(job_id: str) -> dict[str, Any]`
  - CLI `agent-ingest --job-id <job_id> --file <path>`
  - CLI `agent-validate --job-id <job_id>`

- [ ] **Step 1: Write failing tests**

```python
def test_agent_ingest_rejects_files_outside_inbox(self):
    job = json.loads(self.run_cli("agent-job-plan", "--family", "techniques").stdout)["job"]
    result = self.run_cli("agent-ingest", "--job-id", job["job_id"], "--file", "README.md")
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("system/agent_ops/inbox", result.stderr)

def test_agent_validate_accepts_sample_review_and_marks_job_validated(self):
    job = json.loads(self.run_cli("agent-job-plan", "--family", "techniques").stdout)["job"]
    inbox = REPO_ROOT / "system/agent_ops/inbox/valid_antigravity_techniques_review.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text((REPO_ROOT / "tests/fixtures/agent_ops/valid_antigravity_techniques_review.md").read_text(encoding="utf-8"), encoding="utf-8")
    ingest = self.run_cli("agent-ingest", "--job-id", job["job_id"], "--file", str(inbox.relative_to(REPO_ROOT)))
    self.assertEqual(ingest.returncode, 0, ingest.stderr)
    validate = self.run_cli("agent-validate", "--job-id", job["job_id"])
    self.assertEqual(validate.returncode, 0, validate.stderr)
    data = json.loads(validate.stdout)
    self.assertTrue(data["valid"])
    self.assertEqual(data["job"]["state"], "validated")
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.AgentOpsCliTests -v
```

Expected: FAIL because ingest/validate are missing.

- [ ] **Step 3: Implement ingest and validation**

Accept only files under `system/agent_ops/inbox/`. Required sections:

```text
## Job ID
## Structural Review
## Evidence Use
## Originality Risk
## Required Fixes
## Promotion Recommendation
```

Reject text containing:

```text
Chapter 1
正文
第一章
```

On success, copy the file to `system/agent_ops/outbox/<job_id>_validated.md`,
write a validation report, and update the job state to `validated`.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.AgentOpsCliTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_agent_ops.py system/runtime/nrl.py tests/test_dna_production_runtime_v05.py tests/fixtures/agent_ops/valid_antigravity_techniques_review.md system/agent_ops
git commit -m "feat: validate manual antigravity outputs"
```

### Task 5: Runtime Status And Integration

**Files:**
- Modify: `system/runtime/nrl_agent_ops.py`
- Modify: `system/runtime/nrl.py`
- Modify: `system/runtime/nrl_studio_data.py`
- Modify: `system/runtime/nrl_studio_server.py`
- Modify: `system/runtime/README.md`
- Test: `tests/test_dna_production_runtime_v05.py`

**Interfaces:**
- Produces:
  - `build_production_runtime_status(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]`
  - CLI `production-runtime-status`
  - Studio data key `dna_production_runtime`
  - API routes `/api/dna-registry`, `/api/rag-index`, `/api/agent-jobs`, `/api/production-runtime-status`

- [ ] **Step 1: Write failing tests**

```python
def test_production_runtime_status_reports_real_runtime_sections(self):
    self.run_cli("dna-registry-build")
    self.run_cli("rag-index-build")
    self.run_cli("agent-job-plan", "--family", "techniques")
    result = self.run_cli("production-runtime-status")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertEqual(data["version"], "0.5")
    self.assertEqual(data["system_mode"], "SYSTEM_HARDENING")
    self.assertEqual(data["content_progression"], "FROZEN_AT_OWNER_GATE")
    self.assertEqual(data["antigravity"]["mode"], "manual_handoff")
    self.assertEqual(data["hermes"]["status"], "paused_not_removed")
    self.assertIn("techniques", data["agent_jobs"]["by_family"])

def test_studio_data_contains_dna_production_runtime(self):
    result = self.run_cli("studio-data")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertIn("dna_production_runtime", data)
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.ProductionRuntimeIntegrationTests -v
```

Expected: FAIL because status and Studio integration are missing.

- [ ] **Step 3: Implement status and integration**

Status should report:

- DNA registry summary
- RAG index summary
- Agent job queue summary
- current packet path
- inbox/outbox counts
- Antigravity mode
- Hermes status
- Owner Gate status

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_dna_production_runtime_v05.ProductionRuntimeIntegrationTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_agent_ops.py system/runtime/nrl.py system/runtime/nrl_studio_data.py system/runtime/nrl_studio_server.py system/runtime/README.md tests/test_dna_production_runtime_v05.py
git commit -m "feat: expose dna production runtime status"
```

### Task 6: Full Regression

**Files:**
- Modify only files needed for failures found during verification.

**Interfaces:**
- Consumes all v0.5 commands.
- Produces verified working branch.

- [ ] **Step 1: Run focused v0.5 tests**

```bash
python3 -m unittest tests.test_dna_production_runtime_v05 -v
```

Expected: OK.

- [ ] **Step 2: Run existing runtime tests**

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04 tests.test_corpus_pipeline_v03 tests.test_control_plane_v02 tests.test_sys3_runtime -v
```

Expected: OK.

- [ ] **Step 3: Run runtime commands**

```bash
python3 system/runtime/nrl.py validate-state
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py production-runtime-status
python3 system/runtime/nrl.py system-check
```

Expected: all return code 0; `system-status` remains `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.

- [ ] **Step 4: Run frontend/static build guard**

```bash
python3 system/runtime/nrl.py studio-build
cd apps/studio && npm run build
cd apps/studio && npx astryx doctor
```

Expected: all commands pass. Studio may show v0.5 runtime summaries only if backed by data.

- [ ] **Step 5: Check diff hygiene**

```bash
git diff --check
```

Expected: no whitespace errors.

- [ ] **Step 6: Final commit if needed**

```bash
git status --short
git add <only intentional files>
git commit -m "test: verify dna production runtime v0.5"
```

