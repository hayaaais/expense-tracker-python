import pytest
from reports import (
    get_category_totals,
    get_extreme_expenses,
    get_total_spent,
    get_average_expense,
    get_highest_amount,
    get_lowest_amount,
    get_summary,
)


@pytest.fixture
def sample_expenses():
    return [
        {
            "id": 1,
            "amount": 100.0,
            "category": "Food",
            "description": "Lunch",
            "date": "2026-07-01",
        },
        {
            "id": 2,
            "amount": 50.0,
            "category": "Transport",
            "description": "Bus",
            "date": "2026-07-02",
        },
        {
            "id": 3,
            "amount": 200.0,
            "category": "Food",
            "description": "Dinner",
            "date": "2026-07-03",
        },
        {
            "id": 4,
            "amount": 50.0,
            "category": "Transport",
            "description": "Taxi",
            "date": "2026-07-04",
        },
    ]


# --- get_category_totals ---


def test_get_category_totals_sums_by_category(sample_expenses):
    totals = get_category_totals(sample_expenses)
    assert totals == {"Food": 300.0, "Transport": 100.0}


def test_get_category_totals_empty_list():
    assert get_category_totals([]) == {}


def test_get_category_totals_returns_alphabetically_sorted_keys():
    expenses = [
        {"amount": 10, "category": "Zebra"},
        {"amount": 5, "category": "Apple"},
    ]
    assert list(get_category_totals(expenses).keys()) == ["Apple", "Zebra"]


# --- get_extreme_expenses ---


def test_get_extreme_expenses_highest(sample_expenses):
    result = get_extreme_expenses(sample_expenses, mode="highest")
    assert len(result) == 1
    assert result[0]["amount"] == 200.0


def test_get_extreme_expenses_lowest(sample_expenses):
    # Two Transport expenses tie for lowest (50.0 each) -> both are returned
    result = get_extreme_expenses(sample_expenses, mode="lowest")
    assert len(result) == 2
    assert all(e["amount"] == 50.0 for e in result)


def test_get_extreme_expenses_handles_ties():
    # Two expenses tie for the highest amount -> both should be returned
    expenses = [
        {"amount": 100, "category": "A"},
        {"amount": 100, "category": "B"},
        {"amount": 20, "category": "C"},
    ]
    result = get_extreme_expenses(expenses, mode="highest")
    assert len(result) == 2
    assert {r["category"] for r in result} == {"A", "B"}


def test_get_extreme_expenses_empty_list_returns_empty():
    # Regression test: this used to raise IndexError before the fix
    assert get_extreme_expenses([], mode="highest") == []
    assert get_extreme_expenses([], mode="lowest") == []


# --- get_total_spent ---


def test_get_total_spent(sample_expenses):
    assert get_total_spent(sample_expenses) == 400.0


def test_get_total_spent_empty_list():
    assert get_total_spent([]) == 0


# --- get_average_expense ---


def test_get_average_expense(sample_expenses):
    assert get_average_expense(sample_expenses) == 100.0


def test_get_average_expense_empty_list_does_not_divide_by_zero():
    assert get_average_expense([]) == 0


# --- get_highest_amount / get_lowest_amount ---


def test_get_highest_amount(sample_expenses):
    assert get_highest_amount(sample_expenses) == 200.0


def test_get_lowest_amount(sample_expenses):
    assert get_lowest_amount(sample_expenses) == 50.0


# --- get_summary ---


def test_get_summary(sample_expenses):
    summary = get_summary(sample_expenses)
    assert summary == {
        "total_expenses": 4,
        "total_spent": 400.0,
        "average_expense": 100.0,
        "highest_expense": 200.0,
        "lowest_expense": 50.0,
    }
