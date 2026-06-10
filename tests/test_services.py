import pytest

from src.finance.model import Transaction
from src.finance.repository import TransactionRepository
from src.finance.service import FinancialService


@pytest.fixture
def service(tmp_path):
    repository = TransactionRepository(
        tmp_path / "test_repository.json"
    )
    return FinancialService(repository)


def test_add_valid_transaction(service):
    service.add_transaction(
        "income",
        5000,
        "salary",
        "Monthly salary",
        "2026-01-15",
    )

    transactions = service.get_all_transactions()

    assert len(transactions) == 1
    assert transactions[0].amount == 5000


def test_reject_negative_amount():
    with pytest.raises(ValueError):
        Transaction(
            transaction_type="expense",
            category="food",
            amount=-100,
            description="Lunch",
        )


def test_monthly_summary_arithmetic(service):
    service.add_transaction(
        "income",
        5000,
        "salary",
        "Salary",
        "2026-01-10",
    )

    service.add_transaction(
        "expense",
        1500,
        "food",
        "Groceries",
        "2026-01-11",
    )

    service.add_transaction(
        "expense",
        500,
        "transport",
        "Bus fare",
        "2026-01-12",
    )

    summary = service.monthly_summary(2026, 1)

    assert summary["total_income"] == 5000
    assert summary["total_expense"] == 2000
    assert summary["net"] == 3000


def test_monthly_summary_groups_categories(service):
    service.add_transaction(
        "expense",
        100,
        "food",
        "Lunch",
        "2026-01-01",
    )

    service.add_transaction(
        "expense",
        200,
        "food",
        "Dinner",
        "2026-01-02",
    )

    summary = service.monthly_summary(2026, 1)

    assert summary["by_category"]["food"] == 300


def test_top_categories_returns_correct_order(service):
    service.add_transaction(
        "expense",
        100,
        "transport",
        "Taxi",
        "2026-01-01",
    )

    service.add_transaction(
        "expense",
        700,
        "food",
        "Groceries",
        "2026-01-02",
    )

    service.add_transaction(
        "expense",
        300,
        "health",
        "Medicine",
        "2026-01-03",
    )

    result = service.top_categories()

    categories = list(result.keys())

    assert categories == [
        "food",
        "health",
        "transport",
    ]


def test_date_range_filter_excludes_out_of_range_transactions(service):
    service.add_transaction(
        "expense",
        100,
        "food",
        "Lunch",
        "2026-01-10",
    )

    service.add_transaction(
        "expense",
        100,
        "food",
        "Lunch",
        "2026-03-10",
    )

    result = service.filter_by_date_range(
        "2026-01-01",
        "2026-01-31",
    )

    assert len(result) == 1
    assert result[0].date == "2026-01-10"


def test_filter_by_category_is_case_insensitive(service):
    service.add_transaction(
        "expense",
        100,
        "food",
        "Lunch",
        "2026-01-10",
    )

    result = service.filter_by_category("FOOD")

    assert len(result) == 1
    assert result[0].category == "food"


def test_transaction_round_trip():
    transaction = Transaction(
        transaction_type="income",
        category="salary",
        amount=5000,
        description="Monthly salary",
    )

    restored = Transaction.from_dict(
        transaction.to_dict()
    )

    assert restored == transaction

def test_filter_by_category_returns_empty_list(service):
    result = service.filter_by_category("nonexistent")

    assert result == []


def test_monthly_summary_empty_month(service):
    summary = service.monthly_summary(2026, 1)

    assert summary == {
        "total_income": 0,
        "total_expense": 0,
        "net": 0,
        "by_category": {},
    }


def test_monthly_summary_ignores_other_months(service):
    service.add_transaction(
        "income",
        5000,
        "salary",
        "Salary",
        "2026-02-01",
    )

    summary = service.monthly_summary(2026, 1)

    assert summary["total_income"] == 0
    assert summary["total_expense"] == 0


def test_top_categories_ignores_income(service):
    service.add_transaction(
        "income",
        10000,
        "salary",
        "Salary",
        "2026-01-01",
    )

    service.add_transaction(
        "expense",
        500,
        "food",
        "Groceries",
        "2026-01-02",
    )

    result = service.top_categories()

    assert "salary" not in result
    assert result["food"] == 500


def test_top_categories_returns_requested_number(service):
    service.add_transaction(
        "expense",
        100,
        "food",
        "Lunch",
        "2026-01-01",
    )

    service.add_transaction(
        "expense",
        200,
        "health",
        "Medicine",
        "2026-01-01",
    )

    service.add_transaction(
        "expense",
        300,
        "transport",
        "Taxi",
        "2026-01-01",
    )

    result = service.top_categories(2)

    assert len(result) == 2


def test_transaction_rejects_invalid_date():
    with pytest.raises(ValueError):
        Transaction(
            transaction_type="expense",
            category="food",
            amount=100,
            description="Lunch",
            date="01-01-2026",
        )


def test_transaction_to_dict_contains_expected_keys():
    transaction = Transaction(
        transaction_type="income",
        category="salary",
        amount=5000,
        description="Salary",
    )

    data = transaction.to_dict()

    assert "id" in data
    assert "date" in data
    assert "amount" in data
    assert "category" in data


def test_add_multiple_transactions(service):
    service.add_transaction(
        "income",
        5000,
        "salary",
        "Salary",
        "2026-01-01",
    )

    service.add_transaction(
        "expense",
        100,
        "food",
        "Lunch",
        "2026-01-02",
    )

    transactions = service.get_all_transactions()

    assert len(transactions) == 2
