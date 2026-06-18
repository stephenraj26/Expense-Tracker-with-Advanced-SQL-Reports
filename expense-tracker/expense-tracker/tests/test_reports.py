"""
test_reports.py — Tests for SQL report logic
"""

import sys, os, sqlite3, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database

TEST_DB = "test_expenses.db"


def make_conn():
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    return conn


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def seed(conn, rows):
    conn.executemany(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?,?,?,?)",
        rows
    )
    conn.commit()


# ── Tests ────────────────────────────────────

def test_category_group_by():
    """GROUP BY category returns correct totals."""
    conn = make_conn()
    seed(conn, [
        ("2025-06-01", "Food",      "Lunch",   200),
        ("2025-06-02", "Food",      "Dinner",  350),
        ("2025-06-03", "Transport", "Bus",       50),
    ])
    cur = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses GROUP BY category ORDER BY total DESC
    """)
    rows = cur.fetchall()
    assert rows[0]["category"] == "Food"
    assert rows[0]["total"]    == 550
    assert rows[1]["category"] == "Transport"
    assert rows[1]["total"]    == 50
    conn.close()


def test_monthly_summary():
    """strftime GROUP BY month works correctly."""
    conn = make_conn()
    seed(conn, [
        ("2025-06-01", "Food",      "June entry",  100),
        ("2025-06-15", "Rent",      "June rent",  5000),
        ("2025-07-01", "Food",      "July entry",  200),
    ])
    cur = conn.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
        FROM expenses GROUP BY month ORDER BY month
    """)
    rows = cur.fetchall()
    assert rows[0]["month"] == "2025-06"
    assert rows[0]["total"] == 5100
    assert rows[1]["month"] == "2025-07"
    assert rows[1]["total"] == 200
    conn.close()


def test_top_expenses():
    """ORDER BY amount DESC LIMIT returns highest entries."""
    conn = make_conn()
    seed(conn, [
        ("2025-06-01", "Rent",          "Rent",     8000),
        ("2025-06-02", "Shopping",      "Laptop",  45000),
        ("2025-06-03", "Food",          "Party",    2000),
        ("2025-06-04", "Entertainment", "Concert",  1500),
        ("2025-06-05", "Healthcare",    "Doctor",    800),
        ("2025-06-06", "Transport",     "Cab",       300),
    ])
    cur = conn.execute("""
        SELECT amount FROM expenses ORDER BY amount DESC LIMIT 3
    """)
    rows = cur.fetchall()
    assert rows[0]["amount"] == 45000
    assert rows[1]["amount"] == 8000
    assert rows[2]["amount"] == 2000
    conn.close()


def test_monthly_category_filter():
    """WHERE month filter + GROUP BY category returns correct data."""
    conn = make_conn()
    seed(conn, [
        ("2025-06-01", "Food",      "Lunch",   200),
        ("2025-06-10", "Food",      "Dinner",  300),
        ("2025-06-15", "Transport", "Bus",       50),
        ("2025-07-01", "Food",      "July",    999),  # should NOT appear
    ])
    cur = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE strftime('%Y-%m', date) = '2025-06'
        GROUP BY category ORDER BY total DESC
    """)
    rows = cur.fetchall()
    assert len(rows) == 2
    assert rows[0]["category"] == "Food"
    assert rows[0]["total"]    == 500
    conn.close()


def test_empty_table_returns_no_rows():
    """Reports on empty DB return empty result set."""
    conn = make_conn()
    cur = conn.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    assert cur.fetchall() == []
    conn.close()
