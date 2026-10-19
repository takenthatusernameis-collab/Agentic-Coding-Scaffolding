import os
import tempfile
import unittest

from hashlib_utils import (
    blake2b_hash,
    blake2s_hash,
    file_hash,
    md5_hash,
    sha1_hash,
    sha3_256_hash,
    sha3_512_hash,
    sha256_hash,
    sha512_hash,
)


class TestHashlibUtils(unittest.TestCase):
    def test_basic_hashes(self):
        data = b"hello world"
        self.assertEqual(len(md5_hash(data)), 16)
        self.assertEqual(len(sha1_hash(data)), 20)
        self.assertEqual(len(sha256_hash(data)), 32)
        self.assertEqual(len(sha512_hash(data)), 64)
        self.assertEqual(len(sha3_256_hash(data)), 32)
        self.assertEqual(len(sha3_512_hash(data)), 64)

    def test_blake2(self):
        data = b"test"
        self.assertEqual(len(blake2b_hash(data)), 64)
        self.assertEqual(len(blake2s_hash(data)), 32)
        self.assertEqual(len(blake2b_hash(data, digest_size=32)), 32)

    def test_file_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"content")
            path = f.name
        try:
            h = file_hash(path)
            self.assertEqual(len(h), 32)
            h2 = file_hash(path, algorithm="md5")
            self.assertEqual(len(h2), 16)
        finally:
            os.unlink(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            md5_hash("not bytes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            file_hash(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            file_hash("path", algorithm=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            file_hash("path", chunk_size="10")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            file_hash("path", chunk_size=0)
        with self.assertRaises(FileNotFoundError):
            file_hash("/nonexistent/file_xyz")


if __name__ == "__main__":
    unittest.main()
