#!/usr/bin/env python3
"""Audit docstring ``Raises:`` clauses against the exceptions a function raises.

A wrapper module promises, in the ``Raises:`` section of each function's
docstring, which exception types callers may expect. This tool parses every
top-level module, extracts the documented exception type names from each
function's docstring, and checks whether the function (or a same-module helper
it calls, transitively) actually raises each documented type.

The audit is intentionally conservative so it stays quiet on legitimate
documentation of exceptions raised by delegated standard-library calls. A
function is only reported when *none* of the following raise the documented
type:

* a ``raise ExcType(...)`` statement directly in the function body,
* a ``raise ExcType`` statement anywhere reachable through same-module helper
  calls (bounded by ``--depth``).

Exceptions documented by delegation to the standard library (for example
``OSError`` from ``tempfile`` or ``KeyError`` from ``str.format``) are still
reported by the default heuristic because the standard library is opaque to the
tracer; they are low-signal and are expected to remain. The tool's value is in
surfacing the *high-signal* cases: a function that documents ``TypeError`` for a
parameter it never validates.

Usage:
    python tools/audit_contracts.py [--json] [--summary] [--depth N]

Exit codes:
    0  scan completed (issues, if any, are reported on stdout)
    1  a syntax error prevented a file from being scanned
    2  invalid command-line arguments
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent

#: Directories never scanned. Mirrors the exclusions used by the other tools in
#: ``tools/`` so the audit agrees with them about what "the repository" is.
SKIP_DIRS = frozenset(
    {
        "__pycache__",
        ".git",
        ".mypy_cache",
        ".ruff_cache",
        "build",
        "dist",
        ".kilo",
        "agentic_coding_scaffolding.egg-info",
    }
)

#: Docstring section header that introduces documented exceptions.
RAISES_HEADER = "Raises:"

#: Matches a docstring section header line such as ``Args:`` or ``Examples:``
#: regardless of indentation. A header is a single word (or words) followed by
#: a colon and nothing else on the line; exception entries carry a description
#: after the colon (``TypeError: If x is wrong.``) and so never match.
_SECTION_HEADER = re.compile(r"^\s*[A-Za-z][\w ]*:\s*$")


def iter_python_files(root: Path) -> Iterable[Path]:
    """Yield every ``*.py`` file under *root* except in :data:`SKIP_DIRS`."""
    for path in sorted(root.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def documented_raises(doc: str | None) -> Dict[str, int]:
    """Return documented exception type names mapped to their docstring offset.

    Only names that look like exception classes (start with an uppercase letter
    and are valid identifiers) are returned. The offset is the zero-based line
    within the docstring where the name first appears, which lets callers cite
    the docstring location.
    """
    if not doc:
        return {}
    result: Dict[str, int] = {}
    in_raises = False
    for idx, raw in enumerate(doc.splitlines()):
        stripped = raw.strip()
        if stripped.startswith(RAISES_HEADER):
            in_raises = True
            after = stripped[len(RAISES_HEADER) :].strip()
            if after:
                name = after.split(":")[0].split("(")[0].strip()
                if name and name[0].isupper() and name.isidentifier():
                    result.setdefault(name, idx)
            continue
        if not in_raises:
            continue
        # A new section header (e.g. ``Examples:`` or ``Args:``), indented or
        # not, ends the Raises block. Headers carry no description after the
        # colon, which is what distinguishes them from exception entries.
        if _SECTION_HEADER.match(raw):
            in_raises = False
            continue
        token = stripped.split(":")[0]
        for part in token.split(","):
            name = part.strip().split("(")[0].strip()
            if name and name[0].isupper() and name.isidentifier():
                result.setdefault(name, idx)
    return result


def direct_raises(fn: ast.AST) -> Set[str]:
    """Return the exception type names raised directly inside *fn*."""
    raised: Set[str] = set()
    for sub in ast.walk(fn):
        if isinstance(sub, ast.Raise) and sub.exc is not None:
            target = sub.exc.func if isinstance(sub.exc, ast.Call) else sub.exc
            for inner in ast.walk(target):
                if isinstance(inner, ast.Name):
                    raised.add(inner.id)
                elif isinstance(inner, ast.Attribute):
                    raised.add(inner.attr)
    return raised


def called_names(fn: ast.AST) -> Set[str]:
    """Return the names of every callable invoked inside *fn*."""
    called: Set[str] = set()
    for sub in ast.walk(fn):
        if isinstance(sub, ast.Call):
            func = sub.func
            if isinstance(func, ast.Name):
                called.add(func.id)
            elif isinstance(func, ast.Attribute):
                called.add(func.attr)
    return called


def build_index(tree: ast.AST) -> Dict[str, ast.AST]:
    """Map each function name to its definition for same-module resolution."""
    index: Dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            index.setdefault(node.name, node)
    return index


def raises_closure(
    fn: ast.AST,
    index: Dict[str, ast.AST],
    depth: int,
    seen: frozenset[str] = frozenset(),
) -> Set[str]:
    """Return every exception type raised by *fn*, following helper calls.

    *depth* bounds how many levels of same-module helper calls are followed so
    the traversal terminates on cyclic call graphs. *seen* guards against
    re-entering a helper already on the current path.
    """
    result = direct_raises(fn)
    if depth <= 0:
        return result
    for called in called_names(fn):
        if called in seen:
            continue
        target = index.get(called)
        if target is None:
            continue
        result |= raises_closure(target, index, depth - 1, seen | {called})
    return result


def audit_source(source: str, filename: str, depth: int = 3) -> Tuple[List[dict], bool]:
    """Audit one source string.

    *depth* bounds how many levels of same-module helper calls are followed when
    checking whether a documented exception is actually raised. It defaults to
    the CLI default so direct callers keep the documented behaviour.

    Returns ``(issues, syntax_ok)``. Each issue is a dict with ``function``,
    ``exception``, and ``line`` keys. ``syntax_ok`` is ``False`` when the source
    could not be parsed.
    """
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError:
        return [], False
    index = build_index(tree)
    issues: List[dict] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        doc = ast.get_docstring(node) or ""
        documented = documented_raises(doc)
        if not documented:
            continue
        raised = raises_closure(node, index, depth)
        for exc_name, offset in documented.items():
            if exc_name not in raised:
                issues.append(
                    {
                        "function": node.name,
                        "exception": exc_name,
                        "line": node.lineno,
                        "doc_line": offset,
                    }
                )
    return issues, True


def audit_paths(paths: Iterable[Path], depth: int = 3) -> Tuple[List[dict], List[str]]:
    """Audit every file in *paths*.

    Returns ``(issues, syntax_errors)``. Each issue carries a ``path`` key. Each
    syntax error is a ``"path: message"`` string.
    """
    issues: List[dict] = []
    syntax_errors: List[str] = []
    for path in paths:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:  # pragma: no cover - defensive
            syntax_errors.append(f"{path}: {exc}")
            continue
        file_issues, ok = audit_source(source, str(path), depth=depth)
        if not ok:
            syntax_errors.append(f"{path}: could not parse")
            continue
        for issue in file_issues:
            issue["path"] = str(path)
            issues.append(issue)
    return issues, syntax_errors


def format_text(issues: List[dict], scanned: int) -> str:
    """Render the issue list as a human-readable report."""
    lines: List[str] = []
    for issue in issues:
        lines.append(
            f"{issue['path']}:{issue['line']}: {issue['function']}: "
            f"documents Raises: {issue['exception']} but never raises it"
        )
    lines.append("")
    lines.append(f"Scanned {scanned} file(s); {len(issues)} potential contract issue(s).")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the audit tool."""
    parser = argparse.ArgumentParser(
        prog="audit_contracts",
        description="Audit docstring Raises: clauses against actual raises.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to audit (default: the repository root).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the report as JSON instead of text.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Collapse the report to one line per file with its issue count.",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Maximum same-module helper-call depth to follow (default: 3).",
    )
    return parser


def expand_paths(paths: List[str]) -> List[Path]:
    """Expand the positional path arguments into a concrete file list."""
    if not paths:
        return list(iter_python_files(ROOT))
    files: List[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix == ".py":
            files.append(path)
        elif path.is_dir():
            files.extend(iter_python_files(path))
        else:
            print(f"warning: skipping {path!r} (not a .py file or directory)", file=sys.stderr)
    return files


def main(argv: List[str] | None = None) -> int:
    """Entry point. Returns a process exit code."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2
    if args.depth < 0:
        print("error: --depth must be non-negative", file=sys.stderr)
        return 2

    files = expand_paths(args.paths)
    issues, syntax_errors = audit_paths(files, depth=args.depth)

    for err in syntax_errors:
        print(f"error: {err}", file=sys.stderr)

    if args.json:
        payload = {"scanned": len(files), "issues": issues, "errors": syntax_errors}
        print(json.dumps(payload, indent=2))
    elif args.summary:
        counts: Dict[str, int] = {}
        for issue in issues:
            counts[issue["path"]] = counts.get(issue["path"], 0) + 1
        for path in sorted(counts):
            print(f"{path}: {counts[path]} issue(s)")
        print(f"\nScanned {len(files)} file(s); {len(issues)} potential contract issue(s).")
    else:
        print(format_text(issues, len(files)))

    return 1 if syntax_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
