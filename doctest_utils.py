"""Utilities for running documentation examples (wrapping :mod:`doctest`).

The :mod:`doctest` module finds and runs the ``>>>`` examples embedded in
docstrings. This wrapper exposes a small, validated surface over that
functionality so callers can parse examples, run the examples of a docstring,
a module, or a text file, and turn the outcome into a readable report without
having to remember the exact class names of the standard library.
"""

from __future__ import annotations

import doctest as _doctest
import inspect
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

__all__ = [
    "parse_doctests",
    "find_doctests",
    "run_string_examples",
    "run_docstring_examples",
    "run_module_examples",
    "run_file_examples",
    "summarize_results",
    "format_failure",
    "DocTestSuite",
    "DocTestRunner",
    "OutputChecker",
]


def _require_text(value: object, name: str) -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_flag(value: object, name: str) -> bool:
    """Return *value* when it is a boolean, otherwise raise ``TypeError``."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_count(value: object, name: str) -> int:
    """Return *value* when it is a non-negative integer, otherwise raise."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative")
    return value


def _require_mapping(value: object, name: str) -> Dict[str, Any]:
    """Return a shallow copy of *value* when it is a mapping, otherwise raise."""
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping, got {type(value).__name__}")
    return dict(value)


def _default_globs(obj: object) -> Dict[str, Any]:
    """Return the globals the examples of *obj* are executed with.

    The namespace of the module that defines *obj* is used, so that examples
    can call the very functions they document.
    """
    if inspect.ismodule(obj):
        return dict(vars(obj))
    module_name = getattr(obj, "__module__", None)
    module = sys.modules.get(module_name) if isinstance(module_name, str) else None
    if module is None:
        return {}
    return dict(vars(module))


def parse_doctests(
    text: str,
    name: str = "<string>",
    globs: Optional[Mapping[str, Any]] = None,
    filename: Optional[str] = None,
    lineno: int = 1,
) -> List[_doctest.DocTest]:
    """Parse the examples contained in *text* into doctest objects.

    Args:
        text: Text holding ``>>>`` examples.
        name: Name reported for the parsed examples.
        globs: Globals made available to the examples.
        filename: File name reported for the parsed examples.
        lineno: First line number of *text*.

    Returns:
        A list with the parsed doctest, empty when *text* holds no example.

    Raises:
        TypeError: If an argument has an unsupported type.
        ValueError: If *lineno* is negative.
    """
    source = _require_text(text, "text")
    label = _require_text(name, "name")
    namespace = _require_mapping(globs, "globs") if globs is not None else {}
    if filename is not None:
        filename = _require_text(filename, "filename")
    line = _require_count(lineno, "lineno")
    parser = _doctest.DocTestParser()
    test = parser.get_doctest(source, namespace, label, filename, line)
    if not test.examples:
        return []
    return [test]


def find_doctests(obj: object, name: Optional[str] = None) -> List[_doctest.DocTest]:
    """Find every doctest defined by *obj* and the objects it contains.

    Args:
        obj: Module, class, function, or other object to inspect.
        name: Name reported for the found examples.

    Returns:
        The discovered doctests, ordered by name. Tests without examples are
        left out.

    Raises:
        TypeError: If *name* is not a string or ``None``.
        ValueError: If *obj* does not support doctest discovery.
    """
    if name is not None:
        name = _require_text(name, "name")
    finder = _doctest.DocTestFinder()
    tests = finder.find(obj, name=name)
    return sorted((test for test in tests if test.examples), key=lambda test: test.name)


def _run_tests(tests: List[_doctest.DocTest], verbose: bool) -> _doctest.TestResults:
    """Run *tests* with a fresh runner and return the aggregated results."""
    runner = _doctest.DocTestRunner(verbose=verbose)
    for test in tests:
        runner.run(test)
    return runner.summarize()


def run_string_examples(
    text: str,
    globs: Optional[Mapping[str, Any]] = None,
    name: str = "<string>",
    verbose: bool = False,
) -> _doctest.TestResults:
    """Run the doctest examples contained in *text*.

    Args:
        text: Text holding ``>>>`` examples.
        globs: Globals made available to the examples.
        name: Name reported for the examples.
        verbose: Whether the runner prints each example.

    Returns:
        The results of the run, holding the number of failures and attempts.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    source = _require_text(text, "text")
    label = _require_text(name, "name")
    verbose_flag = _require_flag(verbose, "verbose")
    return _run_tests(parse_doctests(source, label, globs), verbose_flag)


def run_docstring_examples(
    obj: object,
    name: Optional[str] = None,
    globs: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> _doctest.TestResults:
    """Run the doctest examples of the docstring of *obj*.

    Only the docstring of *obj* itself is executed; the docstrings of the
    members it contains are left untouched.

    Args:
        obj: Object whose docstring is executed.
        name: Name reported for the examples.
        globs: Globals made available to the examples.
        verbose: Whether the runner prints each example.

    Returns:
        The results of the run, holding the number of failures and attempts.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    if name is not None:
        name = _require_text(name, "name")
    verbose_flag = _require_flag(verbose, "verbose")
    docstring = inspect.getdoc(obj)
    if not docstring:
        return _doctest.TestResults(0, 0)
    label = name if name is not None else getattr(obj, "__name__", repr(obj))
    namespace = _require_mapping(globs, "globs") if globs is not None else _default_globs(obj)
    return _run_tests(parse_doctests(docstring, label, namespace), verbose_flag)


def run_module_examples(
    module: object,
    verbose: bool = False,
) -> _doctest.TestResults:
    """Run every doctest example defined by *module*.

    Args:
        module: Module whose examples are executed.
        verbose: Whether the runner prints each example.

    Returns:
        The results of the run, holding the number of failures and attempts.

    Raises:
        TypeError: If *module* is not a module or *verbose* is not a boolean.
    """
    if not inspect.ismodule(module):
        raise TypeError(f"module must be a module, got {type(module).__name__}")
    verbose_flag = _require_flag(verbose, "verbose")
    finder = _doctest.DocTestFinder()
    runner = _doctest.DocTestRunner(verbose=verbose_flag)
    for test in finder.find(module):
        runner.run(test)
    return runner.summarize()


def run_file_examples(
    path: str,
    base_dir: Optional[str] = None,
    verbose: bool = False,
) -> _doctest.TestResults:
    """Run the doctest examples contained in a text file.

    Args:
        path: Path of the file holding the examples.
        base_dir: Directory the path is resolved against, or ``None`` for the
            current working directory.
        verbose: Whether the runner prints each example.

    Returns:
        The results of the run, holding the number of failures and attempts.

    Raises:
        TypeError: If an argument has an unsupported type.
        OSError: If the file cannot be read.
    """
    location = _require_text(path, "path")
    verbose_flag = _require_flag(verbose, "verbose")
    file_path = Path(location)
    if base_dir is not None:
        file_path = Path(_require_text(base_dir, "base_dir")) / file_path
    text = file_path.read_text(encoding="utf-8")
    return run_string_examples(text, name=str(file_path), verbose=verbose_flag)


def summarize_results(results: object) -> str:
    """Return a one line summary of a doctest run.

    Args:
        results: The :class:`doctest.TestResults` of a run.

    Returns:
        A sentence reporting the number of failed and attempted examples.

    Raises:
        TypeError: If *results* does not expose the result counters.
    """
    failed = _require_count(getattr(results, "failed", None), "failed")
    attempted = _require_count(getattr(results, "attempted", None), "attempted")
    if failed:
        return f"{failed} of {attempted} doctests failed"
    return f"{attempted} doctests passed"


def format_failure(failure: object) -> str:
    """Return a readable description of a doctest failure.

    Args:
        failure: The failure recorded by a doctest runner.

    Returns:
        A description of the mismatch, or of the unexpected exception.

    Raises:
        TypeError: If *failure* is not a doctest failure.
    """
    if isinstance(failure, _doctest.DocTestFailure):
        return f"Expected:\n{failure.example.want}\nGot:\n{failure.got}"
    if isinstance(failure, _doctest.UnexpectedException):
        error = failure.exc_info[1]
        return f"Exception: {type(error).__name__}: {error}"
    raise TypeError(f"failure must be a doctest failure, got {type(failure).__name__}")


DocTestSuite = _doctest.DocTestSuite
DocTestRunner = _doctest.DocTestRunner
OutputChecker = _doctest.OutputChecker
