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


if __name__ == "__main__":
    unittest.main()
