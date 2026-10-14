"""Tests for the scaffold.sh generator.

These tests invoke the real scaffold.sh script in a temporary directory and
verify that the generated project configuration is complete and consistent.
"""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"


class TestScaffoldKiloJson(unittest.TestCase):
    """Verify scaffold.sh emits a complete, valid kilo.json."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scaffold-test-"))
        self.project_dir = self.tmp / "my-project"
        # --no-test keeps the run fast and hermetic.
        result = subprocess.run(
            ["bash", str(SCAFFOLD), "My Project", str(self.project_dir), "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"scaffold.sh failed:\nstdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            ),
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_kilo_json_is_valid(self) -> None:
        kilo_json = self.project_dir / "kilo.json"
        self.assertTrue(kilo_json.is_file(), "kilo.json was not generated")
        data = json.loads(kilo_json.read_text())
        self.assertIsInstance(data, dict)

    def test_kilo_json_has_scaffolder_subagent(self) -> None:
        """Scaffolded projects must define the scaffolder subagent.

        The scaffolding system depends on this subagent being present so that
        scaffolded repositories can themselves scaffold further projects.
        """
        data = json.loads((self.project_dir / "kilo.json").read_text())
        agents = data.get("agent", {})
        self.assertIn(
            "scaffolder",
            agents,
            msg="kilo.json is missing the 'scaffolder' subagent",
        )
        scaffolder = agents["scaffolder"]
        self.assertEqual(scaffolder.get("mode"), "subagent")
        self.assertEqual(scaffolder.get("model"), "kilo/kilo-auto/free")
        self.assertIsInstance(scaffolder.get("description"), str)
        self.assertTrue(scaffolder["description"].strip())

    def test_kilo_json_permission_is_allow(self) -> None:
        data = json.loads((self.project_dir / "kilo.json").read_text())
        self.assertEqual(data.get("permission"), "allow")

    def test_required_files_generated(self) -> None:
        expected = [
            "AGENTS.md",
            "README.md",
            "CHANGELOG.md",
            "Makefile",
            "pyproject.toml",
            "hello.py",
            "calculator.py",
            ".gitignore",
            ".pre-commit-config.yaml",
            ".kilo/.gitignore",
            ".kilo/agent/scaffolder.md",
            ".kilo/command/handover.md",
            ".kilo/command/scaffold-project.md",
            ".kilo/skill/scaffolding-helper.md",
            ".github/workflows/main.yml",
            "tests/test_hello.py",
            "tests/test_calculator.py",
        ]
        for rel in expected:
            path = self.project_dir / rel
            self.assertTrue(path.is_file(), f"Expected generated file missing: {rel}")

    def test_pyproject_has_ruff_config(self) -> None:
        content = (self.project_dir / "pyproject.toml").read_text()
        self.assertIn("[tool.ruff]", content)
        self.assertIn("[tool.ruff.lint]", content)
        self.assertIn('select = ["E", "F", "I", "W"]', content)

    def test_makefile_has_typecheck_and_pre_commit_targets(self) -> None:
        content = (self.project_dir / "Makefile").read_text()
        self.assertIn("typecheck:", content)
        self.assertIn("pre-commit-install:", content)
        self.assertIn("pre-commit-run:", content)

    def test_pre_commit_config_is_valid(self) -> None:
        content = (self.project_dir / ".pre-commit-config.yaml").read_text()
        self.assertIn("ruff", content)
        self.assertIn("mypy", content)
        self.assertIn("unittest", content)
        self.assertIn("scaffold-test", content)

    def test_calculator_has_all_operations(self) -> None:
        content = (self.project_dir / "calculator.py").read_text()
        self.assertIn("def add(", content)
        self.assertIn("def subtract(", content)
        self.assertIn("def multiply(", content)
        self.assertIn("def divide(", content)


class TestScaffoldProjectNameNormalization(unittest.TestCase):
    """Verify project names are normalized into safe identifiers."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scaffold-name-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _scaffold(self, name: str) -> Path:
        out = self.tmp / "out"
        result = subprocess.run(
            ["bash", str(SCAFFOLD), name, str(out), "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"scaffold.sh failed for name '{name}':\n{result.stderr}",
        )
        return out

    def test_spaces_and_mixed_case_normalized(self) -> None:
        out = self._scaffold("My Cool Tool")
        # Directory name should be normalized to lowercase hyphenated form.
        self.assertTrue((out / "pyproject.toml").is_file())
        content = (out / "pyproject.toml").read_text()
        self.assertIn('name = "my-cool-tool"', content)

    def test_special_chars_stripped(self) -> None:
        out = self._scaffold("Awesome!!! Project @#$ 123")
        content = (out / "pyproject.toml").read_text()
        # Only lowercase letters, digits, and hyphens should remain.
        for line in content.splitlines():
            if line.startswith("name = "):
                self.assertRegex(line, r'name = "[a-z0-9-]+"')


if __name__ == "__main__":
    unittest.main()
