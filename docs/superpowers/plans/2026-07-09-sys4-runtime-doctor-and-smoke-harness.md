# SYS-4 Runtime Doctor And Smoke Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a single runtime health command and smoke-test path that proves Novel Research Lab can stage, wait for, ingest, and gate an external Antigravity review without advancing novel prose.

**Architecture:** Keep Codex/NRL as the local runtime host. Add one focused doctor module for read-only environment and mission checks, expose it through `nrl.py doctor`, and reuse existing registry/handoff/state mutation code for smoke tests. Studio remains a generated read-only HTML cockpit.

**Tech Stack:** Python 3 standard library, existing `unittest` test suite, existing static HTML Studio.

## Global Constraints

- Do not write novel prose, first chapters, full character cards, or detailed prose outlines.
- Do not read from `novel_training_set/` for SYS-4.
- Do not upgrade Hermes or Antigravity from `manual_handoff` without an Owner Gate record.
- Do not bind this workspace to a GitHub remote unless the target repository is confirmed.
- Use `python3`, not `python`.
- The workspace is not currently a Git repository; commits are skipped unless Git is initialized or bound later.

---

### Task 1: Runtime Doctor Command

**Files:**
- Create: `system/runtime/nrl_doctor.py`
- Modify: `system/runtime/nrl.py`
- Test: `tests/test_sys3_runtime.py`

**Interfaces:**
- Consumes: `current_mission(state, agent=None)`, `load_state()`, `load_adapters()`, `load_registry()`, `ROOT`
- Produces: `run_doctor() -> dict[str, object]`

- [ ] **Step 1: Write failing test**

```python
def test_doctor_reports_runtime_health_without_mutating_state(self):
    before = (self.root / "system/mission_controller/current_phase_state.json").read_text(encoding="utf-8")
    result = self.run_cli("doctor")
    self.assertEqual(result.returncode, 0, result.stderr)
    data = json.loads(result.stdout)
    self.assertEqual(data["runtime"], "Novel Research Lab")
    self.assertEqual(data["mission"]["mission_id"], "phase2d_antigravity_outline_tree_review")
    self.assertEqual(data["git"]["is_repo"], False)
    self.assertEqual(data["adapters"]["antigravity"]["mode"], "manual_handoff")
    self.assertEqual(data["gates"]["review_status"], "PENDING")
    after = (self.root / "system/mission_controller/current_phase_state.json").read_text(encoding="utf-8")
    self.assertEqual(after, before)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_doctor_reports_runtime_health_without_mutating_state -v`
Expected: FAIL because `doctor` is not a known command.

- [ ] **Step 3: Implement minimal doctor module and CLI command**

```python
def run_doctor() -> dict[str, object]:
    return {
        "runtime": "Novel Research Lab",
        "root": str(ROOT),
        "git": inspect_git(ROOT),
        "mission": mission_summary,
        "adapters": adapter_summary,
        "gates": gate_summary,
        "handoff": handoff_summary,
        "blocked_actions": state.get("blocked_actions", []),
        "recommended_next_command": "python3 system/runtime/nrl.py prepare-handoff --agent antigravity",
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_doctor_reports_runtime_health_without_mutating_state -v`
Expected: PASS.

### Task 2: External Review Smoke Test

**Files:**
- Modify: `tests/test_sys3_runtime.py`
- Modify: `system/runtime/nrl.py` only if test exposes a bug in existing ingest flow.

**Interfaces:**
- Consumes: CLI commands `prepare-handoff`, `ingest`, `gate-status`
- Produces: regression coverage for manual Antigravity handoff lifecycle

- [ ] **Step 1: Write failing/behavioral smoke test**

```python
def test_antigravity_manual_review_smoke_path_reaches_owner_gate(self):
    prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
    self.assertEqual(prepared.returncode, 0, prepared.stderr)
    output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("# Antigravity Review\n\nrecommendation: owner_gate\n", encoding="utf-8")
    ingested = self.run_cli("ingest", "--agent", "antigravity", "--file", "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md")
    self.assertEqual(ingested.returncode, 0, ingested.stderr)
    gate = self.run_cli("gate-status")
    self.assertEqual(gate.returncode, 0, gate.stderr)
    data = json.loads(gate.stdout)
    self.assertEqual(data["owner_gate_required"], True)
    self.assertEqual(data["review_status"], "REVIEW_RECEIVED_PENDING_OWNER_GATE")
```

- [ ] **Step 2: Run test**

Run: `python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_antigravity_manual_review_smoke_path_reaches_owner_gate -v`
Expected: PASS if SYS-3 ingest flow is already correct; if it fails, implement only the minimal fix.

### Task 3: Studio And README Visibility

**Files:**
- Modify: `system/runtime/nrl_studio.py`
- Modify: `system/runtime/README.md`
- Test: `tests/test_sys3_runtime.py`

**Interfaces:**
- Consumes: doctor output concepts
- Produces: Studio HTML that surfaces runtime health and next command

- [ ] **Step 1: Write failing test for Studio doctor visibility**

```python
def test_studio_build_includes_doctor_command(self):
    result = self.run_cli("studio-build")
    self.assertEqual(result.returncode, 0, result.stderr)
    html = (self.root / "system/runtime/studio/index.html").read_text(encoding="utf-8")
    self.assertIn("Runtime Health", html)
    self.assertIn("python3 system/runtime/nrl.py doctor", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_build_includes_doctor_command -v`
Expected: FAIL because Studio does not include runtime health yet.

- [ ] **Step 3: Update Studio and README**

Add a Runtime Health section with doctor, check-inputs, validate-state, and handoff commands.

- [ ] **Step 4: Run full tests**

Run: `python3 -m unittest tests.test_sys3_runtime -v`
Expected: all tests PASS.

### Task 4: Live Workspace Verification

**Files:**
- No required code files.

**Interfaces:**
- Consumes: runtime CLI
- Produces: fresh verification evidence for user handoff

- [ ] **Step 1: Run runtime checks**

```bash
python3 -m unittest tests.test_sys3_runtime -v
python3 system/runtime/nrl.py validate-state
python3 system/runtime/nrl.py doctor
python3 system/runtime/nrl.py studio-build
```

- [ ] **Step 2: Report GitHub binding status**

Use Chrome or GitHub connector to identify the intended repo. If the workspace is still not a Git repo and the target repo is ambiguous, stop before binding.
