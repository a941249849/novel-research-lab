import unittest
import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))
from nrl_controlled_samples import split_sample_chapters, validate_controlled_samples


class ControlledSampleV01Tests(unittest.TestCase):
    def test_split_sample_chapters_preserves_numbers_titles_and_prose(self) -> None:
        rows = split_sample_chapters(
            "# 样章\n\n## 第8章 第二份记录\n\n甲。\n\n## 第9章 新撑旧榫\n\n乙。\n"
        )
        self.assertEqual([row["chapter"] for row in rows], [8, 9])
        self.assertEqual([row["title"] for row in rows], ["第二份记录", "新撑旧榫"])
        self.assertEqual([row["prose"] for row in rows], ["甲。", "乙。"])

    def test_authorized_sample_windows_pass_without_opening_continuous_prose(self) -> None:
        result = validate_controlled_samples("hundred-crafts-night-procession")

        self.assertTrue(result["valid"], result["errors"])
        self.assertFalse(result["continuous_prose_authorized"])
        self.assertFalse(result["publish_authorized"])
        self.assertEqual(
            [window["window_id"] for window in result["windows"]],
            ["sample-008-010", "sample-024-026", "sample-049-051"],
        )
        self.assertTrue(all(window["valid"] for window in result["windows"]))

    def test_cli_persists_auditable_validation_report(self) -> None:
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [
                "python3",
                "system/runtime/nrl.py",
                "--project",
                "hundred-crafts-night-procession",
                "controlled-sample-validate",
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        report_path = root / payload["report_path"]
        self.assertTrue(report_path.is_file())
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertTrue(report["valid"])
        self.assertFalse(report["continuous_prose_authorized"])
        self.assertFalse(report["publish_authorized"])
