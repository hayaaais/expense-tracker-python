import datetime
from storage import read_expenses, save_expenses, load_budget, save_budget
from reports import show_reports, get_total_spent, get_category_totals
from sorting import sorting
from search import search_expenses

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
    print(f"\nYour total is {total:.2f}₸\n")


def get_monthly_expenses(month):
    monthly_expenses = []
    for exp in expenses:
        if exp["date"][:7] == month:
            monthly_expenses.append(exp)
    return get_total_spent(monthly_expenses)


def budgeting():
    while True:
        if not expenses:
            print("No expenses found for budgeting.")
            return
        
        print("\nBudgeting")
        print("1. Set monthly budget")
        print("2. View current budget")
        print("3. Remaining budget")
        print("4. Percentage used")
        print("5. Warning when exceeded")
        print("6. Back")
        choice = input("\nChoose an option: ")

        if choice == "1":
            while True:
                try:
                    budget_data = float(input("\nBudget: "))
                    if budget_data < 0:
                        print("Budget cannot be negative. Please try again.\n")
                        continue
                    break
                except ValueError:
                    print("Invalid input! Please enter a valid number.\n")
            global budget
            budget = {"monthly_budget": budget_data}
            save_budget(budget)
            print("\nBudget set successfully!\n")
        elif choice == "2":
            print(f"\nCurrent monthly budget: {budget.get('monthly_budget', 0):.2f}₸\n")
        elif choice == "3":
            current_month = datetime.date.today().strftime("%Y-%m")
            total_spent = get_monthly_expenses(current_month)
            remaining_budget = budget.get('monthly_budget', 0) - total_spent
            print(f"\nRemaining budget: {remaining_budget:.2f}₸\n")
        elif choice == "4":
            current_month = datetime.date.today().strftime("%Y-%m")
            total_spent = get_monthly_expenses(current_month)
            monthly_budget = budget.get('monthly_budget', 0)
            if monthly_budget > 0:
                percentage_used = (total_spent / monthly_budget) * 100
                print(f"\nPercentage of budget used: {percentage_used:.2f}%\n")
            else:
                print("\nNo budget set. Please set a monthly budget first.\n")
        elif choice == "5":
            current_month = datetime.date.today().strftime("%Y-%m")
            total_spent = get_monthly_expenses(current_month)
            monthly_budget = budget.get('monthly_budget', 0)
            if monthly_budget > 0:
                if total_spent > monthly_budget:
                    exceeded_amount = total_spent - monthly_budget
                    print(f"\n⚠ Budget exceeded by {exceeded_amount:.2f}₸\n")
                else:
                    print("\nYou are within your budget.\n")
            else:
                print("\nNo budget set. Please set a monthly budget first.\n")
        elif choice == "6":
            print()
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue


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
        sorting()

    elif choice == "8":
        budgeting()

    elif choice == "9":
        print("\nExiting tracker. Goodbye!")
        break
    else:
        print("\nPlease choose option from 1 to 9\n")
        continue
