import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests/fixtures/sys3_runtime"
NRL = REPO_ROOT / "system/runtime/nrl.py"


class RuntimeFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "nrl"
        shutil.copytree(FIXTURE_ROOT, self.root)

    def tearDown(self):
        self.tmp.cleanup()

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

    def test_status_reads_fixture_root(self):
        result = self.run_cli("status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["current_phase"], "Phase 2D")
        self.assertEqual(data["next_recommended_mission"], "Phase 2D Antigravity Outline Tree Review")

    def test_missions_lists_registry(self):
        result = self.run_cli("missions")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["missions"], [])

    def test_check_inputs_reports_missing_files(self):
        result = self.run_cli("check-inputs")
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        missing = {item["path"] for item in data["inputs"] if item["exists"] is False}
        self.assertIn("phase2D/01_outline_tree/phase2D_outline_tree.md", missing)

    def test_gate_status_separates_validation_review_owner(self):
        result = self.run_cli("gate-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["validation_status"], "PASS_WITH_WARNINGS")
        self.assertEqual(data["review_status"], "PENDING")
        self.assertEqual(data["owner_gate_status"], "PENDING_ANTIGRAVITY_REVIEW")

    def test_doctor_reports_runtime_health_without_mutating_state(self):
        state_path = self.root / "system/mission_controller/current_phase_state.json"
        before = state_path.read_text(encoding="utf-8")
        result = self.run_cli("doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["runtime"], "Novel Research Lab")
        self.assertEqual(data["mission"]["mission_id"], "phase2d_antigravity_outline_tree_review")
        self.assertEqual(data["git"]["is_repo"], False)
        self.assertEqual(data["adapters"]["antigravity"]["mode"], "manual_handoff")
        self.assertEqual(data["gates"]["review_status"], "PENDING")
        self.assertEqual(data["recommended_next_command"], "python3 system/runtime/nrl.py advance")
        after = state_path.read_text(encoding="utf-8")
        self.assertEqual(after, before)

    def test_prepare_handoff_records_attempt(self):
        result = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("handoff_attempt_id", data)
        self.assertEqual(data["handoff_packet_path"], "handoff/antigravity/current_packet.md")
        registry_path = self.root / "system/runtime/mission_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        self.assertEqual(len(registry), 1)
        self.assertEqual(len(registry[0]["handoff_attempts"]), 1)
        self.assertEqual(
            registry[0]["handoff_attempts"][0]["expected_output_path"],
            "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md",
        )
        packet = (self.root / "handoff/antigravity/current_packet.md").read_text(encoding="utf-8")
        self.assertIn("# Novel Research Lab Antigravity Review Packet", packet)
        self.assertIn("## Mission Contract", packet)
        self.assertIn("## Source Artifacts", packet)
        self.assertNotIn("novel_training_set/", packet)

    def test_prepare_handoff_is_idempotent_while_waiting_for_output(self):
        first = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(first.returncode, 0, first.stderr)
        second = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(second.returncode, 0, second.stderr)
        first_data = json.loads(first.stdout)
        second_data = json.loads(second.stdout)
        self.assertEqual(first_data["handoff_attempt_id"], second_data["handoff_attempt_id"])
        registry = json.loads((self.root / "system/runtime/mission_registry.json").read_text(encoding="utf-8"))
        self.assertEqual(len(registry[0]["handoff_attempts"]), 1)

    def test_advance_prepares_handoff_when_no_attempt_exists(self):
        result = self.run_cli("advance")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["action"], "prepared_handoff")
        self.assertEqual(data["status"], "awaiting_external_output")
        self.assertEqual(data["mission_id"], "phase2d_antigravity_outline_tree_review")
        self.assertEqual(data["responsible_agent"], "antigravity")
        self.assertIn("handoff_attempt_id", data)
        self.assertTrue((self.root / "handoff/antigravity/current_task.md").exists())
        self.assertTrue((self.root / "handoff/antigravity/current_packet.md").exists())

    def test_advance_waits_without_duplicate_attempt_when_output_missing(self):
        prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        result = self.run_cli("advance")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["action"], "awaiting_external_output")
        self.assertEqual(data["status"], "blocked_on_external_agent")
        registry = json.loads((self.root / "system/runtime/mission_registry.json").read_text(encoding="utf-8"))
        self.assertEqual(len(registry[0]["handoff_attempts"]), 1)

    def test_advance_ingests_expected_output_and_reaches_owner_gate(self):
        prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# Antigravity Review\n\nrecommendation: owner_gate\n", encoding="utf-8")
        result = self.run_cli("advance")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["action"], "ingested_external_output")
        self.assertEqual(data["status"], "owner_gate_required")
        gate = self.run_cli("gate-status")
        self.assertEqual(gate.returncode, 0, gate.stderr)
        gate_data = json.loads(gate.stdout)
        self.assertEqual(gate_data["owner_gate_required"], True)

    def test_advance_stops_when_owner_gate_required(self):
        prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# Antigravity Review\n\nrecommendation: owner_gate\n", encoding="utf-8")
        ingested = self.run_cli("ingest", "--agent", "antigravity", "--file", "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md")
        self.assertEqual(ingested.returncode, 0, ingested.stderr)
        result = self.run_cli("advance")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["action"], "owner_gate_required")
        self.assertEqual(data["status"], "manual_owner_decision_required")

    def test_ingest_rejects_without_matching_attempt(self):
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# Review\n", encoding="utf-8")
        result = self.run_cli("ingest", "--agent", "antigravity", "--file", str(output))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no active handoff attempt", result.stderr)

    def test_antigravity_manual_review_smoke_path_reaches_owner_gate(self):
        prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# Antigravity Review\n\nrecommendation: owner_gate\n", encoding="utf-8")
        ingested = self.run_cli(
            "ingest",
            "--agent",
            "antigravity",
            "--file",
            "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md",
        )
        self.assertEqual(ingested.returncode, 0, ingested.stderr)
        gate = self.run_cli("gate-status")
        self.assertEqual(gate.returncode, 0, gate.stderr)
        data = json.loads(gate.stdout)
        self.assertEqual(data["owner_gate_required"], True)
        self.assertEqual(data["review_status"], "REVIEW_RECEIVED_PENDING_OWNER_GATE")

    def test_owner_gate_record_and_list(self):
        record = self.run_cli(
            "owner-gate",
            "record",
            "--decision-id",
            "owner_gate_phase2d_review_acceptance_001",
            "--decision-type",
            "accept_review",
            "--authorized-scope",
            "prepare_phase2e_entry",
            "--forbidden-scope",
            "write_novel_prose",
            "--expires-after-mission",
            "phase2e_entry_preparation",
            "--owner-note",
            "accept review only",
        )
        self.assertEqual(record.returncode, 0, record.stderr)
        listed = self.run_cli("owner-gate", "list")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        data = json.loads(listed.stdout)
        self.assertEqual(data["decisions"][0]["decision_id"], "owner_gate_phase2d_review_acceptance_001")
        self.assertEqual(data["decisions"][0]["forbidden_scope"], ["write_novel_prose"])

    def test_compile_context_writes_compact_packet(self):
        result = self.run_cli("compile-context", "--agent", "antigravity")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        packet_path = self.root / data["packet_path"]
        self.assertTrue(packet_path.exists())
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        self.assertEqual(packet["target_agent"], "antigravity")
        self.assertIn("must_avoid_elements", packet)
        self.assertNotIn("novel_training_set", json.dumps(packet, ensure_ascii=False))

    def test_studio_build_creates_read_only_cockpit(self):
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        html = (self.root / data["studio_path"]).read_text(encoding="utf-8")
        self.assertIn("Phase 2D", html)
        self.assertIn("Phase 2D Antigravity Outline Tree Review", html)
        self.assertIn("write novel prose", html)
        self.assertIn("Read-only cockpit", html)

    def test_studio_build_includes_doctor_command(self):
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / "system/runtime/studio/index.html").read_text(encoding="utf-8")
        self.assertIn("Runtime Health", html)
        self.assertIn("python3 system/runtime/nrl.py doctor", html)
        self.assertIn("python3 system/runtime/nrl.py advance", html)

    def test_readme_documents_sys3_commands(self):
        readme = (REPO_ROOT / "system/runtime/README.md").read_text(encoding="utf-8")
        self.assertIn("compile-context", readme)
        self.assertIn("owner-gate", readme)
        self.assertIn("studio-build", readme)
        self.assertIn("client_handoff", readme)


if __name__ == "__main__":
    unittest.main()
