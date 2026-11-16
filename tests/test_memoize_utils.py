import unittest
from typing import TypeVar

from memoize_utils import T, lru_memoize, memoize


class TestMemoize(unittest.TestCase):
    def test_caches_result(self):
        calls = []

        @memoize
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        self.assertEqual(compute(5), 10)
        self.assertEqual(compute(5), 10)
        self.assertEqual(len(calls), 1)

    def test_different_args_recompute(self):
        calls = []

        @memoize
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        self.assertEqual(compute(5), 10)
        self.assertEqual(compute(6), 12)
        self.assertEqual(len(calls), 2)

    def test_kwargs_cached(self):
        calls = []

        @memoize
        def compute(x: int, y: int = 0) -> int:
            calls.append((x, y))
            return x + y

        self.assertEqual(compute(1, y=2), 3)
        self.assertEqual(compute(1, y=2), 3)
        self.assertEqual(len(calls), 1)

    def test_cache_clear(self):
        calls = []

        @memoize
        def compute() -> int:
            calls.append(1)
            return len(calls)

        self.assertEqual(compute(), 1)
        self.assertEqual(compute(), 1)
        compute.cache_clear()
        self.assertEqual(compute(), 2)
        self.assertEqual(len(calls), 2)

    def test_non_callable_raises(self):
        with self.assertRaises(TypeError):
            memoize(42)  # type: ignore[arg-type]

    def test_memoize_kwargs_order_invariance(self):
        calls = []

        @memoize
        def compute(x: int, y: int) -> int:
            calls.append((x, y))
            return x + y

        self.assertEqual(compute(x=1, y=2), 3)
        self.assertEqual(compute(y=2, x=1), 3)
        self.assertEqual(len(calls), 1)

    def test_memoize_preserves_function_metadata(self):
        def compute(x: int) -> int:
            """Compute docstring."""
            return x

        wrapped = memoize(compute)
        self.assertEqual(wrapped.__name__, "compute")
        self.assertEqual(wrapped.__doc__, "Compute docstring.")


if __name__ == "__main__":
    unittest.main()


class TestLruMemoize(unittest.TestCase):
    def test_caches_result(self):
        calls = []

        @lru_memoize
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        self.assertEqual(compute(5), 10)
        self.assertEqual(compute(5), 10)
        self.assertEqual(len(calls), 1)

    def test_no_parens_kwargs_order_invariance(self):
        calls = []

        @lru_memoize
        def compute(x: int, y: int = 0) -> int:
            calls.append((x, y))
            return x + y

        self.assertEqual(compute(x=1, y=2), 3)
        self.assertEqual(compute(y=2, x=1), 3)
        self.assertEqual(len(calls), 1)

    def test_no_parens_preserves_metadata(self):
        @lru_memoize
        def compute(x: int) -> int:
            """Compute docstring."""
            return x

        self.assertEqual(compute.__name__, "compute")
        self.assertEqual(compute.__doc__, "Compute docstring.")
        self.assertTrue(callable(compute.cache_clear))  # type: ignore[attr-defined]

    def test_callable_with_maxsize_argument(self):
        calls = []

        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        wrapped = lru_memoize(compute, maxsize=2)
        self.assertEqual(wrapped(1), 2)
        self.assertEqual(wrapped(1), 2)
        self.assertEqual(len(calls), 1)

    def test_evicts_lru(self):
        calls = []

        @lru_memoize(maxsize=2)
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        compute(1)
        compute(2)
        compute(3)
        calls_before = len(calls)
        compute(1)
        self.assertEqual(len(calls), calls_before + 1)

    def test_maxsize_zero_disables_cache(self):
        calls = []

        @lru_memoize(maxsize=0)
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        compute(5)
        compute(5)
        self.assertEqual(len(calls), 2)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            lru_memoize("not callable")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lru_memoize(lambda x: x, maxsize="a")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            lru_memoize(lambda x: x, maxsize=-1)

    def test_lru_memoize_cache_clear(self):
        calls = []

        @lru_memoize(maxsize=2)
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        compute(1)
        compute(1)
        compute.cache_clear()
        compute(1)
        self.assertEqual(len(calls), 2)


class TestExportedTypeVars(unittest.TestCase):
    def test_t_typevar(self) -> None:
        self.assertIsInstance(T, TypeVar)
        self.assertEqual(T.__name__, "T")
