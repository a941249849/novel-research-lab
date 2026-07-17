import sys
import tempfile
import unittest
import json
from unittest import mock
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

import nrl_volume1_release as release


class Volume1ReleaseTests(unittest.TestCase):
    def test_volume_one_titles_cover_all_chapters_and_are_unique(self):
        titles = release.load_volume1_titles()
        self.assertEqual(set(titles), set(release.CHAPTER_IDS))
        self.assertEqual(len(set(titles.values())), 100)
        self.assertEqual(titles["chapter-0001"], "灰雨里的错账")

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

    def test_accepting_window_review_settles_release_edit_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest = root / "chapter-0001.json"
            manifest.write_text(json.dumps({"status": "pending_window_re_review"}), encoding="utf-8")
            packet = {
                "valid": True,
                "packet": {
                    "window": "001-010",
                    "chapter_ids": [f"chapter-{number:04d}" for number in range(1, 11)],
                    "chapters": [
                        {"chapter_id": f"chapter-{number:04d}", "source_kind": "release_edit" if number == 1 else "accepted_revision", "revision_sha256": f"hash-{number}"}
                        for number in range(1, 11)
                    ],
                },
            }
            payload = {
                "window": "001-010",
                "chapter_ids": packet["packet"]["chapter_ids"],
                "revision_hashes": {item["chapter_id"]: item["revision_sha256"] for item in packet["packet"]["chapters"]},
                "verdict": "ACCEPT",
                "findings": [],
            }
            with mock.patch.object(release, "build_window_review_packet", return_value=packet), \
                 mock.patch.object(release, "_window_path", return_value=root / "window-001-010.json"), \
                 mock.patch.object(release, "_edit_manifest_path", return_value=manifest), \
                 mock.patch.object(release, "ROOT", root):
                release.record_window_review(payload)
            settled = json.loads(manifest.read_text())
        self.assertEqual(settled["status"], "approved_by_window_review")
        self.assertEqual(settled["reviewed_release_edit_sha256"], "hash-1")

    def test_fanqie_manifest_hashes_exported_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "revision.md"
            source.write_text("正文" * 1600, encoding="utf-8")
            records = {
                chapter_id: {
                    "chapter_id": chapter_id,
                    "stage": "chapter_accepted",
                    "artifacts": {"revision": str(source)},
                }
                for chapter_id in release.CHAPTER_IDS
            }
            titles = {chapter_id: f"标题{ordinal}" for ordinal, chapter_id in enumerate(release.CHAPTER_IDS, 1)}
            with mock.patch.object(release, "RELEASE_ROOT", root / "release"), \
                 mock.patch.object(release, "ROOT", root), \
                 mock.patch.object(release, "build_release_readiness", return_value={"valid": True}), \
                 mock.patch.object(release, "_read_json", return_value={"chapters": list(records.values())}), \
                 mock.patch.object(release, "_effective_revision", side_effect=lambda record: (source, "accepted_revision")), \
                 mock.patch.object(release, "load_volume1_titles", return_value=titles):
                result = release.build_fanqie_upload_package()
            manifest = json.loads((root / "release/00_submission_manifest.json").read_text())
            first = manifest["chapters"][0]
            chapter_file = root / "release" / first["file"]
            chapter_hash = release._sha256(chapter_file)
            manuscript_hash = release._sha256(root / "release/01_volume1_full.txt")
        self.assertTrue(result["valid"])
        self.assertEqual(first["file_sha256"], chapter_hash)
        self.assertEqual(manifest["full_manuscript_sha256"], manuscript_hash)

    def test_next_window_is_blocked_until_the_previous_window_review_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing-review.json"
            with mock.patch.object(release, "_window_path", return_value=missing):
                self.assertTrue(release.prior_window_review_required("chapter-0021"))
                self.assertFalse(release.prior_window_review_required("chapter-0022"))

    def test_release_readiness_rejects_stale_window_hashes(self):
        records = []
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for ordinal in range(1, 101):
                chapter_id = f"chapter-{ordinal:04d}"
                chapter = root / f"{chapter_id}.md"
                chapter.write_text("字" * 3200, encoding="utf-8")
                metrics = root / f"{chapter_id}.metrics.json"
                metrics.write_text(json.dumps({"chinese_character_count": 3200}), encoding="utf-8")
                audit = root / f"{chapter_id}.audit.json"
                audit.write_text(json.dumps({"verdict": "ACCEPT"}), encoding="utf-8")
                records.append({
                    "chapter_id": chapter_id,
                    "stage": "chapter_accepted",
                    "artifacts": {
                        "revision": str(chapter),
                        "revision_metrics": str(metrics),
                        "observation": str(metrics),
                        "settlement": str(metrics),
                        "acceptance": str(metrics),
                        "final_audit": str(audit),
                    },
                })
            reviews = {}
            for start, end in release.WINDOWS:
                window = f"{start:03d}-{end:03d}"
                ids = [f"chapter-{number:04d}" for number in range(start, end + 1)]
                reviews[window] = {
                    "window": window,
                    "chapter_ids": ids,
                    "revision_hashes": {chapter_id: release._sha256(root / f"{chapter_id}.md") for chapter_id in ids},
                    "verdict": "ACCEPT",
                    "findings": [],
                }
                (root / f"window-{window}.json").write_text("{}", encoding="utf-8")
            reviews["001-010"]["revision_hashes"]["chapter-0001"] = "stale"

            def read_json(path):
                path = Path(path)
                if path == release.REGISTRY_PATH:
                    return {"chapters": records}
                if path.name.startswith("window-"):
                    return reviews[path.stem.removeprefix("window-")]
                return json.loads(path.read_text())

            with mock.patch.object(release, "_read_json", side_effect=read_json), \
                 mock.patch.object(release, "runtime_path", side_effect=lambda value: Path(value)), \
                 mock.patch.object(release, "_effective_revision", side_effect=lambda record: (Path(record["artifacts"]["revision"]), "accepted_revision")), \
                 mock.patch.object(release, "_window_path", side_effect=lambda start, end: root / f"window-{start:03d}-{end:03d}.json"), \
                 mock.patch.object(release, "load_volume1_titles", return_value={chapter_id: chapter_id for chapter_id in release.CHAPTER_IDS}):
                status = release.build_release_readiness()
        self.assertFalse(status["valid"])
        self.assertIn("001-010", status["missing_or_rejected_windows"])

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

    def test_failed_generated_release_edit_keeps_best_recovery_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = mock.Mock()
            source.read_text.return_value = "原稿"
            source.relative_to.return_value = Path("revision.md")
            source.read_bytes.return_value = b"original"
            registry = {
                "chapters": [{
                    "chapter_id": "chapter-0001",
                    "stage": "chapter_accepted",
                    "artifacts": {"revision": "revision.md"},
                }]
            }
            short = "短稿" * 500
            closer = "较长候选" * 700
            with mock.patch.object(release, "_read_json", return_value=registry), \
                 mock.patch.object(release, "runtime_path", return_value=source), \
                 mock.patch.object(release, "ask_codex_writer", return_value=short), \
                 mock.patch.object(release, "ask_antigravity_writer", return_value=closer), \
                 mock.patch.object(release, "codex_usage_limited", return_value=False), \
                 mock.patch.object(release, "ROOT", root), \
                 mock.patch.object(release, "EDIT_ROOT", root):
                with self.assertRaisesRegex(RuntimeError, "recovery_candidate"):
                    release.dispatch_release_edit("chapter-0001", "测试修订")
            recovery = root / "chapter-0001.recovery_candidate.md"
            self.assertTrue(recovery.is_file())
            self.assertEqual(recovery.read_text(encoding="utf-8").strip(), closer)


if __name__ == "__main__":
    unittest.main()
