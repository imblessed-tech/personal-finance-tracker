from datetime import datetime
from collections import defaultdict, Counter
from src.finance.repository import TransactionRepository 
from src.finance.model import Transaction


class FinancialService:
    def __init__(self, repository : TransactionRepository = None) -> None:
        self.repository = repository or TransactionRepository()


    def add_transaction(self, transaction_type, amount, category, description, date = None) -> None:
        
        transaction_data = {
            "transaction_type": transaction_type,
            "amount": amount,
            "category": category,
            "description": description,
        }

        if date is not None:
            transaction_data["date"] = date

        transaction = Transaction(**transaction_data)
        self.repository.save(transaction)


    def monthly_summary(self, year: int, month:int) -> dict:
        if not 1 <= month <= 12:
            raise ValueError("month must be between 1 and 12")  

        all_transactions = self.repository.get_all()

        total_income = 0
        total_expense = 0
        by_category = defaultdict(float)

        for transaction in all_transactions:
            date_obj = datetime.strptime(transaction.date, "%Y-%m-%d")
            date_month = date_obj.month
            date_year = date_obj.year

            if date_month == month and date_year == year:
                
                if transaction.transaction_type == 'income':
                    total_income += transaction.amount                    
                elif transaction.transaction_type == 'expense':
                    total_expense += transaction.amount
                    by_category[transaction.category] += transaction.amount

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net": total_income - total_expense,
            "by_category": dict(by_category)
        }

    def top_categories(self, n: int = 5) -> dict:
        if not isinstance(n, int):
            raise ValueError("n must be an integer")

        all_transactions = self.repository.get_all()

        category_totals = Counter()

        for transaction in all_transactions:
            if transaction.transaction_type == "expense":
                category_totals[transaction.category] += transaction.amount

        return dict(category_totals.most_common(n))


    def filter_by_date_range(self, start_date:str, end_date:str) -> list:

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if start_date > end_date:
            raise ValueError(
                "start_date must be before end_date"
            )

        all_transactions = self.repository.get_all()

        transaction_in_range = []
        for transaction in all_transactions:
            date_obj = datetime.strptime(transaction.date, "%Y-%m-%d")
            if start_date <= date_obj <= end_date:
                transaction_in_range.append(transaction)
        return transaction_in_range

    def filter_by_category(self, category: str) -> list:
        all_transactions = self.repository.get_all()
        
        transaction_by_category = []
        for transaction in all_transactions:
            if category.lower() == transaction.category.lower():
                transaction_by_category.append(transaction)
        return transaction_by_category

    def get_all_transactions(self) -> list[Transaction]:
        return self.repository.get_all()

    def delete_transaction(self, transaction_id: str) -> bool:
        return self.repository.delete(transaction_id)






        
           


        

        
        
        