"""Tests for pty_utils."""

import os
import sys
import unittest
from unittest.mock import patch

from pty_utils import (
    CHILD,
    STDERR_FILENO,
    STDIN_FILENO,
    STDOUT_FILENO,
    fork,
    is_available,
    master_open,
    open_terminal,
    openpty,
    slave_open,
    spawn,
)


class TestPtyUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_openpty_returns_fds(self):
        master_fd, slave_fd = openpty()
        self.assertIsInstance(master_fd, int)
        self.assertIsInstance(slave_fd, int)
        self.assertGreaterEqual(master_fd, 0)
        self.assertGreaterEqual(slave_fd, 0)
        os.close(master_fd)
        os.close(slave_fd)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_open_terminal_alias(self):
        master_fd, slave_fd = open_terminal()
        self.assertIsInstance(master_fd, int)
        self.assertIsInstance(slave_fd, int)
        os.close(master_fd)
        os.close(slave_fd)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_master_open(self):
        name, fd = master_open()
        self.assertIsInstance(name, str)
        self.assertIsInstance(fd, int)
        self.assertGreaterEqual(fd, 0)
        try:
            os.close(fd)
        except OSError:
            pass

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_slave_open_validates_arguments(self):
        with self.assertRaises(TypeError):
            slave_open(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            slave_open("")

    @unittest.skipUnless(sys.platform != "win32", "Unix-like required")
    def test_fileno_constants(self):
        self.assertEqual(STDIN_FILENO, 0)
        self.assertEqual(STDOUT_FILENO, 1)
        self.assertEqual(STDERR_FILENO, 2)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_fork_returns_int(self):
        result = fork()
        self.assertTrue(isinstance(result, int) or isinstance(result, tuple))
        if isinstance(result, tuple):
            self.assertTrue(all(isinstance(x, int) for x in result))
            pid = result[0]
        else:
            pid = result
        if pid == 0:
            os._exit(0)
        elif pid > 0:
            os.waitpid(pid, 0)

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_spawn_validates_arguments(self):
        with self.assertRaises(TypeError):
            spawn("echo")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            spawn([])
        with self.assertRaises(TypeError):
            spawn([123])  # type: ignore[arg-type]

    @unittest.skipUnless(is_available(), "pty module not available")
    def test_spawn_runs_true(self):
        status = spawn([sys.executable, "-c", "import sys; sys.exit(0)"])
        self.assertIsInstance(status, int)

    def test_missing_module_raises_runtimeerror(self):
        with patch("pty_utils._pty", None):
            with self.assertRaises(RuntimeError):
                openpty()
            with self.assertRaises(RuntimeError):
                master_open()
            with self.assertRaises(RuntimeError):
                fork()
            with self.assertRaises(RuntimeError):
                spawn([sys.executable])

    def test_child_constant(self):
        self.assertIsInstance(CHILD, int)
