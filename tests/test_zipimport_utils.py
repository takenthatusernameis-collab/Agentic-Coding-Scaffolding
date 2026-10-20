"""Tests for zipimport_utils."""

import tempfile
import unittest
import zipfile

from zipimport_utils import ZipImportError, invalidate_caches, zip_importer


class TestZipimportUtils(unittest.TestCase):
    def test_zip_importer_rejects_non_path(self):
        with self.assertRaises(TypeError):
            zip_importer(123)  # type: ignore[arg-type]

    def test_zip_importer_missing_archive_raises(self):
        with self.assertRaises(ZipImportError):
            zip_importer("/no/such/archive.zip")

    def test_zip_importer_opens_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = tmp + "/mod.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("m.py", "VALUE = 42\n")
            zi = zip_importer(archive)
            self.assertIsNotNone(zi)

    def test_invalidate_caches_clears(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = tmp + "/mod.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("m.py", "VALUE = 42\n")
            zip_importer(archive)
            invalidate_caches()
            import zipimport
            self.assertEqual(len(zipimport._zip_directory_cache), 0)

    def test_all_is_sorted_and_unique(self):
        import zipimport_utils

        self.assertEqual(len(zipimport_utils.__all__), len(set(zipimport_utils.__all__)))
        self.assertEqual(zipimport_utils.__all__, sorted(zipimport_utils.__all__))
        for name in zipimport_utils.__all__:
            self.assertTrue(hasattr(zipimport_utils, name), name)


if __name__ == "__main__":
    unittest.main()
