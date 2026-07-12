def print_expenses(expenses):
    for index, exp in enumerate(expenses, 1):
            print(f"{index}. {exp['amount']}₸ | {exp['category']} - {exp['description']} | Date: {exp['date']}")
    print("")


def show_expenses(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses found.")
    else:
        print_expenses(expenses)