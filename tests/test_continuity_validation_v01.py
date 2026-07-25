import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "system/runtime"))

from nrl_continuity_validation import (  # noqa: E402
    split_chapter_document,
    validate_continuity_contract,
)


PROJECT = ROOT / "projects/hundred-crafts-night-procession"


class ContinuityValidationV01Tests(unittest.TestCase):
    def test_contract_freezes_exact_bounded_scope(self) -> None:
        contract = json.loads(
            (PROJECT / "production_runtime/plans/continuity_validation.v0.1.json").read_text()
        )
        self.assertEqual(contract["chapter_range"], [10, 27])
        self.assertEqual(contract["read_only_anchor_chapters"], [10, 24, 25, 26])
        self.assertEqual(
            contract["generated_chapters"], list(range(11, 24)) + [27]
        )
        self.assertFalse(contract["continuous_prose_authorized"])
        self.assertFalse(contract["publish_authorized"])
        self.assertEqual(contract["status"], "continuity_test_passed")
        self.assertEqual(contract["review_result"]["verdict"], "ACCEPT_CONTINUITY_TEST")

    def test_every_chapter_has_explicit_state_delta(self) -> None:
        result = validate_continuity_contract(
            "hundred-crafts-night-procession", require_prose=False
        )
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["covered_chapters"], list(range(10, 28)))
        self.assertEqual(result["generated_chapters"], list(range(11, 24)) + [27])
        self.assertIn("team_authority", result["tracked_state_keys"])
        self.assertIn("water_compartment_debt", result["tracked_state_keys"])
        self.assertIn("public_dissent", result["tracked_state_keys"])
        self.assertEqual(result["status"], "continuity_test_passed")
        self.assertEqual(result["review_verdict"], "ACCEPT_CONTINUITY_TEST")
        self.assertFalse(result["authorization"]["continuous_prose_authorized"])
        self.assertFalse(result["authorization"]["publish_authorized"])

    def test_split_chapter_document(self) -> None:
        parsed = split_chapter_document("## 第11章 楼下有潮\n\n甲。\n\n## 第12章 白日守门人\n\n乙。")
        self.assertEqual([item["chapter"] for item in parsed], [11, 12])
        self.assertEqual(parsed[0]["title"], "楼下有潮")

    def test_prose_has_no_production_layer_language(self) -> None:
        paths = [
            PROJECT / "production_runtime/continuity_validation/block-011-017.md",
            PROJECT / "production_runtime/continuity_validation/block-018-023.md",
            PROJECT / "production_runtime/continuity_validation/chapter-027.md",
        ]
        prose = "\n".join(path.read_text() for path in paths)
        for phrase in ["下一章", "上一章", "本章", "第24章若", "后续章节"]:
            self.assertNotIn(phrase, prose)
        prose_without_headings = "\n".join(
            line for line in prose.splitlines() if not line.startswith("## 第")
        )
        self.assertNotRegex(prose_without_headings, r"第[一二三四五六七八九十百0-9０-９]+章")


if __name__ == "__main__":
    unittest.main()
