"""Tests for asyncore_utils module."""

import unittest
from unittest import mock

import asyncore_utils
from test.support import asyncore


class TestExports(unittest.TestCase):
    def test_classes_exported(self):
        self.assertIs(asyncore_utils.dispatcher, asyncore.dispatcher)
        self.assertIs(asyncore_utils.dispatcher_with_send, asyncore.dispatcher_with_send)
        self.assertIs(asyncore_utils.file_dispatcher, asyncore.file_dispatcher)

    def test_functions_exported(self):
        self.assertIs(asyncore_utils.loop, asyncore.loop)
        self.assertIs(asyncore_utils.poll, asyncore.poll)


class TestCreateDispatcher(unittest.TestCase):
    def test_create_dispatcher(self):
        with mock.patch("asyncore_utils.dispatcher") as m:
            m.return_value = mock.sentinel.dispatcher
            result = asyncore_utils.create_dispatcher()
            self.assertIs(result, mock.sentinel.dispatcher)

    def test_create_dispatcher_bad_types(self):
        with self.assertRaises(TypeError):
            asyncore_utils.create_dispatcher(map=[])  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
