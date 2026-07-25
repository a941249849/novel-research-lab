import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "system/runtime"))
from nrl_creation_schemas import FAMILIES, validate_creation_asset_store

PROJECT = ROOT / "projects/hundred-crafts-night-procession"


class HundredCraftsVolumeOneTests(unittest.TestCase):
    def _read(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_volume_one_outline_is_schema_valid_and_production_sized(self) -> None:
        outline = self._read(PROJECT / "production_runtime/plans/volume1_outline.v1.json")
        schema = self._read(ROOT / "system/production_runtime/schemas/volume_outline.schema.json")
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(outline, schema)
        self.assertFalse(outline["prose_authorized"])
        self.assertEqual(len(outline["chapters"]), 66)
        self.assertEqual([row["chapter"] for row in outline["chapters"]], list(range(1, 67)))
        self.assertEqual({row["act"] for row in outline["chapters"]}, {"A1", "A2", "A3", "A4", "A5", "A6"})
        self.assertEqual({row["pov"] for row in outline["chapters"]}, {"周砺", "程雪青", "杜承礼", "林岱", "马小满"})

    def test_outline_references_resolve_and_every_chapter_changes_state(self) -> None:
        outline = self._read(PROJECT / "production_runtime/plans/volume1_outline.v1.json")
        store = self._read(PROJECT / "creation_assets/project_assets.json")
        known = {item["asset_id"] for item in store["assets"]}
        for chapter in outline["chapters"]:
            self.assertTrue(set(chapter["asset_refs"]) <= known)
            self.assertTrue(chapter["irreversible_change"])
        self.assertNotIn("novel_training_set/", json.dumps(outline, ensure_ascii=False))

    def test_project_assets_cover_all_families_and_validate(self) -> None:
        store = self._read(PROJECT / "creation_assets/project_assets.json")
        validation = validate_creation_asset_store(store)
        self.assertTrue(validation["valid"], validation["errors"])
        self.assertEqual({item["family"] for item in store["assets"]}, set(FAMILIES))
        self.assertGreaterEqual(len(store["assets"]), 30)
        self.assertNotIn("novel_training_set/", json.dumps(store, ensure_ascii=False))

    def test_controlled_sample_contract_is_exactly_bounded(self) -> None:
        run = self._read(PROJECT / "production_runtime/plans/controlled_sample_run.v0.1.json")
        self.assertEqual(run["status"], "sample_test_passed")
        self.assertTrue(run["review_result"]["sample_test_passed"])
        self.assertFalse(run["controlled_continuity_validation_authorized"])
        self.assertEqual(
            [row["chapters"] for row in run["windows"]],
            [[8, 9, 10], [24, 25, 26], [49, 50, 51]],
        )
        self.assertEqual(run["routes"]["writer"], "gpt-5.6-terra")
        self.assertEqual(run["routes"]["observer"], "gpt-5.6-luna")
        self.assertEqual(run["routes"]["reviewer"], "gpt-5.6-sol")
        self.assertFalse(run["continuous_prose_authorized"])
        self.assertFalse(run["publish_authorized"])
        known = {
            row["asset_id"]
            for row in self._read(PROJECT / "creation_assets/project_assets.json")["assets"]
        }
        for window in run["windows"]:
            self.assertTrue(set(window["required_asset_ids"]) <= known)
        self.assertNotIn("novel_training_set/", json.dumps(run, ensure_ascii=False))

    def test_cli_validates_selected_project_assets(self) -> None:
        result = subprocess.run(
            ["python3", "system/runtime/nrl.py", "--project", "hundred-crafts-night-procession", "validate-creation-assets"],
            cwd=ROOT,
            env={**os.environ, "NRL_PROJECT_ID": "hundred-crafts-night-procession"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertIn("projects/hundred-crafts-night-procession", payload["store_path"])

    def test_project_validation_includes_assets_and_volume_outline(self) -> None:
        result = subprocess.run(
            ["python3", "system/runtime/nrl.py", "--project", "hundred-crafts-night-procession", "project-validate"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["checks"]["creation_assets"]["valid"])
        self.assertTrue(payload["checks"]["volume_plan"]["valid"])
        self.assertEqual(payload["checks"]["volume_plan"]["chapter_count"], 66)
        self.assertTrue(payload["checks"]["continuity_validation"]["valid"])
        self.assertEqual(
            payload["checks"]["continuity_validation"]["review_verdict"],
            "ACCEPT_CONTINUITY_TEST",
        )
        self.assertEqual(payload["checks"]["continuity_validation"]["generated_prose_count"], 14)
        self.assertNotIn("prose_chapters", payload["checks"]["continuity_validation"])

    def test_project_preserves_sample_evidence_after_formal_authorization(self) -> None:
        result = subprocess.run(
            ["python3", "system/runtime/nrl.py", "--project", "hundred-crafts-night-procession", "project-status"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["controlled_sample_ready"])
        self.assertTrue(payload["sample_test_authorized"])
        self.assertTrue(payload["sample_test_passed"])
        self.assertEqual(payload["controlled_sample_status"], "sample_test_passed")
        self.assertEqual(
            payload["sample_owner_decision_id"],
            "owner_hundred_crafts_volume1_controlled_samples_20260718",
        )
        self.assertTrue(payload["content_authorized"])
        self.assertTrue(payload["ready_for_prose"])
        self.assertTrue(payload["continuity_test_authorized"])
        self.assertTrue(payload["continuity_test_passed"])
        self.assertEqual(payload["continuity_status"], "continuity_test_passed")
        self.assertEqual(
            payload["continuity_owner_decision_id"],
            "owner_hundred_crafts_continuity_validation_20260719",
        )
        self.assertEqual(payload["accepted_chapters"], 7)
        self.assertEqual(payload["next_action"], "continue governed production")


if __name__ == "__main__":
    unittest.main()
