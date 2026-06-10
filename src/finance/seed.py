import random
from datetime import date

from src.finance.service import FinancialService


INCOME_CATEGORIES = [
    "salary",
    "freelance",
]

EXPENSE_CATEGORIES = [
    "food",
    "transport",
    "rent",
    "utilities",
    "entertainment",
    "health",
]


def random_amount(category: str) -> float:
    ranges = {
        "salary": (3000, 7000),
        "freelance": (500, 3000),
        "food": (10, 100),
        "transport": (5, 50),
        "rent": (500, 1500),
        "utilities": (50, 300),
        "entertainment": (20, 200),
        "health": (20, 500),
    }

    minimum, maximum = ranges[category]
    return round(random.uniform(minimum, maximum), 2)


def seed_transactions(count: int = 50) -> None:
    service = FinancialService()

    current_year = date.today().year

    categories = (
        INCOME_CATEGORIES
        + EXPENSE_CATEGORIES
    )

    for _ in range(count):
        category = random.choice(categories)

        transaction_type = (
            "income"
            if category in INCOME_CATEGORIES
            else "expense"
        )

        transaction_date = date(
            current_year,
            random.randint(1, 3),      # January–March
            random.randint(1, 28),     # Safe for all months
        )

        service.add_transaction(
            transaction_type=transaction_type,
            amount=random_amount(category),
            category=category,
            description=f"Seeded {category} transaction",
            date=transaction_date.strftime("%Y-%m-%d"),
        )

    print(
        f"Successfully seeded {count} transactions."
    )


if __name__ == "__main__":
    seed_transactions(50)