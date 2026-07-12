import json
import datetime
from main import print_expenses
from reports import get_total_spent
from storage import save_budget

def get_monthly_expenses(month, expenses):
    monthly_expenses = []
    for exp in expenses:
        if exp["date"][:7] == month:
            monthly_expenses.append(exp)
    return get_total_spent(monthly_expenses)


def budgeting(expenses, budget):
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