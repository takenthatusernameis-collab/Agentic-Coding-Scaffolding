"""CSV utility functions."""

import csv
from typing import Any, Dict, List, Optional


def read_csv(
    path: str,
    delimiter: str = ",",
    fieldnames: Optional[List[str]] = None,
) -> List[Dict[str, str]]:
    """Read CSV file and return list of dictionaries."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=delimiter)
        return [dict(row) for row in reader]


def read_csv_as_lists(path: str, delimiter: str = ",") -> List[List[str]]:
    """Read CSV file and return list of lists."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return list(reader)


def write_csv(
    path: str,
    rows: List[Dict[str, Any]],
    fieldnames: Optional[List[str]] = None,
    delimiter: str = ",",
) -> None:
    """Write list of dictionaries to CSV file."""
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def write_csv_from_lists(path: str, rows: List[List[Any]], delimiter: str = ",") -> None:
    """Write list of lists to CSV file."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)


def append_csv_row(path: str, row: Dict[str, Any], fieldnames: Optional[List[str]] = None) -> None:
    """Append a single row to CSV file."""
    if fieldnames is None:
        fieldnames = list(row.keys())
    import os

    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
