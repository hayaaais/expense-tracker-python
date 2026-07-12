import datetime
from storage import read_expenses, save_expenses, load_budget, save_budget
from reports import show_reports, get_total_spent, get_category_totals
from sorting import sorting
from search import search_expenses
from budget import budgeting
from display import show_expenses, print_expenses

print("Expense Tracker")

def show_menu():
    print("\n--- Menu ---")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Delete expense")
    print("4. Show total")
    print("5. Search expenses")
    print("6. Reports")
    print("7. Sorting")
    print("8. Budget")
    print("9. Exit")

expenses = read_expenses()
budget = load_budget()

def add_expense():
    print("")
    while True:
        try:
            amount = float(input("Amount: "))
            if amount < 0:
                print("Amount cannot be negative. Please try again.\n")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.\n")
    while True:
        category = input("Category: ").strip().title()
        if not category:
            print("Category cannot be empty! Please write something.\n")
            continue
        break
    while True:
        description = input("Description: ").strip().capitalize()
        if not description:
            print("Description cannot be empty! Please write something.\n")
            continue
        break
    while True:
        date = input("Date (YYYY-MM-DD, leave blank for today): ").strip()
        if not date:
            date = datetime.date.today().strftime("%Y-%m-%d")
            break
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid format! Please use YYYY-MM-DD.\n")
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("\nExpense added successfully!\n")

def delete_expense():
    print("\n--- Delete Expense ---")
    if not expenses:
        print("No expenses to delete.\n")
    else:
        print_expenses(expenses)
        while True:
            try:
                num = int(input("Enter the number to delete: ")) - 1
                if 0 <= num < len(expenses):
                    del expenses[num]
                    save_expenses(expenses)
                    print("\nExpense was deleted successfully!\n")
                    break
                else:
                    print("Invalid number. Choose an item from the list.\n")
            except ValueError:
                print("Please enter a valid number.\n")

def show_total():
    total = sum(exp['amount'] for exp in expenses)
    print(f"\nYour total is {total:.2f}₸\n")


while True:
    show_menu()

    choice = input("\nChoose an option: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        show_expenses()
    
    elif choice == "3":
        delete_expense()

    elif choice == "4":
        show_total()

    elif choice == "5":
        search_expenses(expenses)

    elif choice == "6":
        show_reports(expenses)

    elif choice == "7":
        sorting(expenses)

    elif choice == "8":
        budgeting(expenses, budget)

    elif choice == "9":
        print("\nExiting tracker. Goodbye!")
        break
    else:
        print("\nPlease choose option from 1 to 9\n")
        continue
