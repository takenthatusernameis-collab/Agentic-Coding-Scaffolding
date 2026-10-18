"""Logging configuration and helper utilities.

This module provides a thin, consistent API around the standard :mod:`logging`
module, including a ``get_logger`` helper, a ``configure_logging`` entry point
for application-wide setup, and a ``log_calls`` decorator for tracing function
entry and exit.
"""

import functools
import logging
from typing import Any, Callable, List, Optional, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

__all__: List[str] = [
    "configure_logging",
    "get_logger",
    "log_calls",
]

_DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DEFAULT_LOGGER_NAME = "logging_utils"


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a :class:`logging.Logger` for the given name.

    Args:
        name: The name for the logger, typically the module's ``__name__``.
            If ``None``, the root logger is returned.

    Returns:
        A :class:`logging.Logger` instance.

    Example:
        >>> logger = get_logger("my_app")
        >>> logger.name
        'my_app'
    """
    return logging.getLogger(name)


def configure_logging(
    level: Optional[int] = None,
    format: str = _DEFAULT_FORMAT,
    datefmt: Optional[str] = None,
    handlers: Optional[List[logging.Handler]] = None,
    force: bool = False,
) -> logging.Logger:
    """Configure the root logger with a consistent format and handlers.

    This is a thin wrapper around :func:`logging.basicConfig` that returns the
    configured root logger for convenience.

    Args:
        level: The logging level (e.g. ``logging.INFO``). When ``None``, the
            :mod:`logging` default of ``logging.WARNING`` is used.
        format: The log message format string. Defaults to a timestamped
            format including the logger name and level.
        datefmt: The date format string passed to
            :func:`logging.basicConfig`. Defaults to ``None``.
        handlers: Optional list of handlers to attach to the root logger.
            When ``None``, a :class:`logging.StreamHandler` is used.
        force: If ``True``, remove any existing handlers from the root logger
            before applying this configuration. Defaults to ``False``.

    Returns:
        The configured root :class:`logging.Logger`.

    Raises:
        TypeError: If ``level`` is not an integer or ``None``.
        TypeError: If ``handlers`` is not a list or ``None``.

    Example:
        >>> root = configure_logging(level=logging.INFO, force=True)
        >>> root.level
        20
    """
    if level is not None and not isinstance(level, int):
        raise TypeError("level must be an integer or None")
    if handlers is not None and not isinstance(handlers, list):
        raise TypeError("handlers must be a list or None")

    if level is None:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        handlers=handlers,
        force=force,
    )
    return logging.getLogger()


def log_calls(
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
) -> Callable[[F], F]:
    """Decorator factory that logs function calls and return values.

    The decorator logs two messages per invocation: one before the wrapped
    function runs (containing the arguments) and one after it returns
    (containing the return value). ``functools.wraps`` is used, so the
    decorated function's metadata (``__name__``, ``__doc__``, etc.) is
    preserved.

    Args:
        logger: The logger to emit messages to. If ``None``, a logger named
            ``"logging_utils"`` is used.
        level: The logging level for the emitted messages. Defaults to
            ``logging.DEBUG``.

    Returns:
        A decorator that wraps a function to log its calls.

    Example:
        >>> @log_calls()
        ... def greet(name: str) -> str:
        ...     return f"Hello, {name}!"
        >>> greet("World")
        'Hello, World!'
    """
    log = logger if logger is not None else logging.getLogger(_DEFAULT_LOGGER_NAME)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log.log(
                level,
                "Calling %s with args=%r, kwargs=%r",
                func.__qualname__,
                args,
                kwargs,
            )
            result = func(*args, **kwargs)
            log.log(
                level,
                "%s returned %r",
                func.__qualname__,
                result,
            )
            return result

        return cast(F, wrapper)

    return decorator
