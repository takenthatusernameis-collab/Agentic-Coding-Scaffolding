"""Tests for tempfile_utils module."""

import os
import unittest
from pathlib import Path

from tempfile_utils import (
    NamedTemporaryFile,
    SpooledTemporaryFile,
    TemporaryDirectory,
    TemporaryFile,
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


class TestTemporaryFile(unittest.TestCase):
    def test_temporary_file_basic(self):
        with TemporaryFile(mode="w+b") as f:
            f.write(b"hello")
            f.seek(0)
            self.assertEqual(f.read(), b"hello")

    def test_temporary_file_text_mode(self):
        with TemporaryFile(mode="w+") as f:
            f.write("hello")
            f.flush()
            f.seek(0)
            self.assertEqual(f.read(), "hello")

    def test_temporary_file_type_errors_all(self):
        cases = [
            ("mode", 123), ("buffering", "x"), ("buffering", True),
            ("encoding", 123), ("newline", 123), ("suffix", 123),
            ("prefix", 123), ("dir", 123),
        ]
        for name, val in cases:
            with self.assertRaises(TypeError):
                TemporaryFile(**{name: val})


class TestTempfileBoundary(unittest.TestCase):
    def test_mkstemp_path_acceptance(self):
        fd, path = mkstemp(suffix=Path(".txt"), prefix=Path("t_"), dir=Path("/tmp"))
        os.close(fd)
        os.unlink(path)

    def test_mkstemp_path_acceptance_suffix_empty_str(self):
        fd, path = mkstemp(suffix="", prefix=Path("t_"), dir=Path("/tmp"))
        os.close(fd)
        os.unlink(path)

    def test_mkstemp_type_errors_all(self):
        for kw in ({"suffix": 1}, {"prefix": 1}, {"dir": 1}):
            with self.assertRaises(TypeError):
                mkstemp(**kw)

    def test_mkdtemp_type_errors_all(self):
        for kw in ({"suffix": 1}, {"prefix": 1}, {"dir": 1}):
            with self.assertRaises(TypeError):
                mkdtemp(**kw)

    def test_named_temporary_file_type_errors_all(self):
        cases = [
            ("mode", 123), ("buffering", "x"), ("buffering", True),
            ("encoding", 123), ("newline", 123), ("suffix", 123),
            ("prefix", 123), ("dir", 123), ("delete", "yes"),
        ]
        for name, val in cases:
            with self.assertRaises(TypeError):
                NamedTemporaryFile(**{name: val})

    def test_temporary_directory_type_errors_all(self):
        for kw in ({"suffix": 1}, {"prefix": 1}, {"dir": 1}, {"ignore_cleanup_errors": "x"}):
            with self.assertRaises(TypeError):
                TemporaryDirectory(**kw)

    def test_spooled_temporary_file_type_errors_all(self):
        cases = [
            ("max_size", "x"), ("max_size", True), ("mode", 123),
            ("buffering", "x"), ("buffering", True), ("encoding", 123),
            ("newline", 123), ("suffix", 123), ("prefix", 123), ("dir", 123),
        ]
        for name, val in cases:
            with self.assertRaises(TypeError):
                SpooledTemporaryFile(**{name: val})

    def test_empty_and_none_prefixes(self):
        fd, path = mkstemp(suffix="", prefix=None)
        os.close(fd)
        os.unlink(path)
        d = mkdtemp(suffix="", prefix=None)
        os.rmdir(d)

    def test_path_acceptance_all(self):
        with NamedTemporaryFile(dir=Path("/tmp")) as f:
            self.assertTrue(os.path.exists(f.name))
        with TemporaryDirectory(dir=Path("/tmp")) as d:
            self.assertTrue(os.path.isdir(d))
        with SpooledTemporaryFile(dir=Path("/tmp")) as f:
            f.write(b"x")


if __name__ == "__main__":
    unittest.main()
