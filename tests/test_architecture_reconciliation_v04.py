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
        self.assertEqual(
            data["architecture_layers"][6]["child_implementation"],
            "corpus_pipeline_v0.3",
        )
        self.assertIn("Core7 小批量试验", data["experiment_calibration"]["label_zh"])
        self.assertIn(
            "runtime_pipeline_ahead_of_architecture",
            {item["mismatch_id"] for item in data["current_mismatch_report"]},
        )
        self.assertEqual(data["agent_role_contract"][2]["agent"], "Hermes")
        self.assertEqual(data["agent_role_contract"][2]["status"], "ready")
        self.assertEqual(data["agent_role_contract"][1]["agent"], "Antigravity")
        self.assertEqual(data["agent_role_contract"][1]["status"], "ready")
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
        self.assertEqual(
            first["production_readiness"]["content_progression"],
            "FROZEN_AT_OWNER_GATE",
        )
        self.assertTrue(first["production_readiness"]["owner_gate_required"])
        self.assertFalse(first["production_readiness"]["content_generation_allowed"])


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
        self.assertEqual(
            architecture["implementation_alignment"]["pipeline_layer"],
            "planning_pipeline",
        )
        self.assertEqual(len(architecture["architecture_layers"]), 10)

    def test_system_check_includes_architecture_reconciliation(self):
        result = self.run_cli("system-check")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["passed"])
        check_ids = {check["check_id"] for check in data["checks"]}
        self.assertIn("architecture_reconciliation", check_ids)
        check = next(
            item
            for item in data["checks"]
            if item["check_id"] == "architecture_reconciliation"
        )
        self.assertEqual(check["detail"]["version"], "0.4")
        self.assertEqual(check["detail"]["layer_count"], 10)


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
        html = (REPO_ROOT / "system/runtime/studio/index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("系统架构", html)
        self.assertIn("#architecture", html)
        self.assertIn("Corpus-to-Creation", html)
        self.assertIn("Core7 小批量试验", html)
        self.assertIn("Hermes: ready", html)
        self.assertIn("CLI 协作文学审查", html)
        self.assertNotIn("人工外部文学审查", html)
        self.assertIn("Owner Gate", html)
        self.assertNotIn("/api/actions/execute-hermes", html)


if __name__ == "__main__":
    unittest.main()
