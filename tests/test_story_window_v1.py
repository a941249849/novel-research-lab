import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "system/runtime"))

from nrl_story_window import build_story_window_prompt, story_beat_for, validate_story_window


class StoryWindowV1Tests(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "system/production_runtime/story_windows/window-011-020.v1.json"
        self.payload = json.loads(self.path.read_text(encoding="utf-8"))

    def test_first_production_window_has_ten_unique_story_beats(self):
        result = validate_story_window(self.payload)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["chapter_count"], 10)

    def test_chapter_sixteen_is_not_a_generic_template_step(self):
        beat = story_beat_for("chapter-0016")
        self.assertEqual(beat["working_title"], "撤灯")
        self.assertIn("住户", beat["character_choice"])
        self.assertTrue(beat["expected_state_deltas"])

    def test_duplicate_events_are_rejected(self):
        self.payload["chapters"][1]["event"] = self.payload["chapters"][0]["event"]
        result = validate_story_window(self.payload)
        self.assertFalse(result["valid"])
        self.assertIn("unique event", " ".join(result["errors"]))

    def test_unknown_creation_asset_is_rejected(self):
        self.payload["chapters"][5]["required_asset_ids"].append("artifact_missing")
        result = validate_story_window(self.payload)
        self.assertFalse(result["valid"])
        self.assertIn("unknown assets", " ".join(result["errors"]))

    def test_next_window_prompt_is_bounded_to_contracts_and_registered_assets(self):
        prompt = build_story_window_prompt(21)
        self.assertIn("第 21-30 章", prompt)
        self.assertIn("artifact_ashlight_cup", prompt)
        self.assertNotIn("novel_training_set/", prompt)


if __name__ == "__main__":
    unittest.main()
