"""Subprocess utility functions.

This module provides helpers for running shell commands safely and
conveniently using the standard library ``subprocess`` module.
"""

from __future__ import annotations

import subprocess
from typing import Any

__all__: list[str] = [
    "run_command",
    "check_output",
    "check_call",
]


def run_command(
    cmd: list[str] | str,
    *,
    capture_output: bool = False,
    text: bool = True,
    check: bool = False,
    timeout: float | None = None,
    **kwargs: Any,
) -> subprocess.CompletedProcess[Any]:
    """Run a command using ``subprocess.run``.

    Args:
        cmd: Command to execute as a list of strings or a shell command string.
        capture_output: Whether to capture stdout/stderr.
        text: Whether to return output as text (str) or bytes.
        check: Whether to raise CalledProcessError on non-zero exit.
        timeout: Optional timeout in seconds.
        **kwargs: Additional arguments passed to subprocess.run.

    Returns:
        A CompletedProcess instance.

    Raises:
        subprocess.CalledProcessError: If check=True and return code is non-zero.
        subprocess.TimeoutExpired: If the command times out.
        TypeError: If cmd is not a string or list.
    """
    if not isinstance(cmd, (str, list)):
        raise TypeError("cmd must be a string or list of strings")
    return subprocess.run(
        cmd,
        capture_output=capture_output,
        text=text,
        check=check,
        timeout=timeout,
        **kwargs,
    )


def check_output(
    cmd: list[str] | str,
    *,
    text: bool = True,
    timeout: float | None = None,
    **kwargs: Any,
) -> Any:
    """Run a command and return its stdout.

    Args:
        cmd: Command to execute.
        text: Whether to return output as text (str) or bytes.
        timeout: Optional timeout in seconds.
        **kwargs: Additional arguments passed to subprocess.check_output.

    Returns:
        The command's stdout.

    Raises:
        subprocess.CalledProcessError: If return code is non-zero.
        subprocess.TimeoutExpired: If the command times out.
        TypeError: If cmd is not a string or list.
    """
    if not isinstance(cmd, (str, list)):
        raise TypeError("cmd must be a string or list of strings")
    return subprocess.check_output(cmd, text=text, timeout=timeout, **kwargs)


def check_call(
    cmd: list[str] | str,
    *,
    timeout: float | None = None,
    **kwargs: Any,
) -> int:
    """Run a command and return the exit code (0 on success).

    Args:
        cmd: Command to execute.
        timeout: Optional timeout in seconds.
        **kwargs: Additional arguments passed to subprocess.check_call.

    Returns:
        The exit code of the command.

    Raises:
        subprocess.CalledProcessError: If return code is non-zero.
        subprocess.TimeoutExpired: If the command times out.
        TypeError: If cmd is not a string or list.
    """
    if not isinstance(cmd, (str, list)):
        raise TypeError("cmd must be a string or list of strings")
    return subprocess.check_call(cmd, timeout=timeout, **kwargs)
