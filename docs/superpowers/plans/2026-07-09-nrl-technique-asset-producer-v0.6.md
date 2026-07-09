# NRL Technique Asset Producer v0.6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic Technique Asset Producer that converts the validated v0.5 Antigravity techniques review plus DNA/RAG evidence into seed-level technique candidate assets.

**Architecture:** Add one focused runtime module `nrl_asset_producers.py` that reads the v0.5 job queue, validated outbox, RAG index, and project asset store. Wire it into `nrl.py`, Studio data, and the read-only Studio server. Produced assets are schema-bound `seed` assets in `system/creation_assets/project_assets.v0.2.json`, not final technique trees or prose.

**Tech Stack:** Python 3 standard library, existing JSON schemas, `unittest`, existing runtime CLI.

## Global Constraints

- No prose generation.
- No combat scenes.
- No final technique tree.
- No final naming dictionary.
- No character or NPC generation.
- No Hermes execution.
- No automatic Antigravity execution.
- No raw `novel_training_set/` reads.
- No Owner Gate bypass.
- Owner Gate remains active.
- Hermes remains `paused_not_removed`.
- Antigravity remains `manual_handoff`.
- `advance` remains blocked at Owner Gate.

---

## File Structure

- Create `system/runtime/nrl_asset_producers.py`: producer status, technique candidate construction, project asset upsert.
- Modify `system/runtime/nrl.py`: add `producer-status` and `produce-techniques --job-id <job_id>`.
- Modify `system/runtime/nrl_studio_data.py`: add `asset_producers`.
- Modify `system/runtime/nrl_studio_server.py`: add `GET /api/producer-status`.
- Modify `system/runtime/README.md`: document producer commands.
- Create `tests/test_asset_producers_v06.py`: focused producer tests.

### Task 1: Producer Status

**Files:**
- Create: `system/runtime/nrl_asset_producers.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_asset_producers_v06.py`

**Interfaces:**
- Consumes:
  - `load_job_queue() -> dict[str, Any]`
  - `load_or_build_rag_index(state: dict[str, Any]) -> dict[str, Any]`
  - `validate_creation_asset_store(store: dict[str, Any] | None = None) -> dict[str, Any]`
- Produces:
  - `build_producer_status(state: dict[str, Any], adapters: dict[str, Any]) -> dict[str, Any]`
  - CLI `producer-status`

- [ ] **Step 1: Write failing tests**

```python
class ProducerStatusCliTests(RuntimeCliCase):
    def test_producer_status_reports_validated_techniques_job(self):
        result = self.run_cli("producer-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.6")
        self.assertIn("techniques", data["supported_families"])
        self.assertTrue(data["techniques"]["job_validated"])
        self.assertEqual(data["system_mode"], "SYSTEM_HARDENING")
        self.assertEqual(data["content_progression"], "FROZEN_AT_OWNER_GATE")
        self.assertFalse(data["hermes_allowed"])
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_asset_producers_v06.ProducerStatusCliTests -v
```

Expected: FAIL because `producer-status` is missing.

- [ ] **Step 3: Implement status**

`build_producer_status()` should report version `0.6`, supported family
`techniques`, job id `job-v05-techniques-antigravity-review`, whether the job
state is `validated`, current techniques candidate count in the project asset
store, whether the store validates, blocked actions, and next safe action.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_asset_producers_v06.ProducerStatusCliTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_asset_producers.py system/runtime/nrl.py tests/test_asset_producers_v06.py
git commit -m "feat: add asset producer status"
```

### Task 2: Technique Candidate Production

**Files:**
- Modify: `system/runtime/nrl_asset_producers.py`
- Modify: `system/runtime/nrl.py`
- Modify: `system/creation_assets/project_assets.v0.2.json`
- Test: `tests/test_asset_producers_v06.py`

**Interfaces:**
- Produces:
  - `produce_technique_candidates(state: dict[str, Any], job_id: str) -> dict[str, Any]`
  - CLI `produce-techniques --job-id <job_id>`

- [ ] **Step 1: Write failing tests**

```python
class TechniqueProducerCliTests(RuntimeCliCase):
    def test_produce_techniques_writes_three_seed_assets_and_validates_store(self):
        result = self.run_cli(
            "produce-techniques",
            "--job-id",
            "job-v05-techniques-antigravity-review",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["produced_count"], 3)
        self.assertTrue(data["store_validation"]["valid"])
        store = json.loads((REPO_ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(encoding="utf-8"))
        techniques = [asset for asset in store["assets"] if asset["family"] == "techniques"]
        self.assertEqual(len(techniques), 3)
        self.assertTrue(all(asset["lifecycle_state"] == "seed" for asset in techniques))
        self.assertNotIn("novel_training_set/", json.dumps(store, ensure_ascii=False))

    def test_produce_techniques_is_idempotent(self):
        first = json.loads(self.run_cli("produce-techniques", "--job-id", "job-v05-techniques-antigravity-review").stdout)
        second = json.loads(self.run_cli("produce-techniques", "--job-id", "job-v05-techniques-antigravity-review").stdout)
        self.assertEqual(first["asset_ids"], second["asset_ids"])
        store = json.loads((REPO_ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(encoding="utf-8"))
        self.assertEqual(len([asset for asset in store["assets"] if asset["family"] == "techniques"]), 3)
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_asset_producers_v06.TechniqueProducerCliTests -v
```

Expected: FAIL because `produce-techniques` is missing.

- [ ] **Step 3: Implement production**

Create exactly these seed assets:

- `technique_costed_advancement`
- `technique_backlash_guard`
- `technique_state_reversal`

Each asset must include:

- `family: techniques`
- `lifecycle_state: seed`
- source refs including validated Antigravity outbox path and at least one DNA id
- `relationships: []`
- constraints that say non-final candidate, no prose, no final technique tree
- technique payload with `cost` and `counter_ids: []`

Upsert by `asset_id`: replace only these owned candidate ids, preserve other
project assets. Validate with `validate_creation_asset_store()` before writing
success.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_asset_producers_v06.TechniqueProducerCliTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_asset_producers.py system/runtime/nrl.py system/creation_assets/project_assets.v0.2.json tests/test_asset_producers_v06.py
git commit -m "feat: produce seed technique candidates"
```

### Task 3: Studio Data And API Integration

**Files:**
- Modify: `system/runtime/nrl_studio_data.py`
- Modify: `system/runtime/nrl_studio_server.py`
- Modify: `system/runtime/README.md`
- Test: `tests/test_asset_producers_v06.py`

**Interfaces:**
- Produces:
  - Studio data key `asset_producers`
  - GET route `/api/producer-status`

- [ ] **Step 1: Write failing tests**

```python
class ProducerIntegrationTests(RuntimeCliCase):
    def test_studio_data_contains_asset_producers(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("asset_producers", data)
        self.assertTrue(data["asset_producers"]["techniques"]["job_validated"])

class ProducerServerTests(unittest.TestCase):
    def test_producer_status_route_returns_status(self):
        from nrl_studio_server import create_studio_server
        server = create_studio_server("127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/api/producer-status"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["version"], "0.6")
            self.assertIn("techniques", data["supported_families"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_asset_producers_v06.ProducerIntegrationTests tests.test_asset_producers_v06.ProducerServerTests -v
```

Expected: FAIL because Studio/API integration is missing.

- [ ] **Step 3: Implement integration**

Add `asset_producers = build_producer_status(state, adapters)` to Studio data.
Add read-only GET route `/api/producer-status`. Document v0.6 commands in
`system/runtime/README.md`.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_asset_producers_v06.ProducerIntegrationTests tests.test_asset_producers_v06.ProducerServerTests -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add system/runtime/nrl_studio_data.py system/runtime/nrl_studio_server.py system/runtime/README.md tests/test_asset_producers_v06.py
git commit -m "feat: expose asset producer status"
```

### Task 4: Full Regression

**Files:**
- Modify only files needed for failures found during verification.

- [ ] **Step 1: Run v0.6 focused tests**

```bash
python3 -m unittest tests.test_asset_producers_v06 -v
```

Expected: OK.

- [ ] **Step 2: Run all existing runtime tests**

```bash
python3 -m unittest tests.test_dna_production_runtime_v05 tests.test_architecture_reconciliation_v04 tests.test_corpus_pipeline_v03 tests.test_control_plane_v02 tests.test_sys3_runtime -v
```

Expected: OK.

- [ ] **Step 3: Run runtime commands**

```bash
python3 system/runtime/nrl.py producer-status
python3 system/runtime/nrl.py validate-creation-assets
python3 system/runtime/nrl.py production-runtime-status
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py advance
```

Expected: all commands succeed; `advance` still reports Owner Gate required.

- [ ] **Step 4: Run build checks**

```bash
python3 system/runtime/nrl.py studio-build
cd apps/studio && npm run build
cd apps/studio && npx astryx doctor
git diff --check
```

Expected: all pass.

