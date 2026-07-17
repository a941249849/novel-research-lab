import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "system/runtime"))

from nrl_story_window import (
    build_story_window_prompt,
    build_story_window_status,
    story_beat_for,
    validate_story_window,
)


class StoryWindowV1Tests(unittest.TestCase):
    def test_volume_one_has_all_ten_story_windows(self):
        status = build_story_window_status()
        self.assertTrue(status["valid"])
        self.assertEqual(status["window_count"], 10)
        self.assertEqual(status["windows"][0]["window"], "001-010")
        self.assertIsNotNone(story_beat_for("chapter-0001"))

    def test_duplicate_required_assets_are_rejected(self):
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        payload["chapters"][0]["required_asset_ids"] *= 2
        result = validate_story_window(payload)
        self.assertFalse(result["valid"])
        self.assertIn("required_asset_ids must be unique", " ".join(result["errors"]))

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
        # The artifact is referenced by a lifecycle boundary even though it is
        # not a direct required_asset_id in the legacy manifest.
        self.assertIn("artifact_ashlight_cup", prompt)
        self.assertIn("artifact.current_acquisition_status", prompt)
        self.assertIn("已从灯座基部取出", prompt)
        self.assertNotIn("novel_training_set/", prompt)
        self.assertLessEqual(len(prompt.encode("utf-8")), 36000)

    def test_future_window_rejects_rollback_of_accepted_artifact_acquisition(self):
        payload = json.loads(
            (ROOT / "system/production_runtime/story_windows/window-041-050.v1.json").read_text(encoding="utf-8")
        )
        payload["window"]["start"] = 51
        payload["window"]["end"] = 60
        payload["start_snapshot"] = [
            "残命灯盏仍处于未取得、未唤醒状态。",
            "命籍衙压力仍在。",
            "泥灯巷护阵仍在承压。",
        ]
        for index, chapter in enumerate(payload["chapters"], start=51):
            chapter["chapter_id"] = f"chapter-{index:04d}"
            chapter["source_status"] = "planned"
            chapter["required_asset_ids"] = chapter["required_asset_ids"][:12]
        result = validate_story_window(payload)
        self.assertFalse(result["valid"])
        self.assertIn("contradicts accepted acquisition state", " ".join(result["errors"]))

    def test_future_window_rejects_more_than_twelve_assets_per_chapter(self):
        payload = json.loads(
            (ROOT / "system/production_runtime/story_windows/window-041-050.v1.json").read_text(encoding="utf-8")
        )
        payload["window"]["start"] = 51
        payload["window"]["end"] = 60
        for index, chapter in enumerate(payload["chapters"], start=51):
            chapter["chapter_id"] = f"chapter-{index:04d}"
            chapter["source_status"] = "planned"
        payload["chapters"][0]["required_asset_ids"] = [
            item["asset_id"]
            for item in json.loads((ROOT / "system/creation_assets/project_assets.v0.2.json").read_text(encoding="utf-8"))["assets"][:13]
        ]
        result = validate_story_window(payload)
        self.assertFalse(result["valid"])
        self.assertIn("at most 12", " ".join(result["errors"]))


if __name__ == "__main__":
    unittest.main()
