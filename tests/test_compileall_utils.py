"""Tests for compileall_utils."""

import tempfile
from pathlib import Path

from compileall_utils import compile_dir, compile_file, compile_path, main


def test_compile_file():
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "a.py"
        src.write_text("x = 1\n")
        out = compile_file(src)
        assert out.exists()


def test_compile_dir():
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "a.py"
        src.write_text("x = 1\n")
        assert compile_dir(d) is True


def test_compile_path_runs():
    # smoke
    compile_path(quiet=2)


def test_main():
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "a.py"
        src.write_text("x = 1\n")
        assert main([str(src)]) == 0


def test_invalid():
    try:
        compile_file(123)  # type: ignore
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")
