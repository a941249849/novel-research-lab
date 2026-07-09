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


class ControlPlaneCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_hardening_status_has_allowed_states_and_one_next_action(self):
        result = self.run_cli("hardening-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["mode"], "SYSTEM_HARDENING")
        self.assertEqual(len(data["capabilities"]), 8)
        self.assertEqual(
            len([item for item in data["capabilities"] if item["is_next_safe_action"]]),
            1,
        )
        self.assertTrue(
            {item["status"] for item in data["capabilities"]}
            <= {"missing", "contract_ready", "data_ready", "runnable", "blocked"}
        )

    def test_hardening_status_counts_full_corpus_proof_as_corpus_engineering_evidence(self):
        result = self.run_cli("hardening-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        corpus = data["capabilities"][0]
        evidence_paths = {item["path"] for item in corpus["evidence"]}
        self.assertIn("system/agent_ops/inbox/full_corpus_proof_v0.8/master.md", evidence_paths)
        self.assertIn("system/agent_ops/validation/full_corpus_proof_v0.8.json", evidence_paths)
        self.assertEqual(corpus["status"], "data_ready")
        self.assertTrue(corpus["evidence_complete"])

    def test_research_assets_indexes_reviewed_phase1_assets(self):
        result = self.run_cli("research-assets", "--title", "遮天")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreaterEqual(data["summary"]["returned"], 4)
        self.assertTrue(all(item["title"] == "遮天" for item in data["items"]))
        self.assertIn("formal", {item["review_state"] for item in data["items"]})
        self.assertNotIn(
            "novel_training_set/",
            json.dumps(data, ensure_ascii=False),
        )

    def test_research_assets_filters_mechanism_category(self):
        result = self.run_cli("research-assets", "--category", "升级与境界机制")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreater(data["summary"]["returned"], 0)
        self.assertTrue(
            all("升级与境界机制" in item["categories"] for item in data["items"])
        )

    def test_research_assets_exposes_verified_full_corpus_proof_without_promotion(self):
        result = self.run_cli("research-assets", "--asset-type", "corpus_proof")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["summary"]["returned"], 1)
        proof = data["items"][0]
        self.assertEqual(proof["asset_id"], "full-corpus-proof-v08")
        self.assertEqual(proof["review_state"], "proof_verified")
        self.assertEqual(proof["provenance"], "verified_not_promoted")
        self.assertEqual(proof["verified_receipts"], 18)
        self.assertEqual(proof["required_receipts"], 18)
        self.assertFalse(proof["promotion_allowed"])
        self.assertNotIn("novel_training_set/", json.dumps(proof, ensure_ascii=False))

    def test_creation_schema_registry_exposes_nine_draft7_families(self):
        result = self.run_cli("creation-schemas")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["draft"], "http://json-schema.org/draft-07/schema#")
        self.assertEqual(data["summary"]["family_count"], 9)
        self.assertTrue(data["summary"]["all_schemas_valid"])

    def test_validate_creation_assets_accepts_current_project_store(self):
        result = self.run_cli("validate-creation-assets")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["valid"])
        self.assertGreaterEqual(data["summary"]["asset_count"], 0)
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

    def test_studio_data_adds_v02_sections_without_removing_v01_sections(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        for key in (
            "system_identity",
            "current_project",
            "owner_gate",
            "control_plane",
            "capability_roadmap",
            "research_asset_catalog",
            "creation_schema_registry",
            "safe_action_catalog",
            "full_corpus_proof",
        ):
            self.assertIn(key, data)
        self.assertNotIn(
            "python3 system/runtime/nrl.py advance",
            data["runtime_status"]["health_commands"],
        )

    def test_studio_data_surfaces_full_corpus_proof_gate(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        proof = json.loads(result.stdout)["full_corpus_proof"]
        self.assertEqual(proof["status"], "proof_gate_ready")
        self.assertEqual(proof["corpus_inventory"]["file_count"], 18)
        self.assertEqual(proof["latest_validation"]["status"], "proof_verified")
        self.assertEqual(proof["promotion_readiness"]["status"], "blocked_on_owner_gate")
        self.assertEqual(proof["promotion_readiness"]["verified_receipts"], 18)
        self.assertEqual(proof["promotion_readiness"]["required_receipts"], 18)
        self.assertFalse(proof["promotion_readiness"]["promotion_allowed"])

    def test_system_check_is_read_only_and_reports_all_contracts(self):
        state_path = REPO_ROOT / "system/mission_controller/current_phase_state.json"
        before = state_path.read_text(encoding="utf-8")
        result = self.run_cli("system-check")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["passed"])
        self.assertEqual(
            {check["check_id"] for check in data["checks"]},
            {
                "runtime_state",
                "capability_roadmap",
                "research_asset_catalog",
                "creation_schemas",
                "creation_asset_store",
                "corpus_pipeline",
                "evidence_pack_matrix",
                "architecture_reconciliation",
            },
        )
        matrix = next(check for check in data["checks"] if check["check_id"] == "evidence_pack_matrix")
        self.assertEqual(matrix["detail"]["family_count"], 9)
        self.assertEqual(matrix["detail"]["valid_family_count"], 9)
        self.assertEqual(state_path.read_text(encoding="utf-8"), before)


class CreationAssetValidationTests(unittest.TestCase):
    def setUp(self):
        from nrl_creation_schemas import validate_creation_asset_store

        self.validate = validate_creation_asset_store

    def asset(self, asset_id, family, display_name, **extra):
        return {
            "asset_id": asset_id,
            "family": family,
            "display_name": display_name,
            "lifecycle_state": "seed",
            "source_refs": ["system:test"],
            "relationships": [],
            "constraints": [],
            **extra,
        }

    def test_rejects_duplicate_asset_ids(self):
        store = {
            "version": "0.2",
            "project": "test",
            "assets": [
                self.asset("char-1", "characters", "甲"),
                self.asset("char-1", "characters", "乙"),
            ],
        }
        result = self.validate(store)
        self.assertFalse(result["valid"])
        self.assertIn("duplicate_asset_id", {error["code"] for error in result["errors"]})

    def test_rejects_unresolved_relationship_reference(self):
        asset = self.asset("char-1", "characters", "甲")
        asset["relationships"] = [
            {"target_id": "missing-1", "relation_type": "opposes"}
        ]
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("unresolved_reference", {error["code"] for error in result["errors"]})

    def test_rejects_normalized_name_collision(self):
        store = {
            "version": "0.2",
            "project": "test",
            "assets": [
                self.asset("char-1", "characters", "天 命"),
                self.asset("char-2", "characters", "天命"),
            ],
        }
        result = self.validate(store)
        self.assertFalse(result["valid"])
        self.assertIn("name_collision", {error["code"] for error in result["errors"]})

    def test_rejects_illegal_lifecycle_transition(self):
        asset = self.asset(
            "char-1",
            "characters",
            "甲",
            lifecycle_state="seed",
            previous_lifecycle_state="retired",
        )
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("invalid_lifecycle_transition", {error["code"] for error in result["errors"]})

    def test_rejects_family_payload_mismatch(self):
        asset = self.asset(
            "tech-1",
            "techniques",
            "试招",
            character={"role": "protagonist"},
        )
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("schema_validation", {error["code"] for error in result["errors"]})

    def test_rejects_invalid_family_payload_shape(self):
        asset = self.asset(
            "tech-1",
            "techniques",
            "试招",
            technique={"counter_ids": [1]},
        )
        result = self.validate({"version": "0.2", "project": "test", "assets": [asset]})
        self.assertFalse(result["valid"])
        self.assertIn("schema_validation", {error["code"] for error in result["errors"]})


class CapabilityDerivationTests(unittest.TestCase):
    def test_missing_evidence_downgrades_capability_and_blocks_dependents(self):
        from nrl_capabilities import build_hardening_status

        roadmap = {
            "version": "test",
            "capabilities": [
                {
                    "capability_id": "first",
                    "label_zh": "第一项",
                    "status": "runnable",
                    "dependencies": [],
                    "evidence": ["missing.file"],
                    "next_action": "补齐证据",
                },
                {
                    "capability_id": "second",
                    "label_zh": "第二项",
                    "status": "runnable",
                    "dependencies": ["first"],
                    "evidence": [],
                    "next_action": "等待依赖",
                },
            ],
        }
        result = build_hardening_status(
            {"owner_gate_required": True},
            {},
            roadmap=roadmap,
            evidence_root=REPO_ROOT,
        )
        self.assertEqual(result["capabilities"][0]["status"], "missing")
        self.assertEqual(result["capabilities"][1]["status"], "blocked")
        self.assertEqual(result["next_safe_action"]["capability_id"], "first")


class StudioServerTests(unittest.TestCase):
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

    def request_json(self, path, method="GET", payload=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_get_routes_return_control_plane_data(self):
        for path, expected_key in (
            ("/api/studio-data", "control_plane"),
            ("/api/research-assets", "catalog_name"),
            ("/api/creation-schemas", "registry_name"),
        ):
            status, data = self.request_json(path)
            self.assertEqual(status, 200)
            self.assertIn(expected_key, data)

    def test_allowlisted_post_actions_run_without_arbitrary_command_input(self):
        status, data = self.request_json(
            "/api/actions/system-check", method="POST", payload={}
        )
        self.assertEqual(status, 200)
        self.assertTrue(data["passed"])

        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.request_json(
                "/api/actions/system-check",
                method="POST",
                payload={"command": "rm -rf /"},
            )
        self.assertEqual(raised.exception.code, 400)

    def test_server_rejects_advance_and_unknown_actions(self):
        for path in ("/api/actions/advance", "/api/actions/not-real"):
            with self.assertRaises(urllib.error.HTTPError) as raised:
                self.request_json(path, method="POST", payload={})
            self.assertEqual(raised.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
