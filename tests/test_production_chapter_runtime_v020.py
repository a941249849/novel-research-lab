import sys
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))
REPO_ROOT = Path(__file__).resolve().parents[1]

from nrl_production_runtime import (
    STAGES,
    analyze_prose_metrics,
    build_rolling_state_snapshot,
    build_observer_prompt_payload,
    compile_chapter_context_payload,
    requires_external_chapter_audit,
    validate_acceptance,
    validate_chapter_sequence,
    validate_settlement_payload,
    validate_stage_transition,
)
import nrl_production_runtime as runtime


class ProductionChapterRuntimeV020Tests(unittest.TestCase):
    def test_length_recovery_inserts_before_closing_beat(self):
        draft = "开头\n\n中段\n\n收束一\n\n收束二"
        result = runtime._insert_length_recovery(draft, "补足场景")
        self.assertEqual(result, "开头\n\n中段\n\n补足场景\n\n收束一\n\n收束二")


    def test_audit_output_parser_accepts_fenced_json_from_stderr(self):
        record = {"stage": "draft_generated", "artifacts": {"context": "context.json", "rule_stack": "rules.json", "trace": "trace.json", "draft": "draft.md"}}
        audit = {"chapter_id": "chapter-0001", "artifact_kind": "draft", "artifact_sha256": "a" * 64, "context_sha256": "b" * 64, "verdict": "ACCEPT", "dimensions": {key: [] for key in ("canon", "character", "state", "causality", "pacing", "life_force", "anti_ai_taste", "originality")}, "issues": []}
        packet = REPO_ROOT / "system/production_runtime/chapters/chapter-0001/test-audit-packet.md"
        packet.write_text("packet", encoding="utf-8")
        with mock.patch.object(runtime, "build_chapter_audit_packet", return_value={"template": audit, "packet_path": str(packet.relative_to(REPO_ROOT))}), mock.patch.object(runtime, "find_agy_binary", return_value="agy"), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "validate_stage_transition", return_value={"valid": True, "errors": []}), mock.patch.object(runtime, "_save_registry"), mock.patch.object(runtime, "_write_json"), mock.patch("nrl_production_runtime.subprocess.run", return_value=mock.Mock(returncode=0, stdout="", stderr="```json\n" + __import__("json").dumps(audit) + "\n```")):
            result = runtime.dispatch_chapter_audit("chapter-0001")
        packet.unlink()
        self.assertTrue(result["valid"])

    def test_failed_external_audit_persists_a_recoverable_attempt_record(self):
        import nrl_production_runtime as runtime

        record = {"stage": "draft_generated", "artifacts": {}}
        packet = REPO_ROOT / "system/production_runtime/chapters/chapter-0001/test-failed-audit-packet.md"
        packet.write_text("packet", encoding="utf-8")
        with mock.patch.object(runtime, "build_chapter_audit_packet", return_value={"template": {}, "packet_path": str(packet.relative_to(REPO_ROOT))}), mock.patch.object(runtime, "find_agy_binary", return_value="agy"), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "_save_registry"), mock.patch.object(runtime, "_write_json") as write_json, mock.patch("nrl_production_runtime.subprocess.run", return_value=mock.Mock(returncode=1, stdout="", stderr="provider unavailable")):
            result = runtime.dispatch_chapter_audit("chapter-0001")
        packet.unlink()
        self.assertFalse(result["valid"])
        self.assertIn("attempt_path", result)
        self.assertEqual(write_json.call_args.args[1]["status"], "provider_failed")
        self.assertIn("continuity_audit_attempt", record["artifacts"])

    def test_audit_normalizer_maps_compatible_agent_issue_labels(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({"issues": [{
            "issue_id": "W-1", "severity": "WARN", "description": "evidence", "recommendation": "fix",
            "dimension": "anti_ai_taste",
        }]})
        self.assertEqual(result["issues"], [{
            "issue_id": "W-1", "severity": "minor", "evidence": "evidence", "required_fix": "fix",
        }])

    def test_audit_normalizer_supplies_only_a_deterministic_missing_issue_id(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({"issues": [{
            "severity": "minor", "evidence": "evidence", "required_fix": "fix",
        }]})
        self.assertEqual(result["issues"][0]["issue_id"], "agent-issue-001")

    def test_audit_normalizer_supplies_neutral_missing_optional_text(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({"issues": [{"severity": "minor"}]})
        self.assertIn("No evidence", result["issues"][0]["evidence"])
        self.assertIn("No corrective action", result["issues"][0]["required_fix"])
    def test_stage_transition_requires_exact_next_stage_and_artifact(self):
        record = {"stage": "chapter_intent", "artifacts": {"intent": "intent.json"}}
        valid = validate_stage_transition(record, "context_compiled", "context.json")
        self.assertTrue(valid["valid"])
        skipped = validate_stage_transition(record, "draft_generated", "draft.md")
        self.assertFalse(skipped["valid"])
        missing = validate_stage_transition(record, "context_compiled", "")
        self.assertFalse(missing["valid"])
        revision = {"stage": "revision_generated", "artifacts": {"revision": "revision.md"}}
        self.assertTrue(
            validate_stage_transition(revision, "final_observed", "observation.json")["valid"]
        )
        self.assertFalse(
            validate_stage_transition(revision, "state_settled", "settlement.json")["valid"]
        )

    def test_accepted_chapter_is_immutable(self):
        record = {"stage": STAGES[-1], "artifacts": {"settlement": "settlement.json"}}
        result = validate_stage_transition(record, STAGES[-1], "new.json")
        self.assertFalse(result["valid"])
        self.assertIn("immutable", " ".join(result["errors"]))

    def test_prose_metrics_flag_repetitive_ai_patterns_without_auto_verdict(self):
        text = (
            "然而，他抬起头。不是因为害怕，而是因为命运。\n\n"
            "然而，他握紧手。不是因为愤怒，而是因为选择。\n\n"
            "然而，他向前走。不是因为勇敢，而是因为责任。"
        )
        result = analyze_prose_metrics(text)
        self.assertGreaterEqual(result["transition_word_hits"], 3)
        self.assertGreaterEqual(result["rhetorical_template_hits"], 3)
        self.assertTrue(result["flags"])
        self.assertNotIn("literary_verdict", result)

    def test_prose_metrics_do_not_treat_closing_quotes_as_sentence_starters(self):
        text = "“先关门。”\n\n“把灯递来。”\n\n“雨已经停了。”\n\n“账页还在。”"
        result = analyze_prose_metrics(text)
        self.assertNotIn("sentence_opening_repetition", result["flags"])

    def test_external_literary_audit_runs_only_at_five_chapter_checkpoints(self):
        self.assertFalse(requires_external_chapter_audit("chapter-0016", "initial"))
        self.assertTrue(requires_external_chapter_audit("chapter-0020", "initial"))
        self.assertFalse(requires_external_chapter_audit("chapter-0020", "final"))

    def test_context_compiler_selects_only_requested_assets_and_emits_trace(self):
        intent = {
            "chapter_id": "chapter-0001",
            "dramatic_purpose": "force a choice",
            "must_keep": ["cost"],
            "must_avoid": ["free power"],
            "expected_state_deltas": [],
            "required_asset_ids": ["character-a"],
            "active_hook_ids": ["hook-a"],
            "scene_constraints": ["one location"],
        }
        assets = [
            {"asset_id": "character-a", "family": "characters"},
            {"asset_id": "artifact-b", "family": "artifacts"},
        ]
        result = compile_chapter_context_payload(
            intent,
            assets,
            {"story_bible": "a" * 64, "volume_outline": "b" * 64},
            [],
        )
        self.assertTrue(result["valid"])
        self.assertEqual([item["asset_id"] for item in result["context"]["assets"]], ["character-a"])
        self.assertEqual(result["trace"]["excluded_asset_count"], 1)
        intent["required_asset_ids"] = ["missing"]
        self.assertFalse(
            compile_chapter_context_payload(intent, assets, {}, [])["valid"]
        )

    def test_rolling_state_replaces_full_settlement_history(self):
        settlements = [
            {
                "chapter_id": f"chapter-{number:04d}",
                "accepted_revision_sha256": str(number) * 64,
                "state_deltas": [{
                    "asset_id": "character-a",
                    "field_path": "character.health",
                    "before": number - 1,
                    "after": number,
                    "evidence": f"evidence-{number}",
                }],
            }
            for number in range(1, 6)
        ]
        snapshot = build_rolling_state_snapshot(settlements)
        self.assertEqual(snapshot["source_chapter_count"], 5)
        self.assertEqual(snapshot["latest_fields"][0]["value"], 5)
        self.assertEqual([item["chapter_id"] for item in snapshot["recent_chapters"]], ["chapter-0004", "chapter-0005"])
        compiled = compile_chapter_context_payload(
            {
                "chapter_id": "chapter-0006", "dramatic_purpose": "test",
                "must_keep": ["state"], "must_avoid": ["drift"],
                "required_asset_ids": ["character-a"], "active_hook_ids": [],
                "scene_constraints": ["bounded"],
            },
            [{"asset_id": "character-a", "family": "characters"}],
            {}, settlements,
        )
        self.assertNotIn("prior_settlements", compiled["context"])
        self.assertEqual(compiled["context"]["rolling_state"]["source_chapter_count"], 5)

    def test_observer_prompt_is_hash_bound_and_excludes_raw_corpus(self):
        payload = build_observer_prompt_payload(
            "chapter-0001", "a" * 64, "正文", {"chapter_id": "chapter-0001"}
        )
        self.assertIn("a" * 64, payload)
        self.assertIn("chapter-0001", payload)
        self.assertNotIn("novel_training_set", payload)

    def test_audit_packet_inlines_bound_artifacts_without_raw_corpus(self):
        import nrl_production_runtime as runtime

        context = {"chapter_id": "chapter-0001", "assets": [], "must_keep": ["cost"]}
        rules = {"hard_rules": ["do not invent assets"]}
        trace = {"chapter_id": "chapter-0001"}
        observation = {"chapter_id": "chapter-0001", "facts": {}}
        record = {
            "stage": "draft_generated",
            "artifacts": {
                "context": "context.json", "rule_stack": "rules.json", "trace": "trace.json",
                "draft": "draft.md",
            },
        }
        with mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "runtime_path", side_effect=lambda value: REPO_ROOT / "system/production_runtime/chapters/chapter-0001" / Path(value).name), mock.patch.object(runtime, "_read_json", side_effect=[context, rules, trace, observation]), mock.patch.object(runtime, "_sha256", return_value="a" * 64):
            packet = runtime.build_chapter_audit_packet("chapter-0001")
        text = (REPO_ROOT / packet["packet_path"]).read_text(encoding="utf-8")
        (REPO_ROOT / packet["packet_path"]).unlink()
        self.assertIn("Compact Context", text)
        self.assertIn("Observed Facts", text)
        self.assertNotIn("novel_training_set", text)

    def test_settlement_must_bind_revision_and_resolve_blocking_audit_issues(self):
        revision_hash = "a" * 64
        audit = {
            "verdict": "ACCEPT_WITH_WARNINGS",
            "issues": [
                {"issue_id": "audit-1", "severity": "blocking"},
                {"issue_id": "audit-2", "severity": "minor"},
            ],
        }
        stale = {
            "chapter_id": "chapter-0001",
            "accepted_revision_sha256": "b" * 64,
            "state_deltas": [],
            "resolved_audit_ids": ["audit-1"],
        }
        self.assertFalse(
            validate_settlement_payload(stale, "chapter-0001", revision_hash, audit)["valid"]
        )
        stale["accepted_revision_sha256"] = revision_hash
        stale["resolved_audit_ids"] = []
        self.assertFalse(
            validate_settlement_payload(stale, "chapter-0001", revision_hash, audit)["valid"]
        )
        stale["resolved_audit_ids"] = ["audit-1"]
        self.assertTrue(
            validate_settlement_payload(stale, "chapter-0001", revision_hash, audit)["valid"]
        )

    def test_acceptance_requires_settlement_bound_to_current_revision(self):
        record = {
            "chapter_id": "chapter-0001",
            "stage": "state_settled",
            "artifacts": {"revision": "revision.md", "settlement": "settlement.json"},
        }
        self.assertFalse(
            validate_acceptance(record, {"accepted_revision_sha256": "a" * 64}, "b" * 64)["valid"]
        )
        self.assertTrue(
            validate_acceptance(record, {"accepted_revision_sha256": "b" * 64}, "b" * 64)["valid"]
        )

    def test_chapter_sequence_requires_immediate_predecessor_acceptance(self):
        self.assertTrue(validate_chapter_sequence([], "chapter-0001")["valid"])
        chapters = [{"chapter_id": "chapter-0001", "stage": "state_settled"}]
        self.assertFalse(validate_chapter_sequence(chapters, "chapter-0002")["valid"])
        chapters[0]["stage"] = "chapter_accepted"
        self.assertTrue(validate_chapter_sequence(chapters, "chapter-0002")["valid"])
        self.assertFalse(validate_chapter_sequence(chapters, "chapter-0003")["valid"])

    def test_rework_required_audit_cannot_be_settled_by_claiming_resolution(self):
        audit = {
            "verdict": "REWORK_REQUIRED",
            "issues": [{"issue_id": "audit-1", "severity": "blocking"}],
        }
        settlement = {
            "chapter_id": "chapter-0001",
            "accepted_revision_sha256": "a" * 64,
            "state_deltas": [],
            "resolved_audit_ids": ["audit-1"],
        }
        self.assertFalse(
            validate_settlement_payload(settlement, "chapter-0001", "a" * 64, audit)["valid"]
        )

    def test_settlement_delta_must_match_an_observed_fact(self):
        audit = {"verdict": "ACCEPT", "issues": []}
        settlement = {
            "chapter_id": "chapter-0001",
            "accepted_revision_sha256": "a" * 64,
            "state_deltas": [{
                "fact_id": "fact-1", "asset_id": "character-a", "field_path": "sanity",
                "operation": "set", "before": 10, "after": 9,
            }],
            "resolved_audit_ids": [],
        }
        observation = {"facts": {"characters": [{
            "fact_id": "fact-1", "asset_id": "character-a", "field_path": "sanity",
            "before": 10, "after": 8, "evidence": "scene consequence",
        }]}}
        self.assertFalse(
            validate_settlement_payload(
                settlement, "chapter-0001", "a" * 64, audit, observation=observation
            )["valid"]
        )
        observation["facts"]["characters"][0]["after"] = 9
        self.assertTrue(
            validate_settlement_payload(
                settlement, "chapter-0001", "a" * 64, audit, observation=observation
            )["valid"]
        )

    def test_observed_settlement_candidate_uses_only_observed_facts(self):
        import nrl_production_runtime as runtime

        record = {
            "stage": "final_audited",
            "artifacts": {"observation": "observation.json", "revision": "revision.md"},
        }
        observation = {"facts": {"characters": [{
            "fact_id": "fact-1", "asset_id": "character-a", "field_path": "character.status",
            "before": "before", "after": "after", "evidence": "text",
        }]}}
        with mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "_read_json", return_value=observation), mock.patch.object(runtime, "_sha256", return_value="a" * 64), mock.patch.object(runtime, "_write_json") as write_json:
            result = runtime.build_observed_settlement_candidate("chapter-0001")
        candidate = write_json.call_args.args[1]
        self.assertEqual(result["state_delta_count"], 1)
        self.assertEqual(candidate["state_deltas"][0]["fact_id"], "fact-1")
        self.assertEqual(candidate["state_deltas"][0]["after"], "after")

    def test_controlled_pipeline_is_idempotent_for_an_accepted_chapter(self):
        import nrl_production_runtime as runtime

        intent = {"chapter_id": "chapter-0001"}
        record = {"chapter_id": "chapter-0001", "stage": "chapter_accepted"}
        with mock.patch.object(runtime, "_read_json", return_value=intent), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}):
            result = runtime.run_controlled_chapter_pipeline("intent.json")
        self.assertTrue(result["valid"])
        self.assertEqual(result["completed"], [])


if __name__ == "__main__":
    unittest.main()
