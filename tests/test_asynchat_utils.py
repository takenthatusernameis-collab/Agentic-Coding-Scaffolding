"""Tests for asynchat_utils."""

from __future__ import annotations

import importlib
import sys
import unittest
from unittest import mock

import asynchat_utils


class TestAsynchatUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in asynchat_utils.__all__:
            self.assertTrue(hasattr(asynchat_utils, name), f"{name} not exported")
        self.assertIn("is_available", asynchat_utils.__all__)

    def test_all_is_sorted_and_complete(self) -> None:
        expected = [
            "async_chat",
            "deque",
            "find_prefix_at_end",
            "is_available",
            "simple_producer",
        ]
        self.assertEqual(sorted(asynchat_utils.__all__), expected)

    def test_is_available(self) -> None:
        self.assertIsInstance(asynchat_utils.is_available(), bool)
        self.assertEqual(
            asynchat_utils.is_available(),
            asynchat_utils._ASYNCHAT_AVAILABLE,  # type: ignore[attr-defined]
        )

    def test_deque_is_real_deque_when_available(self) -> None:
        from collections import deque

        if not asynchat_utils.is_available():
            self.skipTest("asynchat module is not available on this interpreter")
        self.assertIs(asynchat_utils.deque, deque)

    def test_unavailable_helpers_raise_runtime_error(self) -> None:
        if asynchat_utils.is_available():
            self.skipTest("asynchat module is available on this interpreter")
        names = ("async_chat", "find_prefix_at_end", "simple_producer")
        for name in names:
            with self.subTest(name=name):
                with self.assertRaises(RuntimeError) as ctx:
                    getattr(asynchat_utils, name)()
                self.assertIn("asynchat module is not available", str(ctx.exception))

    def test_deque_is_none_when_unavailable(self) -> None:
        if asynchat_utils.is_available():
            self.skipTest("asynchat module is available on this interpreter")
        self.assertIsNone(asynchat_utils.deque)

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"asynchat": None}):
                reloaded = importlib.reload(asynchat_utils)
                self.assertIs(reloaded.is_available(), False)
                for name in ("async_chat", "find_prefix_at_end", "simple_producer"):
                    with self.subTest(name=name):
                        with self.assertRaises(RuntimeError) as ctx:
                            getattr(reloaded, name)()
                        self.assertIn(
                            "asynchat module is not available", str(ctx.exception)
                        )
                self.assertIsNone(reloaded.deque)
        finally:
            importlib.reload(asynchat_utils)


class TestUnavailableFallback(unittest.TestCase):
    """Exercise the active fallback when the stdlib ``asynchat`` module is absent."""

    def test_fallback_helpers_raise_runtime_error(self) -> None:
        if asynchat_utils.is_available():
            self.skipTest("asynchat module is available on this interpreter")
        names = ("async_chat", "find_prefix_at_end", "simple_producer")
        for name in names:
            with self.subTest(name=name):
                with self.assertRaises(RuntimeError) as ctx:
                    getattr(asynchat_utils, name)()
                self.assertIn("asynchat module is not available", str(ctx.exception))

    def test_fallback_deque_is_none(self) -> None:
        if asynchat_utils.is_available():
            self.skipTest("asynchat module is available on this interpreter")
        self.assertIsNone(asynchat_utils.deque)


if __name__ == "__main__":
    unittest.main()
