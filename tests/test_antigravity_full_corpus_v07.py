import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NRL = REPO_ROOT / "system/runtime/nrl.py"
JOB_ID = "job-v07-full-corpus-antigravity-review"


class AntigravityFullCorpusCliTests(unittest.TestCase):
    def run_cli(self, *args):
        env = os.environ.copy()
        env["NRL_ROOT"] = str(self.root)
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
        self.inbox_review = self.root / f"system/agent_ops/inbox/{JOB_ID}.md"

    def tearDown(self):
        self.tmp.cleanup()

    def test_pack_writes_owner_command_packet(self):
        result = self.run_cli("antigravity-full-corpus-pack")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["job_id"], JOB_ID)
        packet_path = self.root / data["packet_path"]
        command_path = self.root / data["command_path"]
        self.assertTrue(packet_path.exists())
        self.assertTrue(command_path.exists())

        command_text = command_path.read_text(encoding="utf-8")
        self.assertIn("中文玄幻小说全量重读", command_text)
        self.assertIn("v0.4 十层架构", command_text)
        self.assertIn("system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md", command_text)
        for family in (
            "characters",
            "npcs",
            "factions",
            "artifacts",
            "techniques",
            "naming",
            "emotional_bonds",
            "foreshadowing",
            "state_ledger",
        ):
            self.assertIn(family, command_text)
        self.assertNotIn("Hermes 已执行", command_text)

    def test_status_reports_cli_bridge_owner_boundary(self):
        self.run_cli("antigravity-full-corpus-pack")
        result = self.run_cli("antigravity-full-corpus-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["job_id"], JOB_ID)
        self.assertEqual(data["contract_version"], "0.7")
        self.assertEqual(data["antigravity_mode"], "cli_bridge_owner_gated_full_corpus_review")
        self.assertFalse(data["hermes_allowed"])
        self.assertEqual(data["state"], "ready_for_antigravity")

    def test_ingest_rejects_file_outside_inbox(self):
        self.run_cli("antigravity-full-corpus-pack")
        result = self.run_cli("antigravity-full-corpus-ingest", "--file", "README.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("system/agent_ops/inbox", result.stderr)

    def test_validate_accepts_structured_full_corpus_review(self):
        self.run_cli("antigravity-full-corpus-pack")
        self.inbox_review.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            REPO_ROOT / "tests/fixtures/agent_ops/valid_full_corpus_antigravity_review.md",
            self.inbox_review,
        )
        ingest = self.run_cli(
            "antigravity-full-corpus-ingest",
            "--file",
            str(self.inbox_review.relative_to(self.root)),
        )
        self.assertEqual(ingest.returncode, 0, ingest.stderr)
        validate = self.run_cli("antigravity-full-corpus-validate")
        self.assertEqual(validate.returncode, 0, validate.stderr)
        data = json.loads(validate.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual(data["job"]["state"], "validated")
        self.assertEqual(set(data["manifest"]["asset_family_evidence"]), {
            "characters",
            "npcs",
            "factions",
            "artifacts",
            "techniques",
            "naming",
            "emotional_bonds",
            "foreshadowing",
            "state_ledger",
        })

    def test_validate_rejects_forbidden_generation_markers(self):
        self.run_cli("antigravity-full-corpus-pack")
        self.inbox_review.parent.mkdir(parents=True, exist_ok=True)
        text = (REPO_ROOT / "tests/fixtures/agent_ops/valid_full_corpus_antigravity_review.md").read_text(
            encoding="utf-8"
        )
        self.inbox_review.write_text(text + "\n第一章\n", encoding="utf-8")
        self.assertEqual(
            self.run_cli(
                "antigravity-full-corpus-ingest",
                "--file",
                str(self.inbox_review.relative_to(self.root)),
            ).returncode,
            0,
        )
        validate = self.run_cli("antigravity-full-corpus-validate")
        self.assertNotEqual(validate.returncode, 0)
        data = json.loads(validate.stdout)
        self.assertFalse(data["valid"])
        self.assertIn("第一章", data["report"]["forbidden_hits"])


if __name__ == "__main__":
    unittest.main()
