"""Unit tests for temp_utils module."""

import os
import unittest

from temp_utils import (
    TEMP_DIR,
    cleanup_temp_path,
    create_temp_dir,
    create_temp_file,
    is_temp_path,
    read_temp_file,
    temp_dir,
    temp_file,
    temp_path_exists,
    write_temp_file,
)


class TestConstants(unittest.TestCase):
    def test_temp_dir_is_string(self):
        self.assertIsInstance(TEMP_DIR, str)
        self.assertTrue(os.path.isdir(TEMP_DIR))


class TestCreateTempFile(unittest.TestCase):
    def test_creates_existing_file(self):
        path = create_temp_file(suffix=".txt", prefix="demo_")
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(path.endswith(".txt"))
        self.assertTrue(os.path.basename(path).startswith("demo_"))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_returns_absolute_path(self):
        path = create_temp_file()
        self.assertTrue(os.path.isabs(path))
        cleanup_temp_path(path)

    def test_custom_dir(self):
        with temp_dir() as parent:
            path = create_temp_file(dir=parent)
            self.assertTrue(os.path.dirname(path) == os.path.abspath(parent))
            cleanup_temp_path(path)

    def test_delete_false_keeps_file(self):
        path = create_temp_file(delete=False)
        self.assertTrue(os.path.exists(path))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            create_temp_file(suffix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(prefix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(dir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(text="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(delete="yes")  # type: ignore[arg-type]


class TestCreateTempDir(unittest.TestCase):
    def test_creates_existing_directory(self):
        path = create_temp_dir(suffix="_suf", prefix="demo_")
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.basename(path).startswith("demo_"))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_returns_absolute_path(self):
        path = create_temp_dir()
        self.assertTrue(os.path.isabs(path))
        cleanup_temp_path(path)

    def test_custom_dir(self):
        with temp_dir() as parent:
            path = create_temp_dir(dir=parent)
            self.assertTrue(os.path.dirname(path) == os.path.abspath(parent))
            cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            create_temp_dir(suffix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_dir(prefix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_dir(dir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_dir(delete="yes")  # type: ignore[arg-type]


class TestTempFileContextManager(unittest.TestCase):
    def test_removes_file_on_exit(self):
        path = None
        with temp_file(suffix=".log") as p:
            path = p
            self.assertTrue(os.path.isfile(path))
            with open(path, "w") as fh:
                fh.write("data")
        self.assertFalse(os.path.exists(path))

    def test_removes_file_on_exception(self):
        path = None
        try:
            with temp_file(suffix=".log") as p:
                path = p
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        self.assertFalse(os.path.exists(path))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            with temp_file(suffix=123):  # type: ignore[arg-type]
                pass


class TestTempDirContextManager(unittest.TestCase):
    def test_removes_directory_on_exit(self):
        path = None
        with temp_dir(prefix="tmpdir_") as p:
            path = p
            self.assertTrue(os.path.isdir(path))
        self.assertFalse(os.path.exists(path))

    def test_removes_directory_contents_on_exit(self):
        path = None
        with temp_dir() as p:
            path = p
            nested = os.path.join(p, "nested.txt")
            with open(nested, "w") as fh:
                fh.write("x")
        self.assertFalse(os.path.exists(path))

    def test_removes_directory_on_exception(self):
        path = None
        try:
            with temp_dir() as p:
                path = p
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        self.assertFalse(os.path.exists(path))


class TestWriteTempFile(unittest.TestCase):
    def test_writes_and_reads_content(self):
        path = write_temp_file("hello world", suffix=".txt")
        self.assertTrue(os.path.isfile(path))
        self.assertEqual(read_temp_file(path), "hello world")
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_delete_false_keeps_file(self):
        path = write_temp_file("keep me", delete=False)
        self.assertTrue(os.path.exists(path))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_custom_dir(self):
        with temp_dir() as parent:
            path = write_temp_file("x", dir=parent)
            self.assertTrue(os.path.dirname(path) == os.path.abspath(parent))
            cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            write_temp_file(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            write_temp_file("x", suffix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            write_temp_file("x", delete="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            write_temp_file("x", mode=123)  # type: ignore[arg-type]


class TestReadTempFile(unittest.TestCase):
    def test_reads_content(self):
        path = write_temp_file("reading me")
        self.assertEqual(read_temp_file(path), "reading me")
        cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            read_temp_file(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            read_temp_file("x", mode=123)  # type: ignore[arg-type]

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            read_temp_file(os.path.join(TEMP_DIR, "definitely_does_not_exist_12345"))


class TestCleanupTempPath(unittest.TestCase):
    def test_removes_file(self):
        path = create_temp_file(delete=False)
        self.assertTrue(cleanup_temp_path(path))
        self.assertFalse(os.path.exists(path))

    def test_removes_directory(self):
        path = create_temp_dir(delete=False)
        self.assertTrue(cleanup_temp_path(path))
        self.assertFalse(os.path.exists(path))

    def test_removes_directory_with_contents(self):
        path = create_temp_dir(delete=False)
        nested = os.path.join(path, "file.txt")
        with open(nested, "w") as fh:
            fh.write("x")
        self.assertTrue(cleanup_temp_path(path))
        self.assertFalse(os.path.exists(path))

    def test_missing_path_returns_false(self):
        missing = os.path.join(TEMP_DIR, "definitely_does_not_exist_67890")
        self.assertFalse(cleanup_temp_path(missing))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            cleanup_temp_path(123)  # type: ignore[arg-type]


class TestIsTempPath(unittest.TestCase):
    def test_temp_path_returns_true(self):
        self.assertTrue(is_temp_path(TEMP_DIR))
        path = create_temp_file(delete=False)
        try:
            self.assertTrue(is_temp_path(path))
        finally:
            cleanup_temp_path(path)

    def test_non_temp_path_returns_false(self):
        self.assertFalse(is_temp_path("/"))
        self.assertFalse(is_temp_path("/usr/bin"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_temp_path(123)  # type: ignore[arg-type]


class TestTempPathExists(unittest.TestCase):
    def test_existing_path_returns_true(self):
        path = create_temp_file(delete=False)
        try:
            self.assertTrue(temp_path_exists(path))
        finally:
            cleanup_temp_path(path)

    def test_missing_path_returns_false(self):
        missing = os.path.join(TEMP_DIR, "definitely_does_not_exist_abcde")
        self.assertFalse(temp_path_exists(missing))

    def test_directory_returns_true(self):
        path = create_temp_dir(delete=False)
        try:
            self.assertTrue(temp_path_exists(path))
        finally:
            cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            temp_path_exists(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
