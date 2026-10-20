"""Utilities wrapping the standard library ``unittest`` module."""

from __future__ import annotations

import unittest as _unittest
from typing import Any, Type

__all__ = [
    "TestCase",
    "TestSuite",
    "TestLoader",
    "TextTestRunner",
    "main",
    "make_suite",
    "run_tests",
    "defaultTestLoader",
]

TestCase = _unittest.TestCase
TestSuite = _unittest.TestSuite
TestLoader = _unittest.TestLoader
TextTestRunner = _unittest.TextTestRunner
defaultTestLoader = _unittest.defaultTestLoader


def make_suite(test_class: Type[TestCase]) -> TestSuite:
    loader = _unittest.TestLoader()
    return loader.loadTestsFromTestCase(test_class)


def run_tests(suite: Any, verbosity: int = 1) -> _unittest.TestResult:
    runner = _unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def main(module=None, exit=True, verbosity=1) -> None:
    _unittest.main(module=module, exit=exit, verbosity=verbosity)
