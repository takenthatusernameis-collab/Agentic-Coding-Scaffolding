"""Utilities for SQLite database access (wrapping :mod:`sqlite3`).

This module provides a small, validated layer over the standard library
``sqlite3`` module for opening connections, executing statements, fetching
rows, and inspecting schema. All functions validate their inputs and raise
``TypeError`` or ``ValueError`` on invalid arguments.
"""

import sqlite3 as _sqlite3
from typing import Any, Optional, Sequence


def connect(database: str = ":memory:", *, timeout: float = 5.0) -> _sqlite3.Connection:
    """Open a connection to the SQLite database *database*.

    Args:
        database: Path to the database file, or ``":memory:"`` for an
            in-memory database.
        timeout: How long to wait for a lock before raising, in seconds.

    Returns:
        A :class:`sqlite3.Connection`.

    Raises:
        TypeError: If *database* is not a str or *timeout* is not a real
            number.
        ValueError: If *timeout* is negative.
    """
    if not isinstance(database, str):
        raise TypeError("database must be a str")
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
        raise TypeError("timeout must be a real number")
    if timeout < 0:
        raise ValueError("timeout must be non-negative")
    return _sqlite3.connect(database, timeout=float(timeout))


def execute(
    conn: _sqlite3.Connection, sql: str, params: Sequence[Any] = ()
) -> _sqlite3.Cursor:
    """Execute *sql* with optional *params* on *conn* and return the cursor.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        sql: The SQL statement to execute.
        params: Optional sequence of query parameters.

    Returns:
        The :class:`sqlite3.Cursor` after execution.

    Raises:
        TypeError: If *conn* is not a Connection, *sql* is not a str, or
            *params* is not a sequence.
    """
    if not isinstance(conn, _sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")
    if not isinstance(sql, str):
        raise TypeError("sql must be a str")
    if not isinstance(params, (list, tuple)):
        raise TypeError("params must be a list or tuple")
    return conn.execute(sql, tuple(params))


def executemany(
    conn: _sqlite3.Connection, sql: str, params_list: Sequence[Sequence[Any]]
) -> _sqlite3.Cursor:
    """Execute *sql* against every parameter sequence in *params_list*.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        sql: The SQL statement to execute.
        params_list: A sequence of parameter sequences, one per execution.

    Returns:
        The :class:`sqlite3.Cursor` after execution.

    Raises:
        TypeError: If *conn* is not a Connection, *sql* is not a str, or
            *params_list* is not a sequence of sequences.
    """
    if not isinstance(conn, _sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")
    if not isinstance(sql, str):
        raise TypeError("sql must be a str")
    if not isinstance(params_list, (list, tuple)):
        raise TypeError("params_list must be a list or tuple")
    for params in params_list:
        if not isinstance(params, (list, tuple)):
            raise TypeError("each entry in params_list must be a list or tuple")
    return conn.executemany(sql, [tuple(params) for params in params_list])


def fetch_all(
    conn: _sqlite3.Connection, sql: str, params: Sequence[Any] = ()
) -> list[tuple[Any, ...]]:
    """Execute *sql* and return all matching rows.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        sql: The SQL SELECT statement to execute.
        params: Optional sequence of query parameters.

    Returns:
        A list of rows, each row as a tuple of column values.
    """
    cursor = execute(conn, sql, params)
    return list(cursor.fetchall())


def fetch_one(
    conn: _sqlite3.Connection, sql: str, params: Sequence[Any] = ()
) -> Optional[tuple[Any, ...]]:
    """Execute *sql* and return the first matching row, or ``None``.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        sql: The SQL SELECT statement to execute.
        params: Optional sequence of query parameters.

    Returns:
        The first row as a tuple, or ``None`` when no rows match.
    """
    cursor = execute(conn, sql, params)
    row: Optional[tuple[Any, ...]] = cursor.fetchone()
    return row


def fetch_many(
    conn: _sqlite3.Connection,
    sql: str,
    size: int,
    params: Sequence[Any] = (),
) -> list[tuple[Any, ...]]:
    """Execute *sql* and return up to *size* matching rows.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        sql: The SQL SELECT statement to execute.
        size: Maximum number of rows to return.
        params: Optional sequence of query parameters.

    Returns:
        A list of up to *size* rows.

    Raises:
        TypeError: If *size* is not an int.
        ValueError: If *size* is negative.
    """
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an int")
    if size < 0:
        raise ValueError("size must be non-negative")
    cursor = execute(conn, sql, params)
    return list(cursor.fetchmany(size))


def create_table(conn: _sqlite3.Connection, table: str, columns: str) -> None:
    """Create *table* with the given *columns* SQL fragment if it does not exist.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        table: Name of the table to create.
        columns: SQL column definitions (e.g. ``"id INTEGER PRIMARY KEY, name TEXT"``).

    Raises:
        TypeError: If *conn* is not a Connection or *table*/*columns* are not strs.
        ValueError: If *table* or *columns* is empty.
    """
    if not isinstance(conn, _sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")
    if not isinstance(table, str):
        raise TypeError("table must be a str")
    if not isinstance(columns, str):
        raise TypeError("columns must be a str")
    if not table:
        raise ValueError("table must not be empty")
    if not columns.strip():
        raise ValueError("columns must not be empty")
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")
    conn.commit()


def insert_row(
    conn: _sqlite3.Connection,
    table: str,
    columns: Sequence[str],
    values: Sequence[Any],
) -> int:
    """Insert a row into *table* and return the new row id.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        table: Name of the table to insert into.
        columns: Sequence of column names.
        values: Sequence of column values, aligned with *columns*.

    Returns:
        The row id of the inserted row.

    Raises:
        TypeError: If *conn* is not a Connection or *table* is not a str, or
            *columns*/*values* are not sequences of the right kind.
        ValueError: If *table* is empty or *columns* and *values* differ in length.
    """
    if not isinstance(conn, _sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")
    if not isinstance(table, str):
        raise TypeError("table must be a str")
    if not table:
        raise ValueError("table must not be empty")
    if not isinstance(columns, (list, tuple)) or not all(
        isinstance(c, str) for c in columns
    ):
        raise TypeError("columns must be a list or tuple of strs")
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    if len(columns) != len(values):
        raise ValueError("columns and values must have the same length")
    placeholders = ", ".join("?" for _ in columns)
    col_list = ", ".join(columns)
    cursor = conn.execute(
        f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})",
        tuple(values),
    )
    conn.commit()
    lastrowid = cursor.lastrowid
    return int(lastrowid) if lastrowid is not None else 0


def query(
    conn: _sqlite3.Connection, sql: str, params: Sequence[Any] = ()
) -> list[dict[str, Any]]:
    """Execute *sql* and return rows as dictionaries keyed by column name.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        sql: The SQL SELECT statement to execute.
        params: Optional sequence of query parameters.

    Returns:
        A list of row dictionaries.
    """
    cursor = execute(conn, sql, params)
    description = cursor.description
    if description is None:
        return []
    column_names = [desc[0] for desc in description]
    return [dict(zip(column_names, row)) for row in cursor.fetchall()]


def table_exists(conn: _sqlite3.Connection, table: str) -> bool:
    """Return ``True`` if *table* exists in the database.

    Args:
        conn: An open :class:`sqlite3.Connection`.
        table: Name of the table to check.

    Returns:
        ``True`` when a table named *table* exists, otherwise ``False``.

    Raises:
        TypeError: If *conn* is not a Connection or *table* is not a str.
        ValueError: If *table* is empty.
    """
    if not isinstance(conn, _sqlite3.Connection):
        raise TypeError("conn must be a sqlite3.Connection")
    if not isinstance(table, str):
        raise TypeError("table must be a str")
    if not table:
        raise ValueError("table must not be empty")
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    return cursor.fetchone() is not None
