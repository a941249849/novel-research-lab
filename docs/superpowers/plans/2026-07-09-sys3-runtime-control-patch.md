# SYS-3 Runtime Control Patch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the SYS-3 runtime control patch so Novel Research Lab can track missions, handoff attempts, owner decisions, and compiled constraint packets without advancing novel content.

**Architecture:** Keep `system/runtime/nrl.py` as the CLI entrypoint, but move reusable runtime behavior into focused modules under `system/runtime/`. Add tests using Python `unittest` and temporary copied project fixtures so production state files are not mutated during tests. Implement read-first runtime commands before any Studio UI, and make Studio a read-only command launcher over existing runtime state.

**Tech Stack:** Python 3 standard library, existing JSON files, optional existing `jsonschema` fallback behavior, shell commands run from `/Users/liuneng/Documents/Novel Research Lab`.

## Global Constraints

- Do not advance novel content.
- Do not write novel prose, first chapter, detailed chapter-by-chapter prose outline, full character cards, or freely read `novel_training_set/`.
- Keep Hermes and Antigravity as external client/manual adapters; do not claim API execution exists.
- Codex mechanical validation and Antigravity literary review must remain separate gate types.
- Studio must not own independent state; all state mutations must go through runtime commands.
- Constraint compiler must not pass raw training-set files, full single-book reports, or unrestricted research archives into Creation-phase prompts.
- Owner Gate decisions must be structured authorization records with authorized scope, forbidden scope, and expiry.
- Current workspace is not a git repository. During implementation, replace commit steps with a checkpoint note listing changed files. If a git repo is initialized later, make one commit per task using the listed commit message.

---

## File Structure

- Modify: `system/runtime/nrl.py`
  - Keep the CLI parser and command dispatch.
  - Delegate state, registry, handoff, owner-gate, compiler, and studio behavior to helper modules.

- Create: `system/runtime/nrl_paths.py`
  - Centralize root path resolution and file paths.
  - Allow tests to override the runtime root with `NRL_ROOT`.

- Create: `system/runtime/nrl_models.py`
  - Define mission status values, adapter modes, and small validation helpers.

- Create: `system/runtime/nrl_registry.py`
  - Load/save mission registry.
  - Upsert missions.
  - Record handoff attempts.
  - Validate stale attempts by input artifact hashes.

- Create: `system/runtime/nrl_owner_gate.py`
  - Create and validate Owner Gate decision records.
  - Store records under `system/runtime/owner_gate_decisions.json`.

- Create: `system/runtime/nrl_compiler.py`
  - Generate compact constraint packets under `system/runtime/constraint_packets/`.
  - Reject raw training-set paths and overly broad input archives.

- Create: `system/runtime/nrl_studio.py`
  - Generate a read-only HTML cockpit under `system/runtime/studio/index.html`.
  - Read runtime state only through local JSON loaders.

- Modify: `system/runtime/agent_adapters.json`
  - Add `supported_modes` and keep current Hermes/Antigravity mode as `manual_handoff`.

- Modify: `system/runtime/README.md`
  - Document new commands and boundaries.

- Create: `tests/test_sys3_runtime.py`
  - Exercise commands and helper functions against a copied fixture root.

- Create: `tests/fixtures/sys3_runtime/`
  - Minimal copied runtime files used by tests.

---

### Task 1: Test Harness And Runtime Root Override

**Files:**
- Create: `system/runtime/nrl_paths.py`
- Modify: `system/runtime/nrl.py`
- Create: `tests/test_sys3_runtime.py`
- Create: `tests/fixtures/sys3_runtime/system/mission_controller/current_phase_state.json`
- Create: `tests/fixtures/sys3_runtime/system/mission_controller/phase_state.schema.json`
- Create: `tests/fixtures/sys3_runtime/system/runtime/agent_adapters.json`
- Create: `tests/fixtures/sys3_runtime/system/runtime/mission_registry.json`

**Interfaces:**
- Produces: `nrl_paths.ROOT: pathlib.Path`
- Produces: `nrl_paths.runtime_path(relative: str) -> pathlib.Path`
- Produces: `tests.test_sys3_runtime.RuntimeFixture.run_cli(*args: str) -> subprocess.CompletedProcess[str]`
- Consumes: existing `system/runtime/nrl.py` CLI commands.

- [ ] **Step 1: Write the failing test**

Add this test file:

```python
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests/fixtures/sys3_runtime"
NRL = REPO_ROOT / "system/runtime/nrl.py"


class RuntimeFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "nrl"
        shutil.copytree(FIXTURE_ROOT, self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        env = os.environ.copy()
        env["NRL_ROOT"] = str(self.root)
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_status_reads_fixture_root(self):
        result = self.run_cli("status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["current_phase"], "Phase 2D")
        self.assertEqual(data["next_recommended_mission"], "Phase 2D Antigravity Outline Tree Review")


if __name__ == "__main__":
    unittest.main()
```

Create this minimal fixture `tests/fixtures/sys3_runtime/system/mission_controller/current_phase_state.json`:

```json
{
  "current_phase": "Phase 2D",
  "current_subphase": "Outline Tree Production",
  "phase_status": "OUTLINE_TREE_VALIDATED_PENDING_ANTIGRAVITY_REVIEW",
  "selected_project": "《借天改命账》",
  "next_recommended_mission": "Phase 2D Antigravity Outline Tree Review",
  "allowed_next_agents": ["Antigravity"],
  "owner_gate_required": true,
  "owner_gate_status": "PENDING_ANTIGRAVITY_REVIEW",
  "validation_status": "PASS_WITH_WARNINGS",
  "review_status": "PENDING",
  "blocked_actions": [
    "write novel prose",
    "write first chapter",
    "generate full character cards",
    "bypass Antigravity review"
  ],
  "key_artifacts": [
    {
      "name": "Phase 2D Outline Tree",
      "path": "phase2D/01_outline_tree/phase2D_outline_tree.md",
      "status": "completed"
    },
    {
      "name": "Phase 2D Codex Validation",
      "path": "phase2D/02_codex_validation/phase2D_outline_tree_validation_report.md",
      "status": "PASS_WITH_WARNINGS"
    }
  ],
  "updated_at": "2026-07-09T00:00:00+08:00",
  "notes": []
}
```

Create this minimal fixture `tests/fixtures/sys3_runtime/system/mission_controller/phase_state.schema.json`:

```json
{
  "type": "object",
  "required": ["current_phase", "phase_status", "next_recommended_mission", "blocked_actions"],
  "properties": {
    "current_phase": {"type": "string"},
    "phase_status": {"type": "string"},
    "next_recommended_mission": {"type": "string"},
    "blocked_actions": {"type": "array"}
  }
}
```

Create this minimal fixture `tests/fixtures/sys3_runtime/system/runtime/agent_adapters.json`:

```json
{
  "codex": {
    "mode": "local",
    "can_execute": true
  },
  "hermes": {
    "mode": "manual_handoff",
    "can_execute": false,
    "handoff_dir": "handoff/hermes",
    "expected_output_dir": "handoff/hermes/outputs"
  },
  "antigravity": {
    "mode": "manual_handoff",
    "can_execute": false,
    "handoff_dir": "handoff/antigravity",
    "expected_output_dir": "handoff/antigravity/outputs"
  }
}
```

Create this minimal fixture `tests/fixtures/sys3_runtime/system/runtime/mission_registry.json`:

```json
[]
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_status_reads_fixture_root -v
```

Expected: FAIL because `nrl.py` still reads the real workspace root instead of `NRL_ROOT`.

- [ ] **Step 3: Add runtime path override**

Create `system/runtime/nrl_paths.py`:

```python
from __future__ import annotations

import os
from pathlib import Path


def resolve_root() -> Path:
    override = os.environ.get("NRL_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[2]


ROOT = resolve_root()


def runtime_path(relative: str) -> Path:
    return ROOT / relative
```

Modify the top of `system/runtime/nrl.py`:

```python
from nrl_paths import ROOT, runtime_path

STATE_PATH = runtime_path("system/mission_controller/current_phase_state.json")
SCHEMA_PATH = runtime_path("system/mission_controller/phase_state.schema.json")
RULES_PATH = runtime_path("system/mission_controller/next_mission_rules.md")
CONTRACT_PATH = runtime_path("system/mission_controller/agent_task_contract.md")
ADAPTERS_PATH = runtime_path("system/runtime/agent_adapters.json")
REGISTRY_PATH = runtime_path("system/runtime/mission_registry.json")
```

Remove the old inline `ROOT = Path(__file__).resolve().parents[2]` assignment and old path assignments.

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_status_reads_fixture_root -v
```

Expected: PASS.

- [ ] **Step 5: Checkpoint**

Run:

```bash
git status --short
```

Expected in current workspace: `fatal: not a git repository`. Record changed files in the task notes. If a git repo exists in the execution workspace, commit with:

```bash
git add system/runtime/nrl.py system/runtime/nrl_paths.py tests/test_sys3_runtime.py tests/fixtures/sys3_runtime
git commit -m "test: add SYS-3 runtime fixture harness"
```

---

### Task 2: Mission Status State Machine And Registry Commands

**Files:**
- Create: `system/runtime/nrl_models.py`
- Create: `system/runtime/nrl_registry.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_sys3_runtime.py`

**Interfaces:**
- Consumes: `nrl_paths.runtime_path(relative: str) -> pathlib.Path`
- Produces: `nrl_models.MISSION_STATUSES: set[str]`
- Produces: `nrl_registry.load_registry() -> list[dict]`
- Produces: `nrl_registry.upsert_registry_mission(mission: dict, status: str, notes: list[str]) -> None`
- Produces CLI: `python3 system/runtime/nrl.py missions`
- Produces CLI: `python3 system/runtime/nrl.py check-inputs`
- Produces CLI: `python3 system/runtime/nrl.py gate-status`

- [ ] **Step 1: Write failing tests**

Append these methods to `RuntimeFixture`:

```python
    def test_missions_lists_registry(self):
        result = self.run_cli("missions")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["missions"], [])

    def test_check_inputs_reports_missing_files(self):
        result = self.run_cli("check-inputs")
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        missing = {item["path"] for item in data["inputs"] if item["exists"] is False}
        self.assertIn("phase2D/01_outline_tree/phase2D_outline_tree.md", missing)

    def test_gate_status_separates_validation_review_owner(self):
        result = self.run_cli("gate-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["validation_status"], "PASS_WITH_WARNINGS")
        self.assertEqual(data["review_status"], "PENDING")
        self.assertEqual(data["owner_gate_status"], "PENDING_ANTIGRAVITY_REVIEW")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_missions_lists_registry tests.test_sys3_runtime.RuntimeFixture.test_check_inputs_reports_missing_files tests.test_sys3_runtime.RuntimeFixture.test_gate_status_separates_validation_review_owner -v
```

Expected: FAIL with argparse invalid choice errors for missing commands.

- [ ] **Step 3: Add models and registry helpers**

Create `system/runtime/nrl_models.py`:

```python
from __future__ import annotations


MISSION_STATUSES = {
    "planned",
    "package_generated",
    "client_staged",
    "awaiting_user_confirmation",
    "awaiting_external_output",
    "output_detected",
    "ingest_started",
    "ingest_failed",
    "validation_passed",
    "validation_failed",
    "review_required",
    "owner_gate_pending",
    "completed",
    "blocked",
}

ADAPTER_MODES = {"local", "manual_handoff", "client_handoff", "api", "cli"}


def require_mission_status(status: str) -> str:
    if status not in MISSION_STATUSES:
        raise RuntimeError(f"unsupported mission status: {status}")
    return status
```

Create `system/runtime/nrl_registry.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nrl_models import require_mission_status
from nrl_paths import runtime_path


REGISTRY_PATH = runtime_path("system/runtime/mission_registry.json")


def load_json(path: Path) -> Any:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_registry() -> list[dict[str, Any]]:
    data = load_json(REGISTRY_PATH)
    if isinstance(data, list):
        return data
    raise RuntimeError("mission_registry.json must be a JSON array")


def save_registry(registry: list[dict[str, Any]]) -> None:
    write_json(REGISTRY_PATH, registry)


def upsert_registry_mission(mission: dict[str, Any], status: str, notes: list[str], now: str) -> None:
    require_mission_status(status)
    registry = load_registry()
    mission_id = mission["mission_id"]
    existing = next((m for m in registry if m.get("mission_id") == mission_id), None)
    if existing is None:
        registry.append(
            {
                "mission_id": mission_id,
                "mission_name": mission["mission_name"],
                "phase": mission["phase"],
                "responsible_agent": mission["responsible_agent"],
                "status": status,
                "input_artifacts": mission["required_inputs"],
                "output_artifacts": mission["expected_outputs"],
                "created_at": now,
                "updated_at": now,
                "gate_status": "owner_gate_required" if mission["whether_owner_gate_required"] else "owner_gate_not_required",
                "notes": notes,
            }
        )
    else:
        existing["mission_name"] = mission["mission_name"]
        existing["phase"] = mission["phase"]
        existing["responsible_agent"] = mission["responsible_agent"]
        existing["status"] = status
        existing["input_artifacts"] = mission["required_inputs"]
        existing["output_artifacts"] = sorted(dict.fromkeys(existing.get("output_artifacts", []) + mission["expected_outputs"]))
        existing["updated_at"] = now
        existing["gate_status"] = "owner_gate_required" if mission["whether_owner_gate_required"] else "owner_gate_not_required"
        existing["notes"] = sorted(dict.fromkeys(existing.get("notes", []) + notes))
    save_registry(registry)
```

- [ ] **Step 4: Add CLI commands**

In `system/runtime/nrl.py`, import registry helper:

```python
from nrl_registry import load_registry, save_registry, upsert_registry_mission
```

Remove the existing local `load_registry`, `save_registry`, and `upsert_registry_mission` definitions after moving call sites to pass `now_iso()`:

```python
upsert_registry_mission(mission, "awaiting_external_output", notes, now_iso())
```

Add these command functions:

```python
def cmd_missions(_: argparse.Namespace) -> int:
    print_json({"missions": load_registry()})
    return 0


def cmd_check_inputs(_: argparse.Namespace) -> int:
    state = load_state()
    mission = current_mission(state)
    rows = []
    for rel in mission["required_inputs"]:
        path = ROOT / rel
        rows.append({"path": rel, "exists": path.exists()})
    print_json({"mission_id": mission["mission_id"], "inputs": rows})
    return 0 if all(row["exists"] for row in rows) else 1


def cmd_gate_status(_: argparse.Namespace) -> int:
    state = load_state()
    print_json(
        {
            "phase_status": state.get("phase_status"),
            "validation_status": state.get("validation_status"),
            "review_status": state.get("review_status"),
            "owner_gate_required": state.get("owner_gate_required", False),
            "owner_gate_status": state.get("owner_gate_status"),
        }
    )
    return 0
```

Add parser entries:

```python
sub.add_parser("missions").set_defaults(func=cmd_missions)
sub.add_parser("check-inputs").set_defaults(func=cmd_check_inputs)
sub.add_parser("gate-status").set_defaults(func=cmd_gate_status)
```

Update `cmd_prepare_handoff` status from old `waiting_for_external_agent` to new `awaiting_external_output`.

- [ ] **Step 5: Run tests to verify they pass**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_missions_lists_registry tests.test_sys3_runtime.RuntimeFixture.test_check_inputs_reports_missing_files tests.test_sys3_runtime.RuntimeFixture.test_gate_status_separates_validation_review_owner -v
```

Expected: PASS.

- [ ] **Step 6: Checkpoint**

Run:

```bash
python -m unittest tests.test_sys3_runtime -v
git status --short
```

Expected: all tests PASS; current workspace reports no git repository. If a git repo exists, commit with:

```bash
git add system/runtime/nrl.py system/runtime/nrl_models.py system/runtime/nrl_registry.py tests/test_sys3_runtime.py
git commit -m "feat: add SYS-3 mission registry commands"
```

---

### Task 3: Handoff Attempt Records And Stale Output Rejection

**Files:**
- Modify: `system/runtime/nrl_registry.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_sys3_runtime.py`

**Interfaces:**
- Produces: `nrl_registry.record_handoff_attempt(mission: dict, adapter_mode: str, now: str) -> dict`
- Produces: `nrl_registry.input_hashes(paths: list[str]) -> dict[str, str]`
- Produces CLI JSON field: `handoff_attempt_id`
- Consumes: existing `prepare-handoff` and `ingest` commands.

- [ ] **Step 1: Write failing tests**

Append:

```python
    def test_prepare_handoff_records_attempt(self):
        result = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("handoff_attempt_id", data)
        registry_path = self.root / "system/runtime/mission_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        self.assertEqual(len(registry), 1)
        self.assertEqual(len(registry[0]["handoff_attempts"]), 1)
        self.assertEqual(registry[0]["handoff_attempts"][0]["expected_output_path"], "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md")

    def test_ingest_rejects_without_matching_attempt(self):
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# Review\n", encoding="utf-8")
        result = self.run_cli("ingest", "--agent", "antigravity", "--file", str(output))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no active handoff attempt", result.stderr)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_prepare_handoff_records_attempt tests.test_sys3_runtime.RuntimeFixture.test_ingest_rejects_without_matching_attempt -v
```

Expected: FAIL because attempts are not recorded and ingest accepts any existing file.

- [ ] **Step 3: Implement attempt helpers**

Add to `system/runtime/nrl_registry.py`:

```python
import hashlib


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_hashes(paths: list[str]) -> dict[str, str]:
    hashes = {}
    for rel in paths:
        hashes[rel] = sha256_file(runtime_path(rel))
    return hashes


def record_handoff_attempt(mission: dict[str, Any], adapter_mode: str, now: str) -> dict[str, Any]:
    upsert_registry_mission(mission, "awaiting_external_output", [f"adapter_mode={adapter_mode}"], now)
    registry = load_registry()
    item = next(m for m in registry if m.get("mission_id") == mission["mission_id"])
    attempts = item.setdefault("handoff_attempts", [])
    attempt_id = f"{mission['mission_id']}_attempt_{len(attempts) + 1:03d}"
    attempt = {
        "handoff_attempt_id": attempt_id,
        "mission_id": mission["mission_id"],
        "target_agent": mission["responsible_agent"],
        "adapter_mode": adapter_mode,
        "input_artifact_hashes": input_hashes(mission["required_inputs"]),
        "expected_output_path": mission["expected_outputs"][0],
        "created_at": now,
        "stale_after": "",
        "ingest_command": f"python3 system/runtime/nrl.py ingest --agent {mission['responsible_agent']} --file {mission['expected_outputs'][0]}",
        "validation_contract": "Codex validation or Owner Gate required by mission contract",
        "status": "awaiting_external_output",
    }
    attempts.append(attempt)
    item["updated_at"] = now
    save_registry(registry)
    return attempt


def find_active_attempt(mission_id: str, output_path: str) -> dict[str, Any] | None:
    registry = load_registry()
    item = next((m for m in registry if m.get("mission_id") == mission_id), None)
    if item is None:
        return None
    for attempt in reversed(item.get("handoff_attempts", [])):
        if attempt.get("expected_output_path") == output_path and attempt.get("status") == "awaiting_external_output":
            return attempt
    return None


def mark_attempt_status(mission_id: str, attempt_id: str, status: str, now: str) -> None:
    registry = load_registry()
    item = next(m for m in registry if m.get("mission_id") == mission_id)
    for attempt in item.get("handoff_attempts", []):
        if attempt.get("handoff_attempt_id") == attempt_id:
            attempt["status"] = status
            attempt["updated_at"] = now
    item["updated_at"] = now
    save_registry(registry)
```

- [ ] **Step 4: Wire attempts into prepare and ingest**

In `system/runtime/nrl.py`, import:

```python
from nrl_registry import find_active_attempt, mark_attempt_status, record_handoff_attempt
```

In `cmd_prepare_handoff`, replace direct `upsert_registry_mission(...)` with:

```python
attempt = record_handoff_attempt(mission, str(adapter.get("mode")), now_iso())
print_json(
    {
        "handoff_path": str(handoff_path.relative_to(ROOT)),
        "status": "awaiting_external_output",
        "handoff_attempt_id": attempt["handoff_attempt_id"],
    }
)
```

In `cmd_ingest`, before status update:

```python
expected_outputs = set(mission["expected_outputs"])
if rel_file not in expected_outputs:
    raise RuntimeError(f"ingest file is not an expected output for this mission: {rel_file}")
attempt = find_active_attempt(mission["mission_id"], rel_file)
if attempt is None:
    raise RuntimeError(f"no active handoff attempt for expected output: {rel_file}")
mark_attempt_status(mission["mission_id"], attempt["handoff_attempt_id"], "output_detected", now_iso())
```

- [ ] **Step 5: Run tests to verify they pass**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_prepare_handoff_records_attempt tests.test_sys3_runtime.RuntimeFixture.test_ingest_rejects_without_matching_attempt -v
```

Expected: PASS.

- [ ] **Step 6: Checkpoint**

Run:

```bash
python -m unittest tests.test_sys3_runtime -v
git status --short
```

Expected: all tests PASS; current workspace reports no git repository. If a git repo exists, commit with:

```bash
git add system/runtime/nrl.py system/runtime/nrl_registry.py tests/test_sys3_runtime.py
git commit -m "feat: record SYS-3 handoff attempts"
```

---

### Task 4: Owner Gate Decision Records

**Files:**
- Create: `system/runtime/nrl_owner_gate.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_sys3_runtime.py`

**Interfaces:**
- Produces: `nrl_owner_gate.record_owner_decision(decision: dict, now: str) -> dict`
- Produces CLI: `python3 system/runtime/nrl.py owner-gate record --decision-type accept_review --authorized-scope prepare_phase2e_entry --forbidden-scope write_novel_prose`
- Produces CLI: `python3 system/runtime/nrl.py owner-gate list`

- [ ] **Step 1: Write failing tests**

Append:

```python
    def test_owner_gate_record_and_list(self):
        record = self.run_cli(
            "owner-gate",
            "record",
            "--decision-id",
            "owner_gate_phase2d_review_acceptance_001",
            "--decision-type",
            "accept_review",
            "--authorized-scope",
            "prepare_phase2e_entry",
            "--forbidden-scope",
            "write_novel_prose",
            "--expires-after-mission",
            "phase2e_entry_preparation",
            "--owner-note",
            "accept review only",
        )
        self.assertEqual(record.returncode, 0, record.stderr)
        listed = self.run_cli("owner-gate", "list")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        data = json.loads(listed.stdout)
        self.assertEqual(data["decisions"][0]["decision_id"], "owner_gate_phase2d_review_acceptance_001")
        self.assertEqual(data["decisions"][0]["forbidden_scope"], ["write_novel_prose"])
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_owner_gate_record_and_list -v
```

Expected: FAIL with argparse invalid choice for missing `owner-gate`.

- [ ] **Step 3: Implement owner gate storage**

Create `system/runtime/nrl_owner_gate.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nrl_paths import runtime_path


OWNER_GATE_PATH = runtime_path("system/runtime/owner_gate_decisions.json")
DECISION_TYPES = {"accept_review", "request_rework", "authorize_next_phase", "authorize_adapter_upgrade"}


def load_decisions() -> list[dict[str, Any]]:
    if not OWNER_GATE_PATH.exists():
        return []
    with OWNER_GATE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    raise RuntimeError("owner_gate_decisions.json must be a JSON array")


def save_decisions(decisions: list[dict[str, Any]]) -> None:
    OWNER_GATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    OWNER_GATE_PATH.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def record_owner_decision(decision: dict[str, Any], now: str) -> dict[str, Any]:
    if decision["decision_type"] not in DECISION_TYPES:
        raise RuntimeError(f"unsupported owner decision type: {decision['decision_type']}")
    if not decision["authorized_scope"]:
        raise RuntimeError("owner decision requires at least one authorized scope")
    if not decision["forbidden_scope"]:
        raise RuntimeError("owner decision requires at least one forbidden scope")
    decisions = load_decisions()
    if any(item.get("decision_id") == decision["decision_id"] for item in decisions):
        raise RuntimeError(f"owner decision already exists: {decision['decision_id']}")
    decision["created_at"] = now
    decisions.append(decision)
    save_decisions(decisions)
    return decision
```

- [ ] **Step 4: Add CLI command**

In `system/runtime/nrl.py`, import:

```python
from nrl_owner_gate import load_decisions, record_owner_decision
```

Add:

```python
def cmd_owner_gate_record(args: argparse.Namespace) -> int:
    decision = {
        "decision_id": args.decision_id,
        "decision_type": args.decision_type,
        "authorized_scope": args.authorized_scope,
        "forbidden_scope": args.forbidden_scope,
        "expires_after_mission": args.expires_after_mission,
        "owner_note": args.owner_note,
    }
    print_json(record_owner_decision(decision, now_iso()))
    return 0


def cmd_owner_gate_list(_: argparse.Namespace) -> int:
    print_json({"decisions": load_decisions()})
    return 0
```

Add parser entries:

```python
owner = sub.add_parser("owner-gate")
owner_sub = owner.add_subparsers(dest="owner_gate_command", required=True)
owner_record = owner_sub.add_parser("record")
owner_record.add_argument("--decision-id", required=True)
owner_record.add_argument("--decision-type", required=True, choices=["accept_review", "request_rework", "authorize_next_phase", "authorize_adapter_upgrade"])
owner_record.add_argument("--authorized-scope", action="append", required=True)
owner_record.add_argument("--forbidden-scope", action="append", required=True)
owner_record.add_argument("--expires-after-mission", required=True)
owner_record.add_argument("--owner-note", default="")
owner_record.set_defaults(func=cmd_owner_gate_record)
owner_sub.add_parser("list").set_defaults(func=cmd_owner_gate_list)
```

- [ ] **Step 5: Run tests**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_owner_gate_record_and_list -v
```

Expected: PASS.

- [ ] **Step 6: Checkpoint**

Run:

```bash
python -m unittest tests.test_sys3_runtime -v
git status --short
```

Expected: all tests PASS; current workspace reports no git repository. If a git repo exists, commit with:

```bash
git add system/runtime/nrl.py system/runtime/nrl_owner_gate.py tests/test_sys3_runtime.py
git commit -m "feat: add owner gate decision records"
```

---

### Task 5: Constraint Pack / Context Compiler Runner

**Files:**
- Create: `system/runtime/nrl_compiler.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_sys3_runtime.py`

**Interfaces:**
- Produces: `nrl_compiler.compile_packet(mission: dict, packet_type: str, now: str) -> dict`
- Produces CLI: `python3 system/runtime/nrl.py compile-context --agent antigravity`
- Produces file: `system/runtime/constraint_packets/<mission_id>_<agent>_packet.json`

- [ ] **Step 1: Write failing tests**

Append:

```python
    def test_compile_context_writes_compact_packet(self):
        result = self.run_cli("compile-context", "--agent", "antigravity")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        packet_path = self.root / data["packet_path"]
        self.assertTrue(packet_path.exists())
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        self.assertEqual(packet["target_agent"], "antigravity")
        self.assertIn("must_avoid_elements", packet)
        self.assertNotIn("novel_training_set", json.dumps(packet, ensure_ascii=False))
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_compile_context_writes_compact_packet -v
```

Expected: FAIL with argparse invalid choice for missing `compile-context`.

- [ ] **Step 3: Implement compiler**

Create `system/runtime/nrl_compiler.py`:

```python
from __future__ import annotations

import json
from typing import Any

from nrl_paths import runtime_path


FORBIDDEN_INPUT_MARKERS = {"novel_training_set/", "data/raw/", "full_corpus/"}


def reject_forbidden_inputs(paths: list[str]) -> None:
    for path in paths:
        normalized = path.replace("\\", "/")
        for marker in FORBIDDEN_INPUT_MARKERS:
            if marker in normalized:
                raise RuntimeError(f"forbidden raw research input for runtime packet: {path}")


def compile_packet(mission: dict[str, Any], packet_type: str, now: str) -> dict[str, Any]:
    reject_forbidden_inputs(mission["required_inputs"])
    packet = {
        "schema_version": "1.0",
        "packet_type": packet_type,
        "mission_id": mission["mission_id"],
        "mission_name": mission["mission_name"],
        "target_agent": mission["responsible_agent"],
        "created_at": now,
        "allowed_input_paths": mission["required_inputs"],
        "source_artifact_list": mission["required_inputs"],
        "protected_state_reads": [
            "system/mission_controller/current_phase_state.json",
            "system/mission_controller/next_mission_rules.md",
            "system/mission_controller/agent_task_contract.md"
        ],
        "must_keep_beats": [
            "Review the current mission artifact only",
            "Respect the current phase and selected project",
            "Return findings in the expected output contract"
        ],
        "must_avoid_elements": mission["blocked_actions"],
        "originality_red_lines": [
            "Do not copy source novel character paths",
            "Do not reproduce proprietary setting combinations",
            "Do not convert type tropes into recognizable source-plot replicas"
        ],
        "review_criteria": [
            "mechanism-pileup risk",
            "long-form potential",
            "protagonist fate-arc traction",
            "reader follow-through",
            "structural originality"
        ],
        "expected_output_contract": mission["expected_outputs"],
    }
    out_dir = runtime_path("system/runtime/constraint_packets")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{mission['mission_id']}_{mission['responsible_agent']}_packet.json"
    out_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    packet["packet_path"] = str(out_path.relative_to(runtime_path("")))
    return packet
```

- [ ] **Step 4: Add CLI command**

In `system/runtime/nrl.py`, import:

```python
from nrl_compiler import compile_packet
```

Add:

```python
def cmd_compile_context(args: argparse.Namespace) -> int:
    state = load_state()
    mission = current_mission(state, args.agent)
    packet = compile_packet(mission, "review" if args.agent == "antigravity" else "creative", now_iso())
    print_json({"packet_path": packet["packet_path"], "mission_id": mission["mission_id"], "target_agent": mission["responsible_agent"]})
    return 0
```

Add parser entry:

```python
compile_context = sub.add_parser("compile-context")
compile_context.add_argument("--agent", required=True, choices=["hermes", "antigravity"])
compile_context.set_defaults(func=cmd_compile_context)
```

- [ ] **Step 5: Run tests**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_compile_context_writes_compact_packet -v
```

Expected: PASS.

- [ ] **Step 6: Checkpoint**

Run:

```bash
python -m unittest tests.test_sys3_runtime -v
git status --short
```

Expected: all tests PASS; current workspace reports no git repository. If a git repo exists, commit with:

```bash
git add system/runtime/nrl.py system/runtime/nrl_compiler.py tests/test_sys3_runtime.py
git commit -m "feat: add SYS-3 constraint compiler"
```

---

### Task 6: Minimal Studio Read-Only Cockpit

**Files:**
- Create: `system/runtime/nrl_studio.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_sys3_runtime.py`

**Interfaces:**
- Produces: `nrl_studio.render_studio() -> pathlib.Path`
- Produces CLI: `python3 system/runtime/nrl.py studio-build`
- Produces file: `system/runtime/studio/index.html`

- [ ] **Step 1: Write failing test**

Append:

```python
    def test_studio_build_creates_read_only_cockpit(self):
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        html = (self.root / data["studio_path"]).read_text(encoding="utf-8")
        self.assertIn("Phase 2D", html)
        self.assertIn("Phase 2D Antigravity Outline Tree Review", html)
        self.assertIn("write novel prose", html)
        self.assertIn("Read-only cockpit", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_build_creates_read_only_cockpit -v
```

Expected: FAIL with missing `studio-build` command.

- [ ] **Step 3: Implement studio renderer**

Create `system/runtime/nrl_studio.py`:

```python
from __future__ import annotations

import html
import json
from pathlib import Path

from nrl_paths import runtime_path


def load_json(relative: str):
    path = runtime_path(relative)
    if not path.exists():
        return [] if relative.endswith(".json") else {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_list(items) -> str:
    if not items:
        return "<li>None</li>"
    return "".join(f"<li>{html.escape(str(item))}</li>" for item in items)


def render_studio() -> Path:
    state = load_json("system/mission_controller/current_phase_state.json")
    registry = load_json("system/runtime/mission_registry.json")
    out_dir = runtime_path("system/runtime/studio")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    missions = "".join(
        f"<li>{html.escape(item.get('mission_id', 'unknown'))}: {html.escape(item.get('status', 'unknown'))}</li>"
        for item in registry
    )
    if not missions:
        missions = "<li>No registered missions</li>"
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Novel Research Lab Studio</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; line-height: 1.45; }}
    section {{ border-top: 1px solid #ddd; padding-top: 16px; margin-top: 16px; }}
    code {{ background: #f5f5f5; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>Novel Research Lab Studio</h1>
  <p><strong>Read-only cockpit.</strong> All state mutations must go through runtime commands.</p>
  <section>
    <h2>Current Phase</h2>
    <p>{html.escape(str(state.get("current_phase", "unknown")))} / {html.escape(str(state.get("current_subphase", "unknown")))}</p>
    <p>Status: <code>{html.escape(str(state.get("phase_status", "unknown")))}</code></p>
  </section>
  <section>
    <h2>Next Mission</h2>
    <p>{html.escape(str(state.get("next_recommended_mission", "unknown")))}</p>
  </section>
  <section>
    <h2>Blocked Actions</h2>
    <ul>{render_list(state.get("blocked_actions", []))}</ul>
  </section>
  <section>
    <h2>Gate Chain</h2>
    <ul>
      <li>Validation: {html.escape(str(state.get("validation_status", "unknown")))}</li>
      <li>Review: {html.escape(str(state.get("review_status", "unknown")))}</li>
      <li>Owner Gate: {html.escape(str(state.get("owner_gate_status", "unknown")))}</li>
    </ul>
  </section>
  <section>
    <h2>Missions</h2>
    <ul>{missions}</ul>
  </section>
</body>
</html>
"""
    out.write_text(content, encoding="utf-8")
    return out
```

- [ ] **Step 4: Add CLI command**

In `system/runtime/nrl.py`, import:

```python
from nrl_studio import render_studio
```

Add:

```python
def cmd_studio_build(_: argparse.Namespace) -> int:
    path = render_studio()
    print_json({"studio_path": str(path.relative_to(ROOT))})
    return 0
```

Add parser entry:

```python
sub.add_parser("studio-build").set_defaults(func=cmd_studio_build)
```

- [ ] **Step 5: Run tests**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_studio_build_creates_read_only_cockpit -v
```

Expected: PASS.

- [ ] **Step 6: Checkpoint**

Run:

```bash
python -m unittest tests.test_sys3_runtime -v
git status --short
```

Expected: all tests PASS; current workspace reports no git repository. If a git repo exists, commit with:

```bash
git add system/runtime/nrl.py system/runtime/nrl_studio.py tests/test_sys3_runtime.py
git commit -m "feat: add read-only SYS-3 studio"
```

---

### Task 7: Documentation And Phase 2D Replay Verification

**Files:**
- Modify: `system/runtime/README.md`
- Modify: `system/runtime/agent_adapters.json`
- Modify: `tests/test_sys3_runtime.py`
- Create: `system/runtime/sys3_replay_report.md`

**Interfaces:**
- Consumes: all commands from Tasks 1-6.
- Produces: updated runtime docs and replay report.

- [ ] **Step 1: Write failing documentation test**

Append:

```python
    def test_readme_documents_sys3_commands(self):
        readme = (REPO_ROOT / "system/runtime/README.md").read_text(encoding="utf-8")
        self.assertIn("compile-context", readme)
        self.assertIn("owner-gate", readme)
        self.assertIn("studio-build", readme)
        self.assertIn("client_handoff", readme)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_readme_documents_sys3_commands -v
```

Expected: FAIL until README is updated.

- [ ] **Step 3: Update adapter config**

Modify `system/runtime/agent_adapters.json` so each adapter includes supported modes while preserving current execution boundaries:

```json
{
  "codex": {
    "mode": "local",
    "supported_modes": ["local"],
    "can_execute": true
  },
  "hermes": {
    "mode": "manual_handoff",
    "supported_modes": ["manual_handoff", "client_handoff", "api", "cli"],
    "can_execute": false,
    "handoff_dir": "handoff/hermes",
    "expected_output_dir": "handoff/hermes/outputs"
  },
  "antigravity": {
    "mode": "manual_handoff",
    "supported_modes": ["manual_handoff", "client_handoff", "api", "cli"],
    "can_execute": false,
    "handoff_dir": "handoff/antigravity",
    "expected_output_dir": "handoff/antigravity/outputs"
  }
}
```

- [ ] **Step 4: Update README**

Add this section to `system/runtime/README.md`:

```markdown
## SYS-3 Runtime Control Patch

SYS-3 keeps Codex / NRL as the local runtime host. Hermes and Antigravity remain external adapters unless their adapter mode is explicitly upgraded by Owner Gate.

New read commands:

```bash
python3 system/runtime/nrl.py missions
python3 system/runtime/nrl.py check-inputs
python3 system/runtime/nrl.py gate-status
```

New handoff and compilation commands:

```bash
python3 system/runtime/nrl.py compile-context --agent antigravity
python3 system/runtime/nrl.py prepare-handoff --agent antigravity
python3 system/runtime/nrl.py ingest --agent antigravity --file handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md
```

Owner Gate records:

```bash
python3 system/runtime/nrl.py owner-gate record --decision-id owner_gate_phase2d_review_acceptance_001 --decision-type accept_review --authorized-scope prepare_phase2e_entry --forbidden-scope write_novel_prose --expires-after-mission phase2e_entry_preparation
python3 system/runtime/nrl.py owner-gate list
```

Studio build:

```bash
python3 system/runtime/nrl.py studio-build
```

Studio is a read-only cockpit plus command launcher. It must not maintain independent project state.

`client_handoff` is a staging mode, not API execution. If a client cannot be automated, the runtime falls back to manual handoff while preserving task packet, expected output path, and ingest command.
```

- [ ] **Step 5: Run documentation test**

Run:

```bash
python -m unittest tests.test_sys3_runtime.RuntimeFixture.test_readme_documents_sys3_commands -v
```

Expected: PASS.

- [ ] **Step 6: Run Phase 2D replay commands**

Run:

```bash
python3 system/runtime/nrl.py status
python3 system/runtime/nrl.py gate-status
python3 system/runtime/nrl.py check-inputs
python3 system/runtime/nrl.py compile-context --agent antigravity
python3 system/runtime/nrl.py prepare-handoff --agent antigravity
python3 system/runtime/nrl.py studio-build
```

Expected:

- `status` prints current Phase 2D.
- `gate-status` shows validation/review/Owner Gate separately.
- `check-inputs` returns `0` only if required files exist; otherwise it lists missing paths.
- `compile-context` writes a packet under `system/runtime/constraint_packets/`.
- `prepare-handoff` writes `handoff/antigravity/current_task.md` and records a handoff attempt.
- `studio-build` writes `system/runtime/studio/index.html`.

- [ ] **Step 7: Write replay report**

Create `system/runtime/sys3_replay_report.md`:

```markdown
# SYS-3 Phase 2D Replay Report

- replay_case: 《借天改命账》 Phase 2D Antigravity Outline Tree Review
- content_advanced: no
- runtime_checked: yes

## Commands

```text
python3 system/runtime/nrl.py status
python3 system/runtime/nrl.py gate-status
python3 system/runtime/nrl.py check-inputs
python3 system/runtime/nrl.py compile-context --agent antigravity
python3 system/runtime/nrl.py prepare-handoff --agent antigravity
python3 system/runtime/nrl.py studio-build
```

## Expected Boundary

The replay prepares and validates runtime control artifacts only. It does not authorize novel prose, first chapter generation, full character cards, detailed chapter outline generation, training-set reads, or bypassing Antigravity review or Owner Gate.
```

After running Step 6, append this section to the same file using the actual exit codes and paths printed by the commands:

```markdown
## Observed Results

- `status`: exit code recorded from the command; current phase line copied from JSON output.
- `gate-status`: exit code recorded from the command; validation, review, and Owner Gate values copied from JSON output.
- `check-inputs`: exit code recorded from the command; missing input count copied from JSON output.
- `compile-context --agent antigravity`: exit code recorded from the command; generated packet path copied from JSON output.
- `prepare-handoff --agent antigravity`: exit code recorded from the command; handoff path and handoff attempt id copied from JSON output.
- `studio-build`: exit code recorded from the command; generated studio path copied from JSON output.
```

- [ ] **Step 8: Run full tests**

Run:

```bash
python -m unittest tests.test_sys3_runtime -v
```

Expected: PASS.

- [ ] **Step 9: Checkpoint**

Run:

```bash
git status --short
```

Expected in current workspace: no git repository. If a git repo exists, commit with:

```bash
git add system/runtime/README.md system/runtime/agent_adapters.json system/runtime/sys3_replay_report.md tests/test_sys3_runtime.py
git commit -m "docs: document SYS-3 runtime replay"
```

---

## Final Verification

After all tasks are complete, run:

```bash
python -m unittest tests.test_sys3_runtime -v
python3 system/runtime/nrl.py validate-state
python3 system/runtime/nrl.py status
python3 system/runtime/nrl.py gate-status
python3 system/runtime/nrl.py missions
```

Expected:

- All unit tests pass.
- `validate-state` returns `state_valid_against_schema: true`.
- `status` shows current Phase 2D without content advancement.
- `gate-status` separates validation, Antigravity review, and Owner Gate.
- `missions` shows mission records without claiming Hermes or Antigravity API execution.

## Self-Review Notes

- Spec coverage: covers mission state machine, handoff attempt records, Owner Gate decision records, Constraint Pack / Context Compiler, Studio single source rule, Antigravity heterogeneous review role, Codex mechanical validation boundary, and Phase 2D replay tests.
- Scope boundary: does not implement novel drafting, chapter generation, API adapters, vector database, knowledge graph, or automatic Owner Gate.
- Type consistency: all helper functions used by later tasks are introduced before use.
