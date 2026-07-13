import sqlite3

DATABASE_NAME = "expenses.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def initialize_database(expenses):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()