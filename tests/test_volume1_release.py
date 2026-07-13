import sys
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

import nrl_volume1_release as release


class Volume1ReleaseTests(unittest.TestCase):
    def test_incomplete_volume_is_not_fanqie_ready(self):
        registry = {"chapters": [{"chapter_id": "chapter-0001", "stage": "chapter_accepted", "artifacts": {}}]}
        with mock.patch.object(release, "_read_json", return_value=registry):
            status = release.build_release_readiness()
        self.assertFalse(status["valid"])
        self.assertFalse(status["checks"]["all_100_chapters_accepted"])

    def test_window_packet_rejects_noncanonical_ranges(self):
        with self.assertRaises(ValueError):
            release.build_window_review_packet(12, 21)


if __name__ == "__main__":
    unittest.main()
