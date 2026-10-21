"""Tests for bdb_utils."""

from __future__ import annotations

import bdb_utils


def test_exports() -> None:
    assert bdb_utils.Bdb is not None
    assert bdb_utils.BdbQuit is not None
    assert bdb_utils.Breakpoint is not None


def test_checkfuncname() -> None:
    assert callable(bdb_utils.checkfuncname)


def test_effective() -> None:
    assert callable(bdb_utils.effective)