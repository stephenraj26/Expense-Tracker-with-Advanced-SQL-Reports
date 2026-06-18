"""
reports.py — Advanced SQL Reports using GROUP BY and aggregate functions

This is the core module that makes this project stand out.
All reports use raw SQL with GROUP BY, SUM, AVG, COUNT, MAX.
"""

from database import get_connection


# ─────────────────────────────────────────────
# REPORT 1: Category-wise Breakdown
# ─────────────────────────────────────────────

def report_category_breakdown():
    """
    Total spending per category, sorted highest to lowest.
    SQL: GROUP BY category + SUM(amount)
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT
            category,
            COUNT(*)        AS transactions,
            SUM(amount)     AS total,
            AVG(amount)     AS avg_per_entry,
            MAX(amount)     AS highest_single
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n  ⚠️  No data available.")
        return

    grand_total = sum(r["total"] for r in rows)

    print("\n  ┌─────────────────────────────────────────────────────────────────────┐")
    print("  │                    CATEGORY-WISE BREAKDOWN                          │")
    print("  ├─────────────────────────────────────────────────────────────────────┤")
    print(f"  │ {'Category':<14} {'Txns':>5} {'Total':>10} {'Avg/Entry':>10} {'Highest':>10} {'% Share':>8} │")
    print("  ├─────────────────────────────────────────────────────────────────────┤")
    for r in rows:
        share = (r["total"] / grand_total * 100) if grand_total else 0
        print(
            f"  │ {r['category']:<14} {r['transactions']:>5} "
            f"₹{r['total']:>9.2f} ₹{r['avg_per_entry']:>9.2f} "
            f"₹{r['highest_single']:>9.2f} {share:>7.1f}% │"
        )
    print("  ├─────────────────────────────────────────────────────────────────────┤")
    print(f"  │ {'GRAND TOTAL':<14} {'':>5} ₹{grand_total:>9.2f}{'':>33}│")
    print("  └─────────────────────────────────────────────────────────────────────┘")


# ─────────────────────────────────────────────
# REPORT 2: Monthly Summary
# ─────────────────────────────────────────────

def report_monthly_summary():
    """
    Total spending per month, with transaction count and daily average.
    SQL: strftime() + GROUP BY + SUM + AVG
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT
            strftime('%Y-%m', date)  AS month,
            COUNT(*)                 AS transactions,
            SUM(amount)              AS total,
            AVG(amount)              AS avg_per_entry,
            MAX(amount)              AS highest
        FROM expenses
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n  ⚠️  No data available.")
        return

    print("\n  ┌──────────────────────────────────────────────────────────┐")
    print("  │                  MONTHLY EXPENSE SUMMARY                 │")
    print("  ├──────────────────────────────────────────────────────────┤")
    print(f"  │ {'Month':<10} {'Txns':>5} {'Total':>10} {'Avg/Entry':>10} {'Highest':>10} │")
    print("  ├──────────────────────────────────────────────────────────┤")
    for r in rows:
        print(
            f"  │ {r['month']:<10} {r['transactions']:>5} "
            f"₹{r['total']:>9.2f} ₹{r['avg_per_entry']:>9.2f} "
            f"₹{r['highest']:>9.2f} │"
        )
    print("  └──────────────────────────────────────────────────────────┘")


# ─────────────────────────────────────────────
# REPORT 3: Monthly + Category Cross Report
# ─────────────────────────────────────────────

def report_monthly_by_category(year_month: str):
    """
    For a given month, show spending broken down by category.
    SQL: WHERE + GROUP BY category + SUM
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT
            category,
            COUNT(*)    AS transactions,
            SUM(amount) AS total
        FROM expenses
        WHERE strftime('%Y-%m', date) = ?
        GROUP BY category
        ORDER BY total DESC
    """, (year_month,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"\n  ⚠️  No data for {year_month}.")
        return

    month_total = sum(r["total"] for r in rows)

    print(f"\n  Category Breakdown for {year_month}:")
    print("  " + "─" * 48)
    print(f"  {'Category':<15} {'Txns':>5} {'Total':>10} {'% Share':>8}")
    print("  " + "─" * 48)
    for r in rows:
        share = (r["total"] / month_total * 100) if month_total else 0
        print(f"  {r['category']:<15} {r['transactions']:>5} ₹{r['total']:>9.2f} {share:>7.1f}%")
    print("  " + "─" * 48)
    print(f"  {'TOTAL':<15} {'':>5} ₹{month_total:>9.2f}")


# ─────────────────────────────────────────────
# REPORT 4: Top 5 Highest Expenses
# ─────────────────────────────────────────────

def report_top_expenses(limit: int = 5):
    """
    Show the N highest single expenses.
    SQL: ORDER BY amount DESC + LIMIT
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT id, date, category, description, amount
        FROM expenses
        ORDER BY amount DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n  ⚠️  No data available.")
        return

    print(f"\n  Top {limit} Highest Expenses:")
    print("  " + "─" * 65)
    print(f"  {'Rank':<5} {'Date':<12} {'Category':<14} {'Description':<18} {'Amount':>8}")
    print("  " + "─" * 65)
    for i, r in enumerate(rows, 1):
        desc = r["description"][:16] + ".." if len(r["description"]) > 16 else r["description"]
        print(f"  #{i:<4} {r['date']:<12} {r['category']:<14} {desc:<18} ₹{r['amount']:>7.2f}")
    print("  " + "─" * 65)


# ─────────────────────────────────────────────
# REPORT 5: Budget vs Actual (if budgets set)
# ─────────────────────────────────────────────

def report_budget_vs_actual(year_month: str):
    """
    Compare budget limits against actual spending for a month.
    SQL: LEFT JOIN + GROUP BY + SUM
    """
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT
            b.category,
            b.monthly_limit,
            COALESCE(SUM(e.amount), 0)  AS spent,
            b.monthly_limit - COALESCE(SUM(e.amount), 0) AS remaining
        FROM budgets b
        LEFT JOIN expenses e
            ON b.category = e.category
            AND strftime('%Y-%m', e.date) = ?
        GROUP BY b.category
        ORDER BY spent DESC
    """, (year_month,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\n  ⚠️  No budgets set yet. Use option 8 to set budgets.")
        return

    print(f"\n  Budget vs Actual — {year_month}:")
    print("  " + "─" * 62)
    print(f"  {'Category':<14} {'Budget':>10} {'Spent':>10} {'Remaining':>10} {'Status'}")
    print("  " + "─" * 62)
    for r in rows:
        status = "⚠️  OVER" if r["remaining"] < 0 else "✅ OK"
        print(
            f"  {r['category']:<14} ₹{r['monthly_limit']:>9.2f} "
            f"₹{r['spent']:>9.2f} ₹{r['remaining']:>9.2f}  {status}"
        )
    print("  " + "─" * 62)
