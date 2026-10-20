"""Utilities for tracing Python program execution (wrapping :mod:`trace`).

The :mod:`trace` module implements a deterministic trace of the execution of a
Python program: it can count how often every line was executed, report each
executed line, and record which functions were called and by whom. This wrapper
exposes a small, validated surface over that functionality so callers can build
a tracer, run code under it, and turn the recorded results into readable
reports.
"""

from __future__ import annotations

import ast
import os
import sys
import trace as _trace
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

__all__ = [
    "new_tracer",
    "run_traced",
    "run_script_traced",
    "counted_lines",
    "line_counts",
    "called_functions",
    "call_relationships",
    "is_ignored_filename",
    "merge_results",
    "write_coverage_report",
    "summarize_coverage",
    "format_coverage_summary",
    "clear_counts",
    "Trace",
    "CoverageResults",
    "PRAGMA_NOCOVER",
]


def _require_bool(value: object, name: str) -> bool:
    """Return *value* when it is a boolean, otherwise raise ``TypeError``."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_text(value: object, name: str) -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_path(value: object, name: str) -> Path:
    """Return *value* as a :class:`pathlib.Path`, otherwise raise ``TypeError``."""
    if isinstance(value, Path):
        return value
    if isinstance(value, str):
        return Path(value)
    if isinstance(value, os.PathLike):
        return Path(os.fspath(value))
    raise TypeError(f"{name} must be a path, got {type(value).__name__}")


def _require_text_sequence(value: object, name: str) -> List[str]:
    """Return *value* as a list of strings, otherwise raise ``TypeError``."""
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple, set, frozenset)):
        raise TypeError(f"{name} must be a sequence of strings, got {type(value).__name__}")
    items: List[str] = []
    for item in value:
        items.append(_require_text(item, f"{name} entry"))
    return items


def _require_results(value: object, name: str = "results") -> _trace.CoverageResults:
    """Return *value* when it holds coverage results, otherwise raise."""
    if not isinstance(value, _trace.CoverageResults):
        raise TypeError(f"{name} must be a trace.CoverageResults, got {type(value).__name__}")
    return value


def _require_tracer(value: object, name: str = "tracer") -> _trace.Trace:
    """Return *value* when it is a tracer, otherwise raise ``TypeError``."""
    if not isinstance(value, _trace.Trace):
        raise TypeError(f"{name} must be a trace.Trace, got {type(value).__name__}")
    return value


def _default_ignoredirs() -> List[str]:
    """Return the installation prefixes that are excluded from tracing."""
    candidates = [sys.prefix, sys.base_prefix, sys.exec_prefix, sys.base_exec_prefix]
    directories: List[str] = []
    for candidate in candidates:
        if candidate and candidate not in directories:
            directories.append(candidate)
    return directories


def _executable_lines(filename: str) -> Optional[Set[int]]:
    """Return the executable line numbers of *filename*, or ``None``.

    The source of the file is parsed to find the lines that hold a statement.
    ``None`` is returned when the file cannot be read or cannot be parsed.
    """
    path = Path(filename)
    if path.suffix == ".pyc" or not path.is_file():
        return None
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError:
        return None
    return {node.lineno for node in ast.walk(tree) if isinstance(node, ast.stmt)}


def new_tracer(
    count: bool = True,
    trace_lines: bool = False,
    count_funcs: bool = False,
    count_callers: bool = False,
    ignoredirs: Optional[Sequence[str]] = None,
    ignoremods: Optional[Sequence[str]] = None,
    infile: Optional[str] = None,
    outfile: Optional[str] = None,
) -> _trace.Trace:
    """Create a tracer that records the execution of the code it runs.

    Args:
        count: Whether the number of executions of every line is counted.
        trace_lines: Whether every executed line is written out.
        count_funcs: Whether the called functions are recorded. This overrides
            ``count`` and ``trace_lines`` in the standard library.
        count_callers: Whether the calling relationships are recorded. This
            overrides ``count``, ``trace_lines``, and ``count_funcs`` in the
            standard library.
        ignoredirs: Directories whose content is not traced. The installation
            prefixes are excluded when this is ``None``.
        ignoremods: Names of the modules that are not traced.
        infile: File holding previously stored counts that are merged into the
            results.
        outfile: File the counts are written to.

    Returns:
        A tracer ready to run code under.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    count_flag = _require_bool(count, "count")
    trace_flag = _require_bool(trace_lines, "trace_lines")
    funcs_flag = _require_bool(count_funcs, "count_funcs")
    callers_flag = _require_bool(count_callers, "count_callers")
    directories = (
        _default_ignoredirs()
        if ignoredirs is None
        else _require_text_sequence(ignoredirs, "ignoredirs")
    )
    modules = [] if ignoremods is None else _require_text_sequence(ignoremods, "ignoremods")
    source = None if infile is None else _require_text(infile, "infile")
    destination = None if outfile is None else _require_text(outfile, "outfile")
    return _trace.Trace(
        count=count_flag,
        trace=trace_flag,
        countfuncs=funcs_flag,
        countcallers=callers_flag,
        ignoremods=tuple(modules),
        ignoredirs=tuple(directories),
        infile=source,
        outfile=destination,
    )


def run_traced(
    func: Callable[..., Any],
    *args: Any,
    tracer: Optional[_trace.Trace] = None,
    **kwargs: Any,
) -> Tuple[Any, _trace.CoverageResults]:
    """Run *func* under a tracer and return its result and the recorded counts.

    Args:
        func: The callable to run.
        *args: Positional arguments passed to *func*.
        tracer: The tracer to run the code under. A counting tracer is created
            when this is ``None``.
        **kwargs: Keyword arguments passed to *func*.

    Returns:
        A tuple with the return value of *func* and the coverage results.

    Raises:
        TypeError: If *func* is not callable or *tracer* is not a tracer.
    """
    if not callable(func):
        raise TypeError(f"func must be callable, got {type(func).__name__}")
    active = new_tracer() if tracer is None else _require_tracer(tracer)
    result = active.runfunc(func, *args, **kwargs)
    return result, active.results()


def run_script_traced(
    path: Any,
    tracer: Optional[_trace.Trace] = None,
) -> Tuple[int, _trace.CoverageResults]:
    """Run the Python script at *path* under a tracer.

    Args:
        path: Path of the script to run.
        tracer: The tracer to run the script under. A counting tracer is
            created when this is ``None``.

    Returns:
        A tuple with the exit code of the script and the coverage results. A
        script that ends without calling :func:`sys.exit` exits with ``0``.

    Raises:
        TypeError: If *path* is not a path or *tracer* is not a tracer.
        FileNotFoundError: If the script does not exist.
    """
    script = _require_path(path, "path")
    if not script.is_file():
        raise FileNotFoundError(f"script not found: {script}")
    active = new_tracer() if tracer is None else _require_tracer(tracer)
    source = script.read_text(encoding="utf-8")
    code = compile(source, str(script), "exec")
    namespace: Dict[str, Any] = {"__name__": "__main__", "__file__": str(script)}
    exit_code = 0
    try:
        active.runctx(code, namespace, namespace)
    except SystemExit as request:
        requested = request.code
        if requested is None:
            exit_code = 0
        elif isinstance(requested, int):
            exit_code = requested
        else:
            print(requested, file=sys.stderr)
            exit_code = 1
    return exit_code, active.results()


def counted_lines(results: object) -> Dict[Tuple[str, int], int]:
    """Return how often every recorded line was executed.

    Args:
        results: The coverage results of a run.

    Returns:
        A mapping from a ``(file name, line number)`` pair to the number of
        executions of that line.

    Raises:
        TypeError: If *results* does not hold coverage results.
    """
    data = _require_results(results)
    return {(str(name), int(number)): int(count) for (name, number), count in data.counts.items()}


def line_counts(results: object) -> Dict[str, Dict[int, int]]:
    """Return the execution counts of the recorded lines, grouped by file.

    Args:
        results: The coverage results of a run.

    Returns:
        A mapping from a file name to a mapping from a line number to the
        number of executions of that line.

    Raises:
        TypeError: If *results* does not hold coverage results.
    """
    per_file: Dict[str, Dict[int, int]] = {}
    for (name, number), count in counted_lines(results).items():
        per_file.setdefault(name, {})[number] = count
    return per_file


def called_functions(results: object) -> List[Tuple[str, str, str]]:
    """Return the functions that were called during the traced run.

    Args:
        results: The coverage results of a run.

    Returns:
        A sorted list of ``(file name, module name, function name)`` triples.

    Raises:
        TypeError: If *results* does not hold coverage results.
    """
    data = _require_results(results)
    return sorted((str(name), str(module), str(func)) for name, module, func in data.calledfuncs)


def call_relationships(results: object) -> List[Tuple[Tuple[str, str, str], Tuple[str, str, str]]]:
    """Return the calling relationships recorded during the traced run.

    Args:
        results: The coverage results of a run.

    Returns:
        A sorted list of ``(caller, callee)`` pairs, each holding a
        ``(file name, module name, function name)`` triple.

    Raises:
        TypeError: If *results* does not hold coverage results.
    """
    data = _require_results(results)
    return sorted(
        (
            (str(caller[0]), str(caller[1]), str(caller[2])),
            (str(callee[0]), str(callee[1]), str(callee[2])),
        )
        for caller, callee in data.callers
    )


def is_ignored_filename(results: object, filename: str) -> bool:
    """Return whether *filename* is excluded from the coverage report.

    Args:
        results: The coverage results of a run.
        filename: Name of the file to check.

    Returns:
        ``True`` when the file is not reported, ``False`` otherwise.

    Raises:
        TypeError: If *results* does not hold coverage results or *filename* is
            not a string.
    """
    data = _require_results(results)
    return bool(data.is_ignored_filename(_require_text(filename, "filename")))


def merge_results(results: object, other: object) -> _trace.CoverageResults:
    """Merge the counts of *other* into *results*.

    Args:
        results: The coverage results that receive the counts.
        other: The coverage results that are merged in.

    Returns:
        The updated *results*.

    Raises:
        TypeError: If either argument does not hold coverage results.
    """
    data = _require_results(results)
    extra = _require_results(other, "other")
    data.update(extra)
    return data


def write_coverage_report(
    results: object,
    coverdir: Optional[str] = None,
    show_missing: bool = True,
    summary: bool = False,
) -> None:
    """Write the coverage report of *results*.

    Args:
        results: The coverage results of a run.
        coverdir: Directory the report files are written to. The files are
            written next to the traced sources when this is ``None``.
        show_missing: Whether the lines that were not executed are reported.
        summary: Whether a summary of the coverage per module is printed.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    data = _require_results(results)
    directory = None if coverdir is None else _require_text(coverdir, "coverdir")
    missing_flag = _require_bool(show_missing, "show_missing")
    summary_flag = _require_bool(summary, "summary")
    data.write_results(show_missing=missing_flag, summary=summary_flag, coverdir=directory)


def summarize_coverage(results: object) -> List[Dict[str, Any]]:
    """Return a coverage summary of every file recorded in *results*.

    Args:
        results: The coverage results of a run.

    Returns:
        One entry per file, sorted by file name. Every entry holds the
        ``file`` name, the number of ``lines`` that hold a statement, the
        number of ``covered`` lines, the number of ``missing`` lines, the
        number of ``hits`` of the covered lines, and the ``percent`` of the
        lines that were covered.

    Raises:
        TypeError: If *results* does not hold coverage results.
    """
    data = _require_results(results)
    summaries: List[Dict[str, Any]] = []
    for name, counts in sorted(line_counts(data).items()):
        if data.is_ignored_filename(name):
            continue
        hit_lines = set(counts)
        executable = _executable_lines(name)
        if executable is None:
            executable = set(hit_lines)
        covered = len(hit_lines & executable)
        total = len(executable)
        summaries.append(
            {
                "file": name,
                "lines": total,
                "covered": covered,
                "missing": total - covered,
                "hits": sum(counts.values()),
                "percent": round(100.0 * covered / total, 1) if total else 0.0,
            }
        )
    return summaries


def format_coverage_summary(summaries: object) -> str:
    """Render coverage summaries as a readable table.

    Args:
        summaries: The entries returned by :func:`summarize_coverage`.

    Returns:
        A table with one row per entry.

    Raises:
        TypeError: If *summaries* is not a sequence of mappings.
    """
    if isinstance(summaries, (str, bytes)) or not isinstance(summaries, (list, tuple)):
        raise TypeError(f"summaries must be a sequence of mappings, got {type(summaries).__name__}")
    header = f"{'file':<40} {'lines':>7} {'covered':>8} {'missing':>8} {'cover%':>7}"
    rows = [header, "-" * len(header)]
    for entry in summaries:
        if not isinstance(entry, Mapping):
            raise TypeError(f"every summary must be a mapping, got {type(entry).__name__}")
        rows.append(
            "{file:<40} {lines:>7} {covered:>8} {missing:>8} {percent:>6.1f}%".format(
                file=str(entry.get("file", "")),
                lines=int(entry.get("lines", 0)),
                covered=int(entry.get("covered", 0)),
                missing=int(entry.get("missing", 0)),
                percent=float(entry.get("percent", 0.0)),
            )
        )
    return "\n".join(rows)


def clear_counts(tracer: object) -> None:
    """Discard the line counts recorded by *tracer*.

    Args:
        tracer: The tracer whose counts are cleared.

    Raises:
        TypeError: If *tracer* is not a tracer.
    """
    active = _require_tracer(tracer)
    active.counts.clear()


Trace = _trace.Trace
CoverageResults = _trace.CoverageResults
PRAGMA_NOCOVER = getattr(_trace, "PRAGMA_NOCOVER", "#pragma NO COVER")
