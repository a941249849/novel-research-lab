from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

import nrl_system_status


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "system/runtime/nrl.py"


class MultiProjectRuntimeV028Tests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "NRL_ROOT": str(root)}
        result = subprocess.run(
            ["python3", str(CLI), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stderr or result.stdout)
        return result

    def test_default_registry_treats_borrowed_heaven_as_one_project(self) -> None:
        result = subprocess.run(
            ["python3", str(CLI), "projects"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["default_project_id"], "borrowed-heaven")
        self.assertEqual(len(payload["projects"]), 1)
        self.assertEqual(payload["projects"][0]["title"], "《借天改命账》")

    def test_new_project_is_initialized_in_an_isolated_workspace(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nrl-multiproject-") as temp:
            root = Path(temp)
            created = self.run_cli(
                root,
                "project-init",
                "--project-id",
                "second-world",
                "--title",
                "《第二世界》",
                "--genre",
                "玄幻",
            )
            self.assertTrue(json.loads(created.stdout)["created"])
            status = json.loads(
                self.run_cli(root, "project-status", "--project", "second-world").stdout
            )
            self.assertEqual(status["storage_mode"], "isolated_v1")
            self.assertFalse(status["ready_for_prose"])
            self.assertEqual(status["assets"], 0)
            self.assertEqual(status["chapters"], 0)
            validation = json.loads(
                self.run_cli(root, "--project", "second-world", "project-validate").stdout
            )
            self.assertTrue(validation["valid"])
            workspace = root / "projects/second-world"
            self.assertTrue((workspace / "project_state.json").is_file())
            self.assertTrue((workspace / "creation_assets/project_assets.json").is_file())
            self.assertTrue((workspace / "production_runtime/chapter_registry.v0.20.json").is_file())
            all_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in workspace.rglob("*")
                if path.is_file()
            )
            self.assertNotIn("借天改命账", all_text)
            self.assertNotIn("borrowed-heaven", all_text)

    def test_project_path_router_separates_mutable_state_and_keeps_schemas_shared(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nrl-path-router-") as temp:
            root = Path(temp)
            self.run_cli(root, "project-init", "--project-id", "alpha-book", "--title", "《甲书》")
            script = """
import json
from nrl_paths import runtime_path
print(json.dumps({
  'assets': str(runtime_path('system/creation_assets/project_assets.v0.2.json')),
  'chapters': str(runtime_path('system/production_runtime/chapters')),
  'schema': str(runtime_path('system/production_runtime/schemas/chapter_intent.schema.json')),
}))
"""
            env = {
                **os.environ,
                "NRL_ROOT": str(root),
                "NRL_PROJECT_ID": "alpha-book",
                "PYTHONPATH": str(ROOT / "system/runtime"),
            }
            result = subprocess.run(
                ["python3", "-c", script], env=env, text=True, capture_output=True, check=True
            )
            paths = json.loads(result.stdout)
            self.assertIn("projects/alpha-book/creation_assets/project_assets.json", paths["assets"])
            self.assertIn("projects/alpha-book/production_runtime/chapters", paths["chapters"])
            self.assertTrue(paths["schema"].endswith("system/production_runtime/schemas/chapter_intent.schema.json"))

    def test_duplicate_or_unsafe_project_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nrl-project-id-") as temp:
            root = Path(temp)
            self.run_cli(root, "project-init", "--project-id", "valid-id", "--title", "《甲》")
            self.run_cli(root, "project-init", "--project-id", "valid-id", "--title", "《乙》", expected=1)
            self.run_cli(root, "project-init", "--project-id", "../escape", "--title", "《乙》", expected=1)

    def test_borrowed_heaven_planner_cannot_run_inside_another_project(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nrl-profile-guard-") as temp:
            root = Path(temp)
            self.run_cli(root, "project-init", "--project-id", "other-book", "--title", "《别册》")
            result = self.run_cli(
                root,
                "longform-candidate-build",
                "--project",
                "other-book",
                expected=1,
            )
            self.assertIn("planning_profile=borrowed_heaven_v1", result.stderr)
            workspace_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (root / "projects/other-book").rglob("*")
                if path.is_file()
            )
            self.assertNotIn("借天改命账", workspace_text)

    def test_unprepared_project_cannot_inherit_another_projects_runtime_authorization(self) -> None:
        project = {
            "ready_for_prose": False,
            "content_authorized": False,
        }
        state = {"owner_gate_required": False, "blocked_actions": []}
        with mock.patch.object(nrl_system_status, "build_project_status", return_value=project):
            self.assertEqual(
                nrl_system_status.content_progression_for(state),
                "BLOCKED_AT_PROJECT_SETUP",
            )
            self.assertEqual(nrl_system_status.operating_mode_for(state), "PROJECT_DESIGN")


if __name__ == "__main__":
    unittest.main()
