"""Tests for inspect_utils module."""

import unittest

from inspect_utils import (
    bind_arguments,
    count_parameters,
    get_callable_name,
    get_parameter_kinds,
    get_parameter_names,
    get_signature,
    get_source_file,
    get_source_lines,
    has_parameter,
    is_async_callable,
    is_builtin,
    is_callable,
)


class TestIsCallable(unittest.TestCase):
    def test_callable_builtin(self):
        self.assertTrue(is_callable(len))
        self.assertTrue(is_callable(print))

    def test_callable_function(self):
        def example():
            pass

        self.assertTrue(is_callable(example))

    def test_callable_class(self):
        class Example:
            pass

        self.assertTrue(is_callable(Example))

    def test_callable_instance(self):
        class Callable:
            def __call__(self):
                pass

        self.assertTrue(is_callable(Callable()))

    def test_not_callable(self):
        self.assertFalse(is_callable(42))
        self.assertFalse(is_callable("hello"))
        self.assertFalse(is_callable(None))
        self.assertFalse(is_callable([1, 2]))


class TestGetCallableName(unittest.TestCase):
    def test_function_name(self):
        def example():
            pass

        self.assertEqual(get_callable_name(example), "example")

    def test_builtin_name(self):
        self.assertEqual(get_callable_name(len), "len")

    def test_class_name(self):
        class Example:
            pass

        self.assertEqual(get_callable_name(Example), "Example")

    def test_callable_instance(self):
        class Callable:
            def __call__(self):
                pass

        self.assertEqual(get_callable_name(Callable()), "Callable")

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            get_callable_name(42)


class TestIsAsyncCallable(unittest.TestCase):
    def test_async_function(self):
        async def coro():
            pass

        self.assertTrue(is_async_callable(coro))

    def test_sync_function(self):
        def example():
            pass

        self.assertFalse(is_async_callable(example))

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            is_async_callable(42)


class TestGetSignature(unittest.TestCase):
    def test_signature(self):
        def example(a: int, b: str = "x"):
            pass

        self.assertEqual(str(get_signature(example)), "(a: int, b: str = 'x')")

    def test_builtin_signature(self):
        self.assertEqual(str(get_signature(len)), "(obj, /)")

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            get_signature(42)


class TestGetParameterNames(unittest.TestCase):
    def test_names(self):
        def example(a, b, c=3):
            pass

        self.assertEqual(get_parameter_names(example), ["a", "b", "c"])

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            get_parameter_names(42)


class TestGetParameterKinds(unittest.TestCase):
    def test_kinds(self):
        def example(a, *args, b=1, **kwargs):
            pass

        kinds = get_parameter_kinds(example)
        self.assertEqual(kinds["a"], "POSITIONAL_OR_KEYWORD")
        self.assertEqual(kinds["args"], "VAR_POSITIONAL")
        self.assertEqual(kinds["b"], "KEYWORD_ONLY")
        self.assertEqual(kinds["kwargs"], "VAR_KEYWORD")


class TestCountParameters(unittest.TestCase):
    def test_count(self):
        def example(a, b, c=3):
            pass

        self.assertEqual(count_parameters(example), 3)

    def test_no_params(self):
        def example():
            pass

        self.assertEqual(count_parameters(example), 0)


class TestHasParameter(unittest.TestCase):
    def test_has(self):
        def example(a, b=1):
            pass

        self.assertTrue(has_parameter(example, "a"))
        self.assertTrue(has_parameter(example, "b"))
        self.assertFalse(has_parameter(example, "c"))

    def test_invalid_name(self):
        def example(a):
            pass

        with self.assertRaises(TypeError):
            has_parameter(example, 1)

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            has_parameter(42, "a")


class TestBindArguments(unittest.TestCase):
    def test_bind(self):
        def example(a, b=2, c=3):
            pass

        result = bind_arguments(example, 1, c=10)
        self.assertEqual(result, {"a": 1, "b": 2, "c": 10})

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            bind_arguments(42)

    def test_mismatch(self):
        def example(a):
            pass

        with self.assertRaises(TypeError):
            bind_arguments(example, 1, 2)


class TestIsBuiltin(unittest.TestCase):
    def test_builtin(self):
        self.assertTrue(is_builtin(len))

    def test_not_builtin(self):
        def example():
            pass

        self.assertFalse(is_builtin(example))

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            is_builtin(42)


class TestGetSourceFile(unittest.TestCase):
    def test_builtin_no_source(self):
        self.assertIsNone(get_source_file(len))

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            get_source_file(42)


class TestGetSourceLines(unittest.TestCase):
    def test_source_lines(self):
        def example():
            return 1

        result = get_source_lines(example)
        self.assertIsNotNone(result)
        lines, start = result
        self.assertIsInstance(lines, list)
        self.assertIsInstance(start, int)

    def test_builtin_no_source(self):
        self.assertIsNone(get_source_lines(len))

    def test_not_callable(self):
        with self.assertRaises(TypeError):
            get_source_lines(42)


if __name__ == "__main__":
    unittest.main()
