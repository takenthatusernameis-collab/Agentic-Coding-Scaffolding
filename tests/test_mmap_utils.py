import mmap
import os
import tempfile
import unittest

from mmap_utils import (
    ACCESS_READ,
    ACCESS_WRITE,
    ACCESS_COPY,
    ALLOCATIONGRANULARITY,
    PAGESIZE,
    access_copy,
    access_read,
    access_write,
    allocation_granularity,
    close_mmap,
    constants,
    create_anonymous,
    create_file_mmap,
    find_bytes,
    is_mmap,
    pagesize,
    read_bytes,
    write_bytes,
)


class TestMmapUtils(unittest.TestCase):
    def test_access_constants_match_mmap(self):
        self.assertEqual(access_read(), mmap.ACCESS_READ)
        self.assertEqual(access_write(), mmap.ACCESS_WRITE)
        self.assertEqual(access_copy(), mmap.ACCESS_COPY)
        self.assertEqual(ACCESS_READ, mmap.ACCESS_READ)
        self.assertEqual(ACCESS_WRITE, mmap.ACCESS_WRITE)
        self.assertEqual(ACCESS_COPY, mmap.ACCESS_COPY)

    def test_pagesize_and_granularity_positive(self):
        self.assertIsInstance(pagesize(), int)
        self.assertGreater(pagesize(), 0)
        self.assertEqual(pagesize(), PAGESIZE)
        self.assertIsInstance(allocation_granularity(), int)
        self.assertGreater(allocation_granularity(), 0)
        self.assertEqual(allocation_granularity(), ALLOCATIONGRANULARITY)

    def test_constants_dict(self):
        result = constants()
        self.assertEqual(
            result,
            {
                "PAGESIZE": pagesize(),
                "ALLOCATIONGRANULARITY": allocation_granularity(),
                "ACCESS_READ": access_read(),
                "ACCESS_WRITE": access_write(),
                "ACCESS_COPY": access_copy(),
            },
        )

    def test_create_anonymous_read_write(self):
        region = create_anonymous(64)
        try:
            self.assertTrue(is_mmap(region))
            write_bytes(region, b"hello mmap")
            self.assertEqual(read_bytes(region, 5), b"hello")
            self.assertEqual(read_bytes(region, 10, 0), b"hello mmap")
        finally:
            close_mmap(region)
        # A closed mmap remains an mmap instance; operations on it fail.
        with self.assertRaises(ValueError):
            region.read(1)

    def test_create_file_mmap_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "mmap_test.bin")
            region = create_file_mmap(path, 64)
            try:
                write_bytes(region, b"persistent mmap data")
                self.assertEqual(read_bytes(region, 20, 0), b"persistent mmap data")
            finally:
                close_mmap(region)

    def test_find_bytes_found_and_missing(self):
        region = create_anonymous(32)
        try:
            write_bytes(region, b"abcdefabcdef")
            self.assertEqual(find_bytes(region, b"def"), 3)
            self.assertEqual(find_bytes(region, b"def", start=4), 9)
            self.assertEqual(find_bytes(region, b"xyz"), -1)
        finally:
            close_mmap(region)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            create_anonymous("not an int")
        with self.assertRaises(TypeError):
            create_anonymous(True)
        with self.assertRaises(ValueError):
            create_anonymous(0)
        with self.assertRaises(ValueError):
            create_anonymous(-3)
        with self.assertRaises(TypeError):
            write_bytes("not an mmap", b"data")
        with self.assertRaises(TypeError):
            write_bytes(create_anonymous(16), "not bytes")
        with self.assertRaises(TypeError):
            read_bytes("not an mmap", 4)
        with self.assertRaises(TypeError):
            find_bytes("not an mmap", b"x")
        with self.assertRaises(TypeError):
            close_mmap("not an mmap")
        self.assertFalse(is_mmap(None))
        self.assertFalse(is_mmap(42))

    def test_create_file_mmap_invalid_arguments(self):
        with self.assertRaises(TypeError):
            create_file_mmap(123, 16)
        with self.assertRaises(ValueError):
            create_file_mmap(__file__, 0)
        with self.assertRaises(ValueError):
            create_file_mmap(__file__, 16, offset=-1)


if __name__ == "__main__":
    unittest.main()
