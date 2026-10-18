"""Tests for codecs_utils."""

import codecs

from codecs_utils import (
    decode,
    encode,
    getdecoder,
    getencoder,
    getincrementaldecoder,
    getincrementalencoder,
    getreader,
    getwriter,
    lookup,
    lookup_error,
    register,
    register_error,
)
from codecs_utils import (
    open as codecs_open,
)


def test_encode_decode():
    assert decode(encode("hello", "utf-8"), "utf-8") == "hello"


def test_lookup():
    info = lookup("utf-8")
    assert info.name == "utf-8"


def test_getencoder_decoder():
    enc = getencoder("utf-8")
    dec = getdecoder("utf-8")
    assert enc("hi")[0] == b"hi"
    assert dec(b"hi")[0] == "hi"


def test_incremental():
    enc = getincrementalencoder("utf-8")
    dec = getincrementaldecoder("utf-8")
    assert enc.encode("hi") == b"hi"
    assert dec.decode(b"hi") == "hi"


def test_reader_writer():
    assert getreader("utf-8") is not None
    assert getwriter("utf-8") is not None


def test_register_error():
    register_error("test_err", codecs.lookup_error("strict"))
    assert lookup_error("test_err") is not None


def test_open(tmp_path):
    p = tmp_path / "f.txt"
    with codecs_open(str(p), "w", encoding="utf-8") as f:
        f.write("hello")
    with codecs_open(str(p), encoding="utf-8") as f:
        assert f.read() == "hello"


def test_register_callable():
    def search(name):
        return None

    register(search)
