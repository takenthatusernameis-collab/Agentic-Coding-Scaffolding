---
description: Scaffold a new project structure for agentic coding
---

Generate scaffolding files for a new agentic coding project. This command creates:

- `.github/workflows/main.yml` — CI workflow for the Kilo agent loop
- `AGENTS.md` — AI agent instructions with task handover protocol
- `README.md` — project overview and getting-started guide
- `kilo.json` — Kilo project configuration
- `.kilo/agent/scaffolder.md` — subagent definition for scaffolding tasks
- `.gitignore` — common ignore patterns

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
