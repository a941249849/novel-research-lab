import json
import subprocess
import sys
import threading
import unittest
import urllib.request
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
        self.assertIn("naming", data["supported_families"])
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


class NamingProducerCliTests(RuntimeCliCase):
    def test_produce_naming_seed_writes_schema_bound_contract(self):
        result = self.run_cli(
            "produce-naming-seed",
            "--job-id",
            "job-v05-naming-antigravity-review",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["produced_count"], 1)
        self.assertTrue(data["store_validation"]["valid"])
        store = json.loads(
            (REPO_ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(
                encoding="utf-8"
            )
        )
        asset = next(
            item
            for item in store["assets"]
            if item["asset_id"] == "naming_project_contract_seed"
        )
        self.assertEqual(asset["lifecycle_state"], "seed")
        self.assertIn("naming_roots", asset["naming"])
        self.assertIn("测名院", asset["naming"]["forbidden_terms"])

    def test_naming_contamination_is_rejected(self):
        from nrl_creation_schemas import validate_creation_asset_store

        store = {
            "version": "0.2",
            "project": "test",
            "assets": [
                {
                    "asset_id": "naming-bad",
                    "family": "naming",
                    "display_name": "bad",
                    "lifecycle_state": "seed",
                    "source_refs": ["system:test"],
                    "relationships": [],
                    "constraints": [],
                    "naming": {
                        "semantic_field": "测名院",
                        "naming_roots": ["x"],
                        "form_rules": ["x"],
                        "forbidden_collisions": [],
                        "forbidden_terms": ["测名院"],
                        "originality_policy": "x",
                    },
                }
            ],
        }
        result = validate_creation_asset_store(store)
        self.assertFalse(result["valid"])
        self.assertIn(
            "naming_anti_contamination",
            {error["code"] for error in result["errors"]},
        )


class NpcProducerCliTests(RuntimeCliCase):
    def test_produce_npc_seed_writes_state_bound_contract(self):
        result = self.run_cli(
            "produce-npc-seed",
            "--job-id",
            "job-v05-npcs-antigravity-review",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["produced_count"], 1)
        self.assertTrue(data["store_validation"]["valid"])
        store = json.loads(
            (REPO_ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(
                encoding="utf-8"
            )
        )
        asset = next(item for item in store["assets"] if item["family"] == "npcs")
        self.assertIn("information_state", asset["npc"])
        self.assertIn("recurrence_policy", asset["npc"])


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


if __name__ == "__main__":
    unittest.main()
