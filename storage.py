import json


def load_expenses():
    try:
        with open("expenses.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Storage file not found or invalid. Starting with empty data.")
        return []


def save_expenses(expenses):
    with open("expenses.json", "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)


def load_budget():
    try:
        with open("budget.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Storage file not found or invalid. Starting with empty data.")
        return {}


def save_budget(budget):
    with open("budget.json", "w", encoding="utf-8") as file:
        json.dump(budget, file, indent=4, ensure_ascii=False)
