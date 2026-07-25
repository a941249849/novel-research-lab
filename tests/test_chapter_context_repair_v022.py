import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "system/runtime"))

from nrl_production_runtime import (
    compile_chapter_context_payload,
    validate_context_compile_stage,
)


class ChapterContextRepairV022Tests(unittest.TestCase):
    def test_accepted_chapter_keeps_canonical_output_not_reproducible_context(self):
        intent_path = REPO_ROOT / "system/production_runtime/intents/chapter-0001.v0.21.json"
        chapter_dir = REPO_ROOT / "system/production_runtime/chapters/chapter-0001"
        canonical_intent = json.loads(intent_path.read_text(encoding="utf-8"))
        compiled_intent = json.loads((chapter_dir / "intent.json").read_text(encoding="utf-8"))
        self.assertEqual(canonical_intent, compiled_intent)
        self.assertTrue((chapter_dir / "revision.md").is_file())
        self.assertTrue((chapter_dir / "acceptance.json").is_file())
        for filename in ("context.json", "trace.json", "rule_stack.json", "draft.md"):
            self.assertFalse((chapter_dir / filename).exists())

    def test_compiler_includes_atomic_peers_and_baseline_metadata(self):
        intent = {
            "chapter_id": "chapter-0001",
            "required_asset_ids": ["ledger-a"],
        }
        assets = [
            {
                "asset_id": "ledger-a",
                "relationships": [
                    {"target_id": "ledger-b", "relation_type": "atomic_transaction_peer"}
                ],
            },
            {
                "asset_id": "ledger-b",
                "relationships": [
                    {
                        "target_id": "ledger-c",
                        "relation_type": "atomic_transaction_peer_when_affected",
                    }
                ],
            },
            {"asset_id": "ledger-c", "relationships": []},
            {"asset_id": "dormant-artifact", "relationships": []},
        ]
        baseline = {
            "path": "system/creation_assets/baselines/canonical-v0.21.json",
            "version": "0.21",
            "sha256": "c" * 64,
        }

        result = compile_chapter_context_payload(intent, assets, {}, [], baseline)

        self.assertTrue(result["valid"])
        self.assertEqual(
            result["trace"]["selected_asset_ids"], ["ledger-a", "ledger-b", "ledger-c"]
        )
        self.assertEqual(result["trace"]["dependency_asset_ids"], ["ledger-b", "ledger-c"])
        for key in ("context", "trace", "rule_stack"):
            self.assertEqual(result[key]["version"], "0.21")
            self.assertEqual(result[key]["canonical_baseline"], baseline)

    def test_compiler_rejects_missing_atomic_peer(self):
        result = compile_chapter_context_payload(
            {"chapter_id": "chapter-0001", "required_asset_ids": ["ledger-a"]},
            [
                {
                    "asset_id": "ledger-a",
                    "relationships": [
                        {"target_id": "missing", "relation_type": "atomic_transaction_peer"}
                    ],
                }
            ],
            {},
            [],
        )
        self.assertFalse(result["valid"])
        self.assertIn("missing atomic transaction peer", result["errors"][0])

    def test_recompile_requires_context_compiled_stage_without_draft(self):
        with tempfile.TemporaryDirectory() as temporary:
            chapter_dir = Path(temporary)
            record = {"stage": "context_compiled", "artifacts": {"context": "context.json"}}
            self.assertTrue(validate_context_compile_stage(record, chapter_dir)["valid"])

            (chapter_dir / "draft.md").write_text("existing", encoding="utf-8")
            blocked = validate_context_compile_stage(record, chapter_dir)
            self.assertFalse(blocked["valid"])

            (chapter_dir / "draft.md").unlink()
            record["artifacts"]["draft"] = "draft.md"
            self.assertFalse(validate_context_compile_stage(record, chapter_dir)["valid"])

    def test_recompile_rejects_later_chapter_stages(self):
        record = {"stage": "draft_generated", "artifacts": {"draft": "draft.md"}}
        with tempfile.TemporaryDirectory() as temporary:
            result = validate_context_compile_stage(record, Path(temporary))
        self.assertFalse(result["valid"])
        self.assertFalse(result["recompile"])


if __name__ == "__main__":
    unittest.main()
