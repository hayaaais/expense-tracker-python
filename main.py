import datetime
from database import initialize_database
from storage import load_expenses, save_expenses, load_budget
from reports import show_reports, get_total_spent
from sorting import sorting_menu
from search import search_expenses
from budget import budgeting
from display import show_expenses, print_expenses


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


def add_expense(expenses):
    print()
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
    new_expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print("\nExpense added successfully!\n")


def delete_expense(expenses):
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


def show_total(expenses):
    total = get_total_spent(expenses)
    print(f"\nYour total is {total:.2f}₸\n")


def main():
    print("Expense Tracker")

    initialize_database()
    expenses = load_expenses()
    budget = load_budget()

    while True:
        show_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            show_expenses(expenses)
        
        elif choice == "3":
            delete_expense(expenses)

        elif choice == "4":
            show_total(expenses)

        elif choice == "5":
            search_expenses(expenses)

        elif choice == "6":
            show_reports(expenses)

        elif choice == "7":
            sorting_menu(expenses)

        elif choice == "8":
            budgeting(expenses, budget)

        elif choice == "9":
            print("\nExiting tracker. Goodbye!")
            break
        else:
            print("\nPlease choose option from 1 to 9\n")
            continue


if __name__ == "__main__":
    main()