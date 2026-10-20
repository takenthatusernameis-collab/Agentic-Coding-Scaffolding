"""Tests for compileall utility functions."""

import os
import py_compile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import compileall_utils


class TestCompileallUtils(unittest.TestCase):
    """Exercise the validated wrappers around the standard library module."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.root = Path(self.tmpdir.name)

    def _write(self, name: str, content: str = "x = 1\n") -> Path:
        """Create a source file below the temporary directory and return its path."""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_compile_file_creates_bytecode(self) -> None:
        source = self._write("module.py")
        self.assertTrue(compileall_utils.compile_file(source))
        self.assertTrue(compileall_utils.pyc_path(source).exists())

    def test_compile_file_accepts_str_path(self) -> None:
        source = self._write("module.py")
        self.assertTrue(compileall_utils.compile_file(str(source)))
        self.assertTrue(compileall_utils.pyc_path(source).exists())

    def test_compile_file_reports_failure(self) -> None:
        source = self._write("broken.py", "def (\n")
        self.assertFalse(compileall_utils.compile_file(source))

    def test_compile_file_with_force(self) -> None:
        source = self._write("module.py")
        self.assertTrue(compileall_utils.compile_file(source))
        self.assertTrue(compileall_utils.compile_file(source, force=True))

    def test_compile_file_with_invalidation_mode(self) -> None:
        source = self._write("module.py")
        self.assertTrue(
            compileall_utils.compile_file(source, invalidation_mode="checked-hash")
        )
        self.assertTrue(
            compileall_utils.compile_file(
                source, invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH
            )
        )

    def test_compile_file_with_rx(self) -> None:
        import re

        source = self._write("skip_me.py")
        self.assertTrue(compileall_utils.compile_file(source, rx=re.compile("skip_me")))
        self.assertFalse(compileall_utils.pyc_path(source).exists())

    def test_compile_file_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            compileall_utils.compile_file(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", ddir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", force="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", legacy="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", hardlink_dupes="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", rx="not-a-pattern")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", quiet=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_file("x.py", quiet=3)
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", optimize=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_file("x.py", optimize=5)
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", stripdir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", prependdir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", limit_sl_dest=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_file("x.py", invalidation_mode=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_file("x.py", invalidation_mode="bogus")

    def test_compile_dir_compiles_tree(self) -> None:
        self._write("pkg/module.py")
        self._write("pkg/nested/deep.py")
        self.assertTrue(compileall_utils.compile_dir(self.root))
        module_pyc = compileall_utils.pyc_path(self.root / "pkg" / "module.py")
        deep_pyc = compileall_utils.pyc_path(self.root / "pkg" / "nested" / "deep.py")
        self.assertTrue(module_pyc.exists())
        self.assertTrue(deep_pyc.exists())

    def test_compile_dir_with_maxlevels(self) -> None:
        self._write("pkg/module.py")
        self._write("pkg/nested/deep.py")
        self.assertTrue(compileall_utils.compile_dir(self.root, maxlevels=1))
        deep_pyc = compileall_utils.pyc_path(self.root / "pkg" / "nested" / "deep.py")
        self.assertFalse(deep_pyc.exists())

    def test_compile_dir_with_workers(self) -> None:
        self._write("module.py")
        self.assertTrue(compileall_utils.compile_dir(self.root, workers=2))

    def test_compile_dir_reports_failure(self) -> None:
        self._write("broken.py", "def (\n")
        self.assertFalse(compileall_utils.compile_dir(self.root))

    def test_compile_dir_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, maxlevels="1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_dir(self.root, maxlevels=-1)
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, workers=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_dir(self.root, workers=0)
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, ddir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, force="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, legacy="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, hardlink_dupes="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, rx=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, quiet=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_dir(self.root, quiet=3)
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, optimize=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_dir(self.root, optimize=5)
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, stripdir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, prependdir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, limit_sl_dest=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_dir(self.root, invalidation_mode=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_dir(self.root, invalidation_mode="bogus")

    def test_compile_path_uses_sys_path(self) -> None:
        source = self._write("module.py")
        with mock.patch.object(compileall_utils.sys, "path", [str(self.root)]):
            self.assertTrue(compileall_utils.compile_path())
        self.assertTrue(compileall_utils.pyc_path(source).exists())

    def test_compile_path_reports_failure(self) -> None:
        self._write("broken.py", "def (\n")
        with mock.patch.object(compileall_utils.sys, "path", [str(self.root)]):
            self.assertFalse(compileall_utils.compile_path())

    def test_compile_path_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(skip_curdir="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(maxlevels="0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_path(maxlevels=-1)
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(force="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(legacy="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(quiet=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_path(quiet=3)
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(optimize=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_path(optimize=5)
        with self.assertRaises(TypeError):
            compileall_utils.compile_path(invalidation_mode=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compileall_utils.compile_path(invalidation_mode="bogus")

    def test_main_returns_zero_on_success(self) -> None:
        source = self._write("module.py")
        self.assertEqual(compileall_utils.main([str(source)]), 0)
        self.assertTrue(compileall_utils.pyc_path(source).exists())

    def test_main_returns_one_on_failure(self) -> None:
        source = self._write("broken.py", "def (\n")
        self.assertEqual(compileall_utils.main([str(source)]), 1)

    def test_main_restores_sys_argv(self) -> None:
        source = self._write("module.py")
        original = list(compileall_utils.sys.argv)
        compileall_utils.main([str(source)])
        self.assertEqual(compileall_utils.sys.argv, original)

    def test_main_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            compileall_utils.main("not-a-list")  # type: ignore[arg-type]

    def test_pyc_path(self) -> None:
        source = self.root / "module.py"
        expected = self.root / "__pycache__" / "module.cpython-312.pyc"
        self.assertEqual(compileall_utils.pyc_path(source).name, expected.name)
        self.assertEqual(compileall_utils.pyc_path(source).parent, expected.parent)
        self.assertEqual(compileall_utils.pyc_path(str(source)), expected)

    def test_pyc_path_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            compileall_utils.pyc_path(123)  # type: ignore[arg-type]

    def test_module_exports(self) -> None:
        for name in ("compile_dir", "compile_file", "compile_path", "main", "pyc_path"):
            self.assertIn(name, compileall_utils.__all__)
            self.assertTrue(hasattr(compileall_utils, name))

    def test_does_not_write_into_repository_root(self) -> None:
        """The helpers must never leave artefacts in the current directory."""
        before = set(os.listdir("."))
        source = self._write("module.py")
        compileall_utils.compile_file(source)
        compileall_utils.compile_dir(self.root)
        self.assertEqual(before, set(os.listdir(".")))


if __name__ == "__main__":
    unittest.main()
