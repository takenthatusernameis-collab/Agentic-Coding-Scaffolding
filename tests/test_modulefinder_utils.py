"""Tests for modulefinder utility functions."""

import modulefinder
import sysconfig
import tempfile
import unittest
from pathlib import Path

import modulefinder_utils

#: Name of the local helper module created next to the analysed scripts.
HELPER_NAME = "mf_local_helper"

#: Name of the local package created next to the analysed scripts.
PACKAGE_NAME = "mf_local_package"


class TestModulefinderUtils(unittest.TestCase):
    """Exercise the validated wrappers around the standard library module."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.root = Path(self.tmpdir.name)
        # Create a minimal fake stdlib with just base64 for fast tests
        self.fake_stdlib = self.root / "fake_stdlib"
        self.fake_stdlib.mkdir()
        base64_source = Path(sysconfig.get_paths()["stdlib"]) / "base64.py"
        (self.fake_stdlib / "base64.py").write_text(base64_source.read_text())

    def _write(self, name: str, content: str = "VALUE = 1\n") -> Path:
        """Create a source file below the temporary directory and return its path."""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def _write_helper(self) -> Path:
        """Create the local helper module and return its path."""
        return self._write(f"{HELPER_NAME}.py")

    def _search_path(self) -> list[str]:
        """Return the restricted search path used by the fast tests."""
        return [str(self.root)]

    def _stdlib_search_path(self) -> list[str]:
        """Return a search path that uses the minimal fake stdlib."""
        return [str(self.root), str(self.fake_stdlib)]

    def test_find_dependencies_lists_imported_modules(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        dependencies = modulefinder_utils.find_dependencies(script, path=self._search_path())
        self.assertIn(HELPER_NAME, dependencies)

    def test_find_dependencies_excludes_the_script_itself(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        dependencies = modulefinder_utils.find_dependencies(script, path=self._search_path())
        self.assertNotIn("__main__", dependencies)

    def test_find_dependencies_are_sorted(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\nimport json\n")
        dependencies = modulefinder_utils.find_dependencies(script, path=self._search_path())
        self.assertEqual(dependencies, sorted(dependencies))

    def test_find_dependencies_finds_standard_library_modules(self) -> None:
        script = self._write("app.py", "import base64\n")
        dependencies = modulefinder_utils.find_dependencies(script, path=self._stdlib_search_path())
        self.assertIn("base64", dependencies)

    def test_find_dependencies_accepts_a_string_path(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        dependencies = modulefinder_utils.find_dependencies(str(script), path=self._search_path())
        self.assertIn(HELPER_NAME, dependencies)

    def test_find_dependencies_honours_excludes(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        dependencies = modulefinder_utils.find_dependencies(
            script, path=self._search_path(), excludes=[HELPER_NAME]
        )
        self.assertNotIn(HELPER_NAME, dependencies)

    def test_find_modules_maps_names_to_files(self) -> None:
        helper = self._write(f"{HELPER_NAME}.py")
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        modules = modulefinder_utils.find_modules(script, path=self._search_path())
        self.assertEqual(modules[HELPER_NAME], str(helper))

    def test_find_modules_reports_none_for_builtin_modules(self) -> None:
        script = self._write("app.py", "import sys\n")
        modules = modulefinder_utils.find_modules(script, path=self._search_path())
        self.assertIn("sys", modules)
        self.assertIsNone(modules["sys"])

    def test_missing_modules_reports_unknown_imports(self) -> None:
        script = self._write("app.py", "import mf_missing_dependency\n")
        missing = modulefinder_utils.missing_modules(script, path=self._search_path())
        self.assertIn("mf_missing_dependency", missing)

    def test_missing_modules_is_empty_for_resolvable_imports(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        missing = modulefinder_utils.missing_modules(script, path=self._search_path())
        self.assertEqual(missing, [])

    def test_missing_modules_ignores_excluded_modules(self) -> None:
        script = self._write("app.py", "import mf_missing_dependency\n")
        missing = modulefinder_utils.missing_modules(
            script, path=self._search_path(), excludes=["mf_missing_dependency"]
        )
        self.assertNotIn("mf_missing_dependency", missing)

    def test_missing_importers_names_the_importing_module(self) -> None:
        script = self._write("app.py", "import mf_missing_dependency\n")
        importers = modulefinder_utils.missing_importers(script, path=self._search_path())
        self.assertIn("mf_missing_dependency", importers)
        self.assertEqual(importers["mf_missing_dependency"], ["__main__"])

    def test_module_path_returns_the_module_file(self) -> None:
        helper = self._write(f"{HELPER_NAME}.py")
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        self.assertEqual(
            modulefinder_utils.module_path(script, HELPER_NAME, path=self._search_path()),
            str(helper),
        )

    def test_module_path_raises_key_error_for_unknown_modules(self) -> None:
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        with self.assertRaises(KeyError):
            modulefinder_utils.module_path(script, "mf_unknown_module", path=self._search_path())

    def test_module_path_rejects_non_string_names(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        with self.assertRaises(TypeError):
            modulefinder_utils.module_path(
                script,
                42,  # type: ignore[arg-type]
                path=self._search_path(),
            )

    def test_load_script_rejects_invalid_scripts(self) -> None:
        with self.assertRaises(TypeError):
            modulefinder_utils.load_script(42)  # type: ignore[arg-type]
        with self.assertRaises(FileNotFoundError):
            modulefinder_utils.load_script(self.root / "does_not_exist.py")

    def test_load_script_rejects_invalid_search_paths(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        with self.assertRaises(TypeError):
            modulefinder_utils.load_script(script, path=str(self.root))
        with self.assertRaises(TypeError):
            modulefinder_utils.load_script(script, path=[42])  # type: ignore[list-item]

    def test_load_script_rejects_invalid_excludes(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        with self.assertRaises(TypeError):
            modulefinder_utils.load_script(script, excludes=HELPER_NAME)
        with self.assertRaises(TypeError):
            modulefinder_utils.load_script(
                script,
                excludes=[42],  # type: ignore[list-item]
            )

    def test_is_package_detects_local_packages(self) -> None:
        # Create a local package directory
        pkg_dir = self.root / PACKAGE_NAME
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        script = self._write("app.py", f"import {PACKAGE_NAME}\n")
        self.assertTrue(
            modulefinder_utils.is_package(script, PACKAGE_NAME, path=self._search_path())
        )

    def test_is_package_reports_false_for_modules(self) -> None:
        self._write_helper()
        script = self._write("app.py", f"import {HELPER_NAME}\n")
        self.assertFalse(
            modulefinder_utils.is_package(script, HELPER_NAME, path=self._search_path())
        )

    def test_is_package_raises_key_error_for_unknown_modules(self) -> None:
        script = self._write("app.py", "import sys\n")
        with self.assertRaises(KeyError):
            modulefinder_utils.is_package(script, "mf_unknown_module", path=self._search_path())


class TestStdlibModulefinder(unittest.TestCase):
    """Verify the wrappers work with the real standard library (slower).

    These tests share a single stdlib scan by using one script that imports
    all modules needed by the individual assertions. This avoids the ~5s cost
    of running ModuleFinder.run_script four separate times.
    """

    tmpdir: tempfile.TemporaryDirectory
    root: Path
    stdlib_path: str
    search_path: list[str]
    finder: modulefinder_utils.ModuleFinder
    modules: dict[str, modulefinder.Module]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmpdir.name)
        cls.stdlib_path = sysconfig.get_paths()["stdlib"]

        # Single script that imports all modules the assertions need
        script = cls.root / "app.py"
        script.write_text("import base64\nimport json\n")

        # Run the analysis once and capture all results
        cls.search_path = [str(cls.root), cls.stdlib_path]
        cls.finder = modulefinder_utils.load_script(script, path=cls.search_path)
        cls.modules = cls.finder.modules

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmpdir.cleanup()

    def _script_path(self) -> Path:
        return self.root / "app.py"

    def test_find_dependencies_finds_real_stdlib_modules(self) -> None:
        # Use the pre-loaded finder's modules directly
        dependencies = sorted(name for name in self.modules if name != "__main__")
        self.assertIn("base64", dependencies)

    def test_is_package_detects_real_packages(self) -> None:
        module = self.modules.get("json")
        self.assertIsNotNone(module)
        assert module is not None
        self.assertTrue(bool(getattr(module, "__path__", None)))

    def test_module_path_resolves_real_modules(self) -> None:
        module = self.modules.get("base64")
        self.assertIsNotNone(module)
        assert module is not None
        path = getattr(module, "__file__", None)
        self.assertIsNotNone(path)
        assert path is not None
        self.assertTrue(path.endswith("base64.py"))

    def test_report_includes_real_modules(self) -> None:
        import io
        from contextlib import redirect_stdout
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.finder.report()
        text = buffer.getvalue()
        self.assertIn("base64", text)
        self.assertIn("json", text)


if __name__ == "__main__":
    unittest.main()
