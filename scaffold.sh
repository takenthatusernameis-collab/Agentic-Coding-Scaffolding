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
#   - LICENSE — MIT license file
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
#   - stats.py statistical utility functions
#   - tests/test_stats.py unit tests for the stats module
#   - datetime_utils.py date and time utility functions
#   - tests/test_datetime_utils.py unit tests for the datetime_utils module
#   - math_utils.py mathematical utility functions
#   - tests/test_math_utils.py unit tests for the math_utils module
#   - data_utils.py data utility functions
#   - tests/test_data_utils.py unit tests for the data_utils module
#   - file_utils.py file and path utility functions
#   - tests/test_file_utils.py unit tests for the file_utils module
#   - url_utils.py URL and web utility functions
#   - tests/test_url_utils.py unit tests for the url_utils module
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

# Default project metadata for generated files
PROJECT_YEARS="${PROJECT_YEARS:-$(date +%Y)}"
PROJECT_AUTHOR="${PROJECT_AUTHOR:-kilo-autonomous}"

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

# --- stats.py ---
cat > "$OUTPUT_DIR/stats.py" <<'STATS'
"""Statistical utility functions for data analysis."""

from typing import List, TypeVar

T = TypeVar("T", int, float)


def mean(numbers: List[T | float]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The average of all numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)


def median(numbers: List[T | float]) -> float:
    """Return the median of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The median value.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 1:
        return float(sorted_nums[n // 2])
    mid1 = sorted_nums[n // 2 - 1]
    mid2 = sorted_nums[n // 2]
    return (mid1 + mid2) / 2.0


def mode(numbers: List[T | float]) -> T | float:
    """Return the mode (most frequent value) of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The most frequently occurring value.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")
    frequency: dict = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_count = max(frequency.values())
    for num in sorted(frequency.keys()):
        if frequency[num] == max_count:
            return num


def variance(numbers: List[T | float], population: bool = True) -> float:
    """Return the variance of a list of numbers.

    Args:
        numbers: A list of numeric values.
        population: If True, calculate population variance (divide by n).
                    If False, calculate sample variance (divide by n-1).

    Returns:
        The variance.

    Raises:
        ValueError: If the list is empty or insufficient elements for sample.
    """
    if not numbers:
        raise ValueError("Cannot calculate variance of empty list")
    if not population and len(numbers) < 2:
        raise ValueError("Cannot calculate sample variance with fewer than 2 elements")
    avg = mean(numbers)
    squared_diff = sum((x - avg) ** 2 for x in numbers)
    if population:
        return squared_diff / len(numbers)
    return squared_diff / (len(numbers) - 1)


def stddev(numbers: List[T | float], population: bool = True) -> float:
    """Return the standard deviation of a list of numbers.

    Args:
        numbers: A list of numeric values.
        population: If True, calculate population std dev (divide by n).
                    If False, calculate sample std dev (divide by n-1).

    Returns:
        The standard deviation.

    Raises:
        ValueError: If the list is empty or insufficient elements for sample.
    """
    import math

    var = variance(numbers, population=population)
    return math.sqrt(var)
STATS

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

# --- tests/test_stats.py ---
cat > "$OUTPUT_DIR/tests/test_stats.py" <<'TESTSTATS'
"""Tests for stats module."""

import unittest

from stats import mean, median, mode, stddev, variance


class TestMean(unittest.TestCase):
    def test_mean_basic(self) -> None:
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)

    def test_mean_even(self) -> None:
        self.assertEqual(mean([1, 3]), 2.0)

    def test_mean_single(self) -> None:
        self.assertEqual(mean([5]), 5.0)

    def test_mean_negative(self) -> None:
        self.assertEqual(mean([-1, 0, 1]), 0.0)

    def test_mean_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            mean([])


class TestMedian(unittest.TestCase):
    def test_median_odd(self) -> None:
        self.assertEqual(median([1, 2, 3, 4, 5]), 3.0)

    def test_median_even(self) -> None:
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_median_single(self) -> None:
        self.assertEqual(median([5]), 5.0)

    def test_median_unsorted(self) -> None:
        self.assertEqual(median([5, 1, 3]), 3.0)

    def test_median_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            median([])


class TestMode(unittest.TestCase):
    def test_mode_basic(self) -> None:
        self.assertEqual(mode([1, 2, 2, 3, 4]), 2)

    def test_mode_all_same(self) -> None:
        self.assertEqual(mode([7, 7, 7]), 7)

    def test_mode_bimodal_returns_first_in_sorted_order(self) -> None:
        self.assertEqual(mode([1, 1, 2, 2]), 1)

    def test_mode_single(self) -> None:
        self.assertEqual(mode([5]), 5)

    def test_mode_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            mode([])


class TestVariance(unittest.TestCase):
    def test_variance_population_basic(self) -> None:
        result = variance([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result, 2.0, places=5)

    def test_variance_population_single(self) -> None:
        self.assertAlmostEqual(variance([5]), 0.0, places=5)

    def test_variance_sample(self) -> None:
        result = variance([1, 2, 3, 4, 5], population=False)
        self.assertAlmostEqual(result, 2.5, places=5)

    def test_variance_sample_requires_two_elements(self) -> None:
        with self.assertRaises(ValueError):
            variance([5], population=False)

    def test_variance_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            variance([])


class TestStddev(unittest.TestCase):
    def test_stddev_population_basic(self) -> None:
        result = stddev([1, 2, 3, 4, 5])
        self.assertAlmostEqual(result, 1.4142135623730951, places=5)

    def test_stddev_population_single(self) -> None:
        self.assertAlmostEqual(stddev([5]), 0.0, places=5)

    def test_stddev_sample(self) -> None:
        result = stddev([1, 2, 3, 4, 5], population=False)
        self.assertAlmostEqual(result, 1.5811388300841898, places=5)

    def test_stddev_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            stddev([])


if __name__ == "__main__":
    unittest.main()
TESTSTATS

# --- math_utils.py ---
cat > "$OUTPUT_DIR/math_utils.py" <<'MATH'
"""Mathematical utility functions."""

import math


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n > 20:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    return math.factorial(n)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor of two integers."""
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """Calculate the Least Common Multiple of two integers."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        raise ValueError("Prime check is only defined for integers >= 2")
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min_val and max_val."""
    if min_val > max_val:
        raise ValueError("min_val must be <= max_val")
    return max(min_val, min(value, max_val))
MATH

# --- data_utils.py ---
cat > "$OUTPUT_DIR/data_utils.py" <<'DATA'
"""Data utility functions."""

import copy
from typing import Any, Dict, Iterable, List, Set, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def deep_copy(obj: Any) -> Any:
    """Create a deep copy of an object."""
    try:
        return copy.deepcopy(obj)
    except Exception:
        return copy.copy(obj)


def merge_dicts(*dicts: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merge multiple dictionaries, later values override earlier ones."""
    result: Dict[Any, Any] = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def pick(d: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    """Return a new dict with only specified keys."""
    key_set: Set[K] = set(keys)
    return {k: d[k] for k in d if k in key_set}


def omit(d: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    """Return a new dict without specified keys."""
    key_set: Set[K] = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "."
) -> Dict[str, Any]:
    """Flatten nested dict to dot-notation keys."""
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
DATA

# --- datetime_utils.py ---
cat > "$OUTPUT_DIR/datetime_utils.py" <<'DATETIME'
"""Date and time utility functions."""

from datetime import datetime, timedelta
from typing import Union

DateTimeLike = Union[str, datetime]


def parse_datetime(value: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse a string into a datetime object.

    Args:
        value: The string to parse.
        fmt: The expected format string. Defaults to %Y-%m-%d %H:%M:%S.

    Returns:
        The parsed datetime object.

    Raises:
        ValueError: If the string does not match the format.
    """
    return datetime.strptime(value, fmt)


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string.

    Args:
        dt: The datetime to format.
        fmt: The desired format string. Defaults to %Y-%m-%d %H:%M:%S.

    Returns:
        The formatted string.
    """
    return dt.strftime(fmt)


def days_between(start: DateTimeLike, end: DateTimeLike) -> int:
    """Return the absolute number of whole days between two dates.

    Args:
        start: A datetime or parseable string (format %Y-%m-%d).
        end: A datetime or parseable string (format %Y-%m-%d).

    Returns:
        The absolute difference in days.

    Raises:
        ValueError: If a string argument cannot be parsed.
    """
    start_dt = _coerce_datetime(start, "%Y-%m-%d")
    end_dt = _coerce_datetime(end, "%Y-%m-%d")
    delta = end_dt - start_dt
    return abs(delta.days)


def is_leap_year(year: int) -> bool:
    """Return True if year is a leap year.

    Args:
        year: The year to check.

    Returns:
        True if the year is a leap year, False otherwise.

    Raises:
        ValueError: If year is less than 1.
    """
    if year < 1:
        raise ValueError("Year must be a positive integer.")
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def add_days(dt: DateTimeLike, days: int) -> datetime:
    """Add (or subtract, if negative) a number of days to a datetime.

    Args:
        dt: A datetime or a string parseable with %Y-%m-%d or %Y-%m-%d %H:%M:%S.
        days: The number of days to add. May be negative.

    Returns:
        A new datetime shifted by the given number of days.

    Raises:
        ValueError: If a string argument cannot be parsed.
    """
    dt_val = _coerce_datetime(dt, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S")
    return dt_val + timedelta(days=days)


def get_weekday_name(dt: DateTimeLike) -> str:
    """Return the full weekday name for a given date.

    Args:
        dt: A datetime or a string parseable with %Y-%m-%d.

    Returns:
        The weekday name (e.g. Monday).

    Raises:
        ValueError: If a string argument cannot be parsed.
    """
    dt_val = _coerce_datetime(dt, "%Y-%m-%d")
    return dt_val.strftime("%A")


def _coerce_datetime(value: DateTimeLike, *formats: str) -> datetime:
    """Coerce a value into a datetime, trying multiple formats if needed.

    Args:
        value: A datetime (returned as-is) or a string to parse.
        *formats: Format strings to try when parsing.

    Returns:
        The resulting datetime.

    Raises:
        ValueError: If value is a string that matches none of the formats.
    """
    if isinstance(value, datetime):
        return value
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(
        f"Could not parse '{value}'. Expected formats: {list(formats)}"
    )
DATETIME
# --- tests/test_math_utils.py ---
cat > "$OUTPUT_DIR/tests/test_math_utils.py" <<'TESTMATH'
"""Tests for math_utils module."""

import unittest

from math_utils import clamp, factorial, fibonacci, gcd, is_prime, lcm


class TestFactorial(unittest.TestCase):
    def test_factorial_zero(self) -> None:
        self.assertEqual(factorial(0), 1)

    def test_factorial_positive(self) -> None:
        self.assertEqual(factorial(5), 120)

    def test_factorial_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            factorial(-1)


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_zero(self) -> None:
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_one(self) -> None:
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_sequence(self) -> None:
        self.assertEqual(fibonacci(5), 5)

    def test_fibonacci_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            fibonacci(-1)


class TestGCD(unittest.TestCase):
    def test_gcd_basic(self) -> None:
        self.assertEqual(gcd(48, 18), 6)


class TestLCM(unittest.TestCase):
    def test_lcm_basic(self) -> None:
        self.assertEqual(lcm(4, 6), 12)


class TestIsPrime(unittest.TestCase):
    def test_prime_numbers(self) -> None:
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))

    def test_non_prime_numbers(self) -> None:
        self.assertFalse(is_prime(4))

    def test_prime_edge_cases(self) -> None:
        self.assertRaises(ValueError, is_prime, 1)


class TestClamp(unittest.TestCase):
    def test_clamp_inside_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_below_range(self) -> None:
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_clamp_above_range(self) -> None:
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_clamp_invalid_range(self) -> None:
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


if __name__ == "__main__":
    unittest.main()
TESTMATH

# --- tests/test_data_utils.py ---
cat > "$OUTPUT_DIR/tests/test_data_utils.py" <<'TESTDATA'
"""Tests for data_utils module."""

import unittest

from data_utils import deep_copy, flatten_dict, merge_dicts, omit, pick


class TestDeepCopy(unittest.TestCase):
    def test_deep_copy_simple_dict(self) -> None:
        original = {"a": 1, "b": 2}
        copied = deep_copy(original)
        self.assertEqual(original, copied)
        self.assertIsNot(original, copied)

    def test_deep_copy_nested(self) -> None:
        original = {"a": 1, "b": {"c": 3, "d": 4}}
        copied = deep_copy(original)
        self.assertEqual(original, copied)
        self.assertIsNot(original["b"], copied["b"])
        copied["b"]["c"] = 99
        self.assertEqual(original["b"]["c"], 3)

    def test_deep_copy_list(self) -> None:
        original = [1, 2, [3, 4]]
        copied = deep_copy(original)
        self.assertEqual(original, copied)
        self.assertIsNot(original, copied)
        self.assertIsNot(original[2], copied[2])

    def test_deep_copy_primitive(self) -> None:
        self.assertEqual(deep_copy(5), 5)
        self.assertEqual(deep_copy("hello"), "hello")


class TestMergeDicts(unittest.TestCase):
    def test_merge_dicts_basic(self) -> None:
        result = merge_dicts({"a": 1}, {"b": 2})
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_merge_dicts_override(self) -> None:
        result = merge_dicts({"a": 1}, {"a": 3, "b": 2})
        self.assertEqual(result, {"a": 3, "b": 2})

    def test_merge_dicts_multiple(self) -> None:
        result = merge_dicts({"a": 1}, {"b": 2}, {"c": 3, "a": 4})
        self.assertEqual(result, {"a": 4, "b": 2, "c": 3})

    def test_merge_dicts_empty(self) -> None:
        self.assertEqual(merge_dicts(), {})
        self.assertEqual(merge_dicts({}, {"a": 1}), {"a": 1})


class TestPick(unittest.TestCase):
    def test_pick_basic(self) -> None:
        result = pick({"a": 1, "b": 2, "c": 3}, ["a", "c"])
        self.assertEqual(result, {"a": 1, "c": 3})

    def test_pick_missing_keys(self) -> None:
        result = pick({"a": 1, "b": 2}, ["a", "d"])
        self.assertEqual(result, {"a": 1})

    def test_pick_empty_keys(self) -> None:
        result = pick({"a": 1, "b": 2}, [])
        self.assertEqual(result, {})

    def test_pick_no_overlap(self) -> None:
        result = pick({"a": 1}, ["b", "c"])
        self.assertEqual(result, {})


class TestOmit(unittest.TestCase):
    def test_omit_basic(self) -> None:
        result = omit({"a": 1, "b": 2, "c": 3}, ["a", "c"])
        self.assertEqual(result, {"b": 2})

    def test_omit_missing_keys(self) -> None:
        result = omit({"a": 1, "b": 2}, ["c", "d"])
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_omit_empty_keys(self) -> None:
        result = omit({"a": 1, "b": 2}, [])
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_omit_all(self) -> None:
        result = omit({"a": 1, "b": 2}, ["a", "b"])
        self.assertEqual(result, {})


class TestFlattenDict(unittest.TestCase):
    def test_flatten_dict_simple(self) -> None:
        d = {"a": 1, "b": 2}
        result = flatten_dict(d)
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_flatten_dict_nested(self) -> None:
        d = {"a": 1, "b": {"c": 2, "d": 3}}
        result = flatten_dict(d)
        self.assertEqual(result, {"a": 1, "b.c": 2, "b.d": 3})

    def test_flatten_dict_deep_nested(self) -> None:
        d = {"a": {"b": {"c": {"d": 1}}}}
        result = flatten_dict(d)
        self.assertEqual(result, {"a.b.c.d": 1})

    def test_flatten_dict_custom_sep(self) -> None:
        d = {"a": {"b": 2}}
        result = flatten_dict(d, sep="_")
        self.assertEqual(result, {"a_b": 2})

    def test_flatten_dict_mixed(self) -> None:
        d = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
        result = flatten_dict(d)
        self.assertEqual(result, {"a": 1, "b.c": 2, "d.e.f": 3})


if __name__ == "__main__":
    unittest.main()
TESTDATA

# --- tests/test_datetime_utils.py ---
cat > "$OUTPUT_DIR/tests/test_datetime_utils.py" <<'TESTDATETIME'
"""Tests for datetime_utils module."""

import unittest
from datetime import datetime

from datetime_utils import (
    add_days,
    days_between,
    format_datetime,
    get_weekday_name,
    is_leap_year,
    parse_datetime,
)


class TestParseDatetime(unittest.TestCase):
    def test_parse_default_format(self) -> None:
        result = parse_datetime("2024-03-15 10:30:00")
        self.assertEqual(result, datetime(2024, 3, 15, 10, 30, 0))

    def test_parse_custom_format(self) -> None:
        result = parse_datetime("15/03/2024", "%d/%m/%Y")
        self.assertEqual(result, datetime(2024, 3, 15))

    def test_parse_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_datetime("not-a-date")


class TestFormatDatetime(unittest.TestCase):
    def test_format_default(self) -> None:
        dt = datetime(2024, 3, 15, 10, 30, 0)
        self.assertEqual(format_datetime(dt), "2024-03-15 10:30:00")

    def test_format_custom(self) -> None:
        dt = datetime(2024, 3, 15, 10, 30, 0)
        self.assertEqual(format_datetime(dt, "%Y-%m-%d"), "2024-03-15")

    def test_format_iso(self) -> None:
        dt = datetime(2024, 3, 15, 10, 30, 0)
        self.assertEqual(format_datetime(dt, "%Y%m%dT%H%M%S"), "20240315T103000")


class TestDaysBetween(unittest.TestCase):
    def test_days_between_basic(self) -> None:
        self.assertEqual(days_between("2024-01-01", "2024-01-10"), 9)

    def test_days_between_negative(self) -> None:
        self.assertEqual(days_between("2024-01-10", "2024-01-01"), 9)

    def test_days_between_same_day(self) -> None:
        self.assertEqual(days_between("2024-01-01", "2024-01-01"), 0)

    def test_days_between_different_months(self) -> None:
        self.assertEqual(days_between("2024-02-01", "2024-03-01"), 29)

    def test_days_between_with_datetime_objects(self) -> None:
        d1 = datetime(2024, 1, 1)
        d2 = datetime(2024, 1, 10)
        self.assertEqual(days_between(d1, d2), 9)

    def test_days_between_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            days_between("not-a-date", "2024-01-01")


class TestIsLeapYear(unittest.TestCase):
    def test_leap_year_divisible_by_4(self) -> None:
        self.assertTrue(is_leap_year(2024))
        self.assertTrue(is_leap_year(2020))

    def test_leap_year_divisible_by_100_not_400(self) -> None:
        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(2100))

    def test_leap_year_divisible_by_400(self) -> None:
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2400))

    def test_non_leap_year(self) -> None:
        self.assertFalse(is_leap_year(2023))
        self.assertFalse(is_leap_year(2025))

    def test_invalid_year_raises(self) -> None:
        with self.assertRaises(ValueError):
            is_leap_year(0)
        with self.assertRaises(ValueError):
            is_leap_year(-1)


class TestAddDays(unittest.TestCase):
    def test_add_positive_days(self) -> None:
        result = add_days("2024-01-01", 10)
        self.assertEqual(result, datetime(2024, 1, 11))

    def test_add_negative_days(self) -> None:
        result = add_days("2024-01-10", -5)
        self.assertEqual(result, datetime(2024, 1, 5))

    def test_add_zero_days(self) -> None:
        result = add_days("2024-01-01", 0)
        self.assertEqual(result, datetime(2024, 1, 1))

    def test_add_with_datetime_object(self) -> None:
        dt = datetime(2024, 1, 1, 12, 0, 0)
        result = add_days(dt, 15)
        self.assertEqual(result, datetime(2024, 1, 16, 12, 0, 0))

    def test_add_crosses_month_boundary(self) -> None:
        result = add_days("2024-01-25", 10)
        self.assertEqual(result, datetime(2024, 2, 4))

    def test_add_crosses_year_boundary(self) -> None:
        result = add_days("2024-12-25", 10)
        self.assertEqual(result, datetime(2025, 1, 4))

    def test_add_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            add_days("not-a-date", 5)


class TestGetWeekdayName(unittest.TestCase):
    def test_weekday_name_monday(self) -> None:
        result = get_weekday_name("2024-03-11")
        self.assertEqual(result, "Monday")

    def test_weekday_name_friday(self) -> None:
        result = get_weekday_name("2024-03-15")
        self.assertEqual(result, "Friday")

    def test_weekday_name_with_datetime_object(self) -> None:
        dt = datetime(2024, 3, 15)
        result = get_weekday_name(dt)
        self.assertEqual(result, "Friday")

    def test_weekday_name_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            get_weekday_name("not-a-date")


if __name__ == "__main__":
    unittest.main()
TESTDATETIME

# --- file_utils.py ---
cat > "$OUTPUT_DIR/file_utils.py" <<'FILEUTILS'
"""File and path utility functions."""

import shutil
from pathlib import Path
from typing import Any, List, Optional, Union


def read_text(path: Union[str, Path]) -> str:
    """Read text content from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
    """Write text content to a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def read_json(path: Union[str, Path]) -> Any:
    """Read JSON content from a file."""
    import json

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(
    path: Union[str, Path],
    data: Any,
    indent: Optional[int] = 2,
    ensure_ascii: bool = False,
) -> None:
    """Write JSON content to a file."""
    import json

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure a directory exists and return its Path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(
    path: Union[str, Path],
    pattern: Optional[str] = None,
    recursive: bool = False,
) -> List[Path]:
    """List files in a directory."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")

    if recursive:
        if pattern:
            return sorted(path.rglob(pattern))
        return sorted([p for p in path.rglob("*") if p.is_file()])
    else:
        if pattern:
            return sorted(path.glob(pattern))
        return sorted([p for p in path.iterdir() if p.is_file()])


def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """Copy a file from src to dst."""
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def delete_file(path: Union[str, Path]) -> None:
    """Delete a file if it exists."""
    path = Path(path)
    if path.exists() and path.is_file():
        path.unlink()
FILEUTILS
# --- tests/test_file_utils.py ---
cat > "$OUTPUT_DIR/tests/test_file_utils.py" <<'TESTFILEUTILS'
"""Tests for file_utils module."""

import tempfile
import unittest
from pathlib import Path

from file_utils import (
    copy_file,
    delete_file,
    ensure_dir,
    list_files,
    read_json,
    read_text,
    write_json,
    write_text,
)


class TestFileUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_read_write_text(self) -> None:
        file_path = Path(self.temp_dir) / "test.txt"
        content = "Hello, World!"
        write_text(file_path, content)
        self.assertTrue(file_path.exists())
        self.assertEqual(read_text(file_path), content)

    def test_read_write_json(self) -> None:
        file_path = Path(self.temp_dir) / "test.json"
        data = {"name": "test", "value": 42}
        write_json(file_path, data)
        self.assertTrue(file_path.exists())
        result = read_json(file_path)
        self.assertEqual(result, data)

    def test_ensure_dir(self) -> None:
        dir_path = Path(self.temp_dir) / "nested" / "dir"
        result = ensure_dir(dir_path)
        self.assertTrue(dir_path.exists())
        self.assertTrue(dir_path.is_dir())
        self.assertEqual(result, dir_path)

    def test_list_files(self) -> None:
        temp_path = Path(self.temp_dir)
        (temp_path / "file1.txt").write_text("1")
        (temp_path / "file2.py").write_text("2")
        (temp_path / "subdir").mkdir()
        (temp_path / "subdir" / "file3.txt").write_text("3")

        files = list_files(temp_path)
        self.assertEqual(len(files), 2)

        txt_files = list_files(temp_path, pattern="*.txt")
        self.assertEqual(len(txt_files), 1)

        all_files = list_files(temp_path, recursive=True)
        self.assertEqual(len(all_files), 3)

    def test_copy_file(self) -> None:
        src = Path(self.temp_dir) / "src.txt"
        dst = Path(self.temp_dir) / "copy" / "dst.txt"
        src.write_text("hello")
        copy_file(src, dst)
        self.assertTrue(dst.exists())
        self.assertEqual(dst.read_text(), "hello")

    def test_delete_file(self) -> None:
        file_path = Path(self.temp_dir) / "to_delete.txt"
        file_path.write_text("delete me")
        self.assertTrue(file_path.exists())
        delete_file(file_path)
        self.assertFalse(file_path.exists())
        delete_file(file_path)


if __name__ == "__main__":
    unittest.main()
TESTFILEUTILS
# --- url_utils.py ---
cat > "$OUTPUT_DIR/url_utils.py" <<'URLUTILS'
"""URL and web utility functions."""

from typing import Dict, List, Optional, Union
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def is_valid_url(url: str, schemes: Optional[List[str]] = None) -> bool:
    """Validate a URL string.

    Args:
        url: The URL string to validate.
        schemes: Optional list of allowed schemes (e.g. ``['http', 'https']``).
            If ``None``, any non-empty scheme is accepted.

    Returns:
        ``True`` if the URL is valid and uses an allowed scheme, ``False`` otherwise.
    """
    try:
        parsed = urlparse(url)
    except (ValueError, TypeError):
        return False
    if not parsed.scheme:
        return False
    if not parsed.netloc:
        return False
    if schemes is not None and parsed.scheme not in schemes:
        return False
    return True


def extract_domain(url: str) -> str:
    """Extract the hostname from a URL.

    Args:
        url: The URL string to extract the domain from.

    Returns:
        The hostname portion of the URL.

    Raises:
        ValueError: If the URL has no valid hostname.
    """
    parsed = urlparse(url)
    if not parsed.hostname:
        raise ValueError(f"URL has no valid domain: {url}")
    return parsed.hostname


def get_query_params(url: str) -> Dict[str, str]:
    """Get all query parameters from a URL as a flat dict.

    When a parameter appears multiple times, the first value is used.

    Args:
        url: The URL string to parse.

    Returns:
        A dict mapping query parameter names to their first value.
    """
    parsed = urlparse(url)
    params: Dict[str, str] = {}
    query_dict = parse_qs(parsed.query, keep_blank_values=True)
    for key, values in query_dict.items():
        params[key] = values[0]
    return params


def get_query_param(url: str, key: str) -> Optional[str]:
    """Get a single query parameter value from a URL.

    Args:
        url: The URL string to parse.
        key: The query parameter name to look up.

    Returns:
        The first value for the given key, or ``None`` if the key is absent.
    """
    params = get_query_params(url)
    return params.get(key)


def add_query_param(url: str, key: str, value: Union[str, int, float]) -> str:
    """Add or update a query parameter in a URL.

    Args:
        url: The URL string to modify.
        key: The query parameter name.
        value: The query parameter value (converted to string).

    Returns:
        The updated URL with the query parameter set.
    """
    parsed = urlparse(url)
    params = get_query_params(url)
    params[key] = str(value)
    new_query = urlencode(params)
    return urlunparse(parsed._replace(query=new_query))


def remove_query_param(url: str, key: str) -> str:
    """Remove a query parameter from a URL.

    If the parameter does not exist, the URL is returned unchanged.

    Args:
        url: The URL string to modify.
        key: The query parameter name to remove.

    Returns:
        The URL with the specified query parameter removed.
    """
    parsed = urlparse(url)
    params = get_query_params(url)
    params.pop(key, None)
    new_query = urlencode(params) if params else ""
    return urlunparse(parsed._replace(query=new_query))


def build_url(
    scheme: str = "https",
    domain: str = "",
    path: str = "",
    port: Optional[int] = None,
    params: Optional[Dict[str, Union[str, int, float]]] = None,
) -> str:
    """Build a URL from its individual components.

    Args:
        scheme: URL scheme (e.g. ``'http'``, ``'https'``).
        domain: The domain or host name.
        path: Path component (should start with ``'/'``).
        port: Optional port number appended to the domain.
        params: Optional query parameters dict.

    Returns:
        The constructed URL string.

    Raises:
        ValueError: If ``domain`` is empty.
    """
    if not domain:
        raise ValueError("domain is required")
    netloc = domain
    if port is not None:
        netloc = f"{domain}:{port}"
    query = ""
    if params:
        query = urlencode(params)
    return urlunparse((scheme, netloc, path, "", query, ""))
URLUTILS
# --- tests/test_url_utils.py ---
cat > "$OUTPUT_DIR/tests/test_url_utils.py" <<'TESTURLUTILS'
"""Tests for url_utils module."""

import unittest

from url_utils import (
    add_query_param,
    build_url,
    extract_domain,
    get_query_param,
    get_query_params,
    is_valid_url,
    remove_query_param,
)


class TestIsValidUrl(unittest.TestCase):
    def test_valid_http(self) -> None:
        self.assertTrue(is_valid_url("http://example.com"))

    def test_valid_https(self) -> None:
        self.assertTrue(is_valid_url("https://example.com/path"))

    def test_valid_with_port(self) -> None:
        self.assertTrue(is_valid_url("http://example.com:8080"))

    def test_missing_scheme(self) -> None:
        self.assertFalse(is_valid_url("example.com/path"))

    def test_missing_domain(self) -> None:
        self.assertFalse(is_valid_url("http://"))

    def test_empty_string(self) -> None:
        self.assertFalse(is_valid_url(""))

    def test_scheme_restriction_allowed(self) -> None:
        self.assertTrue(is_valid_url("https://example.com", schemes=["https"]))

    def test_scheme_restriction_not_allowed(self) -> None:
        self.assertFalse(is_valid_url("http://example.com", schemes=["https"]))

    def test_ftp_scheme(self) -> None:
        self.assertTrue(is_valid_url("ftp://example.com"))


class TestExtractDomain(unittest.TestCase):
    def test_extract_domain_basic(self) -> None:
        self.assertEqual(extract_domain("https://example.com/path"), "example.com")

    def test_extract_domain_with_subdomain(self) -> None:
        self.assertEqual(extract_domain("https://api.sub.example.com"), "api.sub.example.com")

    def test_extract_domain_with_port(self) -> None:
        self.assertEqual(extract_domain("http://example.com:8080"), "example.com")

    def test_extract_domain_no_hostname(self) -> None:
        with self.assertRaises(ValueError):
            extract_domain("not-a-url")


class TestGetQueryParams(unittest.TestCase):
    def test_get_params_basic(self) -> None:
        params = get_query_params("https://example.com?name=alice&age=30")
        self.assertEqual(params, {"name": "alice", "age": "30"})

    def test_get_params_empty(self) -> None:
        self.assertEqual(get_query_params("https://example.com"), {})

    def test_get_params_blank_values(self) -> None:
        params = get_query_params("https://example.com?empty=&full=yes")
        self.assertEqual(params, {"empty": "", "full": "yes"})

    def test_get_params_duplicate_uses_first(self) -> None:
        params = get_query_params("https://example.com?color=red&color=blue")
        self.assertEqual(params["color"], "red")


class TestGetQueryParam(unittest.TestCase):
    def test_get_param_exists(self) -> None:
        self.assertEqual(
            get_query_param("https://example.com?q=test&page=2", "q"), "test"
        )

    def test_get_param_missing(self) -> None:
        self.assertIsNone(get_query_param("https://example.com?q=test", "missing"))


class TestAddQueryParam(unittest.TestCase):
    def test_add_new_param(self) -> None:
        result = add_query_param("https://example.com", "key", "value")
        self.assertIn("key=value", result)

    def test_add_param_preserves_existing(self) -> None:
        result = add_query_param("https://example.com?a=1", "b", "2")
        self.assertIn("a=1", result)
        self.assertIn("b=2", result)

    def test_add_param_overwrites(self) -> None:
        result = add_query_param("https://example.com?a=1", "a", "2")
        self.assertIn("a=2", result)

    def test_add_param_int_value(self) -> None:
        result = add_query_param("https://example.com", "count", 42)
        self.assertIn("count=42", result)


class TestRemoveQueryParam(unittest.TestCase):
    def test_remove_existing(self) -> None:
        result = remove_query_param("https://example.com?a=1&b=2", "a")
        self.assertNotIn("a=1", result)
        self.assertIn("b=2", result)

    def test_remove_missing_no_change(self) -> None:
        result = remove_query_param("https://example.com?a=1", "b")
        self.assertIn("a=1", result)

    def test_remove_last_param(self) -> None:
        result = remove_query_param("https://example.com?a=1", "a")
        self.assertNotIn("a=1", result)
        self.assertNotIn("?", result)


class TestBuildUrl(unittest.TestCase):
    def test_build_basic(self) -> None:
        self.assertEqual(build_url(scheme="https", domain="example.com"), "https://example.com")

    def test_build_with_path(self) -> None:
        url = build_url(scheme="https", domain="example.com", path="/api/v1")
        self.assertEqual(url, "https://example.com/api/v1")

    def test_build_with_port(self) -> None:
        url = build_url(scheme="http", domain="example.com", port=8080)
        self.assertEqual(url, "http://example.com:8080")

    def test_build_with_params(self) -> None:
        url = build_url(
            scheme="https", domain="example.com", path="/search", params={"q": "test", "n": 10}
        )
        self.assertIn("q=test", url)
        self.assertIn("n=10", url)

    def test_build_empty_domain_raises(self) -> None:
        with self.assertRaises(ValueError):
            build_url(domain="")

    def test_build_default_scheme(self) -> None:
        url = build_url(domain="example.com")
        self.assertTrue(url.startswith("https://"))


if __name__ == "__main__":
    unittest.main()
TESTURLUTILS
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
- `LICENSE` — MIT license file
- `Makefile` — common developer targets (test, lint, typecheck, run, scaffold, clean, help, pre-commit-install, pre-commit-run)
- `pyproject.toml` — Python project configuration with pytest, ruff, and mypy settings
- `hello.py` — sample application entry point
- `calculator.py` — simple calculator module with arithmetic operations
- `shapes.py` — geometry utilities for areas and perimeters of common shapes
- `strings.py` — string utilities for text operations
- `utils.py` — general utility helper functions
- `stats.py` — statistical utility functions
- `math_utils.py` — mathematical utility functions
- `data_utils.py` — data utility functions
- `datetime_utils.py` — date and time utility functions
- `file_utils.py` — file and path utility functions
- `url_utils.py` — URL and web utility functions
- `tests/test_hello.py` — unit tests for `hello.py`
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `tests/test_strings.py` — unit tests for `strings.py`
- `tests/test_utils.py` — unit tests for `utils.py`
- `tests/test_stats.py` — unit tests for `stats.py`
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- `tests/test_datetime_utils.py` — unit tests for `datetime_utils.py`
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- `tests/test_url_utils.py` — unit tests for `url_utils.py`

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

# --- LICENSE ---
cat > "$OUTPUT_DIR/LICENSE" <<LICENSE
MIT License

Copyright (c) ${PROJECT_YEARS:-2024} ${PROJECT_AUTHOR:-kilo-autonomous}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICENSE

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
stats.py                     # Statistical utility functions
math_utils.py               # Mathematical utility functions
data_utils.py               # Data utility functions
datetime_utils.py           # Date and time utility functions
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
  .gitignore                   # Common ignore patterns
LICENSE                      # MIT License
tests/                       # Python unit tests
  test_hello.py              # Tests for hello.py
  test_calculator.py         # Tests for calculator.py
  test_scaffold.py           # Tests for scaffold.sh
  test_shapes.py             # Tests for shapes.py
  test_strings.py            # Tests for strings.py
  test_utils.py              # Tests for utils.py
  test_stats.py              # Tests for stats.py
  test_math_utils.py         # Tests for math_utils.py
  test_data_utils.py          # Tests for data_utils.py
  test_datetime_utils.py      # Tests for datetime_utils.py
  test_file_utils.py         # Tests for file_utils.py
  test_url_utils.py          # Tests for url_utils.py
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

- `hello.py` — sample application entry point
- `tests/test_hello.py` — unit tests for `hello.py`
- `scaffold.sh` — project scaffolding script
- `AGENTS.md` — agent instructions with task handover protocol
- `kilo.json` — Kilo project configuration
- `Makefile` — developer targets
- `pyproject.toml` — Python project configuration
- `.gitignore` — common ignore patterns
- `LICENSE` — MIT license file
- `.kilo/agent/scaffolder.md` — scaffolder subagent
- `.kilo/command/handover.md` — handover command
- `.kilo/command/scaffold-project.md` — scaffold-project command
- `.kilo/skill/scaffolding-helper.md` — sample skill
- `.kilo/.gitignore` — ignore patterns for the .kilo directory
- `.github/workflows/main.yml` — CI workflow for Kilo agent loop
- `README.md` — project overview
- `CHANGELOG.md` — changelog following Keep a Changelog format
- `.pre-commit-config.yaml` — pre-commit hooks for ruff, mypy, tests, and scaffold
- `calculator.py` — simple calculator module with arithmetic operations
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `shapes.py` — geometry utilities for areas and perimeters of common shapes
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `strings.py` — string utilities for text operations
- `tests/test_strings.py` — unit tests for `strings.py`
- `utils.py` — general utility helper functions
- `tests/test_utils.py` — unit tests for `utils.py`
- \`stats.py\` — statistical utility functions
- \`tests/test_stats.py\` — unit tests for \`stats.py\`
- \`math_utils.py\` — mathematical utility functions
- \`tests/test_math_utils.py\` — unit tests for \`math_utils.py\`
- \`data_utils.py\` — data utility functions
- \`tests/test_data_utils.py\` — unit tests for \`data_utils.py\`
- \`file_utils.py\` — file and path utility functions
- \`tests/test_file_utils.py\` — unit tests for \`file_utils.py\`
- \`datetime_utils.py\` — date and time utility functions
- \`tests/test_datetime_utils.py\` — unit tests for \`datetime_utils.py\`
- \`url_utils.py\` — URL and web utility functions
- \`tests/test_url_utils.py\` — unit tests for \`url_utils.py\`
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
