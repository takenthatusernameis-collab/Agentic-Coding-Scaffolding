# Makefile for Agentic Coding Scaffolding
# Common developer commands for project management

.PHONY: test lint typecheck run scaffold refresh-scaffold clean help pre-commit-install pre-commit-run verify doctest

## Run the Python test suite using pytest (falling back to unittest if pytest is unavailable)
test:
	@echo "Running tests..."
	@if [ -z "$$(git status --porcelain -- . ':!.kilo/last_verified.checkpoint' 2>/dev/null)" ]; then \
		python -c "import sys; sys.path.insert(0,'tools'); import verify_state_delta as v; m=v.read_marker(); h=v.head(); \
		sys.exit(0 if m and m.get('head')==h else 1 if m and not v.source_changed_since(m['head']) else 2)" >/dev/null 2>&1; \
		rc=$$?; \
		if [ $$rc -eq 0 ]; then \
			echo "Working tree clean and already verified at current checkpoint; skipping smoke test."; \
		elif [ $$rc -eq 1 ]; then \
			echo "Working tree clean; no source-relevant file changed since the last verified checkpoint; skipping smoke test."; \
		else \
			echo "Working tree clean; running public API smoke test and doctests (full suite skipped)."; \
			python -m unittest tests.test_public_api tests.test_doctests; \
		fi; \
	else \
		echo "Working tree dirty; selecting targeted tests for changed source..."; \
		SELECTION=$$(python tools/select_tests.py --from-git --include-untracked); \
		case "$$SELECTION" in \
			FULL_SUITE) \
				echo "Full-suite trigger detected; running full test suite."; \
				if command -v pytest >/dev/null 2>&1; then \
					pytest tests/ -v; \
				else \
					python -m unittest discover tests/ -v; \
				fi; \
				;; \
			*) \
				if [ -n "$$SELECTION" ]; then \
					echo "Running targeted tests: $$SELECTION"; \
					python -m unittest $$SELECTION; \
				else \
					echo "No targeted tests selected; running smoke tests."; \
					python -m unittest tests.test_public_api tests.test_doctests; \
				fi; \
				;; \
		esac; \
	fi

## Run the doctest suite that enforces every module's documented examples
doctest:
	@echo "Running doctests..."
	@python -m unittest tests.test_doctests

## Run ruff to check code style and formatting
lint:
	@echo "Running linting..."
	@if python -m ruff --version >/dev/null 2>&1; then \
		python -m ruff check .; \
	else \
		echo "ruff not installed. Install with: pip install ruff"; \
		exit 1; \
	fi

## Run mypy for static type checking
typecheck:
	@echo "Running type checking..."
	@if python -m mypy --version >/dev/null 2>&1; then \
		python -m mypy . --exclude build --exclude dist; \
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

## Refresh the file copies embedded in scaffold.sh from the repository sources
refresh-scaffold:
	@echo "Refreshing the copies embedded in scaffold.sh..."
	@python tools/refresh_scaffold.py

## Run the bounded state-delta verification pass (foundation checks)
verify:
	@echo "Running state-delta verification..."
	@python tools/verify_state_delta.py

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
	@echo "  doctest   Run the doctest suite that enforces documented examples"
	@echo "  lint      Run ruff code style checker"
	@echo "  typecheck  Run mypy static type checking"
	@echo "  run       Run hello.py (usage: make run [NAME=YourName])"
	@echo "  scaffold  Scaffold a new project using scaffold.sh"
	@echo "  refresh-scaffold  Refresh the copies embedded in scaffold.sh from the repository sources"
	@echo "  verify           Run the bounded state-delta verification pass (foundation checks)"
	@echo "  clean            Remove build artifacts"
	@echo "  help       Show this help message"
	@echo "  pre-commit-install  Install pre-commit hooks into .git/hooks"
	@echo "  pre-commit-run     Run all pre-commit hooks against tracked files"