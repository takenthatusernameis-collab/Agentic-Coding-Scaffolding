---
name: scaffolding-helper
description: Helper skill for scaffolding tasks - provides utilities for generating boilerplate code and project structures
---

# Scaffolding Helper Skill

This skill provides specialized instructions and workflows for scaffolding tasks.

## When to Use

- Creating new modules or files following project conventions
- Generating boilerplate code for common patterns
- Setting up new project structures
- Adding tests for new modules

## Workflows

### Creating a New Utility Module

1. Check existing modules for naming conventions
2. Create the module file with proper `__all__` exports
3. Add comprehensive docstrings
4. Create corresponding test file in tests/
5. Run `make test` to verify

### Creating a New Test File

1. Follow pytest conventions
2. Use descriptive test function names
3. Test both success and error cases
4. Mock external dependencies when appropriate

### Updating Project Configuration

1. Update pyproject.toml for new modules
2. Run `make refresh-scaffold` to sync scaffold.sh
3. Run `make lint` and `make typecheck` to verify

## Best Practices

- Follow existing file patterns in the repository
- Use descriptive file and function names
- Keep changes focused and incremental
- Write clean, well-documented code
- Every public function/class must be in `__all__`
- Run tests after making changes