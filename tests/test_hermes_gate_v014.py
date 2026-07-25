import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NRL = REPO_ROOT / "system/runtime/nrl.py"
sys.path.insert(0, str(REPO_ROOT / "system/runtime"))

from nrl_hermes_gate import latest_final_asset_generation_decision


class HermesGateV014Tests(unittest.TestCase):
    def test_latest_final_asset_generation_decision_requires_matching_scope(self):
        matching = {
            "decision_id": "owner_gate_final_assets_001",
            "decision_type": "authorize_final_asset_generation",
            "authorized_scope": ["generate_final_creation_assets"],
            "expires_after_mission": "phase2f_final_asset_generation",
        }
        wrong_scope = {
            "decision_id": "owner_gate_wrong_scope_001",
            "decision_type": "authorize_final_asset_generation",
            "authorized_scope": ["prepare_hermes_writing_handoff"],
            "expires_after_mission": "phase2f_final_asset_generation",
        }

        self.assertEqual(
            latest_final_asset_generation_decision([wrong_scope, matching]),
            matching,
        )

    def test_legacy_readiness_command_reports_retired_adapter(self):
        result = subprocess.run(
            [sys.executable, str(NRL), "hermes-readiness"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["ready_to_call_hermes"])
        self.assertEqual(data["status"], "retired")
        self.assertEqual(data["replacement"], "codex_three_model_team")
        self.assertEqual(
            set(data["active_models"]),
            {"gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"},
        )


if __name__ == "__main__":
    unittest.main()
