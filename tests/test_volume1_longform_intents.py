import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_volume1_longform import build_volume1_intent, build_volume1_manifest, validate_volume1_manifest


class Volume1LongformIntentTests(unittest.TestCase):
    def test_manifest_covers_only_the_remaining_ninety_volume_one_chapters(self):
        result = validate_volume1_manifest(build_volume1_manifest())
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["chapter_count"], 90)

    def test_chapter_eleven_preserves_the_concealment_constraint(self):
        intent = build_volume1_intent(11)
        self.assertEqual(intent["chapter_id"], "chapter-0011")
        self.assertTrue(any("有限遮掩" in item for item in intent["must_keep"]))

    def test_volume_one_final_chapter_remains_a_prefecture_entry_not_a_final_reveal(self):
        intent = build_volume1_intent(100)
        self.assertTrue(any("州府入口" in item for item in intent["must_keep"]))


if __name__ == "__main__":
    unittest.main()
