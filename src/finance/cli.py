import dataclasses
from tabulate import tabulate

from src.finance.service import FinancialService


class FinanceCLI:
    def __init__(self, service=None):
        self.service = service or FinancialService()

    def run(self):

        while True:
            print("""
[1] Add transaction
[2] View all transactions
[3] Monthly summary
[4] Top spending categories
[5] Filter by category
[6] Delete a transaction
[7] Exit
""")

            try:
                choice = input("Select option: ").strip()

                match choice:
                    case "1":
                        print("\nProvide the following details:")
                        transaction_type = input("Transaction type [income or expense]: "
                                                ).strip().lower()

                        if transaction_type not in ["income", "expense"]:
                            print("Transaction type must be either 'income' or 'expense'.")
                            continue

                        try:
                            amount = float(input("Amount: "))
                        except ValueError:
                            print("Enter a valid number.")
                            continue

                        category = input("Category: ").strip()
                        description = input("Description: ").strip()

                        date = input("Date (optional, YYYY-MM-DD): ").strip()

                        if date == "":
                            date = None

                        self.service.add_transaction(
                            transaction_type,
                            amount,
                            category,
                            description,
                            date,
                        )

                        print("Transaction added successfully.")

                    case "2":
                        transactions = self.service.get_all_transactions()

                        if not transactions:
                            print("No transactions found.")
                            continue

                        for start in range(0, len(transactions), 10):
                            print("\n--- All Transactions ---")
                            page = transactions[start:start + 10]
                            print(tabulate([t.to_dict() for t in page],
                                            headers="keys",
                                            tablefmt="grid"))

                            if start + 10 < len(transactions):
                                user_input = input("Press Enter for next page or 'q' to quit: "
                                                ).strip().lower()

                                if user_input == "q":
                                    break

                    case "3":
                        print("Kindly Provide the month and year of the transaction")
                        try:
                            month = int(input("Month (e.g. 4): ").strip())
                            year = int(input("Year (e.g. 2026): ").strip())
                        except ValueError:
                            print("Enter a valid number.")
                            continue
                        summary = self.service.monthly_summary(year, month)

                        print(f"\n--- Monthly Summary: {month} {year} ---")
                        print("="*40)
                        print(f"Total income: ₦{summary['total_income']:,.2f}"  )
                        print(f"Total expense: ₦{summary['total_expense']:,.2f}")
                        print(f"Net: ₦{summary['net']:,.2f}")
                        print(f"By category: {summary['by_category']}")
                        print("="*40)

                    case "4":
                        print("Kindly Provide the number of top categories")
                        try:
                            n = int(input("Number of top categories: ").strip())
                        except ValueError:
                            print("Enter a valid number for the number of top categories.")
                            continue
                        top_categories = self.service.top_categories(n)
                        print(f"\n--- Top {n} Spending Categories ---")
                        print("="*40)
                        for category, amount in top_categories.items():
                            print(f"  {category}: ₦{amount:,.2f}")
                        print("="*40)

                    case "5":
                        print("Kindly Provide the category of the transaction")
                        category = input("Category: ").strip()
                        transaction_by_category = self.service.filter_by_category(category)
                        if not transaction_by_category:
                            print("No transactions found in this category.")
                            continue
                        print(f"\n--- Transactions in Category: {category} ---")
                        print("="*40)
                        print(tabulate([t.to_dict() for t in transaction_by_category],
                                        headers="keys",
                                        tablefmt="grid"))
                        print("="*40)

                    case "6":
                        print("Kindly provide the id of the transaction to delete")
                        transaction_id = input("Transaction ID: ").strip()
                        deleted = self.service.delete_transaction(transaction_id)
                        if not deleted:
                            print("No transaction found with this id.")
                            continue
                        print(f"\n--- Transaction Deleted: {transaction_id} ---")
                        print("="*40)
                        print("Transaction deleted successfully.")
                        print("="*40)

                    case "7":
                        print("Goodbye!")
                        break

                    case _:
                        print("Invalid option.")

            except ValueError as exc:
                print(f"Error: {exc}")

            except KeyboardInterrupt:
                print("\nOperation cancelled.")