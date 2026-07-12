import json
from storage import read_expenses

expenses = read_expenses()

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
            total_spent = get_total_spent(expenses)
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

def get_total_spent(expenses):
    return sum(exp["amount"] for exp in expenses)