"""
Expense Tracker with Advanced SQL Reports
Technologies: Python + SQLite + SQL
Author: Stephen Raj G
GitHub: github.com/stephenraj26
"""

from database import initialize_db
from expenses import (
    add_expense, view_all_expenses, view_by_category,
    view_by_month, update_expense, delete_expense, CATEGORIES
)
from reports import (
    report_category_breakdown, report_monthly_summary,
    report_monthly_by_category, report_top_expenses,
    report_budget_vs_actual
)
from budgets import set_budget, view_budgets
from datetime import date


# ─────────────────────────────────────────────
# INPUT HELPERS
# ─────────────────────────────────────────────

def get_valid_amount(prompt: str) -> float:
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return round(amount, 2)
            print("  ⚠️  Amount must be greater than 0.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


def get_valid_id(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  ⚠️  Please enter a valid integer ID.")


def get_valid_date(prompt: str) -> str:
    """Accept date in YYYY-MM-DD format or press Enter for today."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return str(date.today())
        try:
            # Validate by parsing
            parts = raw.split("-")
            if len(parts) == 3 and len(parts[0]) == 4:
                date(int(parts[0]), int(parts[1]), int(parts[2]))
                return raw
            raise ValueError
        except (ValueError, IndexError):
            print("  ⚠️  Invalid date. Use YYYY-MM-DD format or press Enter for today.")


def get_valid_month(prompt: str) -> str:
    """Accept month in YYYY-MM format."""
    while True:
        raw = input(prompt).strip()
        if len(raw) == 7 and raw[4] == "-":
            return raw
        print("  ⚠️  Use YYYY-MM format (e.g. 2025-06).")


def pick_category() -> str:
    """Let user pick from predefined categories."""
    print("\n  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        try:
            choice = int(input("  Pick category (number): "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print(f"  ⚠️  Enter a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


# ─────────────────────────────────────────────
# MENUS
# ─────────────────────────────────────────────

def print_main_menu():
    print("""
╔════════════════════════════════════════════╗
║      Expense Tracker — Main Menu           ║
╠════════════════════════════════════════════╣
║  EXPENSES                                  ║
║   1. Add Expense                           ║
║   2. View All Expenses                     ║
║   3. Filter by Category                    ║
║   4. Filter by Month                       ║
║   5. Update Expense                        ║
║   6. Delete Expense                        ║
╠════════════════════════════════════════════╣
║  REPORTS                                   ║
║   7. Category-wise Breakdown               ║
║   8. Monthly Summary                       ║
║   9. Monthly Breakdown by Category         ║
║  10. Top 5 Highest Expenses                ║
║  11. Budget vs Actual                      ║
╠════════════════════════════════════════════╣
║  BUDGETS                                   ║
║  12. Set Category Budget                   ║
║  13. View All Budgets                      ║
╠════════════════════════════════════════════╣
║   0. Exit                                  ║
╚════════════════════════════════════════════╝
""")


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────

def main():
    initialize_db()
    print("\n  ✅ Expense Tracker ready. DB: expenses.db")

    while True:
        print_main_menu()
        choice = input("  Enter your choice: ").strip()

        # ── EXPENSES ──────────────────────────
        if choice == "1":
            print("\n  -- Add New Expense --")
            exp_date    = get_valid_date("  Date (YYYY-MM-DD) [Enter = today]: ")
            category    = pick_category()
            description = input("  Description: ").strip()
            amount      = get_valid_amount("  Amount (₹): ")
            if description:
                add_expense(exp_date, category, description, amount)
            else:
                print("  ⚠️  Description cannot be empty.")

        elif choice == "2":
            view_all_expenses()

        elif choice == "3":
            category = pick_category()
            view_by_category(category)

        elif choice == "4":
            ym = get_valid_month("\n  Enter month (YYYY-MM): ")
            view_by_month(ym)

        elif choice == "5":
            eid         = get_valid_id("\n  Enter Expense ID to update: ")
            new_amount  = get_valid_amount("  New Amount (₹): ")
            new_desc    = input("  New Description: ").strip()
            if new_desc:
                update_expense(eid, new_amount, new_desc)
            else:
                print("  ⚠️  Description cannot be empty.")

        elif choice == "6":
            eid = get_valid_id("\n  Enter Expense ID to delete: ")
            delete_expense(eid)

        # ── REPORTS ───────────────────────────
        elif choice == "7":
            report_category_breakdown()

        elif choice == "8":
            report_monthly_summary()

        elif choice == "9":
            ym = get_valid_month("\n  Enter month (YYYY-MM): ")
            report_monthly_by_category(ym)

        elif choice == "10":
            report_top_expenses(limit=5)

        elif choice == "11":
            ym = get_valid_month("\n  Enter month for budget check (YYYY-MM): ")
            report_budget_vs_actual(ym)

        # ── BUDGETS ───────────────────────────
        elif choice == "12":
            print("\n  -- Set Monthly Budget --")
            category = pick_category()
            limit    = get_valid_amount(f"  Monthly limit for '{category}' (₹): ")
            set_budget(category, limit)

        elif choice == "13":
            view_budgets()

        elif choice == "0":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("\n  ⚠️  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
