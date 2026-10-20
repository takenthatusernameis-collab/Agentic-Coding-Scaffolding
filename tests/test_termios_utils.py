"""Tests for termios_utils."""

import os
import unittest
from unittest.mock import patch

import termios_utils
from termios_utils import (
    Attributes,
    WindowSize,
    baud_rates,
    control_character_names,
    drain,
    flush,
    get_attributes,
    get_window_size,
    is_available,
    make_cbreak,
    make_raw,
    pause_output,
    resume_output,
    send_break,
    set_attributes,
    set_blocking,
    set_read_timeout,
    set_window_size,
)


class TestTermiosUtils(unittest.TestCase):
    """Verify the terminal attribute helpers.

    The tests work on a pseudo terminal that the test itself opens, so no
    test ever changes the terminal of the process that runs the suite.
    """

    def setUp(self):
        self.master_fd = None
        self.slave_fd = None
        if not is_available():
            return
        try:
            self.master_fd, self.slave_fd = os.openpty()
        except OSError:  # pragma: no cover - the platform has no pseudo terminals
            self.skipTest("the platform does not provide pseudo terminals")

    def tearDown(self):
        for fd in (self.slave_fd, self.master_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:  # pragma: no cover - the descriptor is already closed
                    pass

    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_constants_match_the_standard_library(self):
        if not is_available():
            self.skipTest("termios module not available")
        import termios

        self.assertEqual(termios_utils.TCSANOW, termios.TCSANOW)
        self.assertEqual(termios_utils.TCSADRAIN, termios.TCSADRAIN)
        self.assertEqual(termios_utils.TCSAFLUSH, termios.TCSAFLUSH)
        self.assertEqual(termios_utils.TCIFLUSH, termios.TCIFLUSH)
        self.assertEqual(termios_utils.TCOFLUSH, termios.TCOFLUSH)
        self.assertEqual(termios_utils.VMIN, termios.VMIN)
        self.assertEqual(termios_utils.VTIME, termios.VTIME)
        self.assertEqual(termios_utils.VINTR, termios.VINTR)

    def test_get_attributes_reads_the_terminal(self):
        attributes = get_attributes(self.slave_fd)
        self.assertIsInstance(attributes, Attributes)
        self.assertIsInstance(attributes.iflag, int)
        self.assertIsInstance(attributes.oflag, int)
        self.assertIsInstance(attributes.cflag, int)
        self.assertIsInstance(attributes.lflag, int)
        self.assertIsInstance(attributes.ispeed, int)
        self.assertIsInstance(attributes.ospeed, int)
        self.assertIsInstance(attributes.cc, list)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = attributes
        self.assertEqual(iflag, attributes.iflag)
        self.assertEqual(cc, attributes.cc)

    def test_get_attributes_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            get_attributes("0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_attributes(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_attributes(-1)

    def test_set_attributes_writes_the_terminal(self):
        attributes = get_attributes(self.slave_fd)
        raw = make_raw(attributes)
        set_attributes(self.slave_fd, raw)
        self.assertEqual(get_attributes(self.slave_fd), raw)

    def test_set_attributes_validates_its_arguments(self):
        attributes = get_attributes(self.slave_fd)
        with self.assertRaises(TypeError):
            set_attributes("0", attributes)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_attributes(-1, attributes)
        with self.assertRaises(TypeError):
            set_attributes(self.slave_fd, "raw")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            set_attributes(self.slave_fd, attributes, "now")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_attributes(self.slave_fd, attributes, 99)

    def test_set_attributes_accepts_every_known_moment(self):
        attributes = get_attributes(self.slave_fd)
        for when in (
            termios_utils.TCSANOW,
            termios_utils.TCSADRAIN,
            termios_utils.TCSAFLUSH,
        ):
            with self.subTest(when=when):
                set_attributes(self.slave_fd, attributes, when)

    def test_make_raw_removes_the_echo(self):
        attributes = get_attributes(self.slave_fd)
        raw = make_raw(attributes)
        self.assertIsInstance(raw, Attributes)
        self.assertEqual(raw.lflag & termios_utils.ECHO, 0)

    def test_make_raw_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            make_raw("raw")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            make_raw(Attributes(-1, 0, 0, 0, 0, 0, []))

    def test_make_cbreak_keeps_the_signals(self):
        attributes = get_attributes(self.slave_fd)
        cbreak = make_cbreak(attributes)
        self.assertIsInstance(cbreak, Attributes)
        self.assertEqual(
            cbreak.lflag & termios_utils.ISIG,
            attributes.lflag & termios_utils.ISIG,
        )

    def test_make_cbreak_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            make_cbreak(None)  # type: ignore[arg-type]

    def test_set_read_timeout_configures_the_terminal(self):
        attributes = get_attributes(self.slave_fd)
        timed = set_read_timeout(attributes, 1.5)
        self.assertEqual(timed.cc[termios_utils.VMIN], 0)
        self.assertEqual(timed.cc[termios_utils.VTIME], 15)

    def test_set_read_timeout_validates_its_arguments(self):
        attributes = get_attributes(self.slave_fd)
        with self.assertRaises(TypeError):
            set_read_timeout(attributes, "1")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_read_timeout(attributes, -1)
        with self.assertRaises(ValueError):
            set_read_timeout(attributes, float("inf"))

    def test_set_blocking_configures_the_terminal(self):
        attributes = get_attributes(self.slave_fd)
        blocking = set_blocking(attributes)
        self.assertEqual(blocking.cc[termios_utils.VMIN], 1)
        self.assertEqual(blocking.cc[termios_utils.VTIME], 0)

    def test_set_blocking_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            set_blocking(3)  # type: ignore[arg-type]

    def test_get_window_size_reads_the_terminal(self):
        size = get_window_size(self.slave_fd)
        self.assertIsInstance(size, WindowSize)
        self.assertGreaterEqual(size.rows, 0)
        self.assertGreaterEqual(size.columns, 0)

    def test_get_window_size_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            get_window_size("0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_window_size(-1)

    def test_set_window_size_writes_the_terminal(self):
        set_window_size(self.slave_fd, 40, 120)
        size = get_window_size(self.slave_fd)
        self.assertEqual(size.rows, 40)
        self.assertEqual(size.columns, 120)

    def test_set_window_size_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            set_window_size(self.slave_fd, "40", 120)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_window_size(self.slave_fd, -1, 120)
        with self.assertRaises(ValueError):
            set_window_size(self.slave_fd, 40, -1)

    def test_drain_flush_and_break_work_on_a_terminal(self):
        drain(self.slave_fd)
        flush(self.slave_fd, termios_utils.TCIFLUSH)
        flush(self.slave_fd, termios_utils.TCOFLUSH)
        send_break(self.slave_fd)
        pause_output(self.slave_fd)
        resume_output(self.slave_fd)

    def test_drain_and_friends_validate_their_arguments(self):
        with self.assertRaises(TypeError):
            drain("0")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            drain(-1)
        with self.assertRaises(TypeError):
            flush(self.slave_fd, "input")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            flush(self.slave_fd, 99)
        with self.assertRaises(TypeError):
            send_break(self.slave_fd, 1.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            send_break(self.slave_fd, -1)
        with self.assertRaises(TypeError):
            pause_output(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            resume_output(None)  # type: ignore[arg-type]

    def test_control_character_names(self):
        names = control_character_names()
        self.assertTrue(names)
        self.assertEqual(names[termios_utils.VINTR], "VINTR")
        self.assertEqual(names[termios_utils.VMIN], "VMIN")
        self.assertNotIn("VINTR", names)

    def test_baud_rates(self):
        rates = baud_rates()
        self.assertEqual(rates["B9600"], 9600)
        self.assertEqual(rates["B115200"], 115200)
        self.assertEqual(rates["B0"], 0)

    def test_helpers_report_a_missing_standard_library_module(self):
        with patch("termios_utils._termios", None), patch("termios_utils._tty", None):
            with self.assertRaises(RuntimeError):
                get_attributes(self.slave_fd)
            with self.assertRaises(RuntimeError):
                set_attributes(self.slave_fd, Attributes(0, 0, 0, 0, 0, 0, []))
            with self.assertRaises(RuntimeError):
                make_raw(Attributes(0, 0, 0, 0, 0, 0, []))
            with self.assertRaises(RuntimeError):
                make_cbreak(Attributes(0, 0, 0, 0, 0, 0, []))
            with self.assertRaises(RuntimeError):
                drain(self.slave_fd)
            with self.assertRaises(RuntimeError):
                flush(self.slave_fd)
            with self.assertRaises(RuntimeError):
                pause_output(self.slave_fd)
            with self.assertRaises(RuntimeError):
                resume_output(self.slave_fd)
            with self.assertRaises(RuntimeError):
                send_break(self.slave_fd)
            with self.assertRaises(RuntimeError):
                set_window_size(self.slave_fd, 24, 80)
            self.assertFalse(is_available())

    def test_all_names_are_exported(self):
        self.assertIsNotNone(termios_utils.__all__)
        self.assertEqual(len(termios_utils.__all__), len(set(termios_utils.__all__)))
        for name in termios_utils.__all__:
            self.assertTrue(hasattr(termios_utils, name), name)


if __name__ == "__main__":
    unittest.main()
