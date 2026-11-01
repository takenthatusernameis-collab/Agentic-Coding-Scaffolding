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


class TestFileUtilsBoundary(unittest.TestCase):
    """Boundary and TypeError coverage for file_utils."""

    def setUp(self) -> None:
        import tempfile

        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_read_text_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_text(Path(self.temp_dir) / "missing.txt")

    def test_read_text_directory_raises(self) -> None:
        with self.assertRaises((IsADirectoryError, OSError)):
            read_text(self.temp_dir)

    def test_read_text_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            read_text(123)  # type: ignore[arg-type]

    def test_write_text_creates_nested_path(self) -> None:
        nested = Path(self.temp_dir) / "a" / "b" / "c.txt"
        write_text(nested, "deep")
        self.assertEqual(nested.read_text(), "deep")

    def test_write_text_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            write_text(123, "x")  # type: ignore[arg-type]

    def test_read_json_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_json(Path(self.temp_dir) / "missing.json")

    def test_read_json_invalid_json(self) -> None:
        import json

        bad = Path(self.temp_dir) / "bad.json"
        bad.write_text("{not json")
        with self.assertRaises(json.JSONDecodeError):
            read_json(bad)

    def test_read_json_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            read_json(123)  # type: ignore[arg-type]

    def test_write_json_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            write_json(123, {})  # type: ignore[arg-type]

    def test_write_json_round_trip(self) -> None:
        path = Path(self.temp_dir) / "data.json"
        data = {"unicode": "héllo", "list": [1, 2, 3]}
        write_json(path, data)
        self.assertEqual(read_json(path), data)

    def test_ensure_dir_existing(self) -> None:
        result = ensure_dir(self.temp_dir)
        self.assertEqual(result, Path(self.temp_dir))

    def test_ensure_dir_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            ensure_dir(123)  # type: ignore[arg-type]

    def test_list_files_missing_dir(self) -> None:
        with self.assertRaises(FileNotFoundError):
            list_files(Path(self.temp_dir) / "nope")

    def test_list_files_not_a_dir(self) -> None:
        file_path = Path(self.temp_dir) / "file.txt"
        file_path.write_text("x")
        with self.assertRaises(ValueError):
            list_files(file_path)

    def test_list_files_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            list_files(123)  # type: ignore[arg-type]

    def test_list_files_pattern_recursive(self) -> None:
        root = Path(self.temp_dir)
        (root / "a.txt").write_text("1")
        (root / "sub").mkdir()
        (root / "sub" / "b.txt").write_text("2")
        (root / "sub" / "c.py").write_text("3")

        self.assertEqual(len(list_files(root, recursive=True)), 3)
        self.assertEqual(len(list_files(root, "*.txt", recursive=True)), 2)
        self.assertEqual(len(list_files(root, "*.py", recursive=True)), 1)
        self.assertEqual(len(list_files(root, "*.py")), 0)

    def test_list_files_empty_dir(self) -> None:
        self.assertEqual(list_files(self.temp_dir), [])

    def test_copy_file_missing_src(self) -> None:
        with self.assertRaises(FileNotFoundError):
            copy_file(Path(self.temp_dir) / "missing.txt", "dst.txt")

    def test_copy_file_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            copy_file(123, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            copy_file("x", 123)  # type: ignore[arg-type]

    def test_copy_file_overwrites(self) -> None:
        src = Path(self.temp_dir) / "src.txt"
        dst = Path(self.temp_dir) / "dst.txt"
        src.write_text("original")
        copy_file(src, dst)
        dst.write_text("changed")
        copy_file(src, dst)
        self.assertEqual(dst.read_text(), "original")

    def test_delete_file_non_string_raises_typeerror(self) -> None:
        with self.assertRaises(TypeError):
            delete_file(123)  # type: ignore[arg-type]

    def test_delete_file_directory_is_noop(self) -> None:
        # delete_file only unlinks regular files; directories are left alone.
        sub = Path(self.temp_dir) / "subdir"
        sub.mkdir()
        delete_file(sub)
        self.assertTrue(sub.exists())


if __name__ == "__main__":
    unittest.main()
