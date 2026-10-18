"""Tests for contextlib_utils."""

import io

from contextlib_utils import (
    ExitStack,
    chdir,
    closing,
    nullcontext,
    redirect_stderr,
    redirect_stdout,
    suppress,
)


def test_suppress():
    with suppress(ValueError):
        raise ValueError("boom")
    # no exception


def test_nullcontext():
    with nullcontext(42) as v:
        assert v == 42


def test_closing():
    buf = io.StringIO()
    with closing(buf):
        buf.write("hi")
    assert buf.closed


def test_redirect_stdout():
    buf = io.StringIO()
    with redirect_stdout(buf):
        print("hello")
    assert buf.getvalue().strip() == "hello"


def test_redirect_stderr():
    buf = io.StringIO()
    with redirect_stderr(buf):
        import sys
        print("err", file=sys.stderr)
    assert buf.getvalue().strip() == "err"


def test_chdir(tmp_path):
    import os
    here = os.getcwd()
    with chdir(tmp_path):
        assert os.getcwd() == str(tmp_path)
    assert os.getcwd() == here


def test_exitstack():
    with ExitStack() as stack:
        buf = io.StringIO()
        stack.callback(buf.close)
    assert buf.closed
