"""Utilities for traceback (wrapping :mod:`traceback`)."""

import traceback as _traceback


def format_exception(exc):
    """Format an exception as a list of strings.

    Args:
        exc: The exception instance to format.

    Returns:
        A list of strings, each ending in a newline.
    """
    return _traceback.format_exception(exc)


def format_exception_only(exc_type, exc_value=None):
    """Format the exception part of a traceback.

    Args:
        exc_type: The exception class.
        exc_value: The exception instance (optional).

    Returns:
        A list of strings, each ending in a newline.
    """
    return _traceback.format_exception_only(exc_type, exc_value)


def extract_stack():
    """Extract the raw stack trace from the current point.

    Returns:
        A list of :class:`traceback.FrameSummary` objects.
    """
    return _traceback.extract_stack()


def format_stack():
    """Format the current stack trace.

    Returns:
        A list of strings ready for printing.
    """
    return _traceback.format_stack()


def format_exc():
    """Format the current exception as a string.

    Returns:
        A string containing the exception information, or an empty string
        if no exception is being handled.
    """
    try:
        result = _traceback.format_exc()
        if result == "NoneType: None\n":
            return ""
        return result
    except Exception:
        return _traceback.format_exc()
