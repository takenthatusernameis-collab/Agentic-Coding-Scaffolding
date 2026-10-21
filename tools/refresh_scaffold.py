#!/usr/bin/env python3
"""Refresh the file copies embedded in ``scaffold.sh`` from the repository.

The scaffold generator embeds a verbatim copy of every wrapper module and test
file so that a scaffolded project is a faithful copy of the project that
generated it. Those copies live in heredoc blocks inside ``scaffold.sh`` and
drift out of sync whenever a module is edited in the repository without
refreshing the generator.

The documents that name the project are embedded as templates: the name of the
project is replaced with the ``${PROJECT_NAME}`` placeholder, which the
generator substitutes in the scaffolded project.

This script rewrites every heredoc whose target path exists in the repository
with the current contents of that file, and it creates the heredoc of a
wrapper module that the generator does not embed yet. Run it after adding or
editing a module or test, then re-run the test suite to confirm the invariant
holds.

Usage:
    python tools/refresh_scaffold.py [--check]

``--check`` reports stale and missing copies and exits with a non-zero status
instead of rewriting the generator.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"

#: The documents that are embedded as templates instead of verbatim copies.
TEMPLATED_COPIES = ("README.md", "AGENTS.md", "CHANGELOG.md")

#: The placeholder the generator substitutes with the name of the project.
PROJECT_NAME_PLACEHOLDER = "${PROJECT_NAME}"

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
    verbatim. The documents that name the project are embedded as templates,
    and the agent instructions are maintained separately.
    """
    return relative.endswith(".py") or relative == ".kilo/command/scaffold-project.md"


def is_templated_copy(relative: str) -> bool:
    """Return ``True`` when *relative* is embedded as a template.

    A template holds the repository document with the name of the project
    replaced by the placeholder the generator substitutes.
    """
    return relative in TEMPLATED_COPIES


def repository_body(relative: str) -> str | None:
    """Return the repository copy of *relative*, or ``None`` when it is absent."""
    path = ROOT / relative
    if not path.is_file():
        return None
    return path.read_text().rstrip("\n")


def project_name() -> str:
    """Return the name of the project, taken from the title of the README.

    The title of the README is the single line that names the project, so it
    is the source the templates are derived from.
    """
    readme = ROOT / "README.md"
    if not readme.is_file():
        return ""
    first_line = readme.read_text().split("\n", 1)[0]
    if not first_line.startswith("# "):
        return ""
    return first_line[2:].strip()


def templated_body(relative: str) -> str | None:
    """Return the template of *relative*, or ``None`` when it is absent.

    The template is the repository document with the name of the project
    replaced by the placeholder the generator substitutes in the scaffolded
    project. The name is only replaced where it stands on its own, so a word
    that starts with the name of the project is left alone.
    """
    body = repository_body(relative)
    if body is None:
        return None
    name = project_name()
    if not name:
        return body
    return re.sub(rf"\b{re.escape(name)}\b", PROJECT_NAME_PLACEHOLDER, body)


def expected_body(relative: str) -> str | None:
    """Return the body the generator has to hold for *relative*.

    ``None`` is returned for a file the tool does not manage, so the caller
    leaves its block untouched.
    """
    if is_templated_copy(relative):
        return templated_body(relative)
    if is_verbatim_copy(relative):
        return repository_body(relative)
    return None


def wrapper_copies() -> list[str]:
    """Return the repository files the generator has to embed, in a stable order.

    Every wrapper module and its test are copied into a scaffolded project, so
    the generator embeds both. The module comes before its test, so a module
    and its test are added next to each other.
    """
    relatives: list[str] = []
    stems = sorted(path.stem for path in ROOT.glob("*_utils.py") if path.is_file())
    for stem in stems:
        for relative in (f"{stem}.py", f"tests/test_{stem}.py"):
            if (ROOT / relative).is_file():
                relatives.append(relative)
    return relatives


def heredoc_delimiter(relative: str) -> str:
    """Return the heredoc delimiter that belongs to *relative*.

    The delimiter follows the convention of the generator: the name of the
    file in upper case, with the characters a shell delimiter cannot hold
    replaced by an underscore.
    """
    return re.sub(r"[^A-Z0-9_]", "_", Path(relative).stem.upper())


def unique_delimiter(relative: str, body: str) -> str:
    """Return a delimiter that no line of *body* closes the heredoc with.

    A file whose body happens to hold a line that equals the derived
    delimiter would end the heredoc early, so the delimiter is extended until
    it is unique.
    """
    delimiter = heredoc_delimiter(relative)
    lines = set(body.split("\n"))
    while delimiter in lines:
        delimiter = f"{delimiter}_COPY"
    return delimiter


def missing_copies(scaffold_text: str) -> list[str]:
    """Return the wrapper files the generator does not embed yet."""
    embedded = {match.group("path") for match in embedded_blocks(scaffold_text)}
    return [relative for relative in wrapper_copies() if relative not in embedded]


def render_block(relative: str) -> str:
    """Return the generator block that writes *relative* into the output directory.

    The block starts with a blank line, so the new file is separated from the
    block that precedes it by exactly one empty line, the way the blocks of
    the generator are laid out.
    """
    body = repository_body(relative) or ""
    delimiter = unique_delimiter(relative, body)
    return (
        f"\n# --- {relative} ---\n"
        f"cat > \"$OUTPUT_DIR/{relative}\" <<'{delimiter}'\n"
        f"{body}\n"
        f"{delimiter}\n"
    )


def anchor_for(relative: str, scaffold_text: str) -> int:
    """Return the offset in *scaffold_text* where a new block is inserted.

    The test of a module is placed right behind the module it belongs to, and
    a module that the generator does not embed yet is placed behind the last
    block of the generator.
    """
    stem = Path(relative).stem
    if stem.startswith("test_"):
        module = f"{stem[len('test_'):]}.py"
        for match in embedded_blocks(scaffold_text):
            if match.group("path") == module:
                return match.end()
    blocks = embedded_blocks(scaffold_text)
    if blocks:
        return blocks[-1].end()
    return len(scaffold_text)


def add_missing_copies(scaffold_text: str) -> tuple[str, list[str]]:
    """Return the generator with the missing wrapper blocks added."""
    added: list[str] = []
    text = scaffold_text
    for relative in missing_copies(text):
        anchor = anchor_for(relative, text)
        text = text[:anchor] + render_block(relative) + text[anchor:]
        added.append(relative)
    return text, added


def refresh(scaffold_text: str) -> tuple[str, list[str], list[str]]:
    """Return the refreshed generator text together with the changed and stale paths."""
    changed: list[str] = []
    stale: list[str] = []
    pieces: list[str] = []
    cursor = 0
    for match in embedded_blocks(scaffold_text):
        relative = match.group("path")
        expected = expected_body(relative)
        if expected is None:
            if is_verbatim_copy(relative) or is_templated_copy(relative):
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
    refreshed, added = add_missing_copies(refreshed)

    if args.check:
        for relative in changed:
            print(f"stale: {relative}")
        for relative in added:
            print(f"missing: {relative}")
        if changed or added:
            print(f"{len(changed) + len(added)} embedded copies are out of sync")
            return 1
        print("all embedded copies are in sync")
        return 0

    if changed or added:
        SCAFFOLD.write_text(refreshed)
    for relative in changed:
        print(f"refreshed: {relative}")
    for relative in added:
        print(f"added: {relative}")
    for relative in stale:
        print(f"no repository copy: {relative}")
    print(f"{len(changed) + len(added)} embedded copies refreshed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
