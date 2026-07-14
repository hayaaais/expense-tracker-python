from display import print_expenses


def get_category_totals(expenses):
    totals = {}
    for exp in expenses:
        category = exp["category"]
        totals[category] = totals.get(category, 0) + exp["amount"]
    return dict(sorted(totals.items()))


def get_extreme_expenses(expenses, mode="highest"):
    if not expenses:
        return []
    reverse = (mode == "highest")
    sorted_expenses = sorted(expenses, key=lambda x: x["amount"], reverse=reverse)
    target_amount = sorted_expenses[0]["amount"]
    extreme_expenses = []
    for exp in sorted_expenses:
        if exp["amount"] == target_amount:
            extreme_expenses.append(exp)
        else:
            break
    return extreme_expenses

def get_total_spent(expenses):
    return sum(exp["amount"] for exp in expenses)


def get_average_expense(expenses):
    total = get_total_spent(expenses)
    count = len(expenses)
    return total / count if count > 0 else 0


def get_highest_amount(expenses):
    return max(exp["amount"] for exp in expenses)


def get_lowest_amount(expenses):
    return min(exp["amount"] for exp in expenses)


def get_summary(expenses):
    total_spent = get_total_spent(expenses)
    average = get_average_expense(expenses)
    highest_expense = get_highest_amount(expenses)
    lowest_expense = get_lowest_amount(expenses)
    return {
        "total_expenses": len(expenses),
        "total_spent": total_spent,
        "average_expense": average,
        "highest_expense": highest_expense,
        "lowest_expense": lowest_expense,
    }


def show_reports(expenses):
    if not expenses:
            print("No expenses recorded yet.")
            return
    
    while True:
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
            highest_expenses = get_extreme_expenses(expenses, mode="highest")
            print("\nHighest expense\n")
            print_expenses(highest_expenses)
        elif choice == "3":
            lowest_expenses = get_extreme_expenses(expenses, mode="lowest")
            print("\nLowest expense\n")
            print_expenses(lowest_expenses)
        elif choice == "4":
            average = get_average_expense(expenses)
            print("Average expense\n")
            print(f"Your average expense amount is: {average:.2f}₸\n")
        elif choice == "5":
            summary = get_summary(expenses)
            print("\nSummary\n")
            print(f"Total expenses: {summary['total_expenses']}")
            print(f"Total spent: {summary['total_spent']:.2f}₸")
            print(f"Average expense: {summary['average_expense']:.2f}₸")
            print(f"Highest expense: {summary['highest_expense']:.2f}₸")
            print(f"Lowest expense: {summary['lowest_expense']:.2f}₸\n")
        elif choice == "6":
            print()
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue