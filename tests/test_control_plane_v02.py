import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
NRL = RUNTIME_DIR / "nrl.py"
sys.path.insert(0, str(RUNTIME_DIR))


class ControlPlaneCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_hardening_status_has_allowed_states_and_one_next_action(self):
        result = self.run_cli("hardening-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["mode"], "SYSTEM_HARDENING")
        self.assertEqual(len(data["capabilities"]), 8)
        self.assertEqual(
            len([item for item in data["capabilities"] if item["is_next_safe_action"]]),
            1,
        )
        self.assertTrue(
            {item["status"] for item in data["capabilities"]}
            <= {"missing", "contract_ready", "data_ready", "runnable", "blocked"}
        )

    def test_research_assets_indexes_reviewed_phase1_assets(self):
        result = self.run_cli("research-assets", "--title", "遮天")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreaterEqual(data["summary"]["returned"], 4)
        self.assertTrue(all(item["title"] == "遮天" for item in data["items"]))
        self.assertIn("formal", {item["review_state"] for item in data["items"]})
        self.assertNotIn(
            "novel_training_set/",
            json.dumps(data, ensure_ascii=False),
        )

    def test_research_assets_filters_mechanism_category(self):
        result = self.run_cli("research-assets", "--category", "升级与境界机制")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreater(data["summary"]["returned"], 0)
        self.assertTrue(
            all("升级与境界机制" in item["categories"] for item in data["items"])
        )

    def test_creation_schema_registry_exposes_nine_draft7_families(self):
        result = self.run_cli("creation-schemas")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["draft"], "http://json-schema.org/draft-07/schema#")
        self.assertEqual(data["summary"]["family_count"], 9)
        self.assertTrue(data["summary"]["all_schemas_valid"])

    def test_validate_creation_assets_accepts_empty_project_store(self):
        result = self.run_cli("validate-creation-assets")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual(data["summary"]["asset_count"], 0)

    def test_studio_data_adds_v02_sections_without_removing_v01_sections(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        for key in (
            "system_identity",
            "current_project",
            "owner_gate",
            "control_plane",
            "capability_roadmap",
            "research_asset_catalog",
            "creation_schema_registry",
            "safe_action_catalog",
        ):
            self.assertIn(key, data)


class CreationAssetValidationTests(unittest.TestCase):
    def setUp(self):
        from nrl_creation_schemas import validate_creation_asset_store

        self.validate = validate_creation_asset_store

    def asset(self, asset_id, family, display_name, **extra):
        return {
            "asset_id": asset_id,
            "family": family,
            "display_name": display_name,
            "lifecycle_state": "seed",
            "source_refs": ["system:test"],
            "relationships": [],
            "constraints": [],
            **extra,
        }

    def test_rejects_duplicate_asset_ids(self):
        store = {
            "version": "0.2",
            "project": "test",
            "assets": [
                self.asset("char-1", "characters", "甲"),
                self.asset("char-1", "characters", "乙"),
            ],
        }
        result = self.validate(store)
        self.assertFalse(result["valid"])
        self.assertIn("duplicate_asset_id", {error["code"] for error in result["errors"]})

    def test_rejects_unresolved_relationship_reference(self):
        asset = self.asset("char-1", "characters", "甲")
        asset["relationships"] = [
            {"target_id": "missing-1", "relation_type": "opposes"}
        ]
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("unresolved_reference", {error["code"] for error in result["errors"]})

    def test_rejects_normalized_name_collision(self):
        store = {
            "version": "0.2",
            "project": "test",
            "assets": [
                self.asset("char-1", "characters", "天 命"),
                self.asset("char-2", "characters", "天命"),
            ],
        }
        result = self.validate(store)
        self.assertFalse(result["valid"])
        self.assertIn("name_collision", {error["code"] for error in result["errors"]})

    def test_rejects_illegal_lifecycle_transition(self):
        asset = self.asset(
            "char-1",
            "characters",
            "甲",
            lifecycle_state="seed",
            previous_lifecycle_state="retired",
        )
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("invalid_lifecycle_transition", {error["code"] for error in result["errors"]})

    def test_rejects_family_payload_mismatch(self):
        asset = self.asset(
            "tech-1",
            "techniques",
            "试招",
            character={"role": "protagonist"},
        )
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("schema_validation", {error["code"] for error in result["errors"]})


if __name__ == "__main__":
    unittest.main()
