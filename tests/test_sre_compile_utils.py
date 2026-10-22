"""Tests for the :mod:`sre_compile_utils` wrapper."""

from __future__ import annotations

import pytest

import sre_compile_utils


def test_is_available() -> None:
    result = sre_compile_utils.is_available()
    assert isinstance(result, bool)


@pytest.mark.skipif(not sre_compile_utils.is_available(), reason="sre_compile not available")
def test_compile_pattern() -> None:
    code = sre_compile_utils.compile_pattern("abc")
    assert code is not None


def test_compile_pattern_validates_flags() -> None:
    with pytest.raises(TypeError):
        sre_compile_utils.compile_pattern("abc", "bad")  # type: ignore[arg-type]


def test_degradation_without_module() -> None:
    original = sre_compile_utils._sre_compile
    try:
        sre_compile_utils._sre_compile = None  # type: ignore[assignment]
        with pytest.raises(RuntimeError, match="sre_compile"):
            sre_compile_utils.compile_pattern("abc")
    finally:
        sre_compile_utils._sre_compile = original
