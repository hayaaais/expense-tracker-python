import datetime
from reports import get_total_spent
from database import save_budget


def get_monthly_expenses(month, expenses):
    monthly_expenses = [exp for exp in expenses if exp["date"][:7] == month]
    return get_total_spent(monthly_expenses)


def get_current_month_total(expenses):
    current_month = datetime.date.today().strftime("%Y-%m")
    return get_monthly_expenses(current_month, expenses)


def calculate_remaining_budget(budget, expenses):
    total_spent = get_current_month_total(expenses)
    return budget.get('monthly_budget', 0) - total_spent


def calculate_budget_percentage(monthly_budget, expenses):
    total_spent = get_current_month_total(expenses)
    if monthly_budget > 0:
        return (total_spent / monthly_budget) * 100
    return None
    

def calculate_budget_excess(monthly_budget, expenses):
    total_spent = get_current_month_total(expenses)
    if total_spent > monthly_budget:
        return total_spent - monthly_budget
    return 0


def _prompt_budget_input():
    current_month = datetime.date.today().strftime("%Y-%m")
    while True:
        try:
            budget_data = float(input("\nBudget: "))
            if budget_data < 0:
                print("Budget cannot be negative. Please try again.\n")
                continue
            return current_month, budget_data
        except ValueError:
            print("Invalid input! Please enter a valid number.\n")


def budgeting(expenses, budget):
    if not expenses:
        print("No expenses found for budgeting.")
        return
    
    while True:
        monthly_budget = budget.get("monthly_budget", 0)

        print("\nBudgeting")
        print("1. Set monthly budget")
        print("2. View current budget")
        print("3. Remaining budget")
        print("4. Percentage used")
        print("5. Warning when exceeded")
        print("6. Back")
        choice = input("\nChoose an option: ")

        if choice == "1":
            current_month, budget_data = _prompt_budget_input()
            save_budget(current_month, budget_data)
            print("\nBudget set successfully!\n")
            
        elif choice == "2":
            print(f"\nCurrent monthly budget: {monthly_budget:.2f}₸\n")

        elif choice == "3":
            remaining_budget = calculate_remaining_budget(budget, expenses)
            print(f"\nRemaining budget: {remaining_budget:.2f}₸\n")

        elif choice == "4":
            if monthly_budget > 0:
                percentage_used = calculate_budget_percentage(monthly_budget, expenses)
                print(f"\nPercentage of budget used: {percentage_used:.2f}%\n")
            else:
                print("\nNo budget set. Please set a monthly budget first.\n")

        elif choice == "5":
            if monthly_budget > 0:
                exceeded_amount = calculate_budget_excess(monthly_budget, expenses)
                if exceeded_amount > 0:
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