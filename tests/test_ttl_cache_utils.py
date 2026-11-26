"""Tests for ttl_cache_utils module."""

import time
import unittest
from typing import Optional

from ttl_cache_utils import Expired, TTLCache, ttl_cache


class _SteppingCache(TTLCache):
    """A TTLCache with a manually advanced clock for deterministic tests."""

    def __init__(self, ttl: float, maxsize: Optional[int] = 128) -> None:
        super().__init__(ttl=ttl, maxsize=maxsize)
        self._clock = 0.0

    def _now(self) -> float:
        return self._clock

    def advance(self, seconds: float) -> None:
        self._clock += seconds


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

    def test_clear_resets_statistics(self) -> None:
        cache = TTLCache(ttl=0.01)
        cache["a"] = 1
        cache["a"]  # hit
        with self.assertRaises(KeyError):
            cache["missing"]  # miss
        time.sleep(0.02)
        self.assertFalse("a" in cache)  # expired
        self.assertEqual(cache.cache_info()["expired"], 1)
        cache.clear()
        info = cache.cache_info()
        self.assertEqual(info["hits"], 0)
        self.assertEqual(info["misses"], 0)
        self.assertEqual(info["expired"], 0)
        self.assertEqual(info["currsize"], 0)

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

    def test_views_do_not_change_statistics(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        cache["b"] = 2
        cache.keys()
        cache.values()
        cache.items()
        info = cache.cache_info()
        self.assertEqual(info["hits"], 0)
        self.assertEqual(info["misses"], 0)
        self.assertEqual(info["currsize"], 2)

    def test_views_do_not_expire_entries_mid_iteration(self) -> None:
        class SteppingCache(TTLCache):
            def __init__(self, ttl: float) -> None:
                super().__init__(ttl=ttl)
                self.time = 0.0
                self.step = 0.0

            def _now(self) -> float:
                self.time += self.step
                return self.time

        for method in ("values", "items"):
            cache = SteppingCache(ttl=10)
            cache["a"] = 1
            cache["b"] = 2
            cache.step = 4.0
            result = getattr(cache, method)()
            self.assertEqual(len(result), 2, msg=method)
            self.assertEqual(cache.cache_info()["hits"], 0, msg=method)

    def test_validation(self) -> None:
        with self.assertRaises(TypeError):
            TTLCache(ttl=True)
        with self.assertRaises(TypeError):
            TTLCache(ttl="10")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            TTLCache(ttl=-1)
        with self.assertRaises(ValueError):
            TTLCache(ttl=float("nan"))
        with self.assertRaises(ValueError):
            TTLCache(ttl=float("inf"))
        with self.assertRaises(ValueError):
            TTLCache(ttl=float("-inf"))
        with self.assertRaises(TypeError):
            TTLCache(ttl=10, maxsize=True)
        with self.assertRaises(ValueError):
            TTLCache(ttl=10, maxsize=0)

    def test_expire_rejects_non_finite_ttl(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        with self.assertRaises(TypeError):
            cache.expire("a", True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            cache.expire("a", float("nan"))
        with self.assertRaises(ValueError):
            cache.expire("a", float("inf"))
        with self.assertRaises(ValueError):
            cache.expire("a", float("-inf"))

    def test_expire_rejects_negative_ttl(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        with self.assertRaises(ValueError):
            cache.expire("a", -1)

    def test_expire_defaults_to_configured_ttl(self) -> None:
        cache = _SteppingCache(ttl=10)
        cache["a"] = 1
        cache.advance(11)  # entry now expired
        cache.expire("a")  # refresh using the cache's configured ttl
        self.assertTrue("a" in cache)

    def test_len_purges_expired_entries(self) -> None:
        cache = _SteppingCache(ttl=10)
        cache["a"] = 1
        cache.advance(11)
        self.assertEqual(len(cache), 0)
        self.assertEqual(cache.cache_info()["expired"], 1)

    def test_setitem_updates_existing_key(self) -> None:
        cache = TTLCache(ttl=60)
        cache["a"] = 1
        cache["a"] = 2  # update path for an existing key
        self.assertEqual(cache["a"], 2)
        self.assertEqual(len(cache), 1)

    def test_delitem_expired_raises_keyerror(self) -> None:
        cache = _SteppingCache(ttl=10)
        cache["a"] = 1
        cache.advance(11)
        with self.assertRaises(KeyError):
            del cache["a"]
        self.assertEqual(cache.cache_info()["expired"], 1)

    def test_pop_expired_returns_default(self) -> None:
        cache = _SteppingCache(ttl=10)
        cache["a"] = 1
        cache.advance(11)
        self.assertIsNone(cache.pop("a"))
        self.assertEqual(cache.cache_info()["expired"], 1)


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
        self.assertEqual(compute.cache_info()["hits"], 0)  # type: ignore[attr-defined]
        compute(1)
        self.assertEqual(compute.cache_info()["hits"], 1)  # type: ignore[attr-defined]
        compute.cache_clear()  # type: ignore[attr-defined]
        self.assertEqual(compute.cache_info()["currsize"], 0)  # type: ignore[attr-defined]
        self.assertEqual(compute.cache_info()["hits"], 0)  # type: ignore[attr-defined]
        self.assertEqual(compute.cache_info()["misses"], 0)  # type: ignore[attr-defined]

    def test_validation(self) -> None:
        with self.assertRaises(TypeError):
            ttl_cache(ttl=True)
        with self.assertRaises(ValueError):
            ttl_cache(ttl=-1)
        with self.assertRaises(ValueError):
            ttl_cache(ttl=float("nan"))
        with self.assertRaises(ValueError):
            ttl_cache(ttl=float("inf"))
        with self.assertRaises(ValueError):
            ttl_cache(ttl=float("-inf"))

    def test_validation_maxsize(self) -> None:
        with self.assertRaises(TypeError):
            ttl_cache(ttl=60, maxsize=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ttl_cache(ttl=60, maxsize=0)


if __name__ == "__main__":
    unittest.main()
