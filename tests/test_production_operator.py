import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_production_operator import build_operator_status, describe_next_production_action


class ProductionOperatorTests(unittest.TestCase):
    def test_next_action_is_derived_from_current_window(self):
        action = describe_next_production_action(
            {"accepted_contiguous": 30, "target_chapters": 100, "active_window": "031-040", "next_chapter": "chapter-0031", "resume_command": "produce"}
        )
        self.assertIn("031-040", action["label_zh"])
        self.assertIn("第 31 章", action["label_zh"])

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
