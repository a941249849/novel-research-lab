import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_production_runtime import (
    STAGES,
    analyze_prose_metrics,
    compile_chapter_context_payload,
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


if __name__ == "__main__":
    unittest.main()
