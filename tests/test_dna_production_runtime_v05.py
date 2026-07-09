import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
NRL = RUNTIME_DIR / "nrl.py"
sys.path.insert(0, str(RUNTIME_DIR))


class RuntimeCliCase(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )


class DnaRegistryCliTests(RuntimeCliCase):
    def test_dna_registry_builds_all_families_without_raw_corpus(self):
        result = self.run_cli("dna-registry-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.5")
        self.assertEqual(
            set(data["summary"]["by_family"]),
            {"book_dna", "narrative_dna", "mechanism_dna", "state_dna", "project_dna"},
        )
        self.assertTrue((REPO_ROOT / "system/dna_registry/dna_registry.v0.5.json").exists())
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))

    def test_dna_registry_cli_loads_generated_registry(self):
        self.run_cli("dna-registry-build")
        result = self.run_cli("dna-registry")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertGreater(data["summary"]["total_entries"], 0)
        self.assertIn("project_dna", data["summary"]["by_family"])


class RagIndexCliTests(RuntimeCliCase):
    def test_rag_index_builds_structured_items_without_raw_prose(self):
        self.run_cli("dna-registry-build")
        result = self.run_cli("rag-index-build")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.5")
        self.assertGreater(data["summary"]["total_items"], 0)
        item = data["items"][0]
        self.assertIn("retrieval_text", item)
        self.assertIn("evidence_weight", item)
        self.assertNotIn("novel_training_set/", json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
