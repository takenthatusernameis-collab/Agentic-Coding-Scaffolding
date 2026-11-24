"""Tests for functools_utils module."""

import unittest
from typing import TypeVar

from functools_utils import R, T, apply, compose, curry, pipe


class TestCompose(unittest.TestCase):
    def test_compose_basic(self) -> None:
        def add_one(x: int) -> int:
            return x + 1

        def multiply_by_two(x: int) -> int:
            return x * 2

        composed = compose(multiply_by_two, add_one)
        self.assertEqual(composed(3), 8)

    def test_compose_single_function(self) -> None:
        def double(x: int) -> int:
            return x * 2

        composed = compose(double)
        self.assertEqual(composed(5), 10)

    def test_compose_multiple_functions(self) -> None:
        def add_one(x: int) -> int:
            return x + 1

        def double(x: int) -> int:
            return x * 2

        def subtract_three(x: int) -> int:
            return x - 3

        composed = compose(subtract_three, double, add_one)
        self.assertEqual(composed(4), 7)

    def test_compose_no_functions_raises(self) -> None:
        with self.assertRaises(ValueError):
            compose()


class TestPipe(unittest.TestCase):
    def test_pipe_basic(self) -> None:
        def add_one(x: int) -> int:
            return x + 1

        def multiply_by_two(x: int) -> int:
            return x * 2

        result = pipe(3, add_one, multiply_by_two)
        self.assertEqual(result, 8)

    def test_pipe_no_functions(self) -> None:
        result = pipe(5)
        self.assertEqual(result, 5)

    def test_pipe_multiple_functions(self) -> None:
        def double(x: int) -> int:
            return x * 2

        def add_three(x: int) -> int:
            return x + 3

        def subtract_one(x: int) -> int:
            return x - 1

        result = pipe(2, double, add_three, subtract_one)
        self.assertEqual(result, 6)


class TestCurry(unittest.TestCase):
    def test_curry_simple_function(self) -> None:
        def add(x: int, y: int) -> int:
            return x + y

        curried = curry(add)
        self.assertEqual(curried(1)(2), 3)

    def test_curry_full_application_immediate(self) -> None:
        def add(x: int, y: int) -> int:
            return x + y

        curried = curry(add)
        self.assertEqual(curried(1, 2), 3)

    def test_curry_three_args(self) -> None:
        def multiply(a: int, b: int, c: int) -> int:
            return a * b * c

        curried = curry(multiply)
        self.assertEqual(curried(2)(3)(4), 24)
        self.assertEqual(curried(2, 3)(4), 24)
        self.assertEqual(curried(2)(3, 4), 24)

    def test_curry_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            curry("not callable")  # type: ignore[arg-type]

    def test_curry_builtin_function(self) -> None:
        curried = curry(len)
        self.assertEqual(curried([1, 2, 3]), 3)

    def test_curry_with_default_args(self) -> None:
        def add(x: int, y: int, z: int = 10) -> int:
            return x + y + z

        curried = curry(add)
        # Standard currying: call when all required args are satisfied;
        # defaults apply for any remaining parameters.
        self.assertEqual(curried(1)(2), 13)
        self.assertEqual(curried(1, 2), 13)
        self.assertEqual(curried(1)(2, 3), 6)
        self.assertEqual(curried(1, 2, 3), 6)

    def test_curry_with_keyword_only_args(self) -> None:
        def func(a: int, *, b: int = 5) -> int:
            return a + b

        curried = curry(func)
        # b has a default, so supplying a alone completes the call.
        self.assertEqual(curried(1), 6)
        self.assertEqual(curried(1, b=2), 3)

    def test_curry_with_varargs(self) -> None:
        def total(*values: int) -> int:
            return sum(values)

        curried = curry(total)
        # Variadic functions have no required parameters, so the first
        # application is already a complete call.
        self.assertEqual(curried(1), 1)
        self.assertEqual(curried(1, 2, 3), 6)


class TestApply(unittest.TestCase):
    def test_apply_basic(self) -> None:
        result = apply(lambda x: x * 2, 5)
        self.assertEqual(result, 10)

    def test_apply_non_callable_raises(self) -> None:
        with self.assertRaises(TypeError):
            apply("not callable", 5)  # type: ignore[arg-type]


class TestExportedTypeVars(unittest.TestCase):
    def test_r_typevar(self) -> None:
        self.assertIsInstance(R, TypeVar)
        self.assertEqual(R.__name__, "R")

    def test_t_typevar(self) -> None:
        self.assertIsInstance(T, TypeVar)
        self.assertEqual(T.__name__, "T")


if __name__ == "__main__":
    unittest.main()
