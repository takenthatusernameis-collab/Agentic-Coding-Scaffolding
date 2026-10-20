"""Tests for py_compile utility functions."""

import os
import tempfile
from unittest import TestCase
from unittest import mock

import py_compile
import py_compile_utils


class TestPyCompileUtils(TestCase):
    def test_reexports(self):
        self.assertTrue(hasattr(py_compile_utils, "PyCompileError"))
        self.assertTrue(issubclass(py_compile_utils.PyCompileError, Exception))
        self.assertTrue(hasattr(py_compile_utils, "PycInvalidationMode"))
        self.assertIs(
            py_compile_utils.PycInvalidationMode,
            py_compile.PycInvalidationMode,
        )

    def test_parse_invalidation_mode(self):
        self.assertEqual(
            py_compile_utils.parse_invalidation_mode(None),
            py_compile.PycInvalidationMode.TIMESTAMP,
        )
        self.assertEqual(
            py_compile_utils.parse_invalidation_mode("timestamp"),
            py_compile.PycInvalidationMode.TIMESTAMP,
        )
        self.assertEqual(
            py_compile_utils.parse_invalidation_mode("CHECKED_HASH"),
            py_compile.PycInvalidationMode.CHECKED_HASH,
        )
        self.assertEqual(
            py_compile_utils.parse_invalidation_mode(py_compile.PycInvalidationMode.UNCHECKED_HASH),
            py_compile.PycInvalidationMode.UNCHECKED_HASH,
        )

    def test_parse_invalidation_mode_invalid(self):
        with self.assertRaises(ValueError):
            py_compile_utils.parse_invalidation_mode("bogus")
        with self.assertRaises(TypeError):
            py_compile_utils.parse_invalidation_mode(123)

    def test_get_invalidation_mode_default(self):
        with mock.patch("py_compile._get_default_invalidation_mode") as patched:
            patched.return_value = py_compile.PycInvalidationMode.CHECKED_HASH
            self.assertEqual(
                py_compile_utils.get_invalidation_mode(),
                py_compile.PycInvalidationMode.CHECKED_HASH,
            )

    def test_compile_file_and_pyc_alias(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "module.py")
            with open(src, "w") as f:
                f.write("x = 1\n")
            pyc = py_compile_utils.compile_file(src)
            self.assertTrue(os.path.exists(pyc))
            self.assertTrue(str(pyc).endswith(".pyc"))

    def test_py_compile_file_alias(self):
        self.assertIs(py_compile_utils.py_compile_file, py_compile_utils.compile_file)

    def test_compile_file_with_doraise(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "bad.py")
            with open(src, "w") as f:
                f.write("def (\n")
            with self.assertRaises(py_compile_utils.PyCompileError):
                py_compile_utils.compile_file(src, doraise=True)

    def test_compile_file_validates_inputs(self):
        with self.assertRaises(TypeError):
            py_compile_utils.compile_file(123)
        with self.assertRaises(TypeError):
            py_compile_utils.compile_file("x.py", doraise="yes")
        with self.assertRaises(TypeError):
            py_compile_utils.compile_file("x.py", optimize=True)
        with self.assertRaises(ValueError):
            py_compile_utils.compile_file("x.py", optimize=5)
        with self.assertRaises(TypeError):
            py_compile_utils.compile_file("x.py", quiet=True)
        with self.assertRaises(ValueError):
            py_compile_utils.compile_file("x.py", quiet=3)
        with self.assertRaises(TypeError):
            py_compile_utils.compile_file("x.py", cfile=123)
        with self.assertRaises(TypeError):
            py_compile_utils.compile_file("x.py", dfile=123)

    def test_is_pyc_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertTrue(py_compile_utils.is_pyc_file(os.path.join(tmpdir, "module.cpython-310.pyc")))
            self.assertTrue(py_compile_utils.is_pyc_file(os.path.join(tmpdir, "module.pyc")))
            self.assertFalse(py_compile_utils.is_pyc_file(os.path.join(tmpdir, "module.py")))
            self.assertFalse(py_compile_utils.is_pyc_file(os.path.join(tmpdir, "module.txt")))
            self.assertFalse(py_compile_utils.is_pyc_file(os.path.join(tmpdir, ".pyc")))
            self.assertFalse(py_compile_utils.is_pyc_file(123))

    def test_main(self):
        with mock.patch("py_compile.main", return_value=0) as patched:
            self.assertEqual(py_compile_utils.main(["-v"]), 0)
            patched.assert_called_once()