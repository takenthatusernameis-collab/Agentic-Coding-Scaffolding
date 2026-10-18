import os
import stat as _stat
import tempfile
import unittest

from stat_utils import (
    file_mode,
    file_type,
    filemode,
    is_device,
    is_directory,
    is_fifo,
    is_regular_file,
    is_socket,
    is_symlink,
    stat_info,
)


class TestStatUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="stat-utils-test-")
        self.file_path = os.path.join(self.tmpdir, "sample.txt")
        with open(self.file_path, "w", encoding="utf-8") as handle:
            handle.write("stat-utils sample data\n")
        self.dir_path = os.path.join(self.tmpdir, "subdir")
        os.mkdir(self.dir_path)

    def tearDown(self) -> None:
        for name in ("sample.txt", "subdir"):
            path = os.path.join(self.tmpdir, name)
            if os.path.isdir(path) and not os.path.islink(path):
                os.rmdir(path)
            elif os.path.exists(path):
                os.remove(path)
        os.rmdir(self.tmpdir)

    def test_file_mode_regular_file(self):
        mode = file_mode(self.file_path)
        self.assertIsInstance(mode, int)
        self.assertTrue(mode & 0o600)

    def test_file_mode_directory(self):
        mode = file_mode(self.dir_path)
        self.assertIsInstance(mode, int)
        self.assertTrue(_stat.S_ISDIR(mode) or _stat.S_ISDIR(os.stat(self.dir_path).st_mode))

    def test_file_type(self):
        self.assertEqual(file_type(self.file_path), _stat.S_IFREG)
        self.assertEqual(file_type(self.dir_path), _stat.S_IFDIR)

    def test_is_directory(self):
        self.assertTrue(is_directory(self.dir_path))
        self.assertFalse(is_directory(self.file_path))

    def test_is_regular_file(self):
        self.assertTrue(is_regular_file(self.file_path))
        self.assertFalse(is_regular_file(self.dir_path))

    def test_is_symlink(self):
        self.assertFalse(is_symlink(self.file_path))
        link_path = os.path.join(self.tmpdir, "link.txt")
        os.symlink(self.file_path, link_path)
        try:
            self.assertTrue(is_symlink(link_path))
            self.assertTrue(is_regular_file(link_path))
        finally:
            os.remove(link_path)

    def test_is_socket_and_fifo_and_device_false(self):
        self.assertFalse(is_socket(self.file_path))
        self.assertFalse(is_fifo(self.file_path))
        self.assertFalse(is_device(self.file_path))

    def test_filemode_string(self):
        result = filemode(self.file_path)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.startswith("-"))

    def test_stat_info_keys(self):
        info = stat_info(self.file_path)
        expected = {
            "mode", "ino", "dev", "nlink", "uid", "gid", "size",
            "atime", "mtime", "ctime",
        }
        self.assertEqual(set(info.keys()), expected)
        self.assertGreater(info["size"], 0)

    def test_stat_info_rounds_trip_with_os_stat(self):
        info = stat_info(self.file_path)
        direct = os.stat(self.file_path)
        self.assertEqual(info["mode"], direct.st_mode)
        self.assertEqual(info["size"], direct.st_size)
        self.assertEqual(info["mtime"], direct.st_mtime)


if __name__ == "__main__":
    unittest.main()
