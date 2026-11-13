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
with the current contents of that file, it creates the heredoc of a wrapper
module that the generator does not embed yet, and it removes the heredoc of a
wrapper module whose repository file no longer exists. Run it after adding,
editing, or removing a module or test, then re-run the test suite to confirm the
invariant holds.

Usage:
    python tools/refresh_scaffold.py [--check]

``--check`` reports stale and missing copies and exits with a non-zero status
instead of rewriting the generator. A block whose repository copy is gone is
stale as well, so a module removed from the repository is reported instead of
silently kept alive by the generator.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"

#: Persistent mtime cache for the ``--check`` fast path. When ``scaffold.sh``
#: and every managed repository file are unchanged since the last successful
#: in-sync check, the expensive parse/compare work is skipped. The cache lives
#: in ``.kilo/`` and is gitignored so it never dirties the working tree.
CACHE_FILE = ROOT / ".kilo" / "refresh_scaffold_cache.json"

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


def managed_copy_paths() -> list[str]:
    """Return every repository file the tool can compare or embed.

    Includes all embedded wrapper module/test copies and the templated project
    documents. The list is stable so cache fingerprints are deterministic.
    """
    return sorted(set(wrapper_copies()) | set(TEMPLATED_COPIES))


def _mtime(path: Path) -> float | None:
    """Return the modification time of *path*, or ``None`` when absent."""
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def load_check_cache() -> dict:
    """Load the persistent check-mode mtime cache, or an empty cache."""
    try:
        data = json.loads(CACHE_FILE.read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_check_cache(cache: dict) -> None:
    """Atomically persist *cache* to the cache file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_FILE.with_name(CACHE_FILE.name + ".tmp")
    tmp.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")
    tmp.replace(CACHE_FILE)


def _check_cache_fingerprint(managed_paths: list[str] | None = None) -> dict[str, float | None]:
    """Return the mtime fingerprint for an in-sync ``--check`` state.

    If *managed_paths* is provided, use it instead of recomputing the list of
    managed paths. This avoids redundant filesystem discovery when the caller
    already knows the path list.
    """
    fingerprint = {"__scaffold__": _mtime(SCAFFOLD)}
    paths = managed_paths if managed_paths is not None else managed_copy_paths()
    for relative in paths:
        fingerprint[relative] = _mtime(ROOT / relative)
    return fingerprint


def check_cache_hit() -> bool:
    """Return ``True`` when the cached in-sync ``--check`` fingerprint matches.

    Uses a fast path that avoids recomputing the managed-paths list when the
    repository root mtime matches the cached value, indicating no files were
    added or removed since the cache was written.
    """
    cache = load_check_cache()
    if cache.get("status") != "in_sync":
        return False
    expected = cache.get("fingerprint")
    if not isinstance(expected, dict):
        return False
    cached_root_mtime = cache.get("root_mtime")
    if cached_root_mtime is not None:
        current_root_mtime = _mtime(ROOT)
        if current_root_mtime != cached_root_mtime:
            return False
        cached_paths = cache.get("managed_paths")
        if isinstance(cached_paths, list):
            return expected == _check_cache_fingerprint(cached_paths)
    return expected == _check_cache_fingerprint()


def record_check_cache_in_sync() -> None:
    """Record that the generator is currently in sync for ``--check``."""
    paths = managed_copy_paths()
    save_check_cache({
        "status": "in_sync",
        "fingerprint": _check_cache_fingerprint(paths),
        "managed_paths": paths,
        "root_mtime": _mtime(ROOT),
    })


def clear_check_cache() -> None:
    """Invalidate the ``--check`` cache when state is not known in-sync."""
    try:
        CACHE_FILE.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass


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


def stale_copies(scaffold_text: str) -> list[re.Match[str]]:
    """Return the embedded blocks whose repository copy no longer exists.

    A block is stale when the tool manages the path (a Python source or one of
    the templated documents) but the repository holds no file for it. The
    generator must stop emitting such a file, so the block is dropped instead of
    being kept alive after the module was removed.
    """
    stale: list[re.Match[str]] = []
    for match in embedded_blocks(scaffold_text):
        relative = match.group("path")
        if expected_body(relative) is not None:
            continue
        if is_verbatim_copy(relative) or is_templated_copy(relative):
            stale.append(match)
    return stale


def block_start(scaffold_text: str, match: re.Match[str]) -> int:
    """Return the offset where *match*'s block begins, comment included.

    Every block is preceded by a ``# --- <path> ---`` comment. Removing the
    comment together with the heredoc keeps the generator free of orphaned
    comments; a block without one starts at the heredoc itself.
    """
    marker = f"# --- {match.group('path')} ---\n"
    index = scaffold_text.rfind(marker, 0, match.start())
    if index == -1:
        return match.start()
    # Drop the blank line the removed block leaves behind as well, so the
    # remaining blocks stay separated by exactly one empty line.
    if index >= 2 and scaffold_text[index - 2 : index] == "\n\n":
        return index - 1
    return index


def remove_stale_copies(scaffold_text: str) -> tuple[str, list[str]]:
    """Return the generator without the stale blocks and the removed paths."""
    stale = stale_copies(scaffold_text)
    if not stale:
        return scaffold_text, []
    pieces: list[str] = []
    cursor = 0
    for match in stale:
        pieces.append(scaffold_text[cursor : block_start(scaffold_text, match)])
        cursor = match.end()
    pieces.append(scaffold_text[cursor:])
    return "".join(pieces), [match.group("path") for match in stale]


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
        module = f"{stem[len('test_') :]}.py"
        for match in embedded_blocks(scaffold_text):
            if match.group("path") == module:
                return match.end()
    blocks = embedded_blocks(scaffold_text)
    if blocks:
        return blocks[-1].end()
    return len(scaffold_text)


def add_missing_copies(scaffold_text: str) -> tuple[str, list[str]]:
    """Return the generator with the missing wrapper blocks added.

    The list of missing copies and their insertion anchors are computed once
    against the original text. The blocks are then inserted in reverse order
    of their anchor, so earlier anchors stay valid and no block is rescanned
    after it is inserted. Rescanning the growing text for every missing copy
    made this quadratic in the number of embedded blocks: a generator that
    lacked every block took about fourteen seconds to refresh.
    """
    missing = missing_copies(scaffold_text)
    if not missing:
        return scaffold_text, []

    anchors = [(anchor_for(relative, scaffold_text), relative) for relative in missing]
    # Insert from the end backwards so the offsets of earlier anchors are
    # unaffected by the blocks that are added after them.
    anchors.sort(key=lambda pair: pair[0], reverse=True)

    text = scaffold_text
    added: list[str] = []
    for anchor, relative in anchors:
        text = text[:anchor] + render_block(relative) + text[anchor:]
        added.append(relative)
    return text, added


def delimiter_for(relative: str, preferred: str, body: str) -> str:
    """Return a delimiter that the heredoc of *relative* can close with.

    *preferred* is the delimiter the block already uses. It is kept whenever no
    line of *body* equals it, so a rewritten block keeps the style of the
    generator. A body that does hold such a line falls back to a delimiter
    derived from the file name, which is what a newly created block uses.

    Example:
        >>> delimiter_for("README.md", "__README__", "# a title\\n")
        '__README__'
        >>> delimiter_for("README.md", "README", "README\\n")
        'README_COPY'
    """
    if preferred not in set(body.split("\n")):
        return preferred
    return unique_delimiter(relative, body)


def refresh(scaffold_text: str) -> tuple[str, list[str], list[str]]:
    """Return the refreshed generator text together with the changed and stale paths.

    A rewritten block keeps its delimiter, unless the new body holds a line
    that would close the heredoc with it. Reusing such a delimiter is wrong
    once the repository copy grows that line: the emitted heredoc would end
    early, the generator would no longer hold the copy, and the next refresh
    would rewrite the same block forever instead of converging. Falling back
    to the delimiter a newly created block would use makes the refresh
    idempotent.

    Example:
        >>> text = (
        ...     "cat > \\"$OUTPUT_DIR/doctest_utils.py\\" <<'DOCTEST_UTILS'\\n"
        ...     "an outdated body\\nDOCTEST_UTILS\\n"
        ... )
        >>> refreshed, changed, stale = refresh(text)
        >>> changed, stale
        (['doctest_utils.py'], [])
        >>> refresh(refreshed)[0] == refreshed
        True
    """
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
            delimiter = delimiter_for(relative, match.group("delim"), expected)
            replacement = (
                f"cat > \"$OUTPUT_DIR/{relative}\" <<'{delimiter}'\n"
                f"{expected}\n{delimiter}\n"
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

    if args.check and check_cache_hit():
        # Update cache to new format if it was in old format
        cache = load_check_cache()
        if "root_mtime" not in cache or "managed_paths" not in cache:
            record_check_cache_in_sync()
        print("all embedded copies are in sync")
        return 0

    scaffold_text = SCAFFOLD.read_text()
    refreshed, changed, stale = refresh(scaffold_text)
    refreshed, removed = remove_stale_copies(refreshed)
    refreshed, added = add_missing_copies(refreshed)

    if args.check:
        for relative in changed:
            print(f"stale: {relative}")
        for relative in removed:
            print(f"no repository copy: {relative}")
        for relative in added:
            print(f"missing: {relative}")
        if changed or removed or added:
            clear_check_cache()
            print(f"{len(changed) + len(removed) + len(added)} embedded copies are out of sync")
            return 1
        record_check_cache_in_sync()
        print("all embedded copies are in sync")
        return 0

    if changed or removed or added:
        SCAFFOLD.write_text(refreshed)
        clear_check_cache()
    for relative in changed:
        print(f"refreshed: {relative}")
    for relative in removed:
        print(f"removed: {relative}")
    for relative in added:
        print(f"added: {relative}")
    for relative in stale:
        print(f"no repository copy: {relative}")
    print(f"{len(changed) + len(removed) + len(added)} embedded copies refreshed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
