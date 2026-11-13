#!/usr/bin/env python3
"""Select relevant tests based on changed files.

Given a list of changed source files (or git status/diff output), this tool
maps them to their corresponding test files and returns the test module names
that should be run. This enables targeted test runs for local development
while preserving the full suite for CI/milestones.

Usage:
    python tools/select_tests.py [--changed-files FILE1 FILE2 ...]
    python tools/select_tests.py --from-git [--base REF] [--head REF]
    python tools/select_tests.py --all (returns all test modules)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests"

# Files that are not source modules but changes to them should trigger full test suite
FULL_SUITE_TRIGGERS = {
    "Makefile",
    "pyproject.toml",
    "scaffold.sh",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    ".kilo/command/scaffold-project.md",
    "tools/verify_state_delta.py",
    "tools/refresh_scaffold.py",
    "tools/scan_untested.py",
    "tools/select_tests.py",
}

# Source file patterns that map to test files
SOURCE_GLOBS = (
    "*.py",
    "Makefile",
    "pyproject.toml",
    "scaffold.sh",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    ".kilo/command/scaffold-project.md",
    "tools/*.py",
)


def run_git(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd, cwd=ROOT, text=True, capture_output=True, check=False
    )


def get_changed_files_from_git(base: str | None = None, head: str = "HEAD") -> list[str]:
    """Get list of changed files from git diff."""
    cmd = ["git", "diff", "--name-only"]
    if base:
        cmd.extend([base, head])
    else:
        cmd.append(head)
    cmd.extend(["--"] + list(SOURCE_GLOBS))
    result = run_git(cmd)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]


def get_untracked_files() -> list[str]:
    """Get list of untracked source files."""
    result = run_git(["git", "status", "--porcelain", "--"] + list(SOURCE_GLOBS))
    if result.returncode != 0:
        return []
    files = []
    for line in result.stdout.strip().splitlines():
        if line.startswith("?? "):
            files.append(line[3:].strip())
    return files


def map_source_to_test(source_file: str) -> str | None:
    """Map a source file to its test module name.

    Returns the test module name (e.g., 'tests.test_abc_utils') or None if
    the file doesn't have a direct test mapping.
    """
    path = Path(source_file).resolve()

    # Check for full-suite triggers
    if path.name in FULL_SUITE_TRIGGERS:
        return "FULL_SUITE"

    # Handle tools/*.py files
    if path.parent.name == "tools" and path.suffix == ".py":
        test_name = f"test_{path.stem}.py"
        test_path = TESTS_DIR / test_name
        if test_path.is_file():
            return f"tests.test_{path.stem}"
        return "FULL_SUITE"  # Tool changes without direct test should run full suite

    # Handle root-level *.py files
    try:
        if path.relative_to(ROOT).parts[0] != "tests" and path.suffix == ".py":
            test_name = f"test_{path.stem}.py"
            test_path = TESTS_DIR / test_name
            if test_path.is_file():
                return f"tests.test_{path.stem}"
            # Non-wrapper modules like stats.py, strings.py, shapes.py, etc.
            # Check if they have tests
            return None
    except ValueError:
        # Path is not under ROOT
        pass

    # Handle .kilo/command/*.md
    if "command" in path.parts and path.suffix == ".md":
        return "FULL_SUITE"

    return None


def select_tests(changed_files: list[str]) -> tuple[list[str], bool]:
    """Select test modules to run based on changed files.

    Returns:
        Tuple of (test_modules, run_full_suite)
        - test_modules: List of test module names to run (e.g., ['tests.test_abc_utils'])
        - run_full_suite: True if full test suite should be run
    """
    if not changed_files:
        return [], False

    test_modules = set()
    run_full = False

    for f in changed_files:
        mapped = map_source_to_test(f)
        if mapped == "FULL_SUITE":
            run_full = True
            break
        elif mapped:
            test_modules.add(mapped)

    return sorted(test_modules), run_full


def get_all_test_modules() -> list[str]:
    """Get all test module names."""
    modules = []
    for test_file in sorted(TESTS_DIR.glob("test_*.py")):
        if test_file.is_file():
            modules.append(f"tests.{test_file.stem}")
    return modules


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Select relevant tests based on changed files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--changed-files",
        nargs="*",
        help="List of changed source files",
    )
    parser.add_argument(
        "--from-git",
        action="store_true",
        help="Get changed files from git diff (unstaged + staged)",
    )
    parser.add_argument(
        "--base",
        help="Base ref for git diff (default: HEAD~1 for --from-git)",
    )
    parser.add_argument(
        "--head",
        default="HEAD",
        help="Head ref for git diff (default: HEAD)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Return all test modules",
    )
    parser.add_argument(
        "--include-untracked",
        action="store_true",
        help="Include untracked files when using --from-git",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    args = parser.parse_args(argv)

    if args.all:
        modules = get_all_test_modules()
        run_full = True
    elif args.from_git:
        changed = get_changed_files_from_git(args.base, args.head)
        if args.include_untracked:
            changed.extend(get_untracked_files())
        modules, run_full = select_tests(changed)
    elif args.changed_files:
        modules, run_full = select_tests(args.changed_files)
    else:
        # Default: from git with untracked
        changed = get_changed_files_from_git()
        changed.extend(get_untracked_files())
        modules, run_full = select_tests(changed)

    if args.json:
        import json
        print(json.dumps({"modules": modules, "run_full_suite": run_full}))
    else:
        if run_full:
            print("FULL_SUITE")
        else:
            for m in modules:
                print(m)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))