#!/usr/bin/env bash
#
# scaffold.sh - Generate a complete agentic coding project template
#
# Usage: ./scaffold.sh <project-name> [output-dir]
#
# Creates a ready-to-use project structure with:
#   - GitHub Actions workflow (Kilo agent loop)
#   - AGENTS.md with project-specific instructions
#   - README.md for the new project
#   - CHANGELOG.md following Keep a Changelog format
#   - .pre-commit-config.yaml with ruff, mypy, unittest, and scaffold hooks
#   - kilo.json configuration with the scaffolder subagent
#   - .kilo/agent/scaffolder.md, .kilo/command/handover.md,
#     .kilo/command/scaffold-project.md, .kilo/skill/scaffolding-helper.md
#   - .kilo/.gitignore
#   - .gitignore
#   - Makefile with common developer targets (test, lint, typecheck, run,
#     scaffold, clean, help, pre-commit-install, pre-commit-run)
#   - pyproject.toml for Python project configuration and dependencies
#   - hello.py sample application entry point
#   - calculator.py simple calculator module with arithmetic operations
#   - shapes.py geometry utilities for areas and perimeters of common shapes
#   - strings.py string utilities for text operations
#   - tests/test_hello.py unit tests for the sample application
#   - tests/test_calculator.py unit tests for the calculator module
#   - tests/test_shapes.py unit tests for the shapes module
#   - tests/test_strings.py unit tests for the strings module
#   - utils.py general utility helper functions
#   - tests/test_utils.py unit tests for the utils module
#
set -euo pipefail

usage() {
    cat <<EOF
Usage: $0 <project-name> [output-dir] [--no-test]

Arguments:
  project-name   Name for the new project (used in README, etc.)
  output-dir     Destination directory (default: ./<project-name>)
  --no-test      Skip the post-scaffold smoke test (default: run it)

Examples:
  $0 my-new-project
  $0 "My Project" /tmp/projects/my-project
  $0 my-new-project ./out --no-test
EOF
    exit 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
  usage
fi

PROJECT_NAME="$1"

# Normalize project name for use as a directory identifier
PROJECT_ID=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr -s ' ' '-' | tr -cd 'a-z0-9-')

if [[ -z "$PROJECT_ID" ]]; then
    echo "Error: Could not normalize project name '$PROJECT_NAME' to a valid identifier." >&2
    exit 1
fi

SMOKE_TEST=1
OUTPUT_DIR=""
shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-test)
            SMOKE_TEST=0
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$OUTPUT_DIR" ]]; then
                OUTPUT_DIR="$1"
            else
                echo "Warning: Unexpected argument '$1'" >&2
            fi
            ;;
    esac
    shift
done

OUTPUT_DIR="${OUTPUT_DIR:-./${PROJECT_ID}}"

if [[ -d "$OUTPUT_DIR" ]]; then
    echo "Warning: Output directory '$OUTPUT_DIR' already exists." >&2
    echo "Existing files will not be overwritten, but new files will be created." >&2
fi

mkdir -p "$OUTPUT_DIR"/{.github/workflows,.kilo/agent,.kilo/command,.kilo/skill,tests}

# --- .github/workflows/main.yml ---
cat > "$OUTPUT_DIR/.github/workflows/main.yml" <<'WORKFLOW'
name: Kilo General Agent Loop

on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:
    inputs:
      agents:
        description: "Maximum sequential Kilo worker sessions for this activation"
        required: false
        default: "1000"
        type: number

permissions:
  contents: write

concurrency:
  group: kilo-repository
  cancel-in-progress: false

jobs:
  kilo:
    runs-on: ubuntu-24.04
    timeout-minutes: 360

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
          persist-credentials: true

      - name: Run general-purpose Kilo agent loop
        id: kilo
        shell: bash
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          KILO_DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
          KILO_INPUT_AGENTS: ${{ inputs.agents || '1000' }}
          KILO_IDLE_TIMEOUT_SECONDS: "900"
        run: |
          set -Eeuo pipefail
          umask 077

          command='Execute the task assigned by the previous agent and prepare a task for the next agent!'

          echo "Starting Kilo agent loop for project: ${KILO_DEFAULT_BRANCH:-<project>}"
          echo "Run prompt: $command"

          # Install the Kilo CLI
          npm install --no-audit --no-fund --prefix "$RUNNER_TEMP/kilo" @kilocode/cli@7.7.1
          export PATH="$RUNNER_TEMP/kilo/node_modules/.bin:$PATH"
          kilo --version

          git config user.name "kilo-autonomous"
          git config user.email "kilo-autonomous@users.noreply.github.com"

          agents="${KILO_INPUT_AGENTS:-1000}"
          if ! [[ "$agents" =~ ^[0-9]+$ ]]; then agents=1000; fi
          (( agents < 1 )) && agents=1
          (( agents > 1000 )) && agents=1000

          for ((agent_index=1; agent_index<=agents; agent_index++)); do
            echo "Starting Kilo session ${agent_index}/${agents}"

            kilo run --model kilo/kilo-auto/free --auto "$command"

            # Commit any non-workflow changes
            git restore --source=HEAD --staged --worktree -- .github/workflows >/dev/null 2>&1 || true
            git add -A -- . ':(exclude).github/workflows/**' ':(exclude).git/**'
            if ! git diff --cached --quiet; then
              git commit -m "chore(kilo): checkpoint agent session"
              git push origin "HEAD:$(git rev-parse --abbrev-ref HEAD)" || true
              echo "Checkpoint committed and pushed."
            fi
          done
WORKFLOW

# --- .gitignore ---
cat > "$OUTPUT_DIR/.gitignore" <<'GITIGNORE'
node_modules/
*.log
.DS_Store
*.sqlite
*.sqlite3
*.db
.env
.env.*
.venv/
venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.tox/
coverage.xml
.coverage
*.pyc
*.pyo
kilo-session-*.log
kilo-progress-*.log
*.tmp
GITIGNORE

# --- .pre-commit-config.yaml ---
cat > "$OUTPUT_DIR/.pre-commit-config.yaml" <<'PRECOMMIT'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
      - id: ruff-format
      - id: check-toml

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: debug-statements
      - id: check-merge-conflict
      - id: check-added-large-files

  - repo: local
    hooks:
      - id: typecheck
        name: mypy
        entry: mypy . --exclude build --exclude dist
        language: system
        types: [python]
      - id: tests
        name: pytest
        entry: python -m unittest discover tests/
        language: system
        types: [python]
        pass_filenames: false
      - id: scaffold-test
        name: scaffold.sh smoke test
        entry: bash -c './scaffold.sh "__pre-commit-smoke__" /tmp/scaffold-pre-commit-smoke --no-test && rm -rf /tmp/scaffold-pre-commit-smoke'
        language: system
        pass_filenames: false
        always_run: true
PRECOMMIT

# --- Makefile ---
    cat > "$OUTPUT_DIR/Makefile" <<MAKEFILE
# Makefile for ${PROJECT_NAME}
# Common developer commands for project management

.PHONY: test lint typecheck run scaffold clean help pre-commit-install pre-commit-run

## Run the Python test suite using pytest (falling back to unittest if pytest is unavailable)
test:
	@echo "Running tests..."
	@if command -v pytest >/dev/null 2>&1; then \\
		pytest tests/ -v; \\
	else \\
		python -m unittest discover tests/ -v; \\
	fi

## Run ruff to check code style and formatting
lint:
	@echo "Running linting..."
	@if python -m ruff --version >/dev/null 2>&1; then \\
		python -m ruff check .; \\
	else \\
		echo "ruff not installed. Install with: pip install ruff"; \\
		exit 1; \\
	fi

## Run mypy for static type checking
typecheck:
	@echo "Running type checking..."
	@if python -m mypy --version >/dev/null 2>&1; then \\
		python -m mypy . --exclude build --exclude dist; \\
	else \\
		echo "mypy not installed. Install with: pip install mypy"; \\
		exit 1; \\
	fi

## Run hello.py with an optional name argument (e.g., make run or make run NAME=Alice)
run:
	@echo "Running hello.py..."
	@python hello.py \$(NAME)

## Invoke scaffold.sh to scaffold a new project
scaffold:
	@echo "Running scaffold.sh..."
	@./scaffold.sh

## Install pre-commit hooks into .git/hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	@if command -v pre-commit >/dev/null 2>&1; then \\
		pre-commit install; \\
	else \\
		echo "pre-commit not installed. Install with: pip install pre-commit"; \\
		exit 1; \\
	fi

## Run all pre-commit hooks against tracked files
pre-commit-run:
	@echo "Running pre-commit hooks..."
	@if command -v pre-commit >/dev/null 2>&1; then \\
		pre-commit run --all-files; \\
	else \\
		echo "pre-commit not installed. Install with: pip install pre-commit"; \\
		exit 1; \\
	fi

## Remove __pycache__, .pytest_cache, and other build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type f -name "coverage.xml" -delete 2>/dev/null || true

## Print usage information for all available targets
help:
	@echo "Available targets:"
	@echo "  test       Run the Python test suite"
	@echo "  lint       Run ruff code style checker"
	@echo "  typecheck  Run mypy static type checking"
	@echo "  run        Run hello.py (usage: make run [NAME=YourName])"
	@echo "  scaffold   Scaffold a new project using scaffold.sh"
	@echo "  clean      Remove build artifacts"
	@echo "  help       Show this help message"
	@echo "  pre-commit-install  Install pre-commit hooks into .git/hooks"
	@echo "  pre-commit-run     Run all pre-commit hooks against tracked files"
MAKEFILE

# --- pyproject.toml ---
cat > "$OUTPUT_DIR/pyproject.toml" <<PYPROJECT
[project]
name = "${PROJECT_ID}"
version = "0.1.0"
description = "A project scaffolded for autonomous agentic coding with Kilo."
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "kilo-autonomous", email = "kilo-autonomous@users.noreply.github.com" }]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.8",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
strict = false
exclude = [
    "build",
    "dist",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.ruff.format]
docstring-code-format = true
PYPROJECT

# --- hello.py ---
cat > "$OUTPUT_DIR/hello.py" <<'HELLO'
import sys


def main(name: str = "World") -> None:
    """Print a greeting for the given name.

    Args:
        name: The name to greet. Defaults to "World".
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    cli_name = sys.argv[1] if len(sys.argv) > 1 else "World"
    main(cli_name)
HELLO

# --- tests/test_hello.py ---
cat > "$OUTPUT_DIR/tests/test_hello.py" <<'TESTHELLO'
import io
import unittest
from unittest.mock import patch

from hello import main


class TestHello(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_world(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_alice(self, mock_stdout):
        main("Alice")
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Alice!")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_with_custom_name(self, mock_stdout):
        main("Bob")
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Bob!")


if __name__ == '__main__':
    unittest.main()
TESTHELLO

# --- calculator.py ---
cat > "$OUTPUT_DIR/calculator.py" <<'CALCULATOR'
def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return the quotient of a and b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
CALCULATOR

# --- tests/test_calculator.py ---
cat > "$OUTPUT_DIR/tests/test_calculator.py" <<'TESTCALC'
import unittest

from calculator import add, divide, multiply, subtract


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 5), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)
        self.assertEqual(divide(-6, 3), -2)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(5, 0)


if __name__ == '__main__':
    unittest.main()
TESTCALC

# --- shapes.py ---
cat > "$OUTPUT_DIR/shapes.py" <<'SHAPES'
"""Geometry utilities for calculating areas and perimeters of common shapes."""

import math


def circle_area(radius: float) -> float:
    """Return the area of a circle with the given radius.

    Args:
        radius: The radius of the circle.

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return math.pi * radius ** 2

def circle_perimeter(radius: float) -> float:
    """Return the perimeter (circumference) of a circle with the given radius.

    Args:
        radius: The radius of the circle.

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return 2 * math.pi * radius

def rectangle_area(length: float, width: float) -> float:
    """Return the area of a rectangle.

    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.

    Raises:
        ValueError: If length or width is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return length * width

def rectangle_perimeter(length: float, width: float) -> float:
    """Return the perimeter of a rectangle.

    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.

    Raises:
        ValueError: If length or width is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return 2 * (length + width)

def triangle_area(base: float, height: float) -> float:
    """Return the area of a triangle given its base and height.

    Args:
        base: The base length of the triangle.
        height: The height of the triangle.

    Raises:
        ValueError: If base or height is negative.
    """
    if base < 0 or height < 0:
        raise ValueError("Base and height cannot be negative.")
    return 0.5 * base * height

def triangle_perimeter(side_a: float, side_b: float, side_c: float) -> float:
    """Return the perimeter of a triangle given its three sides.

    Args:
        side_a: Length of the first side.
        side_b: Length of the second side.
        side_c: Length of the third side.

    Raises:
        ValueError: If any side is negative or the sides violate the triangle inequality.
    """
    if side_a < 0 or side_b < 0 or side_c < 0:
        raise ValueError("Sides cannot be negative.")
    if not (side_a + side_b > side_c and side_a + side_c > side_b and side_b + side_c > side_a):
        raise ValueError("Sides do not form a valid triangle.")
    return side_a + side_b + side_c
SHAPES

# --- tests/test_shapes.py ---
cat > "$OUTPUT_DIR/tests/test_shapes.py" <<'TESTSHAPES'
import math
import unittest

from shapes import (
    circle_area,
    circle_perimeter,
    rectangle_area,
    rectangle_perimeter,
    triangle_area,
    triangle_perimeter,
)


class TestCircle(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(circle_area(0), 0)
        self.assertAlmostEqual(circle_area(1), math.pi)
        self.assertAlmostEqual(circle_area(2), math.pi * 4)

    def test_perimeter(self):
        self.assertAlmostEqual(circle_perimeter(0), 0)
        self.assertAlmostEqual(circle_perimeter(1), 2 * math.pi)
        self.assertAlmostEqual(circle_perimeter(2), 4 * math.pi)

    def test_negative_radius_area(self):
        with self.assertRaises(ValueError):
            circle_area(-1)

    def test_negative_radius_perimeter(self):
        with self.assertRaises(ValueError):
            circle_perimeter(-5)


class TestRectangle(unittest.TestCase):
    def test_area(self):
        self.assertEqual(rectangle_area(3, 4), 12)
        self.assertEqual(rectangle_area(0, 5), 0)
        self.assertEqual(rectangle_area(2.5, 4), 10)

    def test_perimeter(self):
        self.assertEqual(rectangle_perimeter(3, 4), 14)
        self.assertEqual(rectangle_perimeter(0, 0), 0)

    def test_negative_length_area(self):
        with self.assertRaises(ValueError):
            rectangle_area(-1, 4)

    def test_negative_width_perimeter(self):
        with self.assertRaises(ValueError):
            rectangle_perimeter(3, -2)


class TestTriangle(unittest.TestCase):
    def test_area(self):
        self.assertEqual(triangle_area(4, 3), 6)
        self.assertEqual(triangle_area(10, 5), 25)
        self.assertEqual(triangle_area(0, 5), 0)

    def test_perimeter(self):
        self.assertEqual(triangle_perimeter(3, 4, 5), 12)
        self.assertEqual(triangle_perimeter(1, 1, 1), 3)

    def test_invalid_triangle_inequality(self):
        with self.assertRaises(ValueError):
            triangle_perimeter(1, 2, 10)

    def test_negative_base_area(self):
        with self.assertRaises(ValueError):
            triangle_area(-1, 3)

    def test_negative_side_perimeter(self):
        with self.assertRaises(ValueError):
            triangle_perimeter(3, 4, -5)


if __name__ == '__main__':
    unittest.main()
TESTSHAPES

# --- strings.py ---
cat > "$OUTPUT_DIR/strings.py" <<'STRINGS'
"""String utility functions for common text operations."""


def reverse_string(s: str) -> str:
    """Return the reverse of the given string.

    Args:
        s: The string to reverse.

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("")
        ''
    """
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Return True if the string reads the same forwards and backwards.

    Comparison is case-insensitive and ignores non-alphanumeric characters.

    Args:
        s: The string to check.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
    """
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the given string.

    Comparison is case-insensitive.

    Args:
        s: The string to count vowels in.

    Examples:
        >>> count_vowels("hello")
        2
        >>> count_vowels("rhythm")
        0
    """
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch in vowels)
STRINGS

# --- utils.py ---
cat > "$OUTPUT_DIR/utils.py" <<'UTILS'
"""Utility helper functions."""

from typing import Any, List, TypeVar

T = TypeVar("T")


def flatten(lst: List[List[T]]) -> List[T]:
    """Flatten a list of lists into a single list."""
    result: List[T] = []
    for item in lst:
        result.extend(item)
    return result


def chunk(lst: List[T], size: int) -> List[List[T]]:
    """Split a list into chunks of the specified size."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def unique(lst: List[T]) -> List[T]:
    """Return a list of unique elements preserving order."""
    seen: set = set()
    result: List[T] = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def is_empty(value: Any) -> bool:
    """Check if a value is considered empty."""
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, set, dict)):
        return len(value) == 0
    return False
UTILS

# --- tests/test_strings.py ---
cat > "$OUTPUT_DIR/tests/test_strings.py" <<'TESTSTRINGS'
import unittest

from strings import count_vowels, is_palindrome, reverse_string


class TestReverseString(unittest.TestCase):
    def test_reverse_basic(self):
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_reverse_empty(self):
        self.assertEqual(reverse_string(""), "")

    def test_reverse_single_char(self):
        self.assertEqual(reverse_string("a"), "a")

    def test_reverse_palindrome(self):
        self.assertEqual(reverse_string("racecar"), "racecar")

    def test_reverse_with_spaces(self):
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")


class TestIsPalindrome(unittest.TestCase):
    def test_palindrome_odd(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_palindrome_even(self):
        self.assertTrue(is_palindrome("abba"))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_case_insensitive(self):
        self.assertTrue(is_palindrome("RaceCar"))

    def test_ignores_non_alphanumeric(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))

    def test_empty_is_palindrome(self):
        self.assertTrue(is_palindrome(""))

    def test_single_char_is_palindrome(self):
        self.assertTrue(is_palindrome("a"))


class TestCountVowels(unittest.TestCase):
    def test_count_basic(self):
        self.assertEqual(count_vowels("hello"), 2)

    def test_count_no_vowels(self):
        self.assertEqual(count_vowels("rhythm"), 0)

    def test_count_case_insensitive(self):
        self.assertEqual(count_vowels("AEIOU"), 5)

    def test_count_empty(self):
        self.assertEqual(count_vowels(""), 0)

    def test_count_all_vowels(self):
        self.assertEqual(count_vowels("aeiou"), 5)


if __name__ == "__main__":
    unittest.main()

TESTSTRINGS

# --- tests/test_utils.py ---
cat > "$OUTPUT_DIR/tests/test_utils.py" <<'TESTUTILS'
"""Tests for utils module."""

import unittest

from utils import chunk, flatten, is_empty, unique


class TestFlatten(unittest.TestCase):
    def test_flatten_basic(self) -> None:
        self.assertEqual(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])

    def test_flatten_empty(self) -> None:
        self.assertEqual(flatten([]), [])

    def test_flatten_nested_empty(self) -> None:
        self.assertEqual(flatten([[], [1], []]), [1])


class TestChunk(unittest.TestCase):
    def test_chunk_basic(self) -> None:
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])

    def test_chunk_remainder(self) -> None:
        self.assertEqual(chunk([1, 2, 3], 2), [[1, 2], [3]])

    def test_chunk_size_larger(self) -> None:
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])

    def test_chunk_invalid_size(self) -> None:
        with self.assertRaises(ValueError):
            chunk([1, 2, 3], 0)


class TestUnique(unittest.TestCase):
    def test_unique_basic(self) -> None:
        self.assertEqual(unique([1, 2, 2, 3]), [1, 2, 3])

    def test_unique_preserves_order(self) -> None:
        self.assertEqual(unique([3, 1, 2, 1]), [3, 1, 2])

    def test_unique_all_unique(self) -> None:
        self.assertEqual(unique([1, 2, 3]), [1, 2, 3])


class TestIsEmpty(unittest.TestCase):
    def test_is_empty_none(self) -> None:
        self.assertTrue(is_empty(None))

    def test_is_empty_empty_string(self) -> None:
        self.assertTrue(is_empty(""))

    def test_is_empty_empty_list(self) -> None:
        self.assertTrue(is_empty([]))

    def test_is_empty_empty_dict(self) -> None:
        self.assertTrue(is_empty({}))

    def test_is_empty_non_empty(self) -> None:
        self.assertFalse(is_empty("hello"))
        self.assertFalse(is_empty([1]))
        self.assertFalse(is_empty(5))
TESTUTILS

# --- .kilo/command/handover.md ---
cat > "$OUTPUT_DIR/.kilo/command/handover.md" <<'HANDOVER'
---
description: Prepare and post the next task for the following agent
---

Prepare and post the next task for the following agent.

1. Review the current state of the repository.
2. Check the shared Kilo board (`board_read`) for context.
3. Identify what the next agent should work on based on the current repository state and any incomplete tasks.
4. Post a clear, specific task to the board using `board_post` to `main` with type `INFO`.
5. The task should be actionable, focused, and build on work already done or identified gaps.

When you are done, ensure all work results in committed changes (non-workflow files) so the CI checkpoint can verify meaningful project progress.
HANDOVER

# --- .kilo/command/scaffold-project.md ---
cat > "$OUTPUT_DIR/.kilo/command/scaffold-project.md" <<'SCAFFOLD'
---
description: Scaffold a new project structure for agentic coding
---

Generate scaffolding files for a new agentic coding project. This command creates:

- `.github/workflows/main.yml` — CI workflow for the Kilo agent loop
- `AGENTS.md` — AI agent instructions with task handover protocol
- `README.md` — project overview and getting-started guide
- `CHANGELOG.md` — changelog following Keep a Changelog format
- `.pre-commit-config.yaml` — pre-commit hooks for ruff, mypy, tests, and scaffold smoke testing
- `kilo.json` — Kilo project configuration with the `scaffolder` subagent
- `.kilo/agent/scaffolder.md` — subagent definition for scaffolding tasks
- `.kilo/command/handover.md` — handover command for task handoffs
- `.kilo/command/scaffold-project.md` — scaffold-project command documentation
- `.kilo/skill/scaffolding-helper.md` — sample skill definition
- `.kilo/.gitignore` — ignore patterns for the .kilo directory
- `.gitignore` — common ignore patterns
- `Makefile` — common developer targets (test, lint, typecheck, run, scaffold, clean, help, pre-commit-install, pre-commit-run)
- `pyproject.toml` — Python project configuration with pytest, ruff, and mypy settings
- `hello.py` — sample application entry point
- `calculator.py` — simple calculator module with arithmetic operations
- `shapes.py` — geometry utilities for areas and perimeters of common shapes
- `strings.py` — string utilities for text operations
- `tests/test_hello.py` — unit tests for `hello.py`
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `tests/test_strings.py` — unit tests for `strings.py`

## Usage

```bash
scaffold-project <project-name> [output-dir] [--no-test]
```

After scaffolding, `scaffold.sh` runs a smoke test (unittest) in the new project
to verify the generated files work. Pass `--no-test` to skip it.

## Examples

```bash
scaffold-project "My AI Project"
scaffold-project my-cool-tool /tmp/projects/my-tool
scaffold-project my-cool-tool ./out --no-test
```
SCAFFOLD


# --- .kilo/skill/scaffolding-helper.md ---
cat > "$OUTPUT_DIR/.kilo/skill/scaffolding-helper.md" <<'SKILLSAMPLE'
---
name: scaffolding-helper
description: Helps with project scaffolding tasks and maintaining scaffold templates
---

This is a sample skill for the scaffolding system. Skills provide specialized instructions and workflows for specific tasks.

When using this skill:
1. Follow the established project patterns
2. Maintain consistency across scaffolded files
3. Ensure generated code is well-documented
SKILLSAMPLE

# --- .kilo/.gitignore ---
cat > "$OUTPUT_DIR/.kilo/.gitignore" <<'KILOGITIGNORE'
node_modules
package.json
package-lock.json
pnpm-lock.yaml
bun.lock
yarn.lock
.gitignore
agent-manager.json
KILOGITIGNORE

# --- AGENTS.md ---
cat > "$OUTPUT_DIR/AGENTS.md" <<'AGENTS'
# Agent Instructions

Project: ${PROJECT_NAME}

## Project Purpose

${PROJECT_NAME} is an autonomous agentic coding project powered by Kilo. A GitHub Actions workflow runs a loop of Kilo agent sessions, each receiving the task: "Execute the task assigned by the previous agent and prepare a task for the next agent!"

## Task Handover Protocol

1. Check the shared Kilo board (`board_read`) for any messages from the previous agent
2. If a task is found, execute it
3. If no task is found (bootstrap session), establish the project foundation
4. Post a new task for the next agent via `board_post` to `main`
5. Ensure all work results in committed changes (non-workflow files) for the CI checkpoint

## Workflow Rules

- The CI workflow excludes `.github/workflows/**` from the project progress check
- Only changes to files outside `.github/workflows/` count as "meaningful project progress"
- Do NOT modify `.github/workflows/` files — they are maintainer-managed

## Developer Commands

Use the following Makefile targets during development:

- `make test` — Run the Python test suite
- `make lint` — Run ruff code style checker
- `make typecheck` — Run mypy static type checking
- `make run` — Run hello.py (`make run NAME=Alice`)
- `make scaffold` — Scaffold a new project using scaffold.sh
- `make pre-commit-install` — Install pre-commit hooks into .git/hooks
- `make pre-commit-run` — Run all pre-commit hooks against tracked files
- `make clean` — Remove build artifacts
- `make help` — Show all available targets

## Agent Configuration

- Project config: `kilo.json` at the repository root
- Custom subagents: `.kilo/agent/*.md`
- Custom commands: `.kilo/command/*.md`
- Kilo permissions: `permission` key in `kilo.json`

## Available Subagents

- `scaffolder` - A subagent for generating project scaffolding and templates
- `explore` (built-in) - Read-only codebase exploration

## Available Commands

- `scaffold-project` - Scaffold a new project structure
- `handover` - Prepare and post the next task for the following agent

## Coding Conventions

- Write clean, well-documented code
- Follow existing file patterns in the repository
- Use descriptive file and function names
- Keep changes focused and incremental

## Notes

- This project uses the `kilo/kilo-auto/free` model
- Sessions have an idle timeout of 900 seconds
- The overall CI job has a 355-minute safety cutoff
AGENTS

# --- README.md ---
cat > "$OUTPUT_DIR/README.md" <<README
# ${PROJECT_NAME}

A project scaffolded for autonomous agentic coding with Kilo.

## Overview

This repository provides a foundation for autonomous agent development. A GitHub Actions workflow runs a loop of Kilo agent sessions that iteratively build and refine the project.

## How It Works

Each agent session runs with the prompt "Execute the task assigned by the previous agent and prepare a task for the next agent!" — creating a continuous, evolving codebase.

## Project Structure

\`\`\`
.github/workflows/main.yml   # CI workflow: Kilo agent loop
.kilo/                       # Kilo project configuration
  agent/                     # Custom subagents
  command/                   # Custom commands
  skill/                     # Custom skills
  .gitignore                 # Ignore patterns for .kilo directory
AGENTS.md                    # AI agent instructions
README.md                    # Project overview and getting started guide
CHANGELOG.md                 # Changelog (Keep a Changelog format)
.pre-commit-config.yaml      # Pre-commit hooks (ruff, mypy, tests, scaffold)
kilo.json                    # Kilo project configuration
Makefile                     # Common developer targets (test, lint, typecheck, run, scaffold, clean, help, pre-commit-install, pre-commit-run)
pyproject.toml               # Python project configuration (pytest, ruff, mypy)
hello.py                     # Sample application entry point
calculator.py                # Simple calculator module with arithmetic operations
shapes.py                    # Geometry utilities for areas and perimeters of common shapes
strings.py                   # String utilities for text operations
utils.py                     # General utility helper functions
.gitignore                   # Common ignore patterns
tests/                       # Python unit tests
  test_hello.py              # Tests for hello.py
  test_calculator.py         # Tests for calculator.py
  test_scaffold.py           # Tests for scaffold.sh
  test_shapes.py             # Tests for shapes.py
  test_strings.py            # Tests for strings.py
  test_utils.py              # Tests for utils.py
\`\`\`

## Developer Commands

This project includes a \`Makefile\` with the following targets:

| Target    | Description                              |
|-----------|------------------------------------------|
| \`make test\`             | Run the Python test suite with pytest    |
| \`make lint\`             | Run ruff code style checker              |
| \`make typecheck\`        | Run mypy static type checking            |
| \`make run\`              | Run hello.py (\`make run NAME=Alice\`)      |
| \`make scaffold\`         | Run scaffold.sh to scaffold a new project |
| \`make clean\`            | Remove build artifacts                    |
| \`make help\`             | Show all available targets                |
| \`make pre-commit-install\` | Install pre-commit hooks               |
| \`make pre-commit-run\`   | Run all pre-commit hooks                  |

## Getting Started

\`\`\`bash
# Run the sample application
make run

# Run tests
make test

# Check code style and types
make lint
make typecheck
\`\`\`

## License

MIT
README

# --- CHANGELOG.md ---
cat > "$OUTPUT_DIR/CHANGELOG.md" <<'CHANGELOG'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial scaffold generated by scaffold.sh

## [0.1.0] - Bootstrap

### Added

- \`hello.py\` — sample application entry point
- \`tests/test_hello.py\` — unit tests for \`hello.py\`
- \`scaffold.sh\` — project scaffolding script
- \`AGENTS.md\` — agent instructions with task handover protocol
- \`kilo.json\` — Kilo project configuration
- \`Makefile\` — developer targets
- \`pyproject.toml\` — Python project configuration
- \`.gitignore\` — common ignore patterns
- \`.kilo/agent/scaffolder.md\` — scaffolder subagent
- \`.kilo/command/handover.md\` — handover command
- \`.kilo/command/scaffold-project.md\` — scaffold-project command
- \`.kilo/skill/scaffolding-helper.md\` — sample skill
- \`.kilo/.gitignore\` — ignore patterns for the .kilo directory
- \`.github/workflows/main.yml\` — CI workflow for Kilo agent loop
- \`README.md\` — project overview
- \`CHANGELOG.md\` — changelog following Keep a Changelog format
- \`.pre-commit-config.yaml\` — pre-commit hooks for ruff, mypy, tests, and scaffold
- `calculator.py` — simple calculator module with arithmetic operations
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `shapes.py` — geometry utilities for areas and perimeters of common shapes
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `strings.py` — string utilities for text operations
- `tests/test_strings.py` — unit tests for `strings.py`
- `utils.py` — general utility helper functions
- `tests/test_utils.py` — unit tests for `utils.py`
- `utils.py` — general utility helper functions
- `tests/test_utils.py` — unit tests for `utils.py`
- `utils.py` — general utility helper functions
- `tests/test_utils.py` — unit tests for `utils.py`
CHANGELOG

# --- kilo.json ---
cat > "$OUTPUT_DIR/kilo.json" <<'KILOJSON'
{
  "$schema": "https://app.kilo.ai/config.json",
  "permission": "allow",
  "agent": {
    "scaffolder": {
      "description": "Generates project scaffolding, templates, and boilerplate code for new features. Use when the task involves creating new files or project structure.",
      "mode": "subagent",
      "model": "kilo/kilo-auto/free"
    }
  }
}
KILOJSON

# --- .kilo/agent/scaffolder.md ---
cat > "$OUTPUT_DIR/.kilo/agent/scaffolder.md" <<'AGENT'
---
description: Generates project scaffolding, templates, and boilerplate code
mode: subagent
model: kilo/kilo-auto/free
---

You are a scaffolding specialist subagent. Your purpose is to generate project scaffolding, templates, and boilerplate code.

When invoked:

1. Analyze the requested scaffolding need (new project template, CI workflow, documentation structure, agent configuration, etc.)
2. Generate clean, well-structured files following existing patterns in the repository
3. Create a README or notes file explaining what was scaffolded and how to use it
4. Follow the coding conventions defined in AGENTS.md

Always match the existing file patterns, naming conventions, and documentation style already established in the repository.
AGENT

echo ""
echo "Scaffolded project '$PROJECT_NAME' at: $OUTPUT_DIR"
echo ""
echo "Created files:"
find "$OUTPUT_DIR" -type f | sort | sed "s/^/  /"
echo ""

if [[ "$SMOKE_TEST" == "1" ]] && command -v python >/dev/null 2>&1; then
  echo "Running smoke test in $OUTPUT_DIR ..."
  if (cd "$OUTPUT_DIR" && python -m unittest discover tests/ -v); then
    echo "Smoke test passed."
  else
    echo "Warning: smoke test failed. The scaffold may be incomplete." >&2
  fi
else
  echo "Smoke test skipped (pass --no-test to skip intentionally)."
fi

echo ""
echo "Next steps:"
echo "  cd $OUTPUT_DIR"
echo "  git init"
echo "  git add -A"
echo "  git commit -m \"Initial commit\""
