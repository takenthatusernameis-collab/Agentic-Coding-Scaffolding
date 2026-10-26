"""Tests for asynchat_utils module."""

import unittest

import asynchat_utils
from test.support import asynchat


class TestAsynchatUtils(unittest.TestCase):
    def test_exports(self):
        self.assertIs(asynchat_utils.async_chat, asynchat.async_chat)
        self.assertIs(asynchat_utils.find_prefix_at_end, asynchat.find_prefix_at_end)
        self.assertIs(asynchat_utils.simple_producer, asynchat.simple_producer)
        self.assertIs(asynchat_utils.deque, asynchat.deque)


if __name__ == "__main__":
    unittest.main()
