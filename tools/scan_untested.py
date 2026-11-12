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

Usage:
    python tools/scan_untested.py [--all]
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: Modules that are not wrapper modules but still expose ``__all__``.
EXTRA_MODULES = ("stats.py", "strings.py", "shapes.py", "prompt_utils.py")

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


def exported_names(tree: ast.Module) -> set[str]:
    """Return the names listed in the module's ``__all__``."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                        return {
                            elt.value
                            for elt in node.value.elts
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                        }
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


def scan_module(path: Path, show_all: bool) -> list[str]:
    """Return the exported-but-untested callables of *path*."""
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
        if name in SKIP_NAMES:
            continue
        if not is_function_export(tree, name):
            continue
        if is_typevar_or_constant(tree, name):
            continue
        if module_referenced and name_referenced(test_text, name):
            continue
        gaps.append(name)
    return gaps


def main(argv: list[str] | None = None) -> int:
    """Print every exported-but-untested callable."""
    show_all = "--all" in (argv or [])
    total = 0
    for path in iter_modules():
        gaps = scan_module(path, show_all)
        if gaps:
            total += len(gaps)
            print(f"{path.name}:")
            for name in gaps:
                print(f"  {name}")
    if total:
        print(f"\n{total} exported-but-untested callables")
        return 1
    print("no exported-but-untested callables")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
