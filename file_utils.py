"""File and path utility functions."""

import json
import shutil
from pathlib import Path
from typing import Any, List, Union

__all__ = [
    "copy_file",
    "delete_file",
    "ensure_dir",
    "list_files",
    "read_json",
    "read_text",
    "write_json",
    "write_text",
]


def _require_path(value: object, name: str = "path") -> Union[str, Path]:
    """Validate that *value* is a path-like object (str or Path).

    Raises:
        TypeError: if *value* is not a str or Path.
    """
    if not isinstance(value, (str, Path)):
        raise TypeError(f"{name} must be a str or Path, got {type(value).__name__}")
    return value


def read_text(path: Union[str, Path]) -> str:
    """Read text content from a file.

    Args:
        path: File path as str or Path.

    Returns:
        The full text content of the file.

    Raises:
        TypeError: if *path* is not a str or Path.
        FileNotFoundError: if *path* does not exist.
        OSError: on other I/O errors.

    Examples:
        >>> import tempfile, os
        >>> path = os.path.join(tempfile.gettempdir(), "kilo_read_text.txt")
        >>> _ = open(path, "w").write("hello")
        >>> read_text(path)
        'hello'
        >>> os.remove(path)
    """
    path = _require_path(path)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(
    path: Union[str, Path], content: str, encoding: str = "utf-8"
) -> None:
    """Write text content to a file, creating parent directories as needed.

    Args:
        path: File path as str or Path.
        content: Text to write.
        encoding: Character encoding to use.

    Raises:
        TypeError: if *path* is not a str or Path.
    """
    path = _require_path(path)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def read_json(path: Union[str, Path]) -> Any:
    """Read JSON content from a file.

    Args:
        path: File path as str or Path.

    Returns:
        The parsed JSON value.

    Raises:
        TypeError: if *path* is not a str or Path.
        FileNotFoundError: if *path* does not exist.
        OSError: on other I/O errors.
        json.JSONDecodeError: if the file does not contain valid JSON.

    Examples:
        >>> import tempfile, os
        >>> path = os.path.join(tempfile.gettempdir(), "kilo_read_json.json")
        >>> _ = open(path, "w").write('{"a": 1}')
        >>> read_json(path)
        {'a': 1}
        >>> os.remove(path)
    """
    path = _require_path(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(
    path: Union[str, Path],
    data: Any,
    indent: int = 2,
    ensure_ascii: bool = False,
) -> None:
    """Write JSON content to a file, creating parent directories as needed.

    Args:
        path: File path as str or Path.
        data: JSON-serializable value to write.
        indent: Indentation level for pretty-printing.
        ensure_ascii: If True, escape non-ASCII characters.

    Raises:
        TypeError: if *path* is not a str or Path.
    """
    path = _require_path(path)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it (and parents) if needed.

    Args:
        path: Directory path as str or Path.

    Returns:
        The directory as a Path.

    Raises:
        TypeError: if *path* is not a str or Path.

    Examples:
        >>> import tempfile, os
        >>> path = os.path.join(tempfile.gettempdir(), "kilo_ensure_dir")
        >>> result = ensure_dir(path)
        >>> os.path.isdir(result)
        True
        >>> os.rmdir(result)
    """
    path = _require_path(path)
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(
    path: Union[str, Path],
    pattern: str = "",
    recursive: bool = False,
) -> List[Path]:
    """List files in a directory.

    Args:
        path: Directory path as str or Path.
        pattern: Optional glob pattern to filter entries.
        recursive: If True, search recursively.

    Returns:
        A sorted list of matching file paths.

    Raises:
        TypeError: if *path* is not a str or Path.
        FileNotFoundError: if *path* does not exist.
        ValueError: if *path* exists but is not a directory.
    """
    path = _require_path(path)
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
    """Copy a file from *src* to *dst*, creating parent directories as needed.

    Args:
        src: Source file path as str or Path.
        dst: Destination file path as str or Path.

    Raises:
        TypeError: if *src* or *dst* is not a str or Path.
        FileNotFoundError: if *src* does not exist.
        OSError: on other I/O errors.
    """
    src = _require_path(src, "src")
    dst = _require_path(dst, "dst")
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def delete_file(path: Union[str, Path]) -> None:
    """Delete a file if it exists; no-op for missing files.

    Args:
        path: File path as str or Path.

    Raises:
        TypeError: if *path* is not a str or Path.
        OSError: if *path* exists but is not a regular file.
    """
    path = _require_path(path)
    path = Path(path)
    if path.exists() and path.is_file():
        path.unlink()
