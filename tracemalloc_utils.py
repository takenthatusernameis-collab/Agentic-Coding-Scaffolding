"""Utilities for tracing Python memory allocations (wrapping :mod:`tracemalloc`)."""

import tracemalloc as _tracemalloc


def is_tracing():
    """Return whether tracemalloc is currently tracing allocations."""
    return _tracemalloc.is_tracing()


def get_traced_memory():
    """Return current and peak traced memory as a tuple."""
    return _tracemalloc.get_traced_memory()


def get_traceback_limit():
    """Return the traceback limit used for traces."""
    return _tracemalloc.get_traceback_limit()


def start(nframes=1):
    """Start tracing allocations with the given frame depth."""
    _tracemalloc.start(nframes)


def stop():
    """Stop tracing allocations."""
    _tracemalloc.stop()


def clear_traces():
    """Clear all recorded traces."""
    _tracemalloc.clear_traces()
