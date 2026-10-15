"""Tests for compression_utils module."""

import tempfile
import unittest
from pathlib import Path

from compression_utils import (
    bz2_compress,
    bz2_decompress,
    gzip_compress,
    gzip_decompress,
    tar_compress,
    tar_extract,
    zip_compress_files,
    zip_extract,
)


class TestGzipCompress(unittest.TestCase):
    def test_compress_decompress_bytes(self) -> None:
        data = b"Hello, World!"
        compressed = gzip_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertNotEqual(compressed, data)
        decompressed = gzip_decompress(compressed)
        self.assertEqual(decompressed, data)

    def test_compress_decompress_string(self) -> None:
        data = "Hello, World!"
        compressed = gzip_compress(data)
        self.assertIsInstance(compressed, bytes)
        decompressed = gzip_decompress(compressed, encoding="utf-8")
        self.assertEqual(decompressed, data)

    def test_gzip_errors(self) -> None:
        with self.assertRaises(TypeError):
            gzip_compress(123)  # type: ignore

        with self.assertRaises(TypeError):
            gzip_decompress("not bytes")  # type: ignore


class TestBz2Compress(unittest.TestCase):
    def test_compress_decompress_bytes(self) -> None:
        data = b"Hello, bz2 compression!"
        compressed = bz2_compress(data)
        self.assertIsInstance(compressed, bytes)
        self.assertNotEqual(compressed, data)
        decompressed = bz2_decompress(compressed)
        self.assertEqual(decompressed, data)

    def test_compress_decompress_string(self) -> None:
        data = "Hello, bz2 compression!"
        compressed = bz2_compress(data)
        decompressed = bz2_decompress(compressed, encoding="utf-8")
        self.assertEqual(decompressed, data)

    def test_bz2_errors(self) -> None:
        with self.assertRaises(TypeError):
            bz2_compress(123)  # type: ignore

        with self.assertRaises(TypeError):
            bz2_decompress("not bytes")  # type: ignore


class TestZipCompress(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_zip_compress_and_extract(self) -> None:
        temp_path = Path(self.temp_dir)
        file1 = temp_path / "file1.txt"
        file2 = temp_path / "file2.txt"
        file1.write_text("hello")
        file2.write_text("world")

        zip_path = temp_path / "archive.zip"
        zip_compress_files([file1, file2], zip_path)
        self.assertTrue(zip_path.exists())

        extract_dir = temp_path / "extracted"
        zip_extract(zip_path, extract_dir)
        self.assertTrue((extract_dir / "file1.txt").exists())
        self.assertTrue((extract_dir / "file2.txt").exists())
        self.assertEqual((extract_dir / "file1.txt").read_text(), "hello")

    def test_zip_compress_missing_file(self) -> None:
        temp_path = Path(self.temp_dir)
        zip_path = temp_path / "archive.zip"
        with self.assertRaises(FileNotFoundError):
            zip_compress_files([temp_path / "missing.txt"], zip_path)


class TestTarCompress(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_tar_compress_and_extract(self) -> None:
        temp_path = Path(self.temp_dir)
        file1 = temp_path / "file1.txt"
        file2 = temp_path / "file2.txt"
        file1.write_text("hello")
        file2.write_text("world")

        tar_path = temp_path / "archive.tar"
        tar_compress([file1, file2], tar_path)
        self.assertTrue(tar_path.exists())

        extract_dir = temp_path / "extracted"
        tar_extract(tar_path, extract_dir)
        self.assertTrue((extract_dir / "file1.txt").exists())
        self.assertTrue((extract_dir / "file2.txt").exists())

    def test_tar_compress_missing_file(self) -> None:
        temp_path = Path(self.temp_dir)
        tar_path = temp_path / "archive.tar"
        with self.assertRaises(FileNotFoundError):
            tar_compress([temp_path / "missing.txt"], tar_path)
