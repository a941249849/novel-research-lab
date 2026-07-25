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

    def test_project_compaction_keeps_model_execution_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter = (
                root
                / "projects/example/production_runtime/chapters/chapter-0001"
            )
            chapter.mkdir(parents=True)
            durable = {
                "intent": "intent.json",
                "revision": "revision.md",
                "revision_metrics": "revision.metrics.json",
                "observation": "observation.json",
                "final_audit": "final_audit.json",
                "writer_execution": "writer.execution.json",
                "observer_execution": "observer.execution.json",
                "final_audit_execution": "final_audit.execution.json",
                "reviewer_execution": "final_audit.execution.json",
                "settlement": "settlement.json",
                "acceptance": "acceptance.json",
            }
            artifacts = {}
            for key, name in durable.items():
                path = chapter / name
                path.write_text(
                    "正文" if path.suffix == ".md" else "{}",
                    encoding="utf-8",
                )
                artifacts[key] = str(path.relative_to(root))
            (chapter / "context.json").write_text("{}", encoding="utf-8")
            (chapter / "draft.md").write_text("草稿", encoding="utf-8")
            registry = (
                root
                / "projects/example/production_runtime/chapter_registry.v0.20.json"
            )
            registry.write_text(
                json.dumps(
                    {
                        "chapters": [
                            {
                                "chapter_id": "chapter-0001",
                                "stage": "chapter_accepted",
                                "artifacts": {
                                    **artifacts,
                                    "context": str(
                                        (chapter / "context.json").relative_to(root)
                                    ),
                                    "draft": str(
                                        (chapter / "draft.md").relative_to(root)
                                    ),
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = compact_accepted_chapters(root, registry)
            remaining = json.loads(registry.read_text(encoding="utf-8"))[
                "chapters"
            ][0]["artifacts"]
        self.assertTrue(result["valid"], result)
        self.assertIn("writer_execution", remaining)
        self.assertIn("observer_execution", remaining)
        self.assertIn("reviewer_execution", remaining)
        self.assertNotIn("context", remaining)
        self.assertNotIn("draft", remaining)


if __name__ == "__main__":
    unittest.main()
