"""Tests for tempfile_utils module."""

import os
import unittest

from tempfile_utils import (
    NamedTemporaryFile,
    SpooledTemporaryFile,
    TemporaryDirectory,
    get_tempdir,
    gettempprefix,
    mkdtemp,
    mkstemp,
)


class TestGetTempdir(unittest.TestCase):
    def test_get_tempdir_returns_string(self):
        result = get_tempdir()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestGettempprefix(unittest.TestCase):
    def test_gettempprefix_returns_string(self):
        result = gettempprefix()
        self.assertIsInstance(result, str)


class TestMkstemp(unittest.TestCase):
    def test_mkstemp_creates_file(self):
        fd, path = mkstemp(suffix=".txt", prefix="test_")
        try:
            self.assertTrue(os.path.exists(path))
            os.close(fd)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_mkstemp_type_errors(self):
        with self.assertRaises(TypeError):
            mkstemp(suffix=123)
        with self.assertRaises(TypeError):
            mkstemp(prefix=123)
        with self.assertRaises(TypeError):
            mkstemp(dir=123)


class TestMkdtemp(unittest.TestCase):
    def test_mkdtemp_creates_directory(self):
        path = mkdtemp(suffix="_test", prefix="tmp_")
        try:
            self.assertTrue(os.path.isdir(path))
        finally:
            if os.path.exists(path):
                os.rmdir(path)

    def test_mkdtemp_type_errors(self):
        with self.assertRaises(TypeError):
            mkdtemp(suffix=123)


class TestNamedTemporaryFile(unittest.TestCase):
    def test_named_temporary_file_basic(self):
        with NamedTemporaryFile(mode="w", delete=True) as f:
            f.write("hello")
            f.flush()
            self.assertTrue(os.path.exists(f.name))

    def test_named_temporary_file_type_errors(self):
        with self.assertRaises(TypeError):
            NamedTemporaryFile(mode=123)
        with self.assertRaises(TypeError):
            NamedTemporaryFile(delete="yes")


class TestTemporaryDirectory(unittest.TestCase):
    def test_temporary_directory_basic(self):
        with TemporaryDirectory() as d:
            self.assertTrue(os.path.isdir(d))


class TestSpooledTemporaryFile(unittest.TestCase):
    def test_spooled_temporary_file_basic(self):
        with SpooledTemporaryFile(mode="w+b") as f:
            f.write(b"hello")
            f.seek(0)
            self.assertEqual(f.read(), b"hello")


if __name__ == "__main__":
    unittest.main()
