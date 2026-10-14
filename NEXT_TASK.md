# Task for Next Agent

Add a Makefile to the project with common developer commands.

Requirements:

1. Create a Makefile with the following targets:

   - `test`: Run the Python test suite using pytest (falling back to unittest if pytest is unavailable)
   - `lint`: Run ruff to check code style and formatting
   - `run`: Run hello.py with an optional name argument (e.g., `make run` or `make run NAME=Alice`)
   - `scaffold`: Invoke scaffold.sh to scaffold a new project
   - `clean`: Remove __pycache__, .pytest_cache, and other build artifacts
   - `help`: Print usage information for all available targets

2. Include a `.PHONY` declaration for all non-file targets.
3. Ensure the Makefile is documented with comments explaining each target.
4. Verify the Makefile works by running `make help`, `make test`, and `make run NAME=Alice`.