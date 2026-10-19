"""Guard the synchronization invariant between the repository and the scaffold.

Every stdlib wrapper module in the repository must be reachable from every
surface of the project: the package metadata, the scaffold generator, the
documentation, the command documentation, the changelog, and the scaffold
assertions. The embedded copies inside ``scaffold.sh`` must also be byte
identical to the repository files, so a scaffolded project is a faithful copy
of the project that generated it.
"""

import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"
PYPROJECT = ROOT / "pyproject.toml"
README = ROOT / "README.md"
PROJDOC = ROOT / ".kilo" / "command" / "scaffold-project.md"
CHANGELOG = ROOT / "CHANGELOG.md"
SCAFFOLD_TESTS = ROOT / "tests" / "test_scaffold.py"

HEREDOC = re.compile(
    r"cat > \"\$OUTPUT_DIR/(?P<path>[A-Za-z0-9_./-]+)\" <<'(?P<delim>[A-Z0-9_]+)'\n"
    r"(?P<body>.*?)\n(?P=delim)\n",
    re.S,
)


def module_names() -> list[str]:
    """Return the repository's stdlib wrapper module stems."""
    return sorted(
        path.name[: -len(".py")]
        for path in ROOT.glob("*_utils.py")
        if path.is_file()
    )


def embedded_bodies(scaffold_text: str) -> dict[str, list[str]]:
    """Map generated file path to the list of embedded file bodies."""
    bodies: dict[str, list[str]] = {}
    for match in HEREDOC.finditer(scaffold_text):
        bodies.setdefault(match.group("path"), []).append(match.group("body"))
    return bodies


def header_comment(scaffold_text: str) -> str:
    """Return the leading comment block of the generator."""
    lines = scaffold_text.split("\n")
    for index, line in enumerate(lines):
        if line and not line.startswith("#"):
            return "\n".join(lines[:index])
    return "\n".join(lines)


class TestScaffoldSync(unittest.TestCase):
    """Verify the repository and the scaffold generator stay in sync."""

    modules: list[str]
    scaffold_text: str
    header: str
    bodies: dict[str, list[str]]
    pyproject_text: str
    readme_text: str
    projdoc_text: str
    changelog_text: str
    scaffold_test_text: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = module_names()
        cls.scaffold_text = SCAFFOLD.read_text()
        cls.header = header_comment(cls.scaffold_text)
        cls.bodies = embedded_bodies(cls.scaffold_text)
        cls.pyproject_text = PYPROJECT.read_text()
        cls.readme_text = README.read_text()
        cls.projdoc_text = PROJDOC.read_text()
        cls.changelog_text = CHANGELOG.read_text()
        cls.scaffold_test_text = SCAFFOLD_TESTS.read_text()

    def test_modules_are_discovered(self) -> None:
        self.assertGreater(len(self.modules), 0)

    def test_every_module_has_a_test(self) -> None:
        for name in self.modules:
            with self.subTest(module=name):
                self.assertTrue(
                    (ROOT / "tests" / f"test_{name}.py").is_file(),
                    f"missing tests/test_{name}.py",
                )

    def test_every_module_is_registered_in_pyproject(self) -> None:
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f'"{name}"',
                    self.pyproject_text,
                    f"{name} is not registered in pyproject.toml py_modules",
                )

    def test_scaffold_generates_every_module_and_test(self) -> None:
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(f"{name}.py", self.bodies, f"scaffold.sh does not generate {name}.py")
                self.assertIn(
                    f"tests/test_{name}.py",
                    self.bodies,
                    f"scaffold.sh does not generate tests/test_{name}.py",
                )

    def test_embedded_copies_match_repository(self) -> None:
        for name in self.modules:
            for relative in (f"{name}.py", f"tests/test_{name}.py"):
                with self.subTest(file=relative):
                    bodies = self.bodies.get(relative, [])
                    self.assertGreater(
                        len(bodies),
                        0,
                        f"scaffold.sh does not embed {relative}",
                    )
                    expected = (ROOT / relative).read_text().rstrip("\n")
                    for body in bodies:
                        self.assertEqual(
                            body,
                            expected,
                            f"embedded {relative} in scaffold.sh differs from the repository copy",
                        )

    def test_scaffold_header_lists_every_module(self) -> None:
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f"#   - {name}.py —",
                    self.header,
                    f"scaffold.sh header comment does not list {name}.py",
                )
                self.assertTrue(
                    f"#   - test_{name}.py —" in self.header
                    or f"#   - tests/test_{name}.py —" in self.header,
                    f"scaffold.sh header comment does not list the test for {name}.py",
                )

    def test_every_module_is_documented(self) -> None:
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f"{name}.py",
                    self.readme_text,
                    f"README.md does not mention {name}.py",
                )
                self.assertIn(
                    f"`{name}.py`",
                    self.readme_text,
                    f"README.md does not describe {name}.py",
                )
                self.assertIn(
                    f"tests/test_{name}.py",
                    self.readme_text,
                    f"README.md does not mention tests/test_{name}.py",
                )
                self.assertIn(
                    f"- `{name}.py` —",
                    self.projdoc_text,
                    f"scaffold-project.md does not list {name}.py",
                )
                self.assertIn(
                    f"- `tests/test_{name}.py` —",
                    self.projdoc_text,
                    f"scaffold-project.md does not list tests/test_{name}.py",
                )
                self.assertIn(
                    f"{name}.py",
                    self.changelog_text,
                    f"CHANGELOG.md does not mention {name}.py",
                )
                self.assertIn(
                    f"tests/test_{name}.py",
                    self.changelog_text,
                    f"CHANGELOG.md does not mention tests/test_{name}.py",
                )

    def test_every_module_is_asserted_by_scaffold_tests(self) -> None:
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f'"{name}.py"',
                    self.scaffold_test_text,
                    f"tests/test_scaffold.py does not assert {name}.py",
                )
                self.assertIn(
                    f'"tests/test_{name}.py"',
                    self.scaffold_test_text,
                    f"tests/test_scaffold.py does not assert tests/test_{name}.py",
                )

    def test_generated_project_has_no_unexpected_files(self) -> None:
        """The scaffold must not emit Python files that the repository lacks."""
        repo_files = {
            path.name
            for path in ROOT.glob("*.py")
            if path.is_file() and not path.name.startswith("_")
        }
        generated = {
            os.path.basename(path)
            for path in self.bodies
            if path.endswith(".py") and "/" not in path
        }
        self.assertTrue(
            generated.issubset(repo_files),
            f"scaffold.sh generates unknown modules: {sorted(generated - repo_files)}",
        )


if __name__ == "__main__":
    unittest.main()
