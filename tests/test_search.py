import datetime
import pytest
from search import (
    filter_by_category,
    filter_by_date,
    filter_by_description,
    parse_date,
)


@pytest.fixture
def sample_expenses():
    return [
        {"amount": 10.0, "category": "Food", "description": "Grocery run", "date": "2026-07-01"},
        {"amount": 20.0, "category": "Transport", "description": "Taxi ride", "date": "2026-07-02"},
        {"amount": 30.0, "category": "Food", "description": "Restaurant dinner", "date": "2026-07-02"},
    ]


# --- filter_by_category ---

def test_filter_by_category_matches(sample_expenses):
    result = filter_by_category(sample_expenses, "Food")
    assert len(result) == 2
    assert all(e["category"] == "Food" for e in result)


def test_filter_by_category_no_match_returns_empty(sample_expenses):
    assert filter_by_category(sample_expenses, "Rent") == []


def test_filter_by_category_is_case_sensitive(sample_expenses):
    # Matches current behavior: caller is expected to `.title()` input before calling.
    assert filter_by_category(sample_expenses, "food") == []


# --- filter_by_date ---

def test_filter_by_date_matches(sample_expenses):
    result = filter_by_date(sample_expenses, "2026-07-02")
    assert len(result) == 2


def test_filter_by_date_no_match(sample_expenses):
    assert filter_by_date(sample_expenses, "2020-01-01") == []


# --- filter_by_description ---

def test_filter_by_description_substring_match(sample_expenses):
    result = filter_by_description(sample_expenses, "dinner")
    assert len(result) == 1
    assert result[0]["description"] == "Restaurant dinner"


def test_filter_by_description_no_match(sample_expenses):
    assert filter_by_description(sample_expenses, "movie") == []


# --- parse_date ---

def test_parse_date_valid_format():
    date, error = parse_date("2026-07-14")
    assert date == "2026-07-14"
    assert error is None


def test_parse_date_blank_defaults_to_today():
    date, error = parse_date("")
    assert error is None
    assert date == datetime.date.today().strftime("%Y-%m-%d")


def test_parse_date_invalid_format_returns_error():
    date, error = parse_date("14-07-2026")
    assert date is None
    assert error is not None


def test_parse_date_strips_whitespace():
    date, error = parse_date("  2026-07-14  ")
    assert date == "2026-07-14"
    assert error is None
