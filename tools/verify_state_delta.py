#!/usr/bin/env python3
"""Verify repository state, skipping redundant re-runs via a state-delta guard.

Every activation previously re-ran the full verification battery
(``refresh_scaffold --check``, ``scan_untested``, ``tests.test_public_api``,
``tests.test_scaffold_sync``, ``tests.test_doctests``)
against unchanged state and then manufactured a duplicate handover entry just to
satisfy the CI checkpoint gate. That is a repeated no-op verification cycle
(AVOIDABLE_PROCESS_DELAY).

This tool records the HEAD at which verification last passed in
``.kilo/last_verified.checkpoint``. When the working tree is clean and no
source-relevant file has changed since that checkpoint, the battery is skipped.
When ``tests/`` changed since the last recorded full-suite run, a note is emitted
so test-authoring regressions are not hidden by the clean-tree fast path.
When state has changed, the battery runs and the checkpoint is advanced.

Usage:
    python tools/verify_state_delta.py [--full] [--record-full-suite]

With ``--full`` the battery always runs and the checkpoint is always advanced.
With ``--record-full-suite`` the checkpoint records that a full ``unittest discover``
run accompanied this verification (use after ``make test-full`` or a full-suite run).
"""

from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = ROOT / ".kilo" / "last_verified.checkpoint"

#: Paths whose changes invalidate the verified checkpoint. ``tools/*.py`` is
#: included so an edit to the verification tooling itself forces a fresh battery
#: run instead of trusting a checkpoint produced by the old code. The documents
#: that name the project are included because ``refresh_scaffold.py`` embeds
#: them as templates and ``tests.test_scaffold_sync`` asserts they stay in sync.
SOURCE_GLOBS = (
    "*.py",
    "Makefile",
    "pyproject.toml",
    "scaffold.sh",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    ".kilo/command/scaffold-project.md",
    "tools/*.py",
)


def run(cmd: list[str], timeout: float = 30.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd, cwd=ROOT, text=True, capture_output=True, check=False, timeout=timeout
    )


def working_tree_clean() -> bool:
    """Return ``True`` when ``git status --porcelain`` reports no changes.

    The marker this guard writes is its own output, not a source change, so it
    is excluded: after the guard advances the checkpoint the tree is dirty only
    because of the marker, and a subsequent invocation must still skip the
    battery instead of re-verifying the same HEAD.
    """
    result = run(
        ["git", "status", "--porcelain", "--", ".", ":!.kilo/last_verified.checkpoint"],
        timeout=5.0,
    )
    assert isinstance(result.stdout, str)
    return result.stdout.strip() == ""


def head() -> str:
    result = run(["git", "rev-parse", "HEAD"], timeout=5.0)
    assert isinstance(result.stdout, str)
    return result.stdout.strip()


def read_marker() -> dict | None:
    if not MARKER.is_file():
        return None
    try:
        data = json.loads(MARKER.read_text())
        assert isinstance(data, dict)
        return data
    except (ValueError, OSError):
        return None


def write_marker(data: dict) -> None:
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(json.dumps(data, indent=2) + "\n")


def diff_since(ref: str) -> list[str]:
    """Return changed source-relevant files between *ref* and the working tree.

    Untracked source files are included: the battery must treat a brand new
    module the same as an edited one. A missing or unknown *ref* (for example
    after a rebase, a force-push, or a shallow clone) makes ``git diff`` fail;
    that is reported as a change so the battery runs instead of silently
    trusting a checkpoint that cannot be compared against the current history.
    """
    result = run(
        ["git", "diff", "--name-only", ref, "--"] + list(SOURCE_GLOBS), timeout=5.0
    )
    if result.returncode != 0:
        print(
            f"[verify-state-delta] Cannot diff against {ref!r}; treating state as changed.",
            file=sys.stderr,
        )
        return ["<unknown>"]
    return [line for line in result.stdout.splitlines() if line.strip()]


def untracked_source_files() -> list[str]:
    """Return untracked source-relevant files (including repository-root paths)."""
    result = run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--"]
        + list(SOURCE_GLOBS),
        timeout=5.0,
    )
    if result.returncode != 0:
        return []
    return [line[3:].strip() for line in result.stdout.splitlines() if line.startswith("?? ")]


def source_changed_since(ref: str) -> bool:
    """Return True when any source-relevant file changed between *ref* and now."""
    return bool(diff_since(ref)) or bool(untracked_source_files())


def tests_changed_since(ref: str) -> bool:
    """Return True when any file under tests/ changed since *ref*."""
    result = run(["git", "diff", "--name-only", ref, "--", "tests"], timeout=5.0)
    if result.returncode != 0:
        return True
    if [line for line in result.stdout.splitlines() if line.strip()]:
        return True
    result = run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "tests"],
        timeout=5.0,
    )
    if result.returncode != 0:
        return True
    return bool([line for line in result.stdout.splitlines() if line.startswith("?? ")])



def battery_ok() -> bool:
    """Run the verification battery; return True when every check passes."""
    checks = [
        (["python", "tools/refresh_scaffold.py", "--check"], "refresh_scaffold --check", 10.0),
        (["python", "tools/scan_untested.py"], "scan_untested", 10.0),
        (
            ["python", "-m", "unittest", "tests.test_public_api"],
            "tests.test_public_api",
            15.0,
        ),
        (
            ["python", "-m", "unittest", "tests.test_scaffold_sync"],
            "tests.test_scaffold_sync",
            15.0,
        ),
        (
            ["python", "-m", "unittest", "tests.test_doctests"],
            "tests.test_doctests",
            30.0,
        ),
    ]
    ok = True
    with ThreadPoolExecutor(max_workers=len(checks)) as executor:
        future_to_label = {
            executor.submit(run, cmd, timeout): label for cmd, label, timeout in checks
        }
        for future in future_to_label:
            label = future_to_label[future]
            try:
                result = future.result()
            except subprocess.TimeoutExpired:
                ok = False
                print(f"[verify-state-delta] {label} timed out", file=sys.stderr)
                continue
            if result.returncode != 0:
                ok = False
                print(f"[verify-state-delta] {label} failed:")
                print(result.stdout, end="")
                print(result.stderr, end="", file=sys.stderr)
            # Stderr on a successful run (e.g. ResourceWarnings from doctest
            # modules using tempfile) is expected and must not be reported as a
            # failure.
    return ok


def main(argv: list[str] | None = None) -> int:
    args = argv or []
    force_full = "--full" in args
    show_diff = "--diff" in args
    record_full_suite = "--record-full-suite" in args
    current_head = head()

    if not force_full and working_tree_clean():
        marker = read_marker()
        if marker is not None and marker.get("head") == current_head:
            if record_full_suite:
                pass  # fall through to record marker update below
            else:
                print(
                    "[verify-state-delta] Working tree clean and HEAD matches the "
                    "last verified checkpoint; skipping redundant verification."
                )
                return 0
        if marker is not None:
            # Compute the source delta once. It feeds both the optional --diff
            # listing and the skip decision; the previous code recomputed it via
            # source_changed_since(), paying for a second diff+status pair of
            # subprocesses on every activation (AVOIDABLE_PROCESS_DELAY on the
            # hot clean-tree path).
            changed = diff_since(marker["head"]) + untracked_source_files()
            if show_diff and changed:
                for path in sorted(set(changed)):
                    print(f"[verify-state-delta] changed: {path}")
            if not changed and not record_full_suite:
                print(
                    "[verify-state-delta] Working tree clean and no source-relevant "
                    "file changed since the last verified checkpoint; skipping "
                    "redundant verification."
                )
                return 0

    print("[verify-state-delta] Running verification battery...")
    if not battery_ok():
        print(
            "[verify-state-delta] Verification battery failed; checkpoint not advanced.",
            file=sys.stderr,
        )
        return 1

    marker = read_marker() or {}
    if marker.get("head") != current_head or record_full_suite or force_full:
        new_marker = {"head": current_head}
        # Preserve/record full-suite provenance: --full and --record-full-suite
        # indicate a full `unittest discover` run accompanied this verification.
        if record_full_suite or force_full:
            new_marker["full_suite_head"] = current_head
        elif "full_suite_head" in marker:
            new_marker["full_suite_head"] = marker["full_suite_head"]
        write_marker(new_marker)
        print(f"[verify-state-delta] Verification passed; checkpoint advanced to {current_head}.")
    else:
        print(f"[verify-state-delta] Verification passed; checkpoint already at {current_head}.")
    if marker.get("full_suite_head") and tests_changed_since(marker["full_suite_head"]):
        print(
            "[verify-state-delta] Note: tests/ changed since last recorded full-suite run "
            f"({marker['full_suite_head'][:12]}). Run `make test-full` or `python -m unittest "
            "discover tests/` to exercise test-only changes."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
