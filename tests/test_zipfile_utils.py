import os
import pathlib
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


class TestListNamesBoundary(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="zipfile-utils-test-")
        self.src = os.path.join(self.tmpdir, "a.txt")
        with open(self.src, "w", encoding="utf-8") as handle:
            handle.write("hello")
        self.archive = os.path.join(self.tmpdir, "out.zip")
        create_archive(self.archive, [self.src])

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_list_names_type_errors(self):
        with self.assertRaises(TypeError):
            list_names(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            list_names("")


class TestExtractAllBoundary(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="zipfile-utils-test-")
        self.src = os.path.join(self.tmpdir, "a.txt")
        with open(self.src, "w", encoding="utf-8") as handle:
            handle.write("hello")
        self.archive = os.path.join(self.tmpdir, "out.zip")
        create_archive(self.archive, [self.src])

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_extract_all_type_errors(self):
        with self.assertRaises(TypeError):
            extract_all(123, self.tmpdir)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            extract_all(self.archive, 123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            extract_all("", self.tmpdir)
        with self.assertRaises(ValueError):
            extract_all(self.archive, "")


class TestIsZipfileBoundary(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="zipfile-utils-test-")
        self.src = os.path.join(self.tmpdir, "a.txt")
        with open(self.src, "w", encoding="utf-8") as handle:
            handle.write("hello")
        self.archive = os.path.join(self.tmpdir, "out.zip")
        create_archive(self.archive, [self.src])

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_is_zipfile_type_errors(self):
        with self.assertRaises(TypeError):
            is_zipfile(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_zipfile("")

    def test_is_zipfile_true_for_archive(self):
        self.assertTrue(is_zipfile(self.archive))

    def test_is_zipfile_false_for_non_zip(self):
        self.assertFalse(is_zipfile(self.src))


class TestZipfileUtilsBoundary(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="zipfile-utils-test-")
        self.src = os.path.join(self.tmpdir, "a.txt")
        with open(self.src, "w", encoding="utf-8") as handle:
            handle.write("hello")
        self.archive = os.path.join(self.tmpdir, "out.zip")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_path_accepts_path_objects(self):
        p_archive = pathlib.Path(self.archive)
        p_src = pathlib.Path(self.src)
        create_archive(p_archive, [p_src])
        self.assertTrue(is_zipfile(p_archive))
        self.assertEqual(len(list_names(p_archive)), 1)
        dest = pathlib.Path(self.tmpdir) / "ex"
        dest.mkdir()
        extract_all(p_archive, dest)
        self.assertTrue((dest / "a.txt").exists() or any(dest.rglob("a.txt")))

    def test_create_archive_type_errors(self):
        with self.assertRaises(TypeError):
            create_archive(123, [self.src])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_archive(self.archive, "nope")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_archive(self.archive, [123])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_archive(None, [self.src])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_archive("", [self.src])
        with self.assertRaises(ValueError):
            create_archive(self.archive, [])

    def test_list_names_type_errors(self):
        with self.assertRaises(TypeError):
            list_names(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            list_names(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            list_names("")

    def test_extract_all_type_errors(self):
        with self.assertRaises(TypeError):
            extract_all(123, self.tmpdir)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            extract_all(self.archive, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            extract_all(None, self.tmpdir)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            extract_all(self.archive, None)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            extract_all("", self.tmpdir)
        with self.assertRaises(ValueError):
            extract_all(self.archive, "")

    def test_is_zipfile_type_errors(self):
        with self.assertRaises(TypeError):
            is_zipfile(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_zipfile(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_zipfile("")


if __name__ == "__main__":
    unittest.main()
