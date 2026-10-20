"""Tests for select_utils module."""

import os
import select
import unittest

import select_utils


class TestSelect(unittest.TestCase):
    def test_select_returns_lists(self):
        read_fd, write_fd = os.pipe()
        try:
            readable, writable, exceptional = select_utils.select(
                [read_fd], [write_fd], [], 0
            )
            self.assertIsInstance(readable, list)
            self.assertIsInstance(writable, list)
            self.assertIsInstance(exceptional, list)
        finally:
            os.close(read_fd)
            os.close(write_fd)

    def test_select_no_timeout(self):
        read_fd, write_fd = os.pipe()
        try:
            readable, writable, exceptional = select_utils.select(
                [read_fd], [write_fd], [], 0
            )
            self.assertTrue(all(isinstance(fd, int) for fd in readable + writable + exceptional))
            self.assertIn(write_fd, writable)
        finally:
            os.close(read_fd)
            os.close(write_fd)

    def test_select_invalid_rlist(self):
        with self.assertRaises(TypeError):
            select_utils.select("not-a-list", [], [], 0)  # type: ignore[arg-type]

    def test_select_list_with_non_int(self):
        with self.assertRaises(TypeError):
            select_utils.select([1, "two"], [], [], 0)

    def test_select_timeout_negative(self):
        with self.assertRaises(ValueError):
            select_utils.select([], [], [], -1)

    def test_select_timeout_bool(self):
        with self.assertRaises(TypeError):
            select_utils.select([], [], [], True)  # type: ignore[arg-type]

    def test_select_os_error_on_bad_fd(self):
        with self.assertRaises((OSError, ValueError)):
            select_utils.select([999999], [], [], 0)

    def test_pipe_buf_is_int(self):
        self.assertIsInstance(select_utils.PIPE_BUF, int)
        self.assertGreater(select_utils.PIPE_BUF, 0)


class TestPoller(unittest.TestCase):
    def test_create_poller(self):
        poller = select_utils.create_poller()
        self.assertTrue(hasattr(poller, "register"))
        self.assertTrue(hasattr(poller, "poll"))

    def test_poller_register_and_poll(self):
        read_fd, write_fd = os.pipe()
        poller = select_utils.create_poller()
        try:
            select_utils.poll_register(poller, read_fd, select.POLLIN)
            ready = select_utils.poll_poll(poller, 0)
            self.assertEqual(ready, [])
        finally:
            os.close(read_fd)
            os.close(write_fd)

    def test_poller_register_invalid_fd(self):
        poller = select_utils.create_poller()
        with self.assertRaises(TypeError):
            select_utils.poll_register(poller, "fd", select.POLLIN)  # type: ignore[arg-type]

    def test_poller_register_invalid_events(self):
        poller = select_utils.create_poller()
        with self.assertRaises(TypeError):
            select_utils.poll_register(poller, 3, "events")  # type: ignore[arg-type]

    def test_poller_register_bad_poller(self):
        with self.assertRaises(TypeError):
            select_utils.poll_register("not-a-poller", 3, select.POLLIN)  # type: ignore[arg-type]

    def test_poll_poll_bad_poller(self):
        with self.assertRaises(TypeError):
            select_utils.poll_poll("not-a-poller", 0)  # type: ignore[arg-type]

    def test_poll_timeout_negative(self):
        poller = select_utils.create_poller()
        with self.assertRaises(ValueError):
            select_utils.poll_poll(poller, -1)


if __name__ == "__main__":
    unittest.main()
