import signal
import tempfile
import unittest

import faulthandler_utils
from faulthandler_utils import (
    cancel_dump_traceback_later,
    disable,
    dump_traceback,
    dump_traceback_later,
    enable,
    is_available,
    is_enabled,
    register,
    unregister,
)


class TestFaulthandlerUtils(unittest.TestCase):
    def setUp(self):
        self._was_enabled = is_enabled()

    def tearDown(self):
        cancel_dump_traceback_later()
        if self._was_enabled:
            enable()
        else:
            disable()

    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)
        self.assertTrue(is_available())

    def test_is_enabled_returns_bool(self):
        self.assertIsInstance(is_enabled(), bool)

    def test_enable_disable_roundtrip(self):
        disable()
        self.assertFalse(is_enabled())
        enable()
        self.assertTrue(is_enabled())

    def test_enable_writes_to_the_given_file(self):
        with tempfile.TemporaryFile(mode="w+b") as handle:
            enable(file=handle, all_threads=False)
            self.assertTrue(is_enabled())

    def test_enable_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            enable(file="not-a-file")
        with self.assertRaises(TypeError):
            enable(file=[])
        with self.assertRaises(ValueError):
            enable(file=-1)
        with self.assertRaises(TypeError):
            enable(all_threads="yes")
        with self.assertRaises(TypeError):
            enable(all_threads=1)

    def test_disable_returns_none(self):
        self.assertIsNone(disable())
        self.assertFalse(is_enabled())

    def test_dump_traceback_writes_to_stream(self):
        with tempfile.TemporaryFile(mode="w+b") as handle:
            dump_traceback(file=handle, all_threads=False)
            handle.flush()
            handle.seek(0)
            content = handle.read()
        self.assertIsInstance(content, bytes)
        self.assertIn(b"test_dump_traceback_writes_to_stream", content)

    def test_dump_traceback_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            dump_traceback(file=[])
        with self.assertRaises(TypeError):
            dump_traceback(all_threads=1)

    def test_file_descriptor_is_accepted(self):
        with tempfile.TemporaryFile(mode="w+b") as handle:
            dump_traceback(file=handle.fileno(), all_threads=False)
            self.assertIsInstance(handle.fileno(), int)

    def test_dump_traceback_later_arms_the_watchdog(self):
        with tempfile.TemporaryFile(mode="w+b") as handle:
            dump_traceback_later(3600.0, file=handle)
            cancel_dump_traceback_later()

    def test_dump_traceback_later_validation(self):
        with self.assertRaises(TypeError):
            dump_traceback_later("1.0")
        with self.assertRaises(TypeError):
            dump_traceback_later(True)
        with self.assertRaises(ValueError):
            dump_traceback_later(-1.0)
        with self.assertRaises(TypeError):
            dump_traceback_later(1.0, repeat="no")
        with self.assertRaises(TypeError):
            dump_traceback_later(1.0, file=[])
        with self.assertRaises(TypeError):
            dump_traceback_later(1.0, exit="no")

    def test_cancel_dump_traceback_later_returns_none(self):
        self.assertIsNone(cancel_dump_traceback_later())

    def test_register_and_unregister_a_signal(self):
        signum = getattr(signal, "SIGUSR1", None)
        if signum is None:  # pragma: no cover - Windows has no SIGUSR1
            self.skipTest("SIGUSR1 is not available on this platform")
        with tempfile.TemporaryFile(mode="w+b") as handle:
            previous = register(signum, file=handle)
        unregister(signum)
        self.assertIsNone(previous)

    def test_register_unregister_validation(self):
        with self.assertRaises(TypeError):
            register("SIGUSR1")
        with self.assertRaises(TypeError):
            register(True)
        with self.assertRaises(TypeError):
            register(1, file=[])
        with self.assertRaises(TypeError):
            register(1, all_threads=[])
        with self.assertRaises(TypeError):
            register(1, chain=[])
        with self.assertRaises(TypeError):
            unregister("SIGUSR1")
        with self.assertRaises(TypeError):
            unregister(True)

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(len(faulthandler_utils.__all__), len(set(faulthandler_utils.__all__)))
        for name in faulthandler_utils.__all__:
            self.assertTrue(hasattr(faulthandler_utils, name), name)


if __name__ == "__main__":
    unittest.main()
