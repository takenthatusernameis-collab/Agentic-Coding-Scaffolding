"""Tests for zipimport_utils."""

import os
import py_compile
import tempfile
import unittest
import zipfile

from zipimport_utils import (
    ZipImportError,
    archive_names,
    find_spec,
    get_code,
    get_data,
    get_filename,
    get_source,
    invalidate_caches,
    is_package,
    zip_importer,
)

SOURCE = "VALUE = 42\n"
PACKAGE_SOURCE = ""


def build_archive(directory: str, name: str = "mod.zip") -> str:
    """Return the path of a Zip archive holding a module and a package."""
    archive = os.path.join(directory, name)
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("mod.py", SOURCE)
        handle.writestr("pkg/__init__.py", PACKAGE_SOURCE)
        handle.writestr("pkg/inner.py", SOURCE)
        handle.writestr("data.txt", "payload\n")
    return archive


def build_bytecode_archive(directory: str, name: str = "bytecode.zip") -> str:
    """Return the path of a Zip archive that holds a module as byte code only."""
    source = os.path.join(directory, "compiled.py")
    with open(source, "w", encoding="utf-8") as handle:
        handle.write(SOURCE)
    compiled = os.path.join(directory, "compiled.pyc")
    py_compile.compile(source, cfile=compiled, doraise=True)
    with open(compiled, "rb") as handle:
        payload = handle.read()
    archive = os.path.join(directory, name)
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("compiled.pyc", payload)
    return archive


class TestZipimporter(unittest.TestCase):
    """Verify the zipimporter constructor and the archive helpers."""

    def test_zip_importer_rejects_non_path(self):
        with self.assertRaises(TypeError):
            zip_importer(123)  # type: ignore[arg-type]

    def test_zip_importer_missing_archive_raises(self):
        with self.assertRaises(ZipImportError):
            zip_importer("/no/such/archive.zip")

    def test_zip_importer_opens_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            importer = zip_importer(archive)
            self.assertEqual(importer.archive, archive)

    def test_zip_importer_accepts_path_like(self):
        import pathlib

        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            importer = zip_importer(pathlib.Path(archive))
            self.assertEqual(importer.archive, archive)

    def test_archive_names_lists_members(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            names = archive_names(archive)
            self.assertEqual(
                names,
                ["data.txt", "mod.py", "pkg/__init__.py", "pkg/inner.py"],
            )

    def test_archive_names_rejects_non_path(self):
        with self.assertRaises(TypeError):
            archive_names(None)  # type: ignore[arg-type]

    def test_archive_names_rejects_non_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            broken = os.path.join(directory, "broken.zip")
            with open(broken, "w", encoding="utf-8") as handle:
                handle.write("not a zip file")
            with self.assertRaises(zipfile.BadZipFile):
                archive_names(broken)


class TestModuleLookups(unittest.TestCase):
    """Verify the helpers that read a module from an archive."""

    def test_get_source_returns_source(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            self.assertEqual(get_source(archive, "mod"), SOURCE)

    def test_get_source_of_package(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            self.assertEqual(get_source(archive, "pkg"), PACKAGE_SOURCE)

    def test_get_source_without_source_returns_none(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_bytecode_archive(directory)
            self.assertIsNone(get_source(archive, "compiled"))

    def test_get_source_missing_module_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            with self.assertRaises(ZipImportError):
                get_source(archive, "absent")

    def test_get_code_returns_code_object(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            code = get_code(archive, "mod")
            self.assertIn(42, code.co_consts)

    def test_get_filename_points_into_the_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            filename = get_filename(archive, "mod")
            self.assertTrue(filename.startswith(archive))
            self.assertTrue(filename.endswith("mod.py"))

    def test_is_package(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            self.assertTrue(is_package(archive, "pkg"))
            self.assertFalse(is_package(archive, "mod"))

    def test_get_data_returns_member_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            self.assertEqual(get_data(archive, "data.txt"), b"payload\n")

    def test_get_data_rejects_non_path(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            with self.assertRaises(TypeError):
                get_data(archive, 5)  # type: ignore[arg-type]

    def test_get_data_missing_member_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            with self.assertRaises(OSError):
                get_data(archive, "absent.txt")

    def test_find_spec_returns_spec(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            spec = find_spec(archive, "mod")
            self.assertIsNotNone(spec)
            assert spec is not None
            self.assertEqual(spec.name, "mod")

    def test_find_spec_missing_module_returns_none(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            self.assertIsNone(find_spec(archive, "absent"))


class TestValidation(unittest.TestCase):
    """Verify that every helper validates its arguments."""

    def test_fullname_must_be_a_string(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            with self.assertRaises(TypeError):
                get_source(archive, 5)  # type: ignore[arg-type]

    def test_fullname_must_not_be_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            with self.assertRaises(ValueError):
                get_source(archive, "")

    def test_fullname_must_be_a_dotted_module_name(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            with self.assertRaises(ValueError):
                get_source(archive, "not a name")


class TestInvalidateCaches(unittest.TestCase):
    """Verify the cache handling."""

    def test_invalidate_caches_clears_the_directory_cache(self):
        import zipimport

        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            zip_importer(archive)
            self.assertTrue(zipimport._zip_directory_cache)
            invalidate_caches()
            self.assertEqual(len(zipimport._zip_directory_cache), 0)

    def test_invalidate_caches_refreshes_a_single_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_archive(directory)
            importer = zip_importer(archive)
            self.assertNotIn("extra.py", importer._files)
            invalidate_caches(archive)
            self.assertNotIn("extra.py", importer._files)

    def test_invalidate_caches_rejects_non_path(self):
        with self.assertRaises(TypeError):
            invalidate_caches(5)  # type: ignore[arg-type]


class TestModuleContract(unittest.TestCase):
    """Verify the public interface of the module."""

    def test_all_is_sorted_and_unique(self):
        import zipimport_utils

        self.assertEqual(len(zipimport_utils.__all__), len(set(zipimport_utils.__all__)))
        self.assertEqual(zipimport_utils.__all__, sorted(zipimport_utils.__all__))
        for name in zipimport_utils.__all__:
            self.assertTrue(hasattr(zipimport_utils, name), name)

    def test_zip_import_error_is_the_standard_library_error(self):
        import zipimport

        self.assertIs(ZipImportError, zipimport.ZipImportError)


if __name__ == "__main__":
    unittest.main()
