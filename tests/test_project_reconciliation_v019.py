import copy
import json
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_project_reconciliation import (
    JOB_ID,
    VERSION,
    build_reconciled_asset_store,
    build_reconciliation_application_readiness,
    validate_project_reconciliation_response,
)


class ProjectReconciliationV019Tests(unittest.TestCase):
    def test_validator_requires_all_quality_dimensions_and_bound_inputs(self):
        inputs = [{"path": "a", "sha256": "b"}]
        data = {
            "job_id": JOB_ID,
            "contract_version": VERSION,
            "project": "《借天改命账》",
            "input_hashes": inputs,
            "verdict": "ACCEPT_WITH_WARNINGS",
            "assessments": {
                "long_form_vitality": ["x"],
                "plot_logic": ["x"],
                "character_and_emotional_life": ["x"],
                "anti_ai_prose": ["x"],
                "asset_and_state_consistency": ["x"],
                "originality": ["x"],
            },
            "keep": [],
            "required_changes": [],
            "rejected_source_influences": [],
            "asset_patch_candidates": [],
            "volume1_production_recommendation": "bounded stress test",
        }
        self.assertTrue(validate_project_reconciliation_response(data, inputs)["valid"])
        data["assessments"].pop("anti_ai_prose")
        self.assertFalse(validate_project_reconciliation_response(data, inputs)["valid"])

    def test_asset_patch_candidates_must_replace_existing_assets_and_keep_store_valid(self):
        store = json.loads(
            (Path(__file__).resolve().parents[1] / "system/creation_assets/project_assets.v0.2.json").read_text()
        )
        existing = copy.deepcopy(store["assets"][0])
        unknown = {**existing, "asset_id": "character-b"}
        self.assertFalse(build_reconciled_asset_store(store, [unknown])["valid"])
        replacement = {**existing, "constraints": [*existing["constraints"], "新的可验证约束"]}
        result = build_reconciled_asset_store(store, [replacement])
        self.assertTrue(result["valid"], result["errors"])
        self.assertIn("新的可验证约束", result["store"]["assets"][0]["constraints"])

    def test_reconciliation_application_requires_matching_owner_scope(self):
        data = {"verdict": "ACCEPT", "asset_patch_candidates": []}
        store = json.loads(
            (Path(__file__).resolve().parents[1] / "system/creation_assets/project_assets.v0.2.json").read_text()
        )
        self.assertFalse(
            build_reconciliation_application_readiness(data, store, [], "a" * 64)["ready"]
        )
        decisions = [{
            "decision_id": "owner-reconcile",
            "authorized_scope": ["apply_project_reconciliation_v0.19"],
            "expires_after_mission": JOB_ID,
            "bound_response_sha256": "a" * 64,
        }]
        self.assertTrue(
            build_reconciliation_application_readiness(data, store, decisions, "a" * 64)["ready"]
        )


if __name__ == "__main__":
    unittest.main()
