"""Tests for tabnanny_utils."""

from __future__ import annotations

import io
import tokenize

import pytest

from tabnanny_utils import NannyNag, check, process_tokens


def test_check_clean_file(tmp_path):
    src = tmp_path / "clean.py"
    src.write_text("x = 1\n")
    check(str(src))


def test_process_tokens_raises_on_ambiguous(tmp_path):
    src = "def f():\n  x = 1\n\ty = 2\n"
    tokens = tokenize.generate_tokens(io.StringIO(src).readline)
    with pytest.raises(NannyNag):
        process_tokens(tokens)


def test_nannynag_attributes():
    nag = NannyNag(3, "msg", "line")
    assert nag.get_lineno() == 3
    assert nag.get_msg() == "msg"
    assert nag.get_line() == "line"


def test_check_rejects_non_path():
    with pytest.raises(TypeError):
        check(123)
