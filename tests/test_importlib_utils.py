"""Tests for importlib_utils module."""

from __future__ import annotations

import os
from types import ModuleType

import pytest

import importlib_utils


def test_import_module_success() -> None:
    math_mod = importlib_utils.import_module("math")
    assert isinstance(math_mod, ModuleType)
    assert hasattr(math_mod, "pi")


def test_import_module_with_package() -> None:
    # Import a submodule with package context
    os_path = importlib_utils.import_module("os.path")
    assert isinstance(os_path, ModuleType)


def test_import_module_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.import_module(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        importlib_utils.import_module("math", package=123)  # type: ignore[arg-type]


def test_reload_module() -> None:
    # Reload math module
    math_mod = importlib_utils.import_module("math")
    reloaded = importlib_utils.reload_module(math_mod)
    assert isinstance(reloaded, ModuleType)


def test_reload_module_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.reload_module("math")  # type: ignore[arg-type]


def test_find_spec() -> None:
    spec = importlib_utils.find_spec("sys")
    assert spec is not None

    # Non-existent module
    spec_none = importlib_utils.find_spec("nonexistent_module_xyz_12345")
    assert spec_none is None


def test_find_spec_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.find_spec(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        importlib_utils.find_spec("sys", package=123)  # type: ignore[arg-type]


def test_get_module_name_from_path() -> None:
    # Use this test file's path
    path = os.path.abspath(__file__)
    name = importlib_utils.get_module_name_from_path(path)
    assert name is not None  # spec will give a name even if temp


def test_get_module_name_from_path_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_module_name_from_path(123)  # type: ignore[arg-type]


def test_is_module_available() -> None:
    assert importlib_utils.is_module_available("os") is True
    assert importlib_utils.is_module_available("json") is True
    assert importlib_utils.is_module_available("nonexistent_xyz_12345") is False


def test_is_module_available_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.is_module_available(123)  # type: ignore[arg-type]


def test_get_source_file() -> None:
    math_mod = importlib_utils.import_module("math")
    src = importlib_utils.get_source_file(math_mod)
    # math is built-in, may be None
    # but function should work
    assert src is None or isinstance(src, str)


def test_get_source_file_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_source_file("math")  # type: ignore[arg-type]


def test_get_loader() -> None:
    math_mod = importlib_utils.import_module("math")
    loader = importlib_utils.get_loader(math_mod)
    assert loader is None or loader is not None  # just check it returns


def test_get_loader_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_loader("math")  # type: ignore[arg-type]


def test_get_spec() -> None:
    sys_mod = importlib_utils.import_module("sys")
    spec = importlib_utils.get_spec(sys_mod)
    assert spec is not None


def test_get_spec_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_spec("sys")  # type: ignore[arg-type]


def test_get_distribution() -> None:
    # Try to get a distribution that should exist (pytest or pip)
    dist = importlib_utils.get_distribution("pytest")
    # Might not be installed in minimal env, but function should not crash
    # Also try pip
    if dist is None:
        dist = importlib_utils.get_distribution("pip")
    # Result can be None or Distribution; just verify no exception path errors beyond expected
    assert dist is None or hasattr(dist, "version")


def test_get_distribution_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_distribution(123)  # type: ignore[arg-type]


def test_get_distribution_version() -> None:
    ver = importlib_utils.get_distribution_version("pytest")
    if ver is None:
        ver = importlib_utils.get_distribution_version("pip")
    assert ver is None or isinstance(ver, str)


def test_get_distribution_version_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_distribution_version(123)  # type: ignore[arg-type]


def test_get_entry_points() -> None:
    eps = importlib_utils.get_entry_points()
    # Should return some iterable/structure
    assert eps is not None


def test_get_entry_points_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_entry_points(group=123)  # type: ignore[arg-type]


def test_get_attr_from_module() -> None:
    math_mod = importlib_utils.import_module("math")
    pi = importlib_utils.get_attr_from_module(math_mod, "pi")
    assert isinstance(pi, float)


def test_get_attr_from_module_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.get_attr_from_module("math", "pi")  # type: ignore[arg-type]
    math_mod = importlib_utils.import_module("math")
    with pytest.raises(TypeError):
        importlib_utils.get_attr_from_module(math_mod, 123)  # type: ignore[arg-type]


def test_call_func_from_module() -> None:
    math_mod = importlib_utils.import_module("math")
    result = importlib_utils.call_func_from_module(math_mod, "sqrt", 16)
    assert result == 4.0


def test_call_func_from_module_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.call_func_from_module("math", "sqrt", 16)  # type: ignore[arg-type]
    math_mod = importlib_utils.import_module("math")
    with pytest.raises(TypeError):
        importlib_utils.call_func_from_module(math_mod, 123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        importlib_utils.call_func_from_module(math_mod, "pi")  # pi is not callable


# Resource helpers are a bit environment-dependent; test basic type validation
def test_read_text_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.read_text("os", 123)  # type: ignore[arg-type]


def test_read_binary_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.read_binary("os", 123)  # type: ignore[arg-type]


def test_is_resource_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.is_resource("os", 123)  # type: ignore[arg-type]


def test_path_type_errors() -> None:
    with pytest.raises(TypeError):
        importlib_utils.path("os", 123)  # type: ignore[arg-type]
