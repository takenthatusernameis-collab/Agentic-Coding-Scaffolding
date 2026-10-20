"""Tests for pty_utils."""

import os
import unittest
from unittest.mock import patch

from pty_utils import (
    CHILD,
    STDERR_FILENO,
    STDIN_FILENO,
    STDOUT_FILENO,
    ForkResult,
    fork,
    is_available,
    master_open,
    open_terminal,
    openpty,
    slave_open,
    spawn,
)


class TestPtyUtils(unittest.TestCase):
    """Verify the pseudo-terminal helpers of the wrapper."""

    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)
        self.assertEqual(is_available(), is_available())

    def test_the_file_descriptor_constants(self):
        self.assertEqual(STDIN_FILENO, 0)
        self.assertEqual(STDOUT_FILENO, 1)
        self.assertEqual(STDERR_FILENO, 2)
        self.assertEqual(CHILD, 0)

    def test_the_fork_result_is_a_named_tuple(self):
        result = ForkResult(pid=1, master_fd=2)
        self.assertEqual(result.pid, 1)
        self.assertEqual(result.master_fd, 2)
        self.assertEqual(tuple(result), (1, 2))

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_openpty_returns_two_descriptors(self):
        master_fd, slave_fd = openpty()
        try:
            self.assertIsInstance(master_fd, int)
            self.assertIsInstance(slave_fd, int)
            self.assertGreaterEqual(master_fd, 0)
            self.assertGreaterEqual(slave_fd, 0)
            self.assertNotEqual(master_fd, slave_fd)
        finally:
            os.close(master_fd)
            os.close(slave_fd)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_open_terminal_matches_openpty(self):
        master_fd, slave_fd = open_terminal()
        try:
            self.assertIsInstance(master_fd, int)
            self.assertIsInstance(slave_fd, int)
        finally:
            os.close(master_fd)
            os.close(slave_fd)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_master_open_returns_the_name_and_the_descriptor(self):
        name, master_fd = master_open()
        try:
            self.assertIsInstance(name, str)
            self.assertTrue(name)
            self.assertIsInstance(master_fd, int)
            self.assertGreaterEqual(master_fd, 0)
        finally:
            os.close(master_fd)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_slave_open_reopens_the_slave_device(self):
        name, master_fd = master_open()
        try:
            slave_fd = slave_open(name)
            self.assertIsInstance(slave_fd, int)
            self.assertGreaterEqual(slave_fd, 0)
            os.close(slave_fd)
        finally:
            os.close(master_fd)

    def test_slave_open_validates_the_name(self):
        with self.assertRaises(TypeError):
            slave_open(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            slave_open("")

    def test_fork_returns_a_fork_result(self):
        with patch("pty_utils._pty") as module:
            module.fork.return_value = (4321, 17)
            result = fork()
        self.assertIsInstance(result, ForkResult)
        self.assertEqual(result.pid, 4321)
        self.assertEqual(result.master_fd, 17)

    def test_spawn_validates_the_command_line(self):
        with self.assertRaises(TypeError):
            spawn("echo")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            spawn(42)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            spawn([])
        with self.assertRaises(TypeError):
            spawn([123])  # type: ignore[arg-type]

    def test_spawn_validates_the_readers(self):
        with self.assertRaises(TypeError):
            spawn(["echo"], master_read="not callable")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            spawn(["echo"], stdin_read="not callable")  # type: ignore[arg-type]

    def test_spawn_runs_the_program(self):
        with patch("pty_utils._pty") as module:
            module.spawn.return_value = 0
            status = spawn(["echo", "hello"])
        self.assertEqual(status, 0)
        module.spawn.assert_called_once_with(["echo", "hello"])

    def test_spawn_passes_the_readers(self):
        def read(fd):
            return b""

        with patch("pty_utils._pty") as module:
            module.spawn.return_value = 3
            status = spawn(["echo"], master_read=read, stdin_read=read)
        self.assertEqual(status, 3)
        self.assertEqual(module.spawn.call_args.args[0], ["echo"])
        self.assertIs(module.spawn.call_args.args[1], read)
        self.assertIs(module.spawn.call_args.args[2], read)

    def test_the_missing_module_raises_a_runtime_error(self):
        with patch("pty_utils._pty", None):
            with self.assertRaises(RuntimeError):
                openpty()
            with self.assertRaises(RuntimeError):
                open_terminal()
            with self.assertRaises(RuntimeError):
                master_open()
            with self.assertRaises(RuntimeError):
                slave_open("/dev/pts/0")
            with self.assertRaises(RuntimeError):
                fork()
            with self.assertRaises(RuntimeError):
                spawn(["echo"])

    def test_the_missing_module_still_reports_that_it_is_unavailable(self):
        with patch("pty_utils._pty", None):
            self.assertFalse(is_available())

    def test_all_is_sorted_and_unique(self):
        import pty_utils

        self.assertIsNotNone(pty_utils.__all__)
        self.assertEqual(len(pty_utils.__all__), len(set(pty_utils.__all__)))
        self.assertEqual(pty_utils.__all__, sorted(pty_utils.__all__))
        for name in pty_utils.__all__:
            self.assertTrue(hasattr(pty_utils, name), name)


if __name__ == "__main__":
    unittest.main()
