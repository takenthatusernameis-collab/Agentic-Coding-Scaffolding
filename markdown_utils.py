"""Markdown utility functions."""

from __future__ import annotations

import re
from typing import List


def extract_code_blocks(text: str) -> List[str]:
    """Extract fenced code blocks (``` ... ```) from markdown text."""
    pattern = re.compile(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)
    return [block.strip("\n") for block in pattern.findall(text)]


def strip_markdown(text: str) -> str:
    """Strip common markdown formatting from text."""
    # Remove fenced code blocks entirely, keeping inner content
    text = re.sub(r"```[a-zA-Z0-9_+-]*\n", "", text)
    text = text.replace("```", "")
    # Remove inline code backticks
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove emphasis markers
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    # Remove heading markers
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    # Remove link markup, keep label
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Remove blockquote markers
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    return text


def count_words(text: str) -> int:
    """Count whitespace-delimited words in text."""
    return len(text.split())


def is_heading(line: str) -> bool:
    """Return True if line is a markdown heading."""
    return bool(re.match(r"^#{1,6}\s+\S", line))


def heading_level(line: str) -> int:
    """Return heading level (1-6) or 0 if not a heading."""
    match = re.match(r"^(#{1,6})\s+\S", line)
    if not match:
        return 0
    return len(match.group(1))
