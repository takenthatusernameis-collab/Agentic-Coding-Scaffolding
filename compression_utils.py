"""Compression and decompression utility functions."""

import bz2
import gzip
import io
import tarfile
import zipfile
from pathlib import Path
from typing import List, Optional, Union


def gzip_compress(data: Union[bytes, str], encoding: str = "utf-8") -> bytes:
    """Compress data using gzip."""
    if isinstance(data, str):
        data = data.encode(encoding)
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes or str")
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as f:
        f.write(data)
    return buf.getvalue()


def gzip_decompress(data: bytes, encoding: Optional[str] = None) -> Union[bytes, str]:
    """Decompress gzip compressed data."""
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    buf = io.BytesIO(data)
    with gzip.GzipFile(fileobj=buf, mode="rb") as f:
        result = f.read()
    if encoding is not None:
        return result.decode(encoding)
    return result


def bz2_compress(data: Union[bytes, str], encoding: str = "utf-8") -> bytes:
    """Compress data using bz2."""
    if isinstance(data, str):
        data = data.encode(encoding)
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes or str")
    return bz2.compress(data)


def bz2_decompress(data: bytes, encoding: Optional[str] = None) -> Union[bytes, str]:
    """Decompress bz2 compressed data."""
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    result = bz2.decompress(data)
    if encoding is not None:
        return result.decode(encoding)
    return result


def zip_compress_files(files: List[Union[str, Path]], output_path: Union[str, Path]) -> None:
    """Compress a list of files into a zip archive."""
    output_path = Path(output_path)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in files:
            file_path = Path(file_path)
            if file_path.is_file():
                zf.write(file_path, file_path.name)
            else:
                raise FileNotFoundError(f"File not found: {file_path}")


def zip_extract(archive_path: Union[str, Path], extract_path: Union[str, Path] = ".") -> None:
    """Extract a zip archive."""
    archive_path = Path(archive_path)
    extract_path = Path(extract_path)
    extract_path.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "r") as zf:
        zf.extractall(extract_path)


def tar_compress(
    files: List[Union[str, Path]], output_path: Union[str, Path], mode: str = "w"
) -> None:
    """Compress files into a tar archive."""
    output_path = Path(output_path)
    with tarfile.open(str(output_path), mode) as tf:  # type: ignore[call-overload]
        for file_path in files:
            file_path = Path(file_path)
            if file_path.exists():
                tf.add(file_path, file_path.name)
            else:
                raise FileNotFoundError(f"File not found: {file_path}")


def tar_extract(archive_path: Union[str, Path], extract_path: Union[str, Path] = ".") -> None:
    """Extract a tar archive."""
    archive_path = Path(archive_path)
    extract_path = Path(extract_path)
    extract_path.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r") as tf:
        tf.extractall(extract_path)
