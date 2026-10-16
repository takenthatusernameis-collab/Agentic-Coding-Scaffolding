"""Exception utilities for custom error handling."""

from __future__ import annotations

import traceback
from typing import Any, Callable, Dict, Optional, Type, TypeVar

T = TypeVar("T")


class ValidationError(ValueError):
    """Raised when data validation fails.

    Attributes:
        field: Optional field name that failed validation.
        value: The value that failed validation.
        message: Human-readable error message.
    """

    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        value: Any = None,
    ) -> None:
        self.field = field
        self.value = value
        self.message = message
        super().__init__(message)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""

    pass


class NotFoundError(Exception):
    """Raised when a requested resource is not found."""

    pass


class PermissionError_(Exception):
    """Raised when an operation is not permitted.

    Note: Avoids shadowing built-in PermissionError by using underscore suffix.
    """

    pass


class TimeoutError_(Exception):
    """Raised when an operation times out.

    Note: Avoids shadowing built-in TimeoutError in Python 3.11+ contexts.
    """

    pass


def catch_and_wrap(
    func: Callable[[], T],
    exceptions: tuple[Type[BaseException], ...] = (Exception,),
    wrap_with: Type[BaseException] = Exception,
    message: Optional[str] = None,
) -> T:
    """Execute func and wrap specified exceptions.

    Args:
        func: Callable to execute.
        exceptions: Tuple of exception types to catch and wrap.
        wrap_with: Exception type to wrap caught exceptions with.
        message: Optional message for wrapped exception.

    Returns:
        Result of func if successful.

    Raises:
        wrap_with: If any of the specified exceptions are caught.
    """
    try:
        return func()
    except exceptions as e:
        if message:
            raise wrap_with(message) from e
        raise wrap_with(str(e)) from e


def get_error_details(exc: BaseException) -> Dict[str, Any]:
    """Get detailed information about an exception.

    Args:
        exc: Exception to analyze.

    Returns:
        Dictionary containing exception type, message, and traceback.
    """
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }


def is_instance_of_any(obj: Any, exception_types: tuple[Type[BaseException], ...]) -> bool:
    """Check if obj is an instance of any exception type in the tuple.

    Args:
        obj: Object to check.
        exception_types: Tuple of exception types.

    Returns:
        True if obj is instance of any type, False otherwise.
    """
    return isinstance(obj, exception_types)


__all__ = [
    "ValidationError",
    "ConfigurationError",
    "NotFoundError",
    "PermissionError_",
    "TimeoutError_",
    "catch_and_wrap",
    "get_error_details",
    "is_instance_of_any",
]
