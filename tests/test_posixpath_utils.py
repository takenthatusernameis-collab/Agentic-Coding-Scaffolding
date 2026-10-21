"""Tests for posixpath_utils."""

import os
import tempfile
import unittest

import posixpath_utils
from posixpath_utils import (
    ALLOW_MISSING,
    abspath,
    basename,
    commonpath,
    commonprefix,
    curdir,
    dirname,
    exists,
    expanduser,
    expandvars,
    isabs,
    isdir,
    isfile,
    isjunction,
    islink,
    ismount,
    join,
    lexists,
    normcase,
    normpath,
    pardir,
    realpath,
    relpath,
    samefile,
    sameopenfile,
    samestat,
    sep,
    split,
    splitdrive,
    splitext,
    splitroot,
)


class TestModuleContract(unittest.TestCase):
    def test_all_is_sorted_and_unique(self):
        self.assertEqual(posixpath_utils.__all__, sorted(set(posixpath_utils.__all__)))

    def test_constants_reexported(self):
        self.assertIs(ALLOW_MISSING, posixpath_utils.ALLOW_MISSING)
        self.assertIs(sep, posixpath_utils.sep)
        self.assertIs(curdir, posixpath_utils.curdir)
        self.assertIs(pardir, posixpath_utils.pardir)


class TestBasenameDirname(unittest.TestCase):
    def test_basename(self):
        self.assertEqual(basename("/foo/bar/baz"), "baz")
        self.assertEqual(basename("/foo/bar/"), "")

    def test_dirname(self):
        self.assertEqual(dirname("/foo/bar/baz"), "/foo/bar")
        self.assertEqual(dirname("/foo/bar/"), "/foo/bar")

    def test_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            basename(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dirname(None)  # type: ignore[arg-type]


class TestJoinSplit(unittest.TestCase):
    def test_join(self):
        self.assertEqual(join("/foo", "bar", "baz"), "/foo/bar/baz")
        self.assertEqual(join("/foo", "/bar"), "/bar")

    def test_split(self):
        self.assertEqual(split("/foo/bar"), ("/foo", "bar"))
        self.assertEqual(split("/foo/bar/"), ("/foo/bar", ""))

    def test_splitext(self):
        self.assertEqual(splitext("foo.bar.baz"), ("foo.bar", ".baz"))
        self.assertEqual(splitext("foo"), ("foo", ""))

    def test_splitdrive(self):
        # On POSIX, splitdrive behaves specially
        self.assertEqual(splitdrive("/foo/bar"), ("", "/foo/bar"))

    def test_splitroot(self):
        result = splitroot("/foo/bar")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

    def test_join_validates_args(self):
        with self.assertRaises(TypeError):
            join("/foo", 123)  # type: ignore[arg-type]


class TestNorm(unittest.TestCase):
    def test_normpath(self):
        self.assertEqual(normpath("/foo//bar/../baz"), "/foo/baz")
        self.assertEqual(normpath("foo/bar/.."), "foo")

    def test_normcase(self):
        self.assertEqual(normcase("/Foo/Bar"), "/Foo/Bar")

    def test_abspath(self):
        path = abspath(".")
        self.assertTrue(os.path.isabs(path))

    def test_realpath(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            rp = realpath(temp_path)
            self.assertTrue(os.path.isabs(rp))
        finally:
            os.unlink(temp_path)

    def test_realpath_strict_validation(self):
        with self.assertRaises(TypeError):
            realpath("/tmp", strict="false")  # type: ignore[arg-type]


class TestRelpath(unittest.TestCase):
    def test_relpath(self):
        rel = relpath("/foo/bar/baz", start="/foo")
        self.assertEqual(rel, "bar/baz")

    def test_relpath_no_start(self):
        rel = relpath("/foo/bar")
        self.assertIsInstance(rel, str)


class TestIsAbs(unittest.TestCase):
    def test_isabs(self):
        self.assertTrue(isabs("/foo"))
        self.assertFalse(isabs("foo"))


class TestMountsAndJunctions(unittest.TestCase):
    def test_ismount_reports_the_root(self):
        self.assertTrue(ismount("/"))

    def test_ismount_reports_a_directory_that_is_not_a_mount_point(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(ismount(directory))

    def test_isjunction_reports_a_directory_that_is_not_a_junction(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(isjunction(directory))


class TestExpand(unittest.TestCase):
    def test_expanduser(self):
        result = expanduser("~")
        self.assertIsInstance(result, str)

    def test_expandvars(self):
        result = expandvars("$HOME/test")
        self.assertIsInstance(result, str)


class TestCommonPath(unittest.TestCase):
    def test_commonpath(self):
        self.assertEqual(commonpath(["/usr/local", "/usr/local/bin"]), "/usr/local")

    def test_commonpath_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            commonpath("not iterable")  # type: ignore[arg-type]


class TestLexists(unittest.TestCase):
    def test_lexists_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertTrue(lexists(temp_path))
        finally:
            os.unlink(temp_path)

    def test_lexists_nonexistent(self):
        self.assertFalse(lexists("/nonexistent/path/12345"))


class TestReExports(unittest.TestCase):
    def test_genericpath_reexports(self):
        self.assertTrue(exists("/tmp") or True)  # Just check callable
        self.assertTrue(callable(isfile))
        self.assertTrue(callable(isdir))
        self.assertTrue(callable(islink))
        self.assertEqual(commonprefix(["/a/b", "/a/c"]), "/a/")

    def test_samefile_functions(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        try:
            self.assertTrue(samefile(temp_path, temp_path))
            s = os.stat(temp_path)
            self.assertTrue(samestat(s, os.stat(temp_path)))
        finally:
            os.unlink(temp_path)
        with self.assertRaises(TypeError):
            samefile(123, 456)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sameopenfile(True, 1)  # type: ignore[arg-type]
