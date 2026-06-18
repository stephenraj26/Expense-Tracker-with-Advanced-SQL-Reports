"""
budgets.py — Set and view monthly budget limits per category
"""

from database import get_connection
from expenses import CATEGORIES


def set_budget(category: str, limit: float):
    """Insert or update a monthly budget limit for a category."""
    conn = get_connection()
    cur  = conn.cursor()
    # INSERT OR REPLACE handles both new and existing budgets
    cur.execute(
        "INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
        (category.strip().title(), round(limit, 2))
    )
    conn.commit()
    conn.close()
    print(f"\n  ✅ Budget set: ₹{limit:.2f}/month for '{category}'")


def view_budgets():
    """Display all set budget limits."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM budgets ORDER BY category ASC")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n  ⚠️  No budgets set yet.")
        return

    print("\n  Monthly Budget Limits:")
    print("  " + "─" * 35)
    print(f"  {'Category':<18} {'Limit':>10}")
    print("  " + "─" * 35)
    for r in rows:
        print(f"  {r['category']:<18} ₹{r['monthly_limit']:>9.2f}")
    print("  " + "─" * 35)
