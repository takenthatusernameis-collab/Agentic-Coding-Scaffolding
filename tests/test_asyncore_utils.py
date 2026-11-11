"""Tests for asyncore_utils."""

from __future__ import annotations

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
        for name in ("loop", "poll", "read", "write", "close_all", "select",
                     "poll2", "poll3", "socket_map", "ExitNow", "errorcode"):
            self.assertTrue(hasattr(asyncore_utils, name), f"{name} not exported")

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


if __name__ == "__main__":
    unittest.main()
