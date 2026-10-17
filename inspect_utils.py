"""Callable and object introspection utilities.

This module provides helpers for inspecting Python callables using the
standard library :mod:`inspect` module: retrieving names, signatures,
parameters, source locations, and whether an object is callable or a
coroutine function. All functions validate their inputs and raise
``TypeError`` or ``ValueError`` on invalid arguments.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, List, Optional, Tuple


def get_callable_name(func: Any) -> str:
    """Return the name of *func* or the class name of a callable instance.

    Args:
        func: A callable object.

    Returns:
        The ``__name__`` of functions and methods, or the class name for
        callable instances without a ``__name__``.

    Raises:
        TypeError: If *func* is not callable.

    Examples:
        >>> def example(): ...
        >>> get_callable_name(example)
        'example'
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    name: Optional[str] = getattr(func, "__name__", None)
    if name:
        return name
    return str(type(func).__name__)


def is_callable(obj: Any) -> bool:
    """Return ``True`` if *obj* can be called.

    Args:
        obj: Any object.

    Returns:
        Whether *obj* is callable.

    Examples:
        >>> is_callable(len)
        True
        >>> is_callable(42)
        False
    """
    return callable(obj)


def is_async_callable(func: Any) -> bool:
    """Return ``True`` if *func* is a coroutine function.

    Args:
        func: A callable object.

    Returns:
        Whether *func`` is an async callable.

    Raises:
        TypeError: If *func* is not callable.

    Examples:
        >>> async def coro(): ...
        >>> is_async_callable(coro)
        True
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    return inspect.iscoroutinefunction(func)


def get_signature(func: Any) -> inspect.Signature:
    """Return the :class:`inspect.Signature` of *func*.

    Args:
        func: A callable object.

    Returns:
        The signature describing *func*'s parameters.

    Raises:
        TypeError: If *func* is not callable.
        ValueError: If the signature cannot be introspected.

    Examples:
        >>> def example(a: int, b: str = "x"): ...
        >>> str(get_signature(example))
        "(a: int, b: str = 'x')"
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    try:
        return inspect.signature(func)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"cannot introspect signature of {func!r}") from exc


def get_parameter_names(func: Any) -> List[str]:
    """Return the ordered list of parameter names of *func*.

    Args:
        func: A callable object.

    Returns:
        Parameter names in declaration order.

    Raises:
        TypeError: If *func* is not callable.
        ValueError: If the signature cannot be introspected.
    """
    return list(get_signature(func).parameters)


def get_parameter_kinds(func: Any) -> Dict[str, str]:
    """Return a mapping of parameter name to its kind for *func*.

    Args:
        func: A callable object.

    Returns:
        Dictionary mapping parameter names to kind strings
        (``POSITIONAL_ONLY``, ``POSITIONAL_OR_KEYWORD``, ``VAR_POSITIONAL``,
        ``KEYWORD_ONLY``, ``VAR_KEYWORD``).

    Raises:
        TypeError: If *func* is not callable.
        ValueError: If the signature cannot be introspected.
    """
    sig = get_signature(func)
    return {name: param.kind.name for name, param in sig.parameters.items()}


def count_parameters(func: Any) -> int:
    """Return the number of parameters of *func*.

    Args:
        func: A callable object.

    Returns:
        The total number of declared parameters.

    Raises:
        TypeError: If *func* is not callable.
        ValueError: If the signature cannot be introspected.
    """
    return len(get_signature(func).parameters)


def has_parameter(func: Any, name: str) -> bool:
    """Return ``True`` if *func* declares a parameter named *name*.

    Args:
        func: A callable object.
        name: The parameter name to check.

    Returns:
        Whether *name* is a declared parameter of *func*.

    Raises:
        TypeError: If *func* is not callable or *name* is not a string.
        ValueError: If the signature cannot be introspected.
    """
    if not isinstance(name, str):
        raise TypeError(f"parameter name must be a string, got {type(name).__name__}")
    return name in get_signature(func).parameters


def bind_arguments(func: Any, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Bind *args* and *kwargs* to *func*'s parameters, applying defaults.

    Args:
        func: A callable object.
        *args: Positional arguments to bind.
        **kwargs: Keyword arguments to bind.

    Returns:
        A dictionary mapping parameter names to their bound values, with
        defaults filled in for unbound parameters.

    Raises:
        TypeError: If *func* is not callable or the arguments do not match.
        ValueError: If the signature cannot be introspected.

    Examples:
        >>> def example(a, b=2, c=3): ...
        >>> bind_arguments(example, 1, c=10)
        {'a': 1, 'b': 2, 'c': 10}
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    sig = get_signature(func)
    try:
        bound = sig.bind(*args, **kwargs)
    except TypeError as exc:
        raise TypeError(f"arguments do not match signature of {func!r}: {exc}") from exc
    bound.apply_defaults()
    return dict(bound.arguments)


def is_builtin(func: Any) -> bool:
    """Return ``True`` if *func* is a built-in function or method.

    Args:
        func: A callable object.

    Returns:
        Whether *func* is a built-in.

    Raises:
        TypeError: If *func* is not callable.

    Examples:
        >>> is_builtin(len)
        True
        >>> def example(): ...
        >>> is_builtin(example)
        False
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    return inspect.isbuiltin(func)


def get_source_file(func: Any) -> Optional[str]:
    """Return the source file path defining *func*, if available.

    Args:
        func: A callable object.

    Returns:
        The source file path, or ``None`` if it cannot be determined.

    Raises:
        TypeError: If *func* is not callable.
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    try:
        return inspect.getfile(func)
    except TypeError:
        return None


def get_source_lines(func: Any) -> Optional[Tuple[List[str], int]]:
    """Return the source lines and starting line number of *func*, if available.

    Args:
        func: A callable object.

    Returns:
        A tuple of ``(lines, line_number)``, or ``None`` if unavailable.

    Raises:
        TypeError: If *func* is not callable.
    """
    if not callable(func):
        raise TypeError(f"expected a callable, got {type(func).__name__}")
    try:
        lines, start = inspect.getsourcelines(func)
    except (OSError, TypeError):
        return None
    return lines, start
