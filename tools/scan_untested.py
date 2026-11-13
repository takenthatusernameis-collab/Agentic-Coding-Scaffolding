#!/usr/bin/env python3
"""Scan every top-level module for exported-but-untested public callables.

A wrapper module exposes its public helpers through ``__all__``. This scanner
reports every name in ``__all__`` that is a callable defined in the module (or
re-exported from a standard library alias) and has zero references in the
matching ``tests/test_*.py`` file. The scan is alias-aware: a name referenced
only through an import alias (``import traceback_utils as tb``) is resolved to
its real module so aliased references are no longer reported as false positives.

Names that are type variables, constants, classes, entry points, or interactive
stdlib facades are filtered out by default; pass ``--all`` to list them too.

Pass ``--summary`` to collapse the per-name report to one line per module with
its gap count, which is easier to scan when the list is long. ``--json`` takes
precedence when both flags are given.

Usage:
    python tools/scan_untested.py [--all] [--json] [--summary]
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: Persistent per-module mtime cache. Modules whose source and test mtimes
#: match a cached entry are not re-parsed; the cached gaps are reused. The
#: cache lives in ``.kilo/`` alongside the verification checkpoint and is
#: gitignored so it never marks the working tree dirty.
CACHE_FILE = ROOT / ".kilo" / "scan_untested_cache.json"

#: Modules that are not wrapper modules but still expose ``__all__``.
EXTRA_MODULES = (
    "stats.py",
    "strings.py",
    "shapes.py",
    "prompt_utils.py",
    "utils.py",
    "calculator.py",
    "config_schema.py",
)

#: Names that are known interactive facades, entry points, or constants rather
#: than hermetic, convention-consistent helpers.
SKIP_NAMES = {
    # entry points / interactive facades
    "main",
    "interact",
    "print_zen",
    "run_module",
    # interactive stdlib facades
    "termname",
    "lazycache",
    "is_available",
    "browse",
    "cli",
    "plainpager",
    "writedoc",
    "writedocs",
    "help",
    "UNSET",
}

#: A name is only "referenced" when it appears as a whole word, so a substring
#: such as ``help`` inside ``helpers`` is not mistaken for a real reference.
_WORD_BOUNDARY = r"\b"


def iter_modules() -> list[Path]:
    """Return every top-level module the scanner has to consider."""
    modules = sorted(ROOT.glob("*_utils.py"))
    for name in EXTRA_MODULES:
        path = ROOT / name
        if path.is_file():
            modules.append(path)
    return modules


def _mtime(path: Path) -> float | None:
    """Return the modification time of *path*, or ``None`` when it is absent."""
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def load_cache() -> dict:
    """Load the persistent per-module mtime cache, or an empty cache.

    A missing or corrupt cache file degrades gracefully to an empty cache so
    the next run performs a full scan and repopulates it.
    """
    try:
        data = json.loads(CACHE_FILE.read_text())
    except (OSError, ValueError):
        return {"modules": {}}
    if not isinstance(data, dict) or not isinstance(data.get("modules"), dict):
        return {"modules": {}}
    return data


def save_cache(cache: dict) -> None:
    """Atomically persist *cache* to the cache file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_FILE.with_name(CACHE_FILE.name + ".tmp")
    tmp.write_text(json.dumps(cache, indent=2) + "\n")
    tmp.replace(CACHE_FILE)


def cached_entry(cache: dict, path: Path, source_mtime: float | None,
                 test_mtime: float | None) -> list[str] | None:
    """Return the cached gaps for *path* when its mtimes still match.

    Returns ``None`` when there is no valid cache entry, signalling that the
    module must be re-scanned.
    """
    entry = cache.get("modules", {}).get(path.name)
    if not isinstance(entry, dict):
        return None
    if entry.get("source_mtime") != source_mtime:
        return None
    if entry.get("test_mtime") != test_mtime:
        return None
    gaps = entry.get("gaps")
    return gaps if isinstance(gaps, list) else None


def string_constants(node: ast.expr | None) -> set[str]:
    """Return the string constants of a list/tuple/set literal.

    Anything that is not such a literal (a name, a comprehension, a call)
    yields an empty set so the caller treats the export list as unknown.
    A ``BinOp`` with an ``Add`` operator (for example
    ``__all__ = ["a", "b"] + sorted(_NAMES)``) is handled by collecting the
    string constants from both operands, so statically-known exports are not
    silently dropped when a module concatenates a literal list with a dynamic
    one.

    Example:
        >>> import ast
        >>> string_constants(ast.parse('__all__ = ["a", "b"] + sorted(_NAMES)').body[0].value)
        {'a', 'b'}
        >>> string_constants(ast.parse('__all__ = ["a", "b"] + ["c"]').body[0].value)
        {'a', 'b', 'c'}
        >>> string_constants(ast.parse('__all__ = sorted(_NAMES)').body[0].value)
        set()
        >>> string_constants(ast.parse('__all__ = ["a"]').body[0].value)
        {'a'}
    """
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return {
            elt.value
            for elt in node.elts
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
        }
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return string_constants(node.left) | string_constants(node.right)
    return set()


def exported_names(tree: ast.Module) -> set[str]:
    """Return the names listed in the module's ``__all__``.

    Both the plain (``__all__ = [...]``) and the annotated
    (``__all__: list[str] = [...]``) forms are recognized. The annotated form
    was previously ignored, which silently skipped every module that declared
    its exports with a type annotation.
    """
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return string_constants(node.value)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                return string_constants(node.value)
    return set()


def alias_map(tree: ast.Module) -> dict[str, str]:
    """Return a mapping from alias name to real module name.

    ``import traceback_utils as tb`` maps ``tb`` to ``traceback_utils`` so a
    reference through the alias is resolved to the real module.
    """
    mapping: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                mapping[local] = alias.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                local = alias.asname or alias.name
                module = node.module or ""
                mapping[local] = f"{module}.{alias.name}" if module else alias.name
    return mapping


def is_function_export(tree: ast.Module, name: str) -> bool:
    """Return ``True`` when *name* is a function defined at the top level.

    Re-exported classes, constants, and type variables are not wrapper
    helpers and are excluded so the scan reports only genuine gaps.
    """
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == name:
                return True
    return False


def is_typevar_or_constant(tree: ast.Module, name: str) -> bool:
    """Return ``True`` when *name* is a TypeVar or a module-level constant."""
    for node in tree.body:
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == name:
                annotation = node.annotation
                if isinstance(annotation, ast.Name) and annotation.id in ("TypeVar", "ParamSpec"):
                    return True
                if isinstance(node.value, ast.Constant):
                    return True
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    if isinstance(node.value, ast.Call):
                        func = node.value.func
                        if isinstance(func, ast.Name) and func.id in ("TypeVar", "ParamSpec"):
                            return True
                    if isinstance(node.value, ast.Constant):
                        return True
    return False


def referenced_in_test(module_stem: str, test_text: str, alias_map_: dict[str, str]) -> bool:
    """Return ``True`` when the module is referenced in the test text."""
    if module_stem in test_text:
        return True
    for alias, real in alias_map_.items():
        if real == module_stem and alias in test_text:
            return True
    return False


def name_referenced(test_text: str, name: str) -> bool:
    """Return ``True`` when *name* appears as a whole word in the test text.

    A bare substring test is too loose: the interactive ``help`` facade of
    ``pydoc_utils`` was reported as tested because ``help`` is a substring of
    ``helpers`` in the test prose. Word-boundary matching makes a reference
    real without reporting false positives for embedded substrings.
    """
    return re.search(_WORD_BOUNDARY + re.escape(name) + _WORD_BOUNDARY, test_text) is not None


def scan_module(path: Path, show_all: bool = False) -> list[str]:
    """Return the exported-but-untested callables of *path*.

    By default only genuine gaps are reported: a public callable that the
    module itself defines. Type variables, constants, classes, entry points,
    and interactive stdlib facades are filtered out because they are not
    hermetic helpers. Passing *show_all* disables those filters and reports
    every exported name that the module's test does not reference, which is
    what ``--all`` documents.
    """
    tree = ast.parse(path.read_text())
    names = exported_names(tree)
    if not names:
        return []
    aliases = alias_map(tree)
    test_path = ROOT / "tests" / f"test_{path.stem}.py"
    test_text = test_path.read_text() if test_path.is_file() else ""
    module_referenced = referenced_in_test(path.stem, test_text, aliases)
    gaps: list[str] = []
    for name in sorted(names):
        if name.startswith("_"):
            continue
        # A name referenced anywhere in the module's test counts as tested in
        # both modes; ``--all`` widens which names are eligible, not which
        # references count.
        if module_referenced and name_referenced(test_text, name):
            continue
        if not show_all:
            if name in SKIP_NAMES:
                continue
            if not is_function_export(tree, name):
                continue
            if is_typevar_or_constant(tree, name):
                continue
        gaps.append(name)
    return gaps


def format_summary(results: dict[str, list[str]], total: int) -> str:
    """Return a one-line-per-module summary of *results*.

    Args:
        results: Mapping of module file name to its exported-but-untested
            callable names.
        total: Total number of reported callables across every module.

    Returns:
        A human-readable summary string. When *total* is zero a fixed clean
        message is returned instead of an empty report.

    Example:
        >>> format_summary({"a_utils.py": ["x", "y"], "b_utils.py": ["z"]}, 3)
        'a_utils.py: 2\\nb_utils.py: 1\\n\\n3 exported-but-untested callables in 2 modules'
        >>> format_summary({}, 0)
        'no exported-but-untested callables'
    """
    if not total:
        return "no exported-but-untested callables"
    lines = [f"{module_name}: {len(gaps)}" for module_name, gaps in results.items()]
    lines.append(
        f"\n{total} exported-but-untested callables in {len(results)} modules"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Print every exported-but-untested callable.

    ``--summary`` collapses the report to one line per module with a gap count.
    ``--json`` takes precedence when both ``--summary`` and ``--json`` are given.
    """
    args = argv or []
    show_all = "--all" in args
    json_output = "--json" in args
    summary = "--summary" in args
    total = 0
    results = {}
    #: ``--all`` widens the report, so it always re-scans and never reads or
    #: writes the cache (whose entries are default-mode results only).
    cache = load_cache() if not show_all else {"modules": {}}
    for path in iter_modules():
        source_mtime = _mtime(path)
        test_path = ROOT / "tests" / f"test_{path.stem}.py"
        test_mtime = _mtime(test_path)
        cached = cached_entry(cache, path, source_mtime, test_mtime)
        if cached is not None:
            gaps = cached
        else:
            gaps = scan_module(path, show_all)
        if gaps:
            total += len(gaps)
            results[path.name] = gaps
        cache.setdefault("modules", {})[path.name] = {
            "source_mtime": source_mtime,
            "test_mtime": test_mtime,
            "gaps": gaps,
        }
    if not show_all:
        save_cache(cache)
    if json_output:
        print(json.dumps({"gaps": results, "total": total}, indent=2))
        return 1 if total else 0
    if summary:
        print(format_summary(results, total))
        return 1 if total else 0
    if total:
        for module_name, gaps in results.items():
            print(f"{module_name}:")
            for name in gaps:
                print(f"  {name}")
        print(f"\n{total} exported-but-untested callables")
        return 1
    print("no exported-but-untested callables")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
