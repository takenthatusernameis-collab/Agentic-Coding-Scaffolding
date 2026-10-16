"""Tests for io_utils module."""

import tempfile
import unittest
from pathlib import Path

from io_utils import (
    append_text,
    atomic_write_text,
    count_lines,
    iter_lines,
    read_lines,
    stream_copy,
    write_lines,
)


class TestReadWriteLines(unittest.TestCase):
    def test_write_and_read_lines(self):
        lines = ["alpha", "beta", "gamma"]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            path = f.name
        try:
            write_lines(path, lines)
            self.assertEqual(read_lines(path), lines)
        finally:
            Path(path).unlink()

    def test_write_lines_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "nested" / "lines.txt"
            write_lines(path, ["a", "b"])
            self.assertTrue(path.exists())
            self.assertEqual(read_lines(path), ["a", "b"])

    def test_write_lines_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(TypeError):
                write_lines(path, ["ok", 1])
        finally:
            Path(path).unlink()

    def test_append_text(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("first\n")
            path = f.name
        try:
            append_text(path, "second\n")
            self.assertEqual(read_lines(path), ["first", "second"])
        finally:
            Path(path).unlink()

    def test_append_text_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "new.txt"
            append_text(path, "hello\n")
            self.assertEqual(read_lines(path), ["hello"])

    def test_append_text_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(TypeError):
                append_text(path, 123)
        finally:
            Path(path).unlink()


class TestAtomicWriteText(unittest.TestCase):
    def test_atomic_write_roundtrip(self):
        content = "atomic content"
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            atomic_write_text(path, content)
            self.assertEqual(Path(path).read_text(encoding="utf-8"), content)
            siblings = list(Path(path).parent.glob(Path(path).name + ".*.tmp"))
            self.assertEqual(siblings, [])
        finally:
            Path(path).unlink()

    def test_atomic_write_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "nested" / "atomic.txt"
            atomic_write_text(path, "data")
            self.assertTrue(path.exists())
            self.assertEqual(path.read_text(encoding="utf-8"), "data")

    def test_atomic_write_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(TypeError):
                atomic_write_text(path, 123)
        finally:
            Path(path).unlink()


class TestStreamCopy(unittest.TestCase):
    def test_stream_copy(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            src = Path(tmp_dir) / "src.bin"
            dst = Path(tmp_dir) / "dst.bin"
            data = bytes(range(256)) * 4
            src.write_bytes(data)
            copied = stream_copy(src, dst)
            self.assertEqual(copied, len(data))
            self.assertEqual(dst.read_bytes(), data)

    def test_stream_copy_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            src = Path(tmp_dir) / "src.bin"
            dst = Path(tmp_dir) / "nested" / "dst.bin"
            src.write_bytes(b"hello")
            stream_copy(src, dst)
            self.assertTrue(dst.exists())
            self.assertEqual(dst.read_bytes(), b"hello")


class TestCountLines(unittest.TestCase):
    def test_count_lines(self):
        content = "one\ntwo\nthree\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            self.assertEqual(count_lines(path), 3)
        finally:
            Path(path).unlink()

    def test_count_lines_no_trailing_newline(self):
        content = "one\ntwo\nthree"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            self.assertEqual(count_lines(path), 3)
        finally:
            Path(path).unlink()


class TestIterLines(unittest.TestCase):
    def test_iter_lines(self):
        lines = ["x", "y", "z"]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("\n".join(lines))
            path = f.name
        try:
            self.assertEqual(list(iter_lines(path)), lines)
        finally:
            Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
