---
description: Scaffold a new project structure for agentic coding
---

Generate scaffolding files for a new agentic coding project. This command creates:

- `.github/workflows/main.yml` — CI workflow for the Kilo agent loop
- `AGENTS.md` — AI agent instructions with task handover protocol
- `README.md` — project overview and getting-started guide
- `kilo.json` — Kilo project configuration, including the `scaffolder` subagent
- `.kilo/agent/scaffolder.md` — subagent definition for scaffolding tasks
- `.kilo/command/handover.md` — handover command for task handoffs
- `.kilo/command/scaffold-project.md` — scaffold-project command documentation
- `.kilo/skill/scaffolding-helper.md` — sample skill definition
- `.gitignore` — common ignore patterns
- `Makefile` — common developer targets (test, lint, run, clean, help)
- `pyproject.toml` — Python project configuration and dependencies
- `hello.py` — sample application entry point
- `tests/test_hello.py` — unit tests for the sample application

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
