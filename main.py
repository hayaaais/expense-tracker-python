import datetime
from storage import read_expenses, save_expenses, load_budget, save_budget

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
    print("8. Exit")

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


def search_expenses():
    def find_expense(exp, field, value, partial_match):
            if partial_match:
                if value in exp[field].lower():
                    srch_expenses.append(exp)
            else:
                if exp[field] == value:
                    srch_expenses.append(exp)

    while True:
        if not expenses:
            print("\nNo expenses to search.\n")
            return
        
        print("\nSearch by:")
        print("1. Category")
        print("2. Date")
        print("3. Description")
        print("4. Back")
        choice = input("\nChoose an option: ")
        srch_expenses = []

        if choice == "1":
            field, partial_match = "category", False
            value = input("\nEnter category: ").title()
        elif choice == "2":
            field, partial_match = "date", False
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
            field, partial_match = "description", True
            value = input("\nEnter keyword for description: ").lower()
        elif choice == "4":
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue

        if not value:
            print("Search cannot be empty.")
            return
        else:
            for exp in expenses:
                find_expense(exp, field, value, partial_match)

        if not srch_expenses:
            print("\nNo matching expenses found.\n")
        else:
            print_expenses(srch_expenses)


def get_category_totals(expenses):
    totals_dict = {}
    available_categories = set(exp["category"] for exp in expenses)
    for ctg in sorted(available_categories):
        ctg_list = []
        for exp in expenses:
            if exp["category"] == ctg:
                ctg_list.append(exp)
        if ctg_list:
            category_total = sum(exp['amount'] for exp in ctg_list)
            totals_dict[ctg] = category_total
    return totals_dict


def show_reports():
    def print_extreme_expenses(expenses, mode="highest"):
        is_reverse = True if mode == "highest" else False
        sorted_expenses = sorted(expenses, key=lambda x: x["amount"], reverse=is_reverse)
        target_amount = sorted_expenses[0]["amount"]
        print(f"\n{mode.title()} Expense(s)")
        for exp in sorted_expenses:
            if exp["amount"] == target_amount:
                print(f"{exp['amount']}₸\n{exp['category']}\n{exp['description']}\n{exp['date']}\n---")
            else:
                break

    while True:
        if not expenses:
            print("No expenses recorded yet.")
            return

        print("\nReports")
        print("1. Spending by category")
        print("2. Highest expense")
        print("3. Lowest expense")
        print("4. Average expense")
        print("5. Expense summary")
        print("6. Back")
        choice = input("\nChoose an option: ")

        if choice == "1":
            print("\nSpending by category\n")
            category_data = get_category_totals(expenses)
            for ctg, total in category_data.items():
                print(f"{ctg.ljust(15, '.')} {total:.2f}₸")
            print()        
        elif choice == "2":
            print_extreme_expenses(expenses, mode="highest")
        elif choice == "3":
            print_extreme_expenses(expenses, mode="lowest")
        elif choice == "4":
            print("\nAverage expense\n")
            total_spent = sum(exp['amount'] for exp in expenses)
            average = total_spent / len(expenses)
            print(f"Your average expense amount is: {average:.2f}₸")
        elif choice == "5":
            total_spent = sum(exp['amount'] for exp in expenses)
            average = total_spent / len(expenses)
            highest_expense = max(exp["amount"] for exp in expenses)
            lowest_expense = min(exp["amount"] for exp in expenses)
            print("\nSummary\n")
            print(f"Total expenses: {len(expenses)}\n")
            print(f"Total spent: {total_spent}₸\n")
            print(f"Average expense: {average}₸\n")
            print(f"Highest expense: {highest_expense}₸\n")
            print(f"Lowest expense: {lowest_expense}₸\n")
        elif choice == "6":
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue


def sorting():
    def sort_expenses(expenses, field, reverse):
            return sorted(expenses, key=lambda x: x[field], reverse=reverse)
    
    while True:
        if not expenses:
            print("No expenses found to sort.")
            return
        
        print("\nSorting")
        print("1. Amount ↑")
        print("2. Amount ↓")
        print("3. Date ↑")
        print("4. Date ↓")
        print("5. Category")
        print("6. Description (A–Z)")
        print("7. Back")
        choice = input("\nChoose an option: ")

        if choice == "1":
            field, reverse = "amount", False
        elif choice == "2":
            field, reverse = "amount", True
        elif choice == "3":
            field, reverse = "date", False
        elif choice == "4":
            field, reverse = "date", True
        elif choice == "5":
            field, reverse = "category", False
        elif choice == "6":
            field, reverse = "description", False
        elif choice == "7":
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue
        
        sorted_expenses = sort_expenses(expenses, field, reverse)
        print_expenses(sorted_expenses)


def budgeting():
    while True:
        if not expenses:
            print("No expenses found for budgeting.")
            return
        
        print("\nBudget\n")
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
                    budget_data = float(input("Budget: "))
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
            total_spent = sum(exp['amount'] for exp in expenses)
            remaining_budget = budget.get('monthly_budget', 0) - total_spent
            print(f"\nRemaining budget: {remaining_budget:.2f}₸\n")
        elif choice == "4":
            total_spent = sum(exp['amount'] for exp in expenses)
            monthly_budget = budget.get('monthly_budget', 0)
            if monthly_budget > 0:
                percentage_used = (total_spent / monthly_budget) * 100
                print(f"\nPercentage of budget used: {percentage_used:.2f}%\n")
            else:
                print("\nNo budget set. Please set a monthly budget first.\n")
        elif choice == "5":
            total_spent = sum(exp['amount'] for exp in expenses)
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
        search_expenses()

    elif choice == "6":
        show_reports()

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
