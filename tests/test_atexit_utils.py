"""Tests for atexit_utils module."""

from __future__ import annotations

import atexit
import unittest
from unittest import mock

import atexit_utils


class TestAtexitUtils(unittest.TestCase):

    def test_register_and_unregister(self):
        """Test registering and unregistering an exit handler."""
        calls = []

        def handler():
            calls.append("called")

        # Register the handler
        result = atexit_utils.register(handler)
        assert result is handler

        # Unregister it
        unreg_result = atexit_utils.unregister(handler)
        assert unreg_result is True

        # Unregistering again might return False or True depending on impl
        # but it should not raise
        atexit_utils.unregister(handler)


    def test_register_with_args(self):
        """Test registering a handler with arguments."""
        calls = []

        def handler(x, y=10):
            calls.append((x, y))

        atexit_utils.register(handler, 5, y=20)
        atexit_utils.unregister(handler)


    def test_register_non_callable_raises(self):
        """Test that registering non-callable raises TypeError."""
        with self.assertRaises(TypeError):
            atexit_utils.register(123)  # type: ignore[arg-type]


    def test_unregister_non_callable_raises(self):
        """Test that unregistering non-callable raises TypeError."""
        with self.assertRaises(TypeError):
            atexit_utils.unregister(123)  # type: ignore[arg-type]


    def test_add_and_remove_aliases(self):
        """Test add and remove as aliases."""
        calls = []

        def handler():
            calls.append(1)

        atexit_utils.add(handler)
        assert atexit_utils.remove(handler) is True


    def test_get_registered(self):
        """Test getting registered handlers."""
        handlers = atexit_utils.get_registered()
        assert isinstance(handlers, list)


    def test_clear_and_run_handlers(self):
        """Test clear and run_exit_handlers functions.

        Both functions mutate the process-global ``atexit`` state:
        ``clear()`` unregisters every handler (including coverage's own
        data-saving finalizer) and ``run_exit_handlers()`` invokes
        ``atexit._run_exitfuncs()``. Calling them for real inside the test
        suite would silently disable coverage tracing for every test that
        runs afterwards, so the global state is patched out here and the
        delegation is asserted instead.
        """
        def sentinel_a():
            return None

        def sentinel_b():
            return None

        fake_handlers = [(sentinel_a, (), {}), (sentinel_b, (), {})]

        with mock.patch.object(atexit, "_exithandlers", fake_handlers, create=True), \
                mock.patch.object(atexit, "unregister") as mock_unregister:
            atexit_utils.clear()

        self.assertEqual(mock_unregister.call_count, len(fake_handlers))
        mock_unregister.assert_any_call(sentinel_a)
        mock_unregister.assert_any_call(sentinel_b)

        with mock.patch.object(atexit, "_run_exitfuncs") as mock_run:
            atexit_utils.run_exit_handlers()

        mock_run.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
