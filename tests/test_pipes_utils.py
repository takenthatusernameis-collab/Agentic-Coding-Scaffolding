"""Tests for the :mod:`pipes_utils` wrapper."""

from __future__ import annotations

import importlib
import sys
from typing import Any

import pytest

import pipes_utils


def test_is_available() -> None:
    """``is_available`` reports whether the module ships."""
    result = pipes_utils.is_available()
    assert isinstance(result, bool)


def test_step_kinds() -> None:
    """``step_kinds`` returns the valid step kinds."""
    kinds = pipes_utils.step_kinds()
    assert isinstance(kinds, list)
    assert pipes_utils.SOURCE in kinds
    assert pipes_utils.SINK in kinds
    assert pipes_utils.STDIN_FILEOUT in kinds


def test_quote_validates() -> None:
    """``quote`` validates its arguments."""
    with pytest.raises(TypeError):
        pipes_utils.quote(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        pipes_utils.quote(None)  # type: ignore[arg-type]


def test_quote_command_validates() -> None:
    """``quote_command`` validates its arguments."""
    with pytest.raises(TypeError):
        pipes_utils.quote_command(123)  # type: ignore[arg-type]


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_quote_returns_string() -> None:
    """``quote`` returns a quoted string."""
    result = pipes_utils.quote("hello")
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_create_template_returns_template() -> None:
    """``create_template`` returns a template instance."""
    template = pipes_utils.create_template()
    assert template is not None
    assert hasattr(template, "append")
    assert hasattr(template, "prepend")
    assert hasattr(template, "reset")


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_template_append_prepend() -> None:
    """Templates can append and prepend steps."""
    template = pipes_utils.create_template()
    template.append("tr A-Z a-z", pipes_utils.STDIN_STDOUT)
    template.prepend("cat", pipes_utils.STDIN_STDOUT)
    # Should not raise


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_template_debug() -> None:
    """Templates support debug mode."""
    template = pipes_utils.create_template()
    template.debug(True)
    template.debug(False)


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_template_reset() -> None:
    """Templates can be reset."""
    template = pipes_utils.create_template()
    template.append("cat", pipes_utils.STDIN_STDOUT)
    template.reset()


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_template_clone() -> None:
    """Templates can be cloned."""
    template = pipes_utils.create_template()
    template.append("cat", pipes_utils.STDIN_STDOUT)
    cloned = template.clone()
    assert cloned is not None


@pytest.mark.skipif(not pipes_utils.is_available(), reason="pipes module not available")
def test_make_pipeline_validates() -> None:
    """``make_pipeline`` validates arguments."""
    template = pipes_utils.create_template()
    with pytest.raises(TypeError):
        pipes_utils.make_pipeline(template, 123, "out")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        pipes_utils.make_pipeline(template, "in", 123)  # type: ignore[arg-type]


def test_degradation_without_module() -> None:
    """Helpers raise RuntimeError when the module is missing."""
    import pipes_utils as pu

    original = pu._pipes
    try:
        pu._pipes = None
        with pytest.raises(RuntimeError, match="pipes"):
            pu.quote("x")
        with pytest.raises(RuntimeError, match="pipes"):
            pu.create_template()
        with pytest.raises(RuntimeError, match="pipes"):
            pu._pipes_module()
    finally:
        pu._pipes = original
