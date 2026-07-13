import datetime
from display import print_expenses


def filter_by_category(expenses, category):
    return [
        exp
        for exp in expenses
        if exp["category"] == category
    ]


def filter_by_date(expenses, date):
    return [
        exp
        for exp in expenses
        if exp["date"] == date
    ]


def filter_by_description(expenses, description):
    return [
        exp
        for exp in expenses
        if description in exp["description"].lower()
    ]


def parse_date(date):
    date = date.strip()
    if not date:
        return datetime.date.today().strftime("%Y-%m-%d"), None
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return date, None
    except ValueError:
        return None, "Invalid format! Please use YYYY-MM-DD.\n"


def search_expenses(expenses):
    if not expenses:
            print("\nNo expenses to search.\n")
            return
    
    while True:
        print("\nSearch by:")
        print("1. Category")
        print("2. Date")
        print("3. Description")
        print("4. Back")
        choice = input("\nChoose an option: ")
        matching_expenses = []

        if choice == "1":
            category = input("\nEnter category: ").title()
            if not category:
                print("Search cannot be empty.")
                continue
            matching_expenses = filter_by_category(expenses, category)
        elif choice == "2":
            date = input("\nEnter date (YYYY-MM-DD, leave blank for today): ")
            date, error = parse_date(date)
            if error:
                print(error)
                continue 
            matching_expenses = filter_by_date(expenses, date)
        elif choice == "3":
            description = input("\nEnter keyword for description: ").lower()
            if not description:
                print("Search cannot be empty.")
                continue
            matching_expenses = filter_by_description(expenses, description)
        elif choice == "4":
            print()
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue
        
        if not matching_expenses:
            print("\nNo matching expenses found.\n")
        else:
            print_expenses(matching_expenses)
