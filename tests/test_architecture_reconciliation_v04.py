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
        self.assertEqual(
            first["production_readiness"]["content_progression"],
            "FROZEN_AT_OWNER_GATE",
        )
        self.assertTrue(first["production_readiness"]["owner_gate_required"])
        self.assertFalse(first["production_readiness"]["content_generation_allowed"])


if __name__ == "__main__":
    unittest.main()
