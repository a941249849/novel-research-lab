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

    def test_advance_applies_owner_gate_acceptance_to_phase2e_entry(self):
        prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            "# Antigravity Review\n\n"
            "Verdict: pass_with_warnings\n\n"
            "Required fixes before prose: vary pacing loops; sensory evidence; visible backlash.\n",
            encoding="utf-8",
        )
        ingested = self.run_cli(
            "ingest",
            "--agent",
            "antigravity",
            "--file",
            "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md",
        )
        self.assertEqual(ingested.returncode, 0, ingested.stderr)
        decision = self.run_cli(
            "owner-gate",
            "record",
            "--decision-id",
            "owner_gate_phase2d_antigravity_review_accept_with_warnings_001",
            "--decision-type",
            "accept_review",
            "--authorized-scope",
            "prepare_phase2e_entry",
            "--authorized-scope",
            "incorporate_antigravity_required_fixes",
            "--forbidden-scope",
            "write_novel_prose",
            "--forbidden-scope",
            "write_first_chapter",
            "--expires-after-mission",
            "phase2e_entry_preparation",
            "--owner-note",
            "批准 Phase 2E，接受 Antigravity 的 ACCEPT_WITH_WARNINGS 条件",
        )
        self.assertEqual(decision.returncode, 0, decision.stderr)
        result = self.run_cli("advance")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["action"], "phase2e_entry_prepared")
        self.assertEqual(data["status"], "ready_for_phase2e_planning")
        state = json.loads((self.root / "system/mission_controller/current_phase_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["current_phase"], "Phase 2E")
        self.assertEqual(state["owner_gate_required"], False)
        self.assertEqual(state["next_recommended_mission"], "Phase 2E Chapter Plan Entry Preparation")
        manifest = (self.root / "phase2E/00_entry/phase2E_entry_manifest.md").read_text(encoding="utf-8")
        self.assertIn("ACCEPT_WITH_WARNINGS", manifest)
        self.assertIn("vary pacing loops", manifest)
        self.assertIn("Do not write novel prose", manifest)
        package = self.run_cli("advance")
        self.assertEqual(package.returncode, 0, package.stderr)
        package_data = json.loads(package.stdout)
        self.assertEqual(package_data["action"], "phase2e_planning_package_prepared")
        self.assertEqual(package_data["status"], "phase2e_planning_package_ready")
        package_path = self.root / "phase2E/01_planning_package/phase2E_chapter_plan_control_pack.md"
        package_text = package_path.read_text(encoding="utf-8")
        self.assertIn("Phase 2E Chapter Plan Control Pack", package_text)
        self.assertIn("Vary pacing loops", package_text)
        self.assertIn("Do not write novel prose", package_text)
        self.assertNotIn("Chapter 1 prose", package_text)
        planning = self.run_cli("advance")
        self.assertEqual(planning.returncode, 0, planning.stderr)
        planning_data = json.loads(planning.stdout)
        self.assertEqual(planning_data["action"], "phase2e_controlled_planning_output_prepared")
        self.assertEqual(planning_data["status"], "phase2e_controlled_planning_output_ready")
        output_path = self.root / "system/runtime/phase2e_controlled_chapter_planning_codex_output.md"
        output_text = output_path.read_text(encoding="utf-8")
        self.assertIn("Phase 2E Controlled Chapter Planning Output", output_text)
        self.assertIn("Pacing Variation Map", output_text)
        self.assertIn("Sensory Evidence Translation Rules", output_text)
        self.assertIn("Visible Backlash Escalation", output_text)
        self.assertIn("No novel prose", output_text)
        self.assertNotIn("Chapter 1", output_text)
        self.assertNotIn("第一章", output_text)
        validation = self.run_cli("advance")
        self.assertEqual(validation.returncode, 0, validation.stderr)
        validation_data = json.loads(validation.stdout)
        self.assertEqual(validation_data["action"], "phase2e_controlled_planning_validated")
        self.assertEqual(validation_data["status"], "ready_for_antigravity_controlled_planning_review")
        validation_path = self.root / "system/runtime/phase2e_controlled_planning_validation_codex_output.md"
        validation_text = validation_path.read_text(encoding="utf-8")
        self.assertIn("Phase 2E Controlled Planning Validation", validation_text)
        self.assertIn("validation_status: PASS", validation_text)
        self.assertIn("No Hermes call was made", validation_text)
        self.assertIn("No novel prose detected", validation_text)
        self.assertNotIn("FAIL", validation_text)
        handoff = self.run_cli("advance")
        self.assertEqual(handoff.returncode, 0, handoff.stderr)
        handoff_data = json.loads(handoff.stdout)
        self.assertEqual(handoff_data["action"], "prepared_handoff")
        self.assertEqual(handoff_data["mission_id"], "phase2e_antigravity_controlled_planning_review")
        self.assertEqual(
            handoff_data["handoff_packet_path"],
            "handoff/antigravity/current_packet.md",
        )
        packet_text = (self.root / "handoff/antigravity/current_packet.md").read_text(encoding="utf-8")
        self.assertIn("Review the current mission artifacts", packet_text)
        self.assertIn("Phase 2E Antigravity Controlled Planning Review", packet_text)
        self.assertNotIn("Review the Phase 2D outline tree", packet_text)

    def test_advance_does_not_reuse_stale_owner_gate_decision_for_later_gate(self):
        prepared = self.run_cli("prepare-handoff", "--agent", "antigravity")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        output = self.root / "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            "# Antigravity Review\n\nVerdict: pass_with_warnings\n\nRequired fixes before prose.\n",
            encoding="utf-8",
        )
        ingested = self.run_cli("ingest", "--agent", "antigravity", "--file", "handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md")
        self.assertEqual(ingested.returncode, 0, ingested.stderr)
        decision = self.run_cli(
            "owner-gate",
            "record",
            "--decision-id",
            "owner_gate_phase2d_antigravity_review_accept_with_warnings_001",
            "--decision-type",
            "accept_review",
            "--authorized-scope",
            "prepare_phase2e_entry",
            "--authorized-scope",
            "incorporate_antigravity_required_fixes",
            "--forbidden-scope",
            "write_novel_prose",
            "--forbidden-scope",
            "write_first_chapter",
            "--expires-after-mission",
            "phase2e_entry_preparation",
            "--owner-note",
            "批准 Phase 2E",
        )
        self.assertEqual(decision.returncode, 0, decision.stderr)
        for _ in range(5):
            advanced = self.run_cli("advance")
            self.assertEqual(advanced.returncode, 0, advanced.stderr)
        phase2e_output = self.root / "handoff/antigravity/outputs/phase2e_antigravity_controlled_planning_review.md"
        phase2e_output.parent.mkdir(parents=True, exist_ok=True)
        phase2e_output.write_text("# Phase 2E Review\n\nVerdict: pass\n", encoding="utf-8")
        phase2e_ingest = self.run_cli("advance")
        self.assertEqual(phase2e_ingest.returncode, 0, phase2e_ingest.stderr)
        phase2e_ingest_data = json.loads(phase2e_ingest.stdout)
        self.assertEqual(phase2e_ingest_data["action"], "ingested_external_output")
        blocked = self.run_cli("advance")
        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        blocked_data = json.loads(blocked.stdout)
        self.assertEqual(blocked_data["action"], "owner_gate_required")
        self.assertEqual(blocked_data["status"], "manual_owner_decision_required")
        state = json.loads((self.root / "system/mission_controller/current_phase_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["phase_status"], "review_received_pending_owner_gate")
        self.assertEqual(state["owner_gate_status"], "REQUIRED_PENDING_ACKNOWLEDGEMENT")

    def test_system_status_reports_content_freeze_when_owner_gate_pending(self):
        state_path = self.root / "system/mission_controller/current_phase_state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["phase_status"] = "review_received_pending_owner_gate"
        state["owner_gate_required"] = True
        state["owner_gate_status"] = "REQUIRED_PENDING_ACKNOWLEDGEMENT"
        state["review_status"] = "REVIEW_RECEIVED_PENDING_OWNER_GATE"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = self.run_cli("system-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["operating_mode"], "SYSTEM_HARDENING")
        self.assertEqual(data["content_progression"], "FROZEN_AT_OWNER_GATE")
        self.assertIn("do not advance story phase", data["hard_rules"])
        self.assertEqual(data["hermes_role"], "later_writer_or_literary_enrichment")

    def test_studio_data_returns_required_dashboard_sections(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(
            {
                "system_identity",
                "current_project",
                "agent_panel",
                "artifact_map",
                "creation_coverage_matrix",
                "creation_asset_registry",
                "runtime_status",
                "next_safe_action",
                "owner_gate",
            }.issubset(data),
        )
        self.assertEqual(data["system_identity"]["name"], "Novel Research Lab")
        self.assertIn("Corpus-to-Creation", data["system_identity"]["positioning"])

    def test_studio_data_marks_long_form_assets_honestly(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        matrix = {row["asset"]: row["status"] for row in data["creation_coverage_matrix"]["items"]}
        self.assertEqual(matrix["Characters"], "partial")
        self.assertEqual(matrix["NPCs"], "missing")
        self.assertEqual(matrix["Factions"], "partial")
        self.assertEqual(matrix["Artifacts"], "seed")
        self.assertEqual(matrix["Techniques"], "seed")
        self.assertEqual(matrix["Naming"], "missing")
        self.assertEqual(matrix["Emotional Bonds"], "partial")
        self.assertEqual(matrix["Foreshadowing"], "partial")
        self.assertEqual(matrix["State Ledger"], "seed")
        self.assertNotIn("complete", set(matrix.values()))

    def test_creation_assets_returns_all_asset_families_without_complete_status(self):
        result = self.run_cli("creation-assets")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["registry_name"], "Creation Asset Registry")
        self.assertEqual(data["version"], "0.1")
        families = {item["asset_id"]: item for item in data["asset_families"]}
        self.assertEqual(
            set(families),
            {
                "characters",
                "npcs",
                "factions",
                "artifacts",
                "techniques",
                "naming",
                "emotional_bonds",
                "foreshadowing",
                "state_ledger",
            },
        )
        self.assertNotIn("complete", {item["status"] for item in families.values()})
        self.assertEqual(families["techniques"]["status"], "seed")
        self.assertEqual(families["naming"]["status"], "missing")

    def test_creation_assets_summary_matches_status_counts(self):
        result = self.run_cli("creation-assets")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        status_counts = {}
        for item in data["asset_families"]:
            status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1
        self.assertEqual(data["coverage_summary"]["total"], 9)
        self.assertEqual(data["coverage_summary"]["by_status"], status_counts)
        self.assertIn("No family is complete in v0.1", data["guardrails"])

    def test_studio_data_includes_creation_asset_registry_drilldown(self):
        result = self.run_cli("studio-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        registry = data["creation_asset_registry"]
        self.assertEqual(registry["registry_name"], "Creation Asset Registry")
        self.assertEqual(registry["coverage_summary"]["total"], 9)
        labels = {item["label"] for item in registry["asset_families"]}
        self.assertIn("Characters", labels)
        self.assertIn("NPCs", labels)
        self.assertIn("Techniques", labels)
        self.assertIn("Naming", labels)

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

    def test_owner_gate_records_final_asset_generation_authorization(self):
        record = self.run_cli(
            "owner-gate",
            "record",
            "--decision-id",
            "owner_gate_final_assets_001",
            "--decision-type",
            "authorize_final_asset_generation",
            "--authorized-scope",
            "generate_final_creation_assets",
            "--forbidden-scope",
            "generate_novel_prose",
            "--expires-after-mission",
            "phase2f_final_asset_generation",
            "--owner-note",
            "authorize final assets only",
        )
        self.assertEqual(record.returncode, 0, record.stderr)
        data = json.loads(record.stdout)
        self.assertEqual(data["decision_type"], "authorize_final_asset_generation")

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
        self.assertIn("Novel Research Lab", html)
        self.assertIn("Corpus-to-Creation", html)
        self.assertIn("Phase 2D", html)
        self.assertIn("Phase 2D Antigravity Outline Tree Review", html)
        self.assertIn("Creation Coverage Matrix", html)
        self.assertIn("Creation Asset Registry", html)
        self.assertIn("Owner Gate", html)
        self.assertIn("Characters", html)
        self.assertIn("NPCs", html)
        self.assertIn("Techniques", html)
        self.assertIn("Naming", html)
        self.assertIn("No family is complete in v0.1", html)
        self.assertIn("Readiness Score", html)
        self.assertIn("Known Support", html)
        self.assertIn("Missing Capabilities", html)
        self.assertIn("write novel prose", html)
        self.assertIn("read-only", html)

    def test_studio_build_does_not_write_fixture_data_to_workspace_public_snapshot(self):
        public_snapshot = REPO_ROOT / "apps/studio/public/nrl-studio-data.json"
        before = public_snapshot.read_text(encoding="utf-8")

        result = self.run_cli("studio-build")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(public_snapshot.read_text(encoding="utf-8"), before)

    def test_studio_build_includes_doctor_command(self):
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / "system/runtime/studio/index.html").read_text(encoding="utf-8")
        self.assertIn("Runtime Health", html)
        self.assertIn("python3 system/runtime/nrl.py doctor", html)
        self.assertIn("python3 system/runtime/nrl.py system-status", html)
        self.assertIn("python3 system/runtime/nrl.py studio-data", html)
        self.assertIn("python3 system/runtime/nrl.py system-check", html)
        self.assertNotIn("python3 system/runtime/nrl.py advance", html)

    def test_studio_build_shows_system_hardening_mode(self):
        state_path = self.root / "system/mission_controller/current_phase_state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["owner_gate_required"] = True
        state["owner_gate_status"] = "REQUIRED_PENDING_ACKNOWLEDGEMENT"
        state["phase_status"] = "review_received_pending_owner_gate"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = self.run_cli("studio-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.root / "system/runtime/studio/index.html").read_text(encoding="utf-8")
        self.assertIn("Current Project", html)
        self.assertIn("SYSTEM_HARDENING", html)
        self.assertIn("FROZEN_AT_OWNER_GATE", html)
        self.assertIn("Hermes: paused_not_removed", html)

    def test_readme_documents_sys3_commands(self):
        readme = (REPO_ROOT / "system/runtime/README.md").read_text(encoding="utf-8")
        self.assertIn("compile-context", readme)
        self.assertIn("owner-gate", readme)
        self.assertIn("studio-build", readme)
        self.assertIn("studio-data", readme)
        self.assertIn("creation-assets", readme)
        self.assertIn("open system/runtime/studio/index.html", readme)
        self.assertIn("system-status", readme)
        self.assertIn("SYSTEM_HARDENING", readme)
        self.assertIn("Hermes is paused, not removed", readme)
        self.assertIn("client_handoff", readme)


if __name__ == "__main__":
    unittest.main()
