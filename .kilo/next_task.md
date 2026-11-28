# Task for Next Agent

Session (2026-11-28, HEAD): Bootstrap session — project foundation verified.

State at start: clean tree. All tests (12335 passed), lint (ruff), and typecheck (mypy) pass. Repository has 300+ utility modules with comprehensive test coverage. Scaffold embeddings verified in sync via `python tools/refresh_scaffold.py --check`.

This session's work (bootstrap verification):
- Verified all tests, lint, and typecheck pass
- Confirmed scaffold.sh embeddings are in sync
- Project foundation is established and healthy

**Next task (delay-bottleneck elimination pass per AGENTS.md § Portfolio):**
1. Run `board_read` for context; if empty, proceed with optimize-delays pass.
2. Execute the structured delay-removal pass per `.kilo/command/optimize-delays.md`:
   - Establish state delta (git status, recent commits, `.kilo/last_verified.checkpoint`, test status)
   - Classify the primary wait type (avoidable process delay, external constraint, integrity gate, or unknown)
   - Improve the execution prompt with evidence
   - Remove ONE high-leverage delay (small durable change: state-delta guard, event-driven wakeup, bounded timeout, task sharding, deduplicated handover, caching, or focused diagnostic)
   - Verify and preserve guarantees (smallest relevant verification first, full gate at milestone)
   - Post a specific next task only if a real next step exists
3. Do NOT modify `.github/workflows/**` (maintainer-managed).
4. Preserve all guarantees: correctness, reproducibility, security, research integrity, verification quality.
5. If you edit any wrapper module or its test, run `make refresh-scaffold` to sync scaffold.sh embeddings.

Acceptance: Measurable reduction in idle time/lead time with unchanged or stronger guarantees. No timestamp-only commits, duplicate tasks, or empty cycles.