import datetime
import pytest
import budget

class _FixedDate(datetime.date):
    """A date subclass that always returns a fixed 'today' for deterministic tests."""

    @classmethod
    def today(cls):
        return cls(2026, 7, 15)

@pytest.fixture
def fixed_today(monkeypatch):
    """Freeze budget.py's notion of 'today' to 2026-07-15 (month = 2026-07)."""
    monkeypatch.setattr(budget.datetime, "date", _FixedDate)

@pytest.fixture
def sample_expenses():
    return [
        {"amount": 100.0, "category": "Food", "date": "2026-07-01"},
        {"amount": 50.0, "category": "Transport", "date": "2026-07-10"},
        {"amount": 300.0, "category": "Rent", "date": "2026-06-15"},
    ]


# --- get_expenses_by_month ---

def test_get_expenses_by_month_filters_by_month_prefix(sample_expenses):
    result = budget.get_expenses_by_month("2026-07", sample_expenses)
    assert len(result) == 2
    assert all(exp["date"].startswith("2026-07") for exp in result)

def test_get_expenses_by_month_no_match_returns_empty_list(sample_expenses):
    assert budget.get_expenses_by_month("2025-01", sample_expenses) == []


# --- get_current_month_total ---

def test_get_current_month_total_uses_todays_month(fixed_today, sample_expenses):
    assert budget.get_current_month_total(sample_expenses) == 150.0


# --- calculate_remaining_budget ---

def test_calculate_remaining_budget(fixed_today, sample_expenses):
    remaining = budget.calculate_remaining_budget({"monthly_budget": 500.0}, sample_expenses)
    assert remaining == 350.0

def test_calculate_remaining_budget_no_budget_set(fixed_today, sample_expenses):
    remaining = budget.calculate_remaining_budget({}, sample_expenses)
    assert remaining == -150.0


# --- calculate_budget_percentage ---

def test_calculate_budget_percentage(fixed_today, sample_expenses):
    percentage = budget.calculate_budget_percentage(300.0, sample_expenses)
    assert percentage == 50.0

def test_calculate_budget_percentage_zero_budget_returns_zero_not_none(fixed_today, sample_expenses):
    result = budget.calculate_budget_percentage(0, sample_expenses)
    assert result == 0.0
    assert result is not None

def test_calculate_budget_percentage_negative_budget_returns_zero(fixed_today, sample_expenses):
    result = budget.calculate_budget_percentage(-100, sample_expenses)
    assert result == 0.0


# --- calculate_budget_excess ---

def test_calculate_budget_excess_when_over(fixed_today, sample_expenses):
    assert budget.calculate_budget_excess(100.0, sample_expenses) == 50.0

def test_calculate_budget_excess_when_under_returns_zero(fixed_today, sample_expenses):
    assert budget.calculate_budget_excess(500.0, sample_expenses) == 0