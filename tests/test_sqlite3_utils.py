"""Tests for sqlite3_utils."""

import sqlite3
import unittest

from sqlite3_utils import (
    connect,
    create_table,
    execute,
    executemany,
    fetch_all,
    fetch_many,
    fetch_one,
    insert_row,
    query,
    table_exists,
)


class TestSqlite3Utils(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = connect(":memory:")
        create_table(
            self.conn,
            "users",
            "id INTEGER PRIMARY KEY, name TEXT NOT NULL, score REAL",
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test_connect_returns_connection(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_connect_in_memory_default(self):
        conn = connect()
        try:
            self.assertIsInstance(conn, sqlite3.Connection)
        finally:
            conn.close()

    def test_connect_type_errors(self):
        with self.assertRaises(TypeError):
            connect(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            connect(":memory:", timeout="slow")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            connect(":memory:", timeout=-1)

    def test_insert_row_and_fetch_one(self):
        row_id = insert_row(self.conn, "users", ["name", "score"], ["Ada", 92.5])
        self.assertEqual(row_id, 1)
        row = fetch_one(self.conn, "SELECT name, score FROM users WHERE id = ?", [1])
        self.assertEqual(row, ("Ada", 92.5))

    def test_insert_row_validation(self):
        with self.assertRaises(TypeError):
            insert_row(self.conn, 1, ["name"], ["x"])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            insert_row(self.conn, "", ["name"], ["x"])
        with self.assertRaises(ValueError):
            insert_row(self.conn, "users", ["name", "score"], ["x"])
        with self.assertRaises(TypeError):
            insert_row(self.conn, "users", ["name"], "x")  # type: ignore[arg-type]

    def test_fetch_all(self):
        insert_row(self.conn, "users", ["name", "score"], ["Ada", 92.5])
        insert_row(self.conn, "users", ["name", "score"], ["Bob", 87.0])
        rows = fetch_all(self.conn, "SELECT name FROM users ORDER BY name")
        self.assertEqual(rows, [("Ada",), ("Bob",)])

    def test_fetch_many(self):
        insert_row(self.conn, "users", ["name", "score"], ["Ada", 92.5])
        insert_row(self.conn, "users", ["name", "score"], ["Bob", 87.0])
        insert_row(self.conn, "users", ["name", "score"], ["Cec", 91.0])
        rows = fetch_many(self.conn, "SELECT name FROM users ORDER BY name", 2)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows, [("Ada",), ("Bob",)])

    def test_fetch_many_validation(self):
        with self.assertRaises(TypeError):
            fetch_many(self.conn, "SELECT 1", "2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            fetch_many(self.conn, "SELECT 1", -1)

    def test_executemany(self):
        executemany(
            self.conn,
            "INSERT INTO users (name, score) VALUES (?, ?)",
            [("Ada", 92.5), ("Bob", 87.0)],
        )
        rows = fetch_all(self.conn, "SELECT name FROM users ORDER BY name")
        self.assertEqual(rows, [("Ada",), ("Bob",)])

    def test_executemany_validation(self):
        with self.assertRaises(TypeError):
            executemany(self.conn, "SELECT 1", "not-a-list")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            executemany(self.conn, "SELECT 1", [123])  # type: ignore[arg-type]

    def test_query_dicts(self):
        insert_row(self.conn, "users", ["name", "score"], ["Ada", 92.5])
        rows = query(self.conn, "SELECT id, name, score FROM users")
        self.assertEqual(rows, [{"id": 1, "name": "Ada", "score": 92.5}])

    def test_query_no_rows(self):
        rows = query(self.conn, "SELECT name FROM users WHERE id = ?", [999])
        self.assertEqual(rows, [])

    def test_table_exists(self):
        self.assertTrue(table_exists(self.conn, "users"))
        self.assertFalse(table_exists(self.conn, "nonexistent"))

    def test_table_exists_validation(self):
        with self.assertRaises(TypeError):
            table_exists(self.conn, 1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            table_exists(self.conn, "")

    def test_create_table_validation(self):
        with self.assertRaises(TypeError):
            create_table(self.conn, 1, "x TEXT")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_table(self.conn, "", "x TEXT")
        with self.assertRaises(ValueError):
            create_table(self.conn, "t", "   ")

    def test_execute_validation(self):
        with self.assertRaises(TypeError):
            execute(None, "SELECT 1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            execute(self.conn, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            execute(self.conn, "SELECT 1", "params")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
