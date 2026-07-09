import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NRL = REPO_ROOT / "system/runtime/nrl.py"


class HermesGateV014Tests(unittest.TestCase):
    def test_readiness_stops_before_hermes_and_reports_all_seed_families(self):
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
        self.assertEqual(data["status"], "blocked_on_final_asset_owner_gate")
        self.assertTrue(data["checks"]["research_review_promoted"])
        self.assertTrue(data["checks"]["all_creation_families_seeded"])
        self.assertFalse(data["checks"]["content_generation_authorized"])
        self.assertFalse(data["hermes"]["allowed"])
        self.assertEqual(len(data["creation_families"]), 9)


if __name__ == "__main__":
    unittest.main()
