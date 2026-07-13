import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_longform_cluster1 import _intent


class LongformCluster1IntentTests(unittest.TestCase):
    def test_intents_keep_assets_and_lifecycle_boundaries(self):
        intent = _intent(10)
        self.assertEqual(intent["chapter_id"], "chapter-0010")
        self.assertIn("state_ledger_mother_life_lamp_countdown", intent["required_asset_ids"])
        self.assertTrue(any("残命灯盏" in item for item in intent["must_keep"]))


if __name__ == "__main__":
    unittest.main()
