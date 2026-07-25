import sys
import json
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

import nrl_production_calibration as calibration


class ProductionCalibrationTests(unittest.TestCase):
    def test_planned_calibration_blocks_direct_prose(self):
        with mock.patch.object(calibration, "CALIBRATION_PATH") as path:
            path.exists.return_value = False
            result = calibration.build_direct_writer_calibration_status()
        self.assertFalse(result["valid"])
        self.assertEqual(result["status"], "missing")

    def test_accepted_calibration_requires_three_models_and_nine_runs(self):
        run = {
            "run_id": "candidate-11",
            "blind_label": "样本 01",
            "scenario_id": "cause_under_pressure",
            "model": "gpt-5.6-sol",
            "candidate_path": "system/production_runtime/calibration/candidates/candidate-11.md",
            "sha256": "a" * 64,
            "review_status": "accepted",
        }
        payload = {
            "version": "0.21",
            "status": "accepted",
            "models": ["gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"],
            "criteria": ["continuity"],
            "runs": [dict(run, run_id=f"candidate-{index}") for index in range(9)],
            "independent_reviewer_verdict": "ACCEPT",
            "routing_decision": "Sol showrunner; Terra writer; Luna observer",
        }
        with mock.patch.object(calibration, "CALIBRATION_PATH") as path:
            path.exists.return_value = True
            path.read_text.return_value = json.dumps(payload)
            result = calibration.build_direct_writer_calibration_status()
        self.assertTrue(result["valid"])

    def test_acceptance_rejects_unreviewed_candidates(self):
        run = {
            "run_id": "candidate-11",
            "blind_label": "样本 01",
            "scenario_id": "cause_under_pressure",
            "model": "gpt-5.6-sol",
            "candidate_path": "candidate.md",
            "sha256": "a" * 64,
            "review_status": "pending_blind_review",
        }
        payload = {
            "version": "0.21", "status": "accepted", "models": list(calibration.MODELS),
            "criteria": ["continuity"], "runs": [dict(run, run_id=str(index)) for index in range(9)],
            "independent_reviewer_verdict": "ACCEPT", "routing_decision": "route",
        }
        with mock.patch.object(calibration, "CALIBRATION_PATH") as path:
            path.exists.return_value = True
            path.read_text.return_value = json.dumps(payload)
            result = calibration.build_direct_writer_calibration_status()
        self.assertFalse(result["valid"])

    def test_route_restricted_acceptance_allows_conditional_non_writer_models(self):
        base = {
            "blind_label": "样本", "scenario_id": "scenario", "candidate_path": "candidate.md",
            "sha256": "a" * 64,
        }
        runs = [
            dict(base, run_id=str(index), model=calibration.MODELS[index % 3], review_status="accepted" if index % 3 == 0 else "conditional")
            for index in range(9)
        ]
        payload = {
            "version": "0.21", "status": "accepted_route_restricted", "models": list(calibration.MODELS),
            "criteria": ["continuity"], "runs": runs,
            "independent_reviewer_verdict": "ACCEPT_SOL_ONLY", "routing_decision": "Sol only",
        }
        with mock.patch.object(calibration, "CALIBRATION_PATH") as path:
            path.exists.return_value = True
            path.read_text.return_value = json.dumps(payload)
            result = calibration.build_direct_writer_calibration_status()
        self.assertTrue(result["valid"])
