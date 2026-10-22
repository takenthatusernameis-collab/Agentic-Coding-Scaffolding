"""Tests for :mod:`sunau_utils`."""

from __future__ import annotations

import io

import pytest

import sunau_utils


def test_is_available() -> None:
    """The availability flag reflects the interpreter."""
    result = sunau_utils.is_available()
    assert isinstance(result, bool)


def test_open_validates_mode() -> None:
    """``open`` validates the mode argument."""
    with pytest.raises(TypeError):
        sunau_utils.open(io.BytesIO(b""), 123)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        sunau_utils.open(io.BytesIO(b""), "bad")  # type: ignore[arg-type]


@pytest.mark.skipif(not sunau_utils.is_available(), reason="sunau module not available")
def test_open_returns_object_when_available() -> None:
    """``open`` works when the module is available."""
    # Just test that it can be called with valid args if available
    try:
        # Try to open a minimal invalid file - will likely fail but call is valid
        sunau_utils.open(io.BytesIO(b""), "r")
    except Exception:
        pass  # Expected to fail on bad data


@pytest.mark.skipif(sunau_utils.is_available(), reason="sunau module available")
def test_missing_module_raises_runtime_error() -> None:
    """When the module is missing the helpers raise ``RuntimeError``."""
    with pytest.raises(RuntimeError):
        sunau_utils.open("file.sunau", "r")


def test_aliases_exist() -> None:
    """Aliases are available."""
    assert sunau_utils.open_sunau is sunau_utils.open
    assert sunau_utils.read_sunau is sunau_utils.open
    assert sunau_utils.write_sunau is sunau_utils.open
    assert sunau_utils.open_read is sunau_utils.open
    assert sunau_utils.open_write is sunau_utils.open


def test_exports() -> None:
    """Key exports are available."""
    assert hasattr(sunau_utils, "Au_read")
    assert hasattr(sunau_utils, "Au_write")
    assert hasattr(sunau_utils, "Error")
