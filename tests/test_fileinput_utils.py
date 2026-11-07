"""Tests for fileinput_utils."""

import tempfile
from pathlib import Path

from fileinput_utils import count_lines, filenames, has_lines, read_lines


def test_read_lines():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.txt"
        p.write_text("hello\nworld\n")
        lines = read_lines([str(p)])
        assert lines == ["hello\n", "world\n"]


def test_count_lines():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.txt"
        p.write_text("one\ntwo\nthree\n")
        assert count_lines([str(p)]) == 3


def test_filenames():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.txt"
        p.write_text("x\n")
        assert filenames([str(p)]) == [str(p)]


def test_has_lines_true():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.txt"
        p.write_text("one\ntwo\nthree\n")
        assert has_lines([str(p)]) is True


def test_has_lines_false():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.txt"
        p.write_text("")
        assert has_lines([str(p)]) is False
