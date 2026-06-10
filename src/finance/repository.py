from src.finance.model import Transaction
from src.finance.exception import StorageError

import json

from dataclasses import field
from pathlib import Path

class TransactionRepository:

    def __init__(self, file_path: Path = None) -> None:
        if file_path is None:
            self.file_path = Path("output") / "repository.json"
        else:
            self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.touch(exist_ok=True)


    def _write_all(self, transactions) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                [t.to_dict() for t in transactions],
                file,
                indent=4,
                default=str,
        )


    def save(self, transaction) -> None:
        transactions = self.get_all()
        transactions.append(transaction)
        self._write_all(transactions)

        
    def get_all(self) -> list[Transaction]:
        if self.file_path.stat().st_size == 0:
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as exc:
                raise StorageError("Repository File is corrupted") from exc

        return [Transaction.from_dict(item) for item in data]


    def get_by_id(self, transaction_id : str) -> Transaction | None:
        transactions = self.get_all()

        for transaction in transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def update(self, transaction_id: str, update_payload: dict) -> bool:
        transactions = self.get_all()

        for index, transaction in enumerate(transactions):
            if transaction.id == transaction_id:
                updated_data = transaction.to_dict()
                updated_data.update(update_payload)
                updated_data["id"] = transaction.id
                updated_transaction = Transaction.from_dict(updated_data)
                transactions[index] = updated_transaction
                self._write_all(transactions)
                return True
        return False


    def delete(self, transaction_id : str) -> bool:
        transactions = self.get_all()

        for transaction in transactions:
            if transaction.id == transaction_id:
                transactions.remove(transaction)
                self._write_all(transactions)
                return True
        return False