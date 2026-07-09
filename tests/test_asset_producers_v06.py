import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
NRL = RUNTIME_DIR / "nrl.py"
sys.path.insert(0, str(RUNTIME_DIR))


class RuntimeCliCase(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )


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
        store = json.loads(
            (REPO_ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(
                encoding="utf-8"
            )
        )
        techniques = [asset for asset in store["assets"] if asset["family"] == "techniques"]
        self.assertEqual(len(techniques), 3)
        self.assertTrue(all(asset["lifecycle_state"] == "seed" for asset in techniques))
        self.assertNotIn("novel_training_set/", json.dumps(store, ensure_ascii=False))

    def test_produce_techniques_is_idempotent(self):
        first_result = self.run_cli(
            "produce-techniques",
            "--job-id",
            "job-v05-techniques-antigravity-review",
        )
        self.assertEqual(first_result.returncode, 0, first_result.stderr)
        first = json.loads(first_result.stdout)
        second_result = self.run_cli(
            "produce-techniques",
            "--job-id",
            "job-v05-techniques-antigravity-review",
        )
        self.assertEqual(second_result.returncode, 0, second_result.stderr)
        second = json.loads(second_result.stdout)
        self.assertEqual(first["asset_ids"], second["asset_ids"])
        store = json.loads(
            (REPO_ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len([asset for asset in store["assets"] if asset["family"] == "techniques"]), 3)


if __name__ == "__main__":
    unittest.main()
