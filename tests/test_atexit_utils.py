"""Tests for atexit_utils module."""

from __future__ import annotations

import pytest

import atexit_utils


def test_register_and_unregister():
    """Test registering and unregistering an exit handler."""
    calls = []

    def handler():
        calls.append("called")

    # Register the handler
    result = atexit_utils.register(handler)
    assert result is handler

    # Unregister it
    unreg_result = atexit_utils.unregister(handler)
    assert unreg_result is True

    # Unregistering again might return False or True depending on impl
    # but it should not raise
    atexit_utils.unregister(handler)


def test_register_with_args():
    """Test registering a handler with arguments."""
    calls = []

    def handler(x, y=10):
        calls.append((x, y))

    atexit_utils.register(handler, 5, y=20)
    atexit_utils.unregister(handler)


def test_register_non_callable_raises():
    """Test that registering non-callable raises TypeError."""
    with pytest.raises(TypeError):
        atexit_utils.register(123)  # type: ignore[arg-type]


def test_unregister_non_callable_raises():
    """Test that unregistering non-callable raises TypeError."""
    with pytest.raises(TypeError):
        atexit_utils.unregister(123)  # type: ignore[arg-type]


def test_add_and_remove_aliases():
    """Test add and remove as aliases."""
    calls = []

    def handler():
        calls.append(1)

    atexit_utils.add(handler)
    assert atexit_utils.remove(handler) is True


def test_get_registered():
    """Test getting registered handlers."""
    handlers = atexit_utils.get_registered()
    assert isinstance(handlers, list)


def test_clear_and_run_handlers():
    """Test clear and run_exit_handlers functions."""
    # These are safe to call
    atexit_utils.clear()
    atexit_utils.run_exit_handlers()
