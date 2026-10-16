"""Line-oriented and atomic input/output utility functions."""

import os
import tempfile
from pathlib import Path
from typing import Iterator, List, Union


def read_lines(path: Union[str, Path]) -> List[str]:
    """Read a file and return its lines without trailing newlines.

    Args:
        path: Path to the file to read.

    Returns:
        A list of strings, one per line, with trailing newlines removed.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def write_lines(path: Union[str, Path], lines: List[str], encoding: str = "utf-8") -> None:
    """Write a list of strings to a file, one line per entry.

    Args:
        path: Path to the file to write.
        lines: The lines to write.
        encoding: Text encoding to use (default: "utf-8").

    Raises:
        TypeError: If lines is not a list of strings.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(lines, list) or not all(isinstance(line, str) for line in lines):
        raise TypeError("lines must be a list of strings")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        for line in lines:
            f.write(line)
            f.write("\n")


def append_text(path: Union[str, Path], text: str, encoding: str = "utf-8") -> None:
    """Append text to the end of a file, creating it if needed.

    Args:
        path: Path to the file to append to.
        text: The text to append.
        encoding: Text encoding to use (default: "utf-8").

    Raises:
        TypeError: If text is not a string.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding=encoding) as f:
        f.write(text)


def atomic_write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> None:
    """Write text to a file atomically via a temp file and os.replace.

    The content is first written to a temporary file in the same directory,
    then atomically moved into place so readers never see a partial write.

    Args:
        path: Path to the file to write.
        content: The text content to write.
        encoding: Text encoding to use (default: "utf-8").

    Raises:
        TypeError: If content is not a string.
        OSError: If there is an issue writing or replacing the file.
    """
    if not isinstance(content, str):
        raise TypeError("content must be a string")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def stream_copy(src: Union[str, Path], dst: Union[str, Path], chunk_size: int = 65536) -> int:
    """Copy the contents of src to dst in chunks, returning bytes copied.

    Args:
        src: Path to the source file.
        dst: Path to the destination file.
        chunk_size: Number of bytes to read per chunk (default: 65536).

    Returns:
        The total number of bytes copied.

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If there is an issue reading or writing the files.
    """
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(chunk_size)
            if not chunk:
                break
            fout.write(chunk)
            total += len(chunk)
    return total


def count_lines(path: Union[str, Path]) -> int:
    """Return the number of lines in a file.

    Args:
        path: Path to the file to count.

    Returns:
        The number of lines in the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def iter_lines(path: Union[str, Path]) -> Iterator[str]:
    """Yield lines from a file one at a time without loading it into memory.

    Args:
        path: Path to the file to iterate over.

    Yields:
        Each line of the file with its trailing newline removed.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


__all__ = [
    "read_lines",
    "write_lines",
    "append_text",
    "atomic_write_text",
    "stream_copy",
    "count_lines",
    "iter_lines",
]
