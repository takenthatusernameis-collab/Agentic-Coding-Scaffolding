"""Tests for :mod:`spwd_utils`."""

from __future__ import annotations

import pytest

import spwd_utils


def test_is_available() -> None:
    """The availability flag reflects the interpreter."""
    result = spwd_utils.is_available()
    assert isinstance(result, bool)


def test_getspnam_validates_name() -> None:
    """``getspnam`` validates the name argument."""
    with pytest.raises(TypeError):
        spwd_utils.getspnam(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        spwd_utils.getspnam(b"root")  # type: ignore[arg-type]


def test_getspnam_unknown_user() -> None:
    """``getspnam`` raises ``KeyError`` for an unknown user."""
    if not spwd_utils.is_available():
        pytest.skip("spwd module not available")
    with pytest.raises(KeyError):
        spwd_utils.getspnam("no-such-user-zzz")


def test_getspnam_returns_shadow_entry() -> None:
    """``getspnam`` returns a :class:`ShadowEntry`."""
    if not spwd_utils.is_available():
        pytest.skip("spwd module not available")
    entry = spwd_utils.getspnam("root")
    assert isinstance(entry, spwd_utils.ShadowEntry)
    assert entry.sp_nam == "root"
    assert isinstance(entry.sp_pwdp, str)


def test_shadow_entry_fields() -> None:
    """A :class:`ShadowEntry` carries every aging field."""
    entry = spwd_utils.ShadowEntry(
        sp_nam="root",
        sp_pwdp="x",
        sp_lstchg=None,
        sp_min=None,
        sp_max=None,
        sp_warn=None,
        sp_inact=None,
        sp_expire=None,
        sp_flag=None,
    )
    assert entry.sp_nam == "root"
    assert entry.sp_pwdp == "x"
    assert entry.sp_lstchg is None
    assert entry.sp_max is None


def test_getspnam_negative_fields_become_none() -> None:
    """Aging fields of ``-1`` are reported as ``None``."""
    if not spwd_utils.is_available():
        pytest.skip("spwd module not available")
    entry = spwd_utils.getspnam("root")
    assert entry.sp_lstchg is None
    assert entry.sp_min is None
    assert entry.sp_max is None


def test_getspall_returns_list() -> None:
    """``getspall`` returns a list of :class:`ShadowEntry`."""
    if not spwd_utils.is_available():
        pytest.skip("spwd module not available")
    entries = spwd_utils.getspall()
    assert isinstance(entries, list)
    for entry in entries:
        assert isinstance(entry, spwd_utils.ShadowEntry)


def test_missing_module_raises_runtime_error() -> None:
    """When the module is missing the helpers raise ``RuntimeError``."""
    if spwd_utils.is_available():
        pytest.skip("spwd module available")
    with pytest.raises(RuntimeError):
        spwd_utils.getspnam("root")
    with pytest.raises(RuntimeError):
        spwd_utils.getspall()


def test_exports() -> None:
    """The public API is exported."""
    for name in ("ShadowEntry", "getspall", "getspnam", "is_available"):
        assert hasattr(spwd_utils, name)
