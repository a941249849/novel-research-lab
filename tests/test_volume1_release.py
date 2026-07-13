import sys
import tempfile
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

    def test_next_window_is_blocked_until_the_previous_window_review_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing-review.json"
            with mock.patch.object(release, "_window_path", return_value=missing):
                self.assertTrue(release.prior_window_review_required("chapter-0021"))
                self.assertFalse(release.prior_window_review_required("chapter-0022"))

    def test_external_release_edit_rejects_short_content(self):
        source = Path(self.id().replace(".", "_"))
        source.write_text("短文本", encoding="utf-8")
        registry = {"chapters": [{"chapter_id": "chapter-0001", "stage": "chapter_accepted", "artifacts": {"revision": "x.md"}}]}
        try:
            with mock.patch.object(release, "_read_json", return_value=registry):
                with self.assertRaisesRegex(RuntimeError, "3000-4200"):
                    release.record_external_release_edit("chapter-0001", source, "test", "external")
        finally:
            source.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
