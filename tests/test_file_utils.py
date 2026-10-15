"""Tests for file_utils module."""

import tempfile
import unittest
from pathlib import Path

from file_utils import (
    copy_file,
    delete_file,
    ensure_dir,
    list_files,
    read_json,
    read_text,
    write_json,
    write_text,
)


class TestFileUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_read_write_text(self) -> None:
        file_path = Path(self.temp_dir) / "test.txt"
        content = "Hello, World!"
        write_text(file_path, content)
        self.assertTrue(file_path.exists())
        self.assertEqual(read_text(file_path), content)

    def test_read_write_json(self) -> None:
        file_path = Path(self.temp_dir) / "test.json"
        data = {"name": "test", "value": 42}
        write_json(file_path, data)
        self.assertTrue(file_path.exists())
        result = read_json(file_path)
        self.assertEqual(result, data)

    def test_ensure_dir(self) -> None:
        dir_path = Path(self.temp_dir) / "nested" / "dir"
        result = ensure_dir(dir_path)
        self.assertTrue(dir_path.exists())
        self.assertTrue(dir_path.is_dir())
        self.assertEqual(result, dir_path)

    def test_list_files(self) -> None:
        temp_path = Path(self.temp_dir)
        (temp_path / "file1.txt").write_text("1")
        (temp_path / "file2.py").write_text("2")
        (temp_path / "subdir").mkdir()
        (temp_path / "subdir" / "file3.txt").write_text("3")

        files = list_files(temp_path)
        self.assertEqual(len(files), 2)

        txt_files = list_files(temp_path, pattern="*.txt")
        self.assertEqual(len(txt_files), 1)

        all_files = list_files(temp_path, recursive=True)
        self.assertEqual(len(all_files), 3)

    def test_copy_file(self) -> None:
        src = Path(self.temp_dir) / "src.txt"
        dst = Path(self.temp_dir) / "copy" / "dst.txt"
        src.write_text("hello")
        copy_file(src, dst)
        self.assertTrue(dst.exists())
        self.assertEqual(dst.read_text(), "hello")

    def test_delete_file(self) -> None:
        file_path = Path(self.temp_dir) / "to_delete.txt"
        file_path.write_text("delete me")
        self.assertTrue(file_path.exists())
        delete_file(file_path)
        self.assertFalse(file_path.exists())
        # Should not raise when deleting non-existent file
        delete_file(file_path)


if __name__ == "__main__":
    unittest.main()
