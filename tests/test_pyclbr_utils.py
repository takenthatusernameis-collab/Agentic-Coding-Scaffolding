"""Unit tests for pyclbr_utils module."""

import shutil
import tempfile
import unittest
from pathlib import Path

import pyclbr_utils
from pyclbr_utils import Class, Function, read_module, read_module_ex

_FIXTURE_SOURCE = '''\
class Widget:
    """A sample class."""

    def gadget(self, value):
        return value


def sprocket(x, y):
    """A sample function."""
    return x + y
'''


def _read_fixture(read, name: str = "fixture_module"):
    """Write the fixture source into a temp directory and read it back.

    Reading a private fixture keeps the suite hermetic and deterministic: the
    module under inspection is never imported, and the result does not depend
    on pyclbr's own source or its module-level cache.
    """
    tmpdir = tempfile.mkdtemp(prefix="pyclbr-test-")
    try:
        path = Path(tmpdir) / f"{name}.py"
        path.write_text(_FIXTURE_SOURCE)
        return read(name, path=[tmpdir])
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


class TestReadModule(unittest.TestCase):
    """Exercise reading the classes of a module."""

    def test_read_module_returns_a_mapping(self) -> None:
        result = _read_fixture(read_module)
        self.assertIsInstance(result, dict)

    def test_read_module_returns_the_fixture_class(self) -> None:
        result = _read_fixture(read_module)
        self.assertIsInstance(result["Widget"], Class)

    def test_read_module_unknown_module_raises(self) -> None:
        with self.assertRaises(ModuleNotFoundError):
            read_module("no_such_module_xyz")

    def test_read_module_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            read_module(42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            read_module("fixture_module", path="not-a-sequence")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            read_module("fixture_module", path=[42])  # type: ignore[list-item]


class TestReadModuleEx(unittest.TestCase):
    """Exercise reading the classes and functions of a module."""

    def test_read_module_ex_returns_classes_and_functions(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertIsInstance(result["Widget"], Class)
        self.assertIsInstance(result["sprocket"], Function)

    def test_read_module_ex_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            read_module_ex(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            read_module_ex("fixture_module", path=[1, 2])  # type: ignore[list-item]


class TestClassNames(unittest.TestCase):
    """Exercise the class name helper."""

    def test_class_names_returns_the_class_names(self) -> None:
        self.assertEqual(pyclbr_utils.class_names(_read_fixture(read_module_ex)), ["Widget"])

    def test_class_names_excludes_functions(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertNotIn("sprocket", pyclbr_utils.class_names(result))

    def test_class_names_returns_sorted_strings(self) -> None:
        names = pyclbr_utils.class_names(_read_fixture(read_module_ex))
        self.assertEqual(names, sorted(names))
        self.assertTrue(all(isinstance(name, str) for name in names))

    def test_class_names_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pyclbr_utils.class_names("not-a-dict")  # type: ignore[arg-type]


class TestFunctionNames(unittest.TestCase):
    """Exercise the function name helper."""

    def test_function_names_returns_the_function_names(self) -> None:
        names = pyclbr_utils.function_names(_read_fixture(read_module_ex))
        self.assertIn("sprocket", names)
        self.assertEqual(names, sorted(names))

    def test_function_names_excludes_classes(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertNotIn("Widget", pyclbr_utils.function_names(result))

    def test_function_names_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pyclbr_utils.function_names(42)  # type: ignore[arg-type]


class TestFindClass(unittest.TestCase):
    """Exercise the class lookup helper."""

    def test_find_class_returns_the_class(self) -> None:
        cls = pyclbr_utils.find_class(_read_fixture(read_module_ex), "Widget")
        assert cls is not None
        self.assertEqual(cls.name, "Widget")

    def test_find_class_returns_none_for_unknown_names(self) -> None:
        self.assertIsNone(pyclbr_utils.find_class(_read_fixture(read_module_ex), "NoSuchClass"))

    def test_find_class_ignores_functions(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertIsNone(pyclbr_utils.find_class(result, "sprocket"))

    def test_find_class_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pyclbr_utils.find_class("not-a-dict", "Widget")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pyclbr_utils.find_class(_read_fixture(read_module_ex), 42)  # type: ignore[arg-type]


class TestFindFunction(unittest.TestCase):
    """Exercise the function lookup helper."""

    def test_find_function_returns_the_function(self) -> None:
        func = pyclbr_utils.find_function(_read_fixture(read_module_ex), "sprocket")
        assert func is not None
        self.assertEqual(func.name, "sprocket")

    def test_find_function_returns_none_for_unknown_names(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertIsNone(pyclbr_utils.find_function(result, "NoSuchFunction"))

    def test_find_function_ignores_classes(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertIsNone(pyclbr_utils.find_function(result, "Widget"))

    def test_find_function_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(TypeError):
            pyclbr_utils.find_function(None, "sprocket")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pyclbr_utils.find_function(_read_fixture(read_module_ex), 42)  # type: ignore[arg-type]


class TestHasClassAndFunction(unittest.TestCase):
    """Exercise the membership helpers."""

    def test_has_class_reports_known_and_unknown_classes(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertTrue(pyclbr_utils.has_class(result, "Widget"))
        self.assertFalse(pyclbr_utils.has_class(result, "sprocket"))

    def test_has_function_reports_known_and_unknown_functions(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertTrue(pyclbr_utils.has_function(result, "sprocket"))
        self.assertFalse(pyclbr_utils.has_function(result, "NoSuchFunction"))


class TestIsClassAndFunction(unittest.TestCase):
    """Exercise the type predicates."""

    def test_is_class_recognises_class_descriptors(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertTrue(pyclbr_utils.is_class(result["Widget"]))
        self.assertFalse(pyclbr_utils.is_class(result["sprocket"]))

    def test_is_function_recognises_function_descriptors(self) -> None:
        result = _read_fixture(read_module_ex)
        self.assertTrue(pyclbr_utils.is_function(result["sprocket"]))
        self.assertFalse(pyclbr_utils.is_function(result["Widget"]))

    def test_predicates_handle_plain_objects(self) -> None:
        self.assertFalse(pyclbr_utils.is_class(42))
        self.assertFalse(pyclbr_utils.is_function("not a function"))


class TestReexports(unittest.TestCase):
    """Exercise the standard library re-exports."""

    def test_class_and_function_are_the_stdlib_objects(self) -> None:
        import pyclbr

        self.assertIs(pyclbr_utils.Class, pyclbr.Class)
        self.assertIs(pyclbr_utils.Function, pyclbr.Function)


if __name__ == "__main__":
    unittest.main()
