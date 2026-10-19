"""Path manipulation utilities wrapping the :mod:`pathlib` standard library module."""

from __future__ import annotations

from pathlib import Path
from typing import Union

__all__ = [
    "ensure_dir",
    "join",
    "exists",
    "is_file",
    "is_dir",
    "read_text",
    "write_text",
    "glob",
    "rglob",
    "suffix",
    "stem",
    "parent",
]


def ensure_dir(path: Union[str, Path]) -> Path:
    """Create the directory (and parents) if missing and return it."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def join(base: Union[str, Path], *parts: Union[str, Path]) -> Path:
    """Join path parts and return a :class:`Path`."""
    p = Path(base)
    for part in parts:
        p = p / part
    return p


def exists(path: Union[str, Path]) -> bool:
    return Path(path).exists()


def is_file(path: Union[str, Path]) -> bool:
    return Path(path).is_file()


def is_dir(path: Union[str, Path]) -> bool:
    return Path(path).is_dir()


def read_text(path: Union[str, Path], encoding: str = "utf-8") -> str:
    return Path(path).read_text(encoding=encoding)


def write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> int:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p.write_text(content, encoding=encoding)


def glob(path: Union[str, Path], pattern: str) -> list[Path]:
    return sorted(Path(path).glob(pattern))


def rglob(path: Union[str, Path], pattern: str) -> list[Path]:
    return sorted(Path(path).rglob(pattern))


def suffix(path: Union[str, Path]) -> str:
    return Path(path).suffix


def stem(path: Union[str, Path]) -> str:
    return Path(path).stem


def parent(path: Union[str, Path]) -> Path:
    return Path(path).parent
