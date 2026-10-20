"""Utilities for extracting and formatting tracebacks (wrapping :mod:`traceback`)."""

import traceback
from types import TracebackType
from typing import Any, List, Optional, Type


def format_exception(etype_or_exc: Any, value: Any = None,
                    tb: Any = None, *args, **kwargs) -> List[str]:
    """Format a stack trace and the exception information."""
    if value is None and isinstance(etype_or_exc, BaseException):
        exc = etype_or_exc
        return traceback.format_exception(type(exc), exc, exc.__traceback__, *args, **kwargs)
    etype = etype_or_exc
    if not isinstance(etype, type) or not issubclass(etype, BaseException):
        raise TypeError("etype must be an exception type")
    if not isinstance(value, BaseException):
        raise TypeError("value must be an exception instance")
    if tb is not None and not isinstance(tb, TracebackType):
        raise TypeError("tb must be a traceback")
    return traceback.format_exception(etype, value, tb, *args, **kwargs)


def format_exception_only(etype: Type[BaseException], value: BaseException) -> List[str]:
    """Format the exception part of a traceback."""
    if not isinstance(etype, type) or not issubclass(etype, BaseException):
        raise TypeError("etype must be an exception type")
    if not isinstance(value, BaseException):
        raise TypeError("value must be an exception instance")
    return traceback.format_exception_only(etype, value)


def format_tb(tb: Optional[TracebackType] = None, limit: Optional[int] = None) -> List[str]:
    """Format a traceback object."""
    if tb is not None and not isinstance(tb, TracebackType):
        raise TypeError("tb must be a traceback")
    return traceback.format_tb(tb, limit=limit)


def format_stack(f=None, limit: Optional[int] = None) -> List[str]:
    """Format a stack trace."""
    return traceback.format_stack(f, limit=limit)


def format_exc(limit: Optional[int] = None, chain: bool = True) -> str:
    """Format the current exception as a string."""
    if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool)):
        raise TypeError("limit must be an integer or None")
    if not isinstance(chain, bool):
        raise TypeError("chain must be a bool")
    result = traceback.format_exc(limit=limit, chain=chain)
    if result == 'NoneType: None\n':
        return ''
    return result


def extract_tb(tb: TracebackType, limit: Optional[int] = None) -> List[Any]:
    """Extract traceback information."""
    if not isinstance(tb, TracebackType):
        raise TypeError("tb must be a traceback")
    if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool)):
        raise TypeError("limit must be an integer or None")
    return traceback.extract_tb(tb, limit=limit)


def extract_stack(f=None, limit: Optional[int] = None) -> List[Any]:
    """Extract stack information."""
    if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool)):
        raise TypeError("limit must be an integer or None")
    return traceback.extract_stack(f, limit=limit)


def print_exception(etype_or_exc: Any, value: Any = None, tb: Any = None,
                    limit: Optional[int] = None, file=None, **kwargs) -> None:
    """Print exception information and stack trace."""
    if value is None and isinstance(etype_or_exc, BaseException):
        exc = etype_or_exc
        traceback.print_exception(type(exc), exc, exc.__traceback__,
                                 limit=limit, file=file, **kwargs)
        return
    etype = etype_or_exc
    if not isinstance(etype, type) or not issubclass(etype, BaseException):
        raise TypeError("etype must be an exception type")
    if not isinstance(value, BaseException):
        raise TypeError("value must be an exception instance")
    if tb is not None and not isinstance(tb, TracebackType):
        raise TypeError("tb must be a traceback")
    if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool)):
        raise TypeError("limit must be an integer or None")
    traceback.print_exception(etype, value, tb, limit=limit, file=file, **kwargs)


def print_tb(tb: Optional[TracebackType] = None, limit: Optional[int] = None, file=None) -> None:
    """Print a traceback."""
    if tb is not None and not isinstance(tb, TracebackType):
        raise TypeError("tb must be a traceback")
    if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool)):
        raise TypeError("limit must be an integer or None")
    traceback.print_tb(tb, limit=limit, file=file)


def print_stack(f=None, limit: Optional[int] = None, file=None) -> None:
    """Print a stack trace."""
    if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool)):
        raise TypeError("limit must be an integer or None")
    traceback.print_stack(f, limit=limit, file=file)


def clear_frames(tb: TracebackType) -> None:
    """Clear local variables in a traceback."""
    if not isinstance(tb, TracebackType):
        raise TypeError("tb must be a traceback")
    traceback.clear_frames(tb)
