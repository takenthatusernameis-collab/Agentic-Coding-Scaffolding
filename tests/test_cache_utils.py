"""Tests for cache_utils module."""

import unittest

from cache_utils import cache_info, clear_cache, memoize


class TestMemoize(unittest.TestCase):
    def test_caches_repeated_calls(self) -> None:
        calls = [0]

        @memoize()
        def square(n: int) -> int:
            calls[0] += 1
            return n * n

        self.assertEqual(square(4), 16)
        self.assertEqual(square(4), 16)
        self.assertEqual(calls[0], 1)

    def test_different_args_recompute(self) -> None:
        calls = [0]

        @memoize()
        def add(a: int, b: int) -> int:
            calls[0] += 1
            return a + b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(calls[0], 2)

    def test_kwargs_normalized(self) -> None:
        calls = [0]

        @memoize()
        def greet(name: str, greeting: str = "Hello") -> str:
            calls[0] += 1
            return f"{greeting}, {name}!"

        # Same args, consistent kwarg order should hit the cache.
        self.assertEqual(greet("Alice", greeting="Hi"), "Hi, Alice!")
        self.assertEqual(greet("Alice", greeting="Hi"), "Hi, Alice!")
        self.assertEqual(calls[0], 1)

    def test_unbounded_cache(self) -> None:
        calls = [0]

        @memoize(maxsize=None)
        def double(n: int) -> int:
            calls[0] += 1
            return n * 2

        for i in range(50):
            self.assertEqual(double(i), i * 2)
        self.assertEqual(calls[0], 50)
        # Repeated calls should not recompute.
        for i in range(50):
            self.assertEqual(double(i), i * 2)
        self.assertEqual(calls[0], 50)

    def test_typed_distinct(self) -> None:
        calls = [0]

        @memoize(typed=True)
        def identity(value: object) -> object:
            calls[0] += 1
            return value

        self.assertEqual(identity(1), 1)
        self.assertEqual(identity(1.0), 1.0)
        self.assertEqual(calls[0], 2)

    def test_typed_false_collapses(self) -> None:
        calls = [0]

        @memoize(typed=False)
        def identity(value: object) -> object:
            calls[0] += 1
            return value

        self.assertEqual(identity(1), 1)
        self.assertEqual(identity(1.0), 1.0)
        self.assertEqual(calls[0], 1)

    def test_maxsize_eviction(self) -> None:
        calls = [0]

        @memoize(maxsize=2)
        def value(n: int) -> int:
            calls[0] += 1
            return n

        self.assertEqual(value(1), 1)
        self.assertEqual(value(2), 2)
        self.assertEqual(value(3), 3)
        # Accessing 1 again evicts the oldest (1) when 3 was added.
        self.assertEqual(value(1), 1)
        self.assertEqual(calls[0], 4)

    def test_clear_cache_method(self) -> None:
        calls = [0]

        @memoize()
        def triple(n: int) -> int:
            calls[0] += 1
            return n * 3

        self.assertEqual(triple(5), 15)
        self.assertEqual(triple(5), 15)
        self.assertEqual(calls[0], 1)
        triple.clear_cache()  # type: ignore[attr-defined]
        self.assertEqual(triple(5), 15)
        self.assertEqual(calls[0], 2)

    def test_cache_info_method(self) -> None:
        @memoize()
        def add(a: int, b: int) -> int:
            return a + b

        add(1, 1)
        add(2, 2)
        add(1, 1)  # hit
        info = add.cache_info()  # type: ignore[attr-defined]
        self.assertEqual(info["hits"], 1)
        self.assertEqual(info["misses"], 2)
        self.assertEqual(info["currsize"], 2)
        self.assertEqual(info["maxsize"], 128)

    def test_preserves_metadata(self) -> None:
        @memoize()
        def named(a: int) -> int:
            """Original docstring."""
            return a

        self.assertEqual(named.__name__, "named")
        self.assertEqual(named.__doc__, "Original docstring.")

    def test_invalid_maxsize_type_raises(self) -> None:
        with self.assertRaises(TypeError):
            memoize(maxsize="not-an-int")  # type: ignore[arg-type]

    def test_invalid_maxsize_value_raises(self) -> None:
        with self.assertRaises(ValueError):
            memoize(maxsize=0)
        with self.assertRaises(ValueError):
            memoize(maxsize=-5)

    def test_maxsize_none_allowed(self) -> None:
        @memoize(maxsize=None)
        def fn(x: int) -> int:
            return x

        self.assertEqual(fn(1), 1)
        self.assertEqual(fn.cache_info()["maxsize"], None)  # type: ignore[attr-defined]


class TestClearCacheFunction(unittest.TestCase):
    def test_clears_memoized_cache(self) -> None:
        calls = [0]

        @memoize()
        def inc(n: int) -> int:
            calls[0] += 1
            return n + 1

        inc(1)
        inc(1)
        self.assertEqual(calls[0], 1)
        clear_cache(inc)
        inc(1)
        self.assertEqual(calls[0], 2)

    def test_non_memoized_raises(self) -> None:
        def plain(x: int) -> int:
            return x

        with self.assertRaises(TypeError):
            clear_cache(plain)  # type: ignore[arg-type]


class TestCacheInfoFunction(unittest.TestCase):
    def test_returns_info_for_memoized(self) -> None:
        @memoize()
        def mul(a: int, b: int) -> int:
            return a * b

        mul(2, 3)
        info = cache_info(mul)
        self.assertEqual(info["misses"], 1)
        self.assertEqual(info["hits"], 0)

    def test_non_memoized_raises(self) -> None:
        def plain(x: int) -> int:
            return x

        with self.assertRaises(TypeError):
            cache_info(plain)  # type: ignore[arg-type]


class TestMemoizeExceptions(unittest.TestCase):
    def test_function_raising_is_not_cached(self) -> None:
        calls = [0]

        @memoize()
        def fail(x: int) -> int:
            calls[0] += 1
            if x < 0:
                raise ValueError("negative")
            return x

        self.assertEqual(fail(1), 1)
        with self.assertRaises(ValueError):
            fail(-1)
        with self.assertRaises(ValueError):
            fail(-1)
        self.assertEqual(calls[0], 3)


if __name__ == "__main__":
    unittest.main()
