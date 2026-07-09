import json
import subprocess
import sys
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
NRL = RUNTIME_DIR / "nrl.py"
sys.path.insert(0, str(RUNTIME_DIR))

FAMILIES = (
    "characters",
    "npcs",
    "factions",
    "artifacts",
    "techniques",
    "naming",
    "emotional_bonds",
    "foreshadowing",
    "state_ledger",
)


class CorpusPipelineCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_pipeline_status_reports_one_next_family_without_raw_corpus(self):
        result = self.run_cli("pipeline-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.3")
        self.assertEqual(data["mode"], "SYSTEM_HARDENING")
        self.assertEqual(data["content_progression"], "FROZEN_AT_OWNER_GATE")
        self.assertEqual(data["next_family"]["family"], "naming")
        self.assertEqual(
            len([family for family in data["families"] if family["is_next"]]),
            1,
        )
        self.assertGreaterEqual(len(data["stages"]), 7)
        self.assertIn("prose_generation", {stage["stage_id"] for stage in data["stages"]})
        self.assertIn("write novel prose", data["forbidden_actions"])
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

    def test_pipeline_plan_next_matches_status(self):
        status = json.loads(self.run_cli("pipeline-status").stdout)
        result = self.run_cli("pipeline-plan", "--next")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["target_family"]["family"], status["next_family"]["family"])
        self.assertEqual(plan["pipeline_id"], "corpus-to-creation-naming")
        self.assertFalse(plan["content_generation_allowed"])

    def test_pipeline_plan_rejects_unknown_family(self):
        result = self.run_cli("pipeline-plan", "--family", "unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported creation asset family", result.stderr)

    def test_system_check_includes_corpus_pipeline(self):
        result = self.run_cli("system-check")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn(
            "corpus_pipeline",
            {check["check_id"] for check in data["checks"]},
        )


class CorpusPipelineContractTests(unittest.TestCase):
    def setUp(self):
        from nrl import load_adapters, load_state
        from nrl_corpus_pipeline import build_pipeline_plan, build_pipeline_status

        self.state = load_state()
        self.adapters = load_adapters()
        self.build_status = build_pipeline_status
        self.build_plan = build_pipeline_plan

    def test_status_is_deterministic_and_orders_next_family_by_readiness(self):
        first = self.build_status(self.state, self.adapters)
        second = self.build_status(self.state, self.adapters)
        self.assertEqual(first, second)
        self.assertEqual(first["next_family"]["family"], "naming")
        ordered = [family["family"] for family in first["families"][:2]]
        self.assertEqual(ordered, ["naming", "npcs"])

    def test_every_family_plan_has_schema_evidence_and_validation_gates(self):
        required_gates = {
            "schema_validation",
            "source_evidence",
            "reference_integrity",
            "naming_collision",
            "lifecycle_transition",
            "owner_gate",
        }
        for family in FAMILIES:
            with self.subTest(family=family):
                plan = self.build_plan(self.state, self.adapters, family=family)
                self.assertEqual(plan["version"], "0.3")
                self.assertEqual(plan["target_family"]["family"], family)
                self.assertEqual(plan["schema_contract"]["draft"], "http://json-schema.org/draft-07/schema#")
                self.assertTrue((REPO_ROOT / plan["schema_contract"]["path"]).exists())
                self.assertGreater(len(plan["research_evidence"]), 0)
                self.assertTrue(
                    all(
                        "novel_training_set/" not in item["source_path"]
                        for item in plan["research_evidence"]
                    )
                )
                self.assertTrue(required_gates <= {gate["gate_id"] for gate in plan["validation_gates"]})
                self.assertEqual(plan["agent_review_policy"]["hermes"], "paused_not_removed")
                self.assertEqual(plan["agent_review_policy"]["antigravity"], "manual_handoff")
                self.assertTrue(plan["owner_gate"]["required"])
                self.assertFalse(plan["content_generation_allowed"])


class CorpusPipelineStudioTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_studio_data_contains_corpus_pipeline_section(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("corpus_pipeline", data)
        self.assertEqual(data["corpus_pipeline"]["next_family"]["family"], "naming")

    def test_studio_build_contains_pipeline_view_labels(self):
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (REPO_ROOT / "system/runtime/studio/index.html").read_text(encoding="utf-8")
        self.assertIn("生成管线", html)
        self.assertIn("Corpus-to-Creation Pipeline", html)
        self.assertNotIn("/api/actions/execute-hermes", html)


class CorpusPipelineServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from nrl_studio_server import create_studio_server

        cls.server = create_studio_server("127.0.0.1", 0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request_json(self, path):
        request = urllib.request.Request(self.base_url + path, method="GET")
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_pipeline_get_routes_return_status_and_plans(self):
        for path, expected_key in (
            ("/api/pipeline-status", "next_family"),
            ("/api/pipeline-plan?next=true", "target_family"),
            ("/api/pipeline-plan?family=characters", "target_family"),
        ):
            status, data = self.request_json(path)
            self.assertEqual(status, 200)
            self.assertIn(expected_key, data)

    def test_pipeline_plan_route_rejects_invalid_family(self):
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.request_json("/api/pipeline-plan?family=unknown")
        self.assertEqual(raised.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
