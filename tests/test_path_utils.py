"""Tests for path_utils module."""

import os
import unittest
from pathlib import Path

from path_utils import (
    change_extension,
    ensure_extension,
    get_absolute_path,
    get_common_path,
    get_file_extension,
    get_file_name,
    get_file_stem,
    get_parent_dir,
    get_path_components,
    get_relative_path,
    is_absolute,
    join_path,
    normalize_path,
)


class TestPathJoin(unittest.TestCase):
    def test_join_basic(self) -> None:
        self.assertEqual(join_path("a", "b", "c"), os.path.join("a", "b", "c"))

    def test_join_absolute(self) -> None:
        self.assertEqual(join_path("/usr", "local", "bin"), "/usr/local/bin")

    def test_join_with_path_objects(self) -> None:
        result = join_path(Path("a"), Path("b"))
        self.assertEqual(result, os.path.join("a", "b"))


class TestNormalizePath(unittest.TestCase):
    def test_normalize_redundant_separators(self) -> None:
        self.assertEqual(normalize_path("a//b///c"), os.path.join("a", "b", "c"))

    def test_normalize_dot_segments(self) -> None:
        result = normalize_path("a/b/../c")
        self.assertEqual(result, os.path.join("a", "c"))

    def test_normalize_absolute(self) -> None:
        result = normalize_path("/usr/./local//bin")
        self.assertTrue(result.startswith("/usr/local"))


class TestGetAbsolutePath(unittest.TestCase):
    def test_absolute_returns_string(self) -> None:
        result = get_absolute_path("foo")
        self.assertIsInstance(result, str)
        self.assertTrue(Path(result).is_absolute())


class TestGetRelativePath(unittest.TestCase):
    def test_relative_basic(self) -> None:
        self.assertEqual(get_relative_path("/usr/local/bin", "/usr"), "local/bin")

    def test_relative_same(self) -> None:
        self.assertEqual(get_relative_path("/usr/local", "/usr/local"), ".")

    def test_relative_raises_when_not_relative(self) -> None:
        with self.assertRaises(ValueError):
            get_relative_path("/usr/local", "/var")


class TestGetParentDir(unittest.TestCase):
    def test_parent_of_file(self) -> None:
        self.assertEqual(get_parent_dir("/usr/local/bin/python"), "/usr/local/bin")

    def test_parent_of_single_component(self) -> None:
        self.assertEqual(get_parent_dir("file.txt"), ".")


class TestGetFileName(unittest.TestCase):
    def test_file_name(self) -> None:
        self.assertEqual(get_file_name("/usr/local/bin/python"), "python")

    def test_file_name_with_dots(self) -> None:
        self.assertEqual(get_file_name("archive.tar.gz"), "archive.tar.gz")


class TestGetFileStem(unittest.TestCase):
    def test_stem_simple(self) -> None:
        self.assertEqual(get_file_stem("/usr/local/script.py"), "script")

    def test_stem_multiple_dots(self) -> None:
        self.assertEqual(get_file_stem("archive.tar.gz"), "archive.tar")

    def test_stem_no_extension(self) -> None:
        self.assertEqual(get_file_stem("Makefile"), "Makefile")


class TestGetFileExtension(unittest.TestCase):
    def test_extension_simple(self) -> None:
        self.assertEqual(get_file_extension("script.py"), ".py")

    def test_extension_none(self) -> None:
        self.assertEqual(get_file_extension("Makefile"), "")

    def test_extension_last(self) -> None:
        self.assertEqual(get_file_extension("archive.tar.gz"), ".gz")


class TestChangeExtension(unittest.TestCase):
    def test_change_to_new(self) -> None:
        self.assertEqual(change_extension("script.py", ".txt"), "script.txt")

    def test_change_without_dot(self) -> None:
        self.assertEqual(change_extension("image.png", "jpg"), "image.jpg")

    def test_change_same_extension(self) -> None:
        self.assertEqual(change_extension("script.py", ".py"), "script.py")


class TestIsAbsolute(unittest.TestCase):
    def test_absolute(self) -> None:
        self.assertTrue(is_absolute("/usr/local/bin"))

    def test_relative(self) -> None:
        self.assertFalse(is_absolute("relative/path"))


class TestGetPathComponents(unittest.TestCase):
    def test_absolute_path_components(self) -> None:
        result = get_path_components("/usr/local/bin")
        self.assertEqual(result, [os.sep, "usr", "local", "bin"])

    def test_relative_path_components(self) -> None:
        result = get_path_components("a/b/c")
        self.assertEqual(result, ["a", "b", "c"])


class TestGetCommonPath(unittest.TestCase):
    def test_common_path(self) -> None:
        self.assertEqual(get_common_path("/a/b/c", "/a/b/d"), "/a/b")

    def test_common_path_relative(self) -> None:
        self.assertEqual(get_common_path("x/y/z", "x/y/w"), "x/y")

    def test_no_common_path(self) -> None:
        # Only the root separator is shared; that is still a valid common prefix.
        self.assertEqual(get_common_path("/a/b", "/c/d"), os.sep)

    def test_requires_two_paths(self) -> None:
        with self.assertRaises(ValueError):
            get_common_path("/a/b")

    def test_three_paths(self) -> None:
        self.assertEqual(get_common_path("/a/b/c", "/a/b/d", "/a/b/e"), "/a/b")


class TestEnsureExtension(unittest.TestCase):
    def test_already_has_extension(self) -> None:
        self.assertEqual(ensure_extension("script.py", ".py"), "script.py")

    def test_missing_extension_added(self) -> None:
        self.assertEqual(ensure_extension("script", ".py"), "script.py")

    def test_wrong_extension_appended(self) -> None:
        self.assertEqual(ensure_extension("image.png", ".py"), "image.png.py")

    def test_extension_without_dot(self) -> None:
        self.assertEqual(ensure_extension("script", "py"), "script.py")


class TestReturnTypes(unittest.TestCase):
    def test_all_return_strings(self) -> None:
        self.assertIsInstance(join_path("a", "b"), str)
        self.assertIsInstance(normalize_path("a/b"), str)
        self.assertIsInstance(get_absolute_path("a"), str)
        self.assertIsInstance(get_relative_path("a/b", "a"), str)
        self.assertIsInstance(get_parent_dir("a/b"), str)
        self.assertIsInstance(get_file_name("a/b.txt"), str)
        self.assertIsInstance(get_file_stem("a/b.txt"), str)
        self.assertIsInstance(get_file_extension("a/b.txt"), str)
        self.assertIsInstance(change_extension("a/b.txt", ".md"), str)
        self.assertIsInstance(is_absolute("/a"), bool)
        self.assertIsInstance(get_path_components("/a/b"), list)
        self.assertIsInstance(get_common_path("/a/b", "/a/c"), str)
        self.assertIsInstance(ensure_extension("a", ".txt"), str)


class TestPathUtilsBoundary(unittest.TestCase):
    """Boundary/TypeError coverage for every public path helper.

    Mirrors the validation convention established in ``file_utils``: every
    public function raises ``TypeError`` for non-str/non-Path arguments and
    ``ValueError`` for semantically invalid (but correctly typed) arguments,
    instead of letting the stdlib raise an opaque ``AttributeError`` or
    silently coerce the value.
    """

    def test_join_path_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            join_path(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            join_path("a", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            join_path(Path("a"), 5)  # type: ignore[arg-type]

    def test_normalize_path_type_error(self) -> None:
        with self.assertRaises(TypeError):
            normalize_path(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            normalize_path(None)  # type: ignore[arg-type]

    def test_get_absolute_path_type_error(self) -> None:
        with self.assertRaises(TypeError):
            get_absolute_path(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_absolute_path(123)  # type: ignore[arg-type]

    def test_get_relative_path_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            get_relative_path(None, "/usr")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_relative_path("/usr/local", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_relative_path("/usr/local/bin", 5)  # type: ignore[arg-type]

    def test_get_relative_path_not_relative(self) -> None:
        with self.assertRaises(ValueError):
            get_relative_path("/usr/local", "/var")

    def test_get_parent_dir_type_error(self) -> None:
        with self.assertRaises(TypeError):
            get_parent_dir(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_parent_dir(123)  # type: ignore[arg-type]

    def test_get_file_name_type_error(self) -> None:
        with self.assertRaises(TypeError):
            get_file_name(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_file_name(123)  # type: ignore[arg-type]

    def test_get_file_stem_type_error(self) -> None:
        with self.assertRaises(TypeError):
            get_file_stem(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_file_stem(123)  # type: ignore[arg-type]

    def test_get_file_extension_type_error(self) -> None:
        with self.assertRaises(TypeError):
            get_file_extension(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_file_extension(123)  # type: ignore[arg-type]

    def test_change_extension_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            change_extension(None, ".txt")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            change_extension("a.txt", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            change_extension("a.txt", 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            change_extension(123, ".txt")  # type: ignore[arg-type]

    def test_change_extension_empty_extension(self) -> None:
        with self.assertRaises(ValueError):
            change_extension("a.txt", "")

    def test_is_absolute_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_absolute(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_absolute(123)  # type: ignore[arg-type]

    def test_get_path_components_type_error(self) -> None:
        with self.assertRaises(TypeError):
            get_path_components(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_path_components(123)  # type: ignore[arg-type]

    def test_get_common_path_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            get_common_path(None, "/a/b")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_common_path("/a/b", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_common_path("/a/b", 5)  # type: ignore[arg-type]

    def test_get_common_path_requires_two_paths(self) -> None:
        with self.assertRaises(ValueError):
            get_common_path("/a/b")

    def test_ensure_extension_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            ensure_extension(None, ".txt")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ensure_extension("a.txt", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ensure_extension("a.txt", 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ensure_extension(123, ".txt")  # type: ignore[arg-type]

    def test_ensure_extension_empty_extension(self) -> None:
        with self.assertRaises(ValueError):
            ensure_extension("a", "")

    def test_path_objects_accepted(self) -> None:
        # Path objects must still be accepted everywhere str is documented.
        self.assertEqual(join_path(Path("a"), Path("b")), os.path.join("a", "b"))
        self.assertEqual(get_common_path(Path("/a/b"), Path("/a/c")), "/a")
        self.assertEqual(get_file_name(Path("/usr/local/bin/python")), "python")
        self.assertEqual(get_parent_dir(Path("file.txt")), ".")
        self.assertTrue(is_absolute(Path("/usr/local/bin")))


if __name__ == "__main__":
    unittest.main()
