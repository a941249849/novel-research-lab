import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NRL = REPO_ROOT / "system/runtime/nrl.py"


class AntigravityBridgeCliTests(unittest.TestCase):
    def run_cli(self, *args):
        env = os.environ.copy()
        env["NRL_ROOT"] = str(self.root)
        env["NRL_AGY_BIN"] = str(self.fake_agy)
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(
            REPO_ROOT / "system/mission_controller",
            self.root / "system/mission_controller",
        )
        (self.root / "system/runtime").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            REPO_ROOT / "system/runtime/agent_adapters.json",
            self.root / "system/runtime/agent_adapters.json",
        )
        self.fake_agy = self.root / "bin/fake-agy"
        self.fake_agy.parent.mkdir(parents=True, exist_ok=True)
        self.fake_agy.write_text(
            """#!/bin/sh
if [ "$1" = "--version" ]; then
  echo "fake-agy 1.0"
  exit 0
fi
prompt=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    -p|--print|--prompt)
      shift
      prompt="$1"
      ;;
  esac
  shift
done
printf 'FAKE_ANTIGRAVITY_RESPONSE:%s\\n' "$prompt"
""",
            encoding="utf-8",
        )
        self.fake_agy.chmod(self.fake_agy.stat().st_mode | stat.S_IXUSR)

    def tearDown(self):
        self.tmp.cleanup()

    def test_bridge_status_reports_agy_binary(self):
        result = self.run_cli("antigravity-bridge-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["available"])
        self.assertEqual(data["mode"], "cli")
        self.assertEqual(data["binary_path"], str(self.fake_agy))
        self.assertIn("fake-agy 1.0", data["version_output"])

    def test_system_status_exposes_bridge_without_changing_adapter_boundary(self):
        result = self.run_cli("system-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["antigravity_bridge"]["available"])
        self.assertEqual(data["antigravity_bridge"]["mode"], "cli")
        self.assertEqual(data["adapter_modes"]["antigravity"]["mode"], "cli_bridge")
        self.assertTrue(data["adapter_modes"]["antigravity"]["can_execute"])
        self.assertEqual(data["antigravity_execution"]["effective_state"], "ready")
        self.assertTrue(data["antigravity_execution"]["can_dispatch_registered_reviews"])

    def test_execution_status_blocks_when_agy_is_unavailable(self):
        env = os.environ.copy()
        env["NRL_ROOT"] = str(self.root)
        env["NRL_AGY_BIN"] = str(self.root / "bin/missing-agy")
        result = subprocess.run(
            [sys.executable, str(NRL), "system-status"],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["antigravity_execution"]["effective_state"], "blocked_bridge_unavailable")
        self.assertFalse(data["antigravity_execution"]["can_dispatch_registered_reviews"])

    def test_bridge_ask_runs_agy_and_writes_response(self):
        request_path = self.root / ".agent-handoff/antigravity/requests/ping.md"
        response_path = self.root / ".agent-handoff/antigravity/responses/ping.md"
        request_path.parent.mkdir(parents=True, exist_ok=True)
        request_path.write_text("Reply with bridge ok.", encoding="utf-8")

        result = self.run_cli(
            "antigravity-bridge-ask",
            "--request-file",
            str(request_path.relative_to(self.root)),
            "--output-file",
            str(response_path.relative_to(self.root)),
            "--print-timeout",
            "10s",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["request_file"], str(request_path.relative_to(self.root)))
        self.assertEqual(data["output_file"], str(response_path.relative_to(self.root)))
        self.assertTrue(response_path.exists())
        self.assertIn("FAKE_ANTIGRAVITY_RESPONSE:Reply with bridge ok.", response_path.read_text(encoding="utf-8"))

    def test_bridge_ask_rejects_missing_request_file(self):
        result = self.run_cli(
            "antigravity-bridge-ask",
            "--request-file",
            ".agent-handoff/antigravity/requests/missing.md",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("request file does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
