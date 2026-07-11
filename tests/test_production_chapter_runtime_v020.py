import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_production_runtime import (
    STAGES,
    analyze_prose_metrics,
    build_observer_prompt_payload,
    compile_chapter_context_payload,
    validate_acceptance,
    validate_chapter_sequence,
    validate_settlement_payload,
    validate_stage_transition,
)


class ProductionChapterRuntimeV020Tests(unittest.TestCase):
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
            validate_stage_transition(revision, "revision_audited", "revision_audit.json")["valid"]
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

    def test_observer_prompt_is_hash_bound_and_excludes_raw_corpus(self):
        payload = build_observer_prompt_payload(
            "chapter-0001", "a" * 64, "正文", {"chapter_id": "chapter-0001"}
        )
        self.assertIn("a" * 64, payload)
        self.assertIn("chapter-0001", payload)
        self.assertNotIn("novel_training_set", payload)

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


if __name__ == "__main__":
    unittest.main()
