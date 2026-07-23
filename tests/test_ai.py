import datetime
import pytest
import ai


class _FixedDate(datetime.date):
    """A date subclass that always returns a fixed 'today' for deterministic tests."""

    @classmethod
    def today(cls):
        return cls(2026, 7, 15)


@pytest.fixture
def fixed_today(monkeypatch):
    """Freeze ai.py's notion of 'today' to 2026-07-15 (day 15 of the month)."""
    monkeypatch.setattr(ai.datetime, "date", _FixedDate)


@pytest.fixture
def sample_budget_status():
    return {
        "transactions": 3,
        "spent": 4500.0,
        "monthly_budget": 10000.0,
        "remaining": 5500.0,
        "percentage_used": 45.0,
        "excess": 0,
    }


@pytest.fixture
def sample_expenses():
    return [
        {
            "amount": 3000.0,
            "category": "Food",
            "description": "Groceries",
            "date": "2026-07-01",
        },
        {
            "amount": 1500.0,
            "category": "Transport",
            "description": "Taxi",
            "date": "2026-07-10",
        },
    ]


# --- predict_monthly_spending ---


def test_predict_monthly_spending_projects_based_on_daily_pace(
    fixed_today, sample_budget_status
):
    projected = ai.predict_monthly_spending(sample_budget_status)
    assert projected == 9000.0


def test_predict_monthly_spending_on_day_one_multiplies_spent_by_30(
    monkeypatch, sample_budget_status
):
    monkeypatch.setattr(
        ai.datetime,
        "date",
        type(
            "D1", (datetime.date,), {"today": classmethod(lambda cls: cls(2026, 7, 1))}
        ),
    )
    projected = ai.predict_monthly_spending(sample_budget_status)
    assert projected == sample_budget_status["spent"] * 30.0


def test_predict_monthly_spending_zero_spent_returns_zero(fixed_today):
    assert ai.predict_monthly_spending({"spent": 0.0}) == 0.0


def test_predict_monthly_spending_missing_spent_key_defaults_to_zero(fixed_today):
    assert ai.predict_monthly_spending({}) == 0.0


# --- build_financial_context ---


def test_build_financial_context_includes_budget_numbers(
    sample_expenses, sample_budget_status
):
    context = ai.build_financial_context(sample_expenses, sample_budget_status)
    assert "4500.00" in context
    assert "10000.00" in context
    assert "45.0%" in context


def test_build_financial_context_includes_each_transaction(
    sample_expenses, sample_budget_status
):
    context = ai.build_financial_context(sample_expenses, sample_budget_status)
    assert "Groceries" in context
    assert "Taxi" in context
    assert "Food" in context
    assert "Transport" in context


def test_build_financial_context_empty_expenses_says_so_explicitly(
    sample_budget_status,
):
    context = ai.build_financial_context([], sample_budget_status)
    assert "No transactions logged yet." in context


def test_build_financial_context_handles_missing_budget_keys_gracefully():
    context = ai.build_financial_context([], {})
    assert "0.00" in context
