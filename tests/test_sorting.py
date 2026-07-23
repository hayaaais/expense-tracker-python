from sorting import sort_expenses

SAMPLE = [
    {"amount": 30.0, "category": "Food", "description": "Snacks", "date": "2026-07-05"},
    {
        "amount": 10.0,
        "category": "Transport",
        "description": "Bus",
        "date": "2026-07-01",
    },
    {"amount": 50.0, "category": "Bills", "description": "Wifi", "date": "2026-07-10"},
]


def test_sort_by_amount_ascending():
    result = sort_expenses(SAMPLE, "amount", reverse=False)
    assert [e["amount"] for e in result] == [10.0, 30.0, 50.0]

def test_sort_by_amount_descending():
    result = sort_expenses(SAMPLE, "amount", reverse=True)
    assert [e["amount"] for e in result] == [50.0, 30.0, 10.0]

def test_sort_by_date_ascending():
    result = sort_expenses(SAMPLE, "date", reverse=False)
    assert [e["date"] for e in result] == ["2026-07-01", "2026-07-05", "2026-07-10"]

def test_sort_by_category_alphabetical():
    result = sort_expenses(SAMPLE, "category", reverse=False)
    assert [e["category"] for e in result] == ["Bills", "Food", "Transport"]

def test_sort_does_not_mutate_original_list():
    original_order = [e["amount"] for e in SAMPLE]
    sort_expenses(SAMPLE, "amount", reverse=True)
    assert [e["amount"] for e in SAMPLE] == original_order

def test_sort_empty_list_returns_empty():
    assert sort_expenses([], "amount", reverse=False) == []