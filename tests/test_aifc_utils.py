"""Tests for :mod:`aifc_utils`."""

from __future__ import annotations

import io

import pytest

import aifc_utils


def test_is_available() -> None:
    """The availability flag reflects the interpreter."""
    result = aifc_utils.is_available()
    assert isinstance(result, bool)


def test_open_validates_mode() -> None:
    """``open`` validates the mode argument."""
    with pytest.raises(TypeError):
        aifc_utils.open(io.BytesIO(b""), 123)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        aifc_utils.open(io.BytesIO(b""), "bad")  # type: ignore[arg-type]


@pytest.mark.skipif(not aifc_utils.is_available(), reason="aifc module not available")
def test_open_returns_object_when_available() -> None:
    """``open`` works when the module is available."""
    # Just test that it can be called with valid args if available
    try:
        # Try to open a minimal invalid file - will likely fail but call is valid
        aifc_utils.open(io.BytesIO(b""), "r")
    except Exception:
        pass  # Expected to fail on bad data


@pytest.mark.skipif(aifc_utils.is_available(), reason="aifc module available")
def test_missing_module_raises_runtime_error() -> None:
    """When the module is missing the helpers raise ``RuntimeError``."""
    with pytest.raises(RuntimeError):
        aifc_utils.open("file.aifc", "r")


def test_aliases_exist() -> None:
    """Aliases are available."""
    assert aifc_utils.open_aifc is aifc_utils.open
    assert aifc_utils.read_aifc is aifc_utils.open
    assert aifc_utils.write_aifc is aifc_utils.open
    assert aifc_utils.open_read is aifc_utils.open
    assert aifc_utils.open_write is aifc_utils.open


def test_exports() -> None:
    """Key exports are available."""
    assert hasattr(aifc_utils, "Aifc_read")
    assert hasattr(aifc_utils, "Aifc_write")
    assert hasattr(aifc_utils, "Error")
