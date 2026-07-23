import os
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception:
    client = None


def build_financial_context(expenses: list, budget_status: dict) -> str:
    current_month = datetime.date.today().strftime("%Y-%m")
    data = "\n".join([
        f"{e['date']}: ₸{e['amount']:.2f} under '{e['category']}' - ({e['description']})"
        for e in expenses])

    context = f"""
    Context Data for Month: {current_month}
    ---
    Total Transactions Logged: {budget_status.get('transactions', 0)}
    Total Spent This Month: ₸{budget_status.get('spent', 0.0):.2f}
    Monthly Budget Limit: ₸{budget_status.get('monthly_budget', 0.0):.2f}
    Remaining Balance: ₸{budget_status.get('remaining', 0.0):.2f}
    Percentage of Budget Used: {budget_status.get('percentage_used', 0.0):.1f}%
    Excess Spends: ₸{budget_status.get('excess', 0.0):.2f}

    Transaction History: {data if data else 'No transactions logged yet.'}
    """
    return context


def predict_monthly_spending(budget_status: dict) -> float:
    total_spent = budget_status.get("spent", 0.0)
    day_of_month = datetime.date.today().day

    if day_of_month == 1:
        return total_spent * 30.0

    daily_pace = total_spent / day_of_month
    projected_total = daily_pace * 30.0
    return projected_total


def generate_ai_analysis(expenses: list, budget_status: dict) -> str:
    context = build_financial_context(expenses, budget_status)
    projected_spend = predict_monthly_spending(budget_status)

    system_instruction = """
    You are an expert AI Financial Planner. Analyze the user's data context and generate a report.
    You MUST output your response using the EXACT Markdown template headings below. 
    Do not add extra conversational greetings. Rely STRICTLY on the real numbers provided.

    ### Spending Overview
    [Provide a 1-2 sentence overview noting the largest categories and what dominates their expenses]

    ### Budget Status
    [Detail their percentage used, pacing against the month, and note their projected total spend projection explicitly]

    ### Recommendations
    * [Actionable bullet point 1]
    * [Actionable bullet point 2]
    * [Actionable bullet point 3]

    ### Financial Health Score
    [Output ONLY a single integer score between 0 and 100 based on their budget tracking performance] / 100
    """

    user_prompt = f"Analyze my financial health based on this context:\n{context}\nProjected Spend Pace: ₸{projected_spend:.2f}"
    if client is None:
        raise RuntimeError("Gemini API key not configured")
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_prompt,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")
        


def ask_financial_advisor(expenses: list, budget_status: dict, user_question: str) -> str:
    context = build_financial_context(expenses, budget_status)

    system_instruction = f"""
    You are a helpful Personal Finance Assistant. Answer the user's custom question based on their data.
    Data Context: {context}
    Keep your answer conversational, highly specific, and limit it to 3 sentences max. Use Tenge (₸) formatting symbols.
    """

    if client is None:
        raise RuntimeError("Gemini API key not configured")
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_question,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")