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


class AgentDispatchV013Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(
            REPO_ROOT / "system/mission_controller",
            self.root / "system/mission_controller",
        )
        shutil.copytree(
            REPO_ROOT / "system/creation_assets",
            self.root / "system/creation_assets",
        )
        (self.root / "system/runtime").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            REPO_ROOT / "system/runtime/agent_adapters.json",
            self.root / "system/runtime/agent_adapters.json",
        )
        self.calls = self.root / "agy-calls.txt"
        self.fake_agy = self.root / "bin/fake-agy"
        self.fake_agy.parent.mkdir(parents=True, exist_ok=True)
        self.fake_agy.write_text(
            """#!/bin/sh
if [ "$1" = "--version" ]; then
  echo "fake-agy 1.0"
  exit 0
fi
printf 'called\\n' >> "$FAKE_AGY_CALLS"
if [ "$FAKE_AGY_FAIL" = "1" ]; then
  echo "bridge failure" >&2
  exit 7
fi
printf 'Antigravity bounded review response.\\n'
""",
            encoding="utf-8",
        )
        self.fake_agy.chmod(self.fake_agy.stat().st_mode | stat.S_IXUSR)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, fail=False):
        env = os.environ.copy()
        env["NRL_ROOT"] = str(self.root)
        env["NRL_AGY_BIN"] = str(self.fake_agy)
        env["FAKE_AGY_CALLS"] = str(self.calls)
        if fail:
            env["FAKE_AGY_FAIL"] = "1"
        result = subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        return result

    def plan_and_pack(self):
        planned = self.run_cli("agent-job-plan", "--family", "techniques")
        self.assertEqual(planned.returncode, 0, planned.stderr)
        job = json.loads(planned.stdout)["job"]
        packed = self.run_cli("agent-pack", "--job-id", job["job_id"])
        self.assertEqual(packed.returncode, 0, packed.stderr)
        return job

    def read_queue(self):
        return json.loads(
            (self.root / "system/agent_ops/job_queue.v0.5.json").read_text(
                encoding="utf-8"
            )
        )

    def test_dispatch_transitions_registered_job_to_output_received(self):
        job = self.plan_and_pack()

        result = self.run_cli("agent-dispatch", "--job-id", job["job_id"])

        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["state"], "output_received")
        self.assertEqual(data["job_id"], job["job_id"])
        output_path = self.root / job["expected_output_path"]
        self.assertTrue(output_path.exists())
        self.assertTrue(output_path.read_text(encoding="utf-8").strip())
        self.assertTrue((self.root / data["request_file"]).exists())
        self.assertTrue((self.root / data["bridge_log_path"]).exists())
        self.assertEqual(self.read_queue()["jobs"][0]["state"], "output_received")
        self.assertEqual(self.calls.read_text(encoding="utf-8").count("called"), 1)

    def test_dispatch_rejects_missing_packet_without_mutating_job(self):
        planned = self.run_cli("agent-job-plan", "--family", "techniques")
        job = json.loads(planned.stdout)["job"]

        result = self.run_cli("agent-dispatch", "--job-id", job["job_id"])

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("packet", result.stderr)
        self.assertEqual(self.read_queue()["jobs"][0]["state"], "ready_for_antigravity")
        self.assertFalse(self.calls.exists())

    def test_dispatch_rejects_raw_corpus_packet_without_calling_agy(self):
        job = self.plan_and_pack()
        packet = self.root / job["input_packet_path"]
        packet.write_text("Do not read novel_training_set/example.txt", encoding="utf-8")

        result = self.run_cli("agent-dispatch", "--job-id", job["job_id"])

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("raw corpus", result.stderr)
        self.assertEqual(self.read_queue()["jobs"][0]["state"], "ready_for_antigravity")
        self.assertFalse(self.calls.exists())

    def test_dispatch_failure_marks_job_blocked_and_does_not_validate(self):
        job = self.plan_and_pack()

        result = self.run_cli("agent-dispatch", "--job-id", job["job_id"], fail=True)

        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["state"], "blocked")
        self.assertEqual(self.read_queue()["jobs"][0]["state"], "blocked")
        self.assertFalse(self.read_queue()["jobs"][0].get("validation_report_path"))

    def test_dispatch_rejects_second_dispatch_after_output_received(self):
        job = self.plan_and_pack()
        first = self.run_cli("agent-dispatch", "--job-id", job["job_id"])
        self.assertEqual(first.returncode, 0, first.stderr)

        second = self.run_cli("agent-dispatch", "--job-id", job["job_id"])

        self.assertNotEqual(second.returncode, 0)
        self.assertIn("state", second.stderr)
        self.assertEqual(self.calls.read_text(encoding="utf-8").count("called"), 1)


if __name__ == "__main__":
    unittest.main()
