"""Tests for ntpath_utils."""

import ntpath
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import ntpath_utils
from ntpath_utils import (
    abspath,
    basename,
    commonpath,
    commonprefix,
    dirname,
    exists,
    expanduser,
    expandvars,
    getatime,
    getctime,
    getmtime,
    getsize,
    has_drive,
    is_device_path,
    is_unc_path,
    isabs,
    isdevdrive,
    isdir,
    isfile,
    isjunction,
    islink,
    ismount,
    join,
    lexists,
    normcase,
    normpath,
    realpath,
    relpath,
    samefile,
    sameopenfile,
    samestat,
    split,
    splitdrive,
    splitext,
    splitroot,
    to_backslashes,
    to_slashes,
)


class TestModuleContract(unittest.TestCase):
    """Test the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(ntpath_utils.__all__, sorted(set(ntpath_utils.__all__)))

    def test_every_name_exists(self):
        for name in ntpath_utils.__all__:
            self.assertTrue(hasattr(ntpath_utils, name), name)

    def test_the_constants_are_the_constants_of_the_standard_library(self):
        self.assertEqual(ntpath_utils.sep, ntpath.sep)
        self.assertEqual(ntpath_utils.altsep, ntpath.altsep)
        self.assertEqual(ntpath_utils.curdir, ntpath.curdir)
        self.assertEqual(ntpath_utils.pardir, ntpath.pardir)
        self.assertEqual(ntpath_utils.extsep, ntpath.extsep)
        self.assertEqual(ntpath_utils.pathsep, ntpath.pathsep)
        self.assertEqual(ntpath_utils.defpath, ntpath.defpath)
        self.assertEqual(ntpath_utils.devnull, ntpath.devnull)
        self.assertEqual(
            ntpath_utils.supports_unicode_filenames,
            ntpath.supports_unicode_filenames,
        )
        self.assertIs(ntpath_utils.ALLOW_MISSING, ntpath.ALLOW_MISSING)


class TestSplitting(unittest.TestCase):
    """Test the functions that split a path."""

    def test_split_returns_a_head_and_a_tail(self):
        self.assertEqual(split("C:\\Users\\Barney\\file.txt"), ("C:\\Users\\Barney", "file.txt"))

    def test_split_of_a_root_returns_an_empty_tail(self):
        self.assertEqual(split("C:\\"), ("C:\\", ""))

    def test_split_accepts_bytes(self):
        self.assertEqual(split(b"C:\\Users\\file.txt"), (b"C:\\Users", b"file.txt"))

    def test_split_accepts_a_path_like_object(self):
        self.assertEqual(split(Path("C:/Users")), ntpath.split("C:/Users"))

    def test_splitdrive_returns_the_drive(self):
        self.assertEqual(splitdrive("C:\\Users\\Barney"), ("C:", "\\Users\\Barney"))

    def test_splitdrive_of_a_relative_path_returns_an_empty_drive(self):
        self.assertEqual(splitdrive("Users\\Barney"), ("", "Users\\Barney"))

    def test_splitroot_returns_the_drive_the_root_and_the_tail(self):
        self.assertEqual(splitroot("C:/Users/Barney"), ("C:", "/", "Users/Barney"))

    def test_splitroot_of_a_share_returns_the_share_as_the_drive(self):
        self.assertEqual(splitroot("//server/share/"), ("//server/share", "/", ""))

    def test_splitroot_of_a_relative_path_returns_empty_parts(self):
        self.assertEqual(splitroot("Windows/notepad"), ("", "", "Windows/notepad"))

    def test_splitext_returns_the_extension(self):
        self.assertEqual(splitext("C:\\Users\\file.txt"), ("C:\\Users\\file", ".txt"))

    def test_splitext_of_a_file_without_an_extension(self):
        self.assertEqual(splitext("C:\\Users\\file"), ("C:\\Users\\file", ""))

    def test_dirname_returns_the_directory(self):
        self.assertEqual(dirname("C:\\Users\\Barney\\file.txt"), "C:\\Users\\Barney")

    def test_basename_returns_the_final_component(self):
        self.assertEqual(basename("C:\\Users\\Barney\\file.txt"), "file.txt")

    def test_the_splitting_functions_reject_an_invalid_type(self):
        with self.assertRaises(TypeError):
            split(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            splitdrive(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            splitext(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dirname(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            basename(123)  # type: ignore[arg-type]


class TestJoining(unittest.TestCase):
    """Test the function that joins the components of a path."""

    def test_join_inserts_a_backslash(self):
        self.assertEqual(join("C:\\Users", "Barney"), "C:\\Users\\Barney")

    def test_join_keeps_the_separator_that_is_there(self):
        self.assertEqual(join("C:/Users", "Barney"), "C:/Users\\Barney")

    def test_join_of_a_single_component(self):
        self.assertEqual(join("C:\\Users"), "C:\\Users")

    def test_join_accepts_bytes(self):
        self.assertEqual(join(b"C:\\Users", b"Barney"), b"C:\\Users\\Barney")

    def test_join_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            join(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            join("C:\\Users", 123)  # type: ignore[arg-type]


class TestNormalization(unittest.TestCase):
    """Test the functions that normalize a path."""

    def test_normpath_collapses_the_redundant_parts(self):
        self.assertEqual(normpath("A//B/./C"), "A\\B\\C")

    def test_normpath_resolves_the_parent_directory(self):
        self.assertEqual(normpath("A\\B\\..\\C"), "A\\C")

    def test_normcase_lowercases_the_path(self):
        self.assertEqual(normcase("C:/Foo/Bar"), "c:\\foo\\bar")

    def test_normcase_accepts_bytes(self):
        self.assertEqual(normcase(b"C:/Foo"), b"c:\\foo")

    def test_abspath_resolves_a_relative_path(self):
        self.assertEqual(abspath("file.txt"), ntpath.abspath("file.txt"))

    def test_abspath_keeps_an_absolute_path(self):
        self.assertEqual(abspath("C:\\Users"), "C:\\Users")

    def test_relpath_returns_the_path_relative_to_the_start(self):
        self.assertEqual(relpath("C:\\Users\\Barney\\file.txt", "C:\\Users"), "Barney\\file.txt")

    def test_relpath_of_the_same_path_returns_a_dot(self):
        self.assertEqual(relpath("C:\\Users", "C:\\Users"), ".")

    def test_relpath_rejects_paths_of_different_drives(self):
        with self.assertRaises(ValueError):
            relpath("C:\\Users", "D:\\Users")

    def test_relpath_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            relpath(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            relpath("C:\\Users", 123)  # type: ignore[arg-type]

    def test_commonpath_returns_the_shared_part(self):
        self.assertEqual(commonpath(["C:\\Users\\a", "C:\\Users\\b"]), "C:\\Users")

    def test_commonpath_of_a_single_path(self):
        self.assertEqual(commonpath(["C:\\Users"]), "C:\\Users")

    def test_commonpath_rejects_an_empty_sequence(self):
        with self.assertRaises(ValueError):
            commonpath([])

    def test_commonpath_rejects_a_sequence_of_different_drives(self):
        with self.assertRaises(ValueError):
            commonpath(["C:\\Users", "D:\\Users"])

    def test_commonpath_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            commonpath("C:\\Users")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            commonpath([123])  # type: ignore[list-item]

    def test_commonprefix_returns_the_shared_characters(self):
        self.assertEqual(commonprefix(["C:\\Users\\a", "C:\\Users\\b"]), "C:\\Users\\")

    def test_commonprefix_of_an_empty_sequence(self):
        self.assertEqual(commonprefix([]), "")

    def test_commonprefix_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            commonprefix(123)  # type: ignore[arg-type]

    def test_the_normalizing_functions_reject_an_invalid_type(self):
        with self.assertRaises(TypeError):
            normpath(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            normcase(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            abspath(123)  # type: ignore[arg-type]


class TestWindowsHelpers(unittest.TestCase):
    """Test the helpers that report the shape of a Windows path."""

    def test_has_drive_reports_a_drive_letter(self):
        self.assertTrue(has_drive("C:\\Users"))
        self.assertTrue(has_drive("C:Users"))

    def test_has_drive_reports_a_relative_path(self):
        self.assertFalse(has_drive("Users\\Barney"))

    def test_has_drive_reports_a_share(self):
        self.assertTrue(has_drive("\\\\server\\share\\file.txt"))

    def test_is_unc_path_reports_a_share(self):
        self.assertTrue(is_unc_path("\\\\server\\share\\file.txt"))

    def test_is_unc_path_reports_a_share_that_uses_forward_slashes(self):
        self.assertTrue(is_unc_path("//server/share/file.txt"))

    def test_is_unc_path_reports_a_drive_letter(self):
        self.assertFalse(is_unc_path("C:\\Users"))

    def test_is_device_path_reports_a_device(self):
        self.assertTrue(is_device_path("\\\\?\\C:\\Users"))
        self.assertTrue(is_device_path("\\\\.\\COM1"))

    def test_is_device_path_reports_a_drive_letter(self):
        self.assertFalse(is_device_path("C:\\Users"))

    def test_to_slashes_replaces_the_backslashes(self):
        self.assertEqual(to_slashes("C:\\Users\\Barney"), "C:/Users/Barney")

    def test_to_slashes_accepts_bytes(self):
        self.assertEqual(to_slashes(b"C:\\Users"), b"C:/Users")

    def test_to_backslashes_replaces_the_forward_slashes(self):
        self.assertEqual(to_backslashes("C:/Users/Barney"), "C:\\Users\\Barney")

    def test_the_helpers_reject_an_invalid_type(self):
        with self.assertRaises(TypeError):
            has_drive(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_unc_path(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_device_path(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            to_slashes(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            to_backslashes(123)  # type: ignore[arg-type]


class TestExpansion(unittest.TestCase):
    """Test the functions that expand a path."""

    def test_expanduser_replaces_the_tilde_with_the_profile(self):
        environment = {"USERPROFILE": "C:\\Users\\tester"}
        with mock.patch.dict(os.environ, environment, clear=False):
            self.assertEqual(expanduser("~/documents"), "C:\\Users\\tester/documents")

    def test_expanduser_keeps_a_path_without_a_tilde(self):
        self.assertEqual(expanduser("C:\\Users"), "C:\\Users")

    def test_expandvars_replaces_a_variable(self):
        environment = {"NTPATH_TEST_VARIABLE": "value"}
        with mock.patch.dict(os.environ, environment, clear=False):
            self.assertEqual(expandvars("$NTPATH_TEST_VARIABLE/file.txt"), "value/file.txt")

    def test_expandvars_keeps_an_unknown_variable(self):
        self.assertEqual(
            expandvars("$NTPATH_TEST_UNKNOWN_VARIABLE/file.txt"),
            "$NTPATH_TEST_UNKNOWN_VARIABLE/file.txt",
        )

    def test_the_expanding_functions_reject_an_invalid_type(self):
        with self.assertRaises(TypeError):
            expanduser(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            expandvars(123)  # type: ignore[arg-type]


class TestFileSystemHelpers(unittest.TestCase):
    """Test the helpers that look at the file system."""

    def test_exists_reports_an_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        try:
            self.assertTrue(exists(path))
        finally:
            os.unlink(path)

    def test_exists_reports_a_missing_file(self):
        self.assertFalse(exists(os.path.join(tempfile.gettempdir(), "ntpath-missing-file")))

    def test_isfile_and_isdir_report_the_kind_of_a_path(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(isdir(directory))
            self.assertFalse(isfile(directory))
            file_path = os.path.join(directory, "file.txt")
            with open(file_path, "w", encoding="utf-8") as handle:
                handle.write("hello")
            self.assertTrue(isfile(file_path))
            self.assertFalse(isdir(file_path))

    def test_islink_reports_a_regular_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        try:
            self.assertFalse(islink(path))
        finally:
            os.unlink(path)

    def test_lexists_reports_a_missing_file(self):
        self.assertFalse(lexists(os.path.join(tempfile.gettempdir(), "ntpath-missing-file")))

    def test_getsize_returns_the_size_of_a_file(self):
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as handle:
            handle.write("hello")
            path = handle.name
        try:
            self.assertEqual(getsize(path), 5)
        finally:
            os.unlink(path)

    def test_getmtime_and_getatime_and_getctime_return_a_number(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        try:
            self.assertIsInstance(getmtime(path), float)
            self.assertIsInstance(getatime(path), float)
            self.assertIsInstance(getctime(path), float)
        finally:
            os.unlink(path)

    def test_getsize_raises_for_a_missing_file(self):
        with self.assertRaises(OSError):
            getsize(os.path.join(tempfile.gettempdir(), "ntpath-missing-file"))

    def test_samefile_reports_the_same_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        try:
            self.assertTrue(samefile(path, path))
        finally:
            os.unlink(path)

    def test_samestat_reports_the_same_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        try:
            self.assertTrue(samestat(os.stat(path), os.stat(path)))
        finally:
            os.unlink(path)

    def test_sameopenfile_reports_the_same_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            path = handle.name
        try:
            with open(path, "r") as first, open(path, "r") as second:
                self.assertTrue(sameopenfile(first.fileno(), second.fileno()))
        finally:
            os.unlink(path)

    def test_sameopenfile_rejects_a_bool(self):
        with self.assertRaises(TypeError):
            sameopenfile(True, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sameopenfile(1, False)  # type: ignore[arg-type]

    def test_samestat_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            samestat("not a stat", os.stat("."))  # type: ignore[arg-type]

    def test_ismount_reports_the_root_of_a_drive(self):
        self.assertTrue(ismount("C:/"))

    def test_ismount_reports_a_directory_that_is_not_a_mount_point(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(ismount(directory))

    def test_isjunction_reports_a_directory_that_is_not_a_junction(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(isjunction(directory))

    def test_isdevdrive_answers_with_a_bool(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsInstance(isdevdrive(directory), bool)

    def test_realpath_returns_an_absolute_path(self):
        self.assertEqual(realpath("C:\\Users"), ntpath.realpath("C:\\Users"))

    def test_realpath_rejects_a_strict_argument_that_is_not_a_bool(self):
        with self.assertRaises(TypeError):
            realpath("C:\\Users", strict="yes")  # type: ignore[arg-type]

    def test_the_file_system_helpers_reject_an_invalid_type(self):
        with self.assertRaises(TypeError):
            exists(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isdir(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isfile(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            islink(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lexists(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            getsize(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            getmtime(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            getatime(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            getctime(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ismount(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isjunction(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isdevdrive(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            realpath(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            samefile(123, "C:\\Users")  # type: ignore[arg-type]


class TestIsAbs(unittest.TestCase):
    """Test the predicate that reports an absolute path."""

    def test_isabs_reports_a_drive(self):
        self.assertTrue(isabs("C:\\Users"))

    def test_isabs_reports_a_relative_path(self):
        self.assertFalse(isabs("Users\\Barney"))

    def test_isabs_rejects_an_invalid_type(self):
        with self.assertRaises(TypeError):
            isabs(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
