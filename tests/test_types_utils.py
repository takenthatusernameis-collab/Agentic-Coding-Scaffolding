"""Tests for types_utils."""

import types
import unittest

from types_utils import (
    is_coroutine,
    is_function,
    is_generator,
    is_lambda,
    is_method,
    new_class,
    new_function,
    simple_namespace,
)


class TestTypesUtils(unittest.TestCase):
    def test_new_class(self):
        cls = new_class("Foo", (object,))
        self.assertEqual(cls.__name__, "Foo")
        self.assertTrue(issubclass(cls, object))

    def test_new_class_exec_body(self):
        def body(ns):
            ns["x"] = 5

        cls = new_class("Bar", (), exec_body=body)
        self.assertEqual(cls.x, 5)

    def test_new_class_validation(self):
        with self.assertRaises(TypeError):
            new_class(123)
        with self.assertRaises(TypeError):
            new_class("X", "bases")
        with self.assertRaises(TypeError):
            new_class("X", (), exec_body="nope")

    def test_new_function(self):
        code2 = compile("def f():\n    return 7\n", "<f>", "exec")
        ns = {}
        exec(code2, ns)
        func = new_function(ns["f"].__code__, {"__builtins__": __builtins__})
        self.assertEqual(func(), 7)

    def test_new_function_validation(self):
        code = compile("pass", "<f>", "exec")
        with self.assertRaises(TypeError):
            new_function(code, "notdict")
        with self.assertRaises(TypeError):
            new_function(code, {}, name=123)

    def test_is_function(self):
        def f():
            pass

        self.assertTrue(is_function(f))
        self.assertFalse(is_function(42))

    def test_is_method(self):
        class C:
            def m(self):
                pass

        self.assertTrue(is_method(C().m))
        self.assertFalse(is_method(42))

    def test_is_generator(self):
        def g():
            yield 1

        self.assertTrue(is_generator(g()))
        self.assertFalse(is_generator(42))

    def test_is_coroutine(self):
        async def c():
            return 1


        coro = c()
        self.assertTrue(is_coroutine(coro))
        coro.close()
        self.assertFalse(is_coroutine(42))

    def test_is_lambda(self):
        self.assertTrue(is_lambda(lambda x: x))
        self.assertFalse(is_lambda(42))

    def test_simple_namespace(self):
        ns = simple_namespace(a=1, b=2)
        self.assertEqual(ns.a, 1)
        self.assertEqual(ns.b, 2)
        self.assertIsInstance(ns, types.SimpleNamespace)


if __name__ == "__main__":
    unittest.main()
