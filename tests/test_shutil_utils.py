"""Tests for shutil_utils module."""

import tempfile
import unittest
from pathlib import Path

from shutil_utils import (
    copy_file,
    copy_tree,
    disk_usage,
    make_archive,
    move,
    remove_tree,
    unpack_archive,
    which,
)


class TestShutilUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.src = Path(self.temp_dir) / "src"
        self.dst = Path(self.temp_dir) / "dst"
        self.src.mkdir()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_copy_file(self) -> None:
        (self.src / "a.txt").write_text("hello")
        result = copy_file(self.src / "a.txt", self.dst / "a.txt")
        self.assertTrue(Path(result).exists())
        self.assertEqual(Path(result).read_text(), "hello")

    def test_copy_tree(self) -> None:
        (self.src / "a.txt").write_text("hello")
        result = copy_tree(self.src, self.dst)
        self.assertTrue(Path(result).exists())
        self.assertTrue((self.dst / "a.txt").exists())

    def test_move(self) -> None:
        (self.src / "a.txt").write_text("hello")
        result = move(self.src / "a.txt", self.dst / "a.txt")
        self.assertTrue(Path(result).exists())
        self.assertFalse((self.src / "a.txt").exists())

    def test_remove_tree(self) -> None:
        d = Path(self.temp_dir) / "removeme"
        d.mkdir()
        (d / "f.txt").write_text("x")
        remove_tree(d)
        self.assertFalse(d.exists())

    def test_disk_usage(self) -> None:
        usage = disk_usage(self.temp_dir)
        self.assertTrue(hasattr(usage, "total"))

    def test_make_unpack_archive(self) -> None:
        (self.src / "a.txt").write_text("hello")
        base = Path(self.temp_dir) / "archive"
        path = make_archive(base, "zip", self.src)
        self.assertTrue(Path(path).exists())
        extract = Path(self.temp_dir) / "extracted"
        extract.mkdir()
        unpack_archive(path, extract)
        self.assertTrue((extract / "a.txt").exists())

    def test_which(self) -> None:
        self.assertIsNotNone(which("python3"))
        self.assertIsNone(which("definitely-not-a-command-xyz"))
