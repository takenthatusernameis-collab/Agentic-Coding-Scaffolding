"""Tests for :mod:`pdb_utils`."""

from __future__ import annotations

import pdb as _pdb
from unittest import mock

import pdb_utils


def test_re_exports() -> None:
    assert pdb_utils.Pdb is _pdb.Pdb
    assert pdb_utils.pm is _pdb.pm
    assert callable(pdb_utils.post_mortem)
    assert callable(pdb_utils.run)
    assert callable(pdb_utils.runcall)
    assert callable(pdb_utils.runeval)
    assert callable(pdb_utils.set_trace)


def test_run_validates() -> None:
    try:
        pdb_utils.run(123)  # type: ignore[arg-type]
    except TypeError as exc:
        assert "statement" in str(exc)
    else:
        raise AssertionError


def test_runeval_validates() -> None:
    try:
        pdb_utils.runeval(123)  # type: ignore[arg-type]
    except TypeError as exc:
        assert "expression" in str(exc)
    else:
        raise AssertionError


def test_runcall_validates() -> None:
    try:
        pdb_utils.runcall(123)  # type: ignore[arg-type]
    except TypeError as exc:
        assert "callable" in str(exc)
    else:
        raise AssertionError


def test_set_trace_validates() -> None:
    try:
        pdb_utils.set_trace(header=123)  # type: ignore[arg-type]
    except TypeError as exc:
        assert "header" in str(exc)
    else:
        raise AssertionError


def test_run_forwarded() -> None:
    with mock.patch.object(_pdb, "run") as mocked:
        pdb_utils.run("x=1", globals_={"x": 0}, locals_={"y": 2})
        mocked.assert_called_once_with("x=1", {"x": 0}, {"y": 2})


def test_runeval_forwarded() -> None:
    with mock.patch.object(_pdb, "runeval") as mocked:
        mocked.return_value = 42
        pdb_utils.runeval("1+1", globals_={})


def test_runcall_forwarded() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    with mock.patch.object(_pdb, "runcall") as mocked:
        mocked.return_value = 3
        pdb_utils.runcall(add, 1, 2)


def test_set_trace_forwarded() -> None:
    with mock.patch.object(_pdb, "set_trace") as mocked:
        pdb_utils.set_trace()
        mocked.assert_called_once_with()
