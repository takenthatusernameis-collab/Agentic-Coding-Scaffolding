import os
import shutil
import tempfile
import unittest

from zipfile_utils import create_archive, extract_all, is_zipfile, list_names


class TestZipfileUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="zipfile-utils-test-")
        self.src = os.path.join(self.tmpdir, "a.txt")
        with open(self.src, "w", encoding="utf-8") as handle:
            handle.write("hello")
        self.archive = os.path.join(self.tmpdir, "out.zip")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_create_and_list(self):
        create_archive(self.archive, [self.src])
        self.assertTrue(is_zipfile(self.archive))
        names = list_names(self.archive)
        self.assertEqual(len(names), 1)

    def test_extract_all(self):
        create_archive(self.archive, [self.src])
        dest = os.path.join(self.tmpdir, "extracted")
        os.mkdir(dest)
        extract_all(self.archive, dest)
        found = False
        for root, _, files in os.walk(dest):
            if files:
                found = True
        self.assertTrue(found)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            create_archive(123, [self.src])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_archive("", [self.src])
        with self.assertRaises(ValueError):
            create_archive(self.archive, [])


if __name__ == "__main__":
    unittest.main()
