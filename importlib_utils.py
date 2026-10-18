"""Utilities for working with Python's importlib module.

This module provides convenient wrappers around stdlib `importlib` functions
for dynamic importing, module inspection, and resource loading where applicable.
"""

from __future__ import annotations

import importlib
import importlib.util
from importlib import metadata as importlib_metadata
from importlib import resources as importlib_resources
from types import ModuleType
from typing import Any


def import_module(name: str, package: str | None = None) -> ModuleType:
    """Dynamically import a module.

    Args:
        name: The name of the module to import (e.g., 'math', 'os.path').
        package: Optional package to anchor relative imports.

    Returns:
        The imported module object.

    Raises:
        TypeError: If inputs are not of the expected types.
        ImportError: If the module cannot be imported.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if package is not None and not isinstance(package, str):
        raise TypeError("package must be a string or None")
    return importlib.import_module(name, package)


def reload_module(module: ModuleType) -> ModuleType:
    """Reload an already imported module.

    Args:
        module: The module object to reload.

    Returns:
        The reloaded module object.

    Raises:
        TypeError: If module is not a ModuleType.
        ImportError: If the module cannot be reloaded.
    """
    if not isinstance(module, ModuleType):
        raise TypeError("module must be a ModuleType")
    return importlib.reload(module)


def find_spec(name: str, package: str | None = None) -> importlib.machinery.ModuleSpec | None:
    """Find a module's spec without importing it.

    Args:
        name: The module name to find.
        package: Optional package for relative imports.

    Returns:
        A ModuleSpec if found, else None.

    Raises:
        TypeError: If inputs are not of the expected types.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if package is not None and not isinstance(package, str):
        raise TypeError("package must be a string or None")
    return importlib.util.find_spec(name, package)


def get_module_name_from_path(path: str) -> str | None:
    """Determine the module name for a given file path, if possible.

    Args:
        path: Path to a Python file.

    Returns:
        Module name string or None if it cannot be determined.

    Raises:
        TypeError: If path is not a string.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    spec = importlib.util.spec_from_file_location("tmp_module", path)
    if spec is None:
        return None
    return spec.name


def is_module_available(name: str, package: str | None = None) -> bool:
    """Check if a module is importable without actually importing it.

    Args:
        name: Module name to check.
        package: Optional package for relative imports.

    Returns:
        True if the module spec exists, False otherwise.

    Raises:
        TypeError: If inputs are not of the expected types.
    """
    try:
        spec = find_spec(name, package)
        return spec is not None
    except TypeError:
        raise
    except Exception:
        return False


def get_source_file(module: ModuleType) -> str | None:
    """Get the source file path for a module, if available.

    Args:
        module: Module to inspect.

    Returns:
        Path to source file or None if not available (e.g., builtins).

    Raises:
        TypeError: If module is not a ModuleType.
    """
    if not isinstance(module, ModuleType):
        raise TypeError("module must be a ModuleType")
    return getattr(module, "__file__", None)


def get_loader(module: ModuleType) -> Any | None:
    """Get the loader for a module.

    Args:
        module: Module to inspect.

    Returns:
        Loader object or None if not present.

    Raises:
        TypeError: If module is not a ModuleType.
    """
    if not isinstance(module, ModuleType):
        raise TypeError("module must be a ModuleType")
    return getattr(module, "__loader__", None)


def get_spec(module: ModuleType) -> importlib.machinery.ModuleSpec | None:
    """Get the spec for a module.

    Args:
        module: Module to inspect.

    Returns:
        ModuleSpec or None if not present.

    Raises:
        TypeError: If module is not a ModuleType.
    """
    if not isinstance(module, ModuleType):
        raise TypeError("module must be a ModuleType")
    return getattr(module, "__spec__", None)


# Metadata helpers (PEP 396/modern metadata via importlib.metadata)
def get_distribution(name: str) -> importlib_metadata.Distribution | None:
    """Get distribution metadata for a package name.

    Args:
        name: Package distribution name.

    Returns:
        Distribution object or None if not found.

    Raises:
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    try:
        return importlib_metadata.distribution(name)
    except importlib_metadata.PackageNotFoundError:
        return None


def get_distribution_version(name: str) -> str | None:
    """Get version string for a distribution.

    Args:
        name: Package distribution name.

    Returns:
        Version string or None if not found.

    Raises:
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    dist = get_distribution(name)
    if dist is None:
        return None
    return dist.version


def get_entry_points(group: str | None = None) -> Any:
    """Get entry points, optionally filtered by group.

    Args:
        group: Optional entry point group name.

    Returns:
        EntryPoints object or list depending on Python version semantics.
    """
    if group is not None and not isinstance(group, str):
        raise TypeError("group must be a string or None")
    try:
        # Python 3.10+ supports select/group filtering; try to be compatible
        eps = importlib_metadata.entry_points()
        try:
            if hasattr(eps, "select"):
                if group is not None:
                    return eps.select(group=group)
                return eps
        except Exception:
            pass
        if group is not None:
            try:
                result = []
                for e in eps:
                    try:
                        if getattr(e, "group", None) == group:
                            result.append(e)
                    except Exception:
                        continue
                return type(eps)(result) if hasattr(type(eps), "__call__") else result  # type: ignore
            except Exception:
                return eps
        return eps
    except Exception:
        return importlib_metadata.entry_points()


# Resource helpers (importlib.resources)
def read_text(package: Any, resource: str) -> str:
    """Read a text resource from a package.

    Args:
        package: Package name (str) or module object.
        resource: Resource filename.

    Returns:
        Resource content as string.

    Raises:
        TypeError: If inputs are not of expected types.
        FileNotFoundError: If resource is not found.
    """
    if not isinstance(resource, str):
        raise TypeError("resource must be a string")
    # package can be str or module
    return importlib_resources.read_text(package, resource)  # type: ignore[call-arg]


def read_binary(package: Any, resource: str) -> bytes:
    """Read a binary resource from a package.

    Args:
        package: Package name (str) or module object.
        resource: Resource filename.

    Returns:
        Resource content as bytes.

    Raises:
        TypeError: If inputs are not of expected types.
        FileNotFoundError: If resource is not found.
    """
    if not isinstance(resource, str):
        raise TypeError("resource must be a string")
    return importlib_resources.read_binary(package, resource)  # type: ignore[call-arg]


def is_resource(package: Any, resource: str) -> bool:
    """Check if a resource exists in a package.

    Args:
        package: Package name (str) or module object.
        resource: Resource filename.

    Returns:
        True if resource exists, False otherwise.

    Raises:
        TypeError: If inputs are not of expected types.
    """
    if not isinstance(resource, str):
        raise TypeError("resource must be a string")
    try:
        return importlib_resources.is_resource(package, resource)  # type: ignore[call-arg]
    except Exception:
        return False


def path(package: Any, resource: str) -> Any:
    """Context manager providing a file path to a resource.

    Args:
        package: Package name (str) or module object.
        resource: Resource filename.

    Returns:
        A context manager yielding the file system path.

    Raises:
        TypeError: If inputs are not of expected types.
        FileNotFoundError: If resource is not found.
    """
    if not isinstance(resource, str):
        raise TypeError("resource must be a string")
    return importlib_resources.path(package, resource)  # type: ignore[call-arg]


# Utility to get function by name from module
def get_attr_from_module(module: ModuleType, attr_name: str) -> Any:
    """Retrieve an attribute from a module by name.

    Args:
        module: The module object.
        attr_name: Name of the attribute.

    Returns:
        The attribute value.

    Raises:
        TypeError: If inputs are not of expected types.
        AttributeError: If attribute does not exist.
    """
    if not isinstance(module, ModuleType):
        raise TypeError("module must be a ModuleType")
    if not isinstance(attr_name, str):
        raise TypeError("attr_name must be a string")
    return getattr(module, attr_name)


def call_func_from_module(module: ModuleType, func_name: str, *args: Any, **kwargs: Any) -> Any:
    """Call a function from a module by name.

    Args:
        module: The module object.
        func_name: Name of the function.
        *args: Positional arguments to pass to function.
        **kwargs: Keyword arguments to pass to function.

    Returns:
        Result of function call.

    Raises:
        TypeError: If inputs are not of expected types or target is not callable.
        AttributeError: If function does not exist.
    """
    if not isinstance(module, ModuleType):
        raise TypeError("module must be a ModuleType")
    if not isinstance(func_name, str):
        raise TypeError("func_name must be a string")
    func = getattr(module, func_name)
    if not callable(func):
        raise TypeError("attribute is not callable")
    return func(*args, **kwargs)


__all__ = [
    "import_module",
    "reload_module",
    "find_spec",
    "get_module_name_from_path",
    "is_module_available",
    "get_source_file",
    "get_loader",
    "get_spec",
    "get_distribution",
    "get_distribution_version",
    "get_entry_points",
    "read_text",
    "read_binary",
    "is_resource",
    "path",
    "get_attr_from_module",
    "call_func_from_module",
]
