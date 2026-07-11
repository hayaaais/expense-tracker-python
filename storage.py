import json

def read_expenses():
    try:
        with open("expenses.json", "r", encoding="utf-8") as file:
            return json.load(file)    
    except (FileNotFoundError, json.JSONDecodeError):
        print("File was missing or empty. Starting with a fresh empty list.")
        return []

def save_expenses(expenses):
    with open("expenses.json", "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)