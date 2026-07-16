import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import initialize_database, load_expenses, insert_expense, delete_expense

app = FastAPI()
initialize_database()


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)
    category: str
    description: str
    date: str | None = None 


@app.get("/expenses")
def get_expenses():
    return load_expenses()


@app.post("/expenses")
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
