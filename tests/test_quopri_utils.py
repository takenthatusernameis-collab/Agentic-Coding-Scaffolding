"""Tests for quopri_utils."""

import io

from quopri_utils import decode, decode_file, encode, encode_file, isqp


def test_encode_decode_roundtrip():
    data = b"Hello World = test\r\n"
    enc = encode(data)
    assert decode(enc) == data


def test_encode_quotetabs():
    enc = encode(b"a\tb", quotetabs=True)
    assert b"=09" in enc


def test_isqp():
    assert isqp(ord("="))
    assert not isqp(ord("a"))


def test_encode_file_decode_file():
    inp = io.BytesIO(b"hi = there")
    out = io.BytesIO()
    encode_file(inp, out)
    out.seek(0)
    inp2 = io.BytesIO(out.read())
    out2 = io.BytesIO()
    decode_file(inp2, out2)
    assert out2.getvalue() == b"hi = there"
