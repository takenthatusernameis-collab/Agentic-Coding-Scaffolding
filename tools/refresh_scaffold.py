#!/usr/bin/env python3
"""Refresh the file copies embedded in ``scaffold.sh`` from the repository.

The scaffold generator embeds a verbatim copy of every wrapper module and test
file so that a scaffolded project is a faithful copy of the project that
generated it. Those copies live in heredoc blocks inside ``scaffold.sh`` and
drift out of sync whenever a module is edited in the repository without
refreshing the generator.

This script rewrites every heredoc whose target path exists in the repository
with the current contents of that file. Run it after editing any module or
test, then re-run the test suite to confirm the invariant holds.

Usage:
    python tools/refresh_scaffold.py [--check]

``--check`` reports stale copies and exits with a non-zero status instead of
rewriting the generator.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"

HEREDOC = re.compile(
    r"cat > \"\$OUTPUT_DIR/(?P<path>[A-Za-z0-9_./-]+)\" <<'(?P<delim>[A-Z0-9_]+)'\n"
    r"(?P<body>.*?)\n(?P=delim)\n",
    re.S,
)


def embedded_blocks(scaffold_text: str) -> list[re.Match[str]]:
    """Return every quoted heredoc block that writes into the output directory."""
    return list(HEREDOC.finditer(scaffold_text))


def is_verbatim_copy(relative: str) -> bool:
    """Return ``True`` when *relative* is embedded as a verbatim repository copy.

    Only Python sources and the scaffold command documentation are copied
    verbatim. The README, the changelog, and the agent instructions are
    embedded as templates that use ``${PROJECT_NAME}`` placeholders, so they
    are maintained separately and never overwritten here.
    """
    return relative.endswith(".py") or relative == ".kilo/command/scaffold-project.md"


def repository_body(relative: str) -> str | None:
    """Return the repository copy of *relative*, or ``None`` when it is absent."""
    path = ROOT / relative
    if not path.is_file():
        return None
    return path.read_text().rstrip("\n")


def refresh(scaffold_text: str) -> tuple[str, list[str], list[str]]:
    """Return the refreshed generator text together with the changed and stale paths."""
    changed: list[str] = []
    stale: list[str] = []
    pieces: list[str] = []
    cursor = 0
    for match in embedded_blocks(scaffold_text):
        relative = match.group("path")
        if not is_verbatim_copy(relative):
            continue
        expected = repository_body(relative)
        if expected is None:
            stale.append(relative)
            continue
        if match.group("body") != expected:
            changed.append(relative)
            replacement = (
                f"cat > \"$OUTPUT_DIR/{relative}\" <<'{match.group('delim')}'\n"
                f"{expected}\n{match.group('delim')}\n"
            )
            pieces.append(scaffold_text[cursor : match.start()])
            pieces.append(replacement)
            cursor = match.end()
    pieces.append(scaffold_text[cursor:])
    return "".join(pieces), changed, stale


def main(argv: list[str] | None = None) -> int:
    """Refresh the embedded copies and report the outcome."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale copies without rewriting scaffold.sh",
    )
    args = parser.parse_args(argv)

    scaffold_text = SCAFFOLD.read_text()
    refreshed, changed, stale = refresh(scaffold_text)

    if args.check:
        for relative in changed:
            print(f"stale: {relative}")
        if changed:
            print(f"{len(changed)} embedded copies are out of sync")
            return 1
        print("all embedded copies are in sync")
        return 0

    if changed:
        SCAFFOLD.write_text(refreshed)
    for relative in changed:
        print(f"refreshed: {relative}")
    for relative in stale:
        print(f"no repository copy: {relative}")
    print(f"{len(changed)} embedded copies refreshed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
