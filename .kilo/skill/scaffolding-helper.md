# Scaffolding Helper Skill

## Description
A sample skill that provides helper functions and patterns for scaffolding tasks. This skill demonstrates how to create custom skills for the Kilo agent system.

## Capabilities
This skill provides guidance on:
- Creating new utility modules following project conventions
- Generating test files with proper structure
- Updating pyproject.toml with new module entries
- Running quality checks (lint, typecheck, tests)
- Refreshing scaffold.sh embeddings

## Usage
Load this skill when working on scaffolding tasks:
```
/skill scaffolding-helper
```

## Patterns

### Creating a New Utility Module
1. Create `<name>_utils.py` in the project root
2. Define `__all__` with public exports
3. Add comprehensive docstrings with examples
4. Follow existing code style (ruff, mypy compliant)

### Creating a Test File
1. Create `tests/test_<name>_utils.py`
2. Import the module under test
3. Write test classes following `Test<FunctionName>` pattern
4. Include edge cases and error conditions

### Updating pyproject.toml
Add the new module to `[tool.setuptools].py-modules` list in alphabetical order.

### Quality Checks
Run after creating/modifying files:
```bash
make lint        # Check code style
make typecheck   # Static type checking
make test        # Run tests (delta-aware)
make refresh-scaffold  # Update scaffold.sh embeddings
```

## Example Module Template
```python
"""Module docstring describing purpose and key functions."""

from __future__ import annotations

__all__ = [
    "public_function",
    "PublicClass",
]


def public_function(arg: str) -> str:
    """Public function with docstring and type hints."""
    return arg.upper()


class PublicClass:
    """Public class with docstring."""

    def method(self) -> str:
        """Public method."""
        return "result"
```

## Example Test Template
```python
"""Tests for <name>_utils module."""

import unittest
from <name>_utils import public_function, PublicClass


class TestPublicFunction(unittest.TestCase):
    """Tests for public_function."""

    def test_basic(self) -> None:
        self.assertEqual(public_function("hello"), "HELLO")


class TestPublicClass(unittest.TestCase):
    """Tests for PublicClass."""

    def test_method(self) -> None:
        obj = PublicClass()
        self.assertEqual(obj.method(), "result")


if __name__ == "__main__":
    unittest.main()
```