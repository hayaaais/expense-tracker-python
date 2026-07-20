import datetime
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from database import initialize_database, load_expenses, insert_expense, delete_expense, save_budget, load_budget
from reports import get_category_totals, get_extreme_expenses, get_average_expense, get_summary, get_total_spent
from budget import calculate_remaining_budget, calculate_budget_percentage, calculate_budget_excess, get_expenses_by_month
from sorting import sort_expenses
from search import filter_by_category, filter_by_date, filter_by_description


app = FastAPI()
initialize_database()

class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1) 
    description: str = Field(min_length=1) 
    date: str | None = None 


@app.get("/expenses")
def get_all_expenses():
    return load_expenses()

@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseIn):
    date = expense.date or datetime.date.today().strftime("%Y-%m-%d")

    new_expense = {
        "amount": expense.amount,
        "category": expense.category.strip().title(),
        "description": expense.description.strip().capitalize(),
        "date": date,
    }
    insert_expense(new_expense)
    return new_expense

@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int):
    result = delete_expense(expense_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Expense deleted successfully."}


@app.get("/reports/categories")
def calculate_category_totals():
    expenses = load_expenses()
    return get_category_totals(expenses)

@app.get("/reports/extreme")
def calculate_extreme_expenses(mode: str = "highest"):
    expenses = load_expenses()
    if mode not in {"highest", "lowest"}:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'highest' or 'lowest'.")
    return get_extreme_expenses(expenses, mode)

@app.get("/reports/average")
def calculate_average_expense():
    expenses = load_expenses()
    return get_average_expense(expenses)

@app.get("/reports/summary")
def get_summary_report():
    expenses = load_expenses()
    return get_summary(expenses)


@app.put("/budget/{month}", status_code=200)
def set_budget(month: str, amount: float = Body(gt=0)):
    save_budget(month, amount)
    return {"month": month, "amount": amount}

@app.get("/budget/overview")
def get_overview():
    expenses = load_expenses()
    budget_dict = load_budget()
    current_month = datetime.date.today().strftime("%Y-%m")
    monthly_budget = budget_dict.get(current_month, 0)
    monthly_expenses = get_expenses_by_month(current_month, expenses)
    return {
        "transactions": len(monthly_expenses),
        "spent": get_total_spent(monthly_expenses),
        "monthly_budget": monthly_budget,
        "remaining": calculate_remaining_budget({"monthly_budget": monthly_budget}, expenses),
        "percentage_used": calculate_budget_percentage(monthly_budget, expenses),
        "excess": calculate_budget_excess(monthly_budget, expenses),
    }


@app.get("/expenses/sorted")
def get_sorted_expenses(field: str, reverse: bool = False):
    valid_fields = {"id", "amount", "date", "category", "description"}
    if field not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Valid fields are: {', '.join(valid_fields)}")
    expenses = load_expenses()
    return sort_expenses(expenses, field, reverse)


@app.get("/filtered/category")
def filter_expenses_by_category(category: str):
    category = category.title()
    expenses = load_expenses()
    return filter_by_category(expenses, category)

@app.get("/filtered/date")
def filter_expenses_by_date(date: str):
    expenses = load_expenses()
    return filter_by_date(expenses, date)

@app.get("/filtered/description")
def filter_expenses_by_description(description: str):
    description = description.lower()
    expenses = load_expenses()
    return filter_by_description(expenses, description)