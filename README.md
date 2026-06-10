# Personal Finance Tracker

A simple, robust, and clean command-line interface (CLI) tool in Python to track, manage, and analyze your personal financial transactions (income and expenses).

---

## Features

- **Add Transactions**: Track income or expenses with customizable categories, amounts, descriptions, and custom dates.
- **View All Transactions**: Display all recorded transactions in a neat, tabulated format.
- **Monthly Summary**: Get a quick overview of your total income, total expenses, net savings, and a breakdown of expenses by category for any month.
- **Top Spending Categories**: Identify your top spending categories to see where most of your money goes.
- **Filter by Category**: Look up transaction history for a specific category (case-insensitive).
- **Delete Transactions**: Easily remove any transaction using its unique ID.
- **Data Persistence**: Transactions are serialized and saved locally to `output/repository.json`.

---

## Project Structure

```text
├── output/                   # Holds the serialized JSON repository
│   └── repository.json
├── src/
│   └── finance/
│       ├── cli.py            # Command-Line Interface layout and options
│       ├── exception.py      # Custom errors (e.g., StorageError)
│       ├── model.py          # Transaction data structure and validation
│       ├── repository.py     # JSON file persistence layer
│       ├── seed.py           # Populates mockup transactions
│       └── service.py        # Core financial business logic
├── tests/
│   └── test_services.py      # Unit tests for the financial tracker
├── main.py                   # CLI entry point
├── pytest.ini                # Pytest configuration file
├── requirements.txt          # Python dependencies list
└── README.md                 # Project documentation
```

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/imblessed-tech/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Set up virtual environment
Create a virtual environment and activate it:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

To run the interactive CLI tracker, execute `main.py`:
```bash
python main.py
```

---

## Running Tests

To run the suite of unit tests with coverage, run:
```bash
pytest tests/test_services.py
```

Or run with code coverage report:
```bash
pytest --cov=src tests/test_services.py
```
