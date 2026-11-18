"""Tests for ttl_cache_utils module."""

import time
import unittest

from ttl_cache_utils import Expired, TTLCache, ttl_cache


class TestTTLCache(unittest.TestCase):
    def test_set_and_get(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        self.assertEqual(cache["a"], 1)

    def test_get_missing_raises_keyerror(self) -> None:
        cache = TTLCache(ttl=60)
        with self.assertRaises(KeyError):
            cache["missing"]

    def test_get_returns_default(self) -> None:
        cache = TTLCache(ttl=60)
        self.assertIsNone(cache.get("missing"))
        self.assertEqual(cache.get("missing", "fallback"), "fallback")

    def test_contains(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        self.assertTrue("a" in cache)
        self.assertFalse("b" in cache)

    def test_len(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        cache["b"] = 2
        self.assertEqual(len(cache), 2)

    def test_delitem(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        del cache["a"]
        self.assertFalse("a" in cache)
        with self.assertRaises(KeyError):
            del cache["a"]

    def test_pop(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        self.assertEqual(cache.pop("a"), 1)
        self.assertFalse("a" in cache)
        self.assertIsNone(cache.pop("missing"))
        self.assertEqual(cache.pop("missing", "default"), "default")

    def test_expiration(self) -> None:
        cache = TTLCache(ttl=0.01)
        cache["a"] = 1
        self.assertEqual(cache["a"], 1)
        time.sleep(0.02)
        with self.assertRaises(Expired):
            cache["a"]
        self.assertFalse("a" in cache)
        self.assertIsNone(cache.get("a"))

    def test_lru_eviction(self) -> None:
        cache = TTLCache(ttl=60, maxsize=2)
        cache["a"] = 1
        cache["b"] = 2
        cache["a"]  # touch "a", making "b" the least-recently-used entry
        cache["c"] = 3  # evicts "b"
        self.assertFalse("b" in cache)
        self.assertTrue("a" in cache)
        self.assertTrue("c" in cache)
        self.assertEqual(len(cache), 2)

    def test_expire_refreshes_ttl(self) -> None:
        cache = TTLCache(ttl=0.01)
        cache["a"] = 1
        time.sleep(0.02)
        cache.expire("a", 60)
        self.assertTrue("a" in cache)
        with self.assertRaises(KeyError):
            cache.expire("missing", 60)

    def test_clear(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        cache.clear()
        self.assertEqual(len(cache), 0)
        self.assertEqual(cache.cache_info()["currsize"], 0)

    def test_cache_info(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        cache["a"]  # hit
        with self.assertRaises(KeyError):
            cache["missing"]  # miss
        info = cache.cache_info()
        self.assertEqual(info["hits"], 1)
        self.assertEqual(info["misses"], 1)
        self.assertEqual(info["currsize"], 1)

    def test_iter_keys_values_items(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        cache["b"] = 2
        self.assertEqual(sorted(cache.keys()), ["a", "b"])
        self.assertEqual(sorted(cache.values()), [1, 2])
        self.assertEqual(sorted(cache.items()), [("a", 1), ("b", 2)])
        self.assertEqual(list(cache), ["a", "b"])

    def test_validation(self) -> None:
        with self.assertRaises(TypeError):
            TTLCache(ttl=True)
        with self.assertRaises(TypeError):
            TTLCache(ttl="10")
        with self.assertRaises(ValueError):
            TTLCache(ttl=-1)
        with self.assertRaises(TypeError):
            TTLCache(ttl=10, maxsize=True)
        with self.assertRaises(ValueError):
            TTLCache(ttl=10, maxsize=0)


class TestTTLCacheDecorator(unittest.TestCase):
    def test_caches_result(self) -> None:
        calls: list[int] = []

        @ttl_cache(ttl=60)
        def compute(x: int) -> int:
            calls.append(x)
            return x * 2

        self.assertEqual(compute(5), 10)
        self.assertEqual(compute(5), 10)
        self.assertEqual(calls, [5])

    def test_cache_clear_and_info(self) -> None:
        @ttl_cache(ttl=60)
        def compute(x: int) -> int:
            return x

        compute(1)
        self.assertEqual(compute.cache_info()["hits"], 0)
        compute(1)
        self.assertEqual(compute.cache_info()["hits"], 1)
        compute.cache_clear()
        self.assertEqual(compute.cache_info()["currsize"], 0)

    def test_validation(self) -> None:
        with self.assertRaises(TypeError):
            ttl_cache(ttl=True)
        with self.assertRaises(ValueError):
            ttl_cache(ttl=-1)


if __name__ == "__main__":
    unittest.main()
