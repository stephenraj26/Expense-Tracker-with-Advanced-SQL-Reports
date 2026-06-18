# Expense Tracker with Advanced SQL Reports

A command-line expense tracking application built with **Python** and **SQLite**.  
Features full CRUD operations, category-wise and monthly reports using advanced SQL aggregations, and monthly budget tracking.

---

## Features

- **Add** expenses with date, category, description, and amount
- **View** all expenses in a formatted table
- **Filter** by category or by month
- **Update** and **Delete** expense records
- **5 Advanced SQL Reports** using `GROUP BY`, `SUM`, `AVG`, `COUNT`, `MAX`
- **Budget Management** — set monthly limits per category
- **Budget vs Actual** — see where you're overspending
- **Input Validation** — handles invalid dates, amounts, and IDs

---

## Reports

| # | Report | SQL Used |
|---|--------|----------|
| 1 | Category-wise Breakdown | `GROUP BY category` + `SUM`, `AVG`, `MAX` |
| 2 | Monthly Summary | `strftime()` + `GROUP BY` + `SUM` |
| 3 | Monthly Breakdown by Category | `WHERE` + `GROUP BY` + `SUM` |
| 4 | Top 5 Highest Expenses | `ORDER BY amount DESC` + `LIMIT` |
| 5 | Budget vs Actual | `LEFT JOIN` + `GROUP BY` + `COALESCE` |

---

## Tech Stack

| Layer    | Technology        |
|----------|-------------------|
| Language | Python 3.x        |
| Database | SQLite (built-in) |
| Testing  | pytest            |

---

## Project Structure

```
expense-tracker/
│
├── main.py          # Entry point — menu loop (13 options)
├── database.py      # DB connection and schema (expenses + budgets tables)
├── expenses.py      # CRUD operations
├── reports.py       # 5 advanced SQL report functions
├── budgets.py       # Budget set/view operations
├── requirements.txt
├── .gitignore
│
└── tests/
    └── test_reports.py   # 5 SQL logic tests
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/stephenraj26/expense-tracker.git
cd expense-tracker
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

A `expenses.db` file will be created automatically on first run.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## Sample Report Output

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    CATEGORY-WISE BREAKDOWN                          │
  ├─────────────────────────────────────────────────────────────────────┤
  │ Category       Txns      Total  Avg/Entry    Highest   % Share │
  ├─────────────────────────────────────────────────────────────────────┤
  │ Rent              1  ₹8000.00  ₹8000.00   ₹8000.00    53.2% │
  │ Food              3  ₹4500.00  ₹1500.00   ₹2500.00    29.9% │
  │ Transport         2  ₹2500.00  ₹1250.00   ₹2000.00    16.6% │
  ├─────────────────────────────────────────────────────────────────────┤
  │ GRAND TOTAL       │ ₹15000.00                                       │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## Author

**Stephen Raj G**  
BCA Graduate — DRBCCC Hindu College, University of Madras  
[GitHub](https://github.com/stephenraj26) · [LinkedIn](https://linkedin.com/in/stephen-raj-g)
