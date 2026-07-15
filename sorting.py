from display import print_expenses


def sort_expenses(expenses, field, reverse):
    return sorted(expenses, key=lambda x: x[field], reverse=reverse)


def sorting_menu(expenses):
    if not expenses:
        print("No expenses found to sort.")
        return

    while True:
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
            print()
            break
        else:
            print("\nInvalid input! Going back now - Try again\n")
            continue

        sorted_expenses = sort_expenses(expenses, field, reverse)
        print_expenses(sorted_expenses)
