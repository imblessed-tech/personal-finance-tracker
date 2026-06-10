from dataclasses import asdict, dataclass, field
from datetime import datetime, date
from typing import Literal
import uuid


@dataclass
class Transaction:
    transaction_type: Literal["income", "expense"]
    category: str
    amount: float
    description: str

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: str = field(default_factory=lambda: date.today().strftime("%Y-%m-%d"))

    def __post_init__(self) -> None:
        # Validate amount
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero")

        # Validate date format
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Date must be in YYYY-MM-DD format") from exc

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(**data)
        