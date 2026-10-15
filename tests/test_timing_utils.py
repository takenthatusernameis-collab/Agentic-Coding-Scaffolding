"""Tests for timing_utils module."""

import time
import unittest
from unittest.mock import patch

from timing_utils import benchmark, elapsed_time, timer


class TestTimer(unittest.TestCase):
    """Test the timer context manager."""

    def timer_context_manager(self):
        """Test that timer measures time correctly."""
        with timer("Test") as t:
            time.sleep(0.01)  # Sleep for 10ms
            # Check that start_time was set
            self.assertGreater(t.start_time, 0)

        # After context, elapsed should be set
        self.assertGreater(t.elapsed, 0)
        # Should be approximately 0.01 seconds (allowing for variance)
        self.assertAlmostEqual(t.elapsed, 0.01, places=1)

    def timer_with_label(self):
        """Test timer with custom label."""
        with patch('builtins.print') as mock_print:
            with timer("Custom Label"):
                time.sleep(0.01)
            # Check that print was called with expected format
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Custom Label", call_args)
            self.assertIn("s", call_args)

    def timer_without_label(self):
        """Test timer with default label."""
        with patch('builtins.print') as mock_print:
            with timer():
                time.sleep(0.01)
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Elapsed", call_args)


class TestElapsedTime(unittest.TestCase):
    """Test the elapsed_time function."""

    def test_elapsed_time_basic(self):
        """Test that elapsed_time calculates correctly."""
        start = time.perf_counter()
        time.sleep(0.01)
        elapsed = elapsed_time(start)
        self.assertGreater(elapsed, 0)
        self.assertAlmostEqual(elapsed, 0.01, places=1)

    def test_elapsed_time_zero(self):
        """Test elapsed_time with same start and end time."""
        start = time.perf_counter()
        elapsed = elapsed_time(start)
        self.assertAlmostEqual(elapsed, 0.0, places=2)

    def test_elapsed_time_precision(self):
        """Test that elapsed_time returns a float."""
        start = time.perf_counter()
        elapsed = elapsed_time(start)
        self.assertIsInstance(elapsed, float)


class TestBenchmarkDecorator(unittest.TestCase):
    """Test the benchmark decorator."""

    def test_benchmark_default_iterations(self):
        """Test benchmark with default iterations=1."""
        call_count = 0

        @benchmark()
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        with patch('builtins.print') as mock_print:
            result = test_func()

        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("test_func", call_args)
        self.assertIn("avg of 1 runs", call_args)

    def test_benchmark_multiple_iterations(self):
        """Test benchmark with multiple iterations."""
        call_count = 0

        @benchmark(iterations=3)
        def test_func():
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)
            return "success"

        with patch('builtins.print') as mock_print:
            result = test_func()

        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("test_func", call_args)
        self.assertIn("avg of 3 runs", call_args)

    def test_benchmark_returns_correct_result(self):
        """Test that benchmark returns the function's actual result."""
        @benchmark(iterations=2)
        def test_func():
            return [1, 2, 3]

        result = test_func()
        self.assertEqual(result, [1, 2, 3])

    def test_benchmark_invalid_iterations(self):
        """Test that benchmark raises ValueError for invalid iterations."""
        with self.assertRaises(ValueError):
            @benchmark(iterations=0)
            def test_func():
                pass

        with self.assertRaises(ValueError):
            @benchmark(iterations=-1)
            def test_func():
                pass


if __name__ == "__main__":
    unittest.main()