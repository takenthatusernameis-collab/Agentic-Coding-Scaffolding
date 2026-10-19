"""Unit tests for signal_utils module."""

import signal
import unittest

from signal_utils import (
    alarm,
    get_handler,
    get_signal_name,
    interrupt_handler,
    is_valid_signal,
    pause,
    register_handler,
    register_int_handler,
    register_term_handler,
    set_handler,
    signal_info,
    signal_names,
    suspend_handler,
    unregister_handler,
)

# Use SIGUSR1 when available (POSIX), otherwise fall back to SIGINT so the
# tests run on platforms with a reduced signal set.
_TEST_SIGNAL = signal.SIGUSR1 if hasattr(signal, "SIGUSR1") else signal.SIGINT


class TestSignalUtils(unittest.TestCase):
    def test_is_valid_signal(self):
        self.assertTrue(is_valid_signal(signal.SIGINT))
        self.assertFalse(is_valid_signal("SIGINT"))
        self.assertFalse(is_valid_signal(999999))
        self.assertFalse(is_valid_signal(None))

    def test_get_signal_name(self):
        self.assertEqual(get_signal_name(signal.SIGINT), "SIGINT")
        with self.assertRaises(TypeError):
            get_signal_name("SIGINT")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_signal_name(999999)

    def test_signal_names(self):
        names = signal_names()
        self.assertIsInstance(names, list)
        self.assertIn("SIGINT", names)
        self.assertEqual(names, sorted(names))

    def test_get_handler(self):
        # The handler may have been altered by earlier tests in the same
        # process; compare against the live signal module instead of a
        # hardcoded set.
        self.assertEqual(get_handler(signal.SIGINT), signal.getsignal(signal.SIGINT))

    def test_set_handler_round_trip(self):
        original = signal.getsignal(_TEST_SIGNAL)
        try:
            set_handler(_TEST_SIGNAL, suspend_handler)
            self.assertIs(signal.getsignal(_TEST_SIGNAL), suspend_handler)
        finally:
            signal.signal(_TEST_SIGNAL, original)

    def test_register_int_handler(self):
        original = signal.getsignal(signal.SIGINT)
        try:
            register_int_handler(suspend_handler)
            self.assertIs(signal.getsignal(signal.SIGINT), suspend_handler)
        finally:
            signal.signal(signal.SIGINT, original)

    def test_register_term_handler(self):
        original = signal.getsignal(signal.SIGTERM)
        try:
            register_term_handler(suspend_handler)
            self.assertIs(signal.getsignal(signal.SIGTERM), suspend_handler)
        finally:
            signal.signal(signal.SIGTERM, original)

    def test_register_handler_type_errors(self):
        with self.assertRaises(TypeError):
            register_handler("SIGINT", suspend_handler)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            register_handler(signal.SIGINT, "not callable")  # type: ignore[arg-type]

    def test_interrupt_handler(self):
        with self.assertRaises(KeyboardInterrupt):
            interrupt_handler(signal.SIGINT, None)

    def test_suspend_handler(self):
        self.assertIsNone(suspend_handler(signal.SIGINT, None))

    def test_alarm(self):
        self.assertEqual(alarm(0), 0)

    def test_alarm_type_errors(self):
        with self.assertRaises(TypeError):
            alarm("5")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            alarm(-1)

    def test_pause_is_callable(self):
        self.assertTrue(callable(pause))

    def test_signal_info(self):
        info = signal_info()
        self.assertIsInstance(info, dict)
        self.assertIn("names", info)
        self.assertIn("sigint_handler", info)
        self.assertIn("alarm_available", info)

    def test_unregister_handler(self):
        original = signal.getsignal(_TEST_SIGNAL)
        try:
            unregister_handler(_TEST_SIGNAL)
            self.assertIs(signal.getsignal(_TEST_SIGNAL), signal.SIG_DFL)
        finally:
            signal.signal(_TEST_SIGNAL, original)


if __name__ == "__main__":
    unittest.main()
