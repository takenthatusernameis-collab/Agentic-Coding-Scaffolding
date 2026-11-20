import audioop

import pytest

from audioop_utils import (
    audioop_add,
    audioop_max,
    audioop_minmax,
    audioop_mul,
    audioop_rms,
)


def test_audioop_add():
    a = b"\x00\x01" * 2
    assert audioop_add(a, a, 2) == audioop.add(a, a, 2)


def test_audioop_mul():
    a = b"\x01\x00" * 2
    assert audioop_mul(a, 2, 2.0) == audioop.mul(a, 2, 2.0)


def test_audioop_rms():
    a = b"\x00\x01" * 2
    assert audioop_rms(a, 2) == audioop.rms(a, 2)


def test_audioop_max():
    a = b"\x00\x01" * 2
    assert audioop_max(a, 2) == audioop.max(a, 2)


def test_audioop_minmax():
    a = b"\x00\x01" * 2
    assert audioop_minmax(a, 2) == audioop.minmax(a, 2)


def test_width_type_error():
    with pytest.raises(TypeError):
        audioop_rms(b"\x00", True)
    with pytest.raises(TypeError):
        audioop_rms(b"\x00", "x")


def test_factor_type_error():
    with pytest.raises(TypeError):
        audioop_mul(b"\x00", 2, "x")
    with pytest.raises(TypeError):
        audioop_mul(b"\x00", 2, True)
