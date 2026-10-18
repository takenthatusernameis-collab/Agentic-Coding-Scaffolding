"""Tests for tarfile_utils."""

import os
import tempfile

from tarfile_utils import (
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
