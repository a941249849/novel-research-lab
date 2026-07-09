import json
import subprocess
import sys
import threading
import unittest
import urllib.request
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


class DnaRegistryCliTests(RuntimeCliCase):
    def test_dna_registry_builds_all_families_without_raw_corpus(self):
        result = self.run_cli("dna-registry-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.5")
        self.assertEqual(
            set(data["summary"]["by_family"]),
            {"book_dna", "narrative_dna", "mechanism_dna", "state_dna", "project_dna"},
        )
        self.assertTrue((REPO_ROOT / "system/dna_registry/dna_registry.v0.5.json").exists())
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

    def test_dna_registry_cli_loads_generated_registry(self):
        self.run_cli("dna-registry-build")
        result = self.run_cli("dna-registry")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreater(data["summary"]["total_entries"], 0)
        self.assertIn("project_dna", data["summary"]["by_family"])


class RagIndexCliTests(RuntimeCliCase):
    def test_rag_index_builds_structured_items_without_raw_prose(self):
        self.run_cli("dna-registry-build")
        result = self.run_cli("rag-index-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.5")
        self.assertGreater(data["summary"]["total_items"], 0)
        item = data["items"][0]
        self.assertIn("retrieval_text", item)
        self.assertIn("evidence_weight", item)
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

    def test_creation_context_index_builds_from_evidence_pack_matrix(self):
        result = self.run_cli("creation-context-index-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.12")
        self.assertEqual(data["source_matrix_id"], "evidence-pack-matrix-v0.11")
        self.assertEqual(data["summary"]["family_count"], 9)
        self.assertGreaterEqual(data["summary"]["total_items"], 9 * 3)
        self.assertFalse(data["content_generation_allowed"])
        self.assertFalse(data["external_agent_execution_allowed"])
        self.assertTrue((REPO_ROOT / "system/research_index/creation_context_index.v0.12.json").exists())
        item = data["items"][0]
        self.assertIn("retrieval_text", item)
        self.assertIn("target_family", item)
        self.assertIn("evidence_pack_path", item)
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))


class AgentOpsCliTests(RuntimeCliCase):
    def test_agent_job_plan_creates_techniques_job_and_packet(self):
        result = self.run_cli("agent-job-plan", "--family", "techniques")
        self.assertEqual(result.returncode, 0, result.stderr)
        job = json.loads(result.stdout)["job"]
        self.assertEqual(job["target_family"], "techniques")
        self.assertEqual(job["owner_agent"], "antigravity")
        self.assertIn(job["state"], {"ready_for_antigravity", "validated"})
        self.assertTrue((REPO_ROOT / "system/agent_ops/job_queue.v0.5.json").exists())

        packet = self.run_cli("agent-pack", "--job-id", job["job_id"])
        self.assertEqual(packet.returncode, 0, packet.stderr)
        packet_data = json.loads(packet.stdout)
        packet_text = (REPO_ROOT / packet_data["packet_path"]).read_text(encoding="utf-8")
        self.assertIn("FORBIDDEN ACTIONS", packet_text)
        self.assertIn("Do not write prose", packet_text)

    def test_agent_ingest_rejects_files_outside_inbox(self):
        job = json.loads(self.run_cli("agent-job-plan", "--family", "techniques").stdout)["job"]
        result = self.run_cli("agent-ingest", "--job-id", job["job_id"], "--file", "README.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("system/agent_ops/inbox", result.stderr)

    def test_agent_validate_accepts_sample_review_and_marks_job_validated(self):
        job = json.loads(self.run_cli("agent-job-plan", "--family", "techniques").stdout)["job"]
        inbox = REPO_ROOT / "system/agent_ops/inbox/valid_antigravity_techniques_review.md"
        inbox.parent.mkdir(parents=True, exist_ok=True)
        inbox.write_text(
            (REPO_ROOT / "tests/fixtures/agent_ops/valid_antigravity_techniques_review.md").read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )
        ingest = self.run_cli(
            "agent-ingest",
            "--job-id",
            job["job_id"],
            "--file",
            str(inbox.relative_to(REPO_ROOT)),
        )
        self.assertEqual(ingest.returncode, 0, ingest.stderr)
        validate = self.run_cli("agent-validate", "--job-id", job["job_id"])
        self.assertEqual(validate.returncode, 0, validate.stderr)
        data = json.loads(validate.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual(data["job"]["state"], "validated")

    def test_agent_job_plan_does_not_downgrade_validated_job(self):
        job = json.loads(self.run_cli("agent-job-plan", "--family", "techniques").stdout)["job"]
        inbox = REPO_ROOT / "system/agent_ops/inbox/valid_antigravity_techniques_review.md"
        inbox.parent.mkdir(parents=True, exist_ok=True)
        inbox.write_text(
            (REPO_ROOT / "tests/fixtures/agent_ops/valid_antigravity_techniques_review.md").read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )
        self.assertEqual(
            self.run_cli(
                "agent-ingest",
                "--job-id",
                job["job_id"],
                "--file",
                str(inbox.relative_to(REPO_ROOT)),
            ).returncode,
            0,
        )
        self.assertEqual(self.run_cli("agent-validate", "--job-id", job["job_id"]).returncode, 0)
        self.assertEqual(self.run_cli("agent-pack", "--job-id", job["job_id"]).returncode, 0)
        planned = json.loads(self.run_cli("agent-job-plan", "--family", "techniques").stdout)["job"]
        self.assertEqual(planned["state"], "validated")
        self.assertEqual(planned["actual_output_path"], "system/agent_ops/inbox/valid_antigravity_techniques_review.md")


class ProductionRuntimeIntegrationTests(RuntimeCliCase):
    def test_production_runtime_status_reports_real_runtime_sections(self):
        self.run_cli("dna-registry-build")
        self.run_cli("rag-index-build")
        self.run_cli("agent-job-plan", "--family", "techniques")
        result = self.run_cli("production-runtime-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.5")
        self.assertEqual(data["system_mode"], "SYSTEM_HARDENING")
        self.assertEqual(data["content_progression"], "FROZEN_AT_OWNER_GATE")
        self.assertEqual(data["antigravity"]["mode"], "manual_handoff")
        self.assertEqual(data["hermes"]["status"], "paused_not_removed")
        self.assertIn("techniques", data["agent_jobs"]["by_family"])

    def test_studio_data_contains_dna_production_runtime(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("dna_production_runtime", data)
        self.assertIn("creation_context_index", data)
        self.assertEqual(data["creation_context_index"]["version"], "0.12")


class ProductionRuntimeServerTests(unittest.TestCase):
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

    def test_production_runtime_get_routes_return_data(self):
        for path, expected_key in (
            ("/api/dna-registry", "entries"),
            ("/api/rag-index", "items"),
            ("/api/creation-context-index", "items"),
            ("/api/agent-jobs", "jobs"),
            ("/api/production-runtime-status", "agent_jobs"),
        ):
            status, data = self.request_json(path)
            self.assertEqual(status, 200)
            self.assertIn(expected_key, data)


if __name__ == "__main__":
    unittest.main()
