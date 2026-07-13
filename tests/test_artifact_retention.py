import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_artifact_retention import build_compaction_plan, compact_accepted_chapters


class ArtifactRetentionTests(unittest.TestCase):
    def _fixture(self, root: Path) -> Path:
        chapter = root / "system/production_runtime/chapters/chapter-0001"
        chapter.mkdir(parents=True)
        for name in (
            "intent.json", "revision.md", "revision.metrics.json", "observation.json",
            "final_audit.json", "settlement.json", "acceptance.json", "context.json", "draft.md",
        ):
            (chapter / name).write_text("{}" if name.endswith(".json") else "正文", encoding="utf-8")
        registry = root / "system/production_runtime/chapter_registry.v0.20.json"
        registry.write_text(json.dumps({"chapters": [{
            "chapter_id": "chapter-0001",
            "stage": "chapter_accepted",
            "source_hashes": {"source": "a" * 64},
            "artifacts": {name.replace(".metrics", "_metrics").replace(".json", "").replace(".md", ""): str((chapter / name).relative_to(root)) for name in (
                "intent.json", "revision.md", "revision.metrics.json", "observation.json",
                "final_audit.json", "settlement.json", "acceptance.json", "context.json", "draft.md",
            )},
        }]}), encoding="utf-8")
        return registry

    def test_plan_keeps_release_evidence_and_marks_intermediates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = self._fixture(root)
            plan = build_compaction_plan(root, registry)
            self.assertTrue(plan["valid"])
            self.assertEqual(plan["accepted_chapters"], 1)
            self.assertTrue(any(path.endswith("/context.json") for path in plan["remove_files"]))
            self.assertTrue(any(path.endswith("/draft.md") for path in plan["remove_files"]))
            self.assertFalse(any(path.endswith("/revision.md") for path in plan["remove_files"]))

    def test_compaction_updates_registry_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = self._fixture(root)
            result = compact_accepted_chapters(root, registry)
            self.assertTrue(result["valid"])
            self.assertEqual(result["removed_file_count"], 2)
            artifacts = json.loads(registry.read_text(encoding="utf-8"))["chapters"][0]["artifacts"]
            self.assertNotIn("context", artifacts)
            self.assertNotIn("draft", artifacts)
            second = compact_accepted_chapters(root, registry)
            self.assertEqual(second["removed_file_count"], 0)


if __name__ == "__main__":
    unittest.main()
