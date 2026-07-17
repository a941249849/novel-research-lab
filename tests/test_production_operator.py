import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_production_operator import build_operator_status, describe_next_production_action


class ProductionOperatorTests(unittest.TestCase):
    def test_status_rejects_an_earlier_stale_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "system/production_runtime/chapter_registry.v0.20.json"
            registry.parent.mkdir(parents=True)
            reviews = root / "system/production_runtime/window_reviews"
            reviews.mkdir(parents=True)
            chapters = []
            hashes = {}
            for ordinal in range(1, 21):
                chapter_id = f"chapter-{ordinal:04d}"
                revision = root / f"{chapter_id}.md"
                revision.write_text("字" * 3200, encoding="utf-8")
                chapters.append({"chapter_id": chapter_id, "stage": "chapter_accepted", "artifacts": {"revision": str(revision.relative_to(root))}})
                import hashlib
                hashes[chapter_id] = hashlib.sha256(revision.read_bytes()).hexdigest()
            registry.write_text(json.dumps({"chapters": chapters}), encoding="utf-8")
            for start, end in ((1, 10), (11, 20)):
                ids = [f"chapter-{number:04d}" for number in range(start, end + 1)]
                payload = {"verdict": "ACCEPT", "chapter_ids": ids, "revision_hashes": {chapter_id: hashes[chapter_id] for chapter_id in ids}}
                if start == 1:
                    payload["revision_hashes"]["chapter-0001"] = "stale"
                (reviews / f"window-{start:03d}-{end:03d}.json").write_text(json.dumps(payload), encoding="utf-8")
            status = build_operator_status(registry, target=100)
        self.assertEqual(status["blocking_window_review"], "001-010")
        self.assertEqual(status["blocking_window_verdict"], "STALE")
        self.assertIsNone(status["resume_command"])

    def test_next_action_is_derived_from_current_window(self):
        action = describe_next_production_action(
            {"accepted_contiguous": 30, "target_chapters": 100, "active_window": "031-040", "next_chapter": "chapter-0031", "resume_command": "produce"}
        )
        self.assertIn("031-040", action["label_zh"])
        self.assertIn("第 31 章", action["label_zh"])

    def test_rejected_window_blocks_next_window_action(self):
        action = describe_next_production_action({
            "accepted_contiguous": 70,
            "target_chapters": 100,
            "blocking_window_review": "061-070",
        })
        self.assertIn("禁止推进", action["label_zh"])
        self.assertIn("--start 61 --end 70", action["safe_command"])

    def test_status_exposes_one_resume_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(json.dumps({"chapters": [
                {"chapter_id": "chapter-0001", "stage": "chapter_accepted"},
                {"chapter_id": "chapter-0002", "stage": "chapter_accepted"},
            ]}), encoding="utf-8")
            status = build_operator_status(registry, target=100)
        self.assertEqual(status["accepted_contiguous"], 2)
        self.assertEqual(status["next_chapter"], "chapter-0003")
        self.assertEqual(status["resume_command"], "python3 system/runtime/nrl.py produce --until 100")
        self.assertEqual(status["accepted_chapters_requiring_release_edit"], ["chapter-0001", "chapter-0002"])

    def test_status_reports_registry_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(json.dumps({"chapters": [
                {"chapter_id": "chapter-0001", "stage": "chapter_accepted"},
                {"chapter_id": "chapter-0003", "stage": "chapter_accepted"},
            ]}), encoding="utf-8")
            status = build_operator_status(registry, target=100)
        self.assertFalse(status["valid"])
        self.assertIn("chapter-0002", status["errors"][0])


if __name__ == "__main__":
    unittest.main()
