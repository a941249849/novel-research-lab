# NRL Architecture Reconciliation v0.4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the original Novel Research Lab architecture visible and machine-readable so v0.3 becomes a planning-pipeline layer under the final Corpus-to-Creation architecture.

**Architecture:** Add a focused Python architecture reconciliation module consumed by CLI, system-check, `studio-data`, and the Studio UI. Keep the implementation read-only and deterministic; derive runtime facts from existing source-of-truth files while keeping the fixed architecture constants in code backed by the v0.4 spec.

**Tech Stack:** Python 3 standard library, existing `unittest` test style, Vite + React + Astryx under `apps/studio/`, existing `nrl.py` CLI.

## Global Constraints

- No Phase 2F transition.
- No prose, chapter draft, or final creative asset generation.
- No Hermes execution and no Antigravity execution button.
- No raw `novel_training_set/` reads or paths in the architecture payload.
- `system-status` must remain `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.
- v0.3 pipeline must remain available and be classified as `planning_pipeline`, not as the whole architecture.
- `current_phase_state.json`, `mission_registry.json`, and `agent_adapters.json` remain runtime sources of truth.
- Studio text is Simplified Chinese; commands, IDs, and paths remain English.

---

## File Structure

- Create `system/runtime/nrl_architecture.py`
  - Owns architecture constants and `build_architecture_reconciliation(state, adapters, pipeline_status=None)`.
- Modify `system/runtime/nrl.py`
  - Adds `architecture-status` CLI command.
- Modify `system/runtime/nrl_studio_data.py`
  - Adds `architecture_reconciliation` to `studio-data`.
- Modify `system/runtime/nrl_system_check.py`
  - Adds `architecture_reconciliation` check.
- Modify `tests/test_architecture_reconciliation_v04.py`
  - New tests for CLI, contract, Studio data, system-check, and built UI labels.
- Modify `apps/studio/src/types.ts`
  - Adds TypeScript types for `architecture_reconciliation`.
- Modify `apps/studio/src/App.tsx`
  - Adds `系统架构` view and clarifies `生成管线` as the planning-pipeline layer.
- Modify `system/runtime/README.md`
  - Documents `architecture-status` and the v0.4 architecture reconciliation role.

---

### Task 1: Runtime Architecture Contract

**Files:**
- Create: `tests/test_architecture_reconciliation_v04.py`
- Create: `system/runtime/nrl_architecture.py`
- Modify: `system/runtime/nrl.py`

**Interfaces:**
- Produces: `build_architecture_reconciliation(state: dict[str, Any], adapters: dict[str, Any], pipeline_status: dict[str, Any] | None = None) -> dict[str, Any]`
- Produces CLI: `python3 system/runtime/nrl.py architecture-status`

- [ ] **Step 1: Write the failing CLI and contract tests**

```python
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
NRL = RUNTIME_DIR / "nrl.py"
sys.path.insert(0, str(RUNTIME_DIR))


class ArchitectureReconciliationCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_architecture_status_returns_v04_contract_without_raw_corpus(self):
        result = self.run_cli("architecture-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.4")
        self.assertEqual(data["fixed_identity"]["short_name"], "Novel Research Lab")
        self.assertEqual(data["fixed_identity"]["principle"], "Corpus-to-Creation")
        self.assertEqual(len(data["architecture_layers"]), 10)
        self.assertEqual(data["architecture_layers"][6]["layer_id"], "planning_pipeline")
        self.assertEqual(data["architecture_layers"][6]["child_implementation"], "corpus_pipeline_v0.3")
        self.assertIn("Core7 小批量试验", data["experiment_calibration"]["label_zh"])
        self.assertIn("runtime_pipeline_ahead_of_architecture", {item["mismatch_id"] for item in data["current_mismatch_report"]})
        self.assertEqual(data["agent_role_contract"][2]["agent"], "Hermes")
        self.assertEqual(data["agent_role_contract"][2]["status"], "paused_not_removed")
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))


class ArchitectureReconciliationContractTests(unittest.TestCase):
    def setUp(self):
        from nrl import load_adapters, load_state
        from nrl_architecture import build_architecture_reconciliation

        self.state = load_state()
        self.adapters = load_adapters()
        self.build_architecture = build_architecture_reconciliation

    def test_architecture_status_is_deterministic_and_preserves_owner_gate(self):
        first = self.build_architecture(self.state, self.adapters)
        second = self.build_architecture(self.state, self.adapters)
        self.assertEqual(first, second)
        self.assertEqual(first["production_readiness"]["system_mode"], "SYSTEM_HARDENING")
        self.assertEqual(first["production_readiness"]["content_progression"], "FROZEN_AT_OWNER_GATE")
        self.assertTrue(first["production_readiness"]["owner_gate_required"])
        self.assertFalse(first["production_readiness"]["content_generation_allowed"])
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04 -v
```

Expected: FAIL because `architecture-status` and `nrl_architecture` do not exist.

- [ ] **Step 3: Implement minimal architecture module and CLI**

Create `system/runtime/nrl_architecture.py`:

```python
from __future__ import annotations

from typing import Any

from nrl_corpus_pipeline import build_pipeline_status
from nrl_system_status import build_system_status


VERSION = "0.4"


ARCHITECTURE_LAYERS = [
    ("corpus_layer", "语料层", "protected_input", "raw corpus is protected; normal runtime uses structured derivatives", None),
    ("single_book_decomposition", "单书拆解层", "partial_data", "Book DNA / Narrative DNA / State Ledger derivatives exist with Core7 promoted assets", None),
    ("cross_book_distillation", "跨书蒸馏层", "partial_engine", "mechanism notes and synthesis exist but are not a full mechanism engine", None),
    ("research_asset_engine", "研究资产引擎", "runnable", "structured Phase 1 assets are indexed for runtime evidence", None),
    ("original_project_synthesis", "原创项目综合层", "data_ready", "current project is synthesized into Story Bible and related phase assets", None),
    ("long_form_creation_asset_os", "长篇创作资产系统", "contract_ready", "nine asset families exist as contracts; operating registries are incomplete", None),
    ("planning_pipeline", "规划管线层", "runnable", "v0.3 plans one asset family from research evidence without generating final assets", "corpus_pipeline_v0.3"),
    ("agent_review_and_production", "Agent 审查与生产层", "blocked", "Codex validates locally; Antigravity is manual review; Hermes is paused", None),
    ("runtime_control_plane", "Runtime / Control Plane 层", "runnable", "runtime reads state, validates, exposes safe actions, and serves local APIs", None),
    ("studio_cockpit", "Studio 驾驶舱层", "partial", "Studio exposes system state and must now expose architecture reconciliation", None),
]


def _layers() -> list[dict[str, Any]]:
    return [
        {
            "order": index + 1,
            "layer_id": layer_id,
            "label_zh": label_zh,
            "status": status,
            "purpose": purpose,
            "child_implementation": child,
        }
        for index, (layer_id, label_zh, status, purpose, child) in enumerate(ARCHITECTURE_LAYERS)
    ]


def _agent_roles(system_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "agent": "Codex",
            "status": "local_runtime_host",
            "role": "本地系统宿主 / Runtime / 工程 / 校验 / 编排",
            "execution_boundary": "may execute local runtime and validation only",
        },
        {
            "agent": "Antigravity",
            "status": "manual_external_literary_review",
            "role": "人工外部文学审查 / 长篇生命力评估",
            "execution_boundary": "manual handoff only",
        },
        {
            "agent": "Hermes",
            "status": system_status["hermes_execution_status"],
            "display_status": f"Hermes: {system_status['hermes_execution_status']}",
            "role": "后期写手 / 文学增强 / 受控创意生成",
            "execution_boundary": "paused until explicit Owner authorization",
        },
        {
            "agent": "Web GPT",
            "status": "architecture_review_only",
            "role": "架构互审和源上下文裁决",
            "execution_boundary": "not a task dispatcher",
        },
        {
            "agent": "Owner",
            "status": "gate_authority",
            "role": "阶段、外部 Agent、内容生产授权",
            "execution_boundary": "manual decision authority",
        },
    ]


def build_architecture_reconciliation(
    state: dict[str, Any],
    adapters: dict[str, Any],
    pipeline_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    system_status = build_system_status(state, adapters)
    pipeline = pipeline_status or build_pipeline_status(state, adapters)
    return {
        "version": VERSION,
        "source_context": {
            "conversation_title": "中文玄幻小说汇总",
            "accepted_on": "2026-07-09",
            "source_role": "architecture_review_baseline",
        },
        "fixed_identity": {
            "short_name": "Novel Research Lab",
            "principle": "Corpus-to-Creation",
            "positioning_zh": "基于中文热门长篇小说语料研究蒸馏的原创长篇小说创作引擎",
            "not_a": ["generic writing app", "InkOS clone", "document pipeline"],
            "core_chain": [
                "training corpus",
                "single-book decomposition",
                "cross-book mechanism distillation",
                "narrative law / mechanism library",
                "original project synthesis",
                "Story Bible",
                "long-form creation asset system",
                "outline / chapter planning",
                "draft",
                "review",
                "state ledger",
                "continuous long-form production",
            ],
        },
        "architecture_layers": _layers(),
        "experiment_calibration": {
            "label_zh": "Core7 小批量试验",
            "status": "accepted_as_calibration_basis",
            "scope": "Core7 promoted assets are real calibration data; remaining corpus is not assumed complete.",
            "production_meaning": "small-batch validation supports architecture convergence before full production execution",
        },
        "implementation_alignment": {
            "pipeline_version": pipeline["version"],
            "pipeline_id": pipeline["pipeline_id"],
            "pipeline_layer": "planning_pipeline",
            "classification": "child_implementation_not_full_architecture",
            "next_family": pipeline["next_family"]["family"],
        },
        "agent_role_contract": _agent_roles(system_status),
        "current_mismatch_report": [
            {
                "mismatch_id": "runtime_pipeline_ahead_of_architecture",
                "severity": "high",
                "summary": "Runtime and pipeline work advanced before source architecture reconciliation was locked.",
                "correction": "Classify v0.3 as planning_pipeline and expose the ten-layer architecture in runtime and Studio.",
            },
            {
                "mismatch_id": "product_visibility_gap",
                "severity": "high",
                "summary": "The Owner could not see how research assets, agents, runtime, and creation assets form one system.",
                "correction": "Studio must expose architecture layers, Core7 calibration, mismatch report, and next architecture action.",
            },
        ],
        "production_readiness": {
            "system_mode": system_status["operating_mode"],
            "content_progression": system_status["content_progression"],
            "owner_gate_required": system_status["owner_gate_required"],
            "owner_gate_status": system_status["owner_gate_status"],
            "content_generation_allowed": False,
            "hermes_execution_status": system_status["hermes_execution_status"],
        },
        "next_architecture_action": {
            "action_id": "architecture_reconciliation_v0_4",
            "label_zh": "锁定系统架构并把 v0.3 归位为规划管线层",
            "safe_command": "python3 system/runtime/nrl.py architecture-status",
            "blocked_actions": pipeline["forbidden_actions"],
        },
    }
```

Modify `system/runtime/nrl.py`:

```python
from nrl_architecture import build_architecture_reconciliation


def cmd_architecture_status(_: argparse.Namespace) -> int:
    print_json(build_architecture_reconciliation(load_state(), load_adapters()))
    return 0
```

Add parser registration:

```python
subparsers.add_parser("architecture-status").set_defaults(func=cmd_architecture_status)
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04 -v
```

Expected: PASS for Task 1 tests.

- [ ] **Step 5: Commit**

```bash
git add tests/test_architecture_reconciliation_v04.py system/runtime/nrl_architecture.py system/runtime/nrl.py
git commit -m "feat: add architecture reconciliation status"
```

---

### Task 2: Studio Data and System Check Integration

**Files:**
- Modify: `tests/test_architecture_reconciliation_v04.py`
- Modify: `system/runtime/nrl_studio_data.py`
- Modify: `system/runtime/nrl_system_check.py`

**Interfaces:**
- Consumes: `build_architecture_reconciliation(...)`
- Produces: `studio-data["architecture_reconciliation"]`
- Produces: `system-check` check id `architecture_reconciliation`

- [ ] **Step 1: Add failing integration tests**

Append to `tests/test_architecture_reconciliation_v04.py`:

```python
class ArchitectureReconciliationIntegrationTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_studio_data_contains_architecture_reconciliation(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("architecture_reconciliation", data)
        architecture = data["architecture_reconciliation"]
        self.assertEqual(architecture["version"], "0.4")
        self.assertEqual(architecture["implementation_alignment"]["pipeline_layer"], "planning_pipeline")
        self.assertEqual(len(architecture["architecture_layers"]), 10)

    def test_system_check_includes_architecture_reconciliation(self):
        result = self.run_cli("system-check")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["passed"])
        check_ids = {check["check_id"] for check in data["checks"]}
        self.assertIn("architecture_reconciliation", check_ids)
        check = next(item for item in data["checks"] if item["check_id"] == "architecture_reconciliation")
        self.assertEqual(check["detail"]["version"], "0.4")
        self.assertEqual(check["detail"]["layer_count"], 10)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04 -v
```

Expected: FAIL because `studio-data` and `system-check` are not wired.

- [ ] **Step 3: Wire runtime data**

Modify `system/runtime/nrl_studio_data.py`:

```python
from nrl_architecture import build_architecture_reconciliation
```

Inside `build_studio_data`, after `corpus_pipeline` is built:

```python
architecture_reconciliation = build_architecture_reconciliation(
    state,
    adapters,
    pipeline_status=corpus_pipeline,
)
```

Add to returned object:

```python
"architecture_reconciliation": architecture_reconciliation,
```

Modify `system/runtime/nrl_system_check.py`:

```python
from nrl_architecture import build_architecture_reconciliation
```

Inside `run_system_check`, after `pipeline`:

```python
architecture = build_architecture_reconciliation(state, adapters, pipeline_status=pipeline)
architecture_payload = json.dumps(architecture, ensure_ascii=False)
architecture_passed = (
    architecture["version"] == "0.4"
    and len(architecture["architecture_layers"]) == 10
    and architecture["architecture_layers"][6]["layer_id"] == "planning_pipeline"
    and architecture["architecture_layers"][6]["child_implementation"] == "corpus_pipeline_v0.3"
    and architecture["production_readiness"]["owner_gate_required"]
    and architecture["production_readiness"]["hermes_execution_status"] == "paused_not_removed"
    and "novel_training_set/" not in architecture_payload
)
```

Append a check:

```python
{
    "check_id": "architecture_reconciliation",
    "passed": architecture_passed,
    "detail": {
        "version": architecture["version"],
        "layer_count": len(architecture["architecture_layers"]),
        "pipeline_layer": architecture["implementation_alignment"]["pipeline_layer"],
    },
},
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04 tests.test_control_plane_v02 tests.test_corpus_pipeline_v03 -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_architecture_reconciliation_v04.py system/runtime/nrl_studio_data.py system/runtime/nrl_system_check.py
git commit -m "feat: surface architecture reconciliation in runtime"
```

---

### Task 3: Studio Architecture View

**Files:**
- Modify: `tests/test_architecture_reconciliation_v04.py`
- Modify: `apps/studio/src/types.ts`
- Modify: `apps/studio/src/App.tsx`

**Interfaces:**
- Consumes: `StudioData["architecture_reconciliation"]`
- Produces: SideNav view `系统架构`

- [ ] **Step 1: Add failing Studio build-content test**

Append to `tests/test_architecture_reconciliation_v04.py`:

```python
class ArchitectureReconciliationStudioTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_studio_build_contains_architecture_view_labels(self):
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (REPO_ROOT / "system/runtime/studio/index.html").read_text(encoding="utf-8")
        self.assertIn("系统架构", html)
        self.assertIn("Corpus-to-Creation", html)
        self.assertIn("Core7 小批量试验", html)
        self.assertIn("Hermes: paused_not_removed", html)
        self.assertIn("Owner Gate", html)
        self.assertNotIn("/api/actions/execute-hermes", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04.ArchitectureReconciliationStudioTests -v
```

Expected: FAIL because Studio lacks the architecture view labels.

- [ ] **Step 3: Add TypeScript types**

Add to `StudioData` in `apps/studio/src/types.ts`:

```ts
architecture_reconciliation: {
  version: string;
  source_context: {
    conversation_title: string;
    accepted_on: string;
    source_role: string;
  };
  fixed_identity: {
    short_name: string;
    principle: string;
    positioning_zh: string;
    not_a: string[];
    core_chain: string[];
  };
  architecture_layers: Array<{
    order: number;
    layer_id: string;
    label_zh: string;
    status: string;
    purpose: string;
    child_implementation: string | null;
  }>;
  experiment_calibration: {
    label_zh: string;
    status: string;
    scope: string;
    production_meaning: string;
  };
  implementation_alignment: {
    pipeline_version: string;
    pipeline_id: string;
    pipeline_layer: string;
    classification: string;
    next_family: string;
  };
  agent_role_contract: Array<{
    agent: string;
    status: string;
    display_status?: string;
    role: string;
    execution_boundary: string;
  }>;
  current_mismatch_report: Array<{
    mismatch_id: string;
    severity: string;
    summary: string;
    correction: string;
  }>;
  production_readiness: {
    system_mode: string;
    content_progression: string;
    owner_gate_required: boolean;
    owner_gate_status: string;
    content_generation_allowed: boolean;
    hermes_execution_status: string;
  };
  next_architecture_action: {
    action_id: string;
    label_zh: string;
    safe_command: string;
    blocked_actions: string[];
  };
};
```

Add matching `EMPTY_DATA.architecture_reconciliation`.

- [ ] **Step 4: Add `系统架构` view**

Modify `ViewID`:

```ts
type ViewID = 'overview' | 'architecture' | 'research' | 'creation' | 'pipeline' | 'agents' | 'runtime';
```

Add view label:

```ts
architecture: {label: '系统架构', subtitle: '源架构、Core7 校准与 v0.3 归位', icon: 'info'},
```

Add an `ArchitectureView` component that renders:

```tsx
function ArchitectureView({data, compact}: {data: StudioData; compact: boolean}) {
  const architecture = data.architecture_reconciliation;
  const layerRows: TableRow[] = architecture.architecture_layers.map((layer) => ({
    id: layer.layer_id,
    order: layer.order,
    layer: layer.label_zh,
    status: statusNames[layer.status] || layer.status,
    child: layer.child_implementation || '无',
    purpose: layer.purpose,
  }));
  const agentRows: TableRow[] = architecture.agent_role_contract.map((item) => ({
    id: item.agent,
    agent: item.agent,
    status: item.display_status || item.status,
    role: item.role,
    boundary: item.execution_boundary,
  }));

  return (
    <Section padding={5}>
      <VStack gap={5}>
        <Banner
          status="info"
          title={`${architecture.fixed_identity.short_name} / ${architecture.fixed_identity.principle}`}
          description={architecture.fixed_identity.positioning_zh}
        />
        <Grid columns={{minWidth: 220, max: 4, repeat: 'fit'}} gap={3}>
          <SummaryCard label="架构版本" value={architecture.version} />
          <SummaryCard label="校准依据" value={architecture.experiment_calibration.label_zh} status={architecture.experiment_calibration.status} />
          <SummaryCard label="v0.3 归位" value={architecture.implementation_alignment.pipeline_layer} />
          <SummaryCard label="Owner Gate" value={architecture.production_readiness.owner_gate_status} status="blocked" />
        </Grid>
        <Section title="Corpus-to-Creation 链路">
          <List>
            {architecture.fixed_identity.core_chain.map((item) => (
              <ListItem key={item} title={item} />
            ))}
          </List>
        </Section>
        {compact ? (
          <List>
            {architecture.architecture_layers.map((layer) => (
              <ListItem key={layer.layer_id} title={`${layer.order}. ${layer.label_zh}`} description={layer.purpose} />
            ))}
          </List>
        ) : (
          <Table
            aria-label="architecture layers"
            columns={[
              {key: 'order', name: '#', width: pixel(56)},
              {key: 'layer', name: '架构层', width: proportional(1)},
              {key: 'status', name: '状态', width: pixel(130)},
              {key: 'child', name: '子实现', width: pixel(180)},
              {key: 'purpose', name: '职责', width: proportional(2)},
            ]}
            rows={layerRows}
          />
        )}
        <Banner
          status="warning"
          title="当前偏差修正"
          description={architecture.current_mismatch_report.map((item) => `${item.summary} ${item.correction}`).join(' ')}
        />
        <Section title="Agent 角色边界">
          {compact ? (
            <List>
              {architecture.agent_role_contract.map((item) => (
                <ListItem key={item.agent} title={`${item.agent}: ${item.display_status || item.status}`} description={item.role} />
              ))}
            </List>
          ) : (
            <Table
              aria-label="agent role contract"
              columns={[
                {key: 'agent', name: 'Agent', width: pixel(150)},
                {key: 'status', name: '状态', width: pixel(220)},
                {key: 'role', name: '职责', width: proportional(1)},
                {key: 'boundary', name: '边界', width: proportional(1)},
              ]}
              rows={agentRows}
            />
          )}
        </Section>
        <Banner
          status="success"
          title={architecture.next_architecture_action.label_zh}
          description={architecture.next_architecture_action.safe_command}
        />
      </VStack>
    </Section>
  );
}
```

Wire the view in the SideNav and render switch. Update the `生成管线` view title/subtitle to make clear it is the `Planning Pipeline layer`.

- [ ] **Step 5: Run test and frontend build**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04.ArchitectureReconciliationStudioTests -v
npm run build --prefix apps/studio
```

Expected: PASS and Vite build succeeds.

- [ ] **Step 6: Commit**

```bash
git add tests/test_architecture_reconciliation_v04.py apps/studio/src/types.ts apps/studio/src/App.tsx
git commit -m "feat: add Studio architecture reconciliation view"
```

---

### Task 4: Documentation and Full Verification

**Files:**
- Modify: `system/runtime/README.md`

**Interfaces:**
- Documents: `architecture-status`
- Verifies: v0.4, v0.3, v0.2, SYS-3 runtime checks remain compatible.

- [ ] **Step 1: Add README note**

Add a `Architecture Reconciliation v0.4` section:

```markdown
## Architecture Reconciliation v0.4

`architecture-status` exposes the accepted Novel Research Lab source
architecture as a read-only runtime contract. It classifies v0.3
`corpus_pipeline` as the `planning_pipeline` layer under the full
Corpus-to-Creation architecture, not as the whole system.

```bash
python3 system/runtime/nrl.py architecture-status
python3 system/runtime/nrl.py studio-data
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py studio-build
```

The command must remain read-only. It does not progress Phase 2E, call Hermes,
call Antigravity, read `novel_training_set/`, or generate creative assets.
```

- [ ] **Step 2: Run full verification**

Run:

```bash
python3 -m unittest tests.test_architecture_reconciliation_v04 tests.test_corpus_pipeline_v03 tests.test_control_plane_v02 tests.test_sys3_runtime -v
python3 system/runtime/nrl.py validate-state
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py architecture-status
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py studio-build
npm run build --prefix apps/studio
npx --prefix apps/studio astryx doctor
git diff --check
```

Expected:

- unittest: all tests pass.
- `validate-state`: valid.
- `system-status`: `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.
- `architecture-status`: version `0.4`.
- `system-check`: passed and includes `architecture_reconciliation`.
- `studio-build`: writes `system/runtime/studio/index.html`.
- Vite build succeeds.
- `astryx doctor`: pass.
- `git diff --check`: no output.

- [ ] **Step 3: Commit**

```bash
git add system/runtime/README.md system/runtime/studio apps/studio/public/nrl-studio-data.json
git commit -m "docs: document architecture reconciliation v0.4"
```

---

## Self-Review

- Spec coverage: all v0.4 acceptance points map to Tasks 1-4.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation steps are present.
- Type consistency: `architecture_reconciliation` shape is defined once in Python, mirrored in TypeScript, and asserted through CLI/Studio tests.
