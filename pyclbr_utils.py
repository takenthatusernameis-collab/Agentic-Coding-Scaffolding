"""Class and function browser utilities wrapping the standard library :mod:`pyclbr`.

The :mod:`pyclbr` module reads a Python source file and reports the classes
and functions it defines without importing or executing the source.  The
analysis is therefore purely static: the module under inspection is never
loaded, so this wrapper is safe to run against untrusted or partially written
modules and never opens a network connection or spawns a process.

This wrapper re-exports the standard library :class:`pyclbr.Class` and
:class:`pyclbr.Function` objects and adds validated helpers around
:func:`pyclbr.readmodule` and :func:`pyclbr.readmodule_ex`.  Every helper
checks the types of its arguments before the standard library is reached.
"""

from __future__ import annotations

import pyclbr
from typing import Any, Dict, List, Optional, Sequence, Union

__all__: List[str] = [
    "Class",
    "Function",
    "class_names",
    "find_class",
    "find_function",
    "function_names",
    "has_class",
    "has_function",
    "is_class",
    "is_function",
    "read_module",
    "read_module_ex",
]

#: The standard library class descriptor, re-exported for convenience.
Class = pyclbr.Class

#: The standard library function descriptor, re-exported for convenience.
Function = pyclbr.Function


def _require_str(name: str, value: Any) -> str:
    """Return *value* when it is a string.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated string.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_path(path: Any) -> Optional[Sequence[str]]:
    """Return *path* as a sequence of strings, or ``None`` when unset.

    Args:
        path: The search path to validate.

    Returns:
        The validated path, or ``None``.

    Raises:
        TypeError: If *path* is a string or contains a non-string entry.
    """
    if path is None:
        return None
    if isinstance(path, (str, bytes)):
        raise TypeError("path must be a sequence of strings, not a single string")
    try:
        entries = list(path)
    except TypeError as exc:
        raise TypeError(
            f"path must be a sequence of strings, got {type(path).__name__}"
        ) from exc
    for entry in entries:
        if not isinstance(entry, str):
            raise TypeError(f"path entries must be str, got {type(entry).__name__}")
    return entries


def _require_module_dict(result: Any) -> Dict[str, Any]:
    """Return *result* when it is a mapping of names to browser objects.

    Args:
        result: The value returned by :func:`read_module` or
            :func:`read_module_ex`.

    Returns:
        The validated mapping.

    Raises:
        TypeError: If *result* is not a mapping.
    """
    if not isinstance(result, dict):
        raise TypeError(f"result must be a dict, got {type(result).__name__}")
    return result


def read_module(
    module_name: str, path: Optional[Sequence[str]] = None
) -> Dict[str, Class]:
    """Return the classes defined in *module_name*.

    The source of *module_name* is read statically — it is never imported or
    executed — so this helper is safe to run against untrusted or partially
    written modules.

    Args:
        module_name: The name of the module to read.
        path: An optional list of directories searched before ``sys.path``.

    Returns:
        A dictionary mapping class names to :class:`Class` instances.

    Raises:
        TypeError: If an argument has the wrong type.
        ModuleNotFoundError: If the module cannot be found on the search path.
    """
    _require_str("module_name", module_name)
    search_path = _require_path(path)
    return pyclbr.readmodule(module_name, search_path)


def read_module_ex(
    module_name: str, path: Optional[Sequence[str]] = None
) -> Dict[str, Union[Class, Function]]:
    """Return the classes and functions defined in *module_name*.

    Like :func:`read_module`, but the result also contains the top-level
    functions of the module.

    Args:
        module_name: The name of the module to read.
        path: An optional list of directories searched before ``sys.path``.

    Returns:
        A dictionary mapping class and function names to :class:`Class` or
        :class:`Function` instances.

    Raises:
        TypeError: If an argument has the wrong type.
        ModuleNotFoundError: If the module cannot be found on the search path.
    """
    _require_str("module_name", module_name)
    search_path = _require_path(path)
    return pyclbr.readmodule_ex(module_name, search_path)


def class_names(result: Dict[str, Any]) -> List[str]:
    """Return the names of the classes in *result*, sorted.

    Args:
        result: A mapping as returned by :func:`read_module` or
            :func:`read_module_ex`.

    Returns:
        The sorted names of the classes described by *result*.

    Raises:
        TypeError: If *result* is not a mapping.
    """
    target = _require_module_dict(result)
    return sorted(
        name for name, value in target.items() if isinstance(value, Class)
    )


def function_names(result: Dict[str, Any]) -> List[str]:
    """Return the names of the functions in *result*, sorted.

    Args:
        result: A mapping as returned by :func:`read_module` or
            :func:`read_module_ex`.

    Returns:
        The sorted names of the functions described by *result*.

    Raises:
        TypeError: If *result* is not a mapping.
    """
    target = _require_module_dict(result)
    return sorted(
        name for name, value in target.items() if isinstance(value, Function)
    )


def find_class(result: Dict[str, Any], name: str) -> Optional[Class]:
    """Return the class named *name* in *result*, or ``None`` when absent.

    Args:
        result: A mapping as returned by :func:`read_module` or
            :func:`read_module_ex`.
        name: The name of the class to find.

    Returns:
        The class descriptor, or ``None`` when *result* has no such class.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    target = _require_module_dict(result)
    _require_str("name", name)
    value = target.get(name)
    return value if isinstance(value, Class) else None


def find_function(result: Dict[str, Any], name: str) -> Optional[Function]:
    """Return the function named *name* in *result*, or ``None`` when absent.

    Args:
        result: A mapping as returned by :func:`read_module` or
            :func:`read_module_ex`.
        name: The name of the function to find.

    Returns:
        The function descriptor, or ``None`` when *result* has no such
        function.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    target = _require_module_dict(result)
    _require_str("name", name)
    value = target.get(name)
    return value if isinstance(value, Function) else None


def has_class(result: Dict[str, Any], name: str) -> bool:
    """Report whether *result* describes a class named *name*.

    Args:
        result: A mapping as returned by :func:`read_module` or
            :func:`read_module_ex`.
        name: The name of the class to check.

    Returns:
        ``True`` when *result* contains a class named *name*.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    return find_class(result, name) is not None


def has_function(result: Dict[str, Any], name: str) -> bool:
    """Report whether *result* describes a function named *name*.

    Args:
        result: A mapping as returned by :func:`read_module` or
            :func:`read_module_ex`.
        name: The name of the function to check.

    Returns:
        ``True`` when *result* contains a function named *name*.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    return find_function(result, name) is not None


def is_class(value: Any) -> bool:
    """Report whether *value* is a :class:`Class` descriptor.

    Args:
        value: The object to check.

    Returns:
        ``True`` when *value* is a :class:`Class`.
    """
    return isinstance(value, Class)


def is_function(value: Any) -> bool:
    """Report whether *value* is a :class:`Function` descriptor.

    Args:
        value: The object to check.

    Returns:
        ``True`` when *value* is a :class:`Function`.
    """
    return isinstance(value, Function)
