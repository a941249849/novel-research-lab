import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_project_reconciliation import (
    JOB_ID,
    VERSION,
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


if __name__ == "__main__":
    unittest.main()
