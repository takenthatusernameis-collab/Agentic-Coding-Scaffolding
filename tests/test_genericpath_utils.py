"""Tests for genericpath_utils."""

import os
import tempfile
import unittest

import genericpath_utils
from genericpath_utils import (
    ALLOW_MISSING,
    commonprefix,
    exists,
    getatime,
    getctime,
    getmtime,
    getsize,
    isdir,
    isfile,
    islink,
    samefile,
    sameopenfile,
    samestat,
)


class TestCommonPrefix(unittest.TestCase):
    """Test commonprefix function."""

    def test_commonprefix_of_empty_list(self):
        self.assertEqual(commonprefix([]), "")

    def test_commonprefix_of_single_item(self):
        self.assertEqual(commonprefix(["/usr/local/bin"]), "/usr/local/bin")

    def test_commonprefix_of_multiple_paths(self):
        self.assertEqual(commonprefix(["/usr/local/bin", "/usr/local/lib"]), "/usr/local/")

    def test_commonprefix_with_no_common_prefix(self):
        self.assertEqual(commonprefix(["/usr/bin", "/var/log"]), "/")

    def test_commonprefix_with_bytes(self):
        self.assertEqual(commonprefix([b"/usr/bin", b"/usr/local"]), b"/usr/")

    def test_commonprefix_rejects_non_sequence(self):
        with self.assertRaises(TypeError):
            commonprefix("/usr/bin")  # type: ignore[arg-type]

    def test_commonprefix_rejects_none(self):
        with self.assertRaises(TypeError):
            commonprefix(None)  # type: ignore[arg-type]


class TestExists(unittest.TestCase):
    """Test exists function."""

    def test_exists_returns_true_for_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertTrue(exists(temp_path))
        finally:
            os.unlink(temp_path)

    def test_exists_returns_false_for_nonexistent(self):
        self.assertFalse(exists("/nonexistent/path/to/file/12345"))

    def test_exists_with_path_like(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertTrue(exists(os.fspath(temp_path)))
        finally:
            os.unlink(temp_path)

    def test_exists_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            exists(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            exists(None)  # type: ignore[arg-type]


class TestFileTypeChecks(unittest.TestCase):
    """Test isfile, isdir, islink."""

    def test_isfile_returns_true_for_regular_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertTrue(isfile(temp_path))
            self.assertFalse(isdir(temp_path))
        finally:
            os.unlink(temp_path)

    def test_isdir_returns_true_for_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertTrue(isdir(temp_dir))
            self.assertFalse(isfile(temp_dir))

    def test_isfile_returns_false_for_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertFalse(isfile(temp_dir))

    def test_isdir_returns_false_for_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertFalse(isdir(temp_path))
        finally:
            os.unlink(temp_path)

    def test_islink_returns_false_for_regular_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertFalse(islink(temp_path))
        finally:
            os.unlink(temp_path)

    def test_isfile_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            isfile(123)  # type: ignore[arg-type]


class TestFileStats(unittest.TestCase):
    """Test getsize, getatime, getmtime, getctime."""

    def test_getsize_returns_file_size(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
            f.write("hello")
            temp_path = f.name
        try:
            self.assertEqual(getsize(temp_path), 5)
        finally:
            os.unlink(temp_path)

    def test_getmtime_returns_float(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            mtime = getmtime(temp_path)
            self.assertIsInstance(mtime, float)
        finally:
            os.unlink(temp_path)

    def test_getatime_returns_float(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            atime = getatime(temp_path)
            self.assertIsInstance(atime, float)
        finally:
            os.unlink(temp_path)

    def test_getctime_returns_float(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            ctime = getctime(temp_path)
            self.assertIsInstance(ctime, float)
        finally:
            os.unlink(temp_path)

    def test_getsize_raises_for_nonexistent(self):
        with self.assertRaises(OSError):
            getsize("/nonexistent/file/12345")


class TestSameFile(unittest.TestCase):
    """Test samefile, sameopenfile, samestat."""

    def test_samefile_returns_true_for_same_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertTrue(samefile(temp_path, temp_path))
        finally:
            os.unlink(temp_path)

    def test_samefile_returns_false_for_different_files(self):
        with tempfile.NamedTemporaryFile(delete=False) as f1:
            path1 = f1.name
        with tempfile.NamedTemporaryFile(delete=False) as f2:
            path2 = f2.name
        try:
            self.assertFalse(samefile(path1, path2))
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_samestat(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            s1 = os.stat(temp_path)
            s2 = os.stat(temp_path)
            self.assertTrue(samestat(s1, s2))
        finally:
            os.unlink(temp_path)

    def test_samestat_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            samestat("not a stat", os.stat("."))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            samestat(os.stat("."), 123)  # type: ignore[arg-type]

    def test_sameopenfile(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            with open(temp_path, 'r') as f1, open(temp_path, 'r') as f2:
                self.assertTrue(sameopenfile(f1.fileno(), f2.fileno()))
        finally:
            os.unlink(temp_path)

    def test_sameopenfile_rejects_bool(self):
        with self.assertRaises(TypeError):
            sameopenfile(True, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sameopenfile(1, False)  # type: ignore[arg-type]

    def test_sameopenfile_rejects_non_int(self):
        with self.assertRaises(TypeError):
            sameopenfile("1", 1)  # type: ignore[arg-type]


class TestModuleContract(unittest.TestCase):
    """Test module contract."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(genericpath_utils.__all__, sorted(set(genericpath_utils.__all__)))

    def test_allow_missing_is_reexported(self):
        self.assertIs(ALLOW_MISSING, genericpath_utils.ALLOW_MISSING)
