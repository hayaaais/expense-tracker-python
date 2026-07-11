import datetime
from storage import read_expenses, save_expenses

print("Expense Tracker")

def show_menu():
    print("\n--- Menu ---")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Delete expense")
    print("4. Show total")
    print("5. Search expenses")
    print("6. Exit")

expenses = read_expenses()


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


def print_expenses(expenses):
    for index, exp in enumerate(expenses, 1):
            print(f"{index}. {exp['amount']}₸ | {exp['category']} - {exp['description']} | Date: {exp['date']}")
    print("")


def show_expenses():
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses found.")
    else:
        print_expenses(expenses)


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
    print(f"\nYour total is {total}₸\n")


def search_expenses():
    if not expenses:
        print("\nNo expenses to search.\n")
        return
    
    print("\nSearch by:")
    print("1. Category")
    print("2. Date")
    print("3. Description")
    print("4. Back")
    srch_expenses = []

    def find_expense(exp, field, value, partial_match):
        if partial_match:
            if value in exp[field].lower():
                srch_expenses.append(exp)
        else:
            if exp[field] == value:
                srch_expenses.append(exp)

    choice = input("\nChoose an option: ")

    if choice == "1":
        field = "category"
        partial_match = False
        value = input("\nEnter category: ").title()
    elif choice == "2":
        field = "date"
        partial_match = False
        value = input("\nEnter date (YYYY-MM-DD, leave blank for today): ").strip()
        if not value:
            value = datetime.date.today().strftime("%Y-%m-%d")
        else:
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                print("Invalid format! Please use YYYY-MM-DD.\n")
                return
    elif choice == "3":
        field = "description"
        partial_match = True
        value = input("\nEnter keyword for description: ").lower()
    elif choice == "4":
        return
    else:
        print("\nInvalid input! Going back now - Try again\n")
        return

    for exp in expenses:
        find_expense(exp, field, value, partial_match)

    if not srch_expenses:
        print("\nNo matching expenses found.\n")
    else:
        print_expenses(srch_expenses)


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
        search_expenses()

    elif choice == "6":
        print("\nExiting tracker. Goodbye!")
        break
    else:
        print("\nPlease choose option from 1 to 5\n")