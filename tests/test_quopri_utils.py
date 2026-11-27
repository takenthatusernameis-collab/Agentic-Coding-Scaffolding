"""Tests for quopri_utils."""

import io
import unittest

try:
    import pytest
except ImportError:  # pragma: no cover - pytest is an optional dev dependency
    pytest = None  # type: ignore[assignment]

from quopri_utils import decode, decode_file, encode, encode_file, isqp


@unittest.skipIf(pytest is None, "pytest is required for this test")
class TestQuopriUtils(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        data = b"Hello World = test\r\n"
        enc = encode(data)
        assert decode(enc) == data

    def test_encode_quotetabs(self):
        enc = encode(b"a\tb", quotetabs=True)
        assert b"=09" in enc

    def test_isqp(self):
        assert isqp(ord("="))
        assert not isqp(ord("a"))

    def test_isqp_semantics(self):
        # Bytes outside printable ASCII require quoting; printable ASCII (except
        # the escape char) does not, matching quopri.needsquoting(quotetabs=False).
        assert isqp(0x80)
        assert isqp(0x00)
        assert not isqp(ord("A"))
        assert not isqp(ord(" "))
        assert not isqp(ord("_"))

    def test_isqp_type_validation(self):
        with pytest.raises(TypeError):
            isqp("A")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            isqp(True)
        with pytest.raises(ValueError):
            isqp(256)
        with pytest.raises(ValueError):
            isqp(-1)

    def test_encode_file_decode_file(self):
        inp = io.BytesIO(b"hi = there")
        out = io.BytesIO()
        encode_file(inp, out)
        out.seek(0)
        inp2 = io.BytesIO(out.read())
        out2 = io.BytesIO()
        decode_file(inp2, out2)
        assert out2.getvalue() == b"hi = there"

    def test_encode_leaks_typeerror_on_non_bytes(self):
        # quopri.encodestring raises TypeError for non bytes-like input.
        with pytest.raises(TypeError):
            encode("abc")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            encode(None)  # type: ignore[arg-type]

    def test_decode_leaks_typeerror_on_non_bytes(self):
        # quopri.decodestring raises TypeError for non bytes-like/ASCII input.
        with pytest.raises(TypeError):
            decode(None)  # type: ignore[arg-type]

    def test_encode_file_leaks_attributeerror_on_non_file(self):
        # quopri.encode calls .read on the input stream.
        with pytest.raises(AttributeError):
            encode_file(None, io.BytesIO())  # type: ignore[arg-type]

    def test_decode_file_leaks_attributeerror_on_non_file(self):
        # quopri.decode calls .read on the input stream.
        with pytest.raises(AttributeError):
            decode_file(None, io.BytesIO())  # type: ignore[arg-type]

    def test_encode_file_leaks_attributeerror_on_bad_output(self):
        # quopri.encode calls .write on the output stream.
        with pytest.raises(AttributeError):
            encode_file(io.BytesIO(b"x"), None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
