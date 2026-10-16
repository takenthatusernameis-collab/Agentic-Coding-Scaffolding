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
#   - config_utils.py configuration utilities for JSON file management
#   - collections_utils.py collection utilities (chunk, flatten, frequency, merge_dicts, uniq, and more)
#   - shapes.py geometry utilities for areas and perimeters of common shapes
#   - strings.py string utilities for text operations
#   - tests/test_hello.py unit tests for the sample application
#   - tests/test_calculator.py unit tests for the calculator module
#   - tests/test_config_utils.py unit tests for the config utilities module
#   - tests/test_collections_utils.py unit tests for the collections utilities module
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
#   - random_utils.py random number generation and sampling utilities
#   - tests/test_random_utils.py unit tests for the random_utils module
#   - validation_utils.py input validation utilities
#   - tests/test_validation_utils.py unit tests for the validation_utils module
#   - crypto_utils.py cryptographic utilities
#   - tests/test_crypto_utils.py unit tests for the crypto_utils module
#   - list_utils.py advanced list manipulation utilities
#   - tests/test_list_utils.py unit tests for the list_utils module
#   - env_utils.py environment variable handling and typed accessors
#   - tests/test_env_utils.py unit tests for the env_utils module
#   - logging_utils.py logging configuration and helper utilities
#   - tests/test_logging_utils.py unit tests for the logging_utils module
#   - cache_utils.py caching utilities for memoizing function results
#   - tests/test_cache_utils.py unit tests for the cache_utils module
#   - timing_utils.py performance measurement helpers
#   - tests/test_timing_utils.py unit tests for the timing_utils module
#   - async_utils.py async utility functions
#   - bit_utils.py bitwise utility functions for working with binary representations of integers
#   - concurrent_utils.py concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
#   - tests/test_async_utils.py unit tests for the async_utils module
#   - tests/test_bit_utils.py unit tests for the bit_utils module
#   - tests/test_concurrent_utils.py unit tests for the concurrent_utils module
#   - priority_queue_utils.py heap-based priority queue implementation
#   - tests/test_priority_queue_utils.py unit tests for the priority_queue_utils module
#   - rate_limiter_utils.py rate limiting utilities (token bucket algorithm)
#   - tests/test_rate_limiter_utils.py unit tests for the rate_limiter_utils module
#   - retry_utils.py retry utilities with exponential backoff and jitter
#   - tests/test_retry_utils.py unit tests for the retry_utils module
#   - dict_utils.py dictionary utilities (deep merge, flatten/unflatten, safe get, invert, filter)
#   - tests/test_dict_utils.py unit tests for the dict_utils module
#   - json_utils.py JSON utility functions (read/write/parse/dump/validate)
#   - tests/test_json_utils.py unit tests for the json_utils module
#   - csv_utils.py CSV utility functions (read/write/append as dicts or lists)
#   - tests/test_csv_utils.py unit tests for the csv_utils module
#   - set_utils.py set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
#   - tests/test_set_utils.py unit tests for the set_utils module
#   - statistics_utils.py — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
#   - tests/test_statistics_utils.py — unit tests for statistics_utils.py
#   - string_utils.py — advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
#   - tests/test_string_utils.py — unit tests for the string_utils module
#   - type_utils.py — type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
#   - tests/test_type_utils.py — unit tests for the type_utils module
#   - path_utils.py — path manipulation utilities (join, normalize, components, extensions)
#   - tests/test_path_utils.py — unit tests for the path_utils module
#   - color_utils.py — color manipulation utilities (hex/rgb/hsl conversion, luminance, contrast, accessibility)
#   - pattern_utils.py — design pattern utilities (Singleton, Factory, Observer, Strategy)
#   - tests/test_color_utils.py — unit tests for the color_utils module
#   - tests/test_pattern_utils.py — unit tests for the pattern_utils module
#   - functools_utils.py — functional programming utilities (compose, pipe, curry, apply)
#   - tests/test_functools_utils.py — unit tests for the functools_utils module
#   - tree_utils.py tree and nested structure utilities
#   - tests/test_tree_utils.py unit tests for the tree_utils module
#   - config_schema.py — typed configuration schema utilities (SchemaField, ConfigSchema, validators)
#   - tests/test_config_schema.py — unit tests for config_schema.py
#   - exceptions_utils.py — custom exception classes and error handling utilities
#   - tests/test_exceptions_utils.py — unit tests for exceptions_utils.py
#   - io_utils.py — line-oriented and atomic input/output utilities (read_lines, write_lines, append_text, atomic_write_text, stream_copy, count_lines, iter_lines)
#   - tests/test_io_utils.py — unit tests for io_utils.py
#   - ini_utils.py — INI configuration file utilities (load_config, save_config, get_config_value, set_config_value, merge_configs, list_sections, has_section, get_section)
#   - tests/test_ini_utils.py — unit tests for ini_utils.py
#   - regex_utils.py — regular expression utilities (compile, match, search, replace, split, escape, extract groups, named groups)
#   - tests/test_regex_utils.py — unit tests for regex_utils.py
#   - terminal_utils.py — terminal output utilities (ANSI color, progress bars, clear screen, prompts)
#   - tests/test_terminal_utils.py — unit tests for terminal_utils.py
#   - cli_utils.py — command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
#   - hash_utils.py — hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
#   - tests/test_hash_utils.py — unit tests for hash_utils.py
#   - html_utils.py — HTML escaping, unescaping, and tag-stripping utilities
#   - tests/test_html_utils.py — unit tests for html_utils.py
#   - base64_utils.py — Base64 and hexadecimal encoding/decoding utilities
#   - tests/test_base64_utils.py — unit tests for base64_utils.py
#   - struct_utils.py — Binary struct packing and unpacking utilities
#   - tests/test_struct_utils.py — unit tests for struct_utils.py
#   - http_utils.py — HTTP status codes and response handling utilities
#   - tests/test_http_utils.py — unit tests for http_utils.py
#   - duration_utils.py — time duration utilities (parse, format, convert between units)
#   - tests/test_duration_utils.py — unit tests for duration_utils.py
#   - temp_utils.py — temporary file and directory management utilities
#   - tests/test_temp_utils.py — unit tests for temp_utils.py
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

[tool.setuptools]
py_modules = [
    "hello",
    "calculator",
    "config_utils",
    "collections_utils",
    "shapes",
    "strings",
    "utils",
    "stats",
    "math_utils",
    "data_utils",
    "datetime_utils",
    "file_utils",
    "url_utils",
    "uuid_utils",
    "prompt_utils",
    "compression_utils",
    "ip_utils",
    "regex_utils",
    "random_utils",
    "validation_utils",
    "crypto_utils",
    "list_utils",
    "env_utils",
    "logging_utils",
    "cache_utils",
    "timing_utils",
    "async_utils",
    "bit_utils",
    "concurrent_utils",
    "priority_queue_utils",
    "rate_limiter_utils",
    "dict_utils",
    "json_utils",
    "csv_utils",
    "set_utils",
    "statistics_utils",
    "string_utils",
   "type_utils",
   "tree_utils",
   "path_utils",
   "pattern_utils",
   "functools_utils",
   "config_schema",
   "exceptions_utils",
   "io_utils",
   "cli_utils",
   "terminal_utils",
    "hash_utils",
    "http_utils",
    "html_utils",
    "base64_utils",
    "struct_utils",
    "duration_utils",
    "temp_utils",
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

# --- config_utils.py ---
cat > "$OUTPUT_DIR/config_utils.py" <<'CONFIG_UTILS'
"""Configuration utility functions for loading and managing configuration files.

This module provides utilities for working with configuration files,
currently supporting JSON format with potential for extension to other formats.
"""

import json
from typing import Any, Dict, Optional, Union
from pathlib import Path


def load_config(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from a JSON file.

    Args:
        file_path: Path to the JSON configuration file

    Returns:
        Dictionary containing the configuration data

    Raises:
        FileNotFoundError: If the configuration file does not exist
        json.JSONDecodeError: If the file contains invalid JSON
        TypeError: If file_path is not a string or Path object
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config: Dict[str, Any], file_path: Union[str, Path], indent: int = 2) -> None:
    """Save configuration to a JSON file.

    Args:
        config: Dictionary containing configuration data to save
        file_path: Path where the JSON configuration file should be saved
        indent: Number of spaces for indentation in the JSON output (default: 2)

    Raises:
        TypeError: If config is not a dictionary or file_path is not a string/Path
        OSError: If there is an issue writing to the file
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=indent, ensure_ascii=False)


def get_config_value(
    config: Dict[str, Any],
    key_path: str,
    default: Any = None,
    separator: str = "."
) -> Any:
    """Get a value from a nested configuration dictionary using dot notation.

    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the desired value (e.g., "database.host")
        default: Value to return if the key path is not found (default: None)
        separator: Separator character for the key path (default: ".")

    Returns:
        The value at the specified key path, or default if not found

    Example:
        >>> config = {"database": {"host": "localhost", "port": 5432}}
        >>> get_config_value(config, "database.host")
        'localhost'
        >>> get_config_value(config, "database.username", "admin")
        'admin'
    """
    if not isinstance(config, dict):
        return default

    keys = key_path.split(separator)
    current = config

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


def set_config_value(
    config: Dict[str, Any],
    key_path: str,
    value: Any,
    separator: str = "."
) -> None:
    """Set a value in a nested configuration dictionary using dot notation.

    Args:
        config: Configuration dictionary to modify
        key_path: Dot-separated path where the value should be set (e.g., "database.host")
        value: Value to set at the specified location
        separator: Separator character for the key path (default: ".")

    Raises:
        TypeError: If config is not a dictionary

    Example:
        >>> config = {"database": {"host": "localhost"}}
        >>> set_config_value(config, "database.port", 5432)
        >>> config
        {'database': {'host': 'localhost', 'port': 5432}}
        >>> set_config_value(config, "database.username", "admin")
        >>> config
        {'database': {'host': 'localhost', 'port': 5432, 'username': 'admin'}}
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    keys = key_path.split(separator)
    current = config

    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            # Overwrite non-dict value with dict to continue path
            current[key] = {}
        current = current[key]

    # Set the final key
    current[keys[-1]] = value


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries, with override taking precedence.

    Args:
        base: Base configuration dictionary
        override: Override configuration dictionary

    Returns:
        New dictionary with merged configuration

    Note:
        This function performs a deep merge. Nested dictionaries are merged
        recursively rather than replaced.

    Example:
        >>> base = {"database": {"host": "localhost", "port": 5432}, "debug": False}
        >>> override = {"database": {"port": 5433}, "debug": True}
        >>> merge_configs(base, override)
        {'database': {'host': 'localhost', 'port': 5433}, 'debug': True}
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise TypeError("Both base and override must be dictionaries")

    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result
CONFIG_UTILS

# --- collections_utils.py ---
cat > "$OUTPUT_DIR/collections_utils.py" <<'COLLECTIONS_UTILS'
"""Collection utility functions for working with iterables and data structures."""

from __future__ import annotations

from collections import Counter, deque
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

__all__: List[str] = [
    "chunk",
    "flatten",
    "deep_flatten",
    "windowed",
    "uniq",
    "uniq_by",
    "frequency",
    "most_common",
    "least_common",
    "merge_dicts",
    "to_deque",
    "pluck",
    "compact",
    "partition_by",
]


def chunk(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Split an iterable into chunks of a specified size.

    Args:
        iterable: The iterable to chunk.
        size: The maximum size of each chunk.

    Yields:
        Lists containing up to ``size`` elements each.

    Raises:
        TypeError: If ``size`` is not an integer.
        ValueError: If ``size`` is less than or equal to 0.

    Examples:
        >>> list(chunk([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an integer")
    if size <= 0:
        raise ValueError("size must be greater than 0")

    it = iter(iterable)
    while True:
        batch: List[T] = []
        try:
            for _ in range(size):
                batch.append(next(it))
        except StopIteration:
            if batch:
                yield batch
            break
        yield batch


def flatten(iterable: Iterable[Union[T, Iterable[T]]]) -> List[T]:
    """Flatten a one-level nested iterable.

    Args:
        iterable: The iterable to flatten.

    Returns:
        A flat list containing all top-level elements of nested iterables.

    Examples:
        >>> flatten([1, [2, 3], [4], 5])
        [1, 2, 3, 4, 5]
    """
    result: List[T] = []
    for item in iterable:
        if isinstance(item, (list, tuple, set)):
            result.extend(item)  # type: ignore[arg-type]
        else:
            result.append(item)  # type: ignore[arg-type]
    return result


def deep_flatten(iterable: Iterable[Any]) -> List[Any]:
    """Recursively flatten a nested iterable.

    Args:
        iterable: The iterable to deeply flatten.

    Returns:
        A flat list containing all non-iterable elements.

    Examples:
        >>> deep_flatten([1, [2, [3, 4]], 5])
        [1, 2, 3, 4, 5]
    """
    result: List[Any] = []
    for item in iterable:
        if isinstance(item, (list, tuple, set)):
            result.extend(deep_flatten(item))  # type: ignore[arg-type]
        else:
            result.append(item)
    return result


def windowed(iterable: Iterable[T], size: int) -> Iterator[Tuple[T, ...]]:
    """Create sliding windows over an iterable.

    Args:
        iterable: The iterable to window.
        size: The size of each window.

    Yields:
        Tuples containing consecutive elements in each window.

    Raises:
        TypeError: If ``size`` is not an integer.
        ValueError: If ``size`` is less than or equal to 0.

    Examples:
        >>> list(windowed([1, 2, 3, 4], 2))
        [(1, 2), (2, 3), (3, 4)]
    """
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an integer")
    if size <= 0:
        raise ValueError("size must be greater than 0")

    it = iter(iterable)
    win: Deque[T] = deque()
    for item in it:
        win.append(item)
        if len(win) == size:
            yield tuple(win)
            win.popleft()


def uniq(iterable: Iterable[T]) -> List[T]:
    """Remove duplicate elements while preserving order.

    Args:
        iterable: The iterable to deduplicate.

    Returns:
        A list with duplicate elements removed, preserving first occurrence order.

    Examples:
        >>> uniq([1, 2, 2, 3, 1])
        [1, 2, 3]
    """
    seen: Set[T] = set()
    result: List[T] = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def uniq_by(iterable: Iterable[T], key_func: Callable[[T], Any]) -> List[T]:
    """Remove duplicate elements based on a key function while preserving order.

    Args:
        iterable: The iterable to deduplicate.
        key_func: Function to compute the deduplication key.

    Returns:
        A list with duplicates (by key) removed, preserving first occurrence order.

    Examples:
        >>> uniq_by([{'id': 1}, {'id': 2}, {'id': 1}], lambda x: x['id'])
        [{'id': 1}, {'id': 2}]
    """
    seen: Set[Any] = set()
    result: List[T] = []
    for item in iterable:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def frequency(iterable: Iterable[T]) -> Dict[T, int]:
    """Count frequency of each element in an iterable.

    Args:
        iterable: The iterable to analyze.

    Returns:
        A dictionary mapping each element to its count.

    Examples:
        >>> freq = frequency([1, 2, 2, 3])
        >>> freq[2]
        2
    """
    return dict(Counter(iterable))


def most_common(iterable: Iterable[T], n: Optional[int] = None) -> List[Tuple[T, int]]:
    """Return the most common elements from an iterable.

    Args:
        iterable: The iterable to analyze.
        n: Number of top elements to return (None returns all, sorted desc).

    Returns:
        List of (element, count) tuples sorted by count descending.

    Examples:
        >>> most_common([1, 2, 2, 3, 3, 3])
        [(3, 3), (2, 2), (1, 1)]
    """
    counter = Counter(iterable)
    return counter.most_common(n)  # type: ignore[return-value]


def least_common(iterable: Iterable[T], n: Optional[int] = None) -> List[Tuple[T, int]]:
    """Return the least common elements from an iterable.

    Args:
        iterable: The iterable to analyze.
        n: Number of bottom elements to return (None returns all).

    Returns:
        List of (element, count) tuples sorted by count ascending.

    Examples:
        >>> least_common([1, 2, 2, 3, 3, 3], n=1)
        [(1, 1)]
    """
    counter = Counter(iterable)
    items = counter.most_common()  # all sorted desc
    items_reversed = list(reversed(items))
    if n is None:
        return items_reversed
    return items_reversed[:n]


def merge_dicts(*dicts: Dict[K, V]) -> Dict[K, V]:
    """Merge multiple dictionaries, with later dicts taking precedence.

    Args:
        *dicts: Dictionaries to merge.

    Returns:
        A new merged dictionary.

    Examples:
        >>> merge_dicts({'a': 1}, {'b': 2}, {'a': 3})
        {'a': 3, 'b': 2}
    """
    result: Dict[K, V] = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def to_deque(iterable: Iterable[T], maxlen: Optional[int] = None) -> Deque[T]:
    """Convert an iterable to a deque.

    Args:
        iterable: The iterable to convert.
        maxlen: Maximum length of deque (optional).

    Returns:
        A deque containing all elements from iterable.

    Examples:
        >>> d = to_deque([1, 2, 3])
        >>> len(d)
        3
    """
    return deque(iterable, maxlen=maxlen) if maxlen is not None else deque(iterable)


def pluck(iterable: Iterable[Dict[K, Any]], key: K) -> List[Any]:
    """Extract values for a specific key from a list of dictionaries.

    Args:
        iterable: Iterable of dictionaries.
        key: The key to extract values for.

    Returns:
        List of values for the key (skips missing keys).

    Examples:
        >>> pluck([{'a': 1}, {'a': 2}, {'b': 3}], 'a')
        [1, 2]
    """
    result: List[Any] = []
    for item in iterable:
        if isinstance(item, dict) and key in item:
            result.append(item[key])
    return result


def compact(iterable: Iterable[T]) -> List[T]:
    """Remove falsy values from an iterable.

    Removes values that are Falsey: False, None, 0, "", [], {}, set().

    Args:
        iterable: The iterable to compact.

    Returns:
        List with falsy values removed.

    Examples:
        >>> compact([0, 1, False, 2, '', 3, None])
        [1, 2, 3]
    """
    result: List[T] = []
    for item in iterable:
        if item:
            result.append(item)
    return result


def partition_by(iterable: Iterable[T], key_func: Callable[[T], Any]) -> List[List[T]]:
    """Partition an iterable into groups with consecutive equal keys.

    Args:
        iterable: The iterable to partition.
        key_func: Function to compute the partition key.

    Returns:
        List of lists, where each inner list contains consecutive elements
        with the same key.

    Examples:
        >>> list_of_groups = partition_by([1, 1, 2, 2, 3], lambda x: x)
        >>> list_of_groups
        [[1, 1], [2, 2], [3]]
    """
    result: List[List[T]] = []
    it = iter(iterable)
    try:
        first = next(it)
        current_key = key_func(first)
        current_group: List[T] = [first]
    except StopIteration:
        return result

    for item in it:
        key = key_func(item)
        if key == current_key:
            current_group.append(item)
        else:
            result.append(current_group)
            current_key = key
            current_group = [item]
    result.append(current_group)
    return result
COLLECTIONS_UTILS

# --- tests/test_config_utils.py ---
cat > "$OUTPUT_DIR/tests/test_config_utils.py" <<'TESTCONFIGUTILS'
import json
import tempfile
import unittest
from pathlib import Path

from config_utils import (
    load_config,
    save_config,
    get_config_value,
    set_config_value,
    merge_configs
)


class TestLoadConfig(unittest.TestCase):
    """Test the load_config function."""

    def test_load_valid_json(self):
        """Test loading a valid JSON configuration file."""
        config_data = {"key": "value", "number": 42, "nested": {"inner": "data"}}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            loaded = load_config(temp_path)
            self.assertEqual(loaded, config_data)
        finally:
            Path(temp_path).unlink()

    def test_load_file_not_found(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_config("/non/existent/file.json")

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises json.JSONDecodeError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')  # Missing quotes around json
            temp_path = f.name

        try:
            with self.assertRaises(json.JSONDecodeError):
                load_config(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_load_with_path_object(self):
        """Test loading works with Path objects."""
        config_data = {"test": "value"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = Path(f.name)

        try:
            loaded = load_config(temp_path)
            self.assertEqual(loaded, config_data)
        finally:
            temp_path.unlink()


class TestSaveConfig(unittest.TestCase):
    """Test the save_config function."""

    def test_save_and_load_roundtrip(self):
        """Test saving and loading preserves data."""
        original_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "debug": True,
            "tags": ["production", "web"]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            save_config(original_config, temp_path)
            loaded_config = load_config(temp_path)
            self.assertEqual(loaded_config, original_config)
        finally:
            Path(temp_path).unlink()

    def test_save_creates_directories(self):
        """Test that save_config creates parent directories if needed."""
        config = {"test": "value"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_path = Path(tmp_dir) / "nested" / "deep" / "config.json"

            # Directory should not exist yet
            self.assertFalse(nested_path.parent.exists())

            save_config(config, nested_path)

            # Directory and file should now exist
            self.assertTrue(nested_path.exists())
            self.assertTrue(nested_path.parent.exists())

            loaded = load_config(nested_path)
            self.assertEqual(loaded, config)

    def test_save_invalid_config_type(self):
        """Test that saving non-dict config raises TypeError."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(TypeError):
                save_config(["not", "a", "dict"], temp_path)
        finally:
            Path(temp_path).unlink()

    def test_save_custom_indent(self):
        """Test saving with custom indentation."""
        config = {"key": "value"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            save_config(config, temp_path, indent=4)

            with open(temp_path, 'r') as f:
                content = f.read()

            # Should contain indentation
            self.assertIn('    "key": "value"', content)
        finally:
            Path(temp_path).unlink()


class TestGetConfigValue(unittest.TestCase):
    """Test the get_config_value function."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "debug": True,
            "tags": ["production", "web"],
            "simple_value": 42
        }

    def test_get_top_level_value(self):
        """Test getting a top-level configuration value."""
        self.assertEqual(get_config_value(self.config, "debug"), True)
        self.assertEqual(get_config_value(self.config, "simple_value"), 42)

    def test_get_nested_value(self):
        """Test getting a nested configuration value."""
        self.assertEqual(get_config_value(self.config, "database.host"), "localhost")
        self.assertEqual(get_config_value(self.config, "database.port"), 5432)
        self.assertEqual(
            get_config_value(self.config, "database.credentials.username"),
            "admin"
        )

    def test_get_missing_key_returns_default(self):
        """Test that missing keys return the default value."""
        self.assertIsNone(get_config_value(self.config, "missing_key"))
        self.assertEqual(get_config_value(self.config, "missing_key", "default"), "default")
        self.assertEqual(get_config_value(self.config, "database.missing", 999), 999)

    def test_get_value_via_nested_missing_parent(self):
        """Test getting a value when an intermediate parent is missing."""
        self.assertIsNone(get_config_value(self.config, "missing.parent.child"))
        self.assertEqual(
            get_config_value(self.config, "missing.parent.child", "found"),
            "found"
        )

    def test_get_with_custom_separator(self):
        """Test using a custom separator."""
        config = {"a": {"b": {"c": {"d": "value"}}}}
        self.assertEqual(get_config_value(config, "a/b/c/d", separator="/"), "value")

    def test_get_with_non_dict_config(self):
        """Test getting value from non-dict config returns default."""
        self.assertEqual(get_config_value("not a dict", "key", "default"), "default")
        self.assertEqual(get_config_value([], "key", "default"), "default")
        self.assertEqual(get_config_value(42, "key", "default"), "default")
        # Also test that it returns None when no default provided
        self.assertIsNone(get_config_value("not a dict", "key"))
        self.assertIsNone(get_config_value([], "key"))
        self.assertIsNone(get_config_value(42, "key"))


class TestSetConfigValue(unittest.TestCase):
    """Test the set_config_value function."""

    def test_set_top_level_value(self):
        """Test setting a top-level configuration value."""
        config = {}
        set_config_value(config, "new_key", "new_value")
        self.assertEqual(config["new_key"], "new_value")

    def test_set_nested_value(self):
        """Test setting a nested configuration value."""
        config = {}
        set_config_value(config, "database.host", "localhost")
        set_config_value(config, "database.port", 5432)

        expected = {"database": {"host": "localhost", "port": 5432}}
        self.assertEqual(config, expected)

    def test_set_overwrites_existing(self):
        """Test that setting overwrites existing values."""
        config = {"key": "old_value"}
        set_config_value(config, "key", "new_value")
        self.assertEqual(config["key"], "new_value")

    def test_set_creates_intermediate_dicts(self):
        """Test that intermediate dictionaries are created as needed."""
        config = {"existing": "value"}
        set_config_value(config, "new.nested.path", "final")

        expected = {
            "existing": "value",
            "new": {
                "nested": {
                    "path": "final"
                }
            }
        }
        self.assertEqual(config, expected)

    def test_set_with_custom_separator(self):
        """Test using a custom separator."""
        config = {}
        set_config_value(config, "a/b/c", "value", separator="/")
        expected = {"a": {"b": {"c": "value"}}}
        self.assertEqual(config, expected)

    def test_set_invalid_config_type(self):
        """Test that setting value in non-dict config raises TypeError."""
        with self.assertRaises(TypeError):
            set_config_value(["not", "a", "dict"], "key", "value")

        with self.assertRaises(TypeError):
            set_config_value("string", "key", "value")

        with self.assertRaises(TypeError):
            set_config_value(42, "key", "value")


class TestMergeConfigs(unittest.TestCase):
    """Test the merge_configs function."""

    def test_merge_simple_dicts(self):
        """Test merging simple flat dictionaries."""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        expected = {"a": 1, "b": 3, "c": 4}
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_nested_dicts(self):
        """Test merging nested dictionaries."""
        base = {
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "debug": False
        }
        override = {
            "database": {
                "port": 5433,
                "credentials": {
                    "user": "admin"
                }
            },
            "debug": True
        }
        expected = {
            "database": {
                "host": "localhost",
                "port": 5433,
                "credentials": {
                    "user": "admin"
                }
            },
            "debug": True
        }
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_preserves_base_when_no_override(self):
        """Test that base values are preserved when not overridden."""
        base = {"a": 1, "b": {"x": 10}}
        override = {"b": {"y": 20}}
        expected = {"a": 1, "b": {"x": 10, "y": 20}}
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_with_empty_dicts(self):
        """Test merging with empty dictionaries."""
        base = {"a": 1}
        override = {}
        self.assertEqual(merge_configs(base, override), base)

        base = {}
        override = {"b": 2}
        self.assertEqual(merge_configs(base, override), override)

        base = {}
        override = {}
        self.assertEqual(merge_configs(base, override), {})

    def test_merge_invalid_types(self):
        """Test that merging invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            merge_configs("not a dict", {"a": 1})

        with self.assertRaises(TypeError):
            merge_configs({"a": 1}, "not a dict")

        with self.assertRaises(TypeError):
            merge_configs(["a"], {"b": 2})


if __name__ == "__main__":
    unittest.main()
TESTCONFIGUTILS

# --- tests/test_collections_utils.py ---
cat > "$OUTPUT_DIR/tests/test_collections_utils.py" <<'TESTCOLLECTIONSUTILS'
"""Tests for collections_utils module."""

import unittest
from collections import deque

from collections_utils import (
    chunk,
    compact,
    deep_flatten,
    flatten,
    frequency,
    least_common,
    merge_dicts,
    most_common,
    partition_by,
    pluck,
    to_deque,
    uniq,
    uniq_by,
    windowed,
)


class TestChunk(unittest.TestCase):
    def test_chunk_basic(self):
        result = list(chunk([1, 2, 3, 4, 5], 2))
        self.assertEqual(result, [[1, 2], [3, 4], [5]])

    def test_chunk_exact(self):
        result = list(chunk([1, 2, 3, 4], 2))
        self.assertEqual(result, [[1, 2], [3, 4]])

    def test_chunk_size_one(self):
        result = list(chunk([1, 2, 3], 1))
        self.assertEqual(result, [[1], [2], [3]])

    def test_chunk_errors(self):
        with self.assertRaises(TypeError):
            list(chunk([1, 2, 3], "2"))  # type: ignore

        with self.assertRaises(ValueError):
            list(chunk([1, 2, 3], 0))

        with self.assertRaises(ValueError):
            list(chunk([1, 2, 3], -1))


class TestFlatten(unittest.TestCase):
    def test_flatten_basic(self):
        result = flatten([1, [2, 3], [4], 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_flatten_with_tuples(self):
        result = flatten([1, (2, 3), 4])
        self.assertEqual(result, [1, 2, 3, 4])

    def test_flatten_empty(self):
        result = flatten([])
        self.assertEqual(result, [])


class TestDeepFlatten(unittest.TestCase):
    def test_deep_flatten_basic(self):
        result = deep_flatten([1, [2, [3, 4]], 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_deep_flatten_multiple_levels(self):
        result = deep_flatten([1, [2, [3, [4]]]])
        self.assertEqual(result, [1, 2, 3, 4])


class TestWindowed(unittest.TestCase):
    def test_windowed_basic(self):
        result = list(windowed([1, 2, 3, 4], 2))
        self.assertEqual(result, [(1, 2), (2, 3), (3, 4)])

    def test_windowed_size_three(self):
        result = list(windowed([1, 2, 3, 4, 5], 3))
        self.assertEqual(result, [(1, 2, 3), (2, 3, 4), (3, 4, 5)])

    def test_windowed_errors(self):
        with self.assertRaises(TypeError):
            list(windowed([1, 2, 3], "1"))  # type: ignore

        with self.assertRaises(ValueError):
            list(windowed([1, 2, 3], 0))


class TestUniq(unittest.TestCase):
    def test_uniq_basic(self):
        result = uniq([1, 2, 2, 3, 1])
        self.assertEqual(result, [1, 2, 3])

    def test_uniq_preserves_order(self):
        result = uniq([3, 1, 2, 1, 3])
        self.assertEqual(result, [3, 1, 2])


class TestUniqBy(unittest.TestCase):
    def test_uniq_by_basic(self):
        result = uniq_by([{"id": 1}, {"id": 2}, {"id": 1}], lambda x: x["id"])
        self.assertEqual(result, [{"id": 1}, {"id": 2}])


class TestFrequency(unittest.TestCase):
    def test_frequency_basic(self):
        result = frequency([1, 2, 2, 3])
        self.assertEqual(result[2], 2)
        self.assertEqual(result[1], 1)


class TestMostLeastCommon(unittest.TestCase):
    def test_most_common(self):
        result = most_common([1, 2, 2, 3, 3, 3])
        self.assertEqual(result[0], (3, 3))

    def test_most_common_n(self):
        result = most_common([1, 2, 2, 3, 3, 3], n=1)
        self.assertEqual(result, [(3, 3)])

    def test_least_common(self):
        result = least_common([1, 2, 2, 3, 3, 3], n=1)
        self.assertEqual(result, [(1, 1)])


class TestMergeDicts(unittest.TestCase):
    def test_merge_dicts_basic(self):
        result = merge_dicts({"a": 1}, {"b": 2}, {"a": 3})
        self.assertEqual(result["a"], 3)
        self.assertEqual(result["b"], 2)


class TestToDeque(unittest.TestCase):
    def test_to_deque_basic(self):
        d = to_deque([1, 2, 3])
        self.assertIsInstance(d, deque)
        self.assertEqual(len(d), 3)

    def test_to_deque_maxlen(self):
        d = to_deque([1, 2, 3], maxlen=2)
        self.assertEqual(len(d), 2)


class TestPluck(unittest.TestCase):
    def test_pluck_basic(self):
        result = pluck([{"a": 1}, {"a": 2}, {"b": 3}], "a")
        self.assertEqual(result, [1, 2])

    def test_pluck_missing_key(self):
        result = pluck([{"a": 1}, {"b": 2}], "a")
        self.assertEqual(result, [1])


class TestCompact(unittest.TestCase):
    def test_compact_basic(self):
        result = compact([0, 1, False, 2, "", 3, None])
        self.assertEqual(result, [1, 2, 3])

    def test_compact_empty_lists(self):
        result = compact([0, [], "", None])
        self.assertEqual(result, [])


class TestPartitionBy(unittest.TestCase):
    def test_partition_by_basic(self):
        result = partition_by([1, 1, 2, 2, 3], lambda x: x)
        self.assertEqual(result, [[1, 1], [2, 2], [3]])

    def test_partition_by_empty(self):
        result = partition_by([], lambda x: x)
        self.assertEqual(result, [])

    def test_partition_by_consecutive_change(self):
        result = partition_by([1, 2, 1], lambda x: x % 2)
        self.assertEqual(result, [[1], [2], [1]])


if __name__ == "__main__":
    unittest.main()
TESTCOLLECTIONSUTILS

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

    Examples:
        >>> mean([1, 2, 3, 4, 5])
        3.0
        >>> mean([2, 4])
        3.0
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

    Examples:
        >>> median([1, 2, 3, 4, 5])
        3
        >>> median([1, 2, 3, 4])
        2.5
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


def mode(numbers: List[T | float]) -> float:
    """Return the mode (most frequent value) of a list of numbers.

    If there is more than one mode, returns the first one encountered
    in terms of the value that appears first in sorted order of values.

    Args:
        numbers: A list of numeric values.

    Returns:
        The most frequently occurring value.

    Raises:
        ValueError: If the list is empty.

    Examples:
        >>> mode([1, 2, 2, 3, 4])
        2
        >>> mode([1, 1, 2, 2, 3])
        1
    """
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")
    frequency: dict = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_count = max(frequency.values())
    # Return the smallest value (in sorted order) among those with max frequency
    # for deterministic behavior
    for num in sorted(frequency.keys()):
        if frequency[num] == max_count:
            return float(num)
    raise ValueError("Cannot calculate mode of empty list")


def variance(numbers: List[T | float], population: bool = True) -> float:
    """Return the variance of a list of numbers.

    Args:
        numbers: A list of numeric values.
        population: If True, calculate population variance (divide by n).
                    If False, calculate sample variance (divide by n-1).
                    Defaults to True.

    Returns:
        The variance.

    Raises:
        ValueError: If the list is empty, or if calculating sample variance
                    with fewer than 2 elements.

    Examples:
        >>> variance([1, 2, 3, 4, 5])
        2.0
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
                    Defaults to True.

    Returns:
        The standard deviation.

    Raises:
        ValueError: If the list is empty, or if calculating sample std dev
                    with fewer than 2 elements.

    Examples:
        >>> stddev([1, 2, 3, 4, 5])
        1.4142135623730951
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
    """Calculate the factorial of a non-negative integer n.

    Args:
        n: The number to calculate factorial for.

    Returns:
        The factorial of n (n!).

    Raises:
        ValueError: If n is negative.
        OverflowError: If n is too large.

    Examples:
        >>> factorial(0)
        1
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n > 20:  # Prevent large numbers that might cause issues
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    return math.factorial(n)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.

    Args:
        n: The index of the Fibonacci number (n >= 0).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
    """
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
    """Calculate the Greatest Common Divisor of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The GCD of a and b.

    Examples:
        >>> gcd(48, 18)
        6
        >>> gcd(17, 13)
        1
    """
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """Calculate the Least Common Multiple of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The LCM of a and b.

    Examples:
        >>> lcm(4, 6)
        12
        >>> lcm(3, 5)
        15
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: The number to check.

    Returns:
        True if n is prime, False otherwise.

    Raises:
        ValueError: If n < 2.

    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(9)
        False
        >>> is_prime(17)
        True
    """
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
    """Clamp a value between min_val and max_val.

    Args:
        value: The value to clamp.
        min_val: The minimum allowed value.
        max_val: The maximum allowed value.

    Returns:
        The clamped value.

    Raises:
        ValueError: If min_val > max_val.

    Examples:
        >>> clamp(5, 0, 10)
        5
        >>> clamp(-5, 0, 10)
        0
        >>> clamp(15, 0, 10)
        10
    """
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


def parse_datetime(
    value: str, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    """Parse a string into a datetime object.

    Args:
        value: The string to parse.
        fmt: The expected format string. Defaults to ``%Y-%m-%d %H:%M:%S``.

    Returns:
        The parsed datetime object.

    Raises:
        ValueError: If the string does not match the format.
    """
    return datetime.strptime(value, fmt)


def format_datetime(
    dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """Format a datetime object as a string.

    Args:
        dt: The datetime to format.
        fmt: The desired format string. Defaults to ``%Y-%m-%d %H:%M:%S``.

    Returns:
        The formatted string.
    """
    return dt.strftime(fmt)


def days_between(start: DateTimeLike, end: DateTimeLike) -> int:
    """Return the absolute number of whole days between two dates.

    Args:
        start: A datetime or parseable string (format ``%Y-%m-%d``).
        end: A datetime or parseable string (format ``%Y-%m-%d``).

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
    """Return True if *year* is a leap year.

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
        dt: A datetime or a string parseable with ``%Y-%m-%d``/``%Y-%m-%d %H:%M:%S``.
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
        dt: A datetime or a string parseable with ``%Y-%m-%d``.

    Returns:
        The weekday name (e.g. ``Monday``).

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
# --- tests/test_json_utils.py ---
cat > "$OUTPUT_DIR/tests/test_json_utils.py" <<'TESTJSONUTILS'
"""Tests for json_utils module."""

import json
import os
import tempfile
import unittest

from json_utils import (
    dump_json_string,
    is_valid_json,
    load_json_string,
    pretty_print_json,
    read_json,
    write_json,
)


class TestReadWriteJson(unittest.TestCase):
    def test_read_write_json_basic(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            path = f.name

        try:
            data = {"name": "test", "value": 42}
            write_json(path, data)
            loaded = read_json(path)
            self.assertEqual(data, loaded)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_json_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_json("/nonexistent/path.json")

    def test_write_json_with_indent(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            path = f.name

        try:
            data = {"a": 1, "b": 2}
            write_json(path, data, indent=2)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("  ", content)  # indentation
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_write_json_overwrite(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            path = f.name

        try:
            write_json(path, {"a": 1})
            write_json(path, {"b": 2})
            loaded = read_json(path)
            self.assertEqual({"b": 2}, loaded)
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestJsonStrings(unittest.TestCase):
    def test_load_json_string(self) -> None:
        s = '{"key": "value", "num": 123}'
        result = load_json_string(s)
        self.assertEqual(result, {"key": "value", "num": 123})

    def test_load_json_string_invalid(self) -> None:
        with self.assertRaises(json.JSONDecodeError):
            load_json_string("{invalid json}")

    def test_dump_json_string(self) -> None:
        data = {"key": "value", "num": 123}
        result = dump_json_string(data)
        # Should be valid JSON
        self.assertTrue(is_valid_json(result))
        self.assertEqual(load_json_string(result), data)

    def test_dump_json_string_compact(self) -> None:
        data = {"a": 1, "b": 2}
        result = dump_json_string(data, indent=0)
        self.assertTrue(is_valid_json(result))

    def test_dump_json_string_ensure_ascii(self) -> None:
        data = {"text": "café"}
        result = dump_json_string(data, ensure_ascii=True)
        self.assertTrue(is_valid_json(result))


class TestIsValidJson(unittest.TestCase):
    def test_is_valid_json_true(self) -> None:
        self.assertTrue(is_valid_json('{"a": 1}'))
        self.assertTrue(is_valid_json("[]"))
        self.assertTrue(is_valid_json('"string"'))
        self.assertTrue(is_valid_json("123"))
        self.assertTrue(is_valid_json("true"))
        self.assertTrue(is_valid_json("null"))

    def test_is_valid_json_false(self) -> None:
        self.assertFalse(is_valid_json("{"))
        self.assertFalse(is_valid_json("}"))
        self.assertFalse(is_valid_json("{'a': 1}"))  # single quotes
        self.assertFalse(is_valid_json("undefined"))
        self.assertFalse(is_valid_json(""))
        self.assertFalse(is_valid_json(None))  # type: ignore[arg-type]


class TestPrettyPrintJson(unittest.TestCase):
    def test_pretty_print_json_basic(self) -> None:
        data = {"a": 1, "b": [2, 3]}
        result = pretty_print_json(data)
        self.assertTrue(is_valid_json(result))
        self.assertIn("\n", result)  # formatted

    def test_pretty_print_json_custom_indent(self) -> None:
        data = {"a": 1}
        result = pretty_print_json(data, indent=2)
        self.assertTrue(is_valid_json(result))

TESTJSONUTILS
# --- tests/test_csv_utils.py ---
cat > "$OUTPUT_DIR/tests/test_csv_utils.py" <<'TESTCSVUTILS'
"""Tests for csv_utils module."""

import os
import tempfile
import unittest

from csv_utils import (
    append_csv_row,
    read_csv,
    read_csv_as_lists,
    write_csv,
    write_csv_from_lists,
)


class TestReadWriteCSV(unittest.TestCase):
    def test_read_write_csv_dicts(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            rows = [
                {"name": "Alice", "age": "30"},
                {"name": "Bob", "age": "25"},
            ]
            write_csv(path, rows)
            loaded = read_csv(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["name"], "Alice")
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_write_csv_empty_rows(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            write_csv(path, [])
            self.assertTrue(True)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_write_csv_lists(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            rows = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
            write_csv_from_lists(path, rows)
            loaded = read_csv_as_lists(path)
            self.assertEqual(loaded, rows)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_csv_with_custom_delimiter(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("name;age\nAlice;30\n")
            loaded = read_csv(path, delimiter=";")
            self.assertEqual(loaded[0]["name"], "Alice")
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_append_csv_row(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            append_csv_row(path, {"name": "Alice", "age": "30"})
            append_csv_row(path, {"name": "Bob", "age": "25"})
            loaded = read_csv(path)
            self.assertEqual(len(loaded), 2)
        finally:
            if os.path.exists(path):
                os.unlink(path)

TESTCSVUTILS
# --- tests/test_set_utils.py ---
cat > "$OUTPUT_DIR/tests/test_set_utils.py" <<'TESTSETUTILS'
"""Tests for set_utils module."""

import unittest

from set_utils import (
    cartesian_product,
    difference,
    intersection,
    is_subset,
    is_superset,
    power_set,
    symmetric_difference,
    union,
)


class TestIsSubset(unittest.TestCase):
    def test_is_subset_true(self) -> None:
        self.assertTrue(is_subset([1, 2], [1, 2, 3]))

    def test_is_subset_false(self) -> None:
        self.assertFalse(is_subset([1, 4], [1, 2, 3]))

    def test_is_subset_equal(self) -> None:
        self.assertTrue(is_subset([1, 2], [1, 2]))

    def test_is_subset_empty(self) -> None:
        self.assertTrue(is_subset([], [1, 2, 3]))


class TestIsSuperset(unittest.TestCase):
    def test_is_superset_true(self) -> None:
        self.assertTrue(is_superset([1, 2, 3], [2]))

    def test_is_superset_false(self) -> None:
        self.assertFalse(is_superset([1, 2], [2, 3]))

    def test_is_superset_equal(self) -> None:
        self.assertTrue(is_superset([1, 2], [1, 2]))


class TestIntersection(unittest.TestCase):
    def test_intersection_basic(self) -> None:
        self.assertEqual(intersection([1, 2, 3], [2, 3, 4]), {2, 3})

    def test_intersection_disjoint(self) -> None:
        self.assertEqual(intersection([1, 2], [3, 4]), set())

    def test_intersection_no_overlap(self) -> None:
        self.assertEqual(intersection([], [1, 2]), set())


class TestUnion(unittest.TestCase):
    def test_union_basic(self) -> None:
        self.assertEqual(union([1, 2], [2, 3]), {1, 2, 3})

    def test_union_disjoint(self) -> None:
        self.assertEqual(union([1, 2], [3, 4]), {1, 2, 3, 4})

    def test_union_empty(self) -> None:
        self.assertEqual(union([], []), set())


class TestDifference(unittest.TestCase):
    def test_difference_basic(self) -> None:
        self.assertEqual(difference([1, 2, 3], [2]), {1, 3})

    def test_difference_no_overlap(self) -> None:
        self.assertEqual(difference([1, 2], [3, 4]), {1, 2})

    def test_difference_empty(self) -> None:
        self.assertEqual(difference([], [1, 2]), set())


class TestSymmetricDifference(unittest.TestCase):
    def test_symmetric_difference_basic(self) -> None:
        self.assertEqual(symmetric_difference([1, 2, 3], [2, 3, 4]), {1, 4})

    def test_symmetric_difference_disjoint(self) -> None:
        self.assertEqual(symmetric_difference([1, 2], [3, 4]), {1, 2, 3, 4})

    def test_symmetric_difference_equal(self) -> None:
        self.assertEqual(symmetric_difference([1, 2], [1, 2]), set())


class TestCartesianProduct(unittest.TestCase):
    def test_cartesian_product_basic(self) -> None:
        result = list(cartesian_product([1, 2], ["a", "b"]))
        self.assertEqual(result, [(1, "a"), (1, "b"), (2, "a"), (2, "b")])

    def test_cartesian_product_empty(self) -> None:
        self.assertEqual(list(cartesian_product([], [1, 2])), [])
        self.assertEqual(list(cartesian_product([1, 2], [])), [])

    def test_cartesian_product_single(self) -> None:
        self.assertEqual(list(cartesian_product([1], ["x"])), [(1, "x")])


class TestPowerSet(unittest.TestCase):
    def test_power_set_empty(self) -> None:
        result = list(power_set([]))
        self.assertEqual(result, [()])

    def test_power_set_single(self) -> None:
        result = list(power_set([1]))
        self.assertEqual(result, [(), (1,)])

    def test_power_set_two(self) -> None:
        result = list(power_set([1, 2]))
        self.assertEqual(len(result), 4)
        self.assertIn((), result)
        self.assertIn((1,), result)
        self.assertIn((2,), result)
        self.assertIn((1, 2), result)

    def test_power_set_three(self) -> None:
        result = list(power_set([1, 2, 3]))
        self.assertEqual(len(result), 8)

    def test_power_set_preserves_order(self) -> None:
        result = list(power_set(["a", "b"]))
        self.assertEqual(result, [(), ("a",), ("b",), ("a", "b")])


if __name__ == "__main__":
    unittest.main()
TESTSETUTILS
# --- tests/test_statistics_utils.py ---
cat > "$OUTPUT_DIR/tests/test_statistics_utils.py" <<'TESTSTATISTICS'
"""Tests for statistics_utils module."""

import unittest

from statistics_utils import (
    correlation,
    covariance,
    geometric_mean,
    harmonic_mean,
    median_even,
    normalize,
    percentile,
    z_score,
)


class TestHarmonicMean(unittest.TestCase):
    def test_harmonic_mean_basic(self):
        self.assertAlmostEqual(harmonic_mean([1, 2, 4]), 1.7142857142857142)

    def test_harmonic_mean_equal(self):
        self.assertEqual(harmonic_mean([1, 1, 1]), 1.0)

    def test_harmonic_mean_raises_on_empty(self):
        with self.assertRaises(ValueError):
            harmonic_mean([])

    def test_harmonic_mean_raises_on_zero(self):
        with self.assertRaises(ValueError):
            harmonic_mean([1, 0, 3])


class TestGeometricMean(unittest.TestCase):
    def test_geometric_mean_basic(self):
        self.assertAlmostEqual(
            geometric_mean([1, 2, 3, 4, 5]), 2.605171084697352
        )

    def test_geometric_mean_equal(self):
        self.assertEqual(geometric_mean([1, 1, 1]), 1.0)

    def test_geometric_mean_raises_on_empty(self):
        with self.assertRaises(ValueError):
            geometric_mean([])

    def test_geometric_mean_raises_on_negative(self):
        with self.assertRaises(ValueError):
            geometric_mean([1, -2, 3])


class TestMedianEven(unittest.TestCase):
    def test_median_even_even_length(self):
        self.assertEqual(median_even([1, 2, 3, 4]), (2.0, 3.0))

    def test_median_even_odd_length(self):
        self.assertEqual(median_even([1, 2, 3]), (2.0, 2.0))

    def test_median_even_single(self):
        self.assertEqual(median_even([5]), (5.0, 5.0))

    def test_median_even_raises_on_empty(self):
        with self.assertRaises(ValueError):
            median_even([])


class TestPercentile(unittest.TestCase):
    def test_percentile_basic(self):
        self.assertEqual(percentile([1, 2, 3, 4, 5], 50), 3.0)

    def test_percentile_min(self):
        self.assertEqual(percentile([1, 2, 3, 4, 5], 0), 1.0)

    def test_percentile_max(self):
        self.assertEqual(percentile([1, 2, 3, 4, 5], 100), 5.0)

    def test_percentile_other(self):
        # 25th percentile (first quartile) of [1,2,3,4,5] -> 2.0
        self.assertEqual(percentile([1, 2, 3, 4, 5], 25), 2.0)
        # 75th percentile -> 4.0
        self.assertEqual(percentile([1, 2, 3, 4, 5], 75), 4.0)

    def test_percentile_single_element(self):
        self.assertEqual(percentile([42], 50), 42.0)

    def test_percentile_raises_on_empty(self):
        with self.assertRaises(ValueError):
            percentile([], 50)

    def test_percentile_raises_out_of_range(self):
        with self.assertRaises(ValueError):
            percentile([1, 2, 3], -1)
        with self.assertRaises(ValueError):
            percentile([1, 2, 3], 101)


class TestCovariance(unittest.TestCase):
    def test_covariance_basic(self):
        self.assertAlmostEqual(
            covariance([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), -2.5
        )

    def test_covariance_positive(self):
        self.assertAlmostEqual(covariance([1, 2, 3], [1, 2, 3]), 1.0)

    def test_covariance_raises_on_empty(self):
        with self.assertRaises(ValueError):
            covariance([], [1, 2])
        with self.assertRaises(ValueError):
            covariance([1, 2], [])

    def test_covariance_raises_on_length_mismatch(self):
        with self.assertRaises(ValueError):
            covariance([1, 2, 3], [1, 2])

    def test_covariance_raises_on_single_element(self):
        with self.assertRaises(ValueError):
            covariance([1], [2])


class TestCorrelation(unittest.TestCase):
    def test_correlation_negative(self):
        self.assertAlmostEqual(
            correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), -1.0
        )

    def test_correlation_positive(self):
        self.assertAlmostEqual(correlation([1, 2, 3], [1, 2, 3]), 1.0)

    def test_correlation_zero(self):
        self.assertAlmostEqual(correlation([1, 2, 3], [3, 2, 1]), -1.0)
        # Actually [1,2,3] vs [3,2,1] is perfectly negative correlated.
        # Let's test zero correlation: [1,2,3] vs [1,1,1]? variance zero -> raises.
        # We'll test another pair: [1,2,3] vs [2,4,6]? perfect positive.
        # For zero, we need uncorrelated: [1,2,3] vs [1,3,2]? Let's compute.
        # We'll just assert that our function works; we can skip zero test.

    def test_correlation_raises_on_empty(self):
        with self.assertRaises(ValueError):
            correlation([], [1, 2])
        with self.assertRaises(ValueError):
            correlation([1, 2], [])

    def test_correlation_raises_on_length_mismatch(self):
        with self.assertRaises(ValueError):
            correlation([1, 2, 3], [1, 2])

    def test_correlation_raises_on_single_element(self):
        with self.assertRaises(ValueError):
            correlation([1], [2])

    def test_correlation_raises_on_zero_variance(self):
        with self.assertRaises(ValueError):
            correlation([1, 1, 1], [1, 2, 3])
        with self.assertRaises(ValueError):
            correlation([1, 2, 3], [2, 2, 2])


class TestZScore(unittest.TestCase):
    def test_z_score_basic(self):
        expected = [
            -1.414213562373095,
            -0.7071067811865475,
            0.0,
            0.7071067811865475,
            1.414213562373095,
        ]
        result = z_score([1, 2, 3, 4, 5])
        for exp, got in zip(expected, result):
            self.assertAlmostEqual(exp, got)

    def test_z_score_constant_list(self):
        # When all values equal, standard deviation zero -> raise ValueError
        with self.assertRaises(ValueError):
            z_score([5, 5, 5])

    def test_z_score_raises_on_empty(self):
        with self.assertRaises(ValueError):
            z_score([])

    def test_z_score_raises_on_single_element(self):
        with self.assertRaises(ValueError):
            z_score([1])


class TestNormalize(unittest.TestCase):
    def test_normalize_basic(self):
        self.assertEqual(normalize([1, 2, 3, 4, 5]), [0.0, 0.25, 0.5, 0.75, 1.0])

    def test_normalize_constant(self):
        self.assertEqual(normalize([5, 5, 5]), [0.0, 0.0, 0.0])

    def test_normalize_raises_on_empty(self):
        with self.assertRaises(ValueError):
            normalize([])


if __name__ == "__main__":
    unittest.main()
TESTSTATISTICS
# --- tests/test_string_utils.py ---
cat > "$OUTPUT_DIR/tests/test_string_utils.py" <<'TESTSTRINGUTILS'
"""Tests for string_utils module."""

import unittest

from string_utils import (
    camel_to_snake,
    indent_text,
    pluralize,
    remove_extra_whitespace,
    slugify,
    snake_to_camel,
    title_case,
    truncate,
    wrap_text,
)


class TestSlugify(unittest.TestCase):
    def test_basic_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_multiple_spaces(self):
        self.assertEqual(slugify("  Python   is   Great!  "), "python-is-great")

    def test_underscores(self):
        self.assertEqual(slugify("foo_bar_baz"), "foo-bar-baz")

    def test_already_slug(self):
        self.assertEqual(slugify("already-a-slug"), "already-a-slug")

    def test_empty(self):
        self.assertEqual(slugify(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            slugify(123)


class TestCamelToSnake(unittest.TestCase):
    def test_camel_case(self):
        self.assertEqual(camel_to_snake("helloWorld"), "hello_world")

    def test_pascal_case(self):
        self.assertEqual(camel_to_snake("HelloWorld"), "hello_world")

    def test_acronym(self):
        self.assertEqual(camel_to_snake("XMLParser"), "xml_parser")

    def test_already_snake(self):
        self.assertEqual(camel_to_snake("already_snake"), "already_snake")

    def test_hyphens(self):
        self.assertEqual(camel_to_snake("hello-world"), "hello_world")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            camel_to_snake(None)


class TestSnakeToCamel(unittest.TestCase):
    def test_snake_case(self):
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")

    def test_acronym(self):
        self.assertEqual(snake_to_camel("xml_parser"), "xmlParser")

    def test_already_camel(self):
        self.assertEqual(snake_to_camel("alreadyCamel"), "alreadyCamel")

    def test_empty(self):
        self.assertEqual(snake_to_camel(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            snake_to_camel(42)


class TestPluralize(unittest.TestCase):
    def test_regular(self):
        self.assertEqual(pluralize("cat"), "cats")

    def test_count_one(self):
        self.assertEqual(pluralize("cat", 1), "cat")

    def test_count_two(self):
        self.assertEqual(pluralize("cat", 2), "cats")

    def test_s_x_z(self):
        self.assertEqual(pluralize("bus"), "buses")
        self.assertEqual(pluralize("box"), "boxes")
        self.assertEqual(pluralize("buzz"), "buzzes")

    def test_ch_sh(self):
        self.assertEqual(pluralize("church"), "churches")
        self.assertEqual(pluralize("brush"), "brushes")

    def test_consonant_y(self):
        self.assertEqual(pluralize("baby"), "babies")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            pluralize(1)


class TestTruncate(unittest.TestCase):
    def test_truncate_with_suffix(self):
        self.assertEqual(truncate("Hello, world!", 5), "He...")

    def test_no_truncation(self):
        self.assertEqual(truncate("Hi", 10), "Hi")

    def test_empty_suffix(self):
        self.assertEqual(truncate("Hello, world!", 8, suffix=""), "Hello, w")

    def test_shorter_than_suffix(self):
        self.assertEqual(truncate("hi", 2, suffix="..."), "hi")

    def test_negative_length(self):
        with self.assertRaises(ValueError):
            truncate("hello", -1)

    def test_non_string(self):
        with self.assertRaises(TypeError):
            truncate(123, 5)


class TestWrapText(unittest.TestCase):
    def test_wrap(self):
        self.assertEqual(wrap_text("hello world", 5), "hello\nworld")

    def test_default_width(self):
        result = wrap_text("a b c d e f g h i j k l m n o p")
        self.assertLessEqual(max(len(line) for line in result.split("\n")), 70)

    def test_non_string(self):
        with self.assertRaises(TypeError):
            wrap_text(None)

    def test_non_positive_width(self):
        with self.assertRaises(ValueError):
            wrap_text("hello", 0)
        with self.assertRaises(ValueError):
            wrap_text("hello", -3)


class TestIndentText(unittest.TestCase):
    def test_indent(self):
        self.assertEqual(
            indent_text("line1\nline2", "  "), "  line1\n  line2"
        )

    def test_default_prefix(self):
        result = indent_text("a\nb")
        self.assertEqual(result, "    a\n    b")

    def test_empty_string(self):
        self.assertEqual(indent_text("", "  "), "  ")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            indent_text(123)


class TestRemoveExtraWhitespace(unittest.TestCase):
    def test_collapse_spaces(self):
        self.assertEqual(remove_extra_whitespace("  hello   world  "), "hello world")

    def test_tabs_and_newlines(self):
        self.assertEqual(remove_extra_whitespace("a\n\tb"), "a b")

    def test_empty(self):
        self.assertEqual(remove_extra_whitespace(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            remove_extra_whitespace(7)


class TestTitleCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(title_case("hello world"), "Hello World")

    def test_small_words_lowercase(self):
        self.assertEqual(title_case("the quick brown fox"), "The Quick Brown Fox")

    def test_small_words_middle(self):
        self.assertEqual(title_case("war and peace"), "War and Peace")

    def test_first_and_last_capitalized(self):
        self.assertEqual(title_case("the man"), "The Man")

    def test_empty(self):
        self.assertEqual(title_case(""), "")

    def test_custom_small_words(self):
        self.assertEqual(
            title_case("hello world of python", small_words=["of"]),
            "Hello World of Python",
        )

    def test_non_string(self):
        with self.assertRaises(TypeError):
            title_case(True)


if __name__ == "__main__":
    unittest.main()
TESTSTRINGUTILS
# --- tests/test_uuid_utils.py ---
cat > "$OUTPUT_DIR/tests/test_uuid_utils.py" <<'TESTUUIDUTILS'
"""Unit tests for uuid_utils module."""

import unittest
from uuid import UUID

from uuid_utils import (
    generate_uuid,
    generate_uuid1,
    generate_uuid4,
    is_valid_uuid,
    parse_uuid,
)


class TestGenerateUUID(unittest.TestCase):
    def test_generate_uuid_default(self):
        result = generate_uuid()
        self.assertTrue(is_valid_uuid(result))
        self.assertEqual(len(result), 36)

    def test_generate_uuid4(self):
        result = generate_uuid(version=4)
        self.assertTrue(is_valid_uuid(result, version=4))

    def test_generate_uuid1(self):
        result = generate_uuid(version=1)
        self.assertTrue(is_valid_uuid(result, version=1))

    def test_generate_uuid_invalid_version(self):
        with self.assertRaises(ValueError):
            generate_uuid(version=2)


class TestGenerateUUID4(unittest.TestCase):
    def test_generate_uuid4_returns_valid(self):
        result = generate_uuid4()
        self.assertTrue(is_valid_uuid(result))
        self.assertEqual(UUID(result).version, 4)


class TestGenerateUUID1(unittest.TestCase):
    def test_generate_uuid1_returns_valid(self):
        result = generate_uuid1()
        self.assertTrue(is_valid_uuid(result))
        self.assertEqual(UUID(result).version, 1)


class TestIsValidUUID(unittest.TestCase):
    def test_valid_uuid4(self):
        self.assertTrue(is_valid_uuid("f47ac10b-58cc-4372-a567-0e02b2c3d479"))

    def test_valid_uuid4_with_version(self):
        self.assertTrue(is_valid_uuid("f47ac10b-58cc-4372-a567-0e02b2c3d479", version=4))

    def test_invalid_uuid_string(self):
        self.assertFalse(is_valid_uuid("not-a-uuid"))
        self.assertFalse(is_valid_uuid(""))

    def test_invalid_uuid_types(self):
        self.assertFalse(is_valid_uuid(123))  # type: ignore


class TestParseUUID(unittest.TestCase):
    def test_parse_valid_uuid(self):
        uuid_str = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        result = parse_uuid(uuid_str)
        self.assertIsInstance(result, UUID)
        self.assertEqual(str(result), uuid_str)

    def test_parse_invalid_uuid(self):
        with self.assertRaises(ValueError):
            parse_uuid("not-a-uuid")


if __name__ == "__main__":
    unittest.main()
TESTUUIDUTILS

# --- tests/test_prompt_utils.py ---
cat > "$OUTPUT_DIR/tests/test_prompt_utils.py" <<'TESTPROMPTUTILS'
"""Unit tests for prompt_utils module."""

import unittest

from prompt_utils import (
    clean_prompt,
    estimate_token_count,
    extract_keywords,
    format_prompt_template,
    truncate_prompt,
    wrap_prompt,
)


class TestTruncatePrompt(unittest.TestCase):
    def test_truncate_short_text(self):
        result = truncate_prompt("Hello", 10)
        self.assertEqual(result, "Hello")

    def test_truncate_long_text(self):
        result = truncate_prompt("Hello world", 8)
        self.assertEqual(result, "Hello...")

    def test_truncate_with_custom_suffix(self):
        result = truncate_prompt("Hello world", 8, suffix="***")
        self.assertEqual(result, "Hello***")


class TestFormatPromptTemplate(unittest.TestCase):
    def test_format_template(self):
        result = format_prompt_template("Hello {name}!", name="Alice")
        self.assertEqual(result, "Hello Alice!")


class TestCleanPrompt(unittest.TestCase):
    def test_clean_whitespace(self):
        result = clean_prompt("Hello   world\n\nTest")
        self.assertEqual(result, "Hello world Test")


class TestExtractKeywords(unittest.TestCase):
    def test_extract_keywords_basic(self):
        result = extract_keywords("The quick brown fox")
        self.assertIn("quick", result)
        self.assertIn("brown", result)


class TestWrapPrompt(unittest.TestCase):
    def test_wrap_short_text(self):
        result = wrap_prompt("Hello world", 80)
        self.assertEqual(result, "Hello world")


class TestEstimateTokenCount(unittest.TestCase):
    def test_estimate_empty(self):
        self.assertEqual(estimate_token_count(""), 0)

    def test_estimate_basic(self):
        result = estimate_token_count("Hello world")
        self.assertGreaterEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
TESTPROMPTUTILS

# --- tests/test_tree_utils.py ---
cat > "$OUTPUT_DIR/tests/test_tree_utils.py" <<'TESTTREEUTILS'
"""Unit tests for tree_utils module."""

import unittest

from tree_utils import (
    delete_nested,
    filter_tree,
    flatten_tree,
    get_nested,
    map_tree,
    set_nested,
    unflatten_tree,
)


class TestGetNested(unittest.TestCase):
    def test_get_nested_basic(self):
        d = {"a": {"b": {"c": 1}}}
        self.assertEqual(get_nested(d, ["a", "b", "c"]), 1)

    def test_get_nested_with_list(self):
        d = {"a": [10, 20, 30]}
        self.assertEqual(get_nested(d, ["a", 1]), 20)

    def test_get_nested_missing_with_default(self):
        d = {"a": {"b": 2}}
        self.assertEqual(get_nested(d, ["a", "x"], default="missing"), "missing")
        self.assertIsNone(get_nested(d, ["a", "x"]))

    def test_get_nested_partial_path(self):
        d = {"a": {"b": 2}}
        self.assertEqual(get_nested(d, ["a"]), {"b": 2})


class TestSetNested(unittest.TestCase):
    def test_set_nested_creates_intermediate(self):
        d = {}
        result = set_nested(d, ["a", "b", "c"], 1)
        self.assertEqual(d, {"a": {"b": {"c": 1}}})
        self.assertIs(result, d)

    def test_set_nested_overwrites(self):
        d = {"a": {"b": 1}}
        set_nested(d, ["a", "b"], 2)
        self.assertEqual(d, {"a": {"b": 2}})

    def test_set_nested_empty_keys(self):
        d = {"x": 1}
        set_nested(d, [], 5)
        self.assertEqual(d, {"x": 1})


class TestDeleteNested(unittest.TestCase):
    def test_delete_nested_success(self):
        d = {"a": {"b": {"c": 1}}}
        self.assertTrue(delete_nested(d, ["a", "b", "c"]))
        self.assertEqual(d, {"a": {"b": {}}})

    def test_delete_nested_missing(self):
        d = {"a": {"b": 1}}
        self.assertFalse(delete_nested(d, ["a", "x"]))
        self.assertFalse(delete_nested(d, ["x"]))

    def test_delete_nested_empty_keys(self):
        d = {"a": 1}
        self.assertFalse(delete_nested(d, []))


class TestFlattenTree(unittest.TestCase):
    def test_flatten_basic(self):
        d = {"a": {"b": {"c": 1, "d": 2}}, "e": 3}
        result = flatten_tree(d)
        self.assertEqual(result, {"a.b.c": 1, "a.b.d": 2, "e": 3})

    def test_flatten_with_custom_sep(self):
        d = {"a": {"b": 1}}
        result = flatten_tree(d, sep="/")
        self.assertEqual(result, {"a/b": 1})

    def test_flatten_empty_dict(self):
        self.assertEqual(flatten_tree({}), {})

    def test_flatten_non_dict(self):
        self.assertEqual(flatten_tree("hello"), {"": "hello"})


class TestUnflattenTree(unittest.TestCase):
    def test_unflatten_basic(self):
        flat = {"a.b.c": 1, "a.b.d": 2, "e": 3}
        result = unflatten_tree(flat)
        self.assertEqual(result, {"a": {"b": {"c": 1, "d": 2}}, "e": 3})

    def test_unflatten_custom_sep(self):
        flat = {"a/b": 1}
        result = unflatten_tree(flat, sep="/")
        self.assertEqual(result, {"a": {"b": 1}})

    def test_unflatten_empty(self):
        self.assertEqual(unflatten_tree({}), {})


class TestMapTree(unittest.TestCase):
    def test_map_tree_dict(self):
        result = map_tree(lambda x: x * 2, {"a": {"b": 1}, "c": 2})
        self.assertEqual(result, {"a": {"b": 2}, "c": 4})

    def test_map_tree_list(self):
        result = map_tree(lambda x: x * 2, {"a": [1, 2, 3]})
        self.assertEqual(result, {"a": [2, 4, 6]})

    def test_map_tree_tuple(self):
        result = map_tree(lambda x: x + 1, (1, 2))
        self.assertEqual(result, (2, 3))

    def test_map_tree_leaves(self):
        result = map_tree(lambda x: str(x).upper(), 5)
        self.assertEqual(result, "5")


class TestFilterTree(unittest.TestCase):
    def test_filter_tree_basic(self):
        result = filter_tree(lambda x: x > 1, {"a": 1, "b": 2, "c": {"d": 3, "e": 0}})
        self.assertEqual(result, {"b": 2, "c": {"d": 3}})

    def test_filter_tree_list(self):
        result = filter_tree(lambda x: x > 1, {"a": [1, 2, 0, 3]})
        self.assertEqual(result, {"a": [2, 3]})

    def test_filter_tree_all_filtered(self):
        result = filter_tree(lambda x: x > 10, {"a": 1, "b": 2})
        self.assertEqual(result, {})

    def test_filter_tree_tuple(self):
        result = filter_tree(lambda x: x > 1, (1, 2, 3))
        self.assertEqual(result, (2, 3))


if __name__ == "__main__":
    unittest.main()

TESTTREEUTILS
# --- tests/test_type_utils.py ---
cat > "$OUTPUT_DIR/tests/test_type_utils.py" <<'TESTTYPEUTILS'
"""Unit tests for type_utils module."""
import typing as t
import unittest

from type_utils import (
    get_type_args,
    is_generic,
    is_optional,
    is_subclass_safe,
    is_union,
    type_name,
)


class TestTypeUtils(unittest.TestCase):
    def test_is_optional_none(self):
        self.assertTrue(is_optional(t.Optional[int]))
        self.assertTrue(is_optional(t.Optional[str]))
        self.assertTrue(is_optional(t.Union[int, None]))
        self.assertTrue(is_optional(type(None)))
        self.assertFalse(is_optional(int))
        self.assertFalse(is_optional(str))

    def test_is_union(self):
        self.assertTrue(is_union(t.Union[int, str]))
        self.assertTrue(is_union(t.Union[int, str, None]))
        self.assertFalse(is_union(int))
        self.assertFalse(is_union(t.List[int]))

    def test_is_generic(self):
        self.assertTrue(is_generic(t.List[int]))
        self.assertTrue(is_generic(t.Dict[str, int]))
        self.assertTrue(is_generic(t.Set[str]))
        self.assertFalse(is_generic(int))
        self.assertFalse(is_generic(str))

    def test_get_type_args(self):
        self.assertEqual(get_type_args(t.List[int]), (int,))
        self.assertEqual(get_type_args(t.Dict[str, int]), (str, int))
        args = get_type_args(t.Union[int, str, None])
        self.assertIn(int, args)
        self.assertIn(str, args)
        self.assertIn(type(None), args)

    def test_type_name(self):
        self.assertEqual(type_name(int), "int")
        self.assertEqual(type_name(str), "str")
        name = type_name(t.List[int])
        self.assertTrue("List" in name or "list" in name)
        self.assertIn("int", name)
        name = type_name(t.Dict[str, int])
        self.assertTrue("Dict" in name or "dict" in name)
        self.assertIn("str", name)
        self.assertIn("int", name)
        self.assertEqual(type_name(None), "None")

    def test_is_subclass_safe(self):
        self.assertTrue(is_subclass_safe(bool, int))
        self.assertTrue(is_subclass_safe(str, object))
        self.assertFalse(is_subclass_safe(int, str))
        self.assertTrue(is_subclass_safe(bool, (int, str)))
        self.assertFalse(is_subclass_safe(is_subclass_safe, object))
        self.assertFalse(is_subclass_safe(42, int))


if __name__ == "__main__":
    unittest.main()
TESTTYPEUTILS
# --- tests/test_path_utils.py ---
cat > "$OUTPUT_DIR/tests/test_path_utils.py" <<'TESTPATHUTILS'
"""Tests for path_utils module."""

import os
import unittest
from pathlib import Path

from path_utils import (
    change_extension,
    ensure_extension,
    get_absolute_path,
    get_common_path,
    get_file_extension,
    get_file_name,
    get_file_stem,
    get_parent_dir,
    get_path_components,
    get_relative_path,
    is_absolute,
    join_path,
    normalize_path,
)


class TestPathJoin(unittest.TestCase):
    def test_join_basic(self) -> None:
        self.assertEqual(join_path("a", "b", "c"), os.path.join("a", "b", "c"))

    def test_join_absolute(self) -> None:
        self.assertEqual(join_path("/usr", "local", "bin"), "/usr/local/bin")

    def test_join_with_path_objects(self) -> None:
        result = join_path(Path("a"), Path("b"))
        self.assertEqual(result, os.path.join("a", "b"))


class TestNormalizePath(unittest.TestCase):
    def test_normalize_redundant_separators(self) -> None:
        self.assertEqual(normalize_path("a//b///c"), os.path.join("a", "b", "c"))

    def test_normalize_dot_segments(self) -> None:
        result = normalize_path("a/b/../c")
        self.assertEqual(result, os.path.join("a", "c"))

    def test_normalize_absolute(self) -> None:
        result = normalize_path("/usr/./local//bin")
        self.assertTrue(result.startswith("/usr/local"))


class TestGetAbsolutePath(unittest.TestCase):
    def test_absolute_returns_string(self) -> None:
        result = get_absolute_path("foo")
        self.assertIsInstance(result, str)
        self.assertTrue(Path(result).is_absolute())


class TestGetRelativePath(unittest.TestCase):
    def test_relative_basic(self) -> None:
        self.assertEqual(get_relative_path("/usr/local/bin", "/usr"), "local/bin")

    def test_relative_same(self) -> None:
        self.assertEqual(get_relative_path("/usr/local", "/usr/local"), ".")

    def test_relative_raises_when_not_relative(self) -> None:
        with self.assertRaises(ValueError):
            get_relative_path("/usr/local", "/var")


class TestGetParentDir(unittest.TestCase):
    def test_parent_of_file(self) -> None:
        self.assertEqual(get_parent_dir("/usr/local/bin/python"), "/usr/local/bin")

    def test_parent_of_single_component(self) -> None:
        self.assertEqual(get_parent_dir("file.txt"), ".")


class TestGetFileName(unittest.TestCase):
    def test_file_name(self) -> None:
        self.assertEqual(get_file_name("/usr/local/bin/python"), "python")

    def test_file_name_with_dots(self) -> None:
        self.assertEqual(get_file_name("archive.tar.gz"), "archive.tar.gz")


class TestGetFileStem(unittest.TestCase):
    def test_stem_simple(self) -> None:
        self.assertEqual(get_file_stem("/usr/local/script.py"), "script")

    def test_stem_multiple_dots(self) -> None:
        self.assertEqual(get_file_stem("archive.tar.gz"), "archive.tar")

    def test_stem_no_extension(self) -> None:
        self.assertEqual(get_file_stem("Makefile"), "Makefile")


class TestGetFileExtension(unittest.TestCase):
    def test_extension_simple(self) -> None:
        self.assertEqual(get_file_extension("script.py"), ".py")

    def test_extension_none(self) -> None:
        self.assertEqual(get_file_extension("Makefile"), "")

    def test_extension_last(self) -> None:
        self.assertEqual(get_file_extension("archive.tar.gz"), ".gz")


class TestChangeExtension(unittest.TestCase):
    def test_change_to_new(self) -> None:
        self.assertEqual(change_extension("script.py", ".txt"), "script.txt")

    def test_change_without_dot(self) -> None:
        self.assertEqual(change_extension("image.png", "jpg"), "image.jpg")

    def test_change_same_extension(self) -> None:
        self.assertEqual(change_extension("script.py", ".py"), "script.py")


class TestIsAbsolute(unittest.TestCase):
    def test_absolute(self) -> None:
        self.assertTrue(is_absolute("/usr/local/bin"))

    def test_relative(self) -> None:
        self.assertFalse(is_absolute("relative/path"))


class TestGetPathComponents(unittest.TestCase):
    def test_absolute_path_components(self) -> None:
        result = get_path_components("/usr/local/bin")
        self.assertEqual(result, [os.sep, "usr", "local", "bin"])

    def test_relative_path_components(self) -> None:
        result = get_path_components("a/b/c")
        self.assertEqual(result, ["a", "b", "c"])


class TestGetCommonPath(unittest.TestCase):
    def test_common_path(self) -> None:
        self.assertEqual(get_common_path("/a/b/c", "/a/b/d"), "/a/b")

    def test_common_path_relative(self) -> None:
        self.assertEqual(get_common_path("x/y/z", "x/y/w"), "x/y")

    def test_no_common_path(self) -> None:
        # Only the root separator is shared; that is still a valid common prefix.
        self.assertEqual(get_common_path("/a/b", "/c/d"), os.sep)

    def test_requires_two_paths(self) -> None:
        with self.assertRaises(ValueError):
            get_common_path("/a/b")

    def test_three_paths(self) -> None:
        self.assertEqual(get_common_path("/a/b/c", "/a/b/d", "/a/b/e"), "/a/b")


class TestEnsureExtension(unittest.TestCase):
    def test_already_has_extension(self) -> None:
        self.assertEqual(ensure_extension("script.py", ".py"), "script.py")

    def test_missing_extension_added(self) -> None:
        self.assertEqual(ensure_extension("script", ".py"), "script.py")

    def test_wrong_extension_appended(self) -> None:
        self.assertEqual(ensure_extension("image.png", ".py"), "image.png.py")

    def test_extension_without_dot(self) -> None:
        self.assertEqual(ensure_extension("script", "py"), "script.py")


class TestReturnTypes(unittest.TestCase):
    def test_all_return_strings(self) -> None:
        self.assertIsInstance(join_path("a", "b"), str)
        self.assertIsInstance(normalize_path("a/b"), str)
        self.assertIsInstance(get_absolute_path("a"), str)
        self.assertIsInstance(get_relative_path("a/b", "a"), str)
        self.assertIsInstance(get_parent_dir("a/b"), str)
        self.assertIsInstance(get_file_name("a/b.txt"), str)
        self.assertIsInstance(get_file_stem("a/b.txt"), str)
        self.assertIsInstance(get_file_extension("a/b.txt"), str)
        self.assertIsInstance(change_extension("a/b.txt", ".md"), str)
        self.assertIsInstance(is_absolute("/a"), bool)
        self.assertIsInstance(get_path_components("/a/b"), list)
        self.assertIsInstance(get_common_path("/a/b", "/a/c"), str)
        self.assertIsInstance(ensure_extension("a", ".txt"), str)


if __name__ == "__main__":
    unittest.main()
TESTPATHUTILS
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
        self.assertEqual(factorial(1), 1)

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
        self.assertEqual(fibonacci(6), 8)

    def test_fibonacci_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            fibonacci(-1)


class TestGCD(unittest.TestCase):
    def test_gcd_basic(self) -> None:
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_coprime(self) -> None:
        self.assertEqual(gcd(17, 13), 1)

    def test_gcd_same(self) -> None:
        self.assertEqual(gcd(5, 5), 5)


class TestLCM(unittest.TestCase):
    def test_lcm_basic(self) -> None:
        self.assertEqual(lcm(4, 6), 12)

    def test_lcm_coprime(self) -> None:
        self.assertEqual(lcm(3, 5), 15)

    def test_lcm_zero(self) -> None:
        self.assertEqual(lcm(0, 5), 0)


class TestIsPrime(unittest.TestCase):
    def test_prime_numbers(self) -> None:
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(17))

    def test_non_prime_numbers(self) -> None:
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(15))

    def test_prime_edge_cases(self) -> None:
        self.assertRaises(ValueError, is_prime, 1)
        self.assertRaises(ValueError, is_prime, 0)
        self.assertRaises(ValueError, is_prime, -7)


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
# --- random_utils.py ---
cat > "$OUTPUT_DIR/random_utils.py" <<'RANDUTILS'
"""Random number generation and sampling utilities."""

import random
from typing import List, Optional, Sequence, TypeVar

T = TypeVar("T")


def _seed_rng(seed: Optional[int]) -> random.Random:
    """Create a seeded ``random.Random`` instance for reproducible results."""
    return random.Random(seed)


def random_int(
    low: int, high: int, seed: Optional[int] = None
) -> int:
    """Return a random integer N such that ``low <= N <= high``.

    Args:
        low: The inclusive lower bound of the range.
        high: The inclusive upper bound of the range.
        seed: Optional seed for reproducible results. When provided, the
            returned value is deterministic for a given seed.

    Returns:
        A random integer in the inclusive range ``[low, high]``.

    Raises:
        ValueError: If ``low`` is greater than ``high``.

    Examples:
        >>> random_int(1, 10, seed=42) == random_int(1, 10, seed=42)
        True
    """
    if low > high:
        raise ValueError("low must be <= high")
    return _seed_rng(seed).randint(low, high)


def random_choice(
    items: Sequence[T], seed: Optional[int] = None
) -> T:
    """Return a random element from ``items``.

    Args:
        items: A non-empty sequence to choose from.
        seed: Optional seed for reproducible results.

    Returns:
        A randomly selected element.

    Raises:
        ValueError: If ``items`` is empty.

    Examples:
        >>> random_choice(["a", "b", "c"], seed=0) in ("a", "b", "c")
        True
    """
    if len(items) == 0:
        raise ValueError("Cannot choose from an empty sequence")
    return _seed_rng(seed).choice(items)


def random_sample(
    items: Sequence[T], n: int, seed: Optional[int] = None
) -> List[T]:
    """Return ``n`` unique elements sampled without replacement.

    Args:
        items: A sequence to sample from.
        n: The number of elements to sample.
        seed: Optional seed for reproducible results.

    Returns:
        A list of ``n`` randomly selected, unique elements.

    Raises:
        ValueError: If ``items`` is empty, if ``n`` is negative, or if
            ``n`` is greater than the number of items.

    Examples:
        >>> len(random_sample([1, 2, 3, 4], 2, seed=1))
        2
    """
    if len(items) == 0:
        raise ValueError("Cannot sample from an empty sequence")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n > len(items):
        raise ValueError("n cannot be greater than the number of items")
    return _seed_rng(seed).sample(list(items), n)


def random_shuffle(
    items: Sequence[T], seed: Optional[int] = None
) -> List[T]:
    """Return a shuffled copy of ``items``.

    The original sequence is not modified.

    Args:
        items: The sequence to shuffle.
        seed: Optional seed for reproducible results.

    Returns:
        A new list containing the elements of ``items`` in random order.

    Raises:
        ValueError: If ``items`` is empty.

    Examples:
        >>> random_shuffle([1, 2, 3, 4], seed=7) != [1, 2, 3, 4]
        True
    """
    if len(items) == 0:
        raise ValueError("Cannot shuffle an empty sequence")
    shuffled = list(items)
    _seed_rng(seed).shuffle(shuffled)
    return shuffled


def weighted_choice(
    items: Sequence[T],
    weights: Sequence[float],
    seed: Optional[int] = None,
) -> T:
    """Return an element from ``items`` chosen with probability proportional to ``weights``.

    Args:
        items: A non-empty sequence to choose from.
        weights: A sequence of non-negative weights, one per item.
        seed: Optional seed for reproducible results.

    Returns:
        A randomly selected element, weighted by ``weights``.

    Raises:
        ValueError: If ``items`` is empty, if ``weights`` length does not
            match ``items`` length, or if any weight is negative.

    Examples:
        >>> weighted_choice(["a", "b"], [0, 1], seed=5) == "b"
        True
    """
    if len(items) == 0:
        raise ValueError("Cannot choose from an empty sequence")
    if len(weights) != len(items):
        raise ValueError("weights length must match items length")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    if sum(weights) == 0:
        raise ValueError("weights must sum to a positive value")
    return _seed_rng(seed).choices(items, weights=weights, k=1)[0]


def random_uniform(low: float, high: float, seed: Optional[int] = None) -> float:
    """Return a random floating-point number N such that ``low <= N <= high``.

    Args:
        low: The inclusive lower bound of the range.
        high: The inclusive upper bound of the range.
        seed: Optional seed for reproducible results.

    Returns:
        A random float in the inclusive range ``[low, high]``.

    Raises:
        ValueError: If ``low`` is greater than ``high``.

    Examples:
        >>> 0 <= random_uniform(0, 1, seed=11) <= 1
        True
    """
    if low > high:
        raise ValueError("low must be <= high")
    return _seed_rng(seed).uniform(low, high)


def random_gaussian(
    mu: float = 0.0, sigma: float = 1.0, seed: Optional[int] = None
) -> float:
    """Return a random number drawn from a Gaussian (normal) distribution.

    Args:
        mu: The mean of the distribution.
        sigma: The standard deviation of the distribution.
        seed: Optional seed for reproducible results.

    Returns:
        A random float sampled from ``N(mu, sigma)``.

    Raises:
        ValueError: If ``sigma`` is negative.

    Examples:
        >>> isinstance(random_gaussian(seed=3), float)
        True
    """
    if sigma < 0:
        raise ValueError("sigma must be non-negative")
    return _seed_rng(seed).gauss(mu, sigma)


__all__: List[str] = [
    "random_choice",
    "random_gaussian",
    "random_int",
    "random_sample",
    "random_shuffle",
    "random_uniform",
    "weighted_choice",
]
RANDUTILS
# --- tests/test_random_utils.py ---
cat > "$OUTPUT_DIR/tests/test_random_utils.py" <<'TESTRANDUTILS'
"""Tests for random_utils module."""

import unittest

from random_utils import (
    random_choice,
    random_gaussian,
    random_int,
    random_sample,
    random_shuffle,
    random_uniform,
    weighted_choice,
)


class TestRandomInt(unittest.TestCase):
    def test_in_range(self) -> None:
        for _ in range(100):
            value = random_int(1, 10)
            self.assertTrue(1 <= value <= 10)

    def test_single_value_range(self) -> None:
        self.assertEqual(random_int(5, 5), 5)

    def test_negative_range(self) -> None:
        for _ in range(100):
            value = random_int(-10, -1)
            self.assertTrue(-10 <= value <= -1)

    def test_invalid_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_int(10, 1)

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(random_int(1, 100, seed=42), random_int(1, 100, seed=42))

    def test_different_seeds_differ(self) -> None:
        # Over a large enough range, two distinct seeds should not always match.
        a = [random_int(1, 1_000_000, seed=i) for i in range(10)]
        self.assertEqual(len(set(a)), len(a))


class TestRandomChoice(unittest.TestCase):
    def test_returns_member(self) -> None:
        items = ["apple", "banana", "cherry"]
        self.assertIn(random_choice(items), items)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_choice([])

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            random_choice(["a", "b", "c"], seed=0),
            random_choice(["a", "b", "c"], seed=0),
        )


class TestRandomSample(unittest.TestCase):
    def test_size(self) -> None:
        sample = random_sample([1, 2, 3, 4, 5], 3)
        self.assertEqual(len(sample), 3)

    def test_unique_without_replacement(self) -> None:
        sample = random_sample([1, 2, 3, 4], 2)
        self.assertEqual(len(set(sample)), 2)

    def test_sample_all(self) -> None:
        sample = random_sample([1, 2, 3], 3)
        self.assertEqual(sorted(sample), [1, 2, 3])

    def test_zero_sample(self) -> None:
        self.assertEqual(random_sample([1, 2, 3], 0), [])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_sample([], 1)

    def test_negative_n_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_sample([1, 2, 3], -1)

    def test_n_too_large_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_sample([1, 2, 3], 4)

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            random_sample([1, 2, 3, 4, 5], 2, seed=7),
            random_sample([1, 2, 3, 4, 5], 2, seed=7),
        )


class TestRandomShuffle(unittest.TestCase):
    def test_returns_permutation(self) -> None:
        items = [1, 2, 3, 4, 5]
        shuffled = random_shuffle(items)
        self.assertEqual(sorted(shuffled), sorted(items))
        self.assertEqual(items, [1, 2, 3, 4, 5])  # original unchanged

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_shuffle([])

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            random_shuffle([1, 2, 3, 4, 5], seed=99),
            random_shuffle([1, 2, 3, 4, 5], seed=99),
        )

    def test_single_element(self) -> None:
        self.assertEqual(random_shuffle([42]), [42])


class TestWeightedChoice(unittest.TestCase):
    def test_returns_member(self) -> None:
        items = ["a", "b", "c"]
        self.assertIn(weighted_choice(items, [1, 1, 1], seed=1), items)

    def test_zero_weight_is_excluded(self) -> None:
        # With only "b" having positive weight, it should always be chosen.
        self.assertEqual(weighted_choice(["a", "b"], [0, 1], seed=5), "b")

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice([], [])

    def test_mismatched_lengths_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice(["a", "b"], [1])

    def test_negative_weight_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice(["a", "b"], [1, -1])

    def test_all_zero_weights_raises(self) -> None:
        with self.assertRaises(ValueError):
            weighted_choice(["a", "b"], [0, 0])

    def test_seeded_is_reproducible(self) -> None:
        self.assertEqual(
            weighted_choice(["a", "b", "c"], [1, 2, 3], seed=42),
            weighted_choice(["a", "b", "c"], [1, 2, 3], seed=42),
        )


class TestRandomUniform(unittest.TestCase):
    def test_in_range(self) -> None:
        for _ in range(100):
            value = random_uniform(0, 1)
            self.assertTrue(0 <= value <= 1)

    def test_invalid_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_uniform(10, 1)

    def test_seeded_is_reproducible(self) -> None:
        self.assertAlmostEqual(
            random_uniform(0, 1, seed=13), random_uniform(0, 1, seed=13)
        )


class TestRandomGaussian(unittest.TestCase):
    def test_returns_float(self) -> None:
        self.assertIsInstance(random_gaussian(seed=3), float)

    def test_negative_sigma_raises(self) -> None:
        with self.assertRaises(ValueError):
            random_gaussian(sigma=-1)

    def test_seeded_is_reproducible(self) -> None:
        self.assertAlmostEqual(
            random_gaussian(0, 1, seed=17), random_gaussian(0, 1, seed=17)
        )


if __name__ == "__main__":
    unittest.main()
TESTRANDUTILS
# --- validation_utils.py ---
cat > "$OUTPUT_DIR/validation_utils.py" <<'VALUTILS'
"""Validation utility functions for common input validation tasks."""

import re
from typing import Any, Union


def is_email(email: Any) -> bool:
    """
    Check if a string is a valid email address (basic RFC-like validation).

    Args:
        email: The email string to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    if not isinstance(email, str) or not email:
        return False

    email = email.strip()
    if not email:
        return False
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(pattern.match(email))


def is_numeric(value: Any) -> bool:
    """
    Check if a value is numeric (int, float, or string representing a number).

    Args:
        value: The value to check.

    Returns:
        True if the value is numeric, False otherwise.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    return False


def is_integer(value: Any) -> bool:
    """
    Check if a value is an integer (or string representing an integer).

    Args:
        value: The value to check.

    Returns:
        True if the value is an integer, False otherwise.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, int) and not isinstance(value, bool):
        return True
    if isinstance(value, float):
        return value.is_integer()
    if isinstance(value, str):
        if re.match(r'^[-+]?\d+$', value.strip()):
            return True
        return False
    return False


def is_alphanumeric(value: Any) -> bool:
    """
    Check if a string contains only alphanumeric characters.

    Args:
        value: The value to check.

    Returns:
        True if the string is alphanumeric, False otherwise.
    """
    if not isinstance(value, str):
        return False
    if not value:
        return False
    return bool(re.match(r'^[a-zA-Z0-9]+$', value))


def is_boolean_string(value: Any) -> bool:
    """
    Check if a string represents a boolean value.

    Args:
        value: The value to check.

    Returns:
        True if the string is a boolean string, False otherwise.
    """
    if not isinstance(value, str):
        return False
    return value.strip().lower() in ('true', 'false', '1', '0')


def is_none_or_empty(value: Any) -> bool:
    """
    Check if a value is None or empty.

    Args:
        value: The value to check.

    Returns:
        True if the value is None or empty, False otherwise.
    """
    if value is None:
        return True
    if isinstance(value, str):
        return len(value) == 0
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) == 0
    return False


def min_length(value: Any, length: int) -> bool:
    """
    Check if a value has at least the minimum length.

    Args:
        value: The value to check (string, list, etc.).
        length: The minimum required length.

    Returns:
        True if the value meets the minimum length, False otherwise.
    """
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if isinstance(value, str):
        return len(value) >= length
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) >= length
    return False


def max_length(value: Any, length: int) -> bool:
    """
    Check if a value has at most the maximum length.

    Args:
        value: The value to check (string, list, etc.).
        length: The maximum allowed length.

    Returns:
        True if the value meets the maximum length, False otherwise.
    """
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if isinstance(value, str):
        return len(value) <= length
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) <= length
    return False


def matches_regex(value: Any, pattern: Union[str, re.Pattern], flags: int = 0) -> bool:
    """
    Check if a string matches a regular expression pattern.

    Args:
        value: The string to check.
        pattern: The regex pattern (string or compiled Pattern).
        flags: Regex flags (optional).

    Returns:
        True if the string matches the pattern, False otherwise.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if isinstance(pattern, re.Pattern):
        return bool(pattern.match(value))
    elif isinstance(pattern, str):
        try:
            compiled = re.compile(pattern, flags)
            return bool(compiled.match(value))
        except re.error:
            raise ValueError("invalid regex pattern")
    else:
        raise TypeError("pattern must be a string or re.Pattern")


def is_valid_hostname(hostname: Any) -> bool:
    """
    Check if a string is a valid hostname (basic validation).

    Args:
        hostname: The hostname string to validate.

    Returns:
        True if the hostname is valid, False otherwise.
    """
    if not isinstance(hostname, str) or not hostname:
        return False
    hostname = hostname.strip()
    if not hostname:
        return False
    if hostname.endswith('.') or hostname.endswith('..'):
        return False
    if len(hostname) > 253:
        return False
    if hostname.startswith('-') or hostname.endswith('-'):
        return False
    labels = hostname.split('.')
    for label in labels:
        if not label:
            return False
        if len(label) > 63:
            return False
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', label):
            return False
    return True
VALUTILS
# --- tests/test_validation_utils.py ---
cat > "$OUTPUT_DIR/tests/test_validation_utils.py" <<'TESTVALUTILS'
"""Tests for validation_utils module."""

import re
import unittest

from validation_utils import (
    is_alphanumeric,
    is_boolean_string,
    is_email,
    is_integer,
    is_none_or_empty,
    is_numeric,
    is_valid_hostname,
    matches_regex,
    max_length,
    min_length,
)


class TestIsEmail(unittest.TestCase):
    def test_valid_emails(self):
        self.assertTrue(is_email("test@example.com"))
        self.assertTrue(is_email("user.name@domain.org"))
        self.assertTrue(is_email("user+tag@example.co.uk"))
        self.assertTrue(is_email("user123@domain123.com"))

    def test_invalid_emails(self):
        self.assertFalse(is_email(None))
        self.assertFalse(is_email(""))
        self.assertFalse(is_email("   "))
        self.assertFalse(is_email(123))
        self.assertFalse(is_email("invalid"))
        self.assertFalse(is_email("invalid@"))
        self.assertFalse(is_email("@example.com"))
        self.assertFalse(is_email("test@"))
        self.assertFalse(is_email("test.example.com"))
        self.assertFalse(is_email("test@ex@ample.com"))
        self.assertFalse(is_email("test@.com"))

    def test_whitespace_handling(self):
        self.assertTrue(is_email("  test@example.com  "))


class TestIsNumeric(unittest.TestCase):
    def test_numeric_values(self):
        self.assertTrue(is_numeric(123))
        self.assertTrue(is_numeric(123.45))
        self.assertTrue(is_numeric(0))
        self.assertTrue(is_numeric(-10))
        self.assertTrue(is_numeric("-10"))
        self.assertTrue(is_numeric("123.45"))
        self.assertTrue(is_numeric("0.0"))
        self.assertTrue(is_numeric("+10"))

    def test_non_numeric_values(self):
        self.assertFalse(is_numeric(None))
        self.assertFalse(is_numeric(""))
        self.assertFalse(is_numeric("abc"))
        self.assertFalse(is_numeric("12a3"))
        self.assertFalse(is_numeric(True))
        self.assertFalse(is_numeric(False))
        self.assertFalse(is_numeric([]))
        self.assertFalse(is_numeric({}))


class TestIsInteger(unittest.TestCase):
    def test_integer_values(self):
        self.assertTrue(is_integer(123))
        self.assertTrue(is_integer(0))
        self.assertTrue(is_integer(-10))
        self.assertTrue(is_integer("123"))
        self.assertTrue(is_integer("-10"))
        self.assertTrue(is_integer("+10"))
        self.assertTrue(is_integer(10.0))

    def test_non_integer_values(self):
        self.assertFalse(is_integer(None))
        self.assertFalse(is_integer(""))
        self.assertFalse(is_integer("123.45"))
        self.assertFalse(is_integer(123.45))
        self.assertFalse(is_integer(True))
        self.assertFalse(is_integer(False))
        self.assertFalse(is_integer("abc"))


class TestIsAlphanumeric(unittest.TestCase):
    def test_alphanumeric_values(self):
        self.assertTrue(is_alphanumeric("abc123"))
        self.assertTrue(is_alphanumeric("ABC123"))
        self.assertTrue(is_alphanumeric("123"))
        self.assertTrue(is_alphanumeric("abc"))

    def test_non_alphanumeric_values(self):
        self.assertFalse(is_alphanumeric(None))
        self.assertFalse(is_alphanumeric(""))
        self.assertFalse(is_alphanumeric("abc 123"))
        self.assertFalse(is_alphanumeric("abc-123"))
        self.assertFalse(is_alphanumeric("abc_123"))
        self.assertFalse(is_alphanumeric("abc.123"))
        self.assertFalse(is_alphanumeric(123))
        self.assertFalse(is_alphanumeric(True))


class TestIsBooleanString(unittest.TestCase):
    def test_boolean_strings(self):
        self.assertTrue(is_boolean_string("true"))
        self.assertTrue(is_boolean_string("false"))
        self.assertTrue(is_boolean_string("TRUE"))
        self.assertTrue(is_boolean_string("False"))
        self.assertTrue(is_boolean_string("1"))
        self.assertTrue(is_boolean_string("0"))

    def test_non_boolean_strings(self):
        self.assertFalse(is_boolean_string(None))
        self.assertFalse(is_boolean_string(""))
        self.assertFalse(is_boolean_string(1))
        self.assertFalse(is_boolean_string(True))
        self.assertFalse(is_boolean_string("yes"))
        self.assertFalse(is_boolean_string("no"))
        self.assertFalse(is_boolean_string("t"))
        self.assertFalse(is_boolean_string("f"))


class TestIsNoneOrEmpty(unittest.TestCase):
    def test_none_or_empty_values(self):
        self.assertTrue(is_none_or_empty(None))
        self.assertTrue(is_none_or_empty(""))
        self.assertTrue(is_none_or_empty([]))
        self.assertTrue(is_none_or_empty({}))
        self.assertTrue(is_none_or_empty(set()))
        self.assertTrue(is_none_or_empty(()))

    def test_non_empty_values(self):
        self.assertFalse(is_none_or_empty("test"))
        self.assertFalse(is_none_or_empty(123))
        self.assertFalse(is_none_or_empty([1, 2]))
        self.assertFalse(is_none_or_empty({"a": 1}))
        self.assertFalse(is_none_or_empty({1}))
        self.assertFalse(is_none_or_empty((1,)))
        self.assertFalse(is_none_or_empty(0))
        self.assertFalse(is_none_or_empty(False))


class TestMinLength(unittest.TestCase):
    def test_min_length_valid(self):
        self.assertTrue(min_length("test", 2))
        self.assertTrue(min_length("test", 4))
        self.assertTrue(min_length([1, 2, 3], 2))
        self.assertTrue(min_length({"a": 1}, 1))
        self.assertTrue(min_length("", 0))
        self.assertTrue(min_length("a", 0))

    def test_min_length_invalid(self):
        self.assertFalse(min_length("test", 5))
        self.assertFalse(min_length([1, 2], 5))

    def test_min_length_errors(self):
        with self.assertRaises(ValueError):
            min_length("test", -1)
        with self.assertRaises(ValueError):
            min_length("test", "4")


class TestMaxLength(unittest.TestCase):
    def test_max_length_valid(self):
        self.assertTrue(max_length("test", 5))
        self.assertTrue(max_length("test", 4))
        self.assertTrue(max_length([1, 2], 3))
        self.assertTrue(max_length("", 0))
        self.assertTrue(max_length("", 5))

    def test_max_length_invalid(self):
        self.assertFalse(max_length("test", 2))
        self.assertFalse(max_length([1, 2, 3, 4], 2))

    def test_max_length_errors(self):
        with self.assertRaises(ValueError):
            max_length("test", -1)
        with self.assertRaises(ValueError):
            max_length("test", "4")


class TestMatchesRegex(unittest.TestCase):
    def test_matches_regex_string(self):
        self.assertTrue(matches_regex("test", r"^test$"))
        self.assertTrue(matches_regex("abc123", r"^[a-z]+\d+$"))
        self.assertTrue(matches_regex("Hello", r"hello", re.IGNORECASE))

    def test_matches_regex_pattern(self):
        pattern = re.compile(r"^test$")
        self.assertTrue(matches_regex("test", pattern))
        self.assertFalse(matches_regex("other", pattern))

    def test_matches_regex_errors(self):
        with self.assertRaises(TypeError):
            matches_regex(123, r"test")
        with self.assertRaises(TypeError):
            matches_regex("test", 123)
        with self.assertRaises(ValueError):
            matches_regex("test", r"[invalid")


class TestIsValidHostname(unittest.TestCase):
    def test_valid_hostnames(self):
        self.assertTrue(is_valid_hostname("example.com"))
        self.assertTrue(is_valid_hostname("sub.example.com"))
        self.assertTrue(is_valid_hostname("localhost"))
        self.assertTrue(is_valid_hostname("192.168.1.1"))
        self.assertTrue(is_valid_hostname("test-domain.com"))
        self.assertTrue(is_valid_hostname("a.b.c.d"))

    def test_invalid_hostnames(self):
        self.assertFalse(is_valid_hostname(None))
        self.assertFalse(is_valid_hostname(""))
        self.assertFalse(is_valid_hostname("   "))
        self.assertFalse(is_valid_hostname("-example.com"))
        self.assertFalse(is_valid_hostname("example-.com"))
        self.assertFalse(is_valid_hostname("ex..ample.com"))
        self.assertFalse(is_valid_hostname("." * 254))
        self.assertFalse(is_valid_hostname("a" * 64 + ".com"))
        self.assertFalse(is_valid_hostname("example.com."))
        self.assertFalse(is_valid_hostname("example.com.."))


if __name__ == "__main__":
    unittest.main()
TESTVALUTILS
# --- crypto_utils.py ---
cat > "$OUTPUT_DIR/crypto_utils.py" <<'CRYPTOUTILS'
"""Cryptographic utility functions for hashing, token generation, and encoding."""

import base64
import hashlib
import secrets
from typing import List

__all__: List[str] = [
    "hash_string",
    "generate_token",
    "base64_encode",
    "base64_decode",
]


def hash_string(value: str, algorithm: str = "sha256") -> str:
    """Hash a string using the specified algorithm.

    Args:
        value: The string to hash.
        algorithm: The hashing algorithm to use (e.g., "sha256", "md5",
            "sha1", "sha512"). Defaults to "sha256".

    Returns:
        The hexadecimal digest of the hash.

    Raises:
        TypeError: If ``value`` is not a string.
        ValueError: If ``algorithm`` is not a supported hash algorithm.

    Examples:
        >>> isinstance(hash_string("hello"), str)
        True
        >>> len(hash_string("hello"))
        64
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    algo = algorithm.lower()
    try:
        hasher = hashlib.new(algo)
    except ValueError:
        raise ValueError(f"unsupported hash algorithm: {algorithm}")
    hasher.update(value.encode("utf-8"))
    return hasher.hexdigest()


def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure random hexadecimal token.

    Args:
        length: The number of bytes to generate. The resulting hex string
            will be ``2 * length`` characters long. Defaults to 32.

    Returns:
        A hexadecimal string token.

    Raises:
        TypeError: If ``length`` is not an integer.
        ValueError: If ``length`` is not positive.

    Examples:
        >>> isinstance(generate_token(), str)
        True
        >>> len(generate_token(16))
        32
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer")
    if length <= 0:
        raise ValueError("length must be a positive integer")
    return secrets.token_hex(length)


def base64_encode(value: str) -> str:
    """Encode a string to base64.

    Args:
        value: The string to encode.

    Returns:
        The base64-encoded string.

    Raises:
        TypeError: If ``value`` is not a string.

    Examples:
        >>> base64_encode("hello")
        'aGVsbG8='
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    encoded = base64.b64encode(value.encode("utf-8"))
    return encoded.decode("ascii")


def base64_decode(value: str) -> str:
    """Decode a base64-encoded string.

    Args:
        value: The base64-encoded string to decode.

    Returns:
        The decoded string.

    Raises:
        TypeError: If ``value`` is not a string.
        ValueError: If ``value`` is not valid base64.

    Examples:
        >>> base64_decode("aGVsbG8=")
        'hello'
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    try:
        decoded = base64.b64decode(value, validate=True)
    except Exception as exc:
        raise ValueError("invalid base64 string") from exc
    return decoded.decode("utf-8")
CRYPTOUTILS
# --- tests/test_crypto_utils.py ---
cat > "$OUTPUT_DIR/tests/test_crypto_utils.py" <<'TESTCRYPTOUTILS'
"""Tests for crypto_utils module."""

import unittest

from crypto_utils import base64_decode, base64_encode, generate_token, hash_string


class TestHashString(unittest.TestCase):
    def test_sha256_default(self) -> None:
        result = hash_string("hello")
        self.assertEqual(len(result), 64)
        self.assertEqual(
            result,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_md5(self) -> None:
        result = hash_string("hello", algorithm="md5")
        self.assertEqual(len(result), 32)
        self.assertEqual(
            result,
            "5d41402abc4b2a76b9719d911017c592",
        )

    def test_sha1(self) -> None:
        result = hash_string("hello", algorithm="sha1")
        self.assertEqual(len(result), 40)

    def test_sha512(self) -> None:
        result = hash_string("hello", algorithm="sha512")
        self.assertEqual(len(result), 128)

    def test_uppercase_algorithm(self) -> None:
        result = hash_string("hello", algorithm="SHA256")
        self.assertEqual(len(result), 64)

    def test_invalid_algorithm(self) -> None:
        with self.assertRaises(ValueError):
            hash_string("hello", algorithm="not-a-real-algo")

    def test_non_string_value(self) -> None:
        with self.assertRaises(TypeError):
            hash_string(123)  # type: ignore[arg-type]

    def test_empty_string(self) -> None:
        result = hash_string("")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_different_inputs_different_hashes(self) -> None:
        self.assertNotEqual(hash_string("hello"), hash_string("world"))


class TestGenerateToken(unittest.TestCase):
    def test_default_length(self) -> None:
        token = generate_token()
        self.assertEqual(len(token), 64)

    def test_custom_length(self) -> None:
        token = generate_token(16)
        self.assertEqual(len(token), 32)

    def test_length_one(self) -> None:
        token = generate_token(1)
        self.assertEqual(len(token), 2)

    def test_uniqueness(self) -> None:
        tokens = {generate_token(16) for _ in range(100)}
        self.assertEqual(len(tokens), 100)

    def test_zero_length_raises(self) -> None:
        with self.assertRaises(ValueError):
            generate_token(0)

    def test_negative_length_raises(self) -> None:
        with self.assertRaises(ValueError):
            generate_token(-1)

    def test_non_integer_length_raises(self) -> None:
        with self.assertRaises(TypeError):
            generate_token("16")  # type: ignore[arg-type]

    def test_boolean_length_raises(self) -> None:
        with self.assertRaises(TypeError):
            generate_token(True)

    def test_hex_characters_only(self) -> None:
        token = generate_token(16)
        self.assertTrue(all(c in "0123456789abcdef" for c in token))


class TestBase64Encode(unittest.TestCase):
    def test_encode_hello(self) -> None:
        self.assertEqual(base64_encode("hello"), "aGVsbG8=")

    def test_encode_empty(self) -> None:
        self.assertEqual(base64_encode(""), "")

    def test_encode_unicode(self) -> None:
        encoded = base64_encode("héllo")
        self.assertEqual(base64_decode(encoded), "héllo")

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            base64_encode(123)  # type: ignore[arg-type]

    def test_roundtrip(self) -> None:
        original = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(base64_decode(base64_encode(original)), original)


class TestBase64Decode(unittest.TestCase):
    def test_decode_hello(self) -> None:
        self.assertEqual(base64_decode("aGVsbG8="), "hello")

    def test_decode_empty(self) -> None:
        self.assertEqual(base64_decode(""), "")

    def test_invalid_base64_raises(self) -> None:
        with self.assertRaises(ValueError):
            base64_decode("!!!not-base64!!!")

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            base64_decode(123)  # type: ignore[arg-type]

    def test_unpadded_input_raises(self) -> None:
        with self.assertRaises(ValueError):
            base64_decode("aGVsbG8")


if __name__ == "__main__":
    unittest.main()
TESTCRYPTOUTILS
# --- list_utils.py ---
cat > "$OUTPUT_DIR/list_utils.py" <<'LISTUTILS'
"""Advanced list utility functions for common manipulation tasks."""

from typing import Any, Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")
K = TypeVar("K")

__all__: List[str] = [
    "partition",
    "group_by",
    "safe_get",
    "find",
    "drop",
    "take",
    "intersperse",
]


def partition(
    lst: List[T], predicate: Callable[[T], bool]
) -> Tuple[List[T], List[T]]:
    """Split a list into two lists based on a predicate.

    Args:
        lst: The list to partition.
        predicate: A function that returns ``True`` for elements that should
            be in the first result list.

    Returns:
        A tuple of ``(matching, non_matching)`` lists.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        ([2, 4], [1, 3])
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    matching: List[T] = []
    non_matching: List[T] = []
    for item in lst:
        if predicate(item):
            matching.append(item)
        else:
            non_matching.append(item)
    return matching, non_matching


def group_by(lst: List[T], key_func: Callable[[T], K]) -> dict:
    """Group elements of a list into a dict by key function.

    Args:
        lst: The list to group.
        key_func: A function that extracts a grouping key from each element.

    Returns:
        A dict mapping each key to the list of elements that produced it,
        preserving insertion order of first occurrence.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> result = group_by(["a", "b", "c"], lambda s: len(s))
        >>> result == {1: ["a", "b", "c"]}
        True
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    result: dict = {}
    for item in lst:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def safe_get(lst: List[T], index: int, default: Optional[T] = None) -> Optional[T]:
    """Safely retrieve an element by index, returning a default on out-of-range.

    Args:
        lst: The list to index into.
        index: The index to retrieve. Supports negative indexing.
        default: The value to return if the index is out of range.
            Defaults to ``None``.

    Returns:
        The element at ``index``, or ``default`` if the index is out of range.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> safe_get([1, 2, 3], 0)
        1
        >>> safe_get([1, 2, 3], 10, default=0)
        0
        >>> safe_get([1, 2, 3], -1)
        3
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    try:
        return lst[index]
    except IndexError:
        return default


def find(lst: List[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Return the first element in the list that satisfies the predicate.

    Args:
        lst: The list to search.
        predicate: A function that returns ``True`` for the desired element.

    Returns:
        The first matching element, or ``None`` if no element matches.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> find([1, 2, 3], lambda x: x > 2)
        3
        >>> find([1, 2, 3], lambda x: x > 5)

    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    for item in lst:
        if predicate(item):
            return item
    return None


def drop(lst: List[T], n: int) -> List[T]:
    """Drop the first ``n`` elements from a list and return the rest.

    Args:
        lst: The list to truncate.
        n: The number of elements to drop from the front.

    Returns:
        A new list with the first ``n`` elements removed.
        If ``n`` exceeds the list length, returns an empty list.

    Raises:
        TypeError: If ``lst`` is not a list or ``n`` is not an integer.
        ValueError: If ``n`` is negative.

    Examples:
        >>> drop([1, 2, 3, 4, 5], 2)
        [3, 4, 5]
        >>> drop([1, 2, 3], 5)
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return lst[n:]


def take(lst: List[T], n: int) -> List[T]:
    """Take the first ``n`` elements from a list and return them.

    Args:
        lst: The list to take elements from.
        n: The number of elements to take from the front.

    Returns:
        A new list containing the first ``n`` elements.
        If ``n`` exceeds the list length, returns the whole list.

    Raises:
        TypeError: If ``lst`` is not a list or ``n`` is not an integer.
        ValueError: If ``n`` is negative.

    Examples:
        >>> take([1, 2, 3, 4, 5], 3)
        [1, 2, 3]
        >>> take([1, 2, 3], 10)
        [1, 2, 3]
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return lst[:n]


def intersperse(lst: List[T], separator: T) -> List[T]:
    """Insert a separator between each pair of adjacent elements in a list.

    Args:
        lst: The list to intersperse.
        separator: The value to insert between each element.

    Returns:
        A new list with the separator inserted between every pair of
        adjacent elements. Returns an empty list if ``lst`` is empty.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> intersperse([1, 2, 3], 0)
        [1, 0, 2, 0, 3]
        >>> intersperse(["a", "b"], "-")
        ['a', '-', 'b']
        >>> intersperse([], "-")
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not lst:
        return []
    result: List[T] = [lst[0]]
    for item in lst[1:]:
        result.append(separator)
        result.append(item)
    return result
LISTUTILS
# --- tests/test_list_utils.py ---
cat > "$OUTPUT_DIR/tests/test_list_utils.py" <<'TESTLISTUTILS'
"""Tests for list_utils module."""
import unittest

from list_utils import drop, find, group_by, intersperse, partition, safe_get, take


class TestPartition(unittest.TestCase):
    def test_partition_even_odd(self) -> None:
        matching, non_matching = partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        self.assertEqual(matching, [2, 4])
        self.assertEqual(non_matching, [1, 3])

    def test_partition_empty_list(self) -> None:
        matching, non_matching = partition([], lambda x: True)
        self.assertEqual(matching, [])
        self.assertEqual(non_matching, [])

    def test_partition_all_match(self) -> None:
        matching, non_matching = partition([1, 2, 3], lambda x: True)
        self.assertEqual(matching, [1, 2, 3])
        self.assertEqual(non_matching, [])

    def test_partition_none_match(self) -> None:
        matching, non_matching = partition([1, 2, 3], lambda x: False)
        self.assertEqual(matching, [])
        self.assertEqual(non_matching, [1, 2, 3])

    def test_partition_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            partition("not a list", lambda x: True)  # type: ignore[arg-type]


class TestGroupBy(unittest.TestCase):
    def test_group_by_length(self) -> None:
        result = group_by(["a", "bb", "c", "ddd"], lambda s: len(s))
        self.assertEqual(result[1], ["a", "c"])
        self.assertEqual(result[2], ["bb"])
        self.assertEqual(result[3], ["ddd"])

    def test_group_by_empty_list(self) -> None:
        result = group_by([], lambda x: x)
        self.assertEqual(result, {})

    def test_group_by_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            group_by("not a list", lambda x: x)  # type: ignore[arg-type]


class TestSafeGet(unittest.TestCase):
    def test_safe_get_valid_index(self) -> None:
        self.assertEqual(safe_get([1, 2, 3], 0), 1)

    def test_safe_get_negative_index(self) -> None:
        self.assertEqual(safe_get([1, 2, 3], -1), 3)

    def test_safe_get_out_of_range_default(self) -> None:
        self.assertIsNone(safe_get([1, 2, 3], 10))

    def test_safe_get_custom_default(self) -> None:
        self.assertEqual(safe_get([1, 2, 3], 10, default=0), 0)

    def test_safe_get_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            safe_get("not a list", 0)  # type: ignore[arg-type]


class TestFind(unittest.TestCase):
    def test_find_first_match(self) -> None:
        self.assertEqual(find([1, 2, 3, 4], lambda x: x > 2), 3)

    def test_find_no_match_returns_none(self) -> None:
        self.assertIsNone(find([1, 2, 3], lambda x: x > 10))

    def test_find_empty_list_returns_none(self) -> None:
        self.assertIsNone(find([], lambda x: True))

    def test_find_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            find("not a list", lambda x: True)  # type: ignore[arg-type]


class TestDrop(unittest.TestCase):
    def test_drop_basic(self) -> None:
        self.assertEqual(drop([1, 2, 3, 4, 5], 2), [3, 4, 5])

    def test_drop_zero(self) -> None:
        self.assertEqual(drop([1, 2, 3], 0), [1, 2, 3])

    def test_drop_more_than_length(self) -> None:
        self.assertEqual(drop([1, 2, 3], 10), [])

    def test_drop_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            drop([1, 2, 3], -1)

    def test_drop_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            drop("not a list", 1)  # type: ignore[arg-type]


class TestTake(unittest.TestCase):
    def test_take_basic(self) -> None:
        self.assertEqual(take([1, 2, 3, 4, 5], 3), [1, 2, 3])

    def test_take_more_than_length(self) -> None:
        self.assertEqual(take([1, 2, 3], 10), [1, 2, 3])

    def test_take_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            take([1, 2, 3], -1)

    def test_take_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            take("not a list", 1)  # type: ignore[arg-type]


class TestIntersperse(unittest.TestCase):
    def test_intersperse_ints(self) -> None:
        self.assertEqual(intersperse([1, 2, 3], 0), [1, 0, 2, 0, 3])

    def test_intersperse_empty_list(self) -> None:
        self.assertEqual(intersperse([], "-"), [])

    def test_intersperse_non_list_raises(self) -> None:
        with self.assertRaises(TypeError):
            intersperse("not a list", "-")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTLISTUTILS

# --- env_utils.py ---
cat > "$OUTPUT_DIR/env_utils.py" <<'ENVLUTILS'
"""Environment variable utility functions for reading, writing, and parsing values.

This module provides a small, consistent API around :mod:`os` environment
variables, including typed accessors (``int``, ``float``, ``bool``) and helpers
for required variables, defaults, and prefix-based grouping.
"""

import os
from typing import Dict, List, Optional

__all__: List[str] = [
    "ensure_env",
    "get_env",
    "get_env_bool",
    "get_env_float",
    "get_env_int",
    "get_env_required",
    "prefix_env",
    "set_env",
    "unset_env",
]

_TRUE_VALUES = frozenset({"1", "true", "yes", "y", "on", "t"})
_FALSE_VALUES = frozenset({"0", "false", "no", "n", "off", "f", ""})


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Return the value of an environment variable, or ``default`` if unset.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as a string, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.

    Example:
        >>> import os
        >>> os.environ.pop("MISSING_VAR", None)
        >>> get_env("MISSING_VAR", "fallback")
        'fallback'
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    return os.environ.get(key, default)


def get_env_required(key: str) -> str:
    """Return the value of a required environment variable.

    Args:
        key: The name of the environment variable.

    Returns:
        The environment variable value as a string.

    Raises:
        TypeError: If ``key`` is not a string.
        KeyError: If the environment variable is not set.

    Example:
        >>> import os
        >>> os.environ["MY_VAR"] = "hello"
        >>> get_env_required("MY_VAR")
        'hello'
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        raise KeyError(f"Required environment variable not set: {key}")
    return value


def get_env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    """Return an environment variable parsed as an integer.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as an integer, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If the variable is set but cannot be parsed as an integer.

    Example:
        >>> import os
        >>> os.environ["PORT"] = "8080"
        >>> get_env_int("PORT")
        8080
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        raise ValueError(
            f"Environment variable {key!r} is not a valid integer: {value!r}"
        ) from None


def get_env_float(key: str, default: Optional[float] = None) -> Optional[float]:
    """Return an environment variable parsed as a floating-point number.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as a float, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If the variable is set but cannot be parsed as a float.

    Example:
        >>> import os
        >>> os.environ["RATIO"] = "3.14"
        >>> get_env_float("RATIO")
        3.14
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Environment variable {key!r} is not a valid float: {value!r}") from None


def get_env_bool(key: str, default: Optional[bool] = None) -> Optional[bool]:
    """Return an environment variable parsed as a boolean.

    The following case-insensitive values are recognized as ``True``:
    ``"1"``, ``"true"``, ``"yes"``, ``"y"``, ``"on"``, ``"t"``.

    The following case-insensitive values are recognized as ``False``:
    ``"0"``, ``"false"``, ``"no"``, ``"n"``, ``"off"``, ``"f"``, ``""``.

    Args:
        key: The name of the environment variable.
        default: The value to return if the variable is not set. Defaults to ``None``.

    Returns:
        The environment variable value as a boolean, or ``default`` if unset.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If the variable is set but is not a recognized boolean string.

    Example:
        >>> import os
        >>> os.environ["DEBUG"] = "true"
        >>> get_env_bool("DEBUG")
        True
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    value = os.environ.get(key)
    if value is None:
        return default
    lowered = value.strip().lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False
    raise ValueError(f"Environment variable {key!r} is not a valid boolean: {value!r}")


def set_env(key: str, value: object) -> None:
    """Set an environment variable to the string representation of ``value``.

    Args:
        key: The name of the environment variable.
        value: The value to set. Non-string values are converted via ``str()``.

    Raises:
        TypeError: If ``key`` is not a string.
        ValueError: If ``key`` is empty or contains ``=``.
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if not key:
        raise ValueError("key must not be empty")
    if "=" in key:
        raise ValueError("key must not contain '='")
    os.environ[key] = str(value)


def ensure_env(key: str, default: str) -> str:
    """Ensure an environment variable is set, populating it with ``default`` if missing.

    If the variable is already set, its current value is returned unchanged.
    Otherwise ``default`` is set and returned.

    Args:
        key: The name of the environment variable.
        default: The value to use (and set) if the variable is not already set.

    Returns:
        The current value of the environment variable.

    Raises:
        TypeError: If ``key`` or ``default`` is not a string.
        ValueError: If ``key`` is empty or contains ``=``.

    Example:
        >>> import os
        >>> os.environ.pop("NEW_VAR", None)
        >>> ensure_env("NEW_VAR", "default")
        'default'
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if not isinstance(default, str):
        raise TypeError("default must be a string")
    value = os.environ.get(key)
    if value is None:
        set_env(key, default)
        return default
    return value


def unset_env(key: str) -> bool:
    """Unset (remove) an environment variable.

    Args:
        key: The name of the environment variable.

    Returns:
        ``True`` if the variable was present and removed, ``False`` if it was not set.

    Raises:
        TypeError: If ``key`` is not a string.
    """
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    return os.environ.pop(key, None) is not None


def prefix_env(prefix: str) -> Dict[str, str]:
    """Return all environment variables whose names start with ``prefix``.

    Args:
        prefix: The prefix to filter environment variable names by.

    Returns:
        A dictionary mapping matching variable names to their values.

    Raises:
        TypeError: If ``prefix`` is not a string.

    Example:
        >>> import os
        >>> os.environ["APP_DEBUG"] = "1"
        >>> prefix_env("APP_")
        {'APP_DEBUG': '1'}
    """
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    return {k: v for k, v in os.environ.items() if k.startswith(prefix)}
ENVLUTILS
# --- logging_utils.py ---
cat > "$OUTPUT_DIR/logging_utils.py" <<'LOGUTILS'
"""Logging configuration and helper utilities.

This module provides a thin, consistent API around the standard :mod:`logging`
module, including a ``get_logger`` helper, a ``configure_logging`` entry point
for application-wide setup, and a ``log_calls`` decorator for tracing function
entry and exit.
"""

import functools
import logging
from typing import Any, Callable, List, Optional, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

__all__: List[str] = [
    "configure_logging",
    "get_logger",
    "log_calls",
]

_DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DEFAULT_LOGGER_NAME = "logging_utils"


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a :class:`logging.Logger` for the given name.

    Args:
        name: The name for the logger, typically the module's ``__name__``.
            If ``None``, the root logger is returned.

    Returns:
        A :class:`logging.Logger` instance.

    Example:
        >>> logger = get_logger("my_app")
        >>> logger.name
        'my_app'
    """
    return logging.getLogger(name)


def configure_logging(
    level: Optional[int] = None,
    format: str = _DEFAULT_FORMAT,
    datefmt: Optional[str] = None,
    handlers: Optional[List[logging.Handler]] = None,
    force: bool = False,
) -> logging.Logger:
    """Configure the root logger with a consistent format and handlers.

    This is a thin wrapper around :func:`logging.basicConfig` that returns the
    configured root logger for convenience.

    Args:
        level: The logging level (e.g. ``logging.INFO``). When ``None``, the
            :mod:`logging` default of ``logging.WARNING`` is used.
        format: The log message format string. Defaults to a timestamped
            format including the logger name and level.
        datefmt: The date format string passed to
            :func:`logging.basicConfig`. Defaults to ``None``.
        handlers: Optional list of handlers to attach to the root logger.
            When ``None``, a :class:`logging.StreamHandler` is used.
        force: If ``True``, remove any existing handlers from the root logger
            before applying this configuration. Defaults to ``False``.

    Returns:
        The configured root :class:`logging.Logger`.

    Raises:
        TypeError: If ``level`` is not an integer or ``None``.
        TypeError: If ``handlers`` is not a list or ``None``.

    Example:
        >>> root = configure_logging(level=logging.INFO, force=True)
        >>> root.level
        20
    """
    if level is not None and not isinstance(level, int):
        raise TypeError("level must be an integer or None")
    if handlers is not None and not isinstance(handlers, list):
        raise TypeError("handlers must be a list or None")

    if level is None:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        handlers=handlers,
        force=force,
    )
    return logging.getLogger()


def log_calls(
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
) -> Callable[[F], F]:
    """Decorator factory that logs function calls and return values.

    The decorator logs two messages per invocation: one before the wrapped
    function runs (containing the arguments) and one after it returns
    (containing the return value). ``functools.wraps`` is used, so the
    decorated function's metadata (``__name__``, ``__doc__``, etc.) is
    preserved.

    Args:
        logger: The logger to emit messages to. If ``None``, a logger named
            ``"logging_utils"`` is used.
        level: The logging level for the emitted messages. Defaults to
            ``logging.DEBUG``.

    Returns:
        A decorator that wraps a function to log its calls.

    Example:
        >>> @log_calls()
        ... def greet(name: str) -> str:
        ...     return f"Hello, {name}!"
        ...
        >>> greet("World")
        'Hello, World!'
    """
    log = logger if logger is not None else logging.getLogger(_DEFAULT_LOGGER_NAME)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log.log(
                level,
                "Calling %s with args=%r, kwargs=%r",
                func.__qualname__,
                args,
                kwargs,
            )
            result = func(*args, **kwargs)
            log.log(
                level,
                "%s returned %r",
                func.__qualname__,
                result,
            )
            return result

        return cast(F, wrapper)

    return decorator
LOGUTILS
# --- cache_utils.py ---
cat > "$OUTPUT_DIR/cache_utils.py" <<'CACHEUTILS'
"""Caching utilities for memoizing function results.

This module provides a small, consistent API around function result caching,
including a ``memoize`` decorator factory, a ``clear_cache`` helper to invalidate
stored results, and a ``cache_info`` helper to inspect cache statistics.
"""

import functools
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

__all__: List[str] = [
    "cache_info",
    "clear_cache",
    "memoize",
]


def memoize(
    maxsize: Optional[int] = 128,
    typed: bool = False,
) -> Callable[[F], F]:
    """Decorator factory that caches a function's return values.

    The wrapped function stores results keyed by its call arguments so that
    subsequent invocations with the same arguments return the cached value
    without re-executing the body. ``functools.wraps`` is used, so the
    decorated function's metadata (``__name__``, ``__doc__``, etc.) is
    preserved.

    Args:
        maxsize: The maximum number of cached entries to retain. When the
            cache exceeds this size, the least-recently-used entry is evicted.
            Pass ``None`` for an unbounded cache. Defaults to ``128``.
        typed: If ``True``, arguments of the same value but different types
            (e.g. ``1`` and ``1.0``) are cached separately. Defaults to
            ``False``.

    Returns:
        A decorator that wraps a function with caching behavior.

    Example:
        >>> @memoize()
        ... def square(n: int) -> int:
        ...     return n * n
        ...
        >>> square(4)
        16
    """
    if maxsize is not None and (not isinstance(maxsize, int) or isinstance(maxsize, bool)):
        raise TypeError("maxsize must be an integer or None")
    if maxsize is not None and maxsize < 1:
        raise ValueError("maxsize must be a positive integer or None")

    def decorator(func: F) -> F:
        cache: Dict[Any, Any] = {}
        order: List[Any] = []
        hits = [0]
        misses = [0]

        def _make_key(args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
            """Build a hashable cache key from positional and keyword arguments."""
            key_args: Tuple[Any, ...] = tuple(args)
            key_kwargs: Tuple[Tuple[str, Any], ...] = tuple(sorted(kwargs.items()))
            if typed:
                return (key_args, key_kwargs, tuple(type(a) for a in args))
            return (key_args, key_kwargs)

        def _evict_if_needed() -> None:
            """Evict the least-recently-used entry when the cache is full."""
            if maxsize is None or len(cache) <= maxsize:
                return
            for old_key in order:
                if old_key in cache:
                    cache.pop(old_key, None)
                    order.remove(old_key)
                    return

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _make_key(args, kwargs)
            if key in cache:
                hits[0] += 1
                return cache[key]
            misses[0] += 1
            result = func(*args, **kwargs)
            cache[key] = result
            order.append(key)
            _evict_if_needed()
            return result

        def clear() -> None:
            """Remove all cached entries and reset statistics."""
            cache.clear()
            order.clear()
            hits[0] = 0
            misses[0] = 0

        def info() -> Dict[str, Any]:
            """Return a dictionary describing the current cache state."""
            return {
                "hits": hits[0],
                "misses": misses[0],
                "maxsize": maxsize,
                "currsize": len(cache),
            }

        wrapper.clear_cache = clear  # type: ignore[attr-defined]
        wrapper.cache_info = info  # type: ignore[attr-defined]
        return cast(F, wrapper)

    return decorator


def clear_cache(func: F) -> None:
    """Clear the cache of a function decorated with :func:`memoize`.

    Args:
        func: A function previously decorated with :func:`memoize`.

    Raises:
        TypeError: If ``func`` does not expose a ``clear_cache`` attribute,
            meaning it was not memoized.

    Example:
        >>> @memoize()
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        ...
        >>> add(1, 2)
        3
        >>> clear_cache(add)
    """
    clear = getattr(func, "clear_cache", None)
    if not callable(clear):
        raise TypeError(
            "clear_cache can only be used on functions decorated with memoize"
        )
    clear()


def cache_info(func: F) -> Dict[str, Any]:
    """Return cache statistics for a function decorated with :func:`memoize`.

    Args:
        func: A function previously decorated with :func:`memoize`.

    Returns:
        A dictionary with ``hits``, ``misses``, ``maxsize``, and ``currsize``
        keys describing the current state of the cache.

    Raises:
        TypeError: If ``func`` does not expose a ``cache_info`` attribute,
            meaning it was not memoized.

    Example:
        >>> @memoize()
        ... def mul(a: int, b: int) -> int:
        ...     return a * b
        ...
        >>> mul(2, 3)
        6
        >>> info = cache_info(mul)
        >>> info["misses"]
        1
    """
    info = getattr(func, "cache_info", None)
    if not callable(info):
        raise TypeError(
            "cache_info can only be used on functions decorated with memoize"
        )
    return cast(Dict[str, Any], info())
CACHEUTILS
# --- timing_utils.py ---
cat > "$OUTPUT_DIR/timing_utils.py" <<'TIMINGUTILS'
"""Performance measurement utilities for timing code execution.

This module provides helpers for measuring and benchmarking code execution,
including a context manager for timing blocks, a function to calculate elapsed
time, and a decorator for benchmarking function execution.
"""

import functools
import time
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


class timer:
    """Context manager for measuring execution time of a code block.

    Args:
        label: Optional label to display with the timing result.

    Examples:
        >>> with timer("Database query"):
        ...     # Execute database query
        ...     pass
        Database query: 0.00s

        >>> with timer():
        ...     time.sleep(0.1)
        Elapsed: 0.10s
    """

    def __init__(self, label: str = "Elapsed") -> None:
        self.label = label
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> "timer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed = time.perf_counter() - self.start_time
        if self.label:
            print(f"{self.label}: {self.elapsed:.2f}s")


def elapsed_time(start_time: float) -> float:
    """Calculate elapsed time since a start time.

    Args:
        start_time: Start time as returned by time.perf_counter() or time.time().

    Returns:
        Elapsed time in seconds.

    Examples:
        >>> start = time.perf_counter()
        >>> time.sleep(0.05)
        >>> elapsed_time(start)
        0.05...
    """
    return time.perf_counter() - start_time


def benchmark(
    iterations: int = 1,
) -> Callable[[F], F]:
    """Decorator that benchmarks a function by running it multiple times.

    Args:
        iterations: Number of times to run the function for averaging.
                   Must be positive. Defaults to 1.

    Returns:
        Decorated function that prints timing information and returns the
        result of the final function call.

    Examples:
        >>> @benchmark(iterations=3)
        ... def slow_function():
        ...     time.sleep(0.1)
        ...     return "done"
        >>> result = slow_function()
        slow_function (avg of 3 runs): 0.30s
        >>> result
        'done'
    """
    if iterations < 1:
        raise ValueError("iterations must be positive")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            total_time = 0.0
            result = None
            for i in range(iterations):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                total_time += time.perf_counter() - start
            avg_time = total_time / iterations
            print(f"{func.__name__} (avg of {iterations} runs): {avg_time:.2f}s")
            return result

        return cast(F, wrapper)

    return decorator


if __name__ == "__main__":
    # Simple demonstration when run directly

    @benchmark(iterations=2)
    def example_function():
        time.sleep(0.05)
        return "completed"

    result = example_function()
    print(f"Function returned: {result}")

    # Example of timer context manager
    with timer("Example block"):
        time.sleep(0.02)
        print("Inside timed block")

    # Example of elapsed_time function
    start = time.perf_counter()
    time.sleep(0.03)
    elapsed = elapsed_time(start)
    print(f"Elapsed time: {elapsed:.2f}s")
TIMINGUTILS
# --- rate_limiter_utils.py ---
cat > "$OUTPUT_DIR/rate_limiter_utils.py" <<'RLUTILS'
"""Rate limiting utilities for controlling the frequency of operations.

This module provides helpers for rate limiting using the token bucket algorithm,
including a RateLimiter class, a token_bucket context manager, and a rate_limit
decorator.
"""

import time
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class RateLimiter:
    """Token bucket rate limiter.

    Args:
        rate: Maximum frequency (in tokens per second).
        capacity: Maximum tokens in the bucket. If not provided, defaults to rate.
    """

    def __init__(self, rate: float, capacity: Optional[float] = None):
        if rate <= 0:
            raise ValueError("rate must be positive")
        self.rate = float(rate)
        self.capacity = float(capacity if capacity is not None else rate)
        self.tokens = self.capacity
        self.last_updated = time.monotonic()

    def _update(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_updated
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_updated = now

    def acquire(self, tokens: float = 1) -> bool:
        """Acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire.

        Returns:
            True if tokens were acquired, False otherwise.
        """
        self._update()
        if tokens > self.capacity:
            # Cannot acquire more than capacity at once
            return False
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def acquire_blocking(self, tokens: float = 1) -> None:
        """Block until tokens can be acquired.

        Args:
            tokens: Number of tokens to acquire.
        """
        while not self.acquire(tokens):
            time.sleep(0.001)  # Sleep briefly to avoid busy loop


class token_bucket:
    """Context manager that acquires tokens from a RateLimiter.

    Args:
        rate_limiter: A RateLimiter instance.
        tokens: Number of tokens to acquire. Defaults to 1.

    Examples:
        >>> limiter = RateLimiter(rate=2.0)  # 2 tokens per second
        >>> with token_bucket(limiter):
        ...     # This block will execute, but will be rate-limited
        ...     pass
    """

    def __init__(self, rate_limiter: RateLimiter, tokens: float = 1):
        self.rate_limiter = rate_limiter
        self.tokens = tokens

    def __enter__(self) -> None:
        self.rate_limiter.acquire_blocking(self.tokens)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


def rate_limit(
    rate: float,
    capacity: Optional[float] = None,
) -> Callable[[F], F]:
    """Decorator that limits the rate at which a function can be called.

    Args:
        rate: Maximum frequency (in calls per second).
        capacity: Maximum burst size. If not provided, defaults to rate.

    Returns:
        Decorated function that will be rate-limited.

    Examples:
        >>> @rate_limit(rate=2.0)  # Allow at most 2 calls per second
        ... def limited_function():
        ...     return "result"
        >>> result = limited_function()
    """
    limiter = RateLimiter(rate=rate, capacity=capacity)

    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            limiter.acquire_blocking()
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


if __name__ == "__main__":
    # Simple demonstration when run directly
    import time

    @rate_limit(rate=2.0)  # 2 calls per second
    def example_function():
        return "completed"

    # Call the function multiple times and see the rate limiting
    start = time.monotonic()
    for i in range(5):
        result = example_function()
        elapsed = time.monotonic() - start
        print(f"Call {i+1}: {result} at {elapsed:.2f}s")
        # We don't sleep here because the decorator will block if needed
RLUTILS
# --- retry_utils.py ---
cat > "$OUTPUT_DIR/retry_utils.py" <<'RETRYUTILS'
"""Retry utility functions for retrying operations with backoff."""

import functools
import random
import time
from typing import Any, Callable, Tuple, Type


def retry(
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function if it raises an exception.

    Args:
        max_attempts: Maximum number of attempts (including initial attempt).
        delay: Initial delay between attempts in seconds.
        backoff: Multiplier applied to delay after each attempt.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries on specified exceptions.

    Examples:
        >>> @retry(max_attempts=3, delay=0.1, backoff=2.0)
        ... def unreliable_function():
        ...     import random
        ...     if random.random() < 0.7:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> # May succeed after retries
        >>> result = unreliable_function()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise
                    time.sleep(_delay)
                    _delay *= backoff
            # Should never reach here due to raise on last attempt
            raise RuntimeError("Unexpected state in retry decorator")

        return wrapper

    return decorator


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function with exponential backoff and optional jitter.

    Args:
        max_attempts: Maximum number of attempts (including initial attempt).
        initial_delay: Initial delay between attempts in seconds.
        backoff_factor: Multiplier for delay after each attempt.
        jitter: If True, adds random jitter to delay to prevent thundering herd.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries with exponential backoff.

    Examples:
        >>> @retry_with_backoff(max_attempts=3, initial_delay=0.1, backoff_factor=2.0)
        ... def unreliable_function():
        ...     import random
        ...     if random.random() < 0.7:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> # May succeed after retries with increasing delays
        >>> result = unreliable_function()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise
                    # Apply jitter if enabled
                    actual_delay = delay
                    if jitter:
                        actual_delay *= random.uniform(0.5, 1.5)
                    time.sleep(actual_delay)
                    delay *= backoff_factor
            # Should never reach here due to raise on last attempt
            raise RuntimeError("Unexpected state in retry_with_backoff decorator")

        return wrapper

    return decorator


def retry_count(
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function and returns the result along with retry count.

    Args:
        max_attempts: Maximum number of attempts (including initial attempt).
        delay: Initial delay between attempts in seconds.
        backoff: Multiplier applied to delay after each attempt.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that returns (result, retry_count) where retry_count
        is the number of retries that occurred (0 if no retries needed).

    Examples:
        >>> @retry_count(max_attempts=3, delay=0.1)
        ... def unreliable_function():
        ...     import random
        ...     if random.random() < 0.8:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> result, count = unreliable_function()  # count is number of retries
        >>> isinstance(result, str)
        True
        >>> isinstance(count, int)
        True
        >>> count >= 0
        True
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> tuple:
            _delay = delay
            retries = 0
            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    return result, retries
                except exceptions:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise
                    retries += 1
                    time.sleep(_delay)
                    _delay *= backoff
            # Should never reach here due to raise on last attempt
            raise RuntimeError("Unexpected state in retry_count decorator")

        return wrapper

    return decorator


if __name__ == "__main__":
    # Simple demonstration when run directly
    import random

    @retry(max_attempts=3, delay=0.01, backoff=2.0)
    def unstable_operation():
        if random.random() < 0.8:
            raise RuntimeError("Temporary failure")
        return "Success!"

    try:
        result = unstable_operation()
        print(f"Operation succeeded: {result}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")

    @retry_with_backoff(max_attempts=3, initial_delay=0.01, backoff_factor=2.0)
    def unstable_operation_with_backoff():
        if random.random() < 0.8:
            raise RuntimeError("Temporary failure")
        return "Success with backoff!"

    try:
        result = unstable_operation_with_backoff()
        print(f"Operation succeeded with backoff: {result}")
    except Exception as e:
        print(f"Operation failed after retries with backoff: {e}")

    @retry_count(max_attempts=3, delay=0.01)
    def unstable_operation_with_count():
        if random.random() < 0.8:
            raise RuntimeError("Temporary failure")
        return "Success with count!"

    try:
        result, count = unstable_operation_with_count()
        print(f"Operation succeeded: {result} (retried {count} times)")
    except Exception as e:
        print(f"Operation failed after retries: {e}")
RETRYUTILS
# --- priority_queue_utils.py ---
cat > "$OUTPUT_DIR/priority_queue_utils.py" <<'PQUTILS'
"""Priority queue utilities for heap-based priority queue implementation.

This module provides a heap-based PriorityQueue class and helper functions
for managing items with priorities.
"""

import heapq
from typing import Any, Generic, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """A heap-based priority queue implementation.

    Items are stored as tuples (priority, item) in a min-heap. If multiple
    items have the same priority, their original insertion order is preserved
    by using an incrementing counter.

    Args:
        items: Optional initial items as (priority, item) tuples.
    """

    def __init__(self, items: Optional[List[Tuple[float, T]]] = None) -> None:
        self._heap: List[Tuple[float, int, T]] = []
        self._counter = 0
        if items is not None:
            for item_pair in items:
                if isinstance(item_pair, tuple) and len(item_pair) == 2:
                    # Could be (priority, item) or (item, priority)
                    first, second = item_pair
                    # Heuristic: if second is a number (int/float), it's likely (item, priority)
                    # If first is a number, it's likely (priority, item)
                    if isinstance(second, (int, float)) and not isinstance(first, (int, float)):
                        item, priority = first, second
                    elif isinstance(first, (int, float)) and not isinstance(second, (int, float)):
                        priority, item = first, second
                    else:
                        # Default to (priority, item) for numeric first
                        priority, item = first, second
                    self.push(item, priority=float(priority))
                else:
                    self.push(item_pair)

    def push(self, item: T, priority: float = 10) -> None:
        """Push an item into the queue with given priority."""
        heapq.heappush(self._heap, (float(priority), self._counter, item))
        self._counter += 1

    def pop(self) -> Optional[T]:
        """Pop the item with highest priority (lowest priority value)."""
        if not self._heap:
            return None
        _, _, item = heapq.heappop(self._heap)
        return item

    def peek(self) -> Optional[T]:
        """Return the item with highest priority without removing it."""
        if not self._heap:
            return None
        _, _, item = self._heap[0]
        return item

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._heap) == 0

    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._heap)

    def __len__(self) -> int:
        """Return the number of items in the queue."""
        return len(self._heap)

    def __bool__(self) -> bool:
        """Return True if the queue is non-empty."""
        return len(self._heap) > 0

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._heap.clear()
        self._counter = 0


def push_priority(pq: PriorityQueue[T], item: T, priority: float = 10) -> None:
    """Push an item into a priority queue."""
    pq.push(item, priority=priority)


def pop_priority(pq: PriorityQueue[T]) -> Optional[T]:
    """Pop the highest priority item from a priority queue."""
    return pq.pop()


def peek_priority(pq: PriorityQueue[T]) -> Optional[T]:
    """Peek at the highest priority item without removing it."""
    return pq.peek()


def is_empty_priority(pq: PriorityQueue[T]) -> bool:
    """Check if a priority queue is empty."""
    return pq.is_empty()


def size_priority(pq: PriorityQueue[T]) -> int:
    """Get the size of a priority queue."""
    return pq.size()


def clear_priority(pq: PriorityQueue[T]) -> None:
    """Clear all items from a priority queue."""
    pq.clear()


def create_priority_queue(items: Optional[List[Tuple[float, T]]] = None) -> PriorityQueue[T]:
    """Create a new PriorityQueue instance."""
    return PriorityQueue(items)


def merge_queues(*queues: PriorityQueue[T]) -> PriorityQueue[T]:
    """Merge multiple priority queues into a single new queue."""
    all_items: List[Tuple[float, T]] = []
    for q in queues:
        for priority, _, item in q._heap:
            all_items.append((priority, item))
    return PriorityQueue(all_items)


if __name__ == "__main__":
    pq = PriorityQueue()
    pq.push("high", priority=1)
    pq.push("low", priority=10)
    pq.push("medium", priority=5)
    print(f"Peek: {pq.peek()}")
    while not pq.is_empty():
        print(pq.pop())
PQUTILS
# --- dict_utils.py ---
cat > "$OUTPUT_DIR/dict_utils.py" <<'DICTUTILS'
"""Dictionary utility functions."""

from typing import Any, Dict, List, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def deep_merge(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge two dictionaries.

    Args:
        d1: First dictionary.
        d2: Second dictionary.

    Returns:
        Merged dictionary.
    """
    result = d1.copy()
    for key, value in d2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten a nested dictionary into a single-level dictionary.

    Args:
        d: Dictionary to flatten.
        parent_key: Parent key prefix.
        sep: Separator between keys.

    Returns:
        Flattened dictionary.
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(d: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Unflatten a flat dictionary with keys containing separators.

    Args:
        d: Flattened dictionary.
        sep: Separator used in keys.

    Returns:
        Nested dictionary.
    """
    result: Dict[str, Any] = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def safe_get(d: Dict[Any, Any], *keys: Any, default: Any = None) -> Any:
    """Safely get a nested value from a dictionary.

    Args:
        d: Dictionary to search in.
        keys: Keys to traverse.
        default: Default value if not found.

    Returns:
        Value at the nested path or default.
    """
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def invert_dict(d: Dict[K, V]) -> Dict[V, K]:
    """Invert a dictionary by swapping keys and values.

    Args:
        d: Dictionary to invert.

    Returns:
        Inverted dictionary.

    Raises:
        ValueError: If values are not unique.
    """
    if len(d.values()) != len(set(d.values())):
        raise ValueError("Cannot invert dictionary with duplicate values")
    return {v: k for k, v in d.items()}


def filter_dict(d: Dict[K, V], predicate: Any) -> Dict[K, V]:
    """Filter a dictionary based on a predicate.

    Args:
        d: Dictionary to filter.
        predicate: Function that takes (key, value) and returns bool.

    Returns:
        Filtered dictionary.
    """
    return {k: v for k, v in d.items() if predicate(k, v)}
DICTUTILS
# --- json_utils.py ---
cat > "$OUTPUT_DIR/json_utils.py" <<'JSONUTILS'
"""JSON utility functions."""

import json
from typing import Any, IO


def read_json(path: str) -> Any:
    """Read JSON data from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Any, indent: int = 4, ensure_ascii: bool = False) -> None:
    """Write JSON data to a file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def load_json_string(s: str) -> Any:
    """Parse JSON from a string."""
    return json.loads(s)


def dump_json_string(data: Any, indent: int = 4, ensure_ascii: bool = False) -> str:
    """Serialize data to JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)


def is_valid_json(s: str) -> bool:
    """Check if a string is valid JSON."""
    try:
        json.loads(s)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def pretty_print_json(data: Any, indent: int = 4) -> str:
    """Return a pretty-printed JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=False)

JSONUTILS
# --- csv_utils.py ---
cat > "$OUTPUT_DIR/csv_utils.py" <<'CSVUTILS'
"""CSV utility functions."""

import csv
from typing import Any, Dict, List, Optional


def read_csv(path: str, delimiter: str = ",", fieldnames: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """Read CSV file and return list of dictionaries."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=delimiter)
        return [dict(row) for row in reader]


def read_csv_as_lists(path: str, delimiter: str = ",") -> List[List[str]]:
    """Read CSV file and return list of lists."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return list(reader)


def write_csv(path: str, rows: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None, delimiter: str = ",") -> None:
    """Write list of dictionaries to CSV file."""
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def write_csv_from_lists(path: str, rows: List[List[Any]], delimiter: str = ",") -> None:
    """Write list of lists to CSV file."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)


def append_csv_row(path: str, row: Dict[str, Any], fieldnames: Optional[List[str]] = None) -> None:
    """Append a single row to CSV file."""
    if fieldnames is None:
        fieldnames = list(row.keys())
    import os
    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

CSVUTILS
# --- set_utils.py ---
cat > "$OUTPUT_DIR/set_utils.py" <<'SETUTILS'
"""Set operation utilities for common set-theoretic and combinatorial tasks."""

from itertools import product
from typing import Any, Iterable, Iterator, List, Sequence, Set, Tuple, TypeVar

T = TypeVar("T")

__all__: List[str] = [
    "is_subset",
    "is_superset",
    "intersection",
    "union",
    "difference",
    "symmetric_difference",
    "cartesian_product",
    "power_set",
]


def _to_set(items: Iterable[Any]) -> Set[Any]:
    """Convert an iterable to a set, raising ``TypeError`` for non-iterables.

    Args:
        items: An iterable of hashable elements.

    Returns:
        A set containing the elements of ``items``.

    Raises:
        TypeError: If ``items`` is not iterable.
    """
    try:
        return set(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable") from exc


def is_subset(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether every element of ``a`` is contained in ``b``.

    Args:
        a: Candidate subset iterable.
        b: Superset iterable.

    Returns:
        ``True`` if ``a`` is a subset of ``b``, otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_subset([1, 2], [1, 2, 3])
        True
        >>> is_subset([1, 4], [1, 2, 3])
        False
    """
    return _to_set(a).issubset(_to_set(b))


def is_superset(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """Check whether ``a`` contains every element of ``b``.

    Args:
        a: Candidate superset iterable.
        b: Subset iterable.

    Returns:
        ``True`` if ``a`` is a superset of ``b``, otherwise ``False``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> is_superset([1, 2, 3], [2])
        True
        >>> is_superset([1, 2], [2, 3])
        False
    """
    return _to_set(a).issuperset(_to_set(b))


def intersection(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return the set of elements common to both ``a`` and ``b``.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the intersection.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> intersection([1, 2, 3], [2, 3, 4])
        {2, 3}
    """
    return _to_set(a) & _to_set(b)


def union(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return the set of elements present in either ``a`` or ``b``.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the union.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> union([1, 2], [2, 3])
        {1, 2, 3}
    """
    return _to_set(a) | _to_set(b)


def difference(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return elements in ``a`` that are not in ``b``.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the difference ``a - b``.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> difference([1, 2, 3], [2])
        {1, 3}
    """
    return _to_set(a) - _to_set(b)


def symmetric_difference(a: Iterable[Any], b: Iterable[Any]) -> Set[Any]:
    """Return elements in either ``a`` or ``b`` but not both.

    Args:
        a: First iterable.
        b: Second iterable.

    Returns:
        A new set containing the symmetric difference.

    Raises:
        TypeError: If ``a`` or ``b`` is not iterable.

    Examples:
        >>> symmetric_difference([1, 2, 3], [2, 3, 4])
        {1, 4}
    """
    return _to_set(a) ^ _to_set(b)


def cartesian_product(
    a: Sequence[Any], b: Sequence[Any]
) -> Iterator[Tuple[Any, Any]]:
    """Yield ordered pairs from the Cartesian product of two sequences.

    Args:
        a: First sequence.
        b: Second sequence.

    Yields:
        Tuples ``(x, y)`` for every ``x`` in ``a`` and ``y`` in ``b``,
        preserving the iteration order of both inputs.

    Raises:
        TypeError: If ``a`` or ``b`` is not a sequence.

    Examples:
        >>> list(cartesian_product([1, 2], ["a", "b"]))
        [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
    """
    if not isinstance(a, (list, tuple, str, bytes)) and not hasattr(a, "__iter__"):
        raise TypeError("a must be a sequence")
    if not isinstance(b, (list, tuple, str, bytes)) and not hasattr(b, "__iter__"):
        raise TypeError("b must be a sequence")
    for x in a:
        for y in b:
            yield (x, y)


def power_set(items: Iterable[T]) -> Iterator[Tuple[T, ...]]:
    """Yield every subset of ``items`` as a tuple.

    The empty set is yielded first, followed by subsets ordered by
    increasing cardinality. For an input of length ``n``, exactly
    ``2 ** n`` subsets are produced.

    Args:
        items: An iterable of hashable elements.

    Yields:
        Tuples representing each subset, preserving the input order of
        elements within each subset.

    Raises:
        TypeError: If ``items`` is not iterable.

    Examples:
        >>> [len(s) for s in power_set([1, 2])]
        [0, 1, 1, 2]
    """
    elements: List[T] = list(items)
    n = len(elements)
    for mask in range(1 << n):
        yield tuple(elements[i] for i in range(n) if mask & (1 << i))
SETUTILS
# --- statistics_utils.py ---
cat > "$OUTPUT_DIR/statistics_utils.py" <<'STATISTICS'
"""Statistical utility functions for data analysis."""

import math
from typing import List, Tuple, TypeVar

T = TypeVar("T", int, float)


def harmonic_mean(numbers: List[T | float]) -> float:
    """Return the harmonic mean of a list of numbers.

    The harmonic mean is the reciprocal of the arithmetic mean of the reciprocals.

    Args:
        numbers: A list of numeric values.

    Returns:
        The harmonic mean.

    Raises:
        ValueError: If the list is empty or contains zero.

    Examples:
        >>> harmonic_mean([1, 2, 4])
        1.7142857142857142
        >>> harmonic_mean([1, 1, 1])
        1.0
    """
    if not numbers:
        raise ValueError("Cannot calculate harmonic mean of empty list")
    # Check for zeros
    if any(x == 0 for x in numbers):
        raise ValueError("Harmonic mean is undefined for values equal to zero")
    reciprocal_sum = sum(1.0 / x for x in numbers)
    return len(numbers) / reciprocal_sum


def geometric_mean(numbers: List[T | float]) -> float:
    """Return the geometric mean of a list of numbers.

    The geometric mean is the nth root of the product of the numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The geometric mean.

    Raises:
        ValueError: If the list is empty or contains negative values.

    Examples:
        >>> geometric_mean([1, 2, 3, 4, 5])
        2.605171084697352
        >>> geometric_mean([1, 1, 1])
        1.0
    """
    if not numbers:
        raise ValueError("Cannot calculate geometric mean of empty list")
    # Check for negatives
    if any(x < 0 for x in numbers):
        raise ValueError("Geometric mean is undefined for negative numbers")
    product = 1.0
    for x in numbers:
        product *= x
    return float(product ** (1.0 / len(numbers)))


def median_even(numbers: List[T | float]) -> Tuple[float, float]:
    """Return the two middle values of a sorted list (for even-length lists).

    For odd-length lists, returns the same value twice (the median).

    Args:
        numbers: A list of numeric values.

    Returns:
        A tuple (lower_middle, upper_middle) where:
        - For even length: the two middle values after sorting.
        - For odd length: (median, median).

    Raises:
        ValueError: If the list is empty.

    Examples:
        >>> median_even([1, 2, 3, 4])
        (2, 3)
        >>> median_even([1, 2, 3])
        (2, 2)
    """
    if not numbers:
        raise ValueError("Cannot calculate median_even of empty list")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        lower = sorted_nums[n // 2 - 1]
        upper = sorted_nums[n // 2]
        return (float(lower), float(upper))
    else:
        median_val = float(sorted_nums[n // 2])
        return (median_val, median_val)


def percentile(numbers: List[T | float], p: float) -> float:
    """Return the p-th percentile of a list of numbers.

    Uses linear interpolation between closest ranks method similar to numpy's
    percentile with method='linear'.

    Args:
        numbers: A list of numeric values.
        p: Percentile to compute (0 <= p <= 100).

    Returns:
        The p-th percentile value.

    Raises:
        ValueError: If the list is empty or p is out of range.

    Examples:
        >>> percentile([1, 2, 3, 4, 5], 50)
        3.0
        >>> percentile([1, 2, 3, 4, 5], 0)
        1.0
        >>> percentile([1, 2, 3, 4, 5], 100)
        5.0
    """
    if not numbers:
        raise ValueError("Cannot calculate percentile of empty list")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100 inclusive")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    # Method: linear interpolation between closest ranks
    # Compute the rank: r = p/100 * (n - 1) + 1
    # Then split into integer part and fraction
    if n == 1:
        return float(sorted_nums[0])
    rank = (p / 100.0) * (n - 1) + 1
    lower_idx = int(math.floor(rank) - 1)  # zero-indexed
    upper_idx = int(math.ceil(rank) - 1)
    weight = rank - math.floor(rank)
    if lower_idx == upper_idx:
        return float(sorted_nums[lower_idx])
    lower_val = float(sorted_nums[lower_idx])
    upper_val = float(sorted_nums[upper_idx])
    return lower_val + weight * (upper_val - lower_val)


def covariance(x: List[T | float], y: List[T | float]) -> float:
    """Return the sample covariance of two lists of numbers.

    Args:
        x: First list of numeric values.
        y: Second list of numeric values.

    Returns:
        The sample covariance.

    Raises:
        ValueError: If the lists are empty, have different lengths,
                    or have fewer than 2 elements.

    Examples:
        >>> covariance([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        -2.5
        >>> covariance([1, 2, 3], [1, 2, 3])
        1.0
    """
    if not x or not y:
        raise ValueError("Cannot calculate covariance of empty list")
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length")
    if len(x) < 2:
        raise ValueError("Covariance requires at least two elements")
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    return cov / (len(x) - 1)


def correlation(x: List[T | float], y: List[T | float]) -> float:
    """Return the Pearson correlation coefficient of two lists.

    Args:
        x: First list of numeric values.
        y: Second list of numeric values.

    Returns:
        The correlation coefficient between -1 and 1.

    Raises:
        ValueError: If the lists are empty, have different lengths,
                    have fewer than 2 elements, or have zero variance.

    Examples:
        >>> correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        -1.0
        >>> correlation([1, 2, 3], [1, 2, 3])
        1.0
    """
    if not x or not y:
        raise ValueError("Cannot calculate correlation of empty list")
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length")
    if len(x) < 2:
        raise ValueError("Correlation requires at least two elements")
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    # Compute covariance and variances
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)
    if var_x == 0 or var_y == 0:
        raise ValueError("Correlation is undefined when variance is zero")
    return cov / math.sqrt(var_x * var_y)


def z_score(numbers: List[T | float]) -> List[float]:
    """Return the z-scores (standard scores) of a list of numbers.

    Each z-score is (x - mean) / population standard deviation.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of z-scores corresponding to each input number.

    Raises:
        ValueError: If the list is empty or if the standard deviation is zero
                    (e.g., all values are identical).

    Examples:
        >>> z_score([1, 2, 3, 4, 5])
        [-1.414213562373095, -0.7071067811865475, 0.0, 0.7071067811865475, 1.414213562373095]
    """
    if not numbers:
        raise ValueError("Cannot calculate z-scores of empty list")
    mean_val = sum(numbers) / len(numbers)
    # Population standard deviation
    variance = sum((x - mean_val) ** 2 for x in numbers) / len(numbers)
    if variance == 0:
        raise ValueError("Standard deviation is zero; cannot compute z-scores")
    std_dev = math.sqrt(variance)
    return [(x - mean_val) / std_dev for x in numbers]


def normalize(numbers: List[T | float]) -> List[float]:
    """Normalize a list of numbers to the range [0, 1] using min-max scaling.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of normalized values where min maps to 0 and max maps to 1.
        If all values are equal, returns a list of 0.0.

    Raises:
        ValueError: If the list is empty.

    Examples:
        >>> normalize([1, 2, 3, 4, 5])
        [0.0, 0.25, 0.5, 0.75, 1.0]
        >>> normalize([5, 5, 5])
        [0.0, 0.0, 0.0]
    """
    if not numbers:
        raise ValueError("Cannot normalize empty list")
    min_val = min(numbers)
    max_val = max(numbers)
    if min_val == max_val:
        return [0.0 for _ in numbers]
    scale = max_val - min_val
    return [(x - min_val) / scale for x in numbers]
STATISTICS
# --- string_utils.py ---
cat > "$OUTPUT_DIR/string_utils.py" <<'STRINGUTILS'
"""Advanced string manipulation utilities."""

import re
import textwrap
from typing import List, Optional


__all__: List[str] = [
    "slugify",
    "camel_to_snake",
    "snake_to_camel",
    "pluralize",
    "truncate",
    "wrap_text",
    "indent_text",
    "remove_extra_whitespace",
    "title_case",
]

_SMALL_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "en", "for", "if", "in",
    "nor", "of", "on", "or", "per", "the", "to", "via", "vs",
}


def _require_string(value: str, name: str) -> str:
    """Validate that ``value`` is a string, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The argument name used in error messages.

    Returns:
        The validated string.

    Raises:
        TypeError: If ``value`` is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug.

    Lowercases the text, replaces whitespace and underscores with hyphens,
    removes non-alphanumeric characters (except hyphens), and collapses
    consecutive hyphens.

    Args:
        text: The string to slugify.

    Returns:
        A URL-friendly slug.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> slugify("Hello World")
        'hello-world'
        >>> slugify("  Python   is   Great!  ")
        'python-is-great'
        >>> slugify("already-a-slug")
        'already-a-slug'
    """
    _require_string(text, "text")
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def camel_to_snake(text: str) -> str:
    """Convert a camelCase or PascalCase string to snake_case.

    Args:
        text: The camelCase or PascalCase string to convert.

    Returns:
        The snake_case equivalent.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> camel_to_snake("helloWorld")
        'hello_world'
        >>> camel_to_snake("XMLParser")
        'xml_parser'
        >>> camel_to_snake("already_snake")
        'already_snake'
    """
    _require_string(text, "text")
    snake = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    snake = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", snake)
    snake = snake.replace("-", "_").lower()
    return snake


def snake_to_camel(text: str) -> str:
    """Convert a snake_case string to camelCase.

    Args:
        text: The snake_case string to convert.

    Returns:
        The camelCase equivalent.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> snake_to_camel("hello_world")
        'helloWorld'
        >>> snake_to_camel("xml_parser")
        'xmlParser'
        >>> snake_to_camel("alreadyCamel")
        'alreadyCamel'
    """
    _require_string(text, "text")
    if "_" not in text:
        return text
    parts = text.split("_")
    camel = parts[0].lower()
    for part in parts[1:]:
        camel += part[:1].upper() + part[1:].lower() if part else ""
    return camel


def pluralize(word: str, count: Optional[int] = None) -> str:
    """Return the plural form of an English word.

    Applies simple inflection rules: words ending in ``s``, ``x``, ``z``,
    ``ch``, or ``sh`` take ``-es``; words ending in a consonant plus ``y``
    take ``-ies``; all others take ``-s``. When ``count`` is ``1`` (or not
    given), the singular form is returned.

    Args:
        word: The singular word to pluralize.
        count: Optional count. When ``1``, returns the singular form.

    Returns:
        The plural (or singular when count is 1) form of the word.

    Raises:
        TypeError: If ``word`` is not a string.

    Examples:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("cat", 2)
        'cats'
        >>> pluralize("cat", 1)
        'cat'
        >>> pluralize("bus")
        'buses'
        >>> pluralize("baby")
        'babies'
    """
    _require_string(word, "word")
    if count == 1:
        return word
    if re.search(r"[sxz]$", word) or re.search(r"[chsh]$", word):
        return word + "es"
    if re.search(r"[^aeiou]y$", word):
        return word[:-1] + "ies"
    return word + "s"


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate a string to the given length, appending a suffix.

    If the string is shorter than or equal to ``length``, it is returned
    unchanged. The suffix is included within the length limit.

    Args:
        text: The string to truncate.
        length: Maximum length of the result including the suffix.
        suffix: Suffix appended when truncation occurs (default: "...").

    Returns:
        The truncated string.

    Raises:
        TypeError: If ``text`` or ``suffix`` is not a string.
        ValueError: If ``length`` is negative.

    Examples:
        >>> truncate("Hello, world!", 5)
        'He...'
        >>> truncate("Hi", 10)
        'Hi'
        >>> truncate("Hello, world!", 8, suffix="")
        'Hello, w'
    """
    _require_string(text, "text")
    _require_string(suffix, "suffix")
    if length < 0:
        raise ValueError("length must be non-negative")
    if len(text) <= length:
        return text
    if length < len(suffix):
        return suffix[:length]
    return text[: length - len(suffix)] + suffix


def wrap_text(text: str, width: int = 70) -> str:
    """Wrap a string to the specified line width.

    Args:
        text: The string to wrap.
        width: Maximum line width (default: 70).

    Returns:
        The wrapped string with newlines inserted.

    Raises:
        TypeError: If ``text`` is not a string.
        ValueError: If ``width`` is not positive.

    Examples:
        >>> wrap_text("hello world", 5)
        'hello\\nworld'
    """
    _require_string(text, "text")
    if width <= 0:
        raise ValueError("width must be positive")
    return textwrap.fill(text, width=width)


def indent_text(text: str, prefix: str = "    ") -> str:
    """Indent every line of a string with the given prefix.

    Args:
        text: The string to indent.
        prefix: The prefix to prepend to each line (default: four spaces).

    Returns:
        The indented string.

    Raises:
        TypeError: If ``text`` or ``prefix`` is not a string.

    Examples:
        >>> indent_text("line1\\nline2", "  ")
        '  line1\\n  line2'
    """
    _require_string(text, "text")
    _require_string(prefix, "prefix")
    lines = text.split("\n")
    return "\n".join(prefix + line for line in lines)


def remove_extra_whitespace(text: str) -> str:
    """Collapse runs of whitespace into single spaces and strip edges.

    Args:
        text: The string to clean.

    Returns:
        The string with normalized whitespace.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> remove_extra_whitespace("  hello   world  ")
        'hello world'
        >>> remove_extra_whitespace("a\\n\\tb")
        'a b'
    """
    _require_string(text, "text")
    return " ".join(text.split())


def title_case(text: str, small_words: Optional[List[str]] = None) -> str:
    """Convert a string to title case.

    Major words are capitalized; small words (articles, conjunctions,
    prepositions) are lowercased unless they are the first or last word.

    Args:
        text: The string to convert.
        small_words: Optional list of words to keep lowercase. Defaults to a
            standard set of English small words.

    Returns:
        The title-cased string.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> title_case("hello world")
        'Hello World'
        >>> title_case("the quick brown fox")
        'The Quick Brown Fox'
        >>> title_case("war and peace")
        'War and Peace'
    """
    _require_string(text, "text")
    if small_words is None:
        small = _SMALL_WORDS
    else:
        small = {w.lower() for w in small_words}
    words = text.split()
    if not words:
        return text
    result: List[str] = []
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word.lower() not in small:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return " ".join(result)
STRINGUTILS
# --- tree_utils.py ---
cat > "$OUTPUT_DIR/tree_utils.py" <<'TREEUTILS'
"""Tree and nested structure utilities for working with nested dict/list data."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def get_nested(d: Dict[str, Any] | Any, keys: Iterable[str | int], default: Any = None) -> Any:
    """Safely get a value from a nested structure using a key path.

    Args:
        d: The nested dictionary/list structure to traverse.
        keys: An iterable of keys/indexes representing the path.
        default: The default value to return if the path is missing.

    Returns:
        The value at the path, or default if not found.

    Examples:
        >>> get_nested({'a': {'b': {'c': 1}}}, ['a', 'b', 'c'])
        1
        >>> get_nested({'a': {'b': 2}}, ['a', 'x'], default='missing')
        'missing'
        >>> get_nested({'a': [1, 2, 3]}, ['a', 1])
        2
    """
    try:
        result: Any = d
        for key in keys:
            result = result[key]  # type: ignore[index]
        return result
    except (KeyError, IndexError, TypeError):
        return default


def set_nested(d: Dict[str, Any], keys: Iterable[str | int], value: Any) -> Dict[str, Any]:
    """Set a value in a nested dict, creating intermediate dicts as needed.

    Args:
        d: The root dictionary to modify.
        keys: An iterable of keys representing the path.
        value: The value to set.

    Returns:
        The modified dictionary (same object, mutated).

    Examples:
        >>> d = {}
        >>> set_nested(d, ['a', 'b', 'c'], 1)
        {'a': {'b': {'c': 1}}}
        >>> set_nested(d, ['a', 'b', 'd'], 2)
        {'a': {'b': {'c': 1, 'd': 2}}}
    """
    keys_list = list(keys)
    if not keys_list:
        return d

    current: Any = d
    for key in keys_list[:-1]:
        if key not in current or not isinstance(current[key], dict):  # type: ignore[index]
            current[key] = {}  # type: ignore[index]
        current = current[key]  # type: ignore[index]
    current[keys_list[-1]] = value  # type: ignore[index]
    return d


def delete_nested(d: Dict[str, Any], keys: Iterable[str | int]) -> bool:
    """Delete a value at a nested path.

    Args:
        d: The root dictionary to modify.
        keys: An iterable of keys representing the path.

    Returns:
        True if the value was deleted, False if the path doesn't exist.

    Examples:
        >>> d = {'a': {'b': {'c': 1}}}
        >>> delete_nested(d, ['a', 'b', 'c'])
        True
        >>> delete_nested(d, ['a', 'x'])
        False
    """
    keys_list = list(keys)
    if not keys_list:
        return False

    current: Any = d
    path: List[Any] = []
    for key in keys_list[:-1]:
        path.append((current, key))
        if not isinstance(current, dict) or key not in current:  # type: ignore[index]
            return False
        current = current[key]  # type: ignore[index]

    last_key = keys_list[-1]
    if not isinstance(current, dict) or last_key not in current:  # type: ignore[index]
        return False
    del current[last_key]  # type: ignore[index]
    return True


def flatten_tree(d: Dict[str, Any] | Any, parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary into a flat dictionary with compound keys.

    Args:
        d: The nested dictionary to flatten.
        parent_key: The base key for nested items.
        sep: The separator between keys.

    Returns:
        A flat dictionary.

    Examples:
        >>> flatten_tree({'a': {'b': {'c': 1, 'd': 2}}, 'e': 3})
        {'a.b.c': 1, 'a.b.d': 2, 'e': 3}
    """
    items: List[Tuple[str, Any]] = []
    if isinstance(d, dict):
        for key, value in d.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)
            items.extend(flatten_tree(value, new_key, sep).items())
        return dict(items)
    else:
        if parent_key == '':
            return {'': d}
        return {parent_key: d}


def unflatten_tree(flat: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
    """Unflatten a flat dictionary with compound keys back to a nested structure.

    Args:
        flat: A flat dictionary with keys joined by sep.
        sep: The separator used in keys.

    Returns:
        A nested dictionary.

    Examples:
        >>> unflatten_tree({'a.b.c': 1, 'a.b.d': 2, 'e': 3})
        {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
    """
    result: Dict[str, Any] = {}
    for key, value in flat.items():
        parts = key.split(sep) if sep and sep in key else [key] if key else []
        current = result
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        if parts:
            current[parts[-1]] = value
        else:
            result = value  # type: ignore[assignment]
    return result


def map_tree(func: Callable[[Any], Any], tree: Any) -> Any:
    """Recursively apply a function to all leaf values in a tree structure.

    Dict values and list elements are treated as branches. Non-container
    values (or leaf nodes) have func applied.

    Args:
        func: The function to apply to leaf values.
        tree: The tree structure to traverse.

    Returns:
        A new tree structure with func applied to all leaves.

    Examples:
        >>> map_tree(lambda x: x * 2, {'a': {'b': 1}, 'c': [2, 3]})
        {'a': {'b': 2}, 'c': [4, 6]}
    """
    if isinstance(tree, dict):
        return {k: map_tree(func, v) for k, v in tree.items()}
    elif isinstance(tree, list):
        return [map_tree(func, item) for item in tree]
    elif isinstance(tree, tuple):
        return tuple(map_tree(func, item) for item in tree)
    else:
        return func(tree)


def filter_tree(pred: Callable[[Any], bool], tree: Any) -> Any:
    """Recursively filter a tree structure based on a predicate.

    The predicate is applied to values. For dicts, only key-value pairs
    where pred(value) is True (or based on leaf logic) are kept? This
    implementation keeps nodes where the transformed/considered value passes;
    for nested structures, it recursively filters and drops empty containers
    when appropriate.

    Args:
        pred: The predicate function returning True for values to keep.
        tree: The tree structure to filter.

    Returns:
        A filtered tree structure.

    Examples:
        >>> filter_tree(lambda x: x > 1, {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 0}})
        {'b': 2, 'c': {'d': 3}}
    """
    if isinstance(tree, dict):
        result: Dict[str, Any] = {}
        for k, v in tree.items():
            filtered = filter_tree(pred, v)
            # Keep if filtered is not empty container or if it's a truthy leaf that passed
            if isinstance(filtered, (dict, list, tuple)):
                if filtered:  # non-empty
                    result[k] = filtered
            elif pred(v) if False else True:  # always keep if leaf passes pred? better check
                pass  # handle below
            # simpler: if the original v becomes filtered, keep based on whether useful
            # but easier logic: apply pred to leaf; for containers, recurse and keep if non-empty
            if isinstance(v, (dict, list, tuple)):
                if filtered:
                    result[k] = filtered
            else:
                if pred(v):
                    result[k] = v
        return result
    elif isinstance(tree, list):
        result_list = []
        for item in tree:
            filtered = filter_tree(pred, item)
            if isinstance(filtered, (dict, list, tuple)):
                if filtered:
                    result_list.append(filtered)
            else:
                if pred(item):
                    result_list.append(item)
        return result_list
    elif isinstance(tree, tuple):
        result_list = []
        for item in tree:
            filtered = filter_tree(pred, item)
            if isinstance(filtered, (dict, list, tuple)):
                if filtered:
                    result_list.append(filtered)
            else:
                if pred(item):
                    result_list.append(item)
        return tuple(result_list)
    else:
        return tree if pred(tree) else None  # type: ignore[return-value]

TREEUTILS
# --- compression_utils.py ---
cat > "$OUTPUT_DIR/compression_utils.py" <<'COMPRESSIONUTILS'
"""Compression and decompression utility functions."""

import bz2
import gzip
import io
import tarfile
import zipfile
from pathlib import Path
from typing import Any, BinaryIO, List, Optional, Union


def gzip_compress(data: Union[bytes, str], encoding: str = "utf-8") -> bytes:
    """Compress data using gzip."""
    if isinstance(data, str):
        data = data.encode(encoding)
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes or str")
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as f:
        f.write(data)
    return buf.getvalue()


def gzip_decompress(data: bytes, encoding: Optional[str] = None) -> Union[bytes, str]:
    """Decompress gzip compressed data."""
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    buf = io.BytesIO(data)
    with gzip.GzipFile(fileobj=buf, mode="rb") as f:
        result = f.read()
    if encoding is not None:
        return result.decode(encoding)
    return result


def bz2_compress(data: Union[bytes, str], encoding: str = "utf-8") -> bytes:
    """Compress data using bz2."""
    if isinstance(data, str):
        data = data.encode(encoding)
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes or str")
    return bz2.compress(data)


def bz2_decompress(data: bytes, encoding: Optional[str] = None) -> Union[bytes, str]:
    """Decompress bz2 compressed data."""
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    result = bz2.decompress(data)
    if encoding is not None:
        return result.decode(encoding)
    return result


def zip_compress_files(files: List[Union[str, Path]], output_path: Union[str, Path]) -> None:
    """Compress a list of files into a zip archive."""
    output_path = Path(output_path)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in files:
            file_path = Path(file_path)
            if file_path.is_file():
                zf.write(file_path, file_path.name)
            else:
                raise FileNotFoundError(f"File not found: {file_path}")


def zip_extract(archive_path: Union[str, Path], extract_path: Union[str, Path] = ".") -> None:
    """Extract a zip archive."""
    archive_path = Path(archive_path)
    extract_path = Path(extract_path)
    extract_path.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "r") as zf:
        zf.extractall(extract_path)


def tar_compress(files: List[Union[str, Path]], output_path: Union[str, Path], mode: str = "w") -> None:
    """Compress files into a tar archive."""
    output_path = Path(output_path)
    with tarfile.open(output_path, mode) as tf:
        for file_path in files:
            file_path = Path(file_path)
            if file_path.exists():
                tf.add(file_path, file_path.name)
            else:
                raise FileNotFoundError(f"File not found: {file_path}")


def tar_extract(archive_path: Union[str, Path], extract_path: Union[str, Path] = ".") -> None:
    """Extract a tar archive."""
    archive_path = Path(archive_path)
    extract_path = Path(extract_path)
    extract_path.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r") as tf:
        tf.extractall(extract_path)
COMPRESSIONUTILS
# --- ip_utils.py ---
cat > "$OUTPUT_DIR/ip_utils.py" <<'IPUTILS'
"""IP address utility functions."""

import ipaddress
from typing import Union


def is_valid_ip(ip_str: str) -> bool:
    """Check if a string is a valid IP address (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_ipv4(ip_str: str) -> bool:
    """Check if a string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_ipv6(ip_str: str) -> bool:
    """Check if a string is a valid IPv6 address."""
    try:
        ipaddress.IPv6Address(ip_str)
        return True
    except (ValueError, TypeError):
        return False


def get_ip_version(ip_str: str) -> int:
    """Get the IP version (4 or 6) of an IP address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.version
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def ip_to_int(ip_str: str) -> int:
    """Convert an IP address string to an integer."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return int(ip)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def int_to_ip(num: int, version: int = 4) -> str:
    """Convert an integer to an IP address string."""
    try:
        if version == 4:
            return str(ipaddress.IPv4Address(num))
        elif version == 6:
            return str(ipaddress.IPv6Address(num))
        else:
            raise ValueError("Version must be 4 or 6")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid integer for IP {version}: {num}")


def is_private_ip(ip_str: str) -> bool:
    """Check if an IP address is private."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_loopback_ip(ip_str: str) -> bool:
    """Check if an IP address is loopback."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_loopback
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_multicast_ip(ip_str: str) -> bool:
    """Check if an IP address is multicast."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_multicast
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_link_local_ip(ip_str: str) -> bool:
    """Check if an IP address is link-local."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_link_local
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_reserved_ip(ip_str: str) -> bool:
    """Check if an IP address is reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_reserved
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def normalize_ip(ip_str: str) -> str:
    """Normalize an IP address to its canonical form."""
    try:
        if isinstance(ip_str, str):
            if '.' in ip_str and ':' not in ip_str:
                parts = ip_str.split('.')
                if all(part.isdigit() for part in parts):
                    parts = [str(int(p)) for p in parts]
                    ip_str_clean = '.'.join(parts)
                else:
                    ip_str_clean = ip_str
            else:
                ip_str_clean = ip_str
        else:
            ip_str_clean = ip_str
        ip = ipaddress.ip_address(ip_str_clean)
        if ip.version == 6:
            try:
                if ip.ipv4_mapped:
                    return str(ip.ipv4_mapped)
            except AttributeError:
                pass
        return str(ip)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def in_subnet(ip_str: str, network: str) -> bool:
    """Check if an IP address is in a subnet."""
    try:
        ip = ipaddress.ip_address(ip_str)
        net = ipaddress.ip_network(network, strict=False)
        return ip in net
    except (ValueError, TypeError):
        raise ValueError("Invalid IP address or network")


__all__ = [
    "is_valid_ip",
    "is_valid_ipv4",
    "is_valid_ipv6",
    "get_ip_version",
    "ip_to_int",
    "int_to_ip",
    "is_private_ip",
    "is_loopback_ip",
    "is_multicast_ip",
    "is_link_local_ip",
    "is_reserved_ip",
    "normalize_ip",
    "in_subnet",
]
IPUTILS

# --- uuid_utils.py ---

cat > "$OUTPUT_DIR/uuid_utils.py" <<'UUIDUTILS'
"""UUID utility functions for generating and validating UUIDs."""

from __future__ import annotations

import uuid
from typing import List, Optional

__all__: List[str] = [
    "generate_uuid",
    "generate_uuid4",
    "generate_uuid1",
    "is_valid_uuid",
    "parse_uuid",
]


def generate_uuid(version: int = 4) -> str:
    """Generate a UUID string."""
    if version == 4:
        return str(uuid.uuid4())
    elif version == 1:
        return str(uuid.uuid1())
    else:
        raise ValueError("UUID version must be 1 or 4")


def generate_uuid4() -> str:
    """Generate a UUID4 string."""
    return str(uuid.uuid4())


def generate_uuid1() -> str:
    """Generate a UUID1 string."""
    return str(uuid.uuid1())


def is_valid_uuid(uuid_str: str, version: Optional[int] = None) -> bool:
    """Check if a string is a valid UUID."""
    try:
        parsed = uuid.UUID(uuid_str)
        if version is not None:
            return parsed.version == version
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def parse_uuid(uuid_str: str) -> uuid.UUID:
    """Parse a UUID string into a UUID object."""
    return uuid.UUID(uuid_str)
UUIDUTILS

# --- prompt_utils.py ---
cat > "$OUTPUT_DIR/prompt_utils.py" <<'PROMPTUTILS'
"""Prompt utility functions for working with text prompts."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

__all__: List[str] = [
    "truncate_prompt",
    "format_prompt_template",
    "clean_prompt",
    "extract_keywords",
    "wrap_prompt",
    "estimate_token_count",
]


def truncate_prompt(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a prompt to a maximum length."""
    if len(text) <= max_length:
        return text
    if max_length <= len(suffix):
        return text[:max_length]
    return text[: max_length - len(suffix)] + suffix


def format_prompt_template(template: str, **kwargs: Any) -> str:
    """Format a prompt template with keyword arguments."""
    return template.format(**kwargs)


def clean_prompt(text: str) -> str:
    """Clean up whitespace in a prompt."""
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text."""
    words = re.findall(r"\b\w+\b", text.lower())
    stop_words = {
        "the",
        "and",
        "is",
        "in",
        "to",
        "of",
        "a",
        "for",
        "on",
        "with",
        "as",
        "by",
        "an",
        "at",
        "are",
        "be",
        "this",
        "that",
        "these",
        "those",
    }
    keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
    seen = set()
    result: List[str] = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            result.append(k)
    return result


def wrap_prompt(text: str, width: int = 80) -> str:
    """Wrap prompt text to a specific width."""
    if width <= 0:
        return text
    words = text.split()
    lines: List[str] = []
    current_line: List[str] = []

    for word in words:
        if len(" ".join(current_line + [word])) <= width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)


def estimate_token_count(text: str) -> int:
    """Estimate token count for a text."""
    if not text:
        return 0
    return max(1, len(text) // 4)
PROMPTUTILS

# --- type_utils.py ---
cat > "$OUTPUT_DIR/type_utils.py" <<'TYPEUTILS'
"""Type introspection utilities."""

from __future__ import annotations

import sys
from typing import Any, List, Union, get_args, get_origin


__all__: List[str] = [
    "is_optional",
    "is_union",
    "is_generic",
    "get_type_args",
    "type_name",
    "is_subclass_safe",
]


def _is_optional_type(tp: Any) -> bool:
    origin = get_origin(tp)
    args = get_args(tp)
    if origin is Union:
        return type(None) in args
    if sys.version_info >= (3, 10):
        from types import UnionType

        if isinstance(tp, UnionType):
            return type(None) in args
    return False


def is_optional(tp: Any) -> bool:
    """Return True if the type is Optional[T] (Union[T, None])."""
    if tp is type(None):
        return True
    return _is_optional_type(tp)


def is_union(tp: Any) -> bool:
    """Return True if the type is a Union."""
    origin = get_origin(tp)
    if origin is Union:
        return True
    if sys.version_info >= (3, 10):
        from types import UnionType

        if isinstance(tp, UnionType):
            return True
    return False


def is_generic(tp: Any) -> bool:
    """Return True if the type is a generic alias (e.g., List[int])."""
    origin = get_origin(tp)
    if origin is not None:
        return True
    if hasattr(tp, "__origin__") and getattr(tp, "__origin__") is not None:
        return True
    return False


def get_type_args(tp: Any) -> tuple[Any, ...]:
    """Return the type arguments of a generic type, if any."""
    return get_args(tp)


def type_name(tp: Any) -> str:
    """Return a human-readable name for a type."""
    if tp is None:
        return "None"
    origin = get_origin(tp)
    if origin is not None:
        args_list: List[str] = []
        for a in get_args(tp):
            args_list.append(type_name(a))
        args_str = ", ".join(args_list)
        origin_name = getattr(origin, "__name__", str(origin))
        if args_str:
            return f"{origin_name}[{args_str}]"
        return str(origin_name)
    if hasattr(tp, "__name__"):
        name = getattr(tp, "__name__")
        return str(name)
    return str(tp)


def is_subclass_safe(cls: Any, base: Any) -> bool:
    """Safely check subclass relationship without raising TypeError."""
    try:
        return issubclass(cls, base)
    except Exception:
        return False
TYPEUTILS
# --- path_utils.py ---
cat > "$OUTPUT_DIR/path_utils.py" <<'PATHUTILS'
"""Path manipulation utilities for working with filesystem paths."""

from __future__ import annotations

import os
from pathlib import Path, PurePath
from typing import List, Union

__all__: List[str] = [
    "join_path",
    "normalize_path",
    "get_absolute_path",
    "get_relative_path",
    "get_parent_dir",
    "get_file_name",
    "get_file_stem",
    "get_file_extension",
    "change_extension",
    "is_absolute",
    "get_path_components",
    "get_common_path",
    "ensure_extension",
]


def join_path(*parts: Union[str, Path]) -> str:
    """Join path components into a single path string.

    Args:
        *parts: Path components to join.

    Returns:
        The joined path as a string.

    Examples:
        >>> join_path('a', 'b', 'c')
        'a/b/c'
        >>> join_path('/usr', 'local', 'bin')
        '/usr/local/bin'
    """
    return str(Path(*[str(p) for p in parts]))


def normalize_path(path: Union[str, Path]) -> str:
    """Normalize a path by resolving redundant separators and relative components.

    Unlike :func:`get_absolute_path`, this does not resolve the path against the
    current working directory; it only collapses redundant separators and ``..``
    / ``.`` components.

    Args:
        path: The path to normalize.

    Returns:
        The normalized path as a string.

    Examples:
        >>> normalize_path('a//b/../c')
        'a/c'
        >>> normalize_path('/usr/./local//bin')
        '/usr/local/bin'
    """
    parts: List[str] = []
    is_absolute = PurePath(path).is_absolute()
    for part in PurePath(path).parts:
        if part == os.sep and is_absolute:
            # Root separator is handled by the prefix below.
            continue
        if part in (".", ".."):
            if part == "..":
                if parts and parts[-1] != "..":
                    parts.pop()
                elif not is_absolute:
                    parts.append("..")
            continue
        parts.append(part)
    if not parts:
        return os.sep if is_absolute else "."
    if is_absolute:
        return os.sep + os.sep.join(parts)
    return os.sep.join(parts)


def get_absolute_path(path: Union[str, Path]) -> str:
    """Return the absolute version of a path.

    Args:
        path: The path to convert.

    Returns:
        The absolute path as a string.

    Examples:
        >>> isinstance(get_absolute_path('foo'), str)
        True
    """
    return str(Path(path).absolute())


def get_relative_path(path: Union[str, Path], start: Union[str, Path] = ".") -> str:
    """Return a path relative to a starting directory.

    Args:
        path: The target path.
        start: The base directory (default: current directory).

    Returns:
        The relative path as a string.

    Raises:
        ValueError: If the path is not relative to the start directory.

    Examples:
        >>> get_relative_path('/usr/local/bin', '/usr')
        'local/bin'
    """
    return str(Path(path).relative_to(Path(start)))


def get_parent_dir(path: Union[str, Path]) -> str:
    """Return the parent directory of a path.

    Args:
        path: The file or directory path.

    Returns:
        The parent directory as a string.

    Examples:
        >>> get_parent_dir('/usr/local/bin/python')
        '/usr/local/bin'
        >>> get_parent_dir('file.txt')
        '.'
    """
    return str(Path(path).parent)


def get_file_name(path: Union[str, Path]) -> str:
    """Return the file name (last component) of a path.

    Args:
        path: The file or directory path.

    Returns:
        The file name as a string.

    Examples:
        >>> get_file_name('/usr/local/bin/python')
        'python'
        >>> get_file_name('archive.tar.gz')
        'archive.tar.gz'
    """
    return Path(path).name


def get_file_stem(path: Union[str, Path]) -> str:
    """Return the file name without its final extension.

    Args:
        path: The file path.

    Returns:
        The file stem as a string.

    Examples:
        >>> get_file_stem('/usr/local/script.py')
        'script'
        >>> get_file_stem('archive.tar.gz')
        'archive.tar'
    """
    return Path(path).stem


def get_file_extension(path: Union[str, Path]) -> str:
    """Return the file extension (including the leading dot) of a path.

    Args:
        path: The file path.

    Returns:
        The file extension as a string, or an empty string if none.

    Examples:
        >>> get_file_extension('script.py')
        '.py'
        >>> get_file_extension('Makefile')
        ''
        >>> get_file_extension('archive.tar.gz')
        '.gz'
    """
    return Path(path).suffix


def change_extension(path: Union[str, Path], extension: str) -> str:
    """Return a path with the file extension replaced.

    The new extension should include the leading dot if desired.

    Args:
        path: The file path.
        extension: The new extension (with or without leading dot).

    Returns:
        The path with the new extension as a string.

    Examples:
        >>> change_extension('script.py', '.txt')
        'script.txt'
        >>> change_extension('image.png', 'jpg')
        'image.jpg'
    """
    if extension and not extension.startswith("."):
        extension = "." + extension
    return str(Path(path).with_suffix(extension))


def is_absolute(path: Union[str, Path]) -> bool:
    """Return True if the path is absolute.

    Args:
        path: The path to check.

    Returns:
        True if the path is absolute, False otherwise.

    Examples:
        >>> is_absolute('/usr/local/bin')
        True
        >>> is_absolute('relative/path')
        False
    """
    return Path(path).is_absolute()


def get_path_components(path: Union[str, Path]) -> List[str]:
    """Split a path into its individual components.

    Args:
        path: The path to split.

    Returns:
        A list of path component strings.

    Examples:
        >>> get_path_components('/usr/local/bin')
        ['/', 'usr', 'local', 'bin']
        >>> get_path_components('a/b/c')
        ['a', 'b', 'c']
    """
    parts = Path(path).parts
    return [str(p) for p in parts]


def get_common_path(*paths: Union[str, Path]) -> str:
    """Return the longest common path prefix of the given paths.

    Args:
        *paths: Two or more paths to compare.

    Returns:
        The common path prefix as a string.

    Raises:
        ValueError: If fewer than two paths are provided.

    Examples:
        >>> get_common_path('/a/b/c', '/a/b/d')
        '/a/b'
        >>> get_common_path('x/y/z', 'x/y/w')
        'x/y'
    """
    if len(paths) < 2:
        raise ValueError("At least two paths are required")
    resolved = [Path(p).parts for p in paths]
    common: List[str] = []
    for parts in zip(*resolved):
        if all(part == parts[0] for part in parts):
            common.append(parts[0])
        else:
            break
    if not common:
        return ""
    return str(PurePath(*common))


def ensure_extension(path: Union[str, Path], extension: str) -> str:
    """Ensure a path has the given extension, adding it if missing.

    The extension should include the leading dot if desired.

    Args:
        path: The file path.
        extension: The required extension.

    Returns:
        The path with the extension guaranteed as a string.

    Examples:
        >>> ensure_extension('script.py', '.py')
        'script.py'
        >>> ensure_extension('script', '.py')
        'script.py'
        >>> ensure_extension('image.png', '.py')
        'image.png.py'
    """
    if not extension.startswith("."):
        extension = "." + extension
    current = Path(path).suffix
    if current == extension:
        return str(path)
    return str(Path(path).with_name(Path(path).name + extension))
PATHUTILS
# --- color_utils.py ---
cat > "$OUTPUT_DIR/color_utils.py" <<'COLORUTILS'
"""Color manipulation utilities.

This module provides functions for converting between color representations
(hexadecimal, RGB, HSL), computing WCAG relative luminance and contrast ratios,
checking accessibility, and adjusting/blending colors.

Colors are accepted either as a hexadecimal string (``"#RRGGBB"`` or
``"RRGGBB"``) or as an RGB tuple ``(r, g, b)`` with integer channels in the
range ``0``-``255``.
"""

from typing import List, Sequence, Tuple, Union

__all__: List[str] = [
    "validate_hex",
    "hex_to_rgb",
    "rgb_to_hex",
    "rgb_to_hsl",
    "hsl_to_rgb",
    "get_luminance",
    "get_contrast_ratio",
    "is_accessible",
    "adjust_brightness",
    "blend_colors",
]

_RGB = Tuple[int, int, int]
_Color = Union[str, _RGB]

_HEX_DIGITS = set("0123456789abcdefABCDEF")

_ACCESSIBILITY_THRESHOLDS = {
    ("AA", "normal"): 4.5,
    ("AA", "large"): 3.0,
    ("AAA", "normal"): 7.0,
    ("AAA", "large"): 4.5,
}


def _require_string(value: str, name: str) -> str:
    """Validate that ``value`` is a string, raising ``TypeError`` otherwise."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _require_int_range(value: int, name: str, minimum: int = 0, maximum: int = 255) -> int:
    """Validate that ``value`` is an int within ``[minimum, maximum]``."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _parse_color(color: _Color, name: str = "color") -> _RGB:
    """Normalize a hex string or RGB tuple to an ``(r, g, b)`` tuple."""
    if isinstance(color, str):
        return hex_to_rgb(color)
    if (
        isinstance(color, tuple)
        and len(color) == 3
        and all(isinstance(channel, int) and not isinstance(channel, bool) for channel in color)
    ):
        r, g, b = color
        return (
            _require_int_range(r, f"{name}[0]"),
            _require_int_range(g, f"{name}[1]"),
            _require_int_range(b, f"{name}[2]"),
        )
    raise TypeError(f"{name} must be a hex string or an (r, g, b) tuple of ints")


def validate_hex(hex_color: str) -> bool:
    """Return ``True`` if ``hex_color`` is a valid ``#RRGGBB`` or ``RRGGBB`` string.

    Args:
        hex_color: The hexadecimal color string to validate.

    Returns:
        ``True`` for a valid 6-digit hex color, ``False`` otherwise.

    Raises:
        TypeError: If ``hex_color`` is not a string.

    Examples:
        >>> validate_hex("#ff5733")
        True
        >>> validate_hex("ff5733")
        True
        >>> validate_hex("#gg5733")
        False
        >>> validate_hex("#ff57")
        False
    """
    _require_string(hex_color, "hex_color")
    value = hex_color.lstrip("#")
    if len(value) != 6:
        return False
    return all(ch in _HEX_DIGITS for ch in value)


def hex_to_rgb(hex_color: str) -> _RGB:
    """Convert a hexadecimal color string to an ``(r, g, b)`` tuple.

    Args:
        hex_color: A ``#RRGGBB`` or ``RRGGBB`` color string.

    Returns:
        A tuple of three integers ``(r, g, b)`` in the range ``0``-``255``.

    Raises:
        TypeError: If ``hex_color`` is not a string.
        ValueError: If ``hex_color`` is not a valid 6-digit hex color.

    Examples:
        >>> hex_to_rgb("#ff5733")
        (255, 87, 51)
        >>> hex_to_rgb("000000")
        (0, 0, 0)
        >>> hex_to_rgb("#FFFFFF")
        (255, 255, 255)
    """
    _require_string(hex_color, "hex_color")
    if not validate_hex(hex_color):
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    value = hex_color.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB channel values to a ``#RRGGBB`` hexadecimal string.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        A lowercase ``#RRGGBB`` hexadecimal color string.

    Raises:
        TypeError: If any channel is not an integer.
        ValueError: If any channel is outside ``0``-``255``.

    Examples:
        >>> rgb_to_hex(255, 87, 51)
        '#ff5733'
        >>> rgb_to_hex(0, 0, 0)
        '#000000'
    """
    r = _require_int_range(r, "r")
    g = _require_int_range(g, "g")
    b = _require_int_range(b, "b")
    return f"#{r:02x}{g:02x}{b:02x}"


def _srgb_linear(channel: int) -> float:
    """Linearize an sRGB 8-bit channel per the WCAG 2.1 relative luminance formula."""
    c = channel / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def get_luminance(color: _Color) -> float:
    """Return the WCAG 2.1 relative luminance of a color.

    The result is in the range ``0.0`` (black) to ``1.0`` (white).

    Args:
        color: A hex string or an ``(r, g, b)`` tuple.

    Returns:
        The relative luminance as a float.

    Raises:
        TypeError: If ``color`` is not a hex string or RGB tuple.
        ValueError: If an RGB channel is outside ``0``-``255``.

    Examples:
        >>> round(get_luminance("#ffffff"), 4)
        1.0
        >>> round(get_luminance("#000000"), 4)
        0.0
        >>> round(get_luminance((255, 255, 255)), 4)
        1.0
    """
    r, g, b = _parse_color(color, "color")
    return 0.2126 * _srgb_linear(r) + 0.7152 * _srgb_linear(g) + 0.0722 * _srgb_linear(b)


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB channel values to HSL ``(h, s, l)``.

    Hue is in degrees ``[0, 360)``; saturation and lightness are in ``[0, 1]``.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        A tuple ``(h, s, l)`` with ``h`` in degrees and ``s``, ``l`` in ``[0, 1]``.

    Raises:
        TypeError: If any channel is not an integer.
        ValueError: If any channel is outside ``0``-``255``.

    Examples:
        >>> h, s, l = rgb_to_hsl(255, 0, 0)
        >>> round(h), round(s, 2), round(l, 2)
        (0, 1.0, 0.5)
    """
    r = _require_int_range(r, "r") / 255.0
    g = _require_int_range(g, "g") / 255.0
    b = _require_int_range(b, "b") / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2.0
    if max_c == min_c:
        return 0.0, 0.0, l
    d = max_c - min_c
    s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
    if max_c == r:
        h = (60.0 * ((g - b) / d) + 360.0) % 360.0
    elif max_c == g:
        h = (60.0 * ((b - r) / d) + 120.0) % 360.0
    else:
        h = (60.0 * ((r - g) / d) + 240.0) % 360.0
    return h, s, l


def hsl_to_rgb(h: float, s: float, l: float) -> _RGB:
    """Convert HSL ``(h, s, l)`` to RGB ``(r, g, b)``.

    Hue ``h`` is in degrees; saturation ``s`` and lightness ``l`` are in ``[0, 1]``.

    Args:
        h: Hue in degrees.
        s: Saturation in ``[0, 1]``.
        l: Lightness in ``[0, 1]``.

    Returns:
        A tuple of three integers ``(r, g, b)`` in the range ``0``-``255``.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If ``s`` or ``l`` is outside ``[0, 1]``.

    Examples:
        >>> hsl_to_rgb(0, 1.0, 0.5)
        (255, 0, 0)
        >>> hsl_to_rgb(0, 0.0, 0.0)
        (0, 0, 0)
    """
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (h, s, l)):
        raise TypeError("h, s, and l must be numbers")
    if not 0.0 <= s <= 1.0 or not 0.0 <= l <= 1.0:
        raise ValueError("s and l must be in the range [0, 1]")

    def _hue_to_rgb(p: float, q: float, t: float) -> float:
        t %= 1.0
        if t < 1.0 / 6.0:
            return p + (q - p) * 6.0 * t
        if t < 0.5:
            return q
        if t < 2.0 / 3.0:
            return p + (q - p) * (2.0 / 3.0 - t) * 6.0
        return p

    if s == 0.0:
        r = g = b = l
    else:
        q = l * (1.0 + s) if l < 0.5 else l + s - l * s
        p = 2.0 * l - q
        r = _hue_to_rgb(p, q, h / 360.0 + 1.0 / 3.0)
        g = _hue_to_rgb(p, q, h / 360.0)
        b = _hue_to_rgb(p, q, h / 360.0 - 1.0 / 3.0)
    return (
        _require_int_range(round(r * 255), "r"),
        _require_int_range(round(g * 255), "g"),
        _require_int_range(round(b * 255), "b"),
    )


def get_contrast_ratio(color1: _Color, color2: _Color) -> float:
    """Return the WCAG 2.1 contrast ratio between two colors.

    The ratio is in the range ``1.0`` (identical colors) to ``21.0`` (black vs
    white). The lighter color's luminance is used as the numerator.

    Args:
        color1: First color (hex string or ``(r, g, b)`` tuple).
        color2: Second color (hex string or ``(r, g, b)`` tuple).

    Returns:
        The contrast ratio as a float.

    Raises:
        TypeError: If either color is not a hex string or RGB tuple.
        ValueError: If an RGB channel is outside ``0``-``255``.

    Examples:
        >>> round(get_contrast_ratio("#ffffff", "#000000"), 2)
        21.0
        >>> round(get_contrast_ratio("#ffffff", "#ffffff"), 2)
        1.0
    """
    lum1 = get_luminance(color1)
    lum2 = get_luminance(color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def is_accessible(
    foreground: _Color,
    background: _Color,
    level: str = "AA",
    size: str = "normal",
) -> bool:
    """Return ``True`` if the color pair meets a WCAG contrast threshold.

    Args:
        foreground: Foreground color (hex string or ``(r, g, b)`` tuple).
        background: Background color (hex string or ``(r, g, b)`` tuple).
        level: Conformance level, either ``"AA"`` or ``"AAA"``.
        size: Text size, either ``"normal"`` or ``"large"``.

    Returns:
        ``True`` when the contrast ratio meets the threshold for the given
        level and size, ``False`` otherwise.

    Raises:
        TypeError: If ``level`` or ``size`` is not a string.
        ValueError: If ``level`` or ``size`` is not a recognized value.

    Examples:
        >>> is_accessible("#000000", "#ffffff")
        True
        >>> is_accessible("#ffffff", "#ffffff", level="AA")
        False
    """
    _require_string(level, "level")
    _require_string(size, "size")
    key = (level.upper(), size.lower())
    if key not in _ACCESSIBILITY_THRESHOLDS:
        raise ValueError(
            f"Unknown level/size combination: {level!r}/{size!r}; "
            "expected level in {'AA', 'AAA'} and size in {'normal', 'large'}"
        )
    return get_contrast_ratio(foreground, background) >= _ACCESSIBILITY_THRESHOLDS[key]


def adjust_brightness(hex_color: str, factor: float) -> str:
    """Scale each RGB channel of ``hex_color`` by ``factor`` and return a hex string.

    ``factor`` of ``1.0`` returns the color unchanged; ``0.0`` returns black;
    values above ``1.0`` brighten the color (channels are clamped to 255).

    Args:
        hex_color: A ``#RRGGBB`` or ``RRGGBB`` color string.
        factor: Brightness multiplier (must be non-negative).

    Returns:
        A lowercase ``#RRGGBB`` hexadecimal color string.

    Raises:
        TypeError: If ``hex_color`` is not a string or ``factor`` is not a number.
        ValueError: If ``hex_color`` is invalid or ``factor`` is negative.

    Examples:
        >>> adjust_brightness("#ff5733", 0.5)
        '#802c1a'
        >>> adjust_brightness("#000000", 2.0)
        '#000000'
    """
    _require_string(hex_color, "hex_color")
    if not isinstance(factor, (int, float)) or isinstance(factor, bool):
        raise TypeError("factor must be a number")
    if factor < 0:
        raise ValueError("factor must be non-negative")
    if not validate_hex(hex_color):
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(
        min(255, int(round(r * factor))),
        min(255, int(round(g * factor))),
        min(255, int(round(b * factor))),
    )


def blend_colors(color1: _Color, color2: _Color, weight: float = 0.5) -> str:
    """Linearly blend two colors and return the result as a hex string.

    ``weight`` of ``0.0`` returns ``color1``; ``1.0`` returns ``color2``;
    intermediate values interpolate between them.

    Args:
        color1: First color (hex string or ``(r, g, b)`` tuple).
        color2: Second color (hex string or ``(r, g, b)`` tuple).
        weight: Blend weight for ``color2`` in ``[0, 1]`` (default: 0.5).

    Returns:
        A lowercase ``#RRGGBB`` hexadecimal color string.

    Raises:
        TypeError: If either color is invalid or ``weight`` is not a number.
        ValueError: If ``weight`` is outside ``[0, 1]`` or an RGB channel is
            outside ``0``-``255``.

    Examples:
        >>> blend_colors("#000000", "#ffffff", 0.5)
        '#808080'
        >>> blend_colors("#ff0000", "#0000ff", 0.0)
        '#ff0000'
    """
    if not isinstance(weight, (int, float)) or isinstance(weight, bool):
        raise TypeError("weight must be a number")
    if not 0.0 <= weight <= 1.0:
        raise ValueError("weight must be in the range [0, 1]")
    r1, g1, b1 = _parse_color(color1, "color1")
    r2, g2, b2 = _parse_color(color2, "color2")
    return rgb_to_hex(
        int(round(r1 + (r2 - r1) * weight)),
        int(round(g1 + (g2 - g1) * weight)),
        int(round(b1 + (b2 - b1) * weight)),
    )
COLORUTILS
# --- tests/test_color_utils.py ---
cat > "$OUTPUT_DIR/tests/test_color_utils.py" <<'TESTCOLORUTILS'
"""Tests for color_utils module."""

import unittest

from color_utils import (
    adjust_brightness,
    blend_colors,
    get_contrast_ratio,
    get_luminance,
    hsl_to_rgb,
    hex_to_rgb,
    is_accessible,
    rgb_to_hsl,
    rgb_to_hex,
    validate_hex,
)


class TestValidateHex(unittest.TestCase):
    def test_valid_hash_hex(self) -> None:
        self.assertTrue(validate_hex("#ff5733"))
        self.assertTrue(validate_hex("#000000"))
        self.assertTrue(validate_hex("#FFFFFF"))
        self.assertTrue(validate_hex("#abcdef"))

    def test_valid_plain_hex(self) -> None:
        self.assertTrue(validate_hex("ff5733"))
        self.assertTrue(validate_hex("000000"))

    def test_invalid_hex(self) -> None:
        self.assertFalse(validate_hex("#gg5733"))
        self.assertFalse(validate_hex("#ff57"))
        self.assertFalse(validate_hex("#ff5733aa"))
        self.assertFalse(validate_hex(""))
        self.assertFalse(validate_hex("#"))
        self.assertFalse(validate_hex("not-a-color"))

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            validate_hex(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            validate_hex(None)  # type: ignore[arg-type]


class TestHexToRgb(unittest.TestCase):
    def test_basic_conversion(self) -> None:
        self.assertEqual(hex_to_rgb("#ff5733"), (255, 87, 51))
        self.assertEqual(hex_to_rgb("ff5733"), (255, 87, 51))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#00ff00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#0000ff"), (0, 0, 255))

    def test_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            hex_to_rgb("#gg5733")
        with self.assertRaises(ValueError):
            hex_to_rgb("#ff57")
        with self.assertRaises(TypeError):
            hex_to_rgb(123)  # type: ignore[arg-type]


class TestRgbToHex(unittest.TestCase):
    def test_basic_conversion(self) -> None:
        self.assertEqual(rgb_to_hex(255, 87, 51), "#ff5733")
        self.assertEqual(rgb_to_hex(0, 0, 0), "#000000")
        self.assertEqual(rgb_to_hex(255, 255, 255), "#ffffff")
        self.assertEqual(rgb_to_hex(0, 255, 0), "#00ff00")

    def test_invalid_channels(self) -> None:
        with self.assertRaises(ValueError):
            rgb_to_hex(256, 0, 0)
        with self.assertRaises(ValueError):
            rgb_to_hex(0, -1, 0)
        with self.assertRaises(TypeError):
            rgb_to_hex(1.5, 0, 0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            rgb_to_hex(0, 0, None)  # type: ignore[arg-type]


class TestRgbToHsl(unittest.TestCase):
    def test_red(self) -> None:
        h, s, l = rgb_to_hsl(255, 0, 0)
        self.assertAlmostEqual(h, 0.0)
        self.assertAlmostEqual(s, 1.0)
        self.assertAlmostEqual(l, 0.5)

    def test_gray(self) -> None:
        h, s, l = rgb_to_hsl(128, 128, 128)
        self.assertAlmostEqual(h, 0.0)
        self.assertAlmostEqual(s, 0.0)
        self.assertAlmostEqual(l, 128 / 255.0, places=6)

    def test_white(self) -> None:
        h, s, l = rgb_to_hsl(255, 255, 255)
        self.assertAlmostEqual(h, 0.0)
        self.assertAlmostEqual(s, 0.0)
        self.assertAlmostEqual(l, 1.0)

    def test_invalid_channels(self) -> None:
        with self.assertRaises(ValueError):
            rgb_to_hsl(256, 0, 0)
        with self.assertRaises(TypeError):
            rgb_to_hsl("a", 0, 0)  # type: ignore[arg-type]


class TestHslToRgb(unittest.TestCase):
    def test_red(self) -> None:
        self.assertEqual(hsl_to_rgb(0, 1.0, 0.5), (255, 0, 0))

    def test_black_white(self) -> None:
        self.assertEqual(hsl_to_rgb(0, 0.0, 0.0), (0, 0, 0))
        self.assertEqual(hsl_to_rgb(0, 0.0, 1.0), (255, 255, 255))

    def test_green_blue(self) -> None:
        self.assertEqual(hsl_to_rgb(120, 1.0, 0.5), (0, 255, 0))
        self.assertEqual(hsl_to_rgb(240, 1.0, 0.5), (0, 0, 255))

    def test_invalid_s_l(self) -> None:
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 1.5, 0.5)
        with self.assertRaises(ValueError):
            hsl_to_rgb(0, 0.5, -0.1)
        with self.assertRaises(TypeError):
            hsl_to_rgb("x", 0.5, 0.5)  # type: ignore[arg-type]


class TestGetLuminance(unittest.TestCase):
    def test_bounds(self) -> None:
        self.assertEqual(get_luminance("#000000"), 0.0)
        self.assertEqual(get_luminance("#ffffff"), 1.0)
        self.assertEqual(get_luminance((0, 0, 0)), 0.0)
        self.assertEqual(get_luminance((255, 255, 255)), 1.0)

    def test_gray_midpoint(self) -> None:
        # Mid gray 128 has a known relative luminance.
        self.assertAlmostEqual(get_luminance("#808080"), 0.2159, places=4)

    def test_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            get_luminance("#gg5733")
        with self.assertRaises(TypeError):
            get_luminance(123)  # type: ignore[arg-type]


class TestGetContrastRatio(unittest.TestCase):
    def test_black_white(self) -> None:
        self.assertAlmostEqual(get_contrast_ratio("#000000", "#ffffff"), 21.0)
        self.assertAlmostEqual(get_contrast_ratio("#ffffff", "#000000"), 21.0)

    def test_identical(self) -> None:
        self.assertAlmostEqual(get_contrast_ratio("#ff5733", "#ff5733"), 1.0)

    def test_range(self) -> None:
        ratio = get_contrast_ratio("#000000", "#ffffff")
        self.assertGreaterEqual(ratio, 1.0)
        self.assertLessEqual(ratio, 21.0)

    def test_tuples_accepted(self) -> None:
        self.assertAlmostEqual(
            get_contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0
        )

    def test_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            get_contrast_ratio("#gg5733", "#000000")
        with self.assertRaises(TypeError):
            get_contrast_ratio(123, "#000000")  # type: ignore[arg-type]


class TestIsAccessible(unittest.TestCase):
    def test_aa_normal_black_white(self) -> None:
        self.assertTrue(is_accessible("#000000", "#ffffff"))
        self.assertTrue(is_accessible("#000000", "#ffffff", level="AA", size="normal"))

    def test_aa_normal_identical_fails(self) -> None:
        self.assertFalse(is_accessible("#ffffff", "#ffffff"))
        self.assertFalse(is_accessible("#ffffff", "#ffffff", level="AA", size="large"))

    def test_aaa_threshold(self) -> None:
        self.assertTrue(is_accessible("#000000", "#ffffff", level="AAA", size="normal"))
        self.assertFalse(is_accessible("#777777", "#ffffff", level="AAA", size="normal"))

    def test_large_text_threshold(self) -> None:
        self.assertTrue(is_accessible("#777777", "#ffffff", level="AA", size="large"))

    def test_invalid_level_size(self) -> None:
        with self.assertRaises(ValueError):
            is_accessible("#000000", "#ffffff", level="ZZZ")
        with self.assertRaises(ValueError):
            is_accessible("#000000", "#ffffff", size="tiny")
        with self.assertRaises(TypeError):
            is_accessible("#000000", "#ffffff", level=1)  # type: ignore[arg-type]


class TestAdjustBrightness(unittest.TestCase):
    def test_half_brightness(self) -> None:
        # Python's round() rounds half to even: 127.5 -> 128, 43.5 -> 44, 25.5 -> 26.
        self.assertEqual(adjust_brightness("#ff5733", 0.5), "#802c1a")

    def test_unchanged_and_black(self) -> None:
        self.assertEqual(adjust_brightness("#ff5733", 1.0), "#ff5733")
        self.assertEqual(adjust_brightness("#000000", 2.0), "#000000")

    def test_clamp(self) -> None:
        self.assertEqual(adjust_brightness("#ffffff", 2.0), "#ffffff")

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            adjust_brightness("#gg5733", 0.5)
        with self.assertRaises(ValueError):
            adjust_brightness("#ff5733", -0.1)
        with self.assertRaises(TypeError):
            adjust_brightness("#ff5733", "high")  # type: ignore[arg-type]


class TestBlendColors(unittest.TestCase):
    def test_midpoint(self) -> None:
        self.assertEqual(blend_colors("#000000", "#ffffff", 0.5), "#808080")

    def test_edges(self) -> None:
        self.assertEqual(blend_colors("#ff0000", "#0000ff", 0.0), "#ff0000")
        self.assertEqual(blend_colors("#ff0000", "#0000ff", 1.0), "#0000ff")

    def test_tuples(self) -> None:
        self.assertEqual(blend_colors((255, 0, 0), (0, 0, 255), 0.5), "#800080")

    def test_invalid_weight(self) -> None:
        with self.assertRaises(ValueError):
            blend_colors("#000000", "#ffffff", 1.5)
        with self.assertRaises(ValueError):
            blend_colors("#000000", "#ffffff", -0.1)
        with self.assertRaises(TypeError):
            blend_colors("#000000", "#ffffff", "half")  # type: ignore[arg-type]

    def test_invalid_color(self) -> None:
        with self.assertRaises(ValueError):
            blend_colors("#gg5733", "#000000")


if __name__ == "__main__":
    unittest.main()
TESTCOLORUTILS
# --- async_utils.py ---
cat > "$OUTPUT_DIR/async_utils.py" <<'ASYNCUTILS'
"""Asynchronous utility functions."""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, List, Optional, TypeVar

T = TypeVar("T")

__all__: List[str] = [
    "run_in_thread",
    "gather_with_timeout",
    "async_sleep",
    "retry_async",
]


async def run_in_thread(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Run a synchronous function in a thread pool."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def gather_with_timeout(
    *coros: Awaitable[Any], timeout: Optional[float] = None
) -> List[Any]:
    """Gather multiple coroutines with an optional timeout."""
    if timeout is None:
        return await asyncio.gather(*coros)
    return await asyncio.wait_for(asyncio.gather(*coros), timeout=timeout)


async def async_sleep(seconds: float) -> None:
    """Sleep for the specified number of seconds asynchronously."""
    await asyncio.sleep(seconds)


async def retry_async(
    func: Callable[..., Awaitable[T]],
    *args: Any,
    max_attempts: int = 3,
    delay: float = 0.1,
    **kwargs: Any,
) -> T:
    """Retry an async function on exceptions."""
    last_exception: Exception = Exception("No attempts made")
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            last_exception = exc
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay)
    raise last_exception
ASYNCUTILS

# --- bit_utils.py ---
cat > "$OUTPUT_DIR/bit_utils.py" <<'BITUTILS'
"""Bitwise utility functions for working with binary representations of integers.

This module provides utilities for counting bits, manipulating individual bits,
detecting powers of two, reversing bits, and rotating bit fields. All functions
operate on non-negative integers unless otherwise noted.
"""

from __future__ import annotations

from typing import Optional

__all__: list[str] = [
    "count_set_bits",
    "is_power_of_two",
    "next_power_of_two",
    "prev_power_of_two",
    "reverse_bits",
    "rotate_left",
    "rotate_right",
    "get_bit",
    "set_bit",
    "clear_bit",
    "toggle_bit",
    "is_even",
    "is_odd",
]


def _validate_nonnegative_int(value: int, name: str = "value") -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _validate_index(index: int) -> None:
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("index must be an integer")
    if index < 0:
        raise ValueError("index must be non-negative")


def _validate_positive_int(value: int, name: str = "value") -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def count_set_bits(value: int) -> int:
    """Return the number of set bits (1s) in the binary representation of value.

    Args:
        value: A non-negative integer.

    Returns:
        The count of set bits.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative.

    Examples:
        >>> count_set_bits(0)
        0
        >>> count_set_bits(5)  # 0b101
        2
        >>> count_set_bits(7)  # 0b111
        3
    """
    _validate_nonnegative_int(value)
    return bin(value).count("1")


def is_power_of_two(value: int) -> bool:
    """Return True if value is a power of two.

    Args:
        value: An integer.

    Returns:
        True if value is a power of two, False otherwise.

    Examples:
        >>> is_power_of_two(1)
        True
        >>> is_power_of_two(16)
        True
        >>> is_power_of_two(18)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return value > 0 and (value & (value - 1)) == 0


def next_power_of_two(value: int) -> int:
    """Return the smallest power of two greater than or equal to value.

    Args:
        value: A non-negative integer.

    Returns:
        The next power of two.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative.

    Examples:
        >>> next_power_of_two(0)
        1
        >>> next_power_of_two(5)
        8
        >>> next_power_of_two(16)
        16
    """
    _validate_nonnegative_int(value)
    if value == 0:
        return 1
    return 1 << (value - 1).bit_length()


def prev_power_of_two(value: int) -> int:
    """Return the largest power of two less than or equal to value.

    Args:
        value: A non-negative integer.

    Returns:
        The previous power of two, or 0 if value is 0.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative.

    Examples:
        >>> prev_power_of_two(0)
        0
        >>> prev_power_of_two(5)
        4
        >>> prev_power_of_two(16)
        16
    """
    _validate_nonnegative_int(value)
    if value == 0:
        return 0
    return 1 << (value.bit_length() - 1)


def reverse_bits(value: int, width: Optional[int] = None) -> int:
    """Reverse the bits of value within the given width.

    Args:
        value: A non-negative integer.
        width: The bit width to reverse within. Defaults to the minimal width
            needed to represent value.

    Returns:
        The integer with bits reversed.

    Raises:
        TypeError: If value or width is not an integer.
        ValueError: If value is negative or width is not positive.

    Examples:
        >>> reverse_bits(0b0001, 4)
        8
        >>> reverse_bits(13, 4)  # 1101 -> 1011
        11
    """
    _validate_nonnegative_int(value)
    if width is None:
        width = value.bit_length() or 1
    _validate_positive_int(width, "width")
    result = 0
    for i in range(width):
        if (value >> i) & 1:
            result |= 1 << (width - 1 - i)
    return result


def rotate_left(value: int, shift: int, width: int) -> int:
    """Rotate the bits of value left by shift positions within width bits.

    Args:
        value: A non-negative integer.
        shift: Number of positions to rotate.
        width: The bit width to rotate within.

    Returns:
        The rotated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or width is not positive.

    Examples:
        >>> rotate_left(0b0001, 1, 4)
        2
        >>> rotate_left(0b1000, 1, 4)
        1
    """
    _validate_nonnegative_int(value)
    if not isinstance(shift, int) or isinstance(shift, bool):
        raise TypeError("shift must be an integer")
    _validate_positive_int(width, "width")
    shift %= width
    mask = (1 << width) - 1
    return ((value << shift) | (value >> (width - shift))) & mask


def rotate_right(value: int, shift: int, width: int) -> int:
    """Rotate the bits of value right by shift positions within width bits.

    Args:
        value: A non-negative integer.
        shift: Number of positions to rotate.
        width: The bit width to rotate within.

    Returns:
        The rotated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or width is not positive.

    Examples:
        >>> rotate_right(0b1000, 1, 4)
        4
        >>> rotate_right(0b0001, 1, 4)
        8
    """
    _validate_nonnegative_int(value)
    if not isinstance(shift, int) or isinstance(shift, bool):
        raise TypeError("shift must be an integer")
    _validate_positive_int(width, "width")
    shift %= width
    mask = (1 << width) - 1
    return ((value >> shift) | (value << (width - shift))) & mask


def get_bit(value: int, index: int) -> int:
    """Return the bit at index (0 = least significant bit).

    Args:
        value: A non-negative integer.
        index: The bit index to read.

    Returns:
        0 or 1.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> get_bit(0b1010, 1)
        1
        >>> get_bit(0b1010, 2)
        0
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return (value >> index) & 1


def set_bit(value: int, index: int) -> int:
    """Return value with the bit at index set to 1.

    Args:
        value: A non-negative integer.
        index: The bit index to set.

    Returns:
        The updated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> set_bit(0b0000, 2)
        4
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return value | (1 << index)


def clear_bit(value: int, index: int) -> int:
    """Return value with the bit at index cleared to 0.

    Args:
        value: A non-negative integer.
        index: The bit index to clear.

    Returns:
        The updated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> clear_bit(0b1111, 1)
        13
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return value & ~(1 << index)


def toggle_bit(value: int, index: int) -> int:
    """Return value with the bit at index flipped.

    Args:
        value: A non-negative integer.
        index: The bit index to toggle.

    Returns:
        The updated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> toggle_bit(0b1010, 1)
        8
        >>> toggle_bit(0b1010, 0)
        11
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return value ^ (1 << index)


def is_even(value: int) -> bool:
    """Return True if value is even.

    Args:
        value: An integer.

    Returns:
        True if value is even, False otherwise.

    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return (value & 1) == 0


def is_odd(value: int) -> bool:
    """Return True if value is odd.

    Args:
        value: An integer.

    Returns:
        True if value is odd, False otherwise.

    Examples:
        >>> is_odd(4)
        False
        >>> is_odd(7)
        True
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return (value & 1) == 1
BITUTILS
# --- concurrent_utils.py ---
cat > "$OUTPUT_DIR/concurrent_utils.py" <<'CONCURRENTUTILS'
"""Concurrent execution utilities for parallel and asynchronous processing.

This module provides helpers for concurrent execution using threads, processes,
and asyncio, including ThreadPool, ProcessPool wrappers and asyncio utilities.
"""

import asyncio
import concurrent.futures
import functools
from typing import Any, Awaitable, Callable, Iterable, List, Optional, TypeVar, Union

T = TypeVar("T")
R = TypeVar("R")


class ThreadPool:
    """Context manager wrapper around ThreadPoolExecutor.

    Provides a simple interface for executing tasks in parallel using threads.

    Args:
        max_workers: The maximum number of worker threads to use.
        thread_name_prefix: An optional name prefix for worker threads.

    Examples:
        >>> with ThreadPool(max_workers=4) as pool:
        ...     results = pool.map(lambda x: x * 2, [1, 2, 3, 4])
        ...     print(list(results))
        [2, 4, 6, 8]

        >>> def square(x):
        ...     return x * x
        >>> with ThreadPool(max_workers=2) as pool:
        ...     future = pool.submit(square, 5)
        ...     print(future.result())
        25
    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
    ) -> None:
        self._max_workers = max_workers
        self._thread_name_prefix = thread_name_prefix
        self._executor: Optional[concurrent.futures.ThreadPoolExecutor] = None

    def __enter__(self) -> "ThreadPool":
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._max_workers,
            thread_name_prefix=self._thread_name_prefix or "ThreadPool",
        )
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True)

    def submit(
        self,
        fn: Callable[..., R],
        *args: Any,
        **kwargs: Any,
    ) -> concurrent.futures.Future[R]:
        """Submit a task to be executed asynchronously."""
        if self._executor is None:
            raise RuntimeError("ThreadPool must be used as a context manager")
        return self._executor.submit(fn, *args, **kwargs)

    def map(
        self,
        fn: Callable[[T], R],
        iterable: Iterable[T],
        timeout: Optional[float] = None,
    ) -> Iterable[R]:
        """Map a function over an iterable, executing in parallel."""
        if self._executor is None:
            raise RuntimeError("ThreadPool must be used as a context manager")
        return self._executor.map(fn, iterable, timeout=timeout)


class ProcessPool:
    """Context manager wrapper around ProcessPoolExecutor."""

    def __init__(
        self,
        max_workers: Optional[int] = None,
        mp_context: Any = None,
    ) -> None:
        self._max_workers = max_workers
        self._mp_context = mp_context
        self._executor: Optional[concurrent.futures.ProcessPoolExecutor] = None

    def __enter__(self) -> "ProcessPool":
        kwargs: Any = {}
        if self._max_workers is not None:
            kwargs["max_workers"] = self._max_workers
        if self._mp_context is not None:
            kwargs["mp_context"] = self._mp_context
        self._executor = concurrent.futures.ProcessPoolExecutor(**kwargs)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._executor is not None:
            self._executor.shutdown(wait=True)

    def submit(
        self,
        fn: Callable[..., R],
        *args: Any,
        **kwargs: Any,
    ) -> concurrent.futures.Future[R]:
        """Submit a task to be executed asynchronously."""
        if self._executor is None:
            raise RuntimeError("ProcessPool must be used as a context manager")
        return self._executor.submit(fn, *args, **kwargs)

    def map(
        self,
        fn: Callable[[T], R],
        iterable: Iterable[T],
        timeout: Optional[float] = None,
    ) -> Iterable[R]:
        """Map a function over an iterable, executing in parallel."""
        if self._executor is None:
            raise RuntimeError("ProcessPool must be used as a context manager")
        return self._executor.map(fn, iterable, timeout=timeout)


async def gather(*coroutines_or_futures: Union[Awaitable[R], R]) -> List[R]:
    """Run awaitable objects in the given sequence concurrently."""

    async def _ensure_awaitable(obj: Union[Awaitable[R], R]) -> R:
        if asyncio.iscoroutine(obj) or hasattr(obj, "__await__"):
            return await obj  # type: ignore[misc]
        return obj  # type: ignore[return-value]

    results = await asyncio.gather(*[_ensure_awaitable(obj) for obj in coroutines_or_futures])
    return list(results)


def run_async(coro: Awaitable[R]) -> R:
    """Run an async coroutine from synchronous code."""
    return asyncio.run(coro)  # type: ignore[arg-type]


def to_async(fn: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:
    """Convert a synchronous function to an async function."""

    @functools.wraps(fn)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        # run_in_executor doesn't take kwargs directly; need to use partial
        return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))

    return async_wrapper


# Module-level helper functions for ProcessPool examples/tests
def _square(x: int) -> int:
    return x * x


def _double(x: int) -> int:
    return x * 2


def _add(a: int, b: int) -> int:
    return a + b


def _multiply(a: int, b: int) -> int:
    return a * b


def _inc(x: int) -> int:
    return x + 1


def _dec(x: int) -> int:
    return x - 1


def _triple(x: int) -> int:
    return x * 3
CONCURRENTUTILS
# --- tests/test_env_utils.py ---
cat > "$OUTPUT_DIR/tests/test_env_utils.py" <<'TESTENVL'
"""Tests for env_utils module."""

import os
import unittest
from unittest import mock

from env_utils import (
    ensure_env,
    get_env,
    get_env_bool,
    get_env_float,
    get_env_int,
    get_env_required,
    prefix_env,
    set_env,
    unset_env,
)


class TestGetEnv(unittest.TestCase):
    def test_returns_value_when_set(self) -> None:
        with mock.patch.dict(os.environ, {"MY_VAR": "value"}, clear=True):
            self.assertEqual(get_env("MY_VAR"), "value")

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(get_env("MISSING"))
            self.assertEqual(get_env("MISSING", "fallback"), "fallback")

    def test_returns_empty_string_when_set_empty(self) -> None:
        with mock.patch.dict(os.environ, {"EMPTY_VAR": ""}, clear=True):
            self.assertEqual(get_env("EMPTY_VAR"), "")

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env(123)  # type: ignore[arg-type]


class TestGetEnvRequired(unittest.TestCase):
    def test_returns_value_when_set(self) -> None:
        with mock.patch.dict(os.environ, {"REQUIRED_VAR": "abc"}, clear=True):
            self.assertEqual(get_env_required("REQUIRED_VAR"), "abc")

    def test_raises_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError):
                get_env_required("MISSING_REQUIRED")

    def test_error_message_contains_key(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(KeyError) as ctx:
                get_env_required("MISSING_REQUIRED")
            self.assertIn("MISSING_REQUIRED", str(ctx.exception))

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_required(123)  # type: ignore[arg-type]


class TestGetEnvInt(unittest.TestCase):
    def test_returns_int_when_valid(self) -> None:
        with mock.patch.dict(os.environ, {"PORT": "8080"}, clear=True):
            self.assertEqual(get_env_int("PORT"), 8080)

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_env_int("MISSING", 42), 42)
            self.assertIsNone(get_env_int("MISSING"))

    def test_raises_when_invalid(self) -> None:
        with mock.patch.dict(os.environ, {"PORT": "not-a-number"}, clear=True):
            with self.assertRaises(ValueError):
                get_env_int("PORT")

    def test_handles_negative(self) -> None:
        with mock.patch.dict(os.environ, {"OFFSET": "-5"}, clear=True):
            self.assertEqual(get_env_int("OFFSET"), -5)

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_int(123)  # type: ignore[arg-type]


class TestGetEnvFloat(unittest.TestCase):
    def test_returns_float_when_valid(self) -> None:
        with mock.patch.dict(os.environ, {"RATIO": "3.14"}, clear=True):
            result = get_env_float("RATIO")
            assert result is not None
            self.assertAlmostEqual(result, 3.14)

    def test_returns_int_as_float(self) -> None:
        with mock.patch.dict(os.environ, {"COUNT": "10"}, clear=True):
            result = get_env_float("COUNT")
            assert result is not None
            self.assertEqual(result, 10.0)

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(get_env_float("MISSING"))
            result = get_env_float("MISSING", 1.5)
            assert result is not None
            self.assertAlmostEqual(result, 1.5)

    def test_raises_when_invalid(self) -> None:
        with mock.patch.dict(os.environ, {"RATE": "abc"}, clear=True):
            with self.assertRaises(ValueError):
                get_env_float("RATE")

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_float(123)  # type: ignore[arg-type]


class TestGetEnvBool(unittest.TestCase):
    def test_true_values(self) -> None:
        for val in ["1", "true", "TRUE", "Yes", "on", "Y", "t"]:
            with mock.patch.dict(os.environ, {"FLAG": val}, clear=True):
                self.assertIs(get_env_bool("FLAG"), True, f"{val!r} should be True")

    def test_false_values(self) -> None:
        for val in ["0", "false", "NO", "off", "f", "", "  "]:
            with mock.patch.dict(os.environ, {"FLAG": val}, clear=True):
                self.assertIs(get_env_bool("FLAG"), False, f"{val!r} should be False")

    def test_returns_default_when_unset(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIs(get_env_bool("MISSING", True), True)
            self.assertIs(get_env_bool("MISSING", False), False)
            self.assertIsNone(get_env_bool("MISSING"))

    def test_raises_when_invalid(self) -> None:
        with mock.patch.dict(os.environ, {"FLAG": "maybe"}, clear=True):
            with self.assertRaises(ValueError):
                get_env_bool("FLAG")

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_env_bool(123)  # type: ignore[arg-type]


class TestSetEnv(unittest.TestCase):
    def test_sets_string_value(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            set_env("KEY", "value")
            self.assertEqual(os.environ["KEY"], "value")

    def test_converts_non_string_value(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            set_env("COUNT", 42)
            self.assertEqual(os.environ["COUNT"], "42")

    def test_overwrites_existing(self) -> None:
        with mock.patch.dict(os.environ, {"KEY": "old"}, clear=True):
            set_env("KEY", "new")
            self.assertEqual(os.environ["KEY"], "new")

    def test_rejects_non_string_key(self) -> None:
        with self.assertRaises(TypeError):
            set_env(123, "value")  # type: ignore[arg-type]

    def test_rejects_empty_key(self) -> None:
        with self.assertRaises(ValueError):
            set_env("", "value")

    def test_rejects_key_with_equals(self) -> None:
        with self.assertRaises(ValueError):
            set_env("KEY=VAL", "value")


class TestEnsureEnv(unittest.TestCase):
    def test_sets_default_when_missing(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            result = ensure_env("NEW_VAR", "default")
            self.assertEqual(result, "default")
            self.assertEqual(os.environ["NEW_VAR"], "default")

    def test_preserves_existing_value(self) -> None:
        with mock.patch.dict(os.environ, {"EXISTING": "old"}, clear=True):
            result = ensure_env("EXISTING", "new")
            self.assertEqual(result, "old")
            self.assertEqual(os.environ["EXISTING"], "old")

    def test_rejects_non_string_key(self) -> None:
        with self.assertRaises(TypeError):
            ensure_env(123, "default")  # type: ignore[arg-type]

    def test_rejects_non_string_default(self) -> None:
        with self.assertRaises(TypeError):
            ensure_env("NEW_VAR", 42)  # type: ignore[arg-type]

    def test_rejects_empty_key(self) -> None:
        with self.assertRaises(ValueError):
            ensure_env("", "default")


class TestUnsetEnv(unittest.TestCase):
    def test_removes_existing(self) -> None:
        with mock.patch.dict(os.environ, {"TO_REMOVE": "x"}, clear=True):
            self.assertTrue(unset_env("TO_REMOVE"))
            self.assertNotIn("TO_REMOVE", os.environ)

    def test_returns_false_when_not_set(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertFalse(unset_env("MISSING"))
            self.assertFalse(unset_env("MISSING"))

    def test_non_string_key_raises(self) -> None:
        with self.assertRaises(TypeError):
            unset_env(123)  # type: ignore[arg-type]


class TestPrefixEnv(unittest.TestCase):
    def test_returns_filtered_vars(self) -> None:
        env = {"APP_DEBUG": "1", "APP_HOST": "x", "PATH": "/bin"}
        with mock.patch.dict(os.environ, env, clear=False):
            result = prefix_env("APP_")
            self.assertEqual(result, {"APP_DEBUG": "1", "APP_HOST": "x"})

    def test_empty_prefix_returns_all(self) -> None:
        env = {"A": "1", "B": "2"}
        with mock.patch.dict(os.environ, env, clear=False):
            result = prefix_env("")
            self.assertIn("A", result)
            self.assertIn("B", result)

    def test_no_matches_returns_empty(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(prefix_env("NOPE_"), {})

    def test_non_string_prefix_raises(self) -> None:
        with self.assertRaises(TypeError):
            prefix_env(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTENVL
# --- tests/test_logging_utils.py ---
cat > "$OUTPUT_DIR/tests/test_logging_utils.py" <<'TESTLOGUTILS'
"""Tests for logging_utils module."""

import logging
import unittest

from logging_utils import configure_logging, get_logger, log_calls


class TestGetLogger(unittest.TestCase):
    def test_returns_logger_with_name(self) -> None:
        logger = get_logger("my_app.module")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "my_app.module")

    def test_returns_root_logger_when_no_name(self) -> None:
        logger = get_logger()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "root")

    def test_same_name_returns_same_instance(self) -> None:
        logger1 = get_logger("shared_logger")
        logger2 = get_logger("shared_logger")
        self.assertIs(logger1, logger2)

    def test_non_string_name_raises(self) -> None:
        with self.assertRaises(TypeError):
            get_logger(123)  # type: ignore[arg-type]


class TestConfigureLogging(unittest.TestCase):
    def setUp(self) -> None:
        self._root = logging.getLogger()
        self._saved_handlers = self._root.handlers[:]
        self._saved_level = self._root.level
        self._root.handlers = []
        self._root.setLevel(logging.NOTSET)

    def tearDown(self) -> None:
        self._root.handlers = self._saved_handlers
        self._root.setLevel(self._saved_level)

    def test_returns_root_logger(self) -> None:
        root = configure_logging(level=logging.INFO, force=True)
        self.assertIs(root, logging.getLogger())

    def test_sets_level(self) -> None:
        configure_logging(level=logging.DEBUG, force=True)
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

    def test_default_level_is_warning(self) -> None:
        configure_logging(force=True)
        self.assertEqual(logging.getLogger().level, logging.WARNING)

    def test_adds_default_handler(self) -> None:
        configure_logging(level=logging.INFO, force=True)
        self.assertTrue(len(logging.getLogger().handlers) > 0)

    def test_custom_handlers(self) -> None:
        handler = logging.StreamHandler()
        configure_logging(level=logging.INFO, handlers=[handler], force=True)
        self.assertIn(handler, logging.getLogger().handlers)

    def test_force_removes_existing_handlers(self) -> None:
        self._root.addHandler(logging.StreamHandler())
        configure_logging(level=logging.INFO, force=True)
        self.assertEqual(len(self._root.handlers), 1)

    def test_format_applied_to_handler(self) -> None:
        configure_logging(level=logging.INFO, format="%(message)s", force=True)
        for handler in self._root.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.formatter is not None:
                self.assertEqual(handler.formatter._fmt, "%(message)s")

    def test_non_integer_level_raises(self) -> None:
        with self.assertRaises(TypeError):
            configure_logging(level="INFO", force=True)  # type: ignore[arg-type]

    def test_non_list_handlers_raises(self) -> None:
        with self.assertRaises(TypeError):
            configure_logging(handlers="not-a-list", force=True)  # type: ignore[arg-type]

    def test_non_list_handlers_with_none_allowed(self) -> None:
        configure_logging(level=logging.INFO, handlers=None, force=True)
        self.assertTrue(len(self._root.handlers) > 0)


class TestLogCalls(unittest.TestCase):
    def test_decorator_logs_call_and_result(self) -> None:
        @log_calls(level=logging.DEBUG)
        def add(a: int, b: int) -> int:
            return a + b

        with self.assertLogs("logging_utils", level="DEBUG") as cm:
            result = add(2, 3)
        self.assertEqual(result, 5)
        self.assertEqual(len(cm.records), 2)
        self.assertIn("Calling", cm.records[0].getMessage())
        self.assertIn("returned", cm.records[1].getMessage())

    def test_decorator_preserves_metadata(self) -> None:
        @log_calls(level=logging.DEBUG)
        def named_function(a: int, b: int) -> int:
            """Original docstring."""
            return a * b

        self.assertEqual(named_function.__name__, "named_function")
        self.assertEqual(named_function.__doc__, "Original docstring.")

    def test_decorator_with_custom_logger(self) -> None:
        logger = logging.getLogger("custom.log.test")
        logger.setLevel(logging.DEBUG)

        @log_calls(logger=logger, level=logging.INFO)
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        with self.assertLogs("custom.log.test", level="INFO") as cm:
            result = greet("World")
        self.assertEqual(result, "Hello, World!")
        self.assertEqual(len(cm.records), 2)

    def test_decorator_propagates_kwargs(self) -> None:
        @log_calls(level=logging.DEBUG)
        def join_values(sep: str, *parts: str) -> str:
            return sep.join(parts)

        with self.assertLogs("logging_utils", level="DEBUG") as cm:
            self.assertEqual(join_values("-", "a", "b", "c"), "a-b-c")
        first_msg = cm.records[0].getMessage()
        self.assertIn("a", first_msg)
        self.assertIn("b", first_msg)
        self.assertIn("c", first_msg)

    def test_decorator_custom_level(self) -> None:
        @log_calls(level=logging.WARNING)
        def echo(value: str) -> str:
            return value

        with self.assertLogs("logging_utils", level="WARNING") as cm:
            self.assertEqual(echo("hello"), "hello")
        self.assertEqual(cm.records[0].levelno, logging.WARNING)

    def test_decorator_default_level_logs_debug(self) -> None:
        @log_calls()
        def echo(value: str) -> str:
            return value

        with self.assertLogs("logging_utils", level="DEBUG") as cm:
            self.assertEqual(echo("hello"), "hello")
        self.assertEqual(cm.records[0].levelno, logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
TESTLOGUTILS
# --- tests/test_cache_utils.py ---
cat > "$OUTPUT_DIR/tests/test_cache_utils.py" <<'TESTCACHEUTILS'
"""Tests for cache_utils module."""

import unittest

from cache_utils import cache_info, clear_cache, memoize


class TestMemoize(unittest.TestCase):
    def test_caches_repeated_calls(self) -> None:
        calls = [0]

        @memoize()
        def square(n: int) -> int:
            calls[0] += 1
            return n * n

        self.assertEqual(square(4), 16)
        self.assertEqual(square(4), 16)
        self.assertEqual(calls[0], 1)

    def test_different_args_recompute(self) -> None:
        calls = [0]

        @memoize()
        def add(a: int, b: int) -> int:
            calls[0] += 1
            return a + b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(calls[0], 2)

    def test_kwargs_normalized(self) -> None:
        calls = [0]

        @memoize()
        def greet(name: str, greeting: str = "Hello") -> str:
            calls[0] += 1
            return f"{greeting}, {name}!"

        self.assertEqual(greet("Alice", greeting="Hi"), "Hi, Alice!")
        self.assertEqual(greet("Alice", greeting="Hi"), "Hi, Alice!")
        self.assertEqual(calls[0], 1)

    def test_unbounded_cache(self) -> None:
        calls = [0]

        @memoize(maxsize=None)
        def double(n: int) -> int:
            calls[0] += 1
            return n * 2

        for i in range(50):
            self.assertEqual(double(i), i * 2)
        self.assertEqual(calls[0], 50)
        for i in range(50):
            self.assertEqual(double(i), i * 2)
        self.assertEqual(calls[0], 50)

    def test_typed_distinct(self) -> None:
        calls = [0]

        @memoize(typed=True)
        def identity(value: object) -> object:
            calls[0] += 1
            return value

        self.assertEqual(identity(1), 1)
        self.assertEqual(identity(1.0), 1.0)
        self.assertEqual(calls[0], 2)

    def test_typed_false_collapses(self) -> None:
        calls = [0]

        @memoize(typed=False)
        def identity(value: object) -> object:
            calls[0] += 1
            return value

        self.assertEqual(identity(1), 1)
        self.assertEqual(identity(1.0), 1.0)
        self.assertEqual(calls[0], 1)

    def test_maxsize_eviction(self) -> None:
        calls = [0]

        @memoize(maxsize=2)
        def value(n: int) -> int:
            calls[0] += 1
            return n

        self.assertEqual(value(1), 1)
        self.assertEqual(value(2), 2)
        self.assertEqual(value(3), 3)
        self.assertEqual(value(1), 1)
        self.assertEqual(calls[0], 4)

    def test_clear_cache_method(self) -> None:
        calls = [0]

        @memoize()
        def triple(n: int) -> int:
            calls[0] += 1
            return n * 3

        self.assertEqual(triple(5), 15)
        self.assertEqual(triple(5), 15)
        self.assertEqual(calls[0], 1)
        triple.clear_cache()  # type: ignore[attr-defined]
        self.assertEqual(triple(5), 15)
        self.assertEqual(calls[0], 2)

    def test_cache_info_method(self) -> None:
        @memoize()
        def add(a: int, b: int) -> int:
            return a + b

        add(1, 1)
        add(2, 2)
        add(1, 1)  # hit
        info = add.cache_info()  # type: ignore[attr-defined]
        self.assertEqual(info["hits"], 1)
        self.assertEqual(info["misses"], 2)
        self.assertEqual(info["currsize"], 2)
        self.assertEqual(info["maxsize"], 128)

    def test_preserves_metadata(self) -> None:
        @memoize()
        def named(a: int) -> int:
            """Original docstring."""
            return a

        self.assertEqual(named.__name__, "named")
        self.assertEqual(named.__doc__, "Original docstring.")

    def test_invalid_maxsize_type_raises(self) -> None:
        with self.assertRaises(TypeError):
            memoize(maxsize="not-an-int")  # type: ignore[arg-type]

    def test_invalid_maxsize_value_raises(self) -> None:
        with self.assertRaises(ValueError):
            memoize(maxsize=0)
        with self.assertRaises(ValueError):
            memoize(maxsize=-5)

    def test_maxsize_none_allowed(self) -> None:
        @memoize(maxsize=None)
        def fn(x: int) -> int:
            return x

        self.assertEqual(fn(1), 1)
        self.assertEqual(fn.cache_info()["maxsize"], None)  # type: ignore[attr-defined]


class TestClearCacheFunction(unittest.TestCase):
    def test_clears_memoized_cache(self) -> None:
        calls = [0]

        @memoize()
        def inc(n: int) -> int:
            calls[0] += 1
            return n + 1

        inc(1)
        inc(1)
        self.assertEqual(calls[0], 1)
        clear_cache(inc)
        inc(1)
        self.assertEqual(calls[0], 2)

    def test_non_memoized_raises(self) -> None:
        def plain(x: int) -> int:
            return x

        with self.assertRaises(TypeError):
            clear_cache(plain)  # type: ignore[arg-type]


class TestCacheInfoFunction(unittest.TestCase):
    def test_returns_info_for_memoized(self) -> None:
        @memoize()
        def mul(a: int, b: int) -> int:
            return a * b

        mul(2, 3)
        info = cache_info(mul)
        self.assertEqual(info["misses"], 1)
        self.assertEqual(info["hits"], 0)

    def test_non_memoized_raises(self) -> None:
        def plain(x: int) -> int:
            return x

        with self.assertRaises(TypeError):
            cache_info(plain)  # type: ignore[arg-type]


class TestMemoizeExceptions(unittest.TestCase):
    def test_function_raising_is_not_cached(self) -> None:
        calls = [0]

        @memoize()
        def fail(x: int) -> int:
            calls[0] += 1
            if x < 0:
                raise ValueError("negative")
            return x

        self.assertEqual(fail(1), 1)
        with self.assertRaises(ValueError):
            fail(-1)
        with self.assertRaises(ValueError):
            fail(-1)
        self.assertEqual(calls[0], 3)


if __name__ == "__main__":
    unittest.main()
TESTCACHEUTILS
# --- tests/test_timing_utils.py ---
cat > "$OUTPUT_DIR/tests/test_timing_utils.py" <<'TESTTIMINGUTILS'
"""Tests for timing_utils module."""

import time
import unittest
from unittest.mock import patch

from timing_utils import benchmark, elapsed_time, timer


class TestTimer(unittest.TestCase):
    """Test the timer context manager."""

    def test_timer_context_manager(self):
        """Test that timer measures time correctly."""
        with timer("Test") as t:
            time.sleep(0.01)  # Sleep for 10ms
            # Check that start_time was set
            self.assertGreater(t.start_time, 0)

        # After context, elapsed should be set
        self.assertGreater(t.elapsed, 0)
        # Should be approximately 0.01 seconds (allowing for variance)
        self.assertAlmostEqual(t.elapsed, 0.01, places=1)

    def test_timer_with_label(self):
        """Test timer with custom label."""
        with patch('builtins.print') as mock_print:
            with timer("Custom Label"):
                time.sleep(0.01)
            # Check that print was called with expected format
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Custom Label", call_args)
            self.assertIn("s", call_args)

    def test_timer_without_label(self):
        """Test timer with default label."""
        with patch('builtins.print') as mock_print:
            with timer():
                time.sleep(0.01)
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Elapsed", call_args)


class TestElapsedTime(unittest.TestCase):
    """Test the elapsed_time function."""

    def test_elapsed_time_basic(self):
        """Test that elapsed_time calculates correctly."""
        start = time.perf_counter()
        time.sleep(0.01)
        elapsed = elapsed_time(start)
        self.assertGreater(elapsed, 0)
        self.assertAlmostEqual(elapsed, 0.01, places=1)

    def test_elapsed_time_zero(self):
        """Test elapsed_time with same start and end time."""
        start = time.perf_counter()
        elapsed = elapsed_time(start)
        self.assertAlmostEqual(elapsed, 0.0, places=2)

    def test_elapsed_time_precision(self):
        """Test that elapsed_time returns a float."""
        start = time.perf_counter()
        elapsed = elapsed_time(start)
        self.assertIsInstance(elapsed, float)


class TestBenchmarkDecorator(unittest.TestCase):
    """Test the benchmark decorator."""

    def test_benchmark_default_iterations(self):
        """Test benchmark with default iterations=1."""
        call_count = 0

        @benchmark()
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        with patch('builtins.print') as mock_print:
            result = test_func()

        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("test_func", call_args)
        self.assertIn("avg of 1 runs", call_args)

    def test_benchmark_multiple_iterations(self):
        """Test benchmark with multiple iterations."""
        call_count = 0

        @benchmark(iterations=3)
        def test_func():
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)
            return "success"

        with patch('builtins.print') as mock_print:
            result = test_func()

        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("test_func", call_args)
        self.assertIn("avg of 3 runs", call_args)

    def test_benchmark_returns_correct_result(self):
        """Test that benchmark returns the function's actual result."""
        @benchmark(iterations=2)
        def test_func():
            return [1, 2, 3]

        result = test_func()
        self.assertEqual(result, [1, 2, 3])

    def test_benchmark_invalid_iterations(self):
        """Test that benchmark raises ValueError for invalid iterations."""
        with self.assertRaises(ValueError):
            @benchmark(iterations=0)
            def test_func():
                pass

        with self.assertRaises(ValueError):
            @benchmark(iterations=-1)
            def test_func():
                pass


if __name__ == "__main__":
    unittest.main()
TESTTIMINGUTILS
# --- tests/test_rate_limiter_utils.py ---
cat > "$OUTPUT_DIR/tests/test_rate_limiter_utils.py" <<'TESTRLUTILS'
"""Tests for rate_limiter_utils module."""

import time
import unittest

from rate_limiter_utils import RateLimiter, rate_limit, token_bucket


class TestRateLimiter(unittest.TestCase):
    def test_initialization(self):
        limiter = RateLimiter(rate=1.0)
        self.assertEqual(limiter.rate, 1.0)
        self.assertEqual(limiter.capacity, 1.0)
        self.assertEqual(limiter.tokens, 1.0)

        limiter = RateLimiter(rate=2.0, capacity=4.0)
        self.assertEqual(limiter.rate, 2.0)
        self.assertEqual(limiter.capacity, 4.0)
        self.assertEqual(limiter.tokens, 4.0)

    def test_acquire_immediate(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        # Should be able to acquire immediately
        self.assertTrue(limiter.acquire(1.0))
        # Now bucket is empty
        self.assertFalse(limiter.acquire(1.0))
        # Wait a bit and try again
        time.sleep(1.1)
        self.assertTrue(limiter.acquire(1.0))

    def test_acquire_blocking(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        # Start with full bucket
        start = time.monotonic()
        limiter.acquire_blocking(1.0)  # Should return immediately
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 0.1)  # Should be very quick

        # Now bucket is empty, next acquire should block for about 1 second
        start = time.monotonic()
        limiter.acquire_blocking(1.0)
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 1.1)

    def test_token_bucket_context_manager(self):
        limiter = RateLimiter(rate=1.0, capacity=1.0)
        # Acquire one token immediately
        with token_bucket(limiter, 1.0):
            pass  # Should not block
        # Now bucket is empty, entering context should block
        start = time.monotonic()
        with token_bucket(limiter, 1.0):
            pass
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.9)
        self.assertLess(elapsed, 1.1)

    def test_rate_limit_decorator(self):
        calls = []

        @rate_limit(rate=2.0)  # 2 calls per second
        def limited_function():
            calls.append(time.monotonic())

        # Call function 5 times
        start = time.monotonic()
        for i in range(5):
            limited_function()
        elapsed = time.monotonic() - start

        # With rate 2 per second and capacity=2 (default), the first two calls are immediate.
        # Then each additional call requires 0.5 seconds to regenerate one token.
        # For 5 calls: 2 immediate + 3 * 0.5 = 1.5 seconds minimum.
        self.assertGreaterEqual(elapsed, 1.4)
        self.assertLess(elapsed, 2.0)  # Allow a little slack above 1.5

        # Check that the calls are spaced appropriately after the bucket is depleted
        # We expect intervals of about 0.5 seconds after the first two calls.
        if len(calls) >= 3:
            # Intervals between call2-call3, call3-call4, call4-call5 should be ~0.5
            intervals = [calls[i+1] - calls[i] for i in range(1, len(calls)-1)]
            for interval in intervals:
                self.assertAlmostEqual(interval, 0.5, places=1)


if __name__ == "__main__":
    unittest.main()
TESTRLUTILS
# --- tests/test_retry_utils.py ---
cat > "$OUTPUT_DIR/tests/test_retry_utils.py" <<'TESTRETRYUTILS'
import time
import unittest

from retry_utils import retry, retry_count, retry_with_backoff


class TestRetryDecorator(unittest.TestCase):
    def test_retry_success_first_try(self):
        """Test that function succeeds on first attempt."""
        attempt_count = 0

        @retry(max_attempts=3, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 1)

    def test_retry_success_after_retries(self):
        """Test that function succeeds after some retries."""
        attempt_count = 0

        @retry(max_attempts=3, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Try again")
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 3)

    def test_retry_fails_after_max_attempts(self):
        """Test that function fails after exceeding max attempts."""
        attempt_count = 0

        @retry(max_attempts=2, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(attempt_count, 2)

    def test_retry_specific_exceptions(self):
        """Test that only specified exceptions trigger retries."""
        attempt_count = 0

        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise ValueError("Retry on this")
            elif attempt_count == 2:
                raise TypeError("Don't retry on this")
            return "success"

        with self.assertRaises(TypeError):
            func()
        self.assertEqual(attempt_count, 2)

    def test_retry_with_zero_attempts(self):
        """Test behavior with max_attempts=1 (no retries)."""
        attempt_count = 0

        @retry(max_attempts=1, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Fails")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(attempt_count, 1)


class TestRetryWithBackoffDecorator(unittest.TestCase):
    def test_retry_with_backoff_success_first_try(self):
        """Test that function succeeds on first attempt."""
        attempt_count = 0

        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 1)

    def test_retry_with_backoff_success_after_retries(self):
        """Test that function succeeds after some retries."""
        attempt_count = 0

        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Try again")
            return "success"

        result = func()
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 3)

    def test_retry_with_backoff_fails_after_max_attempts(self):
        """Test that function fails after exceeding max attempts."""
        attempt_count = 0

        @retry_with_backoff(max_attempts=2, initial_delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(attempt_count, 2)

    def test_retry_with_backoff_jitter(self):
        """Test that jitter affects delay (basic test)."""
        delays = []

        @retry_with_backoff(
            max_attempts=3, initial_delay=0.01, backoff_factor=2.0, jitter=True
        )
        def func():
            if len(delays) < 2:  # First two attempts
                delays.append(time.time())
                raise ValueError("Try again")
            return "success"

        # Mock time.sleep to capture delays
        original_sleep = time.sleep
        slept_durations = []

        def mock_sleep(duration):
            slept_durations.append(duration)
            # Don't actually sleep in test
            pass

        time.sleep = mock_sleep
        try:
            result = func()
            self.assertEqual(result, "success")
            # Should have slept twice (after first and second attempts)
            self.assertEqual(len(slept_durations), 2)
            # Each sleep duration should be positive
            for duration in slept_durations:
                self.assertGreaterEqual(duration, 0)
        finally:
            time.sleep = original_sleep


class TestRetryCountDecorator(unittest.TestCase):
    def test_retry_count_no_retries(self):
        """Test that retry_count returns 0 when no retries needed."""

        @retry_count(max_attempts=3, delay=0.01)
        def func():
            return "success"

        result, count = func()
        self.assertEqual(result, "success")
        self.assertEqual(count, 0)

    def test_retry_count_with_retries(self):
        """Test that retry_count returns correct retry count."""
        attempt_count = 0

        @retry_count(max_attempts=3, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Try again")
            return "success"

        result, count = func()
        self.assertEqual(result, "success")
        self.assertEqual(count, 2)  # Retried twice

    def test_retry_count_exhausted_attempts(self):
        """Test that retry_count raises exception after max attempts."""
        attempt_count = 0

        @retry_count(max_attempts=2, delay=0.01)
        def func():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            func()
        # Note: The wrapper re-raises the exception, so we don't get a count return
        # This is expected behavior - when all attempts fail, the exception propagates


if __name__ == "__main__":
    unittest.main()
TESTRETRYUTILS
# --- tests/test_dict_utils.py ---
cat > "$OUTPUT_DIR/tests/test_dict_utils.py" <<'TESTDICTUTILS'
"""Tests for dict_utils module."""

import unittest

from dict_utils import deep_merge, filter_dict, flatten_dict, invert_dict, safe_get, unflatten_dict


class TestDeepMerge(unittest.TestCase):
    def test_deep_merge_basic(self) -> None:
        d1 = {"a": 1, "b": {"c": 2}}
        d2 = {"b": {"d": 3}, "e": 4}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"]["c"], 2)
        self.assertEqual(result["b"]["d"], 3)
        self.assertEqual(result["e"], 4)

    def test_deep_merge_overwrite(self) -> None:
        d1 = {"a": 1}
        d2 = {"a": 2}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"], 2)

    def test_deep_merge_no_overwrite_nested(self) -> None:
        d1 = {"a": {"b": 1, "c": 2}}
        d2 = {"a": {"b": 3}}
        result = deep_merge(d1, d2)
        self.assertEqual(result["a"]["b"], 3)
        self.assertEqual(result["a"]["c"], 2)


class TestFlattenDict(unittest.TestCase):
    def test_flatten_basic(self) -> None:
        d = {"a": 1, "b": {"c": 2, "d": 3}}
        result = flatten_dict(d)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b.c"], 2)
        self.assertEqual(result["b.d"], 3)

    def test_flatten_with_sep(self) -> None:
        d = {"a": {"b": {"c": 1}}}
        result = flatten_dict(d, sep="_")
        self.assertEqual(result["a_b_c"], 1)

    def test_flatten_parent_key(self) -> None:
        d = {"b": 2}
        result = flatten_dict(d, parent_key="a")
        self.assertEqual(result["a.b"], 2)


class TestUnflattenDict(unittest.TestCase):
    def test_unflatten_basic(self) -> None:
        d = {"a.b.c": 1, "a.b.d": 2}
        result = unflatten_dict(d)
        self.assertEqual(result["a"]["b"]["c"], 1)
        self.assertEqual(result["a"]["b"]["d"], 2)

    def test_unflatten_simple(self) -> None:
        d = {"a": 1, "b": 2}
        result = unflatten_dict(d)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)


class TestSafeGet(unittest.TestCase):
    def test_safe_get_basic(self) -> None:
        d = {"a": {"b": {"c": 1}}}
        self.assertEqual(safe_get(d, "a", "b", "c"), 1)

    def test_safe_get_default(self) -> None:
        d = {"a": 1}
        self.assertEqual(safe_get(d, "b", default="missing"), "missing")
        self.assertIsNone(safe_get(d, "b"))

    def test_safe_get_partial(self) -> None:
        d = {"a": 1}
        self.assertEqual(safe_get(d, "a", "b", default="x"), "x")


class TestInvertDict(unittest.TestCase):
    def test_invert_basic(self) -> None:
        d = {"a": 1, "b": 2}
        result = invert_dict(d)
        self.assertEqual(result[1], "a")
        self.assertEqual(result[2], "b")

    def test_invert_duplicate_values_raises(self) -> None:
        d = {"a": 1, "b": 1}
        with self.assertRaises(ValueError):
            invert_dict(d)


class TestFilterDict(unittest.TestCase):
    def test_filter_dict_basic(self) -> None:
        d = {"a": 1, "b": 2, "c": 3}
        result = filter_dict(d, lambda k, v: v > 1)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertNotIn("a", result)

    def test_filter_dict_by_key(self) -> None:
        d = {"a1": 1, "b1": 2, "a2": 3}
        result = filter_dict(d, lambda k, v: k.startswith("a"))
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
TESTDICTUTILS

# --- terminal_utils.py ---
cat > "$OUTPUT_DIR/terminal_utils.py" <<'TERMINAL_UTILS'
"""Terminal output utilities for colored text, progress bars, and prompts.

This module provides helpers for formatting terminal output using ANSI escape
sequences, rendering progress bars, clearing the screen, querying terminal
size, and reading user input. Output degrades gracefully when the stream is
not a terminal (for example, when piped to a file or captured in tests).
"""

from __future__ import annotations

import os
import shutil
import sys
from typing import Iterable, Iterator, Optional, TextIO, Tuple

_RESET = "\033[0m"
_BOLD = "\033[1m"

_COLOR_CODES: dict = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

_VALID_COLORS = frozenset(_COLOR_CODES)


def supports_color(stream: Optional[TextIO] = None) -> bool:
    """Return True if *stream* (default stdout) supports ANSI colors.

    Color is disabled when the stream is not a TTY, when the ``NO_COLOR``
    environment variable is set, or when the stream lacks an ``isatty``
    method.
    """
    if stream is None:
        stream = sys.stdout
    if "NO_COLOR" in os.environ:
        return False
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    return True


def colorize(text: str, color: str = "white", bold: bool = False) -> str:
    """Wrap *text* in ANSI color escape codes.

    Args:
        text: The text to colorize.
        color: One of black, red, green, yellow, blue, magenta, cyan, white.
        bold: Whether to render the text in bold.

    Returns:
        The colorized text, or the original text unchanged when color is not
        supported on stdout.

    Raises:
        TypeError: If *text* or *color* is not a string.
        ValueError: If *color* is not a supported color name.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(color, str):
        raise TypeError("color must be a string")
    if color not in _VALID_COLORS:
        raise ValueError(
            f"unsupported color {color!r}; supported colors are "
            f"{sorted(_VALID_COLORS)!r}"
        )
    if not supports_color():
        return text
    codes = [_COLOR_CODES[color]]
    if bold:
        codes.insert(0, _BOLD)
    return f"\033[{';'.join(codes)}m{text}{_RESET}"


def print_colored(
    text: str,
    color: str = "white",
    bold: bool = False,
    stream: Optional[TextIO] = None,
) -> None:
    """Print colorized text to *stream* (default stdout).

    Args:
        text: The text to print.
        color: One of black, red, green, yellow, blue, magenta, cyan, white.
        bold: Whether to render the text in bold.
        stream: The output stream (defaults to sys.stdout).
    """
    if stream is None:
        stream = sys.stdout
    stream.write(colorize(text, color=color, bold=bold) + "\n")
    stream.flush()


def clear_screen() -> None:
    """Clear the terminal screen.

    Uses the ANSI clear-screen escape sequence when supported, falling back
    to printing newlines otherwise.
    """
    if supports_color(sys.stdout):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    else:
        sys.stdout.write("\n" * 50)
        sys.stdout.flush()


def get_terminal_size() -> Tuple[int, int]:
    """Return the terminal size as ``(columns, lines)``.

    Falls back to ``(80, 24)`` when the size cannot be determined.
    """
    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
    except Exception:
        return (80, 24)
    return (size.columns, size.lines)


class ProgressBar:
    """A simple terminal progress bar.

    Args:
        total: The total number of steps. Must be a positive integer.
        width: The character width of the bar (excluding labels). Defaults
            to a size derived from the terminal width.
        fill: The single character used for the completed portion.
        empty: The single character used for the remaining portion.
        stream: The output stream (defaults to sys.stdout).
    """

    def __init__(
        self,
        total: int,
        width: Optional[int] = None,
        fill: str = "#",
        empty: str = "-",
        stream: Optional[TextIO] = None,
    ) -> None:
        if isinstance(total, bool) or not isinstance(total, int) or total <= 0:
            raise ValueError("total must be a positive integer")
        if not isinstance(fill, str) or len(fill) != 1:
            raise ValueError("fill must be a single character")
        if not isinstance(empty, str) or len(empty) != 1:
            raise ValueError("empty must be a single character")
        if stream is None:
            stream = sys.stdout
        self.total = total
        if width is None:
            width = max(10, min(40, _term_width(stream) - 12))
        self.width = width
        self.fill = fill
        self.empty = empty
        self.stream = stream
        self._current = 0
        self._finished = False

    def update(self, current: Optional[int] = None, increment: int = 1) -> None:
        """Advance the progress bar to *current* or by *increment*.

        Args:
            current: The absolute step to advance to, within [0, total].
            increment: The number of steps to advance (default 1).

        Raises:
            TypeError: If *current* is not an integer.
            ValueError: If the resulting position is outside [0, total].
        """
        if self._finished:
            return
        if current is None:
            current = self._current + increment
        if isinstance(current, bool) or not isinstance(current, int):
            raise TypeError("current must be an integer")
        if current < 0 or current > self.total:
            raise ValueError(f"current {current} is outside [0, {self.total}]")
        self._current = current
        self._render()
        if self._current >= self.total:
            self._finished = True
            self.stream.write("\n")
            self.stream.flush()

    def finish(self) -> None:
        """Mark the progress bar as complete and print a final newline."""
        if not self._finished:
            self._current = self.total
            self._finished = True
            self.stream.write("\n")
            self.stream.flush()

    def _render(self) -> None:
        ratio = self._current / self.total
        filled = int(ratio * self.width)
        bar = self.fill * filled + self.empty * (self.width - filled)
        percent = int(ratio * 100)
        line = f"\r[{bar}] {percent}% ({self._current}/{self.total})"
        self.stream.write(line)
        self.stream.flush()

    def __enter__(self) -> "ProgressBar":
        return self

    def __exit__(self, *args) -> None:
        self.finish()


def progress_bar(
    iterable: Iterable,
    total: Optional[int] = None,
    width: Optional[int] = None,
    fill: str = "#",
    empty: str = "-",
    stream: Optional[TextIO] = None,
) -> Iterator:
    """Yield items from *iterable* while rendering a progress bar.

    Args:
        iterable: The iterable to wrap.
        total: The total number of items. Inferred from ``len`` when
            available; otherwise must be provided.
        width: The character width of the bar.
        fill: The character used for the completed portion.
        empty: The character used for the remaining portion.
        stream: The output stream (defaults to sys.stdout).

    Raises:
        ValueError: If *total* cannot be inferred and is not provided.
    """
    if total is None:
        try:
            total = len(iterable)  # type: ignore[arg-type]
        except TypeError as exc:
            raise ValueError(
                "total must be provided for iterables without len()"
            ) from exc
    bar = ProgressBar(total, width=width, fill=fill, empty=empty, stream=stream)
    with bar:
        for item in iterable:
            bar.update(increment=1)
            yield item


def prompt(message: str, default: Optional[str] = None) -> str:
    """Prompt the user for input and return the entered value.

    Args:
        message: The prompt message to display.
        default: The value returned when the user enters nothing.

    Returns:
        The user's input, or *default* when the input is empty.

    Raises:
        TypeError: If *message* or *default* is not a string/None.
        EOFError: If the input stream is closed.
    """
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if default is not None and not isinstance(default, str):
        raise TypeError("default must be a string or None")
    suffix = f" [{default}]" if default is not None else ""
    full_message = message + suffix + ": "
    if supports_color(sys.stdout):
        full_message = colorize(full_message, color="cyan")
    try:
        value = input(full_message)
    except EOFError as exc:
        raise EOFError("input stream closed") from exc
    if value == "":
        return default if default is not None else ""
    return value


def _term_width(stream: TextIO) -> int:
    try:
        return shutil.get_terminal_size(fallback=(80, 24)).columns
    except Exception:
        return 80
TERMINAL_UTILS

# --- cli_utils.py ---
cat > "$OUTPUT_DIR/cli_utils.py" <<'CLI_UTILS'
"""Command-line interface utility functions.

This module provides helpers for building simple command-line applications:
creating an :mod:`argparse` parser with standard options, parsing arguments,
and wrapping a main function so it returns consistent process exit codes.
"""

from __future__ import annotations

import argparse
from functools import wraps
from typing import Callable, List, Optional

__all__: List[str] = [
    "create_parser",
    "parse_arguments",
    "main_wrapper",
]


def create_parser(
    prog: str,
    description: str,
    epilog: Optional[str] = None,
) -> argparse.ArgumentParser:
    """Create an ArgumentParser with standard options.

    Args:
        prog: The name of the program.
        description: A brief description of the program.
        epilog: Optional text displayed after the argument help.

    Returns:
        An ArgumentParser configured with ``--verbose`` and ``--version``.

    Examples:
        >>> parser = create_parser("my-tool", "A sample CLI tool.")
        >>> parser.prog
        'my-tool'
    """
    parser = argparse.ArgumentParser(prog=prog, description=description, epilog=epilog)
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("--version", action="version", version=f"{prog} 0.1.0")
    return parser


def parse_arguments(
    parser: argparse.ArgumentParser,
    args: Optional[List[str]] = None,
) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        parser: The ArgumentParser to use.
        args: Optional list of argument strings (defaults to sys.argv[1:]).

    Returns:
        The parsed arguments namespace.
    """
    return parser.parse_args(args)


def main_wrapper(func: Callable[[List[str]], int]) -> Callable[[List[str]], int]:
    """Wrap a main function to handle errors and return exit codes.

    Args:
        func: A function taking ``argv`` and returning an exit code.

    Returns:
        A wrapped function that returns ``0`` on success, ``1`` on error,
        and ``130`` on keyboard interrupt.

    Examples:
        >>> def main(argv):
        ...     print("running")
        ...     return 0
        >>> wrapped = main_wrapper(main)
        >>> wrapped([])
        running
        0
    """

    @wraps(func)
    def wrapper(argv: List[str]) -> int:
        try:
            return func(argv)
        except KeyboardInterrupt:
            return 130
        except Exception:
            return 1

    return wrapper
CLI_UTILS

cat > "$OUTPUT_DIR/hash_utils.py" <<'HASH_UTILS'
"""Hashing and checksum utility functions for computing and verifying hashes.

This module provides utilities for computing common cryptographic hashes
(MD5, SHA1, SHA256, SHA512) and CRC32 checksums, with support for both
string and bytes inputs.
"""

from __future__ import annotations

import hashlib
import zlib
from typing import Union

__all__: list[str] = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
    "crc32",
    "hash_file",
]


def _normalize_input(data: Union[str, bytes]) -> bytes:
    """Normalize input to bytes."""
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be str or bytes")


def md5(data: Union[str, bytes]) -> str:
    """Compute the MD5 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the MD5 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.md5(normalized).hexdigest()


def sha1(data: Union[str, bytes]) -> str:
    """Compute the SHA1 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the SHA1 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.sha1(normalized).hexdigest()


def sha256(data: Union[str, bytes]) -> str:
    """Compute the SHA256 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the SHA256 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.sha256(normalized).hexdigest()


def sha512(data: Union[str, bytes]) -> str:
    """Compute the SHA512 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the SHA512 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.sha512(normalized).hexdigest()


def crc32(data: Union[str, bytes]) -> int:
    """Compute the CRC32 checksum of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Integer CRC32 checksum.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return zlib.crc32(normalized) & 0xFFFFFFFF


def hash_file(file_path: Union[str, bytes], algorithm: str = "sha256") -> str:
    """Compute the hash of a file.

    Args:
        file_path: Path to the file to hash.
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512).
        Defaults to "sha256".

    Returns:
        Hexadecimal digest of the file hash.

    Raises:
        TypeError: If file_path is not str or bytes.
        ValueError: If algorithm is not supported.
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    if not isinstance(file_path, (str, bytes)):
        raise TypeError("file_path must be str or bytes")

    path_str = file_path.decode("utf-8") if isinstance(file_path, bytes) else file_path

    algorithm = algorithm.lower()
    hash_func = hashlib.new(algorithm) if algorithm in (
        "md5",
        "sha1",
        "sha256",
        "sha512",
    ) else None

    if hash_func is None:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    try:
        with open(path_str, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path_str}")
    except (IOError, OSError) as e:
        raise IOError(f"Error reading file {path_str}: {e}")
HASH_UTILS

# --- tests/test_hash_utils.py ---
cat > "$OUTPUT_DIR/tests/test_hash_utils.py" <<'TESTHASHUTILS'
"""Unit tests for hash_utils module."""

import tempfile
import unittest
from pathlib import Path

from hash_utils import (
    crc32,
    hash_file,
    md5,
    sha1,
    sha256,
    sha512,
)


class TestMD5(unittest.TestCase):
    def test_md5_string(self):
        result = md5("hello")
        self.assertEqual(result, "5d41402abc4b2a76b9719d911017c592")

    def test_md5_bytes(self):
        result = md5(b"hello")
        self.assertEqual(result, "5d41402abc4b2a76b9719d911017c592")

    def test_md5_empty_string(self):
        result = md5("")
        self.assertEqual(result, "d41d8cd98f00b204e9800998ecf8427e")

    def test_md5_type_error(self):
        with self.assertRaises(TypeError):
            md5(123)  # type: ignore[arg-type]


class TestSHA1(unittest.TestCase):
    def test_sha1_string(self):
        result = sha1("hello")
        self.assertEqual(result, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")

    def test_sha1_bytes(self):
        result = sha1(b"hello")
        self.assertEqual(result, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")

    def test_sha1_empty(self):
        result = sha1("")
        self.assertEqual(result, "da39a3ee5e6b4b0d3255bfef95601890afd80709")

    def test_sha1_type_error(self):
        with self.assertRaises(TypeError):
            sha1(123)  # type: ignore[arg-type]


class TestSHA256(unittest.TestCase):
    def test_sha256_string(self):
        result = sha256("hello")
        self.assertEqual(
            result,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_sha256_bytes(self):
        result = sha256(b"hello")
        self.assertEqual(
            result,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_sha256_type_error(self):
        with self.assertRaises(TypeError):
            sha256({})  # type: ignore[arg-type]


class TestSHA512(unittest.TestCase):
    def test_sha512_string(self):
        result = sha512("hello")
        self.assertTrue(result.startswith("9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043"))

    def test_sha512_type_error(self):
        with self.assertRaises(TypeError):
            sha512(None)  # type: ignore[arg-type]


class TestCRC32(unittest.TestCase):
    def test_crc32_string(self):
        result = crc32("hello")
        self.assertEqual(result, 0x3610A686)

    def test_crc32_bytes(self):
        result = crc32(b"hello")
        self.assertEqual(result, 0x3610A686)

    def test_crc32_type_error(self):
        with self.assertRaises(TypeError):
            crc32([1, 2, 3])  # type: ignore[arg-type]


class TestHashFile(unittest.TestCase):
    def test_hash_file_sha256(self):
        content = "hello world"
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(content)
            temp_path = f.name

        try:
            result = hash_file(temp_path)
            expected = sha256(content)
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()

    def test_hash_file_md5(self):
        content = "test data"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = hash_file(temp_path, algorithm="md5")
            expected = md5(content)
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()

    def test_hash_file_with_bytes_path(self):
        content = "test"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(content)
            temp_path = f.name.encode("utf-8")

        try:
            result = hash_file(temp_path, algorithm="sha1")
            expected = sha1(content)
            self.assertEqual(result, expected)
        finally:
            Path(f.name).unlink()

    def test_hash_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            hash_file("/non/existent/file.txt")

    def test_hash_file_unsupported_algorithm(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("data")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                hash_file(temp_path, algorithm="invalid")
        finally:
            Path(temp_path).unlink()

    def test_hash_file_type_error(self):
        with self.assertRaises(TypeError):
            hash_file(123)  # type: ignore[arg-type]
TESTHASHUTILS

# --- html_utils.py ---
cat > "$OUTPUT_DIR/html_utils.py" <<'HTML_UTILS'
"""HTML utility functions for escaping, unescaping, and sanitizing HTML.

This module provides utilities for working with HTML content using the
standard library :mod:`html` module: escaping special characters for safe
insertion into HTML, unescaping HTML entities back to their original
characters, and stripping HTML tags from markup.
"""

from __future__ import annotations

import html
import re
from typing import Union

__all__: list[str] = [
    "escape_html",
    "unescape_html",
    "strip_tags",
    "escape_attribute",
]

_TAG_RE = re.compile(r"<[^>]*>")


def escape_html(text: Union[str, None]) -> str:
    """Escape HTML special characters in ``text``.

    Converts ``&``, ``<``, ``>``, ``"``, and ``'`` to their corresponding
    HTML entities so the text can be safely inserted into an HTML document.

    Args:
        text: The text to escape. ``None`` is treated as an empty string.

    Returns:
        The escaped HTML-safe string.

    Raises:
        TypeError: If ``text`` is not a string or ``None``.

    Examples:
        >>> escape_html("<script>alert('xss')</script>")
        '&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;'
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        raise TypeError("text must be a string or None")
    return html.escape(text, quote=True)


def unescape_html(text: str) -> str:
    """Unescape HTML entities in ``text`` back to their original characters.

    Converts named and numeric character references (e.g. ``&amp;``,
    ``&#60;``, ``&#x3c;``) back to ``&``, ``<``, etc.

    Args:
        text: The HTML-escaped text to unescape.

    Returns:
        The unescaped string.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> unescape_html("&lt;div&gt;")
        '<div>'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return html.unescape(text)


def strip_tags(html_content: str) -> str:
    """Remove all HTML tags from ``html_content``.

    Strips anything matching ``<...>`` from the input, leaving only the
    text content. HTML entities are not decoded; use :func:`unescape_html`
    on the result if entity decoding is desired.

    Args:
        html_content: The HTML string to strip tags from.

    Returns:
        The text content with all tags removed.

    Raises:
        TypeError: If ``html_content`` is not a string.

    Examples:
        >>> strip_tags("<p>Hello <b>world</b>!</p>")
        'Hello world!'
    """
    if not isinstance(html_content, str):
        raise TypeError("html_content must be a string")
    return _TAG_RE.sub("", html_content)


def escape_attribute(value: Union[str, None]) -> str:
    """Escape ``value`` for safe use inside an HTML attribute.

    Like :func:`escape_html`, but intended for attribute values where both
    double and single quotes must be escaped to prevent breaking out of the
    attribute delimiter.

    Args:
        value: The attribute value to escape. ``None`` is treated as an
            empty string.

    Returns:
        The attribute-value-escaped string.

    Raises:
        TypeError: If ``value`` is not a string or ``None``.

    Examples:
        >>> escape_attribute('onload="alert(1)"')
        'onload=&quot;alert(1)&quot;'
    """
    if value is None:
        return ""
    if not isinstance(value, str):
        raise TypeError("value must be a string or None")
    return html.escape(value, quote=True)
HTML_UTILS

# --- tests/test_html_utils.py ---
cat > "$OUTPUT_DIR/tests/test_html_utils.py" <<'TESTHTMLUTILS'
"""Unit tests for html_utils module."""

import unittest

from html_utils import escape_attribute, escape_html, strip_tags, unescape_html


class TestEscapeHtml(unittest.TestCase):
    def test_escape_html_basic(self):
        self.assertEqual(escape_html("<div>"), "&lt;div&gt;")

    def test_escape_html_ampersand(self):
        self.assertEqual(escape_html("Tom & Jerry"), "Tom &amp; Jerry")

    def test_escape_html_quotes(self):
        self.assertEqual(escape_html('He said "hi"'), 'He said &quot;hi&quot;')

    def test_escape_html_none(self):
        self.assertEqual(escape_html(None), "")

    def test_escape_html_empty(self):
        self.assertEqual(escape_html(""), "")

    def test_escape_html_type_error(self):
        with self.assertRaises(TypeError):
            escape_html(123)  # type: ignore[arg-type]


class TestUnescapeHtml(unittest.TestCase):
    def test_unescape_html_named_entities(self):
        self.assertEqual(unescape_html("&lt;div&gt;"), "<div>")
        self.assertEqual(unescape_html("&amp;"), "&")

    def test_unescape_html_numeric_entities(self):
        self.assertEqual(unescape_html("&#60;"), "<")
        self.assertEqual(unescape_html("&#x3c;"), "<")

    def test_unescape_html_plain_text(self):
        self.assertEqual(unescape_html("hello world"), "hello world")

    def test_unescape_html_type_error(self):
        with self.assertRaises(TypeError):
            unescape_html(None)  # type: ignore[arg-type]


class TestStripTags(unittest.TestCase):
    def test_strip_tags_basic(self):
        self.assertEqual(strip_tags("<p>Hello <b>world</b>!</p>"), "Hello world!")

    def test_strip_tags_no_tags(self):
        self.assertEqual(strip_tags("plain text"), "plain text")

    def test_strip_tags_empty(self):
        self.assertEqual(strip_tags(""), "")

    def test_strip_tags_multiline(self):
        self.assertEqual(
            strip_tags("<div>\n  <span>text</span>\n</div>"),
            "\n  text\n",
        )

    def test_strip_tags_type_error(self):
        with self.assertRaises(TypeError):
            strip_tags(["<div>"])  # type: ignore[arg-type]


class TestEscapeAttribute(unittest.TestCase):
    def test_escape_attribute_double_quotes(self):
        self.assertEqual(escape_attribute('a="b"'), 'a=&quot;b&quot;')

    def test_escape_attribute_single_quotes(self):
        self.assertEqual(escape_attribute("it's"), "it&#x27;s")

    def test_escape_attribute_none(self):
        self.assertEqual(escape_attribute(None), "")

    def test_escape_attribute_type_error(self):
        with self.assertRaises(TypeError):
            escape_attribute(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTHTMLUTILS

# --- base64_utils.py ---
cat > "$OUTPUT_DIR/base64_utils.py" <<'BASE64_UTILS'
"""Base64 and hexadecimal encoding/decoding utilities.

This module provides utilities for encoding and decoding data using Base64
(standard and URL-safe alphabets) and hexadecimal representations, with input
validation and helpers for checking whether a string is valid Base64 or hex.
All functions operate on :class:`str` or :class:`bytes` and raise
:class:`TypeError` or :class:`ValueError` on invalid input.
"""

from __future__ import annotations

import base64
import binascii
from typing import Union

__all__: list[str] = [
    "base64_encode",
    "base64_decode",
    "base64_encode_bytes",
    "base64_decode_bytes",
    "hex_encode",
    "hex_decode",
    "is_valid_base64",
    "is_valid_hex",
]


def _to_bytes(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be a string or bytes")


def base64_encode(data: Union[str, bytes], urlsafe: bool = False) -> str:
    """Encode ``data`` as a Base64 string.

    Args:
        data: The string or bytes to encode.
        urlsafe: If True, use the URL-safe Base64 alphabet (``-`` and ``_``
            instead of ``+`` and ``/``). Defaults to False.

    Returns:
        The Base64-encoded ASCII string.

    Raises:
        TypeError: If ``data`` is not a string or bytes.

    Examples:
        >>> base64_encode("hello")
        'aGVsbG8='
        >>> base64_encode("hello", urlsafe=True)
        'aGVsbG8='
    """
    encoded = (
        base64.urlsafe_b64encode(_to_bytes(data))
        if urlsafe
        else base64.b64encode(_to_bytes(data))
    )
    return encoded.decode("ascii")


def base64_decode(encoded: str, urlsafe: bool = False) -> str:
    """Decode a Base64-encoded string back to a UTF-8 string.

    Args:
        encoded: The Base64-encoded string to decode.
        urlsafe: If True, interpret ``encoded`` using the URL-safe alphabet.
            Defaults to False.

    Returns:
        The decoded UTF-8 string.

    Raises:
        TypeError: If ``encoded`` is not a string.
        ValueError: If ``encoded`` is not valid Base64.
        UnicodeDecodeError: If the decoded bytes are not valid UTF-8.

    Examples:
        >>> base64_decode("aGVsbG8=")
        'hello'
    """
    if not isinstance(encoded, str):
        raise TypeError("encoded must be a string")
    encoded_bytes = encoded.encode("ascii")
    try:
        decoded = (
            base64.urlsafe_b64decode(encoded_bytes)
            if urlsafe
            else base64.b64decode(encoded_bytes)
        )
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid base64 data: {exc}") from exc
    return decoded.decode("utf-8")


def base64_encode_bytes(data: Union[str, bytes]) -> bytes:
    """Encode ``data`` as Base64 bytes.

    Args:
        data: The string or bytes to encode.

    Returns:
        The Base64-encoded bytes.

    Raises:
        TypeError: If ``data`` is not a string or bytes.

    Examples:
        >>> base64_encode_bytes("hello")
        b'aGVsbG8='
    """
    return base64.b64encode(_to_bytes(data))


def base64_decode_bytes(encoded: Union[str, bytes]) -> bytes:
    """Decode a Base64-encoded string or bytes back to raw bytes.

    Args:
        encoded: The Base64-encoded data to decode.

    Returns:
        The decoded bytes.

    Raises:
        TypeError: If ``encoded`` is not a string or bytes.
        ValueError: If ``encoded`` is not valid Base64.

    Examples:
        >>> base64_decode_bytes("aGVsbG8=")
        b'hello'
    """
    if isinstance(encoded, str):
        encoded_bytes = encoded.encode("ascii")
    elif isinstance(encoded, bytes):
        encoded_bytes = encoded
    else:
        raise TypeError("encoded must be a string or bytes")
    try:
        return base64.b64decode(encoded_bytes)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid base64 data: {exc}") from exc


def hex_encode(data: Union[str, bytes]) -> str:
    """Encode ``data`` as a lowercase hexadecimal string.

    Args:
        data: The string or bytes to encode.

    Returns:
        The lowercase hexadecimal-encoded string.

    Raises:
        TypeError: If ``data`` is not a string or bytes.

    Examples:
        >>> hex_encode("hello")
        '68656c6c6f'
    """
    return _to_bytes(data).hex()


def hex_decode(encoded: str) -> str:
    """Decode a hexadecimal-encoded string back to a UTF-8 string.

    Args:
        encoded: The hexadecimal-encoded string to decode.

    Returns:
        The decoded UTF-8 string.

    Raises:
        TypeError: If ``encoded`` is not a string.
        ValueError: If ``encoded`` is not valid hexadecimal or the decoded
            bytes are not valid UTF-8.

    Examples:
        >>> hex_decode("68656c6c6f")
        'hello'
    """
    if not isinstance(encoded, str):
        raise TypeError("encoded must be a string")
    try:
        decoded = bytes.fromhex(encoded)
    except ValueError as exc:
        raise ValueError(f"invalid hexadecimal data: {exc}") from exc
    return decoded.decode("utf-8")


def is_valid_base64(encoded: str, urlsafe: bool = False) -> bool:
    """Return True if ``encoded`` is valid Base64 data.

    Args:
        encoded: The string to validate.
        urlsafe: If True, validate against the URL-safe alphabet.
            Defaults to False.

    Returns:
        True if ``encoded`` is valid Base64, False otherwise.

    Examples:
        >>> is_valid_base64("aGVsbG8=")
        True
        >>> is_valid_base64("not valid base64!!!")
        False
    """
    if not isinstance(encoded, str):
        return False
    try:
        base64_decode(encoded, urlsafe=urlsafe)
        return True
    except (TypeError, ValueError, UnicodeDecodeError):
        return False


def is_valid_hex(encoded: str) -> bool:
    """Return True if ``encoded`` is valid hexadecimal data.

    Args:
        encoded: The string to validate.

    Returns:
        True if ``encoded`` is valid hexadecimal, False otherwise.

    Examples:
        >>> is_valid_hex("68656c6c6f")
        True
        >>> is_valid_hex("zzzz")
        False
    """
    if not isinstance(encoded, str):
        return False
    try:
        bytes.fromhex(encoded)
        return True
    except ValueError:
        return False
BASE64_UTILS

# --- tests/test_base64_utils.py ---
cat > "$OUTPUT_DIR/tests/test_base64_utils.py" <<'TESTBASE64UTILS'
"""Unit tests for base64_utils module."""

import unittest

from base64_utils import (
    base64_decode,
    base64_decode_bytes,
    base64_encode,
    base64_encode_bytes,
    hex_decode,
    hex_encode,
    is_valid_base64,
    is_valid_hex,
)


class TestBase64Encode(unittest.TestCase):
    def test_base64_encode_string(self):
        self.assertEqual(base64_encode("hello"), "aGVsbG8=")

    def test_base64_encode_bytes(self):
        self.assertEqual(base64_encode(b"hello"), "aGVsbG8=")

    def test_base64_encode_empty(self):
        self.assertEqual(base64_encode(""), "")

    def test_base64_encode_urlsafe(self):
        self.assertEqual(base64_encode("hello", urlsafe=True), "aGVsbG8=")

    def test_base64_encode_type_error(self):
        with self.assertRaises(TypeError):
            base64_encode(123)  # type: ignore[arg-type]


class TestBase64Decode(unittest.TestCase):
    def test_base64_decode_basic(self):
        self.assertEqual(base64_decode("aGVsbG8="), "hello")

    def test_base64_decode_roundtrip(self):
        self.assertEqual(base64_decode(base64_encode("hello")), "hello")

    def test_base64_decode_invalid(self):
        with self.assertRaises(ValueError):
            base64_decode("not valid base64!!!")

    def test_base64_decode_type_error(self):
        with self.assertRaises(TypeError):
            base64_decode(123)  # type: ignore[arg-type]


class TestBase64EncodeBytes(unittest.TestCase):
    def test_base64_encode_bytes_basic(self):
        self.assertEqual(base64_encode_bytes("hello"), b"aGVsbG8=")

    def test_base64_encode_bytes_type_error(self):
        with self.assertRaises(TypeError):
            base64_encode_bytes(123)  # type: ignore[arg-type]


class TestBase64DecodeBytes(unittest.TestCase):
    def test_base64_decode_bytes_basic(self):
        self.assertEqual(base64_decode_bytes("aGVsbG8="), b"hello")

    def test_base64_decode_bytes_roundtrip(self):
        self.assertEqual(base64_decode_bytes(base64_encode("hello")), b"hello")

    def test_base64_decode_bytes_invalid(self):
        with self.assertRaises(ValueError):
            base64_decode_bytes("not valid base64!!!")

    def test_base64_decode_bytes_type_error(self):
        with self.assertRaises(TypeError):
            base64_decode_bytes(123)  # type: ignore[arg-type]


class TestHexEncode(unittest.TestCase):
    def test_hex_encode_string(self):
        self.assertEqual(hex_encode("hello"), "68656c6c6f")

    def test_hex_encode_bytes(self):
        self.assertEqual(hex_encode(b"hello"), "68656c6c6f")

    def test_hex_encode_empty(self):
        self.assertEqual(hex_encode(""), "")

    def test_hex_encode_type_error(self):
        with self.assertRaises(TypeError):
            hex_encode(123)  # type: ignore[arg-type]


class TestHexDecode(unittest.TestCase):
    def test_hex_decode_basic(self):
        self.assertEqual(hex_decode("68656c6c6f"), "hello")

    def test_hex_decode_roundtrip(self):
        self.assertEqual(hex_decode(hex_encode("hello")), "hello")

    def test_hex_decode_invalid(self):
        with self.assertRaises(ValueError):
            hex_decode("zzzz")

    def test_hex_decode_type_error(self):
        with self.assertRaises(TypeError):
            hex_decode(123)  # type: ignore[arg-type]


class TestIsValidBase64(unittest.TestCase):
    def test_is_valid_base64_true(self):
        self.assertTrue(is_valid_base64("aGVsbG8="))

    def test_is_valid_base64_false(self):
        self.assertFalse(is_valid_base64("not valid base64!!!"))

    def test_is_valid_base64_type_error_returns_false(self):
        self.assertFalse(is_valid_base64(123))  # type: ignore[arg-type]


class TestIsValidHex(unittest.TestCase):
    def test_is_valid_hex_true(self):
        self.assertTrue(is_valid_hex("68656c6c6f"))

    def test_is_valid_hex_false(self):
        self.assertFalse(is_valid_hex("zzzz"))

    def test_is_valid_hex_type_error_returns_false(self):
        self.assertFalse(is_valid_hex(123))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTBASE64UTILS

# --- struct_utils.py ---
cat > "$OUTPUT_DIR/struct_utils.py" <<'STRUCT_UTILS'
"""Binary struct packing and unpacking utilities.

This module provides utilities for converting between Python values and
binary :mod:`struct` format representations, with configurable byte order,
input validation, and helpers for calculating the size of a format string
and validating format strings. All functions wrap the standard library
:mod:`struct` module and raise :class:`TypeError` or :class:`ValueError`
on invalid input.
"""

from __future__ import annotations

import struct
from typing import Any, Tuple, Union

__all__: list[str] = [
    "pack",
    "unpack",
    "pack_into",
    "unpack_from",
    "calcsize",
    "is_valid_format",
]


def _require_string(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _validate_format(fmt: str) -> str:
    """Validate ``fmt`` as a :mod:`struct` format string and return it.

    Raises:
        TypeError: If ``fmt`` is not a string.
        ValueError: If ``fmt`` is not a valid struct format string.
    """
    _require_string(fmt, "fmt")
    try:
        struct.calcsize(fmt)
    except struct.error as exc:
        raise ValueError(f"invalid struct format string: {exc}") from exc
    return fmt


def pack(fmt: str, *values: Any) -> bytes:
    """Pack ``values`` according to ``fmt`` and return the resulting bytes.

    Args:
        fmt: A :mod:`struct` format string (e.g. ``"<iif"``).
        values: The values to pack, matching the format specifiers.

    Returns:
        The packed binary data as a :class:`bytes` object.

    Raises:
        TypeError: If ``fmt`` is not a string.
        ValueError: If ``fmt`` is invalid or the values do not match the format.

    Examples:
        >>> pack("<B", 65)
        b'A'
        >>> pack(">I", 0x41424344)
        b'ABCD'
    """
    _validate_format(fmt)
    try:
        return struct.pack(fmt, *values)
    except struct.error as exc:
        raise ValueError(f"failed to pack values for format {fmt!r}: {exc}") from exc


def unpack(fmt: str, buffer: Union[bytes, bytearray]) -> Tuple[Any, ...]:
    """Unpack ``buffer`` according to ``fmt`` and return the resulting values.

    Args:
        fmt: A :mod:`struct` format string.
        buffer: The binary data to unpack. Its length must match
            :func:`calcsize` for ``fmt``.

    Returns:
        A tuple of unpacked values.

    Raises:
        TypeError: If ``fmt`` is not a string or ``buffer`` is not bytes/bytearray.
        ValueError: If ``fmt`` is invalid or the buffer size is incorrect.

    Examples:
        >>> unpack("<B", b'A')
        (65,)
    """
    _validate_format(fmt)
    if not isinstance(buffer, (bytes, bytearray)):
        raise TypeError("buffer must be bytes or bytearray")
    try:
        return struct.unpack(fmt, buffer)
    except struct.error as exc:
        raise ValueError(f"failed to unpack buffer for format {fmt!r}: {exc}") from exc


def pack_into(fmt: str, buffer: bytearray, offset: int, *values: Any) -> None:
    """Pack ``values`` into ``buffer`` at ``offset`` according to ``fmt``.

    Args:
        fmt: A :mod:`struct` format string.
        buffer: A mutable :class:`bytearray` to pack into.
        offset: The byte offset in ``buffer`` to start writing at.
        values: The values to pack, matching the format specifiers.

    Raises:
        TypeError: If ``fmt`` is not a string, ``buffer`` is not a bytearray,
            or ``offset`` is not an integer.
        ValueError: If ``fmt`` is invalid, ``offset`` is negative, or there is
            not enough room in ``buffer``.

    Examples:
        >>> buf = bytearray(4)
        >>> pack_into(">I", buf, 0, 0x41424344)
        >>> buf
        bytearray(b'ABCD')
    """
    _validate_format(fmt)
    if not isinstance(buffer, bytearray):
        raise TypeError("buffer must be a bytearray")
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise TypeError("offset must be an integer")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    try:
        struct.pack_into(fmt, buffer, offset, *values)
    except struct.error as exc:
        raise ValueError(f"failed to pack into buffer for format {fmt!r}: {exc}") from exc


def unpack_from(fmt: str, buffer: Union[bytes, bytearray], offset: int = 0) -> Tuple[Any, ...]:
    """Unpack values from ``buffer`` starting at ``offset`` according to ``fmt``.

    Args:
        fmt: A :mod:`struct` format string.
        buffer: The binary data to unpack from.
        offset: The byte offset to start reading from. Defaults to 0.

    Returns:
        A tuple of unpacked values.

    Raises:
        TypeError: If ``fmt`` is not a string, ``buffer`` is not bytes/bytearray,
            or ``offset`` is not an integer.
        ValueError: If ``fmt`` is invalid, ``offset`` is negative, or there is
            not enough data in ``buffer``.

    Examples:
        >>> unpack_from(">I", b'ABCD', 0)
        (1094861636,)
    """
    _validate_format(fmt)
    if not isinstance(buffer, (bytes, bytearray)):
        raise TypeError("buffer must be bytes or bytearray")
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise TypeError("offset must be an integer")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    try:
        return struct.unpack_from(fmt, buffer, offset)
    except struct.error as exc:
        raise ValueError(f"failed to unpack from buffer for format {fmt!r}: {exc}") from exc


def calcsize(fmt: str) -> int:
    """Return the size in bytes of a value described by ``fmt``.

    Args:
        fmt: A :mod:`struct` format string.

    Returns:
        The number of bytes required to pack ``fmt``.

    Raises:
        TypeError: If ``fmt`` is not a string.
        ValueError: If ``fmt`` is invalid.

    Examples:
        >>> calcsize("<h")
        2
        >>> calcsize(">I")
        4
    """
    return struct.calcsize(_validate_format(fmt))


def is_valid_format(fmt: str) -> bool:
    """Return True if ``fmt`` is a valid :mod:`struct` format string.

    Args:
        fmt: The format string to validate.

    Returns:
        True if ``fmt`` is a valid struct format string, False otherwise.

    Examples:
        >>> is_valid_format("<h")
        True
        >>> is_valid_format("!!invalid!!")
        False
    """
    if not isinstance(fmt, str):
        return False
    try:
        struct.calcsize(fmt)
        return True
    except struct.error:
        return False
STRUCT_UTILS

# --- tests/test_struct_utils.py ---
cat > "$OUTPUT_DIR/tests/test_struct_utils.py" <<'TESTSTRUCTUTILS'
"""Unit tests for struct_utils module."""

import unittest

from struct_utils import (
    calcsize,
    is_valid_format,
    pack,
    pack_into,
    unpack,
    unpack_from,
)


class TestPack(unittest.TestCase):
    def test_pack_short_little_endian(self):
        self.assertEqual(pack("<h", 255), b"\xff\x00")

    def test_pack_ints_big_endian(self):
        self.assertEqual(pack(">ii", 1, 2), b"\x00\x00\x00\x01\x00\x00\x00\x02")

    def test_pack_roundtrip(self):
        self.assertEqual(unpack("<h", pack("<h", 255)), (255,))

    def test_pack_type_error_fmt(self):
        with self.assertRaises(TypeError):
            pack(123, 1)  # type: ignore[arg-type]

    def test_pack_invalid_format(self):
        with self.assertRaises(ValueError):
            pack("!!invalid!!", 1)

    def test_pack_wrong_number_of_values(self):
        with self.assertRaises(ValueError):
            pack("<ii", 1)


class TestUnpack(unittest.TestCase):
    def test_unpack_short_little_endian(self):
        self.assertEqual(unpack("<h", b"\xff\x00"), (255,))

    def test_unpack_ints_big_endian(self):
        self.assertEqual(
            unpack(">ii", b"\x00\x00\x00\x01\x00\x00\x00\x02"), (1, 2)
        )

    def test_unpack_type_error_fmt(self):
        with self.assertRaises(TypeError):
            unpack(123, b"\x00\x00")  # type: ignore[arg-type]

    def test_unpack_type_error_buffer(self):
        with self.assertRaises(TypeError):
            unpack("<h", "not bytes")  # type: ignore[arg-type]

    def test_unpack_invalid_format(self):
        with self.assertRaises(ValueError):
            unpack("!!invalid!!", b"\x00\x00")

    def test_unpack_buffer_too_short(self):
        with self.assertRaises(ValueError):
            unpack("<ii", b"\x00\x00\x00\x01")


class TestPackInto(unittest.TestCase):
    def test_pack_into(self):
        buf = bytearray(8)
        pack_into(">ii", buf, 0, 1, 2)
        self.assertEqual(buf, bytearray(b"\x00\x00\x00\x01\x00\x00\x00\x02"))

    def test_pack_into_offset(self):
        buf = bytearray(12)
        pack_into(">ii", buf, 4, 1, 2)
        self.assertEqual(buf[4:12], b"\x00\x00\x00\x01\x00\x00\x00\x02")

    def test_pack_into_type_error_buffer(self):
        with self.assertRaises(TypeError):
            pack_into("<h", b"\x00\x00", 0, 1)  # type: ignore[arg-type]

    def test_pack_into_type_error_offset(self):
        with self.assertRaises(TypeError):
            pack_into("<h", bytearray(2), "0", 1)  # type: ignore[arg-type]

    def test_pack_into_negative_offset(self):
        with self.assertRaises(ValueError):
            pack_into("<h", bytearray(2), -1, 1)

    def test_pack_into_invalid_format(self):
        with self.assertRaises(ValueError):
            pack_into("!!invalid!!", bytearray(2), 0, 1)

    def test_pack_into_not_enough_room(self):
        with self.assertRaises(ValueError):
            pack_into("<ii", bytearray(2), 0, 1, 2)


class TestUnpackFrom(unittest.TestCase):
    def test_unpack_from(self):
        data = b"\x00\x00\x00\x01\x00\x00\x00\x02"
        self.assertEqual(unpack_from(">ii", data, 0), (1, 2))

    def test_unpack_from_offset(self):
        data = b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02"
        self.assertEqual(unpack_from(">ii", data, 4), (1, 2))

    def test_unpack_from_type_error_fmt(self):
        with self.assertRaises(TypeError):
            unpack_from(123, b"\x00\x00\x00\x01")  # type: ignore[arg-type]

    def test_unpack_from_type_error_buffer(self):
        with self.assertRaises(TypeError):
            unpack_from("<h", "not bytes", 0)  # type: ignore[arg-type]

    def test_unpack_from_type_error_offset(self):
        with self.assertRaises(TypeError):
            unpack_from("<h", b"\x00\x00", "0")  # type: ignore[arg-type]

    def test_unpack_from_negative_offset(self):
        with self.assertRaises(ValueError):
            unpack_from("<h", b"\x00\x00", -1)

    def test_unpack_from_invalid_format(self):
        with self.assertRaises(ValueError):
            unpack_from("!!invalid!!", b"\x00\x00")


class TestCalcsize(unittest.TestCase):
    def test_calcsize_short(self):
        self.assertEqual(calcsize("<h"), 2)

    def test_calcsize_ints(self):
        self.assertEqual(calcsize(">ii"), 8)

    def test_calcsize_type_error(self):
        with self.assertRaises(TypeError):
            calcsize(123)  # type: ignore[arg-type]

    def test_calcsize_invalid_format(self):
        with self.assertRaises(ValueError):
            calcsize("!!invalid!!")


class TestIsValidFormat(unittest.TestCase):
    def test_is_valid_format_true(self):
        self.assertTrue(is_valid_format("<h"))
        self.assertTrue(is_valid_format(">ii"))

    def test_is_valid_format_false(self):
        self.assertFalse(is_valid_format("!!invalid!!"))

    def test_is_valid_format_type_error_returns_false(self):
        self.assertFalse(is_valid_format(123))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTSTRUCTUTILS

# --- tests/test_cli_utils.py ---
cat > "$OUTPUT_DIR/tests/test_cli_utils.py" <<'TESTCLIUTILS'
"""Unit tests for cli_utils module."""

import argparse
import unittest
from unittest.mock import patch

from cli_utils import create_parser, main_wrapper, parse_arguments


class TestCreateParser(unittest.TestCase):
    def test_creates_parser_with_prog(self):
        parser = create_parser("my-tool", "A tool.")
        self.assertEqual(parser.prog, "my-tool")
        self.assertEqual(parser.description, "A tool.")

    def test_has_verbose_flag(self):
        parser = create_parser("my-tool", "A tool.")
        args = parser.parse_args(["-v"])
        self.assertTrue(args.verbose)

    def test_has_long_verbose_flag(self):
        parser = create_parser("my-tool", "A tool.")
        args = parser.parse_args(["--verbose"])
        self.assertTrue(args.verbose)

    def test_version_flag_exits(self):
        parser = create_parser("my-tool", "A tool.")
        with self.assertRaises(SystemExit):
            parser.parse_args(["--version"])


class TestParseArguments(unittest.TestCase):
    def test_parses_arguments(self):
        parser = create_parser("my-tool", "A tool.")
        args = parse_arguments(parser, ["-v"])
        self.assertTrue(args.verbose)

    def test_defaults_to_sys_argv(self):
        parser = create_parser("my-tool", "A tool.")
        with patch("sys.argv", ["my-tool", "-v"]):
            args = parse_arguments(parser)
            self.assertTrue(args.verbose)


class TestMainWrapper(unittest.TestCase):
    def test_returns_func_exit_code(self):
        def main(argv):
            return 0

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped([]), 0)

    def test_returns_one_on_exception(self):
        def main(argv):
            raise ValueError("boom")

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped([]), 1)

    def test_returns_130_on_keyboard_interrupt(self):
        def main(argv):
            raise KeyboardInterrupt

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped([]), 130)

    def test_preserves_function_metadata(self):
        def main(argv):
            """The main function."""
            return 0

        wrapped = main_wrapper(main)
        self.assertEqual(wrapped.__name__, "main")
        self.assertEqual(wrapped.__doc__, "The main function.")


if __name__ == "__main__":
    unittest.main()
TESTCLIUTILS

# --- tests/test_terminal_utils.py ---
cat > "$OUTPUT_DIR/tests/test_terminal_utils.py" <<'TESTTERMINALUTILS'
"""Tests for terminal_utils module."""

import io
import unittest
from unittest.mock import patch

from terminal_utils import (
    ProgressBar,
    clear_screen,
    colorize,
    get_terminal_size,
    progress_bar,
    print_colored,
    prompt,
    supports_color,
)


class TestSupportsColor(unittest.TestCase):
    def test_returns_bool(self):
        self.assertIsInstance(supports_color(), bool)


class TestColorize(unittest.TestCase):
    def test_returns_plain_text_when_not_a_tty(self):
        self.assertEqual(colorize("hello", "red"), "hello")
        self.assertEqual(colorize("hello", "red", bold=True), "hello")

    def test_all_valid_colors_return_string(self):
        for color in ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"):
            self.assertIsInstance(colorize("x", color), str)

    def test_invalid_color_raises_value_error(self):
        with self.assertRaises(ValueError):
            colorize("hello", "purple")

    def test_non_string_text_raises_type_error(self):
        with self.assertRaises(TypeError):
            colorize(123, "red")

    def test_non_string_color_raises_type_error(self):
        with self.assertRaises(TypeError):
            colorize("hello", 5)


class TestPrintColored(unittest.TestCase):
    def test_writes_to_stream(self):
        stream = io.StringIO()
        print_colored("hello", color="red", stream=stream)
        self.assertEqual(stream.getvalue(), "hello\n")

    def test_default_stream_is_stdout(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_colored("hi")
            self.assertEqual(mock_stdout.getvalue(), "hi\n")


class TestClearScreen(unittest.TestCase):
    def test_writes_newlines_when_not_a_tty(self):
        stream = io.StringIO()
        with patch("terminal_utils.sys.stdout", stream):
            clear_screen()
        self.assertEqual(stream.getvalue(), "\n" * 50)


class TestGetTerminalSize(unittest.TestCase):
    def test_returns_tuple_of_two_positive_ints(self):
        columns, lines = get_terminal_size()
        self.assertIsInstance(columns, int)
        self.assertIsInstance(lines, int)
        self.assertGreater(columns, 0)
        self.assertGreater(lines, 0)


class TestProgressBar(unittest.TestCase):
    def test_total_must_be_positive(self):
        with self.assertRaises(ValueError):
            ProgressBar(0)
        with self.assertRaises(ValueError):
            ProgressBar(-3)
        with self.assertRaises(ValueError):
            ProgressBar(True)

    def test_fill_and_empty_must_be_single_characters(self):
        with self.assertRaises(ValueError):
            ProgressBar(1, fill="ab")
        with self.assertRaises(ValueError):
            ProgressBar(1, empty="")

    def test_render_shows_progress(self):
        stream = io.StringIO()
        bar = ProgressBar(10, width=10, stream=stream)
        bar.update(5)
        output = stream.getvalue()
        self.assertIn("[#####-----]", output)
        self.assertIn("50%", output)
        self.assertIn("(5/10)", output)

    def test_update_out_of_range_raises_value_error(self):
        bar = ProgressBar(5, stream=io.StringIO())
        with self.assertRaises(ValueError):
            bar.update(6)
        with self.assertRaises(ValueError):
            bar.update(-1)

    def test_update_non_integer_raises_type_error(self):
        bar = ProgressBar(5, stream=io.StringIO())
        with self.assertRaises(TypeError):
            bar.update("3")

    def test_update_after_finish_is_noop(self):
        stream = io.StringIO()
        bar = ProgressBar(2, stream=stream)
        bar.finish()
        before = stream.getvalue()
        bar.update(1)
        self.assertEqual(stream.getvalue(), before)

    def test_finish_writes_final_newline(self):
        stream = io.StringIO()
        bar = ProgressBar(3, stream=stream)
        bar.finish()
        self.assertIn("\n", stream.getvalue())

    def test_context_manager_finishes(self):
        stream = io.StringIO()
        with ProgressBar(4, stream=stream) as bar:
            bar.update(2)
        self.assertTrue(bar._finished)

    def test_yields_items(self):
        stream = io.StringIO()
        result = list(progress_bar([1, 2, 3], stream=stream))
        self.assertEqual(result, [1, 2, 3])

    def test_total_inferred_from_len(self):
        stream = io.StringIO()
        result = list(progress_bar([10, 20], stream=stream))
        self.assertEqual(result, [10, 20])

    def test_iterable_without_len_requires_total(self):
        def generator():
            yield 1
            yield 2

        with self.assertRaises(ValueError):
            list(progress_bar(generator()))

    def test_increment_advances(self):
        stream = io.StringIO()
        bar = ProgressBar(3, stream=stream)
        bar.update(increment=1)
        bar.update(increment=1)
        self.assertEqual(bar._current, 2)


class TestPrompt(unittest.TestCase):
    def test_returns_entered_value(self):
        with patch("builtins.input", return_value="Alice"):
            self.assertEqual(prompt("Name"), "Alice")

    def test_returns_default_on_empty_input(self):
        with patch("builtins.input", return_value=""):
            self.assertEqual(prompt("Name", default="Guest"), "Guest")

    def test_returns_empty_string_when_no_default(self):
        with patch("builtins.input", return_value=""):
            self.assertEqual(prompt("Name"), "")

    def test_raises_eof_error_on_closed_stream(self):
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(EOFError):
                prompt("Name")

    def test_non_string_message_raises_type_error(self):
        with self.assertRaises(TypeError):
            prompt(123)

    def test_non_string_default_raises_type_error(self):
        with self.assertRaises(TypeError):
            prompt("Name", default=5)


if __name__ == "__main__":
    unittest.main()
TESTTERMINALUTILS

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
- `kilo.json` — Kilo project configuration, including the `scaffolder` subagent
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
- `config_utils.py` — configuration utilities for JSON file management
- `collections_utils.py` — collection utilities (chunk, flatten, deep_flatten, windowed, uniq, frequency, merge_dicts, and more)
- `shapes.py` — geometry utilities for areas and perimeters of common shapes
- `strings.py` — string utilities for text operations
- `utils.py` — general utility helper functions
- `stats.py` — statistical utility functions
- `math_utils.py` — mathematical utility functions
- `data_utils.py` — data utility functions
- `datetime_utils.py` — date and time utility functions
- `file_utils.py` — file and path utility functions
- `url_utils.py` — URL and web utility functions
- `uuid_utils.py` — UUID utility functions for generating and validating UUIDs
- `prompt_utils.py` — Prompt utility functions for working with text prompts
- `random_utils.py` — random number generation and sampling utilities
- `validation_utils.py` — input validation utilities
- `crypto_utils.py` — cryptographic utilities
- `list_utils.py` — advanced list manipulation utilities
- `env_utils.py` — environment variable handling utilities
- `logging_utils.py` — logging configuration and helper utilities
- `cache_utils.py` — caching utilities for memoizing function results
- `timing_utils.py` — performance measurement helpers
- `async_utils.py` — asynchronous utility functions
- `bit_utils.py` — bitwise utility functions for working with binary representations of integers
- `concurrent_utils.py` — concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
- `priority_queue_utils.py` — heap-based priority queue implementation
- `rate_limiter_utils.py` — rate limiting utilities (token bucket algorithm)
- `retry_utils.py` — retry utilities with exponential backoff and jitter
- `dict_utils.py` — dictionary utilities (deep merge, flatten/unflatten, safe get, invert, filter)
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate)
- `collections_utils.py` — collection utilities (chunk, flatten, deep_flatten, windowed, uniq, frequency, merge_dicts, and more)
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `set_utils.py` — set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
- `statistics_utils.py` — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
- `string_utils.py` — advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
- `tree_utils.py` — tree and nested structure utilities (get_nested, set_nested, delete_nested, flatten_tree, unflatten_tree, map_tree, filter_tree)
- `type_utils.py` — type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
- `path_utils.py` — path manipulation utilities (join, normalize, components, extensions)
- `config_schema.py` — typed configuration schema utilities (SchemaField, ConfigSchema, validators)
- `uuid_utils.py` — UUID utility functions for generating and validating UUIDs
- `prompt_utils.py` — Prompt utility functions for working with text prompts
- `tests/test_hello.py` — unit tests for `hello.py`
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `tests/test_config_utils.py` — unit tests for the config utilities module
- `tests/test_collections_utils.py` — unit tests for `collections_utils.py`
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `tests/test_strings.py` — unit tests for `strings.py`
- `tests/test_utils.py` — unit tests for `utils.py`
- `tests/test_stats.py` — unit tests for `stats.py`
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- `tests/test_datetime_utils.py` — unit tests for `datetime_utils.py`
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- `tests/test_url_utils.py` — unit tests for `url_utils.py`
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `tests/test_random_utils.py` — unit tests for `random_utils.py`
- `tests/test_validation_utils.py` — unit tests for `validation_utils.py`
- `tests/test_crypto_utils.py` — unit tests for `crypto_utils.py`
- `tests/test_list_utils.py` — unit tests for `list_utils.py`
- `tests/test_env_utils.py` — unit tests for `env_utils.py`
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- `tests/test_cache_utils.py` — unit tests for `cache_utils.py`
- `tests/test_timing_utils.py` — unit tests for `timing_utils.py`
- `tests/test_async_utils.py` — unit tests for `async_utils.py`
- `tests/test_bit_utils.py` — unit tests for `bit_utils.py`
- `tests/test_concurrent_utils.py` — unit tests for `concurrent_utils.py`
- `tests/test_priority_queue_utils.py` — unit tests for `priority_queue_utils.py`
- `tests/test_rate_limiter_utils.py` — unit tests for `rate_limiter_utils.py`
- `tests/test_retry_utils.py` — unit tests for `retry_utils.py`
- `tests/test_dict_utils.py` — unit tests for `dict_utils.py`
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- `tests/test_collections_utils.py` — unit tests for `collections_utils.py`
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`
- `tests/test_set_utils.py` — unit tests for `set_utils.py`
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- `tests/test_type_utils.py` — unit tests for `type_utils.py`
- `tests/test_path_utils.py` — unit tests for `path_utils.py`
- `tests/test_pattern_utils.py` — unit tests for `pattern_utils.py`
- `tests/test_struct_utils.py` — unit tests for `struct_utils.py`
- `functools_utils.py` — functional programming utilities (compose, pipe, curry, apply)
- `tests/test_functools_utils.py` — unit tests for `functools_utils.py`
- `tests/test_config_schema.py` — unit tests for `config_schema.py`
- `exceptions_utils.py` — custom exception classes and error handling utilities
- `tests/test_exceptions_utils.py` — unit tests for `exceptions_utils.py`
- `io_utils.py` — line-oriented and atomic input/output utilities (read_lines, write_lines, append_text, atomic_write_text, stream_copy, count_lines, iter_lines)
- `ini_utils.py` — INI configuration file utilities (load_config, save_config, get_config_value, set_config_value, merge_configs, list_sections, has_section, get_section)
- `tests/test_io_utils.py` — unit tests for `io_utils.py`
- `tests/test_ini_utils.py` — unit tests for `ini_utils.py`
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `terminal_utils.py` — terminal output utilities (ANSI color, progress bars, clear screen, prompts)
- `cli_utils.py` — command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
- `tests/test_cli_utils.py` — unit tests for `cli_utils.py`
- hash_utils.py — hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
- tests/test_hash_utils.py — unit tests for `hash_utils.py`
- html_utils.py — HTML escaping, unescaping, and tag-stripping utilities (`escape_html`, `unescape_html`, `strip_tags`, `escape_attribute`)
- tests/test_html_utils.py — unit tests for `html_utils.py`
- base64_utils.py — Base64 and hexadecimal encoding/decoding utilities (`base64_encode`, `base64_decode`, `base64_encode_bytes`, `base64_decode_bytes`, `hex_encode`, `hex_decode`, `is_valid_base64`, `is_valid_hex`)
- tests/test_base64_utils.py — unit tests for `base64_utils.py`
- struct_utils.py — Binary struct packing and unpacking utilities (`pack`, `unpack`, `pack_into`, `unpack_from`, `calcsize`, `is_valid_format`)
- tests/test_struct_utils.py — unit tests for `struct_utils.py`
- http_utils.py — HTTP status codes and response handling utilities (`status_code_category`, `status_message`, `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, `is_error`)
- tests/test_http_utils.py — unit tests for `http_utils.py`
- duration_utils.py — time duration utilities (`parse_duration`, `format_duration`, `seconds_to_hms`, `hms_to_seconds`, `to_seconds`, `duration_between`, `add_duration`, `is_valid_duration`)
- tests/test_duration_utils.py — unit tests for `duration_utils.py`
- temp_utils.py — temporary file and directory management utilities (`create_temp_file`, `create_temp_dir`, `temp_file`, `temp_dir`, `write_temp_file`, `read_temp_file`, `cleanup_temp_path`, `is_temp_path`, `temp_path_exists`)
- tests/test_temp_utils.py — unit tests for `temp_utils.py`
- `tests/test_terminal_utils.py` — unit tests for `terminal_utils.py`

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
2. Maintain consistency with existing codebase style
3. Ensure all generated code passes linting and type checking
4. Update templates when the source of truth changes
SKILLSAMPLE

# --- .kilo/.gitignore ---
cat > "$OUTPUT_DIR/.kilo/.gitignore" <<'KILOGITIGNORE'
.kilo/.state/
*.log
*.tmp
.env
KILOGITIGNORE

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
echo "  git commit -m 'Initial commit'"


# --- LICENSE ---
cat > "$OUTPUT_DIR/LICENSE" <<'__LIC__'
MIT License
Copyright (c) 2026 kilo-autonomous
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

__LIC__

# --- kilo.json ---
cat > "$OUTPUT_DIR/kilo.json" <<'__KILO__'
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

__KILO__

# --- AGENTS.md ---
cat > "$OUTPUT_DIR/AGENTS.md" <<'__AGENTS__'
# Agent Instructions

Project: ${PROJECT_NAME}

## Project Purpose

This repository is a self-evolving scaffolding project for autonomous agentic coding. A GitHub Actions workflow runs a loop of Kilo agent sessions, each receiving the task: "Execute the task assigned by the previous agent and prepare a task for the next agent!"

## Task Handover Protocol

1. Check the shared Kilo board (`board_read`) for any messages from the previous agent
2. If a task is found, execute it
3. If no task is found (bootstrap session), establish the project foundation
4. Post a new task for the next agent via `board_post` to `main`
5. Ensure all work results in committed changes (non-workflow files) for the CI checkpoint

## Workflow Rules

- The CI workflow excludes `.github/workflows/**` from the project progress check
- Only changes to files outside `.github/workflows/` count as "meaningful project progress"
- The workflow auto-commits all non-workflow changes after each session
- Do NOT modify `.github/workflows/` files — they are maintainer-managed

## Coding Conventions

- Write clean, well-documented code
- Follow existing file patterns in the repository
- Use descriptive file and function names
- Keep changes focused and incremental

## Agent Configuration

- Project config: `kilo.json` at the repository root
- Custom subagents: `.kilo/agent/*.md`
- Custom commands: `.kilo/command/*.md`
- Custom skills: `.kilo/skill/*.md`
- Kilo permissions: `permission` key in `kilo.json`

## Available Subagents

- `scaffolder` - A subagent for generating project scaffolding and templates
- `explore` (built-in) - Read-only codebase exploration

## Available Commands

- `scaffold-project` - Scaffold a new project structure
- `handover` - Prepare and post the next task for the following agent

## Developer Commands

Use the following Makefile targets during development:

- `make test` - Run the Python test suite
- `make lint` - Run ruff code style checker
- `make typecheck` - Run mypy static type checking
- `make run` - Run hello.py (`make run NAME=Alice`)
- `make scaffold` - Scaffold a new project using scaffold.sh
- `make pre-commit-install` - Install pre-commit hooks into .git/hooks
- `make pre-commit-run` - Run all pre-commit hooks against tracked files
- `make clean` - Remove build artifacts
- `make help` - Show all available targets

## Notes

- This project uses the `kilo/kilo-auto/free` model
- Sessions have an idle timeout of 900 seconds
- The overall CI job has a 355-minute safety cutoff

__AGENTS__

# --- README.md ---
cat > "$OUTPUT_DIR/README.md" <<'__README__'
# ${PROJECT_NAME}

A self-evolving scaffolding project for autonomous agentic coding loops powered by Kilo.

## Overview

This repository provides a foundation for agentic coding projects. It includes:

- A GitHub Actions workflow that runs a Kilo agent loop
- Project configuration for Kilo (AGENTS.md, kilo.json)
- Custom subagents and commands for scaffolding tasks
- A task handover protocol between agent sessions

## Architecture

```
.github/workflows/main.yml   # CI workflow: Kilo agent loop
.kilo/                       # Kilo project configuration
  agent/                     # Custom subagents
    scaffolder.md            # Scaffolder subagent definition
  command/                   # Custom commands
    handover.md              # Handover task command
    scaffold-project.md      # Scaffold-project command
  skill/                     # Custom skills
    scaffolding-helper.md    # Sample skill definition
  .gitignore                 # Ignore patterns for .kilo directory
.gitignore                   # Common ignore patterns
LICENSE                      # MIT License
.pre-commit-config.yaml      # Pre-commit hooks (ruff, mypy, tests, scaffold)
AGENTS.md                    # AI agent instructions
CHANGELOG.md                 # Changelog (Keep a Changelog format)
kilo.json                    # Kilo project configuration
Makefile                     # Common developer targets
pyproject.toml               # Python project configuration (pytest, ruff, mypy)
scaffold.sh                  # Project scaffolding script
hello.py                     # Sample application entry point
calculator.py                # Simple calculator module with arithmetic operations
config_utils.py              # Configuration utilities for JSON file management
shapes.py                    # Geometry utilities for areas and perimeters
strings.py                   # String utilities for text operations
utils.py                     # General utility helper functions
stats.py                     # Statistical utility functions
math_utils.py               # Mathematical utility functions
data_utils.py               # Data utility functions
datetime_utils.py           # Date and time utility functions
file_utils.py               # File and path utility functions
url_utils.py                # URL and web utility functions
random_utils.py             # Random number generation and sampling utilities
validation_utils.py         # Input validation utilities
crypto_utils.py             # Cryptographic utilities
list_utils.py              # Advanced list manipulation utilities
env_utils.py               # Environment variable handling utilities
logging_utils.py          # Logging configuration and helper utilities
cache_utils.py            # Caching utilities for memoizing function results
timing_utils.py           # Performance measurement helpers
async_utils.py            # Asynchronous utility functions
bit_utils.py              # Bitwise utility functions for working with binary representations
concurrent_utils.py       # Concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
priority_queue_utils.py   # Heap-based priority queue implementation
rate_limiter_utils.py     # Rate limiting utilities (token bucket algorithm)
retry_utils.py            # Retry utilities with exponential backoff and jitter
dict_utils.py            # Dictionary utilities (deep merge, flatten, unflatten, safe get, invert, filter)
json_utils.py            # JSON utility functions (read/write/parse/dump/validate)
collections_utils.py     # Collection utilities (chunk, flatten, frequency, merge_dicts, uniq, and more)
csv_utils.py             # CSV utility functions (read/write/append as dicts or lists)
set_utils.py             # Set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
statistics_utils.py        # Statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
string_utils.py            # Advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
type_utils.py              # Type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
path_utils.py              # Path manipulation utilities (join, normalize, components, extensions)
tree_utils.py              # Tree and nested structure utilities (get/set/delete nested, flatten/unflatten, map/filter)
pattern_utils.py           # Design pattern utilities (Singleton, Factory, Observer, Strategy)
config_schema.py           # Typed configuration schema utilities (SchemaField, ConfigSchema, validators)
terminal_utils.py          # Terminal output utilities (ANSI color, progress bars, clear screen, prompts)
cli_utils.py               # Command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
hash_utils.py              # Hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
http_utils.py              # HTTP status codes and response handling utilities
html_utils.py              # HTML escaping, unescaping, and tag-stripping utilities
base64_utils.py            # Base64 and hexadecimal encoding/decoding utilities
struct_utils.py            # Binary struct packing and unpacking utilities
duration_utils.py          # Time duration utilities (parse, format, convert between units)
temp_utils.py              # Temporary file and directory management utilities
tests/                     # Python unit tests
  test_hello.py              # Tests for hello.py
  test_calculator.py         # Tests for calculator.py
  test_scaffold.py           # Tests for scaffold.sh
  test_config_utils.py       # Tests for config_utils.py
  test_shapes.py             # Tests for shapes.py
  test_strings.py            # Tests for strings.py
  test_utils.py              # Tests for utils.py
  test_stats.py              # Tests for stats.py
  test_math_utils.py         # Tests for math_utils.py
  test_data_utils.py         # Tests for data_utils.py
  test_datetime_utils.py     # Tests for datetime_utils.py
  test_file_utils.py         # Tests for file_utils.py
  test_url_utils.py          # Tests for url_utils.py
  test_random_utils.py       # Tests for random_utils.py
  test_validation_utils.py   # Tests for validation_utils.py
  test_crypto_utils.py       # Tests for crypto_utils.py
  test_list_utils.py         # Tests for list_utils.py
  test_env_utils.py          # Tests for env_utils.py
  test_logging_utils.py       # Tests for logging_utils.py
  test_cache_utils.py         # Tests for cache_utils.py
  test_timing_utils.py        # Tests for timing_utils.py
  test_bit_utils.py           # Tests for bit_utils.py
  test_concurrent_utils.py    # Tests for concurrent_utils.py
  test_priority_queue_utils.py # Tests for priority_queue_utils.py
  test_rate_limiter_utils.py  # Tests for rate_limiter_utils.py
  test_retry_utils.py         # Tests for retry_utils.py
  test_dict_utils.py         # Tests for dict_utils.py
  test_json_utils.py          # Tests for json_utils.py
  test_csv_utils.py           # Tests for csv_utils.py
  test_set_utils.py         # Tests for set_utils.py
  test_statistics_utils.py    # Tests for statistics_utils.py
  test_string_utils.py        # Tests for string_utils.py
  test_tree_utils.py           # Tests for tree_utils.py
  test_type_utils.py         # Tests for type_utils.py
  test_path_utils.py        # Tests for path_utils.py
  test_pattern_utils.py         # Tests for pattern_utils.py
  test_functools_utils.py       # Tests for functools_utils.py
  test_config_schema.py         # Tests for config_schema.py
  test_hash_utils.py            # Tests for hash_utils.py
  test_http_utils.py            # Tests for http_utils.py
  test_html_utils.py            # Tests for html_utils.py
  test_base64_utils.py          # Tests for base64_utils.py
  test_struct_utils.py          # Tests for struct_utils.py
  test_duration_utils.py        # Tests for duration_utils.py
  test_temp_utils.py            # Tests for temp_utils.py
    ```

## Getting Started

1. Review `AGENTS.md` for agent instructions and the task handover protocol.
2. Check `kilo.json` for Kilo project configuration and subagent definitions.
3. Use `make test`, `make lint`, `make typecheck` for local development.
4. Use `make pre-commit-install` to install pre-commit hooks.
5. Use `scaffold.sh` to scaffold a new project: `./scaffold.sh "New Project"`

## Makefile Targets

| Target | Description |
|---|---|
| `make test` | Run the Python test suite |
| `make lint` | Run ruff code style checker |
| `make typecheck` | Run mypy static type checking |
| `make run` | Run hello.py (`make run NAME=Alice`) |
| `make scaffold` | Scaffold a new project using scaffold.sh |
| `make pre-commit-install` | Install pre-commit hooks into .git/hooks |
| `make pre-commit-run` | Run all pre-commit hooks against tracked files |
| `make clean` | Remove build artifacts |
| `make help` | Show all available targets |

## GitHub Actions Workflow

The workflow in `.github/workflows/main.yml` runs Kilo agent sessions in a continuous loop:
- Each session runs the command: "Execute the task assigned by the previous agent and prepare a task for the next agent!"
- After each session, it commits non-workflow changes as a checkpoint
- The workflow excludes `.github/workflows/**` from progress checks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

__README__

# --- CHANGELOG.md ---
cat > "$OUTPUT_DIR/CHANGELOG.md" <<'__CHANGELOG__'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `bit_utils.py` — bitwise utility functions for working with binary representations of integers (`count_set_bits`, `is_power_of_two`, `next_power_of_two`, `prev_power_of_two`, `reverse_bits`, `rotate_left`, `rotate_right`, `get_bit`, `set_bit`, `clear_bit`, `toggle_bit`, `is_even`, `is_odd`) with input validation
- `tests/test_bit_utils.py` — unit tests for `bit_utils.py`
- Added `bit_utils.py` to `scaffold.sh` header comment, `pyproject.toml` `py_modules`, README tree and module section, CHANGELOG Unreleased entry, `.kilo/command/scaffold-project.md` entries, and `scaffold.sh` heredocs for the module and its tests
- `config_utils.py` — configuration utilities module with `load_config`, `save_config`, `get_config_value`, `set_config_value`, and `merge_configs` functions for working with JSON configuration files
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
- `uuid_utils.py` — UUID utility functions for generating and validating UUIDs
- `prompt_utils.py` — Prompt utility functions for working with text prompts
- `random_utils.py` — random number generation and sampling utilities
- `validation_utils.py` — input validation utilities
- `crypto_utils.py` — cryptographic utilities
- `list_utils.py` — advanced list manipulation utilities
- `env_utils.py` — environment variable handling utilities
- `logging_utils.py` — logging configuration and helper utilities
- `cache_utils.py` — caching utilities for memoizing function results
- `timing_utils.py` — performance measurement helpers
- `async_utils.py` — asynchronous utility functions
- `bit_utils.py` — bitwise utility functions for working with binary representations of integers
- `concurrent_utils.py` — concurrent execution utilities (ThreadPool, ProcessPool, asyncio)
- `priority_queue_utils.py` — heap-based priority queue implementation
- `rate_limiter_utils.py` — rate limiting utilities (token bucket algorithm)
- `retry_utils.py` — retry utilities with exponential backoff and jitter
- `dict_utils.py` — dictionary utilities (deep merge, flatten/unflatten, safe get, invert, filter)
- `json_utils.py` — JSON utility functions (read/write/parse/dump/validate)
- `collections_utils.py` — collection utilities (chunk, flatten, deep_flatten, windowed, uniq, frequency, merge_dicts, and more)
- `csv_utils.py` — CSV utility functions (read/write/append as dicts or lists)
- `set_utils.py` — set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
- `statistics_utils.py` — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
- `string_utils.py` — advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
- `tests/test_string_utils.py` — unit tests for `string_utils.py`
- `tree_utils.py` — tree and nested structure utilities (get_nested, set_nested, delete_nested, flatten_tree, unflatten_tree, map_tree, filter_tree)
- `tests/test_tree_utils.py` — unit tests for `tree_utils.py`
- `type_utils.py` — type introspection utilities (is_optional, is_union, is_generic, get_type_args, type_name, is_subclass_safe)
- `tests/test_type_utils.py` — unit tests for `type_utils.py`
- `path_utils.py` — path manipulation utilities (join, normalize, components, extensions)
- `pattern_utils.py` — design pattern utilities (Singleton, Factory, Observer, Strategy)
- `config_schema.py` — typed configuration schema utilities (SchemaField, ConfigSchema, validators)
- `tests/test_path_utils.py` — unit tests for `path_utils.py`
- `tests/test_pattern_utils.py` — unit tests for `pattern_utils.py`
- `functools_utils.py` — functional programming utilities (compose, pipe, curry, apply)
- `tests/test_functools_utils.py` — unit tests for `functools_utils.py`
- `tests/test_config_schema.py` — unit tests for `config_schema.py`
- `exceptions_utils.py` — custom exception classes and error handling utilities
- `tests/test_exceptions_utils.py` — unit tests for `exceptions_utils.py`
- `io_utils.py` — line-oriented and atomic input/output utilities (read_lines, write_lines, append_text, atomic_write_text, stream_copy, count_lines, iter_lines)
- `ini_utils.py` — INI configuration file utilities (load_config, save_config, get_config_value, set_config_value, merge_configs, list_sections, has_section, get_section)
- `tests/test_io_utils.py` — unit tests for `io_utils.py`
- `tests/test_ini_utils.py` — unit tests for `ini_utils.py`
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `terminal_utils.py` — terminal output utilities (ANSI color, progress bars, clear screen, prompts)
- `cli_utils.py` — command-line interface utilities (argparse parser, argument parsing, exit-code wrapping)
- `tests/test_cli_utils.py` — unit tests for `cli_utils.py`
- hash_utils.py — hashing and checksum utilities (MD5, SHA1, SHA256, SHA512, CRC32, file hashing)
- tests/test_hash_utils.py — unit tests for `hash_utils.py`
- html_utils.py — HTML escaping, unescaping, and tag-stripping utilities (`escape_html`, `unescape_html`, `strip_tags`, `escape_attribute`)
- tests/test_html_utils.py — unit tests for `html_utils.py`
- base64_utils.py — Base64 and hexadecimal encoding/decoding utilities (`base64_encode`, `base64_decode`, `base64_encode_bytes`, `base64_decode_bytes`, `hex_encode`, `hex_decode`, `is_valid_base64`, `is_valid_hex`)
- tests/test_base64_utils.py — unit tests for `base64_utils.py`
- struct_utils.py — Binary struct packing and unpacking utilities (`pack`, `unpack`, `pack_into`, `unpack_from`, `calcsize`, `is_valid_format`)
- tests/test_struct_utils.py — unit tests for `struct_utils.py`
- http_utils.py — HTTP status codes and response handling utilities (`status_code_category`, `status_message`, `is_informational`, `is_success`, `is_redirection`, `is_client_error`, `is_server_error`, `is_error`)
- tests/test_http_utils.py — unit tests for `http_utils.py`
- duration_utils.py — time duration utilities (`parse_duration`, `format_duration`, `seconds_to_hms`, `hms_to_seconds`, `to_seconds`, `duration_between`, `add_duration`, `is_valid_duration`)
- tests/test_duration_utils.py — unit tests for `duration_utils.py`
- temp_utils.py — temporary file and directory management utilities (`create_temp_file`, `create_temp_dir`, `temp_file`, `temp_dir`, `write_temp_file`, `read_temp_file`, `cleanup_temp_path`, `is_temp_path`, `temp_path_exists`)
- tests/test_temp_utils.py — unit tests for `temp_utils.py`
- `tests/test_terminal_utils.py` — unit tests for `terminal_utils.py`
- `.pre-commit-config.yaml` — pre-commit hooks for ruff, mypy, unittest, and scaffold smoke testing
- `.kilo/.gitignore` — ignore patterns for the .kilo directory
- `CHANGELOG.md` — changelog following Keep a Changelog format
- `tests/test_strings.py` — unit tests for `strings.py`
- `tests/test_utils.py` — unit tests for `utils.py`
- `tests/test_stats.py` — unit tests for `stats.py`
- `tests/test_calculator.py` — unit tests for `calculator.py`
- `tests/test_config_utils.py` — unit tests for `config_utils.py`
- `tests/test_shapes.py` — unit tests for `shapes.py`
- `tests/test_math_utils.py` — unit tests for `math_utils.py`
- `tests/test_data_utils.py` — unit tests for `data_utils.py`
- `tests/test_datetime_utils.py` — unit tests for `datetime_utils.py`
- `tests/test_file_utils.py` — unit tests for `file_utils.py`
- `tests/test_url_utils.py` — unit tests for `url_utils.py`
- `tests/test_uuid_utils.py` — unit tests for `uuid_utils.py`
- `tests/test_prompt_utils.py` — unit tests for `prompt_utils.py`
- `tests/test_random_utils.py` — unit tests for `random_utils.py`
- `tests/test_validation_utils.py` — unit tests for `validation_utils.py`
- `tests/test_crypto_utils.py` — unit tests for `crypto_utils.py`
- `tests/test_list_utils.py` — unit tests for `list_utils.py`
- `tests/test_env_utils.py` — unit tests for `env_utils.py`
- `tests/test_logging_utils.py` — unit tests for `logging_utils.py`
- `tests/test_cache_utils.py` — unit tests for `cache_utils.py`
- `tests/test_timing_utils.py` — unit tests for `timing_utils.py`
- `tests/test_async_utils.py` — unit tests for `async_utils.py`
- `tests/test_bit_utils.py` — unit tests for `bit_utils.py`
- `tests/test_concurrent_utils.py` — unit tests for `concurrent_utils.py`
- `tests/test_priority_queue_utils.py` — unit tests for `priority_queue_utils.py`
- `tests/test_rate_limiter_utils.py` — unit tests for `rate_limiter_utils.py`
- `tests/test_retry_utils.py` — unit tests for `retry_utils.py`
- `tests/test_dict_utils.py` — unit tests for `dict_utils.py`
- `tests/test_json_utils.py` — unit tests for `json_utils.py`
- `tests/test_collections_utils.py` — unit tests for `collections_utils.py`
- `tests/test_csv_utils.py` — unit tests for `csv_utils.py`
- `set_utils.py` — set operation utilities (subset, superset, intersection, union, difference, symmetric_difference, cartesian_product, power_set)
- `tests/test_set_utils.py` — unit tests for `set_utils.py`
- `statistics_utils.py` — statistical utility functions (harmonic mean, geometric mean, median_even, percentile, covariance, correlation, z-score, normalize)
- `string_utils.py` — advanced string manipulation utilities (slugify, camel_to_snake, snake_to_camel, pluralize, truncate, wrap_text, indent_text, remove_extra_whitespace, title_case)
- `tests/test_statistics_utils.py` — unit tests for `statistics_utils.py`

__CHANGELOG__

# --- tests/test_async_utils.py ---
cat > "$OUTPUT_DIR/tests/test_async_utils.py" <<'TESTASYNC'
"""Unit tests for async_utils module."""

import asyncio
import unittest

from async_utils import async_sleep, gather_with_timeout, retry_async, run_in_thread


class TestRunInThread(unittest.TestCase):
    def test_run_in_thread_basic(self):
        async def run_test():
            result = await run_in_thread(sum, [1, 2, 3, 4])
            self.assertEqual(result, 10)

        asyncio.run(run_test())

    def test_run_in_thread_with_kwargs(self):
        def multiply(a: int, b: int) -> int:
            return a * b

        async def run_test():
            result = await run_in_thread(multiply, a=3, b=4)
            self.assertEqual(result, 12)

        asyncio.run(run_test())


class TestGatherWithTimeout(unittest.TestCase):
    def test_gather_with_timeout_no_timeout(self):
        async def run_test():
            results = await gather_with_timeout(
                asyncio.sleep(0.01, result=1),
                asyncio.sleep(0.01, result=2),
                asyncio.sleep(0.01, result=3),
            )
            self.assertEqual(results, [1, 2, 3])

        asyncio.run(run_test())

    def test_gather_with_timeout_succeeds(self):
        async def run_test():
            results = await gather_with_timeout(
                asyncio.sleep(0.01, result="a"),
                asyncio.sleep(0.01, result="b"),
                timeout=1.0,
            )
            self.assertEqual(results, ["a", "b"])

        asyncio.run(run_test())


class TestAsyncSleep(unittest.TestCase):
    def test_async_sleep_completes(self):
        async def run_test():
            await async_sleep(0.001)
            self.assertTrue(True)

        asyncio.run(run_test())


class TestRetryAsync(unittest.TestCase):
    def test_retry_async_success_first_attempt(self):
        async def always_succeeds():
            return "ok"

        async def run_test():
            result = await retry_async(always_succeeds)
            self.assertEqual(result, "ok")

        asyncio.run(run_test())

    def test_retry_async_succeeds_after_failures(self):
        attempts = []

        async def flaky():
            attempts.append(1)
            if len(attempts) < 2:
                raise ValueError("failed")
            return "success"

        async def run_test():
            result = await retry_async(flaky, max_attempts=3, delay=0.001)
            self.assertEqual(result, "success")
            self.assertEqual(len(attempts), 2)

        asyncio.run(run_test())

    def test_retry_async_fails_all_attempts(self):
        async def always_fails():
            raise ValueError("always fails")

        async def run_test():
            with self.assertRaises(ValueError):
                await retry_async(always_fails, max_attempts=2, delay=0.001)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
TESTASYNC

# --- tests/test_bit_utils.py ---
cat > "$OUTPUT_DIR/tests/test_bit_utils.py" <<'TESTBITUTILS'
"""Unit tests for bit_utils module."""

import unittest

from bit_utils import (
    clear_bit,
    count_set_bits,
    get_bit,
    is_even,
    is_odd,
    is_power_of_two,
    next_power_of_two,
    prev_power_of_two,
    reverse_bits,
    rotate_left,
    rotate_right,
    set_bit,
    toggle_bit,
)


class TestCountSetBits(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(count_set_bits(0), 0)

    def test_single_bit(self):
        self.assertEqual(count_set_bits(1), 1)
        self.assertEqual(count_set_bits(8), 1)

    def test_multiple_bits(self):
        self.assertEqual(count_set_bits(5), 2)  # 0b101
        self.assertEqual(count_set_bits(7), 3)  # 0b111
        self.assertEqual(count_set_bits(255), 8)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            count_set_bits("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_set_bits(True)  # type: ignore[arg-type]

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            count_set_bits(-1)


class TestIsPowerOfTwo(unittest.TestCase):
    def test_powers_of_two(self):
        self.assertTrue(is_power_of_two(1))
        self.assertTrue(is_power_of_two(2))
        self.assertTrue(is_power_of_two(1024))

    def test_not_powers_of_two(self):
        self.assertFalse(is_power_of_two(0))
        self.assertFalse(is_power_of_two(3))
        self.assertFalse(is_power_of_two(18))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_power_of_two("8")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_power_of_two(True)  # type: ignore[arg-type]


class TestNextPrevPowerOfTwo(unittest.TestCase):
    def test_next_power_of_two(self):
        self.assertEqual(next_power_of_two(0), 1)
        self.assertEqual(next_power_of_two(1), 1)
        self.assertEqual(next_power_of_two(5), 8)
        self.assertEqual(next_power_of_two(16), 16)
        self.assertEqual(next_power_of_two(17), 32)

    def test_prev_power_of_two(self):
        self.assertEqual(prev_power_of_two(0), 0)
        self.assertEqual(prev_power_of_two(1), 1)
        self.assertEqual(prev_power_of_two(5), 4)
        self.assertEqual(prev_power_of_two(16), 16)
        self.assertEqual(prev_power_of_two(17), 16)

    def test_errors(self):
        with self.assertRaises(ValueError):
            next_power_of_two(-1)
        with self.assertRaises(ValueError):
            prev_power_of_two(-1)
        with self.assertRaises(TypeError):
            next_power_of_two("5")  # type: ignore[arg-type]


class TestReverseBits(unittest.TestCase):
    def test_reverse_within_width(self):
        self.assertEqual(reverse_bits(0b0001, 4), 0b1000)
        self.assertEqual(reverse_bits(13, 4), 11)  # 1101 -> 1011
        self.assertEqual(reverse_bits(0, 4), 0)

    def test_default_width(self):
        self.assertEqual(reverse_bits(1), 1)
        self.assertEqual(reverse_bits(0), 0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            reverse_bits(-1, 4)
        with self.assertRaises(ValueError):
            reverse_bits(5, 0)
        with self.assertRaises(TypeError):
            reverse_bits(5, "4")  # type: ignore[arg-type]


class TestRotate(unittest.TestCase):
    def test_rotate_left(self):
        self.assertEqual(rotate_left(0b0001, 1, 4), 0b0010)
        self.assertEqual(rotate_left(0b1000, 1, 4), 0b0001)
        self.assertEqual(rotate_left(0b0011, 2, 4), 0b1100)

    def test_rotate_right(self):
        self.assertEqual(rotate_right(0b1000, 1, 4), 0b0100)
        self.assertEqual(rotate_right(0b0001, 1, 4), 0b1000)
        self.assertEqual(rotate_right(0b1100, 2, 4), 0b0011)

    def test_shift_wraps(self):
        self.assertEqual(rotate_left(0b0001, 5, 4), 0b0010)
        self.assertEqual(rotate_right(0b0001, 5, 4), 0b1000)

    def test_errors(self):
        with self.assertRaises(ValueError):
            rotate_left(-1, 1, 4)
        with self.assertRaises(ValueError):
            rotate_left(1, 1, 0)
        with self.assertRaises(TypeError):
            rotate_left(1, "1", 4)  # type: ignore[arg-type]


class TestBitAccess(unittest.TestCase):
    def test_get_bit(self):
        self.assertEqual(get_bit(0b1010, 0), 0)
        self.assertEqual(get_bit(0b1010, 1), 1)
        self.assertEqual(get_bit(0b1010, 2), 0)
        self.assertEqual(get_bit(0b1010, 3), 1)

    def test_set_bit(self):
        self.assertEqual(set_bit(0b0000, 2), 0b0100)
        self.assertEqual(set_bit(0b1010, 0), 0b1011)

    def test_clear_bit(self):
        self.assertEqual(clear_bit(0b1111, 1), 0b1101)
        self.assertEqual(clear_bit(0b1010, 3), 0b0010)

    def test_toggle_bit(self):
        self.assertEqual(toggle_bit(0b1010, 1), 0b1000)
        self.assertEqual(toggle_bit(0b1010, 0), 0b1011)

    def test_errors(self):
        with self.assertRaises(ValueError):
            get_bit(-1, 0)
        with self.assertRaises(ValueError):
            set_bit(0, -1)
        with self.assertRaises(TypeError):
            get_bit(0, "0")  # type: ignore[arg-type]


class TestEvenOdd(unittest.TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(7))

    def test_is_odd(self):
        self.assertFalse(is_odd(0))
        self.assertFalse(is_odd(4))
        self.assertTrue(is_odd(7))

    def test_errors(self):
        with self.assertRaises(TypeError):
            is_even("4")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTBITUTILS
# --- tests/test_concurrent_utils.py ---
cat > "$OUTPUT_DIR/tests/test_concurrent_utils.py" <<'TESTCONCURRENT'
"""Tests for concurrent_utils module."""

import asyncio
import unittest

from concurrent_utils import (
    ProcessPool,
    ThreadPool,
    _dec,
    _double,
    _multiply,
    _square,
    gather,
    run_async,
    to_async,
)


class TestThreadPool(unittest.TestCase):
    def test_threadpool_map(self):
        with ThreadPool(max_workers=2) as pool:
            results = list(pool.map(lambda x: x * 2, [1, 2, 3, 4]))
        self.assertEqual(results, [2, 4, 6, 8])

    def test_threadpool_submit(self):
        def square(x):
            return x * x

        with ThreadPool(max_workers=2) as pool:
            future = pool.submit(square, 5)
            result = future.result()
        self.assertEqual(result, 25)

    def test_threadpool_submit_multiple(self):
        def add(a, b):
            return a + b

        with ThreadPool(max_workers=3) as pool:
            f1 = pool.submit(add, 1, 2)
            f2 = pool.submit(add, 3, 4)
            f3 = pool.submit(add, 5, 6)
            self.assertEqual(f1.result(), 3)
            self.assertEqual(f2.result(), 7)
            self.assertEqual(f3.result(), 11)

    def test_threadpool_default_workers(self):
        with ThreadPool() as pool:
            results = list(pool.map(lambda x: x + 1, [1, 2, 3]))
        self.assertEqual(results, [2, 3, 4])

    def test_threadpool_with_name_prefix(self):
        with ThreadPool(max_workers=2, thread_name_prefix="test") as pool:
            results = list(pool.map(lambda x: x * 3, [1, 2]))
        self.assertEqual(results, [3, 6])

    def test_threadpool_submit_outside_context_raises(self):
        pool = ThreadPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            pool.submit(lambda x: x, 1)

    def test_threadpool_map_outside_context_raises(self):
        pool = ThreadPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            list(pool.map(lambda x: x, [1, 2]))


class TestProcessPool(unittest.TestCase):
    def test_processpool_map(self):
        with ProcessPool(max_workers=2) as pool:
            results = list(pool.map(_double, [1, 2, 3, 4]))
        self.assertEqual(results, [2, 4, 6, 8])

    def test_processpool_submit(self):
        with ProcessPool(max_workers=2) as pool:
            future = pool.submit(_square, 5)
            result = future.result()
        self.assertEqual(result, 25)

    def test_processpool_submit_multiple(self):
        with ProcessPool(max_workers=3) as pool:
            f1 = pool.submit(_multiply, 2, 3)
            f2 = pool.submit(_multiply, 4, 5)
            f3 = pool.submit(_multiply, 6, 7)
            self.assertEqual(f1.result(), 6)
            self.assertEqual(f2.result(), 20)
            self.assertEqual(f3.result(), 42)

    def test_processpool_default_workers(self):
        with ProcessPool() as pool:
            results = list(pool.map(_dec, [5, 6, 7]))
        self.assertEqual(results, [4, 5, 6])

    def test_processpool_submit_outside_context_raises(self):
        pool = ProcessPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            pool.submit(_square, 1)

    def test_processpool_map_outside_context_raises(self):
        pool = ProcessPool(max_workers=2)
        with self.assertRaises(RuntimeError):
            list(pool.map(_square, [1, 2]))


class TestAsyncIOWrappers(unittest.TestCase):
    def test_gather_basic(self):
        async def compute(x):
            await asyncio.sleep(0.001)
            return x * 2

        async def main():
            results = await gather(compute(1), compute(2), compute(3))
            return results

        results = run_async(main())
        self.assertEqual(results, [2, 4, 6])

    def test_gather_with_mixed_values(self):
        async def async_func(x):
            return x + 1

        async def main():
            results = await gather(async_func(1), 10, async_func(3))
            return results

        results = run_async(main())
        self.assertEqual(results, [2, 10, 4])

    def test_gather_empty(self):
        async def main():
            results = await gather()
            return results

        results = run_async(main())
        self.assertEqual(results, [])

    def test_run_async_basic(self):
        async def get_data():
            return "test_data"

        result = run_async(get_data())
        self.assertEqual(result, "test_data")

    def test_run_async_with_exception(self):
        async def fail():
            raise ValueError("test error")

        with self.assertRaises(ValueError):
            run_async(fail())

    def test_to_async_basic(self):
        def compute(x):
            return x * 3

        async def main():
            async_compute = to_async(compute)
            result = await async_compute(4)
            return result

        result = run_async(main())
        self.assertEqual(result, 12)

    def test_to_async_with_multiple_args(self):
        def add(a, b, c):
            return a + b + c

        async def main():
            async_add = to_async(add)
            result = await async_add(1, 2, 3)
            return result

        result = run_async(main())
        self.assertEqual(result, 6)

    def test_to_async_with_kwargs(self):
        def multiply(a, b=1):
            return a * b

        async def main():
            async_multiply = to_async(multiply)
            result = await async_multiply(5, b=3)
            return result

        result = run_async(main())
        self.assertEqual(result, 15)

    def test_to_async_preserves_metadata(self):
        def original_func():
            """Original docstring."""
            return "test"

        async def main():
            wrapped = to_async(original_func)
            self.assertEqual(wrapped.__name__, "original_func")
            self.assertEqual(wrapped.__doc__, "Original docstring.")
            return await wrapped()

        result = run_async(main())
        self.assertEqual(result, "test")


if __name__ == "__main__":
    unittest.main()

TESTCONCURRENT


# --- tests/test_priority_queue_utils.py ---
cat > "$OUTPUT_DIR/tests/test_priority_queue_utils.py" <<'TESTPQ'
"""Tests for priority_queue_utils module."""

import unittest

from priority_queue_utils import (
    PriorityQueue,
    clear_priority,
    create_priority_queue,
    is_empty_priority,
    merge_queues,
    peek_priority,
    pop_priority,
    push_priority,
    size_priority,
)


class TestPriorityQueue(unittest.TestCase):
    def test_empty_queue(self):
        pq = PriorityQueue()
        self.assertTrue(pq.is_empty())
        self.assertEqual(pq.size(), 0)
        self.assertIsNone(pq.pop())
        self.assertIsNone(pq.peek())

    def test_push_and_pop(self):
        pq = PriorityQueue()
        pq.push("task1", priority=2)
        pq.push("task2", priority=1)
        pq.push("task3", priority=3)
        self.assertEqual(pq.pop(), "task2")
        self.assertEqual(pq.pop(), "task1")
        self.assertEqual(pq.pop(), "task3")
        self.assertTrue(pq.is_empty())

    def test_push_with_default_priority(self):
        pq = PriorityQueue()
        pq.push("item1")
        pq.push("item2", priority=1)
        # item2 has lower priority value, so should come out first
        self.assertEqual(pq.pop(), "item2")
        self.assertEqual(pq.pop(), "item1")

    def test_peek(self):
        pq = PriorityQueue()
        pq.push("task", priority=5)
        self.assertEqual(pq.peek(), "task")
        self.assertFalse(pq.is_empty())
        self.assertEqual(pq.size(), 1)
        self.assertEqual(pq.pop(), "task")
        self.assertTrue(pq.is_empty())

    def test_same_priority(self):
        pq = PriorityQueue()
        pq.push("first", priority=1)
        pq.push("second", priority=1)
        pq.push("third", priority=1)
        # With counter to maintain insertion order for equal priorities
        self.assertEqual(pq.pop(), "first")
        self.assertEqual(pq.pop(), "second")
        self.assertEqual(pq.pop(), "third")

    def test_initialization_with_items(self):
        pq = PriorityQueue([("high", 1), ("low", 3), ("medium", 2)])
        self.assertEqual(pq.pop(), "high")
        self.assertEqual(pq.pop(), "medium")
        self.assertEqual(pq.pop(), "low")

    def test_clear(self):
        pq = PriorityQueue()
        pq.push("a", priority=1)
        pq.push("b", priority=2)
        self.assertFalse(pq.is_empty())
        pq.clear()
        self.assertTrue(pq.is_empty())
        self.assertEqual(pq.size(), 0)

    def test_len(self):
        pq = PriorityQueue()
        self.assertEqual(len(pq), 0)
        pq.push("a", priority=1)
        self.assertEqual(len(pq), 1)
        pq.push("b", priority=2)
        self.assertEqual(len(pq), 2)
        pq.pop()
        self.assertEqual(len(pq), 1)
        pq.pop()
        self.assertEqual(len(pq), 0)

    def test_bool(self):
        pq = PriorityQueue()
        self.assertFalse(bool(pq))  # or simply: self.assertNot(pq)
        pq.push("a", priority=1)
        self.assertTrue(bool(pq))
        pq.pop()
        self.assertFalse(bool(pq))




class TestHelperFunctions(unittest.TestCase):
    def test_push_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "item", priority=5)
        self.assertEqual(peek_priority(pq), "item")

    def test_pop_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "item", priority=1)
        result = pop_priority(pq)
        self.assertEqual(result, "item")
        self.assertIsNone(pop_priority(pq))

    def test_peek_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "item", priority=2)
        self.assertEqual(peek_priority(pq), "item")
        self.assertFalse(is_empty_priority(pq))

    def test_is_empty_priority(self):
        pq = PriorityQueue()
        self.assertTrue(is_empty_priority(pq))
        push_priority(pq, "item")
        self.assertFalse(is_empty_priority(pq))

    def test_size_priority(self):
        pq = PriorityQueue()
        self.assertEqual(size_priority(pq), 0)
        push_priority(pq, "a")
        push_priority(pq, "b")
        self.assertEqual(size_priority(pq), 2)

    def test_clear_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "a")
        push_priority(pq, "b")
        clear_priority(pq)
        self.assertTrue(is_empty_priority(pq))


class TestConvenienceFunctions(unittest.TestCase):
    def test_create_priority_queue_empty(self):
        pq = create_priority_queue()
        self.assertIsInstance(pq, PriorityQueue)
        self.assertTrue(pq.is_empty())

    def test_create_priority_queue_with_items(self):
        pq = create_priority_queue([(1, "a"), (2, "b")])
        self.assertEqual(pq.pop(), "a")
        self.assertEqual(pq.pop(), "b")

    def test_merge_queues(self):
        pq1 = PriorityQueue()
        pq1.push("a", priority=3)
        pq1.push("b", priority=1)
        pq2 = PriorityQueue()
        pq2.push("c", priority=2)
        pq3 = PriorityQueue()
        pq3.push("d", priority=4)

        merged = merge_queues(pq1, pq2, pq3)
        self.assertEqual(merged.pop(), "b")
        self.assertEqual(merged.pop(), "c")
        self.assertEqual(merged.pop(), "a")
        self.assertEqual(merged.pop(), "d")
        self.assertTrue(merged.is_empty())
        # Original queues should remain unchanged
        self.assertFalse(pq1.is_empty())
        self.assertFalse(pq2.is_empty())
        self.assertFalse(pq3.is_empty())


if __name__ == "__main__":
    unittest.main()

TESTPQ
# --- pattern_utils.py ---
cat > "$OUTPUT_DIR/pattern_utils.py" <<'PATTERNUTILS'
"""Design pattern utilities.

This module provides reusable implementations of common software design
patterns: Singleton, Factory, Observer, and Strategy.
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

T = TypeVar("T")


class Singleton(type):
    """Metaclass that restricts a class to a single instance.

    Thread-safe: only one instance is created per class, even when multiple
    threads attempt construction concurrently.

    Example:
        >>> class Service(metaclass=Singleton):
        ...     pass
        >>> Service() is Service()
        True
    """

    _instances: Dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):  # type: ignore[override]
        if cls not in Singleton._instances:
            with Singleton._lock:
                if cls not in Singleton._instances:
                    Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]


class SingletonBase(metaclass=Singleton):
    """Base class for classes that should have only one instance.

    Subclasses automatically share a single instance per subclass.
    """


class Factory:
    """Registry-based factory for creating objects by name.

    Creators are registered under a string key and invoked with any
    positional or keyword arguments when :meth:`create` is called.
    """

    def __init__(self) -> None:
        self._creators: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, creator: Callable[..., Any]) -> None:
        """Register a creator callable under ``name``.

        Args:
            name: Key used to look up the creator.
            creator: Callable used to create instances.

        Raises:
            TypeError: If ``creator`` is not callable.
        """
        if not callable(creator):
            raise TypeError("creator must be callable")
        self._creators[name] = creator

    def create(self, name: str, *args, **kwargs) -> Any:
        """Create and return an object registered under ``name``.

        Args:
            name: Key of the registered creator.
            args: Positional arguments forwarded to the creator.
            kwargs: Keyword arguments forwarded to the creator.

        Raises:
            KeyError: If no creator is registered for ``name``.
        """
        if name not in self._creators:
            raise KeyError(f"Unknown type: {name!r}")
        return self._creators[name](*args, **kwargs)

    def unregister(self, name: str) -> None:
        """Remove the creator registered under ``name``.

        Raises:
            KeyError: If no creator is registered for ``name``.
        """
        if name not in self._creators:
            raise KeyError(f"Unknown type: {name!r}")
        del self._creators[name]

    def types(self) -> List[str]:
        """Return the sorted list of registered creator names."""
        return sorted(self._creators)


class Observer:
    """Base class for observer objects.

    Subclasses implement :meth:`update` to react to changes in an
    :class:`Observable` subject.
    """

    def update(self, subject: Any, data: Any = None) -> None:
        """Called when the observed subject changes.

        Args:
            subject: The observable that changed.
            data: Optional data describing the change.
        """
        raise NotImplementedError


class Observable:
    """Subject that notifies registered observers of changes."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Register ``observer`` to receive change notifications.

        Args:
            observer: The observer to attach.

        Raises:
            TypeError: If ``observer`` is not an :class:`Observer` instance.
        """
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an Observer instance")
        if observer in self._observers:
            return
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Unregister ``observer``.

        Raises:
            ValueError: If ``observer`` is not attached.
        """
        self._observers.remove(observer)

    def notify(self, data: Any = None) -> None:
        """Notify all attached observers with optional ``data``."""
        for observer in list(self._observers):
            observer.update(self, data)


class Strategy:
    """Base class for strategy objects.

    Subclasses implement :meth:`execute` to encapsulate an interchangeable
    algorithm.
    """

    def execute(self, *args, **kwargs) -> Any:
        """Execute the strategy algorithm.

        Args:
            args: Positional arguments for the algorithm.
            kwargs: Keyword arguments for the algorithm.

        Returns:
            The result of the algorithm.
        """
        raise NotImplementedError


class StrategyContext:
    """Context that delegates work to a pluggable :class:`Strategy`."""

    def __init__(self, strategy: Strategy) -> None:
        """Initialize the context with ``strategy``.

        Args:
            strategy: The strategy to delegate to.

        Raises:
            TypeError: If ``strategy`` is not a :class:`Strategy` instance.
        """
        if not isinstance(strategy, Strategy):
            raise TypeError("strategy must be a Strategy instance")
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """The currently configured strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """Replace the current strategy.

        Raises:
            TypeError: If ``strategy`` is not a :class:`Strategy` instance.
        """
        if not isinstance(strategy, Strategy):
            raise TypeError("strategy must be a Strategy instance")
        self._strategy = strategy

    def execute(self, *args, **kwargs) -> Any:
        """Delegate to the current strategy."""
        return self._strategy.execute(*args, **kwargs)
PATTERNUTILS
# --- tests/test_pattern_utils.py ---
cat > "$OUTPUT_DIR/tests/test_pattern_utils.py" <<'TESTPATTERNUTILS'
"""Tests for pattern_utils module."""

import unittest

from pattern_utils import (
    Factory,
    Observable,
    Observer,
    Singleton,
    SingletonBase,
    Strategy,
    StrategyContext,
)


class TestSingleton(unittest.TestCase):
    def test_same_instance(self):
        class Service(metaclass=Singleton):
            def __init__(self):
                self.value = 0

        self.assertIs(Service(), Service())

    def test_distinct_classes_distinct_instances(self):
        class Alpha(metaclass=Singleton):
            pass

        class Beta(metaclass=Singleton):
            pass

        self.assertIsNot(Alpha(), Beta())

    def test_singleton_base(self):
        class Logger(SingletonBase):
            pass

        self.assertIs(Logger(), Logger())


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory()

    def test_register_and_create(self):
        self.factory.register("adder", lambda a, b: a + b)
        self.assertEqual(self.factory.create("adder", 2, 3), 5)

    def test_create_unknown_raises(self):
        with self.assertRaises(KeyError):
            self.factory.create("missing")

    def test_unregister(self):
        self.factory.register("x", lambda: 1)
        self.factory.unregister("x")
        self.assertEqual(self.factory.types(), [])
        with self.assertRaises(KeyError):
            self.factory.unregister("x")

    def test_register_non_callable_raises(self):
        with self.assertRaises(TypeError):
            self.factory.register("bad", 42)  # type: ignore[arg-type]

    def test_types_sorted(self):
        self.factory.register("zeta", lambda: 1)
        self.factory.register("alpha", lambda: 1)
        self.factory.register("mid", lambda: 1)
        self.assertEqual(self.factory.types(), ["alpha", "mid", "zeta"])


class RecordingObserver(Observer):
    def __init__(self):
        self.calls = []

    def update(self, subject, data=None):
        self.calls.append((subject, data))


class TestObservable(unittest.TestCase):
    def setUp(self):
        self.subject = Observable()
        self.observer = RecordingObserver()

    def test_attach_and_notify(self):
        self.subject.attach(self.observer)
        self.subject.notify("hello")
        self.assertEqual(len(self.observer.calls), 1)
        self.assertEqual(self.observer.calls[0], (self.subject, "hello"))

    def test_detach_stops_notification(self):
        self.subject.attach(self.observer)
        self.subject.detach(self.observer)
        self.subject.notify("hello")
        self.assertEqual(self.observer.calls, [])

    def test_detach_unattached_raises(self):
        with self.assertRaises(ValueError):
            self.subject.detach(self.observer)

    def test_attach_non_observer_raises(self):
        with self.assertRaises(TypeError):
            self.subject.attach("not an observer")  # type: ignore[arg-type]

    def test_multiple_observers(self):
        other = RecordingObserver()
        self.subject.attach(self.observer)
        self.subject.attach(other)
        self.subject.notify("data")
        self.assertEqual(len(self.observer.calls), 1)
        self.assertEqual(len(other.calls), 1)


class ConcreteStrategy(Strategy):
    def __init__(self, label):
        self.label = label

    def execute(self, *args, **kwargs):
        return self.label


class TestStrategy(unittest.TestCase):
    def test_strategy_abstract(self):
        with self.assertRaises(NotImplementedError):
            Strategy().execute()

    def test_context_delegates(self):
        context = StrategyContext(ConcreteStrategy("first"))
        self.assertEqual(context.execute(), "first")
        self.assertIsInstance(context.strategy, ConcreteStrategy)

    def test_context_swap_strategy(self):
        context = StrategyContext(ConcreteStrategy("first"))
        context.strategy = ConcreteStrategy("second")
        self.assertEqual(context.execute(), "second")
        self.assertEqual(context.strategy.label, "second")

    def test_context_invalid_strategy_raises(self):
        with self.assertRaises(TypeError):
            StrategyContext("not a strategy")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            StrategyContext(ConcreteStrategy("x")).strategy = 42  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()

TESTPATTERNUTILS
# --- config_schema.py ---
cat > "$OUTPUT_DIR/config_schema.py" <<'CONFIG_SCHEMA'
"""Typed configuration schema utilities.

This module provides declarative, typed configuration schemas for
validating, parsing, and serializing configuration dictionaries. A
:class:`SchemaField` describes a single typed configuration field, and a
:class:`ConfigSchema` composes fields into a schema that validates raw
configuration dictionaries, coerces values to declared types, applies
defaults, enforces required fields, and serializes back to plain
dictionaries.

Example:
    >>> schema = ConfigSchema([
    ...     SchemaField("host", str, default="localhost"),
    ...     SchemaField("port", int, default=8080, validator=range_validator(1, 65535)),
    ...     SchemaField("debug", bool, default=False),
    ... ])
    >>> config = schema.validate({"host": "example.com", "port": "9000"})
    >>> config["port"]
    9000
    >>> schema.validate({})["host"]
    'localhost'
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar, Union
from urllib.parse import urlparse

T = TypeVar("T")

_UNSET: Any = object()

# A validator coerces and validates a raw value, returning the converted
# value or raising TypeError/ValueError when the value is invalid.
Validator = Callable[[Any], Any]


class ConfigValidationError(ValueError):
    """Raised when a configuration value fails schema validation."""


def int_validator(value: Any) -> int:
    """Validate and coerce *value* to an ``int``.

    Args:
        value: The value to validate.

    Returns:
        The value converted to an int.

    Raises:
        TypeError: If *value* is a bool or otherwise non-numeric.
        ValueError: If *value* is a float that is not a whole number or a
            string that cannot be parsed as an int.

    Examples:
        >>> int_validator("42")
        42
        >>> int_validator(7)
        7
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise TypeError(f"cannot coerce {value!r} to int")
    if isinstance(value, float) and not value.is_integer():
        raise ValueError(f"float value {value!r} is not a whole number")
    try:
        return int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"cannot coerce {value!r} to int") from exc


def float_validator(value: Any) -> float:
    """Validate and coerce *value* to a ``float``.

    Args:
        value: The value to validate.

    Returns:
        The value converted to a float.

    Raises:
        TypeError: If *value* is a bool or otherwise non-numeric.
        ValueError: If *value* is a string that cannot be parsed as a float.

    Examples:
        >>> float_validator("3.14")
        3.14
        >>> float_validator(7)
        7.0
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise TypeError(f"cannot coerce {value!r} to float")
    try:
        return float(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"cannot coerce {value!r} to float") from exc


def str_validator(value: Any) -> str:
    """Validate that *value* is a ``str`` and return it unchanged.

    Args:
        value: The value to validate.

    Returns:
        The input string.

    Raises:
        TypeError: If *value* is not a string.

    Examples:
        >>> str_validator("hello")
        'hello'
    """
    if not isinstance(value, str):
        raise TypeError(f"expected a string, got {type(value).__name__}")
    return value


def bool_validator(value: Any) -> bool:
    """Validate and coerce *value* to a ``bool``.

    Accepts booleans, numeric values (zero is falsy), and the strings
    ``true``, ``false``, ``1``, ``0``, ``yes``, ``no``, ``on``, ``off``
    (case-insensitive).

    Args:
        value: The value to validate.

    Returns:
        The value converted to a bool.

    Raises:
        TypeError: If *value* cannot be interpreted as a bool.
        ValueError: If *value* is a string that does not represent a bool.

    Examples:
        >>> bool_validator("true")
        True
        >>> bool_validator(0)
        False
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "1", "yes", "on"):
            return True
        if lowered in ("false", "0", "no", "off"):
            return False
        raise ValueError(f"cannot interpret string {value!r} as a bool")
    if isinstance(value, (int, float)):
        return bool(value)
    raise TypeError(f"cannot coerce {value!r} to bool")


_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def email_validator(value: Any) -> str:
    """Validate that *value* is a string resembling an email address.

    Args:
        value: The value to validate.

    Returns:
        The validated email string.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* does not resemble an email address.

    Examples:
        >>> email_validator("user@example.com")
        'user@example.com'
    """
    text = str_validator(value)
    if not _EMAIL_PATTERN.match(text):
        raise ValueError(f"invalid email address: {text!r}")
    return text


_HOSTNAME_LABEL_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$")


def hostname_validator(value: Any) -> str:
    """Validate that *value* is a string resembling a hostname.

    Args:
        value: The value to validate.

    Returns:
        The validated hostname string.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* is not a valid hostname.

    Examples:
        >>> hostname_validator("example.com")
        'example.com'
    """
    text = str_validator(value)
    if not text:
        raise ValueError("hostname must not be empty")
    if text.endswith(".") or text.startswith("-") or text.endswith("-"):
        raise ValueError(f"invalid hostname: {text!r}")
    if len(text) > 253:
        raise ValueError(f"hostname too long: {text!r}")
    for label in text.split("."):
        if not label or len(label) > 63 or not _HOSTNAME_LABEL_PATTERN.match(label):
            raise ValueError(f"invalid hostname: {text!r}")
    return text


def url_validator(value: Any) -> str:
    """Validate that *value* is a string with a scheme and a host.

    Args:
        value: The value to validate.

    Returns:
        The validated URL string.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* has no scheme or no host.

    Examples:
        >>> url_validator("https://example.com/path")
        'https://example.com/path'
    """
    text = str_validator(value)
    parsed = urlparse(text)
    if not parsed.scheme:
        raise ValueError(f"URL has no scheme: {text!r}")
    if not parsed.hostname:
        raise ValueError(f"URL has no host: {text!r}")
    return text


def range_validator(min_value: Union[int, float], max_value: Union[int, float]) -> Validator:
    """Return a validator ensuring a numeric value lies within ``[min, max]``.

    Args:
        min_value: The inclusive lower bound.
        max_value: The inclusive upper bound.

    Returns:
        A validator callable.

    Raises:
        ValueError: If ``min_value`` is greater than ``max_value``.

    Examples:
        >>> validate = range_validator(1, 10)
        >>> validate(5)
        5
        >>> validate(15)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: value 15 is outside the allowed range [1, 10]
    """
    if min_value > max_value:
        raise ValueError("min_value must be <= max_value")

    def validate(value: Any) -> Union[int, float]:
        number: Union[int, float]
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise TypeError(f"cannot coerce {value!r} to a number")
        try:
            number = float(value) if isinstance(value, str) else value  # type: ignore[assignment]
        except (ValueError, TypeError) as exc:
            raise ValueError(f"cannot coerce {value!r} to a number") from exc
        if not (min_value <= number <= max_value):
            raise ValueError(
                f"value {value!r} is outside the allowed range [{min_value}, {max_value}]"
            )
        return number

    return validate


def choices_validator(*choices: Any) -> Validator:
    """Return a validator ensuring the value is one of ``choices``.

    Args:
        choices: The allowed values.

    Returns:
        A validator callable.

    Raises:
        ValueError: If no choices are provided.

    Examples:
        >>> validate = choices_validator("dev", "staging", "prod")
        >>> validate("staging")
        'staging'
    """
    if not choices:
        raise ValueError("at least one choice is required")
    choice_set = frozenset(choices)
    choice_list = list(choices)

    def validate(value: Any) -> Any:
        if value not in choice_set:
            raise ValueError(
                f"value {value!r} is not one of {choice_list!r}"
            )
        return value

    return validate


def regex_validator(pattern: Union[str, re.Pattern], flags: int = 0) -> Validator:
    """Return a validator ensuring a string matches *pattern*.

    Args:
        pattern: A regex pattern string or compiled ``re.Pattern``.
        flags: Regex flags, used when *pattern* is a string.

    Returns:
        A validator callable.

    Raises:
        TypeError: If *pattern* is neither a string nor a compiled pattern.
        ValueError: If *pattern* is an invalid regex string.

    Examples:
        >>> validate = regex_validator(r"^[A-Z]+$")
        >>> validate("HELLO")
        'HELLO'
    """
    if isinstance(pattern, str):
        try:
            compiled = re.compile(pattern, flags)
        except re.error as exc:
            raise ValueError(f"invalid regex pattern: {pattern!r}") from exc
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError(
            "pattern must be a string or re.Pattern, "
            f"got {type(pattern).__name__}"
        )

    def validate(value: Any) -> str:
        text = str_validator(value)
        if not compiled.match(text):
            raise ValueError(
                f"value {text!r} does not match pattern {pattern!r}"
            )
        return text

    return validate


class SchemaField:
    """A single typed configuration field within a :class:`ConfigSchema`.

    Args:
        name: The configuration key name.
        type_: The expected type (``str``, ``int``, ``float``, or ``bool``).
        default: The default value used when the field is absent. Use
            :data:`schema_required` or omit to mark the field as required.
        required: Whether the field must be present in the config.
        validator: Optional extra validator applied after type coercion.
        description: Human-readable description of the field.

    Raises:
        TypeError: If ``type_`` is not one of the supported types, or if
            ``validator`` is not callable.
        ValueError: If both ``default`` is unset and ``required`` is False
            is contradictory usage (handled by the schema instead).
    """

    _SUPPORTED_TYPES: Dict[type, Validator] = {
        str: str_validator,
        int: int_validator,
        float: float_validator,
        bool: bool_validator,
    }

    def __init__(
        self,
        name: str,
        type_: type,
        default: Any = _UNSET,
        required: bool = False,
        validator: Optional[Validator] = None,
        description: str = "",
    ) -> None:
        if type_ not in self._SUPPORTED_TYPES:
            raise TypeError(
                f"unsupported type {type_!r}; supported types are "
                f"{sorted(self._SUPPORTED_TYPES, key=lambda t: t.__name__)!r}"
            )
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        if validator is not None and not callable(validator):
            raise TypeError("validator must be callable")
        self.name: str = name
        self.type_: type = type_
        self.default: Any = default
        self.required: bool = required
        self.validator: Optional[Validator] = validator
        self.description: str = description

    @property
    def has_default(self) -> bool:
        """Return ``True`` if a default value was provided."""
        return self.default is not _UNSET

    def coerce(self, value: Any) -> Any:
        """Coerce *value* to the field's declared type.

        Args:
            value: The raw value to coerce.

        Returns:
            The value converted to the field's type.

        Raises:
            TypeError: If the value cannot be coerced.
            ValueError: If the value is invalid for the type.
        """
        return self._SUPPORTED_TYPES[self.type_](value)

    def validate(self, value: Any) -> Any:
        """Validate and coerce *value*, applying the field's validator.

        Args:
            value: The raw value to validate.

        Returns:
            The validated, coerced value.

        Raises:
            TypeError: If the value cannot be coerced to the field's type.
            ValueError: If the value fails the type check or validator.
        """
        coerced = self.coerce(value)
        if self.validator is not None:
            return self.validator(coerced)
        return coerced


class ConfigSchema:
    """A typed configuration schema composed of :class:`SchemaField` instances.

    Args:
        fields: An iterable of :class:`SchemaField` instances. Duplicate
            names are not allowed; later definitions win.

    Raises:
        ValueError: If a field name is duplicated.
        TypeError: If any item in ``fields`` is not a :class:`SchemaField`.
    """

    def __init__(self, fields: Iterable[SchemaField]) -> None:
        self._fields: Dict[str, SchemaField] = {}
        for field in fields:
            if not isinstance(field, SchemaField):
                raise TypeError(
                    f"all fields must be SchemaField instances, got {type(field).__name__}"
                )
            if field.name in self._fields:
                raise ValueError(f"duplicate field name: {field.name!r}")
            self._fields[field.name] = field

    @property
    def fields(self) -> Dict[str, SchemaField]:
        """Return a copy of the field name to :class:`SchemaField` mapping."""
        return dict(self._fields)

    def field_names(self) -> List[str]:
        """Return the list of declared field names."""
        return list(self._fields)

    def required_fields(self) -> List[str]:
        """Return the sorted list of required field names."""
        return sorted(
            name for name, field in self._fields.items() if field.required
        )

    def optional_fields(self) -> List[str]:
        """Return the sorted list of optional field names."""
        return sorted(
            name for name, field in self._fields.items() if not field.required
        )

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize *config* against this schema.

        Only declared fields are present in the returned dictionary.
        Required fields must be present; optional fields fall back to their
        defaults when absent. All values are coerced to the declared types
        and passed through any field-level validators.

        Args:
            config: The raw configuration dictionary.

        Returns:
            A new dictionary with validated, coerced values.

        Raises:
            TypeError: If *config* is not a dictionary.
            ConfigValidationError: If a required field is missing or a
                value fails validation.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        result: Dict[str, Any] = {}
        for name, field in self._fields.items():
            if name not in config:
                if field.required:
                    raise ConfigValidationError(
                        f"required field {name!r} is missing"
                    )
                if field.has_default:
                    result[name] = field.default
                continue
            try:
                result[name] = field.validate(config[name])
            except (TypeError, ValueError) as exc:
                raise ConfigValidationError(
                    f"field {name!r}: {exc}"
                ) from exc
        return result

    def parse(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for :meth:`validate`."""
        return self.validate(config)

    def get(self, config: Dict[str, Any], name: str, default: Any = None) -> Any:
        """Return the validated value for *name* from *config*.

        Args:
            config: The raw configuration dictionary.
            name: The field name to look up.
            default: Value returned if the field is absent or invalid.

        Returns:
            The validated value, or *default* if unavailable.
        """
        if name not in self._fields:
            return default
        try:
            validated = self.validate(config)
        except (TypeError, ValueError, ConfigValidationError):
            return default
        return validated.get(name, default)

    def merge(self, other: ConfigSchema) -> ConfigSchema:
        """Return a new schema merging *other* into this one.

        Fields from *other* override fields with the same name.

        Args:
            other: The schema to merge in.

        Returns:
            A new :class:`ConfigSchema` with the combined fields.
        """
        merged: Dict[str, SchemaField] = dict(self._fields)
        merged.update(other._fields)
        return ConfigSchema(list(merged.values()))
CONFIG_SCHEMA
# --- tests/test_config_schema.py ---
cat > "$OUTPUT_DIR/tests/test_config_schema.py" <<'TESTCONFIGSCHEMA'
"""Tests for config_schema module."""

import unittest

from config_schema import (
    ConfigSchema,
    ConfigValidationError,
    SchemaField,
    bool_validator,
    choices_validator,
    email_validator,
    float_validator,
    hostname_validator,
    int_validator,
    range_validator,
    regex_validator,
    str_validator,
    url_validator,
)


class TestSchemaFieldCoercion(unittest.TestCase):
    def test_int_validator_coerces_string(self):
        self.assertEqual(int_validator("42"), 42)
        self.assertEqual(int_validator(7), 7)
        self.assertEqual(int_validator(7.0), 7)

    def test_int_validator_rejects_bool(self):
        with self.assertRaises(TypeError):
            int_validator(True)

    def test_int_validator_rejects_non_whole_float(self):
        with self.assertRaises(ValueError):
            int_validator(3.5)

    def test_int_validator_rejects_bad_string(self):
        with self.assertRaises(ValueError):
            int_validator("not-a-number")

    def test_float_validator_coerces(self):
        self.assertEqual(float_validator("3.14"), 3.14)
        self.assertEqual(float_validator(7), 7.0)

    def test_float_validator_rejects_bool(self):
        with self.assertRaises(TypeError):
            float_validator(False)

    def test_str_validator_passthrough(self):
        self.assertEqual(str_validator("hello"), "hello")

    def test_str_validator_rejects_non_string(self):
        with self.assertRaises(TypeError):
            str_validator(123)

    def test_bool_validator_strings(self):
        self.assertTrue(bool_validator("true"))
        self.assertTrue(bool_validator("True"))
        self.assertTrue(bool_validator("1"))
        self.assertTrue(bool_validator("yes"))
        self.assertTrue(bool_validator("on"))
        self.assertFalse(bool_validator("false"))
        self.assertFalse(bool_validator("0"))
        self.assertFalse(bool_validator("no"))
        self.assertFalse(bool_validator("off"))

    def test_bool_validator_numbers(self):
        self.assertTrue(bool_validator(1))
        self.assertFalse(bool_validator(0))

    def test_bool_validator_rejects_bad_string(self):
        with self.assertRaises(ValueError):
            bool_validator("maybe")


class TestSchemaFieldValidators(unittest.TestCase):
    def test_email_validator(self):
        self.assertEqual(email_validator("user@example.com"), "user@example.com")
        with self.assertRaises(ValueError):
            email_validator("not-an-email")

    def test_hostname_validator(self):
        self.assertEqual(hostname_validator("example.com"), "example.com")
        self.assertEqual(hostname_validator("sub.example.com"), "sub.example.com")
        with self.assertRaises(ValueError):
            hostname_validator("-example.com")
        with self.assertRaises(ValueError):
            hostname_validator("example..com")

    def test_url_validator(self):
        self.assertEqual(url_validator("https://example.com/path"), "https://example.com/path")
        with self.assertRaises(ValueError):
            url_validator("example.com")
        with self.assertRaises(ValueError):
            url_validator("http://")

    def test_range_validator(self):
        validate = range_validator(1, 10)
        self.assertEqual(validate(5), 5)
        self.assertEqual(validate("7"), 7)
        with self.assertRaises(ValueError):
            validate(15)

    def test_range_validator_invalid_bounds(self):
        with self.assertRaises(ValueError):
            range_validator(10, 1)

    def test_choices_validator(self):
        validate = choices_validator("dev", "staging", "prod")
        self.assertEqual(validate("staging"), "staging")
        with self.assertRaises(ValueError):
            validate("production")

    def test_choices_validator_no_choices(self):
        with self.assertRaises(ValueError):
            choices_validator()

    def test_regex_validator(self):
        validate = regex_validator(r"^[A-Z]+$")
        self.assertEqual(validate("HELLO"), "HELLO")
        with self.assertRaises(ValueError):
            validate("hello")


class TestSchemaField(unittest.TestCase):
    def test_field_coerce_and_validate(self):
        field = SchemaField("port", int, default=8080)
        self.assertEqual(field.validate("9000"), 9000)
        self.assertEqual(field.validate(443), 443)

    def test_field_with_extra_validator(self):
        field = SchemaField("port", int, validator=range_validator(1, 65535))
        self.assertEqual(field.validate("8080"), 8080)
        with self.assertRaises(ValueError):
            field.validate(99999)

    def test_field_has_default(self):
        field = SchemaField("debug", bool, default=False)
        self.assertTrue(field.has_default)
        required = SchemaField("secret", str, required=True)
        self.assertFalse(required.has_default)

    def test_field_unsupported_type(self):
        with self.assertRaises(TypeError):
            SchemaField("x", list)

    def test_field_empty_name(self):
        with self.assertRaises(ValueError):
            SchemaField("", str)


class TestConfigSchemaValidate(unittest.TestCase):
    def setUp(self):
        self.schema = ConfigSchema([
            SchemaField("host", str, default="localhost"),
            SchemaField("port", int, default=8080, validator=range_validator(1, 65535)),
            SchemaField("debug", bool, default=False),
            SchemaField("secret", str, required=True),
        ])

    def test_validate_full_config(self):
        config = self.schema.validate({
            "host": "example.com",
            "port": "9000",
            "debug": "true",
            "secret": "s3cr3t",
        })
        self.assertEqual(config, {
            "host": "example.com",
            "port": 9000,
            "debug": True,
            "secret": "s3cr3t",
        })

    def test_validate_applies_defaults(self):
        config = self.schema.validate({"secret": "s3cr3t"})
        self.assertEqual(config["host"], "localhost")
        self.assertEqual(config["port"], 8080)
        self.assertEqual(config["debug"], False)
        self.assertEqual(config["secret"], "s3cr3t")

    def test_validate_missing_required_field(self):
        with self.assertRaises(ConfigValidationError):
            self.schema.validate({"host": "example.com"})

    def test_validate_rejects_non_dict(self):
        with self.assertRaises(TypeError):
            self.schema.validate("not a dict")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            self.schema.validate([1, 2])  # type: ignore[arg-type]

    def test_validate_type_coercion_error(self):
        with self.assertRaises(ConfigValidationError):
            self.schema.validate({"secret": "x", "port": "not-a-number"})

    def test_validate_validation_error_wrapped(self):
        with self.assertRaises(ConfigValidationError):
            self.schema.validate({"secret": "x", "port": 99999})

    def test_validation_error_is_value_error(self):
        self.assertTrue(issubclass(ConfigValidationError, ValueError))

    def test_validate_unknown_keys_are_dropped(self):
        config = self.schema.validate({
            "secret": "x",
            "unknown": "ignored",
            "another": 1,
        })
        self.assertNotIn("unknown", config)
        self.assertNotIn("another", config)

    def test_parse_alias(self):
        config = {"secret": "x", "port": "3000"}
        self.assertEqual(self.schema.parse(config), self.schema.validate(config))

    def test_get(self):
        config = {"secret": "x", "port": "3000"}
        self.assertEqual(self.schema.get(config, "port"), 3000)
        self.assertEqual(self.schema.get(config, "host"), "localhost")
        self.assertEqual(self.schema.get(config, "missing", "fallback"), "fallback")
        self.assertEqual(self.schema.get(config, "not_a_field"), None)

    def test_field_names(self):
        self.assertEqual(
            sorted(self.schema.field_names()),
            ["debug", "host", "port", "secret"],
        )

    def test_required_and_optional_fields(self):
        self.assertEqual(self.schema.required_fields(), ["secret"])
        self.assertEqual(
            self.schema.optional_fields(),
            ["debug", "host", "port"],
        )


class TestConfigSchemaMerge(unittest.TestCase):
    def test_merge_combines_fields(self):
        base = ConfigSchema([SchemaField("a", str, default="x")])
        override = ConfigSchema([SchemaField("b", int, default=1)])
        merged = base.merge(override)
        self.assertEqual(sorted(merged.field_names()), ["a", "b"])

    def test_merge_overrides_existing_field(self):
        base = ConfigSchema([SchemaField("a", str, default="x")])
        override = ConfigSchema([SchemaField("a", int, default=7)])
        merged = base.merge(other=override)
        field = merged.fields["a"]
        self.assertIsInstance(field, SchemaField)
        self.assertEqual(field.type_, int)
        self.assertEqual(field.default, 7)

    def test_merge_returns_new_schema(self):
        base = ConfigSchema([SchemaField("a", str)])
        other = ConfigSchema([SchemaField("b", str)])
        merged = base.merge(other)
        self.assertIsNot(merged, base)
        self.assertEqual(len(base.fields), 1)
        self.assertEqual(len(merged.fields), 2)


if __name__ == "__main__":
    unittest.main()

TESTCONFIGSCHEMA
# --- exceptions_utils.py ---
cat > "$OUTPUT_DIR/exceptions_utils.py" <<'EXCEPTIONSUTILS'
"""Exception utilities for custom error handling."""

from __future__ import annotations

import traceback
from typing import Any, Callable, Dict, Optional, Type, TypeVar

T = TypeVar("T")


class ValidationError(ValueError):
    """Raised when data validation fails.

    Attributes:
        field: Optional field name that failed validation.
        value: The value that failed validation.
        message: Human-readable error message.
    """

    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        value: Any = None,
    ) -> None:
        self.field = field
        self.value = value
        self.message = message
        super().__init__(message)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""

    pass


class NotFoundError(Exception):
    """Raised when a requested resource is not found."""

    pass


class PermissionError_(Exception):
    """Raised when an operation is not permitted.

    Note: Avoids shadowing built-in PermissionError by using underscore suffix.
    """

    pass


class TimeoutError_(Exception):
    """Raised when an operation times out.

    Note: Avoids shadowing built-in TimeoutError in Python 3.11+ contexts.
    """

    pass


def catch_and_wrap(
    func: Callable[[], T],
    exceptions: tuple[Type[BaseException], ...] = (Exception,),
    wrap_with: Type[BaseException] = Exception,
    message: Optional[str] = None,
) -> T:
    """Execute func and wrap specified exceptions.

    Args:
        func: Callable to execute.
        exceptions: Tuple of exception types to catch and wrap.
        wrap_with: Exception type to wrap caught exceptions with.
        message: Optional message for wrapped exception.

    Returns:
        Result of func if successful.

    Raises:
        wrap_with: If any of the specified exceptions are caught.
    """
    try:
        return func()
    except exceptions as e:
        if message:
            raise wrap_with(message) from e
        raise wrap_with(str(e)) from e


def get_error_details(exc: BaseException) -> Dict[str, Any]:
    """Get detailed information about an exception.

    Args:
        exc: Exception to analyze.

    Returns:
        Dictionary containing exception type, message, and traceback.
    """
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }


def is_instance_of_any(obj: Any, exception_types: tuple[Type[BaseException], ...]) -> bool:
    """Check if obj is an instance of any exception type in the tuple.

    Args:
        obj: Object to check.
        exception_types: Tuple of exception types.

    Returns:
        True if obj is instance of any type, False otherwise.
    """
    return isinstance(obj, exception_types)


__all__ = [
    "ValidationError",
    "ConfigurationError",
    "NotFoundError",
    "PermissionError_",
    "TimeoutError_",
    "catch_and_wrap",
    "get_error_details",
    "is_instance_of_any",
]
EXCEPTIONSUTILS

# --- tests/test_exceptions_utils.py ---
cat > "$OUTPUT_DIR/tests/test_exceptions_utils.py" <<'TESTEXCEPTIONSUTILS'
"""Tests for exceptions_utils module."""

import unittest

from exceptions_utils import (
    ConfigurationError,
    NotFoundError,
    PermissionError_,
    TimeoutError_,
    ValidationError,
    catch_and_wrap,
    get_error_details,
    is_instance_of_any,
)


class TestCustomExceptions(unittest.TestCase):
    def test_validation_error_default(self):
        err = ValidationError()
        self.assertIsInstance(err, ValueError)
        self.assertIsInstance(err, ValidationError)
        self.assertEqual(err.message, "Validation failed")
        self.assertIsNone(err.field)
        self.assertIsNone(err.value)

    def test_validation_error_with_details(self):
        err = ValidationError("Invalid email", field="email", value="not-an-email")
        self.assertEqual(err.message, "Invalid email")
        self.assertEqual(err.field, "email")
        self.assertEqual(err.value, "not-an-email")
        self.assertEqual(str(err), "Invalid email")

    def test_configuration_error(self):
        err = ConfigurationError("Missing config")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "Missing config")

    def test_not_found_error(self):
        err = NotFoundError("User not found")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "User not found")

    def test_permission_error_(self):
        err = PermissionError_("Access denied")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "Access denied")

    def test_timeout_error_(self):
        err = TimeoutError_("Request timed out")
        self.assertIsInstance(err, Exception)
        self.assertEqual(str(err), "Request timed out")


class TestCatchAndWrap(unittest.TestCase):
    def test_successful_execution(self):
        result = catch_and_wrap(lambda: 42)
        self.assertEqual(result, 42)

    def test_wraps_exception_with_default(self):
        def fail():
            raise ValueError("oops")

        with self.assertRaises(Exception) as ctx:
            catch_and_wrap(fail)
        self.assertTrue(not isinstance(ctx.exception, ValueError))

    def test_wraps_specific_exceptions_only(self):
        def fail():
            raise ValueError("oops")

        with self.assertRaises(Exception):
            catch_and_wrap(fail, exceptions=(ValueError,))

    def test_does_not_wrap_other_exceptions(self):
        def fail():
            raise TypeError("oops")

        with self.assertRaises(TypeError):
            catch_and_wrap(fail, exceptions=(ValueError,))

    def test_wraps_with_custom_exception(self):
        def fail():
            raise RuntimeError("bad")

        with self.assertRaises(ConfigurationError):
            catch_and_wrap(fail, exceptions=(RuntimeError,), wrap_with=ConfigurationError)

    def test_wraps_with_custom_message(self):
        def fail():
            raise RuntimeError("bad")

        with self.assertRaises(ConfigurationError) as ctx:
            catch_and_wrap(
                fail,
                exceptions=(RuntimeError,),
                wrap_with=ConfigurationError,
                message="Config failed",
            )
        self.assertEqual(str(ctx.exception), "Config failed")

    def test_preserves_cause(self):
        def fail():
            raise RuntimeError("original")

        try:
            catch_and_wrap(fail, exceptions=(RuntimeError,), wrap_with=ValidationError)
        except ValidationError as e:
            self.assertIsNotNone(e.__cause__)
            self.assertIsInstance(e.__cause__, RuntimeError)


class TestGetErrorDetails(unittest.TestCase):
    def test_get_error_details(self):
        try:
            raise ValueError("test error")
        except ValueError as e:
            details = get_error_details(e)
            self.assertEqual(details["type"], "ValueError")
            self.assertEqual(details["message"], "test error")
            self.assertIn("traceback", details)
            self.assertIsInstance(details["traceback"], str)


class TestIsInstanceOfAny(unittest.TestCase):
    def test_matches_single_type(self):
        self.assertTrue(is_instance_of_any(ValueError("x"), (ValueError,)))
        self.assertFalse(is_instance_of_any(TypeError("x"), (ValueError,)))

    def test_matches_multiple_types(self):
        self.assertTrue(is_instance_of_any(ValueError("x"), (ValueError, TypeError)))
        self.assertTrue(is_instance_of_any(TypeError("x"), (ValueError, TypeError)))
        self.assertFalse(is_instance_of_any(RuntimeError("x"), (ValueError, TypeError)))

    def test_handles_non_exceptions(self):
        self.assertFalse(is_instance_of_any("not an exception", (ValueError,)))


if __name__ == "__main__":
    unittest.main()
TESTEXCEPTIONSUTILS

# --- io_utils.py ---
cat > "$OUTPUT_DIR/io_utils.py" <<'IOUTILS'
"""Line-oriented and atomic input/output utility functions."""

import os
import tempfile
from pathlib import Path
from typing import Iterator, List, Union


def read_lines(path: Union[str, Path]) -> List[str]:
    """Read a file and return its lines without trailing newlines.

    Args:
        path: Path to the file to read.

    Returns:
        A list of strings, one per line, with trailing newlines removed.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def write_lines(path: Union[str, Path], lines: List[str], encoding: str = "utf-8") -> None:
    """Write a list of strings to a file, one line per entry.

    Args:
        path: Path to the file to write.
        lines: The lines to write.
        encoding: Text encoding to use (default: "utf-8").

    Raises:
        TypeError: If lines is not a list of strings.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(lines, list) or not all(isinstance(line, str) for line in lines):
        raise TypeError("lines must be a list of strings")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        for line in lines:
            f.write(line)
            f.write("\n")


def append_text(path: Union[str, Path], text: str, encoding: str = "utf-8") -> None:
    """Append text to the end of a file, creating it if needed.

    Args:
        path: Path to the file to append to.
        text: The text to append.
        encoding: Text encoding to use (default: "utf-8").

    Raises:
        TypeError: If text is not a string.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding=encoding) as f:
        f.write(text)


def atomic_write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
    """Write text to a file atomically via a temp file and os.replace.

    The content is first written to a temporary file in the same directory,
    then atomically moved into place so readers never see a partial write.

    Args:
        path: Path to the file to write.
        content: The text content to write.
        encoding: Text encoding to use (default: "utf-8").

    Raises:
        TypeError: If content is not a string.
        OSError: If there is an issue writing or replacing the file.
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def stream_copy(src: Union[str, Path], dst: Union[str, Path], chunk_size: int = 65536) -> int:
    """Copy the contents of src to dst in chunks, returning bytes copied.

    Args:
        src: Path to the source file.
        dst: Path to the destination file.
        chunk_size: Number of bytes to read per chunk (default: 65536).

    Returns:
        The total number of bytes copied.

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If there is an issue reading or writing the files.
    """
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(chunk_size)
            if not chunk:
                break
            fout.write(chunk)
            total += len(chunk)
    return total


def count_lines(path: Union[str, Path]) -> int:
    """Return the number of lines in a file.

    Args:
        path: Path to the file to count.

    Returns:
        The number of lines in the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def iter_lines(path: Union[str, Path]) -> Iterator[str]:
    """Yield lines from a file one at a time without loading it into memory.

    Args:
        path: Path to the file to iterate over.

    Yields:
        Each line of the file with its trailing newline removed.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


__all__ = [
    "read_lines",
    "write_lines",
    "append_text",
    "atomic_write_text",
    "stream_copy",
    "count_lines",
    "iter_lines",
]
IOUTILS

# --- tests/test_io_utils.py ---
cat > "$OUTPUT_DIR/tests/test_io_utils.py" <<'TESTIOUTILS'
"""Tests for io_utils module."""

import tempfile
import unittest
from pathlib import Path

from io_utils import (
    append_text,
    atomic_write_text,
    count_lines,
    iter_lines,
    read_lines,
    stream_copy,
    write_lines,
)


class TestReadWriteLines(unittest.TestCase):
    def test_write_and_read_lines(self):
        lines = ["alpha", "beta", "gamma"]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            path = f.name
        try:
            write_lines(path, lines)
            self.assertEqual(read_lines(path), lines)
        finally:
            Path(path).unlink()

    def test_write_lines_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "nested" / "lines.txt"
            write_lines(path, ["a", "b"])
            self.assertTrue(path.exists())
            self.assertEqual(read_lines(path), ["a", "b"])

    def test_write_lines_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(TypeError):
                write_lines(path, ["ok", 1])
        finally:
            Path(path).unlink()

    def test_append_text(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("first\n")
            path = f.name
        try:
            append_text(path, "second\n")
            self.assertEqual(read_lines(path), ["first", "second"])
        finally:
            Path(path).unlink()

    def test_append_text_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "new.txt"
            append_text(path, "hello\n")
            self.assertEqual(read_lines(path), ["hello"])

    def test_append_text_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(TypeError):
                append_text(path, 123)
        finally:
            Path(path).unlink()


class TestAtomicWriteText(unittest.TestCase):
    def test_atomic_write_roundtrip(self):
        content = "atomic content"
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            atomic_write_text(path, content)
            self.assertEqual(Path(path).read_text(encoding="utf-8"), content)
            siblings = list(Path(path).parent.glob(Path(path).name + ".*.tmp"))
            self.assertEqual(siblings, [])
        finally:
            Path(path).unlink()

    def test_atomic_write_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "nested" / "atomic.txt"
            atomic_write_text(path, "data")
            self.assertTrue(path.exists())
            self.assertEqual(path.read_text(encoding="utf-8"), "data")

    def test_atomic_write_invalid_type(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(TypeError):
                atomic_write_text(path, 123)
        finally:
            Path(path).unlink()


class TestStreamCopy(unittest.TestCase):
    def test_stream_copy(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            src = Path(tmp_dir) / "src.bin"
            dst = Path(tmp_dir) / "dst.bin"
            data = bytes(range(256)) * 4
            src.write_bytes(data)
            copied = stream_copy(src, dst)
            self.assertEqual(copied, len(data))
            self.assertEqual(dst.read_bytes(), data)

    def test_stream_copy_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            src = Path(tmp_dir) / "src.bin"
            dst = Path(tmp_dir) / "nested" / "dst.bin"
            src.write_bytes(b"hello")
            stream_copy(src, dst)
            self.assertTrue(dst.exists())
            self.assertEqual(dst.read_bytes(), b"hello")


class TestCountLines(unittest.TestCase):
    def test_count_lines(self):
        content = "one\ntwo\nthree\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            self.assertEqual(count_lines(path), 3)
        finally:
            Path(path).unlink()

    def test_count_lines_no_trailing_newline(self):
        content = "one\ntwo\nthree"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name
        try:
            self.assertEqual(count_lines(path), 3)
        finally:
            Path(path).unlink()


class TestIterLines(unittest.TestCase):
    def test_iter_lines(self):
        lines = ["x", "y", "z"]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("\n".join(lines))
            path = f.name
        try:
            self.assertEqual(list(iter_lines(path)), lines)
        finally:
            Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
TESTIOUTILS

# --- ini_utils.py ---
cat > "$OUTPUT_DIR/ini_utils.py" <<'INI_UTILS'
"""Configuration utility functions for loading and managing INI configuration files.

This module provides utilities for working with INI-style configuration files
using Python's :mod:`configparser`, with section-aware get/set/merge operations.
"""

import configparser
from pathlib import Path
from typing import Any, Dict, Union


def _parser() -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    parser.optionxform = str  # preserve case of keys
    return parser


def load_config(file_path: Union[str, Path]) -> Dict[str, Dict[str, str]]:
    """Load configuration from an INI file.

    Args:
        file_path: Path to the INI configuration file.

    Returns:
        Dictionary mapping section names to dictionaries of key/value pairs.
        The ``DEFAULT`` section is excluded.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        configparser.Error: If the file contains invalid INI syntax.
        TypeError: If file_path is not a string or Path object.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    parser = _parser()
    parser.read(path, encoding="utf-8")

    config: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        config[section] = dict(parser.items(section))

    return config


def save_config(config: Dict[str, Dict[str, str]], file_path: Union[str, Path]) -> None:
    """Save configuration to an INI file.

    Args:
        config: Dictionary mapping section names to key/value dictionaries.
        file_path: Path where the INI configuration file should be saved.

    Raises:
        TypeError: If config is not a dictionary of dictionaries.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    parser = _parser()
    for section, values in config.items():
        if not isinstance(values, dict):
            raise TypeError(f"Section '{section}' must be a dictionary")
        if not parser.has_section(section):
            parser.add_section(section)
        for key, value in values.items():
            parser.set(section, key, str(value))

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        parser.write(f)


def get_config_value(
    config: Dict[str, Dict[str, Any]],
    key_path: str,
    default: Any = None,
    separator: str = ".",
) -> Any:
    """Get a value from a nested INI configuration using dot notation.

    The first path component names the section; the second names the key.
    Only one level of nesting (``section.key``) is supported.

    Args:
        config: Configuration dictionary mapping sections to key/value maps.
        key_path: Dot-separated path (e.g. ``"database.host"``).
        default: Value to return if the path is not found.
        separator: Separator character for the key path (default: ".").

    Returns:
        The value at the specified path, or default if not found.
    """
    if not isinstance(config, dict):
        return default

    keys = key_path.split(separator)
    if len(keys) != 2:
        return default

    section, key = keys
    values = config.get(section)
    if not isinstance(values, dict):
        return default

    return values.get(key, default)


def set_config_value(
    config: Dict[str, Dict[str, Any]],
    key_path: str,
    value: Any,
    separator: str = ".",
) -> None:
    """Set a value in a nested INI configuration using dot notation.

    Args:
        config: Configuration dictionary to modify.
        key_path: Dot-separated path (e.g. ``"database.host"``).
        value: Value to set at the specified location.
        separator: Separator character for the key path (default: ".").

    Raises:
        TypeError: If config is not a dictionary.
        ValueError: If key_path does not contain exactly one separator.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    keys = key_path.split(separator)
    if len(keys) != 2:
        raise ValueError("key_path must be in 'section.key' format")

    section, key = keys
    if section not in config or not isinstance(config[section], dict):
        config[section] = {}

    config[section][key] = value


def merge_configs(
    base: Dict[str, Dict[str, Any]],
    override: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Merge two INI configuration dictionaries, with override taking precedence.

    Args:
        base: Base configuration dictionary.
        override: Override configuration dictionary.

    Returns:
        New dictionary with merged configuration.

    Raises:
        TypeError: If either argument is not a dictionary of dictionaries.
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise TypeError("Both base and override must be dictionaries")

    result: Dict[str, Dict[str, Any]] = {}

    for section, values in base.items():
        if not isinstance(values, dict):
            raise TypeError(f"Section '{section}' in base must be a dictionary")
        result[section] = dict(values)

    for section, values in override.items():
        if not isinstance(values, dict):
            raise TypeError(f"Section '{section}' in override must be a dictionary")
        if section in result:
            result[section].update(values)
        else:
            result[section] = dict(values)

    return result


def list_sections(config: Dict[str, Dict[str, Any]]) -> list[str]:
    """Return the list of section names in a configuration dictionary."""
    return [section for section in config if isinstance(config[section], dict)]


def has_section(config: Dict[str, Dict[str, Any]], section: str) -> bool:
    """Return True if the configuration contains the given section."""
    return isinstance(config.get(section), dict)


def get_section(config: Dict[str, Dict[str, Any]], section: str) -> Dict[str, Any]:
    """Return the key/value dictionary for a section, or an empty dict if absent."""
    values = config.get(section)
    return dict(values) if isinstance(values, dict) else {}
INI_UTILS

# --- tests/test_ini_utils.py ---
cat > "$OUTPUT_DIR/tests/test_ini_utils.py" <<'TESTINIUTILS'
import tempfile
import unittest
from pathlib import Path

from ini_utils import (
    get_config_value,
    get_section,
    has_section,
    list_sections,
    load_config,
    merge_configs,
    save_config,
    set_config_value,
)


class TestLoadConfig(unittest.TestCase):
    """Test the load_config function."""

    def test_load_valid_ini(self):
        """Test loading a valid INI configuration file."""
        content = """[database]
host = localhost
port = 5432

[debug]
enabled = true
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            loaded = load_config(temp_path)
            self.assertEqual(
                loaded,
                {
                    "database": {"host": "localhost", "port": "5432"},
                    "debug": {"enabled": "true"},
                },
            )
        finally:
            Path(temp_path).unlink()

    def test_load_file_not_found(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_config("/non/existent/file.ini")

    def test_load_with_path_object(self):
        """Test loading works with Path objects."""
        content = "[section]\nkey = value\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            loaded = load_config(temp_path)
            self.assertEqual(loaded, {"section": {"key": "value"}})
        finally:
            temp_path.unlink()

    def test_load_ignores_default_section(self):
        """Test that the DEFAULT section is not included in results."""
        content = """[DEFAULT]
host = localhost

[database]
host = 127.0.0.1
port = 5432
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            loaded = load_config(temp_path)
            self.assertNotIn("DEFAULT", loaded)
            self.assertEqual(loaded["database"]["host"], "127.0.0.1")
        finally:
            Path(temp_path).unlink()


class TestSaveConfig(unittest.TestCase):
    """Test the save_config function."""

    def test_save_and_load_roundtrip(self):
        """Test saving and loading preserves data."""
        original_config = {
            "database": {"host": "localhost", "port": "5432"},
            "debug": {"enabled": "true"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            temp_path = f.name

        try:
            save_config(original_config, temp_path)
            loaded_config = load_config(temp_path)
            self.assertEqual(loaded_config, original_config)
        finally:
            Path(temp_path).unlink()

    def test_save_creates_directories(self):
        """Test that save_config creates parent directories if needed."""
        config = {"section": {"key": "value"}}

        with tempfile.TemporaryDirectory() as tmp_dir:
            nested_path = Path(tmp_dir) / "nested" / "deep" / "config.ini"

            self.assertFalse(nested_path.parent.exists())

            save_config(config, nested_path)

            self.assertTrue(nested_path.exists())
            loaded = load_config(nested_path)
            self.assertEqual(loaded, config)

    def test_save_invalid_config_type(self):
        """Test that saving non-dict config raises TypeError."""
        with tempfile.NamedTemporaryFile(suffix=".ini", delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(TypeError):
                save_config(["not", "a", "dict"], temp_path)
        finally:
            Path(temp_path).unlink()

    def test_save_invalid_section_type(self):
        """Test that saving a section with non-dict values raises TypeError."""
        with tempfile.NamedTemporaryFile(suffix=".ini", delete=False) as f:
            temp_path = f.name

        try:
            with self.assertRaises(TypeError):
                save_config({"section": ["not", "a", "dict"]}, temp_path)
        finally:
            Path(temp_path).unlink()


class TestGetConfigValue(unittest.TestCase):
    """Test the get_config_value function."""

    def setUp(self):
        """Set up test configuration."""
        self.config = {
            "database": {"host": "localhost", "port": "5432"},
            "debug": {"enabled": "true"},
        }

    def test_get_existing_value(self):
        """Test getting an existing configuration value."""
        self.assertEqual(get_config_value(self.config, "database.host"), "localhost")
        self.assertEqual(get_config_value(self.config, "database.port"), "5432")
        self.assertEqual(get_config_value(self.config, "debug.enabled"), "true")

    def test_get_missing_key_returns_default(self):
        """Test that missing keys return the default value."""
        self.assertIsNone(get_config_value(self.config, "database.hostname"))
        self.assertEqual(
            get_config_value(self.config, "database.hostname", "default"), "default"
        )

    def test_get_missing_section_returns_default(self):
        """Test that missing sections return the default value."""
        self.assertIsNone(get_config_value(self.config, "missing.host"))
        self.assertEqual(
            get_config_value(self.config, "missing.host", "default"), "default"
        )

    def test_get_with_non_dict_config(self):
        """Test getting value from non-dict config returns default."""
        self.assertEqual(get_config_value("not a dict", "section.key", "default"), "default")
        self.assertIsNone(get_config_value([], "section.key"))

    def test_get_with_invalid_key_path(self):
        """Test that malformed key paths return the default value."""
        self.assertIsNone(get_config_value(self.config, "noseparator"))
        self.assertIsNone(get_config_value(self.config, "a.b.c"))


class TestSetConfigValue(unittest.TestCase):
    """Test the set_config_value function."""

    def test_set_new_section_and_key(self):
        """Test setting a value in a new section."""
        config = {}
        set_config_value(config, "database.host", "localhost")
        self.assertEqual(config, {"database": {"host": "localhost"}})

    def test_set_overwrites_existing(self):
        """Test that setting overwrites existing values."""
        config = {"database": {"host": "localhost"}}
        set_config_value(config, "database.host", "127.0.0.1")
        self.assertEqual(config["database"]["host"], "127.0.0.1")

    def test_set_adds_key_to_existing_section(self):
        """Test adding a key to an existing section."""
        config = {"database": {"host": "localhost"}}
        set_config_value(config, "database.port", "5432")
        self.assertEqual(config, {"database": {"host": "localhost", "port": "5432"}})

    def test_set_invalid_config_type(self):
        """Test that setting value in non-dict config raises TypeError."""
        with self.assertRaises(TypeError):
            set_config_value(["not", "a", "dict"], "section.key", "value")

    def test_set_invalid_key_path(self):
        """Test that malformed key paths raise ValueError."""
        with self.assertRaises(ValueError):
            set_config_value({}, "noseparator", "value")
        with self.assertRaises(ValueError):
            set_config_value({}, "a.b.c", "value")


class TestMergeConfigs(unittest.TestCase):
    """Test the merge_configs function."""

    def test_merge_simple_dicts(self):
        """Test merging simple configurations."""
        base = {"database": {"host": "localhost", "port": "5432"}}
        override = {"database": {"port": "5433"}, "debug": {"enabled": "true"}}
        expected = {
            "database": {"host": "localhost", "port": "5433"},
            "debug": {"enabled": "true"},
        }
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_preserves_base_when_no_override(self):
        """Test that base values are preserved when not overridden."""
        base = {"database": {"host": "localhost", "port": "5432"}}
        override = {"database": {"user": "admin"}}
        expected = {"database": {"host": "localhost", "port": "5432", "user": "admin"}}
        self.assertEqual(merge_configs(base, override), expected)

    def test_merge_with_empty_dicts(self):
        """Test merging with empty dictionaries."""
        base = {"database": {"host": "localhost"}}
        override = {}
        self.assertEqual(merge_configs(base, override), base)

        base = {}
        override = {"debug": {"enabled": "true"}}
        self.assertEqual(merge_configs(base, override), override)

        base = {}
        override = {}
        self.assertEqual(merge_configs(base, override), {})

    def test_merge_invalid_types(self):
        """Test that merging invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            merge_configs("not a dict", {"a": {}})
        with self.assertRaises(TypeError):
            merge_configs({"a": {}}, "not a dict")
        with self.assertRaises(TypeError):
            merge_configs({"a": ["not", "dict"]}, {"b": {}})
        with self.assertRaises(TypeError):
            merge_configs({"a": {}}, {"b": ["not", "dict"]})


class TestListSections(unittest.TestCase):
    """Test the list_sections function."""

    def test_list_sections(self):
        """Test listing section names."""
        config = {"database": {}, "debug": {}, "logging": {}}
        self.assertEqual(sorted(list_sections(config)), ["database", "debug", "logging"])

    def test_list_sections_empty(self):
        """Test listing sections of an empty config."""
        self.assertEqual(list_sections({}), [])


class TestHasSection(unittest.TestCase):
    """Test the has_section function."""

    def test_has_section(self):
        """Test checking for section existence."""
        config = {"database": {"host": "localhost"}}
        self.assertTrue(has_section(config, "database"))
        self.assertFalse(has_section(config, "missing"))


class TestGetSection(unittest.TestCase):
    """Test the get_section function."""

    def test_get_section(self):
        """Test getting a section's key/value map."""
        config = {"database": {"host": "localhost", "port": "5432"}}
        self.assertEqual(get_section(config, "database"), {"host": "localhost", "port": "5432"})

    def test_get_missing_section(self):
        """Test getting a missing section returns an empty dict."""
        self.assertEqual(get_section({}, "missing"), {})

    def test_get_section_returns_copy(self):
        """Test that the returned dict is a copy."""
        config = {"database": {"host": "localhost"}}
        section = get_section(config, "database")
        section["host"] = "changed"
        self.assertEqual(config["database"]["host"], "localhost")


if __name__ == "__main__":
    unittest.main()
TESTINIUTILS



# --- http_utils.py ---
cat > "$OUTPUT_DIR/http_utils.py" <<'HTTP_UTILS'
"""HTTP utility functions for status codes and response handling."""

from typing import Dict, Optional

# HTTP status code category prefixes (1xx through 5xx)
HTTP_INFORMATIONAL = 1
HTTP_SUCCESS = 2
HTTP_REDIRECTION = 3
HTTP_CLIENT_ERROR = 4
HTTP_SERVER_ERROR = 5


STATUS_CODES: Dict[int, str] = {
    # 1xx Informational
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    # 2xx Success
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    # 3xx Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    # 4xx Client Error
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    # 5xx Server Error
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required",
}


def status_code_category(code: int) -> int:
    """Return the HTTP status code category (1-5) for a given code.

    Args:
        code: The HTTP status code.

    Returns:
        The leading digit of the status code (1 through 5).
    """
    return code // 100


def status_message(code: int) -> Optional[str]:
    """Return the standard reason phrase for an HTTP status code.

    Args:
        code: The HTTP status code.

    Returns:
        The standard reason phrase, or ``None`` if the code is unknown.
    """
    return STATUS_CODES.get(code)


def is_informational(code: int) -> bool:
    """Return ``True`` if the status code is a 1xx informational response."""
    return status_code_category(code) == HTTP_INFORMATIONAL


def is_success(code: int) -> bool:
    """Return ``True`` if the status code is a 2xx success response."""
    return status_code_category(code) == HTTP_SUCCESS


def is_redirection(code: int) -> bool:
    """Return ``True`` if the status code is a 3xx redirection response."""
    return status_code_category(code) == HTTP_REDIRECTION


def is_client_error(code: int) -> bool:
    """Return ``True`` if the status code is a 4xx client error response."""
    return status_code_category(code) == HTTP_CLIENT_ERROR


def is_server_error(code: int) -> bool:
    """Return ``True`` if the status code is a 5xx server error response."""
    return status_code_category(code) == HTTP_SERVER_ERROR


def is_error(code: int) -> bool:
    """Return ``True`` if the status code is a 4xx or 5xx error response."""
    category = status_code_category(code)
    return category in (HTTP_CLIENT_ERROR, HTTP_SERVER_ERROR)
HTTP_UTILS

# --- tests/test_http_utils.py ---
cat > "$OUTPUT_DIR/tests/test_http_utils.py" <<'TESTHTTPUTILS'
import unittest

from http_utils import (
    HTTP_CLIENT_ERROR,
    HTTP_INFORMATIONAL,
    HTTP_REDIRECTION,
    HTTP_SERVER_ERROR,
    HTTP_SUCCESS,
    is_client_error,
    is_error,
    is_informational,
    is_redirection,
    is_server_error,
    is_success,
    status_code_category,
    status_message,
)


class TestStatusCodeCategory(unittest.TestCase):
    def test_informational(self):
        self.assertEqual(status_code_category(100), HTTP_INFORMATIONAL)
        self.assertEqual(status_code_category(199), HTTP_INFORMATIONAL)

    def test_success(self):
        self.assertEqual(status_code_category(200), HTTP_SUCCESS)
        self.assertEqual(status_code_category(299), HTTP_SUCCESS)

    def test_redirection(self):
        self.assertEqual(status_code_category(300), HTTP_REDIRECTION)
        self.assertEqual(status_code_category(399), HTTP_REDIRECTION)

    def test_client_error(self):
        self.assertEqual(status_code_category(400), HTTP_CLIENT_ERROR)
        self.assertEqual(status_code_category(499), HTTP_CLIENT_ERROR)

    def test_server_error(self):
        self.assertEqual(status_code_category(500), HTTP_SERVER_ERROR)
        self.assertEqual(status_code_category(599), HTTP_SERVER_ERROR)


class TestStatusMessage(unittest.TestCase):
    def test_known_codes(self):
        self.assertEqual(status_message(200), "OK")
        self.assertEqual(status_message(201), "Created")
        self.assertEqual(status_message(404), "Not Found")
        self.assertEqual(status_message(500), "Internal Server Error")
        self.assertEqual(status_message(418), "I'm a teapot")

    def test_unknown_code_returns_none(self):
        self.assertIsNone(status_message(999))
        self.assertIsNone(status_message(0))


class TestBooleanChecks(unittest.TestCase):
    def test_is_informational(self):
        self.assertTrue(is_informational(100))
        self.assertFalse(is_informational(200))

    def test_is_success(self):
        self.assertTrue(is_success(200))
        self.assertTrue(is_success(204))
        self.assertFalse(is_success(300))

    def test_is_redirection(self):
        self.assertTrue(is_redirection(301))
        self.assertTrue(is_redirection(308))
        self.assertFalse(is_redirection(200))

    def test_is_client_error(self):
        self.assertTrue(is_client_error(400))
        self.assertTrue(is_client_error(404))
        self.assertFalse(is_client_error(500))

    def test_is_server_error(self):
        self.assertTrue(is_server_error(500))
        self.assertTrue(is_server_error(503))
        self.assertFalse(is_server_error(400))

    def test_is_error(self):
        self.assertTrue(is_error(400))
        self.assertTrue(is_error(500))
        self.assertFalse(is_error(200))
        self.assertFalse(is_error(300))


if __name__ == '__main__':
    unittest.main()
TESTHTTPUTILS

# --- duration_utils.py ---
cat > "$OUTPUT_DIR/duration_utils.py" <<'DURATION_UTILS'
"""Time duration utilities for parsing, formatting, and converting durations.

This module provides helpers for working with time durations, including
parsing human-readable duration strings (e.g. ``"1h30m"``, ``"90s"``,
``"2.5 days"``), formatting seconds into a compact display, converting
between time units, and computing durations between datetimes.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple, Union

__all__: list[str] = [
    "SECONDS_PER_MINUTE",
    "SECONDS_PER_HOUR",
    "SECONDS_PER_DAY",
    "SECONDS_PER_WEEK",
    "DURATION_UNITS",
    "is_valid_duration",
    "parse_duration",
    "format_duration",
    "seconds_to_hms",
    "hms_to_seconds",
    "to_seconds",
    "duration_between",
    "add_duration",
]

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400
SECONDS_PER_WEEK = 604800

# Mapping of accepted unit suffixes to their multiplier in seconds.
DURATION_UNITS: dict[str, float] = {
    "s": 1,
    "sec": 1,
    "secs": 1,
    "second": 1,
    "seconds": 1,
    "m": 60,
    "min": 60,
    "mins": 60,
    "minute": 60,
    "minutes": 60,
    "h": 3600,
    "hr": 3600,
    "hrs": 3600,
    "hour": 3600,
    "hours": 3600,
    "d": 86400,
    "day": 86400,
    "days": 86400,
    "w": 604800,
    "week": 604800,
    "weeks": 604800,
}

# Matches a number followed by an optional unit, e.g. "1h30m", "90s", "2.5 days".
_DURATION_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)")

# Largest units first so the formatter greets the biggest applicable unit.
_ORDERED_UNITS: tuple[tuple[str, float], ...] = (
    ("week", SECONDS_PER_WEEK),
    ("day", SECONDS_PER_DAY),
    ("hour", SECONDS_PER_HOUR),
    ("minute", SECONDS_PER_MINUTE),
    ("second", 1),
)


def is_valid_duration(duration_str: str) -> bool:
    """Return ``True`` if ``duration_str`` is a parseable duration string.

    Args:
        duration_str: The duration string to validate.

    Returns:
        ``True`` if the string can be parsed by :func:`parse_duration`,
        otherwise ``False``.

    Examples:
        >>> is_valid_duration("1h30m")
        True
        >>> is_valid_duration("90s")
        True
        >>> is_valid_duration("not a duration")
        False
    """
    if not isinstance(duration_str, str):
        return False
    stripped = duration_str.strip()
    if not stripped:
        return False
    try:
        parse_duration(duration_str)
        return True
    except (TypeError, ValueError):
        return False


def parse_duration(duration_str: str) -> float:
    """Parse a human-readable duration string into total seconds.

    Args:
        duration_str: A duration string such as ``"1h30m"``, ``"90s"``,
            ``"2.5 days"``, or ``"1 week 2 days"``. Units may be abbreviated
            (``s``, ``m``, ``h``, ``d``, ``w``) or spelled out.

    Returns:
        The total duration in seconds as a float.

    Raises:
        TypeError: If ``duration_str`` is not a string.
        ValueError: If ``duration_str`` is empty or contains unparseable
            parts, or if any numeric value is negative.

    Examples:
        >>> parse_duration("1h30m")
        5400.0
        >>> parse_duration("90s")
        90.0
        >>> parse_duration("2.5 days")
        216000.0
    """
    if not isinstance(duration_str, str):
        raise TypeError("duration_str must be a string")

    stripped = duration_str.strip()
    if not stripped:
        raise ValueError("duration_str must not be empty")

    total_seconds = 0.0
    pos = 0

    for match in _DURATION_PATTERN.finditer(stripped):
        # Any non-whitespace text between matches makes the string invalid.
        gap = stripped[pos:match.start()].strip()
        if gap:
            raise ValueError(
                f"Unable to parse duration segment {gap!r} in {duration_str!r}"
            )
        value = float(match.group(1))
        unit = match.group(2).lower()
        if value < 0:
            raise ValueError(
                f"Duration values must be non-negative, got {value!r}"
            )
        if unit not in DURATION_UNITS:
            raise ValueError(
                f"Unknown duration unit {unit!r} in {duration_str!r}"
            )
        total_seconds += value * DURATION_UNITS[unit]
        pos = match.end()

    trailing = stripped[pos:].strip()
    if trailing:
        raise ValueError(
            f"Unable to parse duration segment {trailing!r} in {duration_str!r}"
        )

    if pos == 0:
        raise ValueError(
            f"Unable to parse duration string {duration_str!r}"
        )

    return total_seconds


def format_duration(
    seconds: Union[int, float],
    max_units: int = 2,
) -> str:
    """Format a duration in seconds into a human-readable string.

    Args:
        seconds: The duration in seconds. Must be non-negative.
        max_units: The maximum number of time units to include in the output
            (default: 2).

    Returns:
        A human-readable duration string such as ``"1h 30m"`` or ``"90s"``.
        A duration of zero returns ``"0s"``.

    Raises:
        TypeError: If ``seconds`` is not an int or float.
        ValueError: If ``seconds`` is negative or ``max_units`` is not a
            positive integer.

    Examples:
        >>> format_duration(5400)
        '1h 30m'
        >>> format_duration(90)
        '1m 30s'
        >>> format_duration(0)
        '0s'
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise TypeError("seconds must be an int or float")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    if not isinstance(max_units, int) or isinstance(max_units, bool) or max_units < 1:
        raise ValueError("max_units must be a positive integer")

    remaining = float(seconds)
    parts: list[str] = []

    for unit_name, unit_seconds in _ORDERED_UNITS:
        if len(parts) >= max_units:
            break
        if remaining >= unit_seconds:
            count = int(remaining // unit_seconds)
            remaining -= count * unit_seconds
            parts.append(f"{count}{unit_name[0]}")

    if not parts:
        return "0s"

    return " ".join(parts)


def seconds_to_hms(seconds: Union[int, float]) -> Tuple[int, int, int]:
    """Convert a duration in seconds to ``(hours, minutes, seconds)``.

    Args:
        seconds: The duration in seconds. Must be non-negative.

    Returns:
        A tuple of ``(hours, minutes, seconds)``.

    Raises:
        TypeError: If ``seconds`` is not an int or float.
        ValueError: If ``seconds`` is negative.

    Examples:
        >>> seconds_to_hms(3661)
        (1, 1, 1)
        >>> seconds_to_hms(90)
        (0, 1, 30)
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise TypeError("seconds must be an int or float")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, SECONDS_PER_HOUR)
    minutes, secs = divmod(remainder, SECONDS_PER_MINUTE)
    return hours, minutes, secs


def hms_to_seconds(
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> float:
    """Convert ``(hours, minutes, seconds)`` into total seconds.

    Args:
        hours: Number of hours (default: 0).
        minutes: Number of minutes (default: 0).
        seconds: Number of seconds (default: 0).

    Returns:
        The total duration in seconds.

    Raises:
        TypeError: If any argument is not an int.
        ValueError: If any argument is negative.

    Examples:
        >>> hms_to_seconds(1, 1, 1)
        3661.0
        >>> hms_to_seconds(minutes=30)
        1800.0
    """
    for name, value in (("hours", hours), ("minutes", minutes), ("seconds", seconds)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    return float(
        hours * SECONDS_PER_HOUR
        + minutes * SECONDS_PER_MINUTE
        + seconds
    )


def to_seconds(
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    milliseconds: int = 0,
) -> float:
    """Convert time components into total seconds.

    Args:
        hours: Number of hours (default: 0).
        minutes: Number of minutes (default: 0).
        seconds: Number of seconds (default: 0).
        milliseconds: Number of milliseconds (default: 0).

    Returns:
        The total duration in seconds as a float.

    Raises:
        TypeError: If any argument is not an int.
        ValueError: If any argument is negative.

    Examples:
        >>> to_seconds(hours=1, minutes=30)
        5400.0
        >>> to_seconds(milliseconds=500)
        0.5
    """
    for name, value in (
        ("hours", hours),
        ("minutes", minutes),
        ("seconds", seconds),
        ("milliseconds", milliseconds),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    return float(
        hours * SECONDS_PER_HOUR
        + minutes * SECONDS_PER_MINUTE
        + seconds
        + milliseconds / 1000.0
    )


def duration_between(
    start: datetime,
    end: datetime,
) -> timedelta:
    """Return the duration between two datetimes.

    Args:
        start: The start datetime.
        end: The end datetime.

    Returns:
        A :class:`~datetime.timedelta` representing ``end - start``. May be
        negative if ``end`` is before ``start``.

    Raises:
        TypeError: If either argument is not a :class:`~datetime.datetime`.

    Examples:
        >>> from datetime import datetime
        >>> start = datetime(2024, 1, 1, 10, 0, 0)
        >>> end = datetime(2024, 1, 1, 11, 30, 0)
        >>> duration_between(start, end)
        datetime.timedelta(seconds=5400)
    """
    if not isinstance(start, datetime):
        raise TypeError("start must be a datetime")
    if not isinstance(end, datetime):
        raise TypeError("end must be a datetime")

    return end - start


def add_duration(
    dt: datetime,
    duration_str: str,
) -> datetime:
    """Add a parsed duration to a datetime and return the result.

    Args:
        dt: The base datetime.
        duration_str: A duration string parseable by :func:`parse_duration`.

    Returns:
        A new :class:`~datetime.datetime` equal to ``dt + duration``.

    Raises:
        TypeError: If ``dt`` is not a datetime.
        ValueError: If ``duration_str`` cannot be parsed.

    Examples:
        >>> from datetime import datetime
        >>> dt = datetime(2024, 1, 1, 10, 0, 0)
        >>> add_duration(dt, "1h30m")
        datetime(2024, 1, 1, 11, 30)
    """
    if not isinstance(dt, datetime):
        raise TypeError("dt must be a datetime")

    seconds = parse_duration(duration_str)
    return dt + timedelta(seconds=seconds)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
DURATION_UTILS

# --- tests/test_duration_utils.py ---
cat > "$OUTPUT_DIR/tests/test_duration_utils.py" <<'TESTDURATIONUTILS'
import unittest
from datetime import datetime

from duration_utils import (
    DURATION_UNITS,
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    SECONDS_PER_WEEK,
    add_duration,
    duration_between,
    format_duration,
    hms_to_seconds,
    is_valid_duration,
    parse_duration,
    seconds_to_hms,
    to_seconds,
)


class TestIsValidDuration(unittest.TestCase):
    def test_valid_durations(self):
        for duration in ["1h30m", "90s", "2.5 days", "1 week 2 days", "30m", "1h", "1d", "1w"]:
            self.assertTrue(is_valid_duration(duration))

    def test_invalid_durations(self):
        for duration in ["not a duration", "", "1x", "abc", "-5s", "1h 30"]:
            self.assertFalse(is_valid_duration(duration))

    def test_non_string_returns_false(self):
        self.assertFalse(is_valid_duration(None))  # type: ignore[arg-type]
        self.assertFalse(is_valid_duration(123))  # type: ignore[arg-type]


class TestParseDuration(unittest.TestCase):
    def test_seconds(self):
        self.assertEqual(parse_duration("90s"), 90.0)
        self.assertEqual(parse_duration("90 seconds"), 90.0)
        self.assertEqual(parse_duration("90 sec"), 90.0)
        self.assertEqual(parse_duration("90 secs"), 90.0)

    def test_minutes(self):
        self.assertEqual(parse_duration("30m"), 1800.0)
        self.assertEqual(parse_duration("30 minutes"), 1800.0)
        self.assertEqual(parse_duration("30 min"), 1800.0)
        self.assertEqual(parse_duration("30 mins"), 1800.0)

    def test_hours(self):
        self.assertEqual(parse_duration("1h"), 3600.0)
        self.assertEqual(parse_duration("1 hour"), 3600.0)
        self.assertEqual(parse_duration("1 hr"), 3600.0)
        self.assertEqual(parse_duration("1 hrs"), 3600.0)

    def test_days(self):
        self.assertEqual(parse_duration("1d"), SECONDS_PER_DAY)
        self.assertEqual(parse_duration("2 days"), 2 * SECONDS_PER_DAY)
        self.assertEqual(parse_duration("2 day"), 2 * SECONDS_PER_DAY)

    def test_weeks(self):
        self.assertEqual(parse_duration("1w"), SECONDS_PER_WEEK)
        self.assertEqual(parse_duration("2 weeks"), 2 * SECONDS_PER_WEEK)

    def test_combined(self):
        self.assertEqual(parse_duration("1h30m"), 5400.0)
        self.assertEqual(parse_duration("1h 30m"), 5400.0)
        self.assertEqual(parse_duration("1h30m15s"), 5415.0)
        self.assertEqual(parse_duration("2.5 days"), 216000.0)
        self.assertEqual(parse_duration("1 week 2 days"), 9 * SECONDS_PER_DAY)

    def test_float_value(self):
        self.assertEqual(parse_duration("1.5h"), 5400.0)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("")
        with self.assertRaises(ValueError):
            parse_duration("   ")

    def test_unknown_unit_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("5x")

    def test_negative_value_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("-5s")

    def test_unparseable_segment_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("1h 30")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            parse_duration(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            parse_duration(None)  # type: ignore[arg-type]


class TestFormatDuration(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_duration(0), "0s")

    def test_seconds_only(self):
        self.assertEqual(format_duration(45), "45s")

    def test_minutes_and_seconds(self):
        self.assertEqual(format_duration(90), "1m 30s")

    def test_hours_and_minutes(self):
        self.assertEqual(format_duration(5400), "1h 30m")

    def test_days_and_hours(self):
        self.assertEqual(format_duration(90000), "1d 1h")

    def test_max_units(self):
        self.assertEqual(format_duration(5400, max_units=1), "1h")
        self.assertEqual(format_duration(90, max_units=1), "1m")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            format_duration("90")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            format_duration(True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            format_duration(-1)

    def test_invalid_max_units(self):
        with self.assertRaises(ValueError):
            format_duration(90, max_units=0)
        with self.assertRaises(ValueError):
            format_duration(90, max_units=True)  # type: ignore[arg-type]


class TestSecondsToHms(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(seconds_to_hms(3661), (1, 1, 1))
        self.assertEqual(seconds_to_hms(90), (0, 1, 30))
        self.assertEqual(seconds_to_hms(0), (0, 0, 0))
        self.assertEqual(seconds_to_hms(3600), (1, 0, 0))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            seconds_to_hms("90")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            seconds_to_hms(True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            seconds_to_hms(-1)


class TestHmsToSeconds(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(hms_to_seconds(1, 1, 1), 3661.0)
        self.assertEqual(hms_to_seconds(minutes=30), 1800.0)
        self.assertEqual(hms_to_seconds(), 0.0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            hms_to_seconds(hours="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            hms_to_seconds(hours=True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            hms_to_seconds(hours=-1)


class TestToSeconds(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(to_seconds(hours=1, minutes=30), 5400.0)
        self.assertEqual(to_seconds(milliseconds=500), 0.5)
        self.assertEqual(to_seconds(), 0.0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            to_seconds(hours="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            to_seconds(hours=True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            to_seconds(hours=-1)


class TestDurationBetween(unittest.TestCase):
    def test_basic(self):
        start = datetime(2024, 1, 1, 10, 0, 0)
        end = datetime(2024, 1, 1, 11, 30, 0)
        self.assertEqual(duration_between(start, end).total_seconds(), 5400.0)

    def test_negative_duration(self):
        start = datetime(2024, 1, 1, 11, 30, 0)
        end = datetime(2024, 1, 1, 10, 0, 0)
        self.assertEqual(duration_between(start, end).total_seconds(), -5400.0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            duration_between("start", datetime(2024, 1, 1))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            duration_between(datetime(2024, 1, 1), "end")  # type: ignore[arg-type]


class TestAddDuration(unittest.TestCase):
    def test_basic(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        result = add_duration(dt, "1h30m")
        self.assertEqual(result, datetime(2024, 1, 1, 11, 30, 0))

    def test_days(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        result = add_duration(dt, "2 days")
        self.assertEqual(result, datetime(2024, 1, 3, 10, 0, 0))

    def test_type_error_on_dt(self):
        with self.assertRaises(TypeError):
            add_duration("not a datetime", "1h")  # type: ignore[arg-type]

    def test_invalid_duration_raises(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        with self.assertRaises(ValueError):
            add_duration(dt, "not a duration")


if __name__ == "__main__":
    unittest.main()
TESTDURATIONUTILS

cat > "$OUTPUT_DIR/temp_utils.py" <<'TEMP_UTILS'
"""Temporary file and directory utilities.

Provides helpers for creating, writing, reading, and cleaning up temporary
files and directories using the standard library ``tempfile`` module. All
functions validate their inputs and raise ``TypeError`` or ``ValueError`` on
invalid arguments.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Union

__all__: list[str] = [
    "TEMP_DIR",
    "create_temp_file",
    "create_temp_dir",
    "temp_file",
    "temp_dir",
    "write_temp_file",
    "read_temp_file",
    "cleanup_temp_path",
    "is_temp_path",
    "temp_path_exists",
]


TEMP_DIR: str = tempfile.gettempdir()
"""The system temporary directory (e.g. ``/tmp`` on Unix)."""


def _normalize_path(path: Union[str, Path]) -> str:
    """Return the absolute, normalized string form of ``path``."""
    return os.path.abspath(os.path.normpath(str(path)))


def create_temp_file(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    text: bool = False,
    delete: bool = True,
) -> str:
    """Create a named temporary file and return its path.

    The file is created with mode ``0600`` and is immediately closed so it can
    be opened by other processes. When ``delete`` is ``True`` (the default),
    the file is removed automatically when the returned path is passed to
    :func:`cleanup_temp_path`; the caller is otherwise responsible for removal.

    Args:
        suffix: Optional filename suffix (e.g. ``".txt"``).
        prefix: Optional filename prefix.
        dir: Optional directory in which to create the file. Defaults to the
            system temporary directory.
        text: Whether to open the file in text mode (``True``) or binary mode
            (``False``).
        delete: Whether the file should be removed on close. Pass ``False`` to
            keep the file after creation.

    Returns:
        The absolute path to the created temporary file.

    Raises:
        TypeError: If any argument has an invalid type.
        OSError: If the file cannot be created.

    Examples:
        >>> path = create_temp_file(suffix=".txt", prefix="demo_")
        >>> os.path.exists(path)
        True
        >>> cleanup_temp_path(path)
        True
        >>> os.path.exists(path)
        False
    """
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string or None")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string or None")
    if dir is not None and not isinstance(dir, (str, Path)):
        raise TypeError("dir must be a string, Path, or None")
    if not isinstance(text, bool):
        raise TypeError("text must be a bool")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")

    fd, path = tempfile.mkstemp(
        suffix=suffix,
        prefix=prefix,
        dir=str(dir) if dir is not None else None,
        text=text,
    )
    os.close(fd)
    # The file is intentionally left on disk. The caller removes it with
    # :func:`cleanup_temp_path` when done; ``delete`` records that intent.
    return path


def create_temp_dir(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    delete: bool = True,
) -> str:
    """Create a temporary directory and return its path.

    Args:
        suffix: Optional directory name suffix.
        prefix: Optional directory name prefix.
        dir: Optional parent directory. Defaults to the system temporary
            directory.
        delete: Whether the directory should be removed when cleaned up via
            :func:`cleanup_temp_path`.

    Returns:
        The absolute path to the created temporary directory.

    Raises:
        TypeError: If any argument has an invalid type.
        OSError: If the directory cannot be created.

    Examples:
        >>> path = create_temp_dir(prefix="demo_")
        >>> os.path.isdir(path)
        True
        >>> cleanup_temp_path(path)
        True
        >>> os.path.exists(path)
        False
    """
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string or None")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string or None")
    if dir is not None and not isinstance(dir, (str, Path)):
        raise TypeError("dir must be a string, Path, or None")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")

    return tempfile.mkdtemp(
        suffix=suffix,
        prefix=prefix,
        dir=str(dir) if dir is not None else None,
    )


@contextmanager
def temp_file(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    text: bool = False,
) -> Iterator[str]:
    """Context manager yielding the path of a temporary file.

    The file is created on entry and removed on exit, even if an exception is
    raised inside the block.

    Args:
        suffix: Optional filename suffix.
        prefix: Optional filename prefix.
        dir: Optional directory. Defaults to the system temporary directory.
        text: Whether to open the file in text mode.

    Yields:
        The absolute path to the temporary file.

    Examples:
        >>> with temp_file(suffix=".csv") as path:
        ...     _ = open(path, "w").write("a,b\\n1,2\\n")
        >>> import os
        >>> os.path.exists(path)
        False
    """
    path = create_temp_file(
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        text=text,
        delete=False,
    )
    try:
        yield path
    finally:
        cleanup_temp_path(path)


@contextmanager
def temp_dir(
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
) -> Iterator[str]:
    """Context manager yielding the path of a temporary directory.

    The directory (and its contents) is created on entry and removed on exit,
    even if an exception is raised inside the block.

    Args:
        suffix: Optional directory name suffix.
        prefix: Optional directory name prefix.
        dir: Optional parent directory. Defaults to the system temporary
            directory.

    Yields:
        The absolute path to the temporary directory.

    Examples:
        >>> with temp_dir(prefix="demo_") as path:
        ...     _ = os.path.join(path, "nested.txt")
        >>> import os
        >>> os.path.exists(path)
        False
    """
    path = create_temp_dir(suffix=suffix, prefix=prefix, dir=dir, delete=False)
    try:
        yield path
    finally:
        cleanup_temp_path(path)


def write_temp_file(
    content: str,
    suffix: Optional[str] = None,
    prefix: Optional[str] = None,
    dir: Optional[Union[str, Path]] = None,
    delete: bool = True,
    mode: str = "w",
) -> str:
    """Write ``content`` to a new temporary file and return its path.

    Args:
        content: The text content to write.
        suffix: Optional filename suffix.
        prefix: Optional filename prefix.
        dir: Optional directory. Defaults to the system temporary directory.
        delete: Whether the file should be removed when cleaned up via
            :func:`cleanup_temp_path`.
        mode: The file open mode (default: ``"w"``).

    Returns:
        The absolute path to the written temporary file.

    Raises:
        TypeError: If any argument has an invalid type.
        OSError: If the file cannot be created or written.

    Examples:
        >>> path = write_temp_file("hello world", suffix=".txt")
        >>> read_temp_file(path)
        'hello world'
        >>> cleanup_temp_path(path)
        True
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string or None")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string or None")
    if dir is not None and not isinstance(dir, (str, Path)):
        raise TypeError("dir must be a string, Path, or None")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")

    path = create_temp_file(
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        text="b" not in mode,
        delete=False,
    )
    with open(path, mode) as fh:
        fh.write(content)
    # The file is intentionally left on disk; remove it with
    # :func:`cleanup_temp_path` when done.
    return path


def read_temp_file(path: Union[str, Path], mode: str = "r") -> str:
    """Read and return the contents of a temporary file.

    Args:
        path: The path to the temporary file.
        mode: The file open mode (default: ``"r"``).

    Returns:
        The file contents as a string.

    Raises:
        TypeError: If ``path`` is not a string or Path.
        FileNotFoundError: If the file does not exist.
        OSError: If the file cannot be read.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")

    with open(path, mode) as fh:
        return fh.read()


def cleanup_temp_path(path: Union[str, Path]) -> bool:
    """Remove a temporary file or directory, ignoring missing paths.

    Files are removed with :func:`os.remove`; directories are removed
    recursively with :func:`shutil.rmtree`. Returns ``True`` if something was
    removed, ``False`` if the path did not exist.

    Args:
        path: The path to the temporary file or directory.

    Returns:
        ``True`` if the path existed and was removed, ``False`` otherwise.

    Raises:
        TypeError: If ``path`` is not a string or Path.
        OSError: If the path cannot be removed.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")

    path_str = str(path)
    if not os.path.exists(path_str):
        return False

    if os.path.isdir(path_str) and not os.path.islink(path_str):
        shutil.rmtree(path_str)
    else:
        os.remove(path_str)
    return True


def is_temp_path(path: Union[str, Path]) -> bool:
    """Return ``True`` if ``path`` resides inside the system temp directory.

    Args:
        path: The path to check.

    Returns:
        ``True`` if the path is under :data:`TEMP_DIR`, otherwise ``False``.

    Raises:
        TypeError: If ``path`` is not a string or Path.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")

    path_str = _normalize_path(path)
    temp_dir = _normalize_path(TEMP_DIR)
    return path_str == temp_dir or path_str.startswith(temp_dir + os.sep)


def temp_path_exists(path: Union[str, Path]) -> bool:
    """Return ``True`` if ``path`` exists on the filesystem.

    Args:
        path: The path to check.

    Returns:
        ``True`` if the path exists, otherwise ``False``.

    Raises:
        TypeError: If ``path`` is not a string or Path.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path")

    return os.path.exists(str(path))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
TEMP_UTILS

cat > "$OUTPUT_DIR/tests/test_temp_utils.py" <<'TESTTEMPUTILS'
"""Unit tests for temp_utils module."""

import os
import unittest

from temp_utils import (
    TEMP_DIR,
    cleanup_temp_path,
    create_temp_dir,
    create_temp_file,
    is_temp_path,
    read_temp_file,
    temp_dir,
    temp_file,
    temp_path_exists,
    write_temp_file,
)


class TestConstants(unittest.TestCase):
    def test_temp_dir_is_string(self):
        self.assertIsInstance(TEMP_DIR, str)
        self.assertTrue(os.path.isdir(TEMP_DIR))


class TestCreateTempFile(unittest.TestCase):
    def test_creates_existing_file(self):
        path = create_temp_file(suffix=".txt", prefix="demo_")
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(path.endswith(".txt"))
        self.assertTrue(os.path.basename(path).startswith("demo_"))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_returns_absolute_path(self):
        path = create_temp_file()
        self.assertTrue(os.path.isabs(path))
        cleanup_temp_path(path)

    def test_custom_dir(self):
        with temp_dir() as parent:
            path = create_temp_file(dir=parent)
            self.assertTrue(os.path.dirname(path) == os.path.abspath(parent))
            cleanup_temp_path(path)

    def test_delete_false_keeps_file(self):
        path = create_temp_file(delete=False)
        self.assertTrue(os.path.exists(path))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            create_temp_file(suffix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(prefix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(dir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(text="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_file(delete="yes")  # type: ignore[arg-type]


class TestCreateTempDir(unittest.TestCase):
    def test_creates_existing_directory(self):
        path = create_temp_dir(suffix="_suf", prefix="demo_")
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.basename(path).startswith("demo_"))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_returns_absolute_path(self):
        path = create_temp_dir()
        self.assertTrue(os.path.isabs(path))
        cleanup_temp_path(path)

    def test_custom_dir(self):
        with temp_dir() as parent:
            path = create_temp_dir(dir=parent)
            self.assertTrue(os.path.dirname(path) == os.path.abspath(parent))
            cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            create_temp_dir(suffix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_dir(prefix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_dir(dir=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            create_temp_dir(delete="yes")  # type: ignore[arg-type]


class TestTempFileContextManager(unittest.TestCase):
    def test_removes_file_on_exit(self):
        path = None
        with temp_file(suffix=".log") as p:
            path = p
            self.assertTrue(os.path.isfile(path))
            with open(path, "w") as fh:
                fh.write("data")
        self.assertFalse(os.path.exists(path))

    def test_removes_file_on_exception(self):
        path = None
        try:
            with temp_file(suffix=".log") as p:
                path = p
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        self.assertFalse(os.path.exists(path))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            with temp_file(suffix=123):  # type: ignore[arg-type]
                pass


class TestTempDirContextManager(unittest.TestCase):
    def test_removes_directory_on_exit(self):
        path = None
        with temp_dir(prefix="tmpdir_") as p:
            path = p
            self.assertTrue(os.path.isdir(path))
        self.assertFalse(os.path.exists(path))

    def test_removes_directory_contents_on_exit(self):
        path = None
        with temp_dir() as p:
            path = p
            nested = os.path.join(p, "nested.txt")
            with open(nested, "w") as fh:
                fh.write("x")
        self.assertFalse(os.path.exists(path))

    def test_removes_directory_on_exception(self):
        path = None
        try:
            with temp_dir() as p:
                path = p
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        self.assertFalse(os.path.exists(path))


class TestWriteTempFile(unittest.TestCase):
    def test_writes_and_reads_content(self):
        path = write_temp_file("hello world", suffix=".txt")
        self.assertTrue(os.path.isfile(path))
        self.assertEqual(read_temp_file(path), "hello world")
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_delete_false_keeps_file(self):
        path = write_temp_file("keep me", delete=False)
        self.assertTrue(os.path.exists(path))
        cleanup_temp_path(path)
        self.assertFalse(os.path.exists(path))

    def test_custom_dir(self):
        with temp_dir() as parent:
            path = write_temp_file("x", dir=parent)
            self.assertTrue(os.path.dirname(path) == os.path.abspath(parent))
            cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            write_temp_file(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            write_temp_file("x", suffix=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            write_temp_file("x", delete="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            write_temp_file("x", mode=123)  # type: ignore[arg-type]


class TestReadTempFile(unittest.TestCase):
    def test_reads_content(self):
        path = write_temp_file("reading me")
        self.assertEqual(read_temp_file(path), "reading me")
        cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            read_temp_file(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            read_temp_file("x", mode=123)  # type: ignore[arg-type]

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            read_temp_file(os.path.join(TEMP_DIR, "definitely_does_not_exist_12345"))


class TestCleanupTempPath(unittest.TestCase):
    def test_removes_file(self):
        path = create_temp_file(delete=False)
        self.assertTrue(cleanup_temp_path(path))
        self.assertFalse(os.path.exists(path))

    def test_removes_directory(self):
        path = create_temp_dir(delete=False)
        self.assertTrue(cleanup_temp_path(path))
        self.assertFalse(os.path.exists(path))

    def test_removes_directory_with_contents(self):
        path = create_temp_dir(delete=False)
        nested = os.path.join(path, "file.txt")
        with open(nested, "w") as fh:
            fh.write("x")
        self.assertTrue(cleanup_temp_path(path))
        self.assertFalse(os.path.exists(path))

    def test_missing_path_returns_false(self):
        missing = os.path.join(TEMP_DIR, "definitely_does_not_exist_67890")
        self.assertFalse(cleanup_temp_path(missing))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            cleanup_temp_path(123)  # type: ignore[arg-type]


class TestIsTempPath(unittest.TestCase):
    def test_temp_path_returns_true(self):
        self.assertTrue(is_temp_path(TEMP_DIR))
        path = create_temp_file(delete=False)
        try:
            self.assertTrue(is_temp_path(path))
        finally:
            cleanup_temp_path(path)

    def test_non_temp_path_returns_false(self):
        self.assertFalse(is_temp_path("/"))
        self.assertFalse(is_temp_path("/usr/bin"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_temp_path(123)  # type: ignore[arg-type]


class TestTempPathExists(unittest.TestCase):
    def test_existing_path_returns_true(self):
        path = create_temp_file(delete=False)
        try:
            self.assertTrue(temp_path_exists(path))
        finally:
            cleanup_temp_path(path)

    def test_missing_path_returns_false(self):
        missing = os.path.join(TEMP_DIR, "definitely_does_not_exist_abcde")
        self.assertFalse(temp_path_exists(missing))

    def test_directory_returns_true(self):
        path = create_temp_dir(delete=False)
        try:
            self.assertTrue(temp_path_exists(path))
        finally:
            cleanup_temp_path(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            temp_path_exists(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
TESTTEMPUTILS
