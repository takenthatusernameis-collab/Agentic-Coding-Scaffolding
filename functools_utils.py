"""Functional programming utilities for composing and transforming functions."""

from typing import Any, Callable, List, TypeVar

T = TypeVar("T")
R = TypeVar("R")

__all__: List[str] = [
    "compose",
    "pipe",
    "curry",
    "apply",
]


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose multiple functions from right to left.

    Args:
        *functions: Functions to compose. The rightmost function is applied
            first, and its result is passed to the function to its left.

    Returns:
        A composed function.

    Raises:
        ValueError: If no functions are provided.

    Examples:
        >>> def add_one(x: int) -> int: return x + 1
        >>> def multiply_by_two(x: int) -> int: return x * 2
        >>> composed = compose(multiply_by_two, add_one)
        >>> composed(3)
        8
    """

    if not functions:
        raise ValueError("At least one function must be provided")

    def composed(arg: Any) -> Any:
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result

    return composed


def pipe(arg: Any, *functions: Callable[[Any], Any]) -> Any:
    """Apply a value through a pipeline of functions from left to right.

    Args:
        arg: The initial value to pass through the pipeline.
        *functions: Functions to apply in order.

    Returns:
        The final result after applying all functions.

    Examples:
        >>> def add_one(x: int) -> int: return x + 1
        >>> def multiply_by_two(x: int) -> int: return x * 2
        >>> pipe(3, add_one, multiply_by_two)
        8
    """
    result = arg
    for func in functions:
        result = func(result)
    return result


def curry(func: Callable[..., R]) -> Callable[..., Any]:
    """Curry a function to allow partial application.

    Args:
        func: The function to curry.

    Returns:
        A curried version of the function.

    Raises:
        TypeError: If ``func`` is not callable.

    Examples:
        >>> def add(x: int, y: int) -> int: return x + y
        >>> curried = curry(add)
        >>> curried(1)(2)
        3
    """
    if not callable(func):
        raise TypeError("func must be callable")

    def curried(*args: Any, **kwargs: Any) -> Any:
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *more_args, **more_kwargs: curried(
            *args, *more_args, **kwargs, **more_kwargs
        )

    return curried


def apply(func: Callable[[T], R], value: T) -> R:
    """Apply a function to a value.

    Args:
        func: The function to apply.
        value: The value to apply the function to.

    Returns:
        The result of applying the function.

    Raises:
        TypeError: If ``func`` is not callable.

    Examples:
        >>> apply(lambda x: x * 2, 5)
        10
    """
    if not callable(func):
        raise TypeError("func must be callable")
    return func(value)
