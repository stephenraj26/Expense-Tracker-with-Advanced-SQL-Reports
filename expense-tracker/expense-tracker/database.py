"""
database.py — DB connection and schema setup
"""

import sqlite3

DB_NAME = "expenses.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cur  = conn.cursor()

    # Main expenses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT    NOT NULL,          -- stored as YYYY-MM-DD
            category    TEXT    NOT NULL,
            description TEXT    NOT NULL,
            amount      REAL    NOT NULL CHECK(amount > 0)
        )
    """)

    # Optional: category budget limits table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category    TEXT PRIMARY KEY,
            monthly_limit REAL NOT NULL CHECK(monthly_limit > 0)
        )
    """)

    conn.commit()
    conn.close()
