"""Tests for tarfile_utils."""

import os
import tempfile
import unittest

from tarfile_utils import (
    tarfile_add,
    tarfile_create,
    tarfile_extract,
    tarfile_extractall,
    tarfile_list,
    tarfile_open,
)


def test_tarfile_create_list_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "a.txt")
        with open(src, "w") as f:
            f.write("hello")
        archive = os.path.join(d, "test.tar")
        tarfile_create(archive, [src], arcnames=["a.txt"])
        assert tarfile_list(archive) == ["a.txt"]


def test_tarfile_extract():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "a.txt")
        with open(src, "w") as f:
            f.write("hello")
        archive = os.path.join(d, "test.tar")
        tarfile_create(archive, [src], arcnames=["a.txt"])
        out = os.path.join(d, "out")
        os.makedirs(out)
        tarfile_extract(archive, "a.txt", path=out)
        with open(os.path.join(out, "a.txt")) as f:
            assert f.read() == "hello"


def test_tarfile_extractall():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "a.txt")
        with open(src, "w") as f:
            f.write("hello")
        archive = os.path.join(d, "test.tar")
        tarfile_create(archive, [src], arcnames=["a.txt"])
        out = os.path.join(d, "out")
        os.makedirs(out)
        tarfile_extractall(archive, path=out)
        with open(os.path.join(out, "a.txt")) as f:
            assert f.read() == "hello"


def test_tarfile_open():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "a.txt")
        with open(src, "w") as f:
            f.write("hello")
        archive = os.path.join(d, "test.tar")
        tarfile_create(archive, [src], arcnames=["a.txt"])
        with tarfile_open(archive) as tf:
            assert tf.getnames() == ["a.txt"]


class TestTarfileUtilsBoundary(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(prefix="tarfile-utils-test-")
        self.src = os.path.join(self.tmpdir, "a.txt")
        with open(self.src, "w", encoding="utf-8") as handle:
            handle.write("hello")
        self.archive = os.path.join(self.tmpdir, "out.tar")
        tarfile_create(self.archive, [self.src], arcnames=["a.txt"])

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_open_type_value_errors(self) -> None:
        with self.assertRaises(TypeError):
            tarfile_open(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_open(self.archive, 123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tarfile_open("")
        with self.assertRaises(ValueError):
            tarfile_open(self.archive, "")

    def test_add_type_value_errors(self) -> None:
        with self.assertRaises(TypeError):
            tarfile_add(123, self.src)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_add(self.archive, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_add(self.archive, self.src, arcname=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tarfile_add("", self.src)
        with self.assertRaises(ValueError):
            tarfile_add(self.archive, "")
        with self.assertRaises(ValueError):
            tarfile_add(self.archive, self.src, arcname="")

    def test_list_type_value_errors(self) -> None:
        with self.assertRaises(TypeError):
            tarfile_list(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tarfile_list("")

    def test_extract_type_value_errors(self) -> None:
        with self.assertRaises(TypeError):
            tarfile_extract(123, "a.txt")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_extract(self.archive, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_extract(self.archive, "a.txt", path=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tarfile_extract("", "a.txt")
        with self.assertRaises(ValueError):
            tarfile_extract(self.archive, "")

    def test_extractall_type_value_errors(self) -> None:
        with self.assertRaises(TypeError):
            tarfile_extractall(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_extractall(self.archive, path=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tarfile_extractall("")
        with self.assertRaises(ValueError):
            tarfile_extractall(self.archive, path="")

    def test_create_type_value_errors(self) -> None:
        with self.assertRaises(TypeError):
            tarfile_create(123, [self.src])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_create(self.archive, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_create(self.archive, [123])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_create(self.archive, [self.src], arcnames="x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_create(self.archive, [self.src], arcnames=[123])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tarfile_create(self.archive, [self.src], base_dir=123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tarfile_create("", [self.src])
        with self.assertRaises(ValueError):
            tarfile_create(self.archive, [])
        with self.assertRaises(ValueError):
            tarfile_create(self.archive, [self.src], base_dir="")

    def test_path_acceptance(self) -> None:
        from pathlib import Path

        outdir = Path(self.tmpdir) / "outp"
        outdir.mkdir()
        archive_p = Path(self.tmpdir) / "p.tar"
        tarfile_create(archive_p, [Path(self.src)], arcnames=[Path("a.txt")])
        tarfile_add(archive_p, Path(self.src), arcname=Path("b.txt"))
        names = tarfile_list(archive_p)
        self.assertIn("a.txt", names)
        self.assertIn("b.txt", names)
        tarfile_extract(archive_p, "a.txt", path=outdir)
        tarfile_extractall(archive_p, path=outdir)
        with tarfile_open(archive_p) as tf:
            self.assertGreaterEqual(len(tf.getnames()), 2)
