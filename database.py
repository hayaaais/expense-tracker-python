import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget (
                month TEXT PRIMARY KEY,
                amount REAL NOT NULL
            )
        """)


def load_expenses() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, amount, category, description, date FROM expenses")

        rows = cursor.fetchall()
        expenses = [
            {
                "id": row[0],
                "amount": row[1],
                "category": row[2],
                "description": row[3],
                "date": row[4],
            }
            for row in rows
        ]
        return expenses


def insert_expense(expense: dict) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (
                expense["amount"],
                expense["category"],
                expense["description"],
                expense["date"],
            ),
        )


def delete_expense(expense_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        if cursor.rowcount == 0:
            return False
        return True


def load_budget() -> dict[str, float]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT month, amount FROM budget")

        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}


def save_budget(month: str, amount: float) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO budget (month, amount) VALUES (?, ?)",
            (month, amount),
        )
