## backoff_utils

- Add `backoff_utils.py` wrapping backoff utilities with `constant_backoff` and `exponential_backoff` helpers, input validation, and typed signatures, plus unit tests in `tests/test_backoff_utils.py`.
- Synchronized `backoff_utils.py` and `tests/test_backoff_utils.py` across `scaffold.sh`, `pyproject.toml`, README, `.kilo/command/scaffold-project.md`, `tests/test_scaffold.py`, and this CHANGELOG.

## Unreleased

- Hardened the `strings` module with `reverse_words` and synchronized `strings.py`, its tests, and scaffold documentation (README and embedded `scaffold.sh`) so generated projects and docs reflect the expanded string utilities API.
