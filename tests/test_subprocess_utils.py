"""Tests for subprocess_utils module."""

from __future__ import annotations

import subprocess
import unittest

from subprocess_utils import check_call, check_output, run_command


class TestRunCommand(unittest.TestCase):
    def test_run_command_echo(self) -> None:
        result = run_command(["echo", "hello"], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(hasattr(result.stdout, "strip"))
        if isinstance(result.stdout, str):
            self.assertEqual(result.stdout.strip(), "hello")

    def test_run_command_check_true_success(self) -> None:
        result = run_command(["true"], check=True)
        self.assertEqual(result.returncode, 0)

    def test_run_command_check_true_failure(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            run_command(["false"], check=True)

    def test_run_command_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            run_command(123)  # type: ignore[arg-type]


class TestCheckOutput(unittest.TestCase):
    def test_check_output_echo(self) -> None:
        output = check_output(["echo", "test"], text=True)
        if isinstance(output, str):
            self.assertEqual(output.strip(), "test")

    def test_check_output_failure(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            check_output(["false"])

    def test_check_output_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            check_output(123)  # type: ignore[arg-type]


class TestCheckCall(unittest.TestCase):
    def test_check_call_success(self) -> None:
        returncode = check_call(["true"])
        self.assertEqual(returncode, 0)

    def test_check_call_failure(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            check_call(["false"])

    def test_check_call_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            check_call(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
