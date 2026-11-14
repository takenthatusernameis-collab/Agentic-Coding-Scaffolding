"""Guard the synchronization invariant between the repository and the scaffold.

Every stdlib wrapper module in the repository must be reachable from every
surface of the project: the package metadata, the scaffold generator, the
documentation, the command documentation, the changelog, and the scaffold
assertions. The embedded copies inside ``scaffold.sh`` must also be byte
identical to the repository files, so a scaffolded project is a faithful copy
of the project that generated it.
"""

import importlib.util
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"
TOOL = ROOT / "tools" / "refresh_scaffold.py"
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

PYPROJECT_HEREDOC = re.compile(
    r"cat > \"\$OUTPUT_DIR/pyproject\.toml\" <<(?P<delim>[A-Z0-9_]+)\n"
    r"(?P<body>.*?)\n(?P=delim)\n",
    re.S,
)


def load_refresh_tool():
    """Return the refresh tool module loaded from its file path.

    The refresh tool is the single definition of which embedded copies are
    verbatim and which are templates, so the sync tests ask it instead of
    repeating the rules and letting the two drift apart.
    """
    spec = importlib.util.spec_from_file_location("refresh_scaffold", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


refresh_scaffold = load_refresh_tool()


def module_names() -> list[str]:
    """Return the repository's stdlib wrapper module stems."""
    return sorted(path.name[: -len(".py")] for path in ROOT.glob("*_utils.py") if path.is_file())


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


def embedded_pyproject(scaffold_text: str) -> str:
    """Return the body of the ``pyproject.toml`` template of the generator."""
    match = PYPROJECT_HEREDOC.search(scaffold_text)
    return match.group("body") if match else ""


def readme_module_paragraph(readme_text: str, name: str) -> str:
    """Return the paragraph of the README that describes a module."""
    for line in readme_text.split("\n"):
        if line.startswith("The project includes") and f"`{name}.py`" in line:
            return line
    return ""


def readme_tree_line(readme_text: str, name: str) -> str:
    """Return the line of the architecture tree of the README for a module."""
    pattern = re.compile(rf"^{re.escape(name)}\.py\s+#")
    for line in readme_text.split("\n"):
        if pattern.match(line):
            return line
    return ""


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

    @classmethod
    def embedded_text(cls, path: str) -> str:
        """Return the body of the embedded *path* of the generator."""
        bodies = cls.bodies.get(path, [])
        return bodies[0] if bodies else ""

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

    def test_every_module_is_registered_in_the_embedded_pyproject(self) -> None:
        pyproject = embedded_pyproject(self.scaffold_text)
        self.assertTrue(pyproject, "scaffold.sh does not embed a pyproject.toml template")
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f'"{name}"',
                    pyproject,
                    f"{name} is not registered in the embedded pyproject.toml py_modules",
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

    def test_the_embedded_readme_documents_every_module(self) -> None:
        readme = self.embedded_text("README.md")
        self.assertTrue(readme, "scaffold.sh does not embed a README.md template")
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f"{name}.py",
                    readme,
                    f"the embedded README.md does not mention {name}.py",
                )
                self.assertIn(
                    f"tests/test_{name}.py",
                    readme,
                    f"the embedded README.md does not mention tests/test_{name}.py",
                )

    def test_the_embedded_readme_reuses_the_repository_module_sections(self) -> None:
        readme = self.embedded_text("README.md")
        self.assertTrue(readme, "scaffold.sh does not embed a README.md template")
        for name in self.modules:
            paragraph = readme_module_paragraph(self.readme_text, name)
            if not paragraph:
                continue
            with self.subTest(module=name):
                self.assertIn(
                    paragraph,
                    readme,
                    f"the embedded README.md does not reuse the module section of {name}.py",
                )

    def test_the_embedded_readme_reuses_the_repository_architecture_tree(self) -> None:
        readme = self.embedded_text("README.md")
        self.assertTrue(readme, "scaffold.sh does not embed a README.md template")
        for name in self.modules:
            tree_line = readme_tree_line(self.readme_text, name)
            if not tree_line:
                continue
            with self.subTest(module=name):
                self.assertIn(
                    tree_line,
                    readme,
                    f"the embedded README.md does not reuse the tree entry of {name}.py",
                )

    def test_the_embedded_changelog_documents_every_module(self) -> None:
        changelog = self.embedded_text("CHANGELOG.md")
        self.assertTrue(changelog, "scaffold.sh does not embed a CHANGELOG.md template")
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f"{name}.py",
                    changelog,
                    f"the embedded CHANGELOG.md does not mention {name}.py",
                )
                self.assertIn(
                    f"tests/test_{name}.py",
                    changelog,
                    f"the embedded CHANGELOG.md does not mention tests/test_{name}.py",
                )

    def test_the_embedded_command_document_lists_every_module(self) -> None:
        document = self.embedded_text(".kilo/command/scaffold-project.md")
        self.assertTrue(document, "scaffold.sh does not embed the command document")
        for name in self.modules:
            with self.subTest(module=name):
                self.assertIn(
                    f"- `{name}.py` —",
                    document,
                    f"the embedded command document does not list {name}.py",
                )
                self.assertIn(
                    f"- `tests/test_{name}.py` —",
                    document,
                    f"the embedded command document does not list tests/test_{name}.py",
                )

    def test_the_embedded_documents_match_the_repository_templates(self) -> None:
        """The templated documents must be byte identical to the repository copies.

        ``test_the_embedded_readme_*`` and ``test_the_embedded_changelog_*``
        only require that the embedded documents mention every module, so an
        edit to ``README.md`` or ``CHANGELOG.md`` that is not followed by
        ``make refresh-scaffold`` keeps passing them while the generator ships a
        stale document. Comparing the whole template is the check that catches
        such drift, so it lives in the test suite instead of depending on
        someone running the refresh tool after editing a document.
        """
        for relative in refresh_scaffold.TEMPLATED_COPIES:
            with self.subTest(document=relative):
                self.assertIn(
                    relative,
                    self.bodies,
                    f"scaffold.sh does not embed {relative}",
                )
                expected = refresh_scaffold.templated_body(relative)
                self.assertIsNotNone(
                    expected,
                    f"the refresh tool does not manage {relative}",
                )
                self.assertEqual(
                    self.bodies[relative][0],
                    expected,
                    f"the embedded {relative} is out of sync; run `make refresh-scaffold`",
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

    def test_no_dead_module_manifest_files_exist(self) -> None:
        """The repository must not carry a stale module manifest.

        ``have.txt`` and ``want.txt`` were once maintained by hand as an
        integrity gate, but nothing consumes them: no tool, test, Makefile,
        ``pyproject.toml``, pre-commit hook, or CI step reads them, so they
        drifted out of date (274 entries against 278 modules on disk) while
        prose still cited ``want.txt == have.txt`` as a live guarantee. A
        manifest that nothing enforces is dead weight, so the repository must
        not hold one.
        """
        manifests = sorted(path.name for path in ROOT.glob("*.txt") if path.is_file())
        self.assertEqual(
            manifests,
            [],
            f"dead module-manifest files present: {manifests}",
        )


if __name__ == "__main__":
    unittest.main()
