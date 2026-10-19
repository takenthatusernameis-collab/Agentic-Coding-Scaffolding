"""Utilities for working with Python types wrapping the standard library ``types`` module.

This module exposes helpers around dynamic type creation, function types, and
simple type checks. Each helper validates its arguments and raises ``TypeError``
on invalid input.
"""

from __future__ import annotations

import types
from typing import Any, Callable, Optional

__all__ = [
    "new_class",
    "new_function",
    "is_function",
    "is_method",
    "is_generator",
    "is_coroutine",
    "is_lambda",
    "simple_namespace",
]


def new_class(
    name: str,
    bases: tuple = (),
    exec_body: Optional[Callable[[dict], None]] = None,
) -> type:
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(bases, tuple):
        raise TypeError("bases must be a tuple")
    if exec_body is not None and not callable(exec_body):
        raise TypeError("exec_body must be callable or None")
    return types.new_class(name, bases, exec_body=exec_body)


def new_function(
    code: Any,
    globals_dict: dict,
    name: Optional[str] = None,
    argdefs: Optional[tuple] = None,
    closure: Optional[tuple] = None,
) -> types.FunctionType:
    if not isinstance(globals_dict, dict):
        raise TypeError("globals_dict must be a dict")
    if name is not None and not isinstance(name, str):
        raise TypeError("name must be a str or None")
    if argdefs is not None and not isinstance(argdefs, tuple):
        raise TypeError("argdefs must be a tuple or None")
    if closure is not None and not isinstance(closure, tuple):
        raise TypeError("closure must be a tuple or None")
    return types.FunctionType(code, globals_dict, name, argdefs, closure)


def is_function(obj: Any) -> bool:
    return isinstance(obj, types.FunctionType)


def is_method(obj: Any) -> bool:
    return isinstance(obj, types.MethodType)


def is_generator(obj: Any) -> bool:
    return isinstance(obj, types.GeneratorType)


def is_coroutine(obj: Any) -> bool:
    return isinstance(obj, types.CoroutineType)


def is_lambda(obj: Any) -> bool:
    return isinstance(obj, types.LambdaType)


def simple_namespace(**kwargs: Any) -> types.SimpleNamespace:
    return types.SimpleNamespace(**kwargs)