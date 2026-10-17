"""Tests for difflib_utils."""

from __future__ import annotations

from difflib_utils import (
    context_diff,
    get_close_matches,
    ndiff,
    ratio,
    unified_diff,
)


def test_get_close_matches() -> None:
    assert get_close_matches("appel", ["apple", "ape", "peach"]) == ["apple", "ape"]


def test_ratio_identical() -> None:
    assert ratio("abc", "abc") == 1.0


def test_ratio_different() -> None:
    assert 0.0 <= ratio("abc", "xyz") < 1.0


def test_unified_diff() -> None:
    a = ["line1\n", "line2\n"]
    b = ["line1\n", "line3\n"]
    out = unified_diff(a, b, fromfile="a", tofile="b")
    assert any("line2" in line for line in out)
    assert any("line3" in line for line in out)


def test_context_diff() -> None:
    a = ["line1\n", "line2\n"]
    b = ["line1\n", "line3\n"]
    out = context_diff(a, b)
    assert len(out) > 0


def test_ndiff() -> None:
    out = ndiff(["a\n"], ["b\n"])
    assert len(out) > 0
