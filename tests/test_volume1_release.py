import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

import nrl_volume1_release as release


class Volume1ReleaseTests(unittest.TestCase):
    def test_release_edit_falls_back_to_antigravity(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.object(release, "_read_json") as read_json, \
                 mock.patch.object(release, "runtime_path") as runtime_path, \
                 mock.patch.object(release, "ask_codex_writer", side_effect=RuntimeError("usage limit")), \
                 mock.patch.object(release, "ask_antigravity_writer", return_value="字" * 3200), \
                 mock.patch.object(release, "_edit_manifest_path") as manifest_path:
                source = mock.Mock()
                source.read_text.return_value = "原稿"
                source.relative_to.return_value = Path("revision.md")
                source.read_bytes.return_value = b"original"
                runtime_path.return_value = source
                read_json.return_value = {
                    "chapters": [{"chapter_id": "chapter-0025", "stage": "chapter_accepted", "artifacts": {"revision": "revision.md"}}]
                }
                with mock.patch.object(release, "ROOT", Path(temp_dir)), \
                     mock.patch.object(release, "EDIT_ROOT", Path(temp_dir)):
                    manifest_path.return_value = Path(temp_dir) / "chapter-0025.json"
                    result = release.dispatch_release_edit("chapter-0025", "修复重复结尾")
        self.assertEqual(result["provider"], "antigravity")

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
