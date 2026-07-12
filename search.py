import datetime
from main import print_expenses

def find_expense(exp, field, value, partial_match, srch_expenses):
            if partial_match:
                if value in exp[field].lower():
                    srch_expenses.append(exp)
            else:
                if exp[field] == value:
                    srch_expenses.append(exp)

def search_expenses(expenses):
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
            print()
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue

        if not value:
            print("Search cannot be empty.")
            return
        else:
            for exp in expenses:
                find_expense(exp, field, value, partial_match, srch_expenses)

        if not srch_expenses:
            print("\nNo matching expenses found.\n")
        else:
            print_expenses(srch_expenses)
