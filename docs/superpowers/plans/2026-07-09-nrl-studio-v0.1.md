# NRL Studio v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `Novel Research Lab Studio v0.1` as a read-only local product dashboard backed by runtime state.

**Architecture:** Add a Python `studio-data` contract that assembles one JSON object from Mission Controller state, Mission Registry, adapter config, and derived system status. Create a dedicated `apps/studio/` Vite React app using Astryx, then make `studio-build` generate data, build the app, and copy static output into `system/runtime/studio/`.

**Tech Stack:** Python 3 runtime CLI, `unittest`, Vite, React, TypeScript, Astryx packages, npm.

## Global Constraints

- No Phase 2F.
- No novel prose.
- No chapter plan content deliverable.
- No full character cards.
- No Hermes execution.
- No Antigravity execution.
- No raw `novel_training_set/` reads.
- `current_phase_state.json` and `mission_registry.json` remain source of truth.
- Astryx is installed only inside `apps/studio/`, never in the repo root.
- Studio v0.1 is read-only.

---

## File Structure

- Create `system/runtime/nrl_studio_data.py`: focused data assembler for the eight Studio sections.
- Modify `system/runtime/nrl.py`: add `studio-data` CLI command and route `studio-build` through the upgraded build function.
- Modify `system/runtime/nrl_studio.py`: generate data JSON, run the frontend build when available, copy `apps/studio/dist` to `system/runtime/studio`, and keep a narrow fallback for missing frontend during early development.
- Modify `tests/test_sys3_runtime.py`: add contract tests and update Studio build smoke assertions.
- Create `apps/studio/package.json`: isolated frontend package.
- Create `apps/studio/index.html`, `apps/studio/src/main.tsx`, `apps/studio/src/App.tsx`, `apps/studio/src/styles.css`, `apps/studio/src/types.ts`: dashboard app.
- Create or accept Astryx-generated files inside `apps/studio/` after `npx astryx init --features agents --agent codex`.
- Modify `system/runtime/README.md`: document `studio-data`, `studio-build`, app build, and static open path.

---

### Task 1: Runtime Studio Data Contract

**Files:**
- Modify: `tests/test_sys3_runtime.py`
- Create: `system/runtime/nrl_studio_data.py`
- Modify: `system/runtime/nrl.py`

**Interfaces:**
- Produces: `build_studio_data(state: dict[str, Any], registry: list[dict[str, Any]], adapters: dict[str, Any]) -> dict[str, Any]`
- Produces CLI: `python3 system/runtime/nrl.py studio-data`
- Consumes: `build_system_status(state, adapters)`

- [ ] **Step 1: Write failing tests**

Add tests that call `studio-data` and assert the eight top-level keys:

```python
def test_studio_data_returns_required_dashboard_sections(self):
    result = self.run_cli("studio-data")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertEqual(
        set(data),
        {
            "system_identity",
            "current_project",
            "agent_panel",
            "artifact_map",
            "creation_coverage_matrix",
            "runtime_status",
            "next_safe_action",
            "owner_gate",
        },
    )
    self.assertEqual(data["system_identity"]["name"], "Novel Research Lab")
    self.assertIn("Corpus-to-Creation", data["system_identity"]["positioning"])

def test_studio_data_marks_long_form_assets_honestly(self):
    result = self.run_cli("studio-data")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    matrix = {row["asset"]: row["status"] for row in data["creation_coverage_matrix"]["items"]}
    self.assertEqual(matrix["Characters"], "partial")
    self.assertEqual(matrix["NPCs"], "missing")
    self.assertEqual(matrix["Factions"], "partial")
    self.assertEqual(matrix["Artifacts"], "seed")
    self.assertEqual(matrix["Techniques"], "missing")
    self.assertEqual(matrix["Naming"], "missing")
    self.assertEqual(matrix["Emotional Bonds"], "partial")
    self.assertEqual(matrix["Foreshadowing"], "partial")
    self.assertEqual(matrix["State Ledger"], "seed")
    self.assertNotIn("complete", set(matrix.values()))
```

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_data_returns_required_dashboard_sections tests.test_sys3_runtime.RuntimeFixture.test_studio_data_marks_long_form_assets_honestly -v
```

Expected: fail because `studio-data` is not a known command.

- [ ] **Step 3: Implement the data assembler and CLI**

Create `nrl_studio_data.py` with constants for the eight sections and deterministic coverage matrix. Add `cmd_studio_data` to `nrl.py`, loading state, adapters, and registry, then printing `build_studio_data(...)`.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_data_returns_required_dashboard_sections tests.test_sys3_runtime.RuntimeFixture.test_studio_data_marks_long_form_assets_honestly -v
```

Expected: both tests pass.

- [ ] **Step 5: Commit**

```bash
git add tests/test_sys3_runtime.py system/runtime/nrl.py system/runtime/nrl_studio_data.py
git commit -m "feat: add studio data contract"
```

---

### Task 2: Isolated Astryx Studio App

**Files:**
- Create: `apps/studio/package.json`
- Create: `apps/studio/index.html`
- Create: `apps/studio/src/main.tsx`
- Create: `apps/studio/src/App.tsx`
- Create: `apps/studio/src/types.ts`
- Create: `apps/studio/src/styles.css`
- Create or modify: Astryx-generated files inside `apps/studio/`

**Interfaces:**
- Consumes static JSON: `/nrl-studio-data.json`
- Produces build output: `apps/studio/dist/index.html` and assets.

- [ ] **Step 1: Create frontend package skeleton**

Create a Vite React TypeScript package under `apps/studio/` only. Do not add `package.json` to the repository root.

- [ ] **Step 2: Install and initialize Astryx**

Run from `apps/studio/`:

```bash
npm install
npm install @astryxdesign/core @astryxdesign/theme-neutral @astryxdesign/cli
npx astryx init --features agents --agent codex
```

Then read generated local agent docs before coding.

- [ ] **Step 3: Query Astryx before building the page**

Run:

```bash
npx astryx template --list
npx astryx search dashboard --type template --detail
npx astryx component --list
npx astryx docs tokens
```

Use the installed CLI output to choose component imports and token usage.

- [ ] **Step 4: Implement dashboard rendering**

Build one dense dashboard page with the eight sections: System Identity, Current Project, Agent Panel, Artifact Map, Creation Coverage Matrix, Runtime Status, Next Safe Action, and Owner Gate.

- [ ] **Step 5: Verify frontend build and Astryx doctor**

Run from `apps/studio/`:

```bash
npm run build
npx astryx doctor
```

Expected: build exits 0, doctor exits 0 or reports only non-blocking warnings that are documented in the final verification.

- [ ] **Step 6: Commit**

```bash
git add apps/studio
git commit -m "feat: add astryx studio dashboard app"
```

---

### Task 3: Studio Build Integration And Docs

**Files:**
- Modify: `system/runtime/nrl_studio.py`
- Modify: `tests/test_sys3_runtime.py`
- Modify: `system/runtime/README.md`
- Generated: `system/runtime/studio/`

**Interfaces:**
- Consumes: `build_studio_data(...)`
- Produces: `system/runtime/studio/index.html`
- Produces: `apps/studio/public/nrl-studio-data.json` during build.

- [ ] **Step 1: Write failing build assertions**

Update `test_studio_build_creates_read_only_cockpit`, `test_studio_build_includes_doctor_command`, and `test_studio_build_shows_system_hardening_mode` to assert the new Studio strings:

```python
self.assertIn("Novel Research Lab", html)
self.assertIn("Corpus-to-Creation", html)
self.assertIn("Creation Coverage Matrix", html)
self.assertIn("Owner Gate", html)
self.assertIn("Hermes: paused_not_removed", html)
```

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_build_creates_read_only_cockpit tests.test_sys3_runtime.RuntimeFixture.test_studio_build_includes_doctor_command tests.test_sys3_runtime.RuntimeFixture.test_studio_build_shows_system_hardening_mode -v
```

Expected: fail until `studio-build` emits the upgraded product shell.

- [ ] **Step 3: Implement build integration**

Update `render_studio()` to:

1. Load state, adapters, and registry.
2. Write `apps/studio/public/nrl-studio-data.json`.
3. Run `npm run build` in `apps/studio/` when `apps/studio/package.json` exists.
4. Remove the previous `system/runtime/studio/` build output.
5. Copy `apps/studio/dist/*` into `system/runtime/studio/`.
6. Return the built `index.html` path.

Keep the simple fallback only if `apps/studio/package.json` does not exist.

- [ ] **Step 4: Update README**

Document:

```bash
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py studio-data
python3 system/runtime/nrl.py studio-build
open system/runtime/studio/index.html
```

State that Studio is read-only, uses `current_phase_state.json` and `mission_registry.json`, and does not call Hermes or Antigravity.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_build_creates_read_only_cockpit tests.test_sys3_runtime.RuntimeFixture.test_studio_build_includes_doctor_command tests.test_sys3_runtime.RuntimeFixture.test_studio_build_shows_system_hardening_mode tests.test_sys3_runtime.RuntimeFixture.test_readme_documents_sys3_commands -v
```

Expected: all selected tests pass.

- [ ] **Step 6: Commit**

```bash
git add system/runtime/nrl_studio.py tests/test_sys3_runtime.py system/runtime/README.md system/runtime/studio apps/studio/public/nrl-studio-data.json
git commit -m "feat: build studio from runtime data"
```

---

### Task 4: Full Guardrail Verification

**Files:**
- No new production files expected.

**Interfaces:**
- Verifies runtime and frontend contract.

- [ ] **Step 1: Run state validation**

```bash
python3 system/runtime/nrl.py validate-state
```

Expected: exit 0 and `state_valid_against_schema: true`.

- [ ] **Step 2: Run full runtime tests**

```bash
python3 -m unittest tests.test_sys3_runtime -v
```

Expected: all tests pass.

- [ ] **Step 3: Run frontend build and Astryx doctor**

```bash
cd apps/studio && npm run build
cd apps/studio && npx astryx doctor
```

Expected: build exits 0; doctor exits 0 or documented non-blocking warnings only.

- [ ] **Step 4: Run integrated Studio build**

```bash
python3 system/runtime/nrl.py studio-build
```

Expected: prints `system/runtime/studio/index.html`.

- [ ] **Step 5: Inspect built Studio strings**

```bash
rg "Novel Research Lab|Corpus-to-Creation|SYSTEM_HARDENING|Hermes: paused_not_removed|Creation Coverage Matrix|Owner Gate" system/runtime/studio/index.html
```

Expected: all required strings are present.

- [ ] **Step 6: Check whitespace and final diff**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intentional files are modified.

- [ ] **Step 7: Final implementation commit if needed**

If any verification fixes were made after prior commits:

```bash
git add <changed files>
git commit -m "fix: verify studio product shell"
```
