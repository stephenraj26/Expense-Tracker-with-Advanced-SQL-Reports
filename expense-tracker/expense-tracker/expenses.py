"""
expenses.py — CRUD operations for expense records
"""

from database import get_connection
from datetime import date


CATEGORIES = [
    "Food", "Transport", "Rent", "Utilities",
    "Healthcare", "Education", "Entertainment", "Shopping", "Other"
]


# ─────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────

def add_expense(expense_date: str, category: str, description: str, amount: float):
    """Insert a new expense record."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
        (expense_date, category.strip().title(), description.strip(), round(amount, 2))
    )
    conn.commit()
    eid = cur.lastrowid
    conn.close()
    print(f"\n  ✅ Expense added! ID: {eid} | ₹{amount:.2f} under '{category}'")


# ─────────────────────────────────────────────
# READ
# ─────────────────────────────────────────────

def view_all_expenses():
    """Display all expense records sorted by date descending."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n  ⚠️  No expenses recorded yet.")
        return

    _print_expense_table(rows)
    total = sum(r["amount"] for r in rows)
    print(f"  Total: ₹{total:.2f}")


def view_by_category(category: str):
    """Filter expenses by a specific category."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC",
        (category.strip().title(),)
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"\n  ⚠️  No expenses found under '{category}'.")
        return

    print(f"\n  Expenses for category: {category.title()}")
    _print_expense_table(rows)
    total = sum(r["amount"] for r in rows)
    print(f"  Category Total: ₹{total:.2f}")


def view_by_month(year_month: str):
    """Filter expenses by month. year_month format: YYYY-MM"""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ? ORDER BY date ASC",
        (year_month,)
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"\n  ⚠️  No expenses found for {year_month}.")
        return

    print(f"\n  Expenses for {year_month}:")
    _print_expense_table(rows)
    total = sum(r["amount"] for r in rows)
    print(f"  Month Total: ₹{total:.2f}")


# ─────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────

def update_expense(expense_id: int, amount: float, description: str):
    """Update amount and description of an existing expense."""
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cur.fetchone()

    if not row:
        print(f"\n  ⚠️  No expense found with ID {expense_id}.")
        conn.close()
        return

    cur.execute(
        "UPDATE expenses SET amount = ?, description = ? WHERE id = ?",
        (round(amount, 2), description.strip(), expense_id)
    )
    conn.commit()
    conn.close()
    print(f"\n  ✅ Expense #{expense_id} updated → ₹{amount:.2f} | '{description}'")


# ─────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────

def delete_expense(expense_id: int):
    """Delete an expense record after confirmation."""
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cur.fetchone()

    if not row:
        print(f"\n  ⚠️  No expense found with ID {expense_id}.")
        conn.close()
        return

    print(f"\n  Found: [{row['date']}] {row['category']} — {row['description']} — ₹{row['amount']:.2f}")
    confirm = input("  Delete this? (yes/no): ").strip().lower()
    if confirm == "yes":
        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        print("  ✅ Expense deleted.")
    else:
        print("  ❌ Deletion cancelled.")

    conn.close()


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def _print_expense_table(rows):
    print("\n" + "─" * 72)
    print(f"  {'ID':<5} {'Date':<12} {'Category':<15} {'Description':<22} {'Amount':>8}")
    print("─" * 72)
    for r in rows:
        desc = r["description"][:20] + ".." if len(r["description"]) > 20 else r["description"]
        print(f"  {r['id']:<5} {r['date']:<12} {r['category']:<15} {desc:<22} ₹{r['amount']:>7.2f}")
    print("─" * 72)
