"""Tests for asyncore_utils."""

from __future__ import annotations

import importlib
import sys
import unittest
from unittest import mock

import asyncore_utils


class TestExports(unittest.TestCase):
    def test_classes_exported(self) -> None:
        self.assertTrue(callable(asyncore_utils.dispatcher))
        self.assertTrue(callable(asyncore_utils.dispatcher_with_send))
        self.assertTrue(callable(asyncore_utils.file_dispatcher))
        self.assertTrue(callable(asyncore_utils.file_wrapper))

    def test_functions_exported(self) -> None:
        for name in (
            "loop",
            "poll",
            "read",
            "write",
            "close_all",
            "select",
            "poll2",
            "poll3",
            "socket_map",
            "ExitNow",
            "errorcode",
            "is_available",
        ):
            self.assertTrue(hasattr(asyncore_utils, name), f"{name} not exported")
        self.assertIn("is_available", asyncore_utils.__all__)

    def test_is_available(self) -> None:
        self.assertIsInstance(asyncore_utils.is_available(), bool)
        self.assertEqual(
            asyncore_utils.is_available(),
            asyncore_utils._ASYNCHORE_AVAILABLE,  # type: ignore[attr-defined]
        )

    def test_create_dispatcher_helper_exported(self) -> None:
        self.assertTrue(callable(asyncore_utils.create_dispatcher))


class TestCreateDispatcher(unittest.TestCase):
    def test_create_dispatcher_calls_dispatcher(self) -> None:
        with mock.patch("asyncore_utils.dispatcher") as mocked:
            mocked.return_value = mock.sentinel.dispatcher
            result = asyncore_utils.create_dispatcher()
            self.assertIs(result, mock.sentinel.dispatcher)
            mocked.assert_called_once()

    def test_create_dispatcher_passes_map(self) -> None:
        sentinel_map = {"fd": "x"}
        with mock.patch("asyncore_utils.dispatcher") as mocked:
            mocked.return_value = mock.sentinel.dispatcher
            asyncore_utils.create_dispatcher(map=sentinel_map)
            _, kwargs = mocked.call_args
            self.assertIs(kwargs["map"], sentinel_map)

    def test_create_dispatcher_bad_types(self) -> None:
        with self.assertRaises(TypeError):
            asyncore_utils.create_dispatcher(map=[])  # type: ignore[arg-type]

    def test_create_dispatcher_accepts_none(self) -> None:
        with mock.patch("asyncore_utils.dispatcher") as mocked:
            mocked.return_value = mock.sentinel.dispatcher
            result = asyncore_utils.create_dispatcher(map=None)
            self.assertIs(result, mock.sentinel.dispatcher)


class TestUnavailableFallback(unittest.TestCase):
    """Exercise the active fallback when the stdlib ``asyncore`` module is absent."""

    def test_fallback_helpers_raise_runtime_error(self) -> None:
        if asyncore_utils.is_available():
            self.skipTest("asyncore module is available on this interpreter")
        names = (
            "dispatcher",
            "dispatcher_with_send",
            "file_dispatcher",
            "file_wrapper",
            "loop",
            "poll",
            "read",
            "write",
            "close_all",
            "select",
            "poll2",
            "poll3",
        )
        for name in names:
            with self.subTest(name=name):
                with self.assertRaises(RuntimeError) as ctx:
                    getattr(asyncore_utils, name)()
                self.assertIn("asyncore module is not available", str(ctx.exception))

    def test_fallback_constants(self) -> None:
        if asyncore_utils.is_available():
            self.skipTest("asyncore module is available on this interpreter")
        self.assertEqual(asyncore_utils.socket_map, {})
        self.assertEqual(asyncore_utils.errorcode, {})
        self.assertIs(asyncore_utils.ExitNow, RuntimeError)

    def test_create_dispatcher_raises_when_unavailable(self) -> None:
        if asyncore_utils.is_available():
            self.skipTest("asyncore module is available on this interpreter")
        with self.assertRaises(RuntimeError):
            asyncore_utils.create_dispatcher()
        with self.assertRaises(RuntimeError):
            asyncore_utils.create_dispatcher(map={})

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"asyncore": None}):
                reloaded = importlib.reload(asyncore_utils)
                self.assertIs(reloaded.is_available(), False)
                names = (
                    "dispatcher",
                    "dispatcher_with_send",
                    "file_dispatcher",
                    "file_wrapper",
                    "loop",
                    "poll",
                    "read",
                    "write",
                    "close_all",
                    "select",
                    "poll2",
                    "poll3",
                )
                for name in names:
                    with self.subTest(name=name):
                        with self.assertRaises(RuntimeError) as ctx:
                            getattr(reloaded, name)()
                        self.assertIn(
                            "asyncore module is not available", str(ctx.exception)
                        )
                self.assertEqual(reloaded.socket_map, {})
                self.assertEqual(reloaded.errorcode, {})
                self.assertIs(reloaded.ExitNow, RuntimeError)
                with self.assertRaises(RuntimeError):
                    reloaded.create_dispatcher()
                with self.assertRaises(RuntimeError):
                    reloaded.create_dispatcher(map={})
        finally:
            importlib.reload(asyncore_utils)


if __name__ == "__main__":
    unittest.main()
