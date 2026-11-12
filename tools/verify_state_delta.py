#!/usr/bin/env python3
"""Verify repository state, skipping redundant re-runs via a state-delta guard.

Every activation previously re-ran the full verification battery
(``refresh_scaffold --check``, ``scan_untested``, ``tests.test_public_api``)
against unchanged state and then manufactured a duplicate handover entry just to
satisfy the CI checkpoint gate. That is a repeated no-op verification cycle
(AVOIDABLE_PROCESS_DELAY).

This tool records the HEAD at which verification last passed in
``.kilo/last_verified.checkpoint``. When the working tree is clean and no
source-relevant file has changed since that checkpoint, the battery is skipped.
When state has changed, the battery runs and the checkpoint is advanced.

Usage:
    python tools/verify_state_delta.py [--full]

With ``--full`` the battery always runs and the checkpoint is always advanced.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = ROOT / ".kilo" / "last_verified.checkpoint"

#: Paths whose changes invalidate the verified checkpoint.
SOURCE_GLOBS = (
    "*.py",
    "Makefile",
    "pyproject.toml",
    "scaffold.sh",
    ".kilo/command/scaffold-project.md",
)


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)


def working_tree_clean() -> bool:
    result = run(["git", "status", "--porcelain"])
    assert isinstance(result.stdout, str)
    return result.stdout.strip() == ""


def head() -> str:
    result = run(["git", "rev-parse", "HEAD"])
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


def source_changed_since(ref: str) -> bool:
    """Return True when any source-relevant file changed between *ref* and HEAD."""
    result = run(["git", "diff", "--name-only", ref, "HEAD", "--"] + list(SOURCE_GLOBS))
    return bool(result.stdout.strip())


def battery_ok() -> bool:
    """Run the verification battery; return True when every check passes."""
    checks = [
        (["python", "tools/refresh_scaffold.py", "--check"], "refresh_scaffold --check"),
        (["python", "tools/scan_untested.py"], "scan_untested"),
        (
            ["python", "-m", "unittest", "tests.test_public_api"],
            "tests.test_public_api",
        ),
    ]
    ok = True
    for cmd, label in checks:
        result = run(cmd)
        if result.returncode != 0:
            ok = False
            print(f"[verify-state-delta] {label} failed:")
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
    return ok


def main(argv: list[str] | None = None) -> int:
    force_full = "--full" in (argv or [])
    current_head = head()

    if not force_full and working_tree_clean():
        marker = read_marker()
        if marker is not None and marker.get("head") == current_head:
            print(
                "[verify-state-delta] Working tree clean and HEAD matches the "
                "last verified checkpoint; skipping redundant verification."
            )
            return 0
        if marker is not None and not source_changed_since(marker["head"]):
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

    write_marker({"head": current_head})
    print(f"[verify-state-delta] Verification passed; checkpoint advanced to {current_head}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
