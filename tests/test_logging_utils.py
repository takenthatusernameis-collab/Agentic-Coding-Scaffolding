"""Tests for logging_utils module."""

import logging
import unittest

from logging_utils import configure_logging, get_logger, log_calls


class TestGetLogger(unittest.TestCase):
    def test_returns_logger_with_name(self) -> None:
        logger = get_logger("my_app.module")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "my_app.module")

    def test_returns_root_logger_when_no_name(self) -> None:
        logger = get_logger()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "root")

    def test_same_name_returns_same_instance(self) -> None:
        logger1 = get_logger("shared_logger")
        logger2 = get_logger("shared_logger")
        self.assertIs(logger1, logger2)

    def test_non_string_name_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_logger(123)  # type: ignore[arg-type]


class TestConfigureLogging(unittest.TestCase):
    def setUp(self) -> None:
        self._root = logging.getLogger()
        self._saved_handlers = self._root.handlers[:]
        self._saved_level = self._root.level
        self._root.handlers = []
        self._root.setLevel(logging.NOTSET)

    def tearDown(self) -> None:
        self._root.handlers = self._saved_handlers
        self._root.setLevel(self._saved_level)

    def test_returns_root_logger(self) -> None:
        root = configure_logging(level=logging.INFO, force=True)
        self.assertIs(root, logging.getLogger())

    def test_sets_level(self) -> None:
        configure_logging(level=logging.DEBUG, force=True)
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

    def test_default_level_is_warning(self) -> None:
        configure_logging(force=True)
        self.assertEqual(logging.getLogger().level, logging.WARNING)

    def test_adds_default_handler(self) -> None:
        configure_logging(level=logging.INFO, force=True)
        self.assertTrue(len(logging.getLogger().handlers) > 0)

    def test_custom_handlers(self) -> None:
        handler = logging.StreamHandler()
        configure_logging(level=logging.INFO, handlers=[handler], force=True)
        self.assertIn(handler, logging.getLogger().handlers)

    def test_force_removes_existing_handlers(self) -> None:
        self._root.addHandler(logging.StreamHandler())
        configure_logging(level=logging.INFO, force=True)
        self.assertEqual(len(self._root.handlers), 1)

    def test_format_applied_to_handler(self) -> None:
        configure_logging(level=logging.INFO, format="%(message)s", force=True)
        for handler in self._root.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.formatter is not None:
                self.assertEqual(handler.formatter._fmt, "%(message)s")

    def test_non_integer_level_raises(self) -> None:
        with self.assertRaises(TypeError):
            configure_logging(level="INFO", force=True)  # type: ignore[arg-type]

    def test_non_list_handlers_raises(self) -> None:
        with self.assertRaises(TypeError):
            configure_logging(handlers="not-a-list", force=True)  # type: ignore[arg-type]

    def test_non_list_handlers_with_none_allowed(self) -> None:
        configure_logging(level=logging.INFO, handlers=None, force=True)
        self.assertTrue(len(self._root.handlers) > 0)


class TestLogCalls(unittest.TestCase):
    def test_decorator_logs_call_and_result(self) -> None:
        @log_calls(level=logging.DEBUG)
        def add(a: int, b: int) -> int:
            return a + b

        with self.assertLogs("logging_utils", level="DEBUG") as cm:
            result = add(2, 3)
        self.assertEqual(result, 5)
        self.assertEqual(len(cm.records), 2)
        self.assertIn("Calling", cm.records[0].getMessage())
        self.assertIn("returned", cm.records[1].getMessage())

    def test_decorator_preserves_metadata(self) -> None:
        @log_calls(level=logging.DEBUG)
        def named_function(a: int, b: int) -> int:
            """Original docstring."""
            return a * b

        self.assertEqual(named_function.__name__, "named_function")
        self.assertEqual(named_function.__doc__, "Original docstring.")

    def test_decorator_with_custom_logger(self) -> None:
        logger = logging.getLogger("custom.log.test")
        logger.setLevel(logging.DEBUG)

        @log_calls(logger=logger, level=logging.INFO)
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        with self.assertLogs("custom.log.test", level="INFO") as cm:
            result = greet("World")
        self.assertEqual(result, "Hello, World!")
        self.assertEqual(len(cm.records), 2)

    def test_decorator_propagates_kwargs(self) -> None:
        @log_calls(level=logging.DEBUG)
        def join_values(sep: str, *parts: str) -> str:
            return sep.join(parts)

        with self.assertLogs("logging_utils", level="DEBUG") as cm:
            self.assertEqual(join_values("-", "a", "b", "c"), "a-b-c")
        first_msg = cm.records[0].getMessage()
        self.assertIn("a", first_msg)
        self.assertIn("b", first_msg)
        self.assertIn("c", first_msg)

    def test_decorator_custom_level(self) -> None:
        @log_calls(level=logging.WARNING)
        def echo(value: str) -> str:
            return value

        with self.assertLogs("logging_utils", level="WARNING") as cm:
            self.assertEqual(echo("hello"), "hello")
        self.assertEqual(cm.records[0].levelno, logging.WARNING)

    def test_decorator_default_level_logs_debug(self) -> None:
        @log_calls()
        def echo(value: str) -> str:
            return value

        with self.assertLogs("logging_utils", level="DEBUG") as cm:
            self.assertEqual(echo("hello"), "hello")
        self.assertEqual(cm.records[0].levelno, logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
