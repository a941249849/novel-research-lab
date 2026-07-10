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
        self.assertEqual(data["next_family"]["family"], "npcs")
        self.assertEqual(
            len([family for family in data["families"] if family["is_next"]]),
            1,
        )
        self.assertGreaterEqual(len(data["stages"]), 7)
        self.assertIn("prose_generation", {stage["stage_id"] for stage in data["stages"]})
        self.assertIn("write novel prose", data["forbidden_actions"])
        self.assertTrue(data["creation_contract_seed_matrix_ready"])
        self.assertIn("hermes-readiness", data["next_safe_action"])
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

    def test_pipeline_plan_next_matches_status(self):
        status = json.loads(self.run_cli("pipeline-status").stdout)
        result = self.run_cli("pipeline-plan", "--next")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["target_family"]["family"], status["next_family"]["family"])
        self.assertEqual(plan["pipeline_id"], "corpus-to-creation-npcs")
        self.assertFalse(plan["content_generation_allowed"])

    def test_evidence_pack_next_writes_guarded_manifest_without_raw_corpus(self):
        output_path = REPO_ROOT / "system/research_assets/evidence_packs/npcs.v0.10.json"
        if output_path.exists():
            output_path.unlink()
        result = self.run_cli("evidence-pack", "--next", "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        pack = json.loads(result.stdout)
        self.assertTrue(output_path.exists())
        written = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(pack, written)
        self.assertEqual(pack["evidence_pack_id"], "evidence-pack-npcs-v0.10")
        self.assertEqual(pack["family"], "npcs")
        self.assertEqual(
            pack["schema_contract"]["path"],
            "system/creation_assets/schemas/npcs.schema.json",
        )
        self.assertGreaterEqual(pack["evidence_summary"]["item_count"], 3)
        self.assertFalse(pack["content_generation_allowed"])
        self.assertFalse(pack["external_agent_execution_allowed"])
        self.assertIn("execute_hermes", pack["blocked_actions"])
        self.assertIn("execute_antigravity", pack["blocked_actions"])
        serialized = json.dumps(pack, ensure_ascii=False)
        self.assertNotIn("novel_training_set/", serialized)
        self.assertEqual(
            pack["promotion_dependencies"]["full_corpus_proof"]["status"],
            "promotable_research_asset",
        )

    def test_evidence_pack_validate_enforces_active_gates(self):
        write_result = self.run_cli("evidence-pack", "--next", "--write")
        self.assertEqual(write_result.returncode, 0, write_result.stderr)
        result = self.run_cli("evidence-pack-validate", "--next")
        self.assertEqual(result.returncode, 0, result.stderr)
        validation = json.loads(result.stdout)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["family"], "npcs")
        required_gates = {
            "schema_validation",
            "source_evidence",
            "raw_corpus_boundary",
            "creation_asset_store",
            "owner_gate",
            "agent_execution_boundary",
        }
        self.assertTrue(required_gates <= {check["gate_id"] for check in validation["checks"]})
        self.assertTrue(all(check["passed"] for check in validation["checks"]))
        self.assertNotIn("novel_training_set/", json.dumps(validation, ensure_ascii=False))

    def test_evidence_pack_validate_rejects_raw_corpus_path(self):
        pack = json.loads(self.run_cli("evidence-pack", "--next").stdout)
        pack["research_evidence"][0]["source_path"] = "novel_training_set/example.txt"
        fixture = REPO_ROOT / "system/research_assets/evidence_packs/_invalid_raw_path.test.json"
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            result = self.run_cli("evidence-pack-validate", "--file", str(fixture))
            self.assertNotEqual(result.returncode, 0)
            validation = json.loads(result.stdout)
            self.assertFalse(validation["valid"])
            self.assertIn("raw_corpus_boundary", {error["gate_id"] for error in validation["errors"]})
        finally:
            fixture.unlink(missing_ok=True)

    def test_evidence_pack_matrix_writes_all_families_and_manifest(self):
        output_path = REPO_ROOT / "system/research_assets/evidence_packs/manifest.v0.11.json"
        if output_path.exists():
            output_path.unlink()
        result = self.run_cli("evidence-pack-matrix", "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        matrix = json.loads(result.stdout)
        self.assertTrue(output_path.exists())
        self.assertEqual(matrix, json.loads(output_path.read_text(encoding="utf-8")))
        self.assertEqual(matrix["version"], "0.11")
        self.assertEqual(matrix["matrix_id"], "evidence-pack-matrix-v0.11")
        self.assertEqual(matrix["family_count"], len(FAMILIES))
        self.assertEqual(set(matrix["families"].keys()), set(FAMILIES))
        self.assertFalse(matrix["content_generation_allowed"])
        self.assertFalse(matrix["external_agent_execution_allowed"])
        for family in FAMILIES:
            with self.subTest(family=family):
                item = matrix["families"][family]
                pack_path = REPO_ROOT / item["output_path"]
                self.assertTrue(pack_path.exists())
                self.assertEqual(item["family"], family)
                self.assertGreaterEqual(item["evidence_item_count"], 3)
                self.assertEqual(item["validation_status"], "valid")
        self.assertNotIn("novel_training_set/", json.dumps(matrix, ensure_ascii=False))

    def test_evidence_pack_validate_all_reports_all_family_packs_valid(self):
        result = self.run_cli("evidence-pack-validate", "--all")
        self.assertEqual(result.returncode, 0, result.stderr)
        validation = json.loads(result.stdout)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["mode"], "all")
        self.assertEqual(validation["family_count"], len(FAMILIES))
        self.assertEqual(validation["valid_family_count"], len(FAMILIES))
        self.assertEqual(set(validation["families"].keys()), set(FAMILIES))
        self.assertNotIn("novel_training_set/", json.dumps(validation, ensure_ascii=False))

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
        evidence_matrix = next(
            check for check in data["checks"] if check["check_id"] == "evidence_pack_matrix"
        )
        self.assertTrue(evidence_matrix["passed"])
        self.assertEqual(evidence_matrix["detail"]["family_count"], len(FAMILIES))
        self.assertEqual(evidence_matrix["detail"]["valid_family_count"], len(FAMILIES))


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
        self.assertEqual(first["next_family"]["family"], "npcs")
        ordered = [family["family"] for family in first["families"][:2]]
        self.assertEqual(ordered, ["npcs", "artifacts"])

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
                self.assertEqual(plan["agent_review_policy"]["hermes"], "ready")
                self.assertEqual(plan["agent_review_policy"]["antigravity"], "ready")
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
        self.assertEqual(data["corpus_pipeline"]["next_family"]["family"], "npcs")
        self.assertIn("evidence_pack_matrix", data["corpus_pipeline"])
        self.assertEqual(
            data["corpus_pipeline"]["evidence_pack_matrix"]["family_count"],
            len(FAMILIES),
        )

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
            ("/api/evidence-pack-matrix", "families"),
        ):
            status, data = self.request_json(path)
            self.assertEqual(status, 200)
            self.assertIn(expected_key, data)

    def test_evidence_pack_route_returns_next_pack(self):
        status, data = self.request_json("/api/evidence-pack?next=true")
        self.assertEqual(status, 200)
        self.assertEqual(data["family"], "npcs")
        self.assertEqual(data["evidence_pack_id"], "evidence-pack-npcs-v0.10")
        self.assertFalse(data["content_generation_allowed"])

    def test_pipeline_plan_route_rejects_invalid_family(self):
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.request_json("/api/pipeline-plan?family=unknown")
        self.assertEqual(raised.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
