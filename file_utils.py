"""File and path utility functions."""

import shutil
from pathlib import Path
from typing import Any, List, Optional, Union


def read_text(path: Union[str, Path]) -> str:
    """Read text content from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
    """Write text content to a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def read_json(path: Union[str, Path]) -> Any:
    """Read JSON content from a file."""
    import json

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(
    path: Union[str, Path],
    data: Any,
    indent: Optional[int] = 2,
    ensure_ascii: bool = False,
) -> None:
    """Write JSON content to a file."""
    import json

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure a directory exists and return its Path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(
    path: Union[str, Path],
    pattern: Optional[str] = None,
    recursive: bool = False,
) -> List[Path]:
    """List files in a directory."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")

    if recursive:
        if pattern:
            return sorted(path.rglob(pattern))
        return sorted([p for p in path.rglob("*") if p.is_file()])
    else:
        if pattern:
            return sorted(path.glob(pattern))
        return sorted([p for p in path.iterdir() if p.is_file()])


def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """Copy a file from src to dst."""
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def delete_file(path: Union[str, Path]) -> None:
    """Delete a file if it exists."""
    path = Path(path)
    if path.exists() and path.is_file():
        path.unlink()
