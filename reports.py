def get_category_totals(expenses):
    totals = {}
    for exp in expenses:
        category = exp["category"]
        totals[category] = totals.get(category, 0) + exp["amount"]
    return dict(sorted(totals.items()))


def print_extreme_expenses(expenses, mode="highest"):
    is_reverse = (mode == "highest")
    sorted_expenses = sorted(expenses, key=lambda x: x["amount"], reverse=is_reverse)
    target_amount = sorted_expenses[0]["amount"]
    print(f"\n{mode.title()} Expense(s)")
    for exp in sorted_expenses:
        if exp["amount"] == target_amount:
            print(f"{exp['amount']:.2f}₸ | {exp['category']} - {exp['description']} | Date: {exp['date']}")
        else:
            break
    print()


def get_total_spent(expenses):
    return sum(exp["amount"] for exp in expenses)


def get_average_expense(expenses):
    total = get_total_spent(expenses)
    count = len(expenses)
    return total / count if count > 0 else 0


def show_reports(expenses):
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
            print("Average expense\n")
            average = get_average_expense(expenses)
            print(f"Your average expense amount is: {average:.2f}₸")
            print()
        elif choice == "5":
            total_spent = get_total_spent(expenses)
            average = get_average_expense(expenses)
            highest_expense = max(exp["amount"] for exp in expenses)
            lowest_expense = min(exp["amount"] for exp in expenses)
            print("\nSummary\n")
            print(f"Total expenses: {len(expenses)}")
            print(f"Total spent: {total_spent:.2f}₸")
            print(f"Average expense: {average:.2f}₸")
            print(f"Highest expense: {highest_expense:.2f}₸")
            print(f"Lowest expense: {lowest_expense:.2f}₸\n")
        elif choice == "6":
            print()
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue