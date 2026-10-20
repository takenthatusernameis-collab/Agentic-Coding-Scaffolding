import unittest
from unittest.mock import patch

import syslog_utils
from syslog_utils import (
    LOG_ALERT,
    LOG_CRIT,
    LOG_DEBUG,
    LOG_EMERG,
    LOG_ERR,
    LOG_INFO,
    LOG_LOCAL0,
    LOG_NOTICE,
    LOG_PERROR,
    LOG_PID,
    LOG_UPTO,
    LOG_USER,
    LOG_WARNING,
    close_log,
    facility_name,
    facility_names,
    is_available,
    log_mask,
    log_message,
    log_upto,
    open_log,
    option_names,
    priority_name,
    priority_names,
    set_log_mask,
)


class TestSyslogUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_constants_match_the_standard_library(self):
        self.assertEqual(LOG_EMERG, 0)
        self.assertEqual(LOG_ALERT, 1)
        self.assertEqual(LOG_CRIT, 2)
        self.assertEqual(LOG_ERR, 3)
        self.assertEqual(LOG_WARNING, 4)
        self.assertEqual(LOG_NOTICE, 5)
        self.assertEqual(LOG_INFO, 6)
        self.assertEqual(LOG_DEBUG, 7)
        self.assertEqual(LOG_USER, 8)
        self.assertEqual(LOG_LOCAL0, 128)

    @patch("syslog_utils._syslog.openlog")
    def test_open_log(self, mock_openlog):
        open_log("myapp", LOG_PID, LOG_USER)
        mock_openlog.assert_called_once_with("myapp", LOG_PID, LOG_USER)

    @patch("syslog_utils._syslog.openlog")
    def test_open_log_defaults(self, mock_openlog):
        open_log()
        mock_openlog.assert_called_once_with(None, 0, LOG_USER)

    @patch("syslog_utils._syslog.openlog")
    def test_open_log_rejects_unknown_facility(self, mock_openlog):
        with self.assertRaises(ValueError):
            open_log("myapp", 0, 3)
        mock_openlog.assert_not_called()

    @patch("syslog_utils._syslog.openlog")
    def test_open_log_rejects_unknown_options(self, mock_openlog):
        with self.assertRaises(ValueError):
            open_log("myapp", 1 << 20, LOG_USER)
        mock_openlog.assert_not_called()

    def test_open_log_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            open_log(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            open_log("")
        with self.assertRaises(TypeError):
            open_log("myapp", "pid")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            open_log("myapp", -1, LOG_USER)
        with self.assertRaises(TypeError):
            open_log("myapp", 0, "user")  # type: ignore[arg-type]

    @patch("syslog_utils._syslog.syslog")
    def test_log_message(self, mock_syslog):
        log_message("hello", LOG_WARNING)
        mock_syslog.assert_called_once_with(LOG_WARNING, "hello")

    @patch("syslog_utils._syslog.syslog")
    def test_log_message_defaults_to_info(self, mock_syslog):
        log_message("hello")
        mock_syslog.assert_called_once_with(LOG_INFO, "hello")

    @patch("syslog_utils._syslog.syslog")
    def test_log_message_supports_the_message_first_signature(self, mock_syslog):
        calls = []

        def fake_syslog(*args):
            calls.append(args)
            if len(args) == 2 and isinstance(args[0], int):
                raise TypeError("argument 'message': 'int' object cannot be converted")

        mock_syslog.side_effect = fake_syslog
        log_message("hello", LOG_ERR)
        self.assertEqual(calls, [(LOG_ERR, "hello"), ("hello", LOG_ERR)])

    def test_log_message_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            log_message(123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            log_message("")
        with self.assertRaises(TypeError):
            log_message("hello", "info")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            log_message("hello", 42)

    @patch("syslog_utils._syslog.closelog")
    def test_close_log(self, mock_closelog):
        close_log()
        mock_closelog.assert_called_once_with()

    @patch("syslog_utils._syslog.setlogmask", return_value=255)
    def test_set_log_mask(self, mock_setlogmask):
        self.assertEqual(set_log_mask(log_upto(LOG_WARNING)), 255)
        mock_setlogmask.assert_called_once_with(log_upto(LOG_WARNING))

    def test_set_log_mask_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            set_log_mask("all")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            set_log_mask(-1)

    def test_log_mask(self):
        self.assertEqual(log_mask(LOG_EMERG), 1)
        self.assertEqual(log_mask(LOG_ERR), 8)
        self.assertEqual(log_mask(LOG_DEBUG), 128)

    def test_log_upto(self):
        self.assertEqual(log_upto(LOG_EMERG), 1)
        self.assertEqual(log_upto(LOG_WARNING), 31)
        self.assertEqual(log_upto(LOG_DEBUG), 255)
        self.assertEqual(LOG_UPTO(LOG_WARNING), log_upto(LOG_WARNING))

    def test_mask_helpers_validate_their_arguments(self):
        with self.assertRaises(TypeError):
            log_mask("info")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            log_mask(42)
        with self.assertRaises(TypeError):
            log_upto("info")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            log_upto(42)

    def test_priority_name(self):
        self.assertEqual(priority_name(LOG_INFO), "LOG_INFO")
        self.assertEqual(priority_name(LOG_DEBUG), "LOG_DEBUG")

    def test_priority_name_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            priority_name("info")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            priority_name(42)

    def test_facility_name(self):
        self.assertEqual(facility_name(LOG_USER), "LOG_USER")
        self.assertEqual(facility_name(LOG_LOCAL0), "LOG_LOCAL0")

    def test_facility_name_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            facility_name("user")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            facility_name(3)

    def test_name_tables(self):
        priorities = priority_names()
        facilities = facility_names()
        options = option_names()
        self.assertEqual(priorities["LOG_INFO"], LOG_INFO)
        self.assertEqual(facilities["LOG_USER"], LOG_USER)
        self.assertEqual(options["LOG_PID"], LOG_PID)
        self.assertEqual(options["LOG_PERROR"], LOG_PERROR)
        priorities["LOG_INFO"] = 99
        self.assertEqual(priority_names()["LOG_INFO"], LOG_INFO)

    def test_helpers_report_a_missing_standard_library_module(self):
        with patch("syslog_utils._syslog", None):
            with self.assertRaises(RuntimeError):
                open_log("myapp")
            with self.assertRaises(RuntimeError):
                log_message("hello")
            with self.assertRaises(RuntimeError):
                close_log()
            with self.assertRaises(RuntimeError):
                set_log_mask(0)
            self.assertFalse(is_available())

    def test_all_names_are_exported(self):
        self.assertIsNotNone(syslog_utils.__all__)
        self.assertEqual(len(syslog_utils.__all__), len(set(syslog_utils.__all__)))
        for name in syslog_utils.__all__:
            self.assertTrue(hasattr(syslog_utils, name), name)


if __name__ == "__main__":
    unittest.main()
