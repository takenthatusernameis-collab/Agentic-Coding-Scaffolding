# Makefile for Agentic Coding Scaffolding
# Common developer commands for project management

.PHONY: test lint typecheck run scaffold clean help pre-commit-install pre-commit-run

## Run the Python test suite using pytest (falling back to unittest if pytest is unavailable)
test:
	@echo "Running tests..."
	@if command -v pytest >/dev/null 2>&1; then \
		pytest tests/ -v; \
	else \
		python -m unittest discover tests/ -v; \
	fi

## Run ruff to check code style and formatting
lint:
	@echo "Running linting..."
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check .; \
	else \
		echo "ruff not installed. Install with: pip install ruff"; \
		exit 1; \
	fi

## Run mypy for static type checking
typecheck:
	@echo "Running type checking..."
	@if command -v mypy >/dev/null 2>&1; then \
		mypy . --exclude build --exclude dist; \
	else \
		echo "mypy not installed. Install with: pip install mypy"; \
		exit 1; \
	fi

## Run hello.py with an optional name argument (e.g., make run or make run NAME=Alice)
run:
	@echo "Running hello.py..."
	@python hello.py $(NAME)

## Invoke scaffold.sh to scaffold a new project
scaffold:
	@echo "Running scaffold.sh..."
	@./scaffold.sh

## Install pre-commit hooks into .git/hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	@if command -v pre-commit >/dev/null 2>&1; then \
		pre-commit install; \
	else \
		echo "pre-commit not installed. Install with: pip install pre-commit"; \
		exit 1; \
	fi

## Run all pre-commit hooks against staged and tracked files
pre-commit-run:
	@echo "Running pre-commit hooks..."
	@if command -v pre-commit >/dev/null 2>&1; then \
		pre-commit run --all-files; \
	else \
		echo "pre-commit not installed. Install with: pip install pre-commit"; \
		exit 1; \
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