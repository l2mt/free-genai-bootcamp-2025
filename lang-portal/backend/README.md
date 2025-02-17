# Language Learning Portal Backend

This is the backend service for the Language Learning Portal, built with FastAPI and SQLAlchemy.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd lang-portal/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

On Windows:
```bash
source venv/Scripts/activate  # Git Bash
# OR
.\venv\Scripts\activate      # PowerShell
# OR
venv\Scripts\activate.bat    # Command Prompt
```

On Unix or MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database:
```bash
python init_db.py
```

6. Load seed data (optional):
```bash
python seed_data.py
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Testing

1. Install test dependencies:
```bash
pip install pytest pytest-cov
```

2. Run tests:
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app tests/ --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app tests/ --cov-report=html
```

The HTML coverage report will be generated in the `htmlcov` directory. Open `htmlcov/index.html` in a web browser to view the detailed coverage report.

## Project Structure

```
backend/
├── app/                    # Application package
│   ├── routers/           # API route handlers
│   ├── models.py          # Database models
│   ├── database.py        # Database configuration
│   └── main.py           # Application entry point
├── migrations/            # Database migrations
├── tests/                # Test suite
├── seeds/                # Seed data
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Development Guidelines

1. Always work within the virtual environment
2. Add new dependencies to `requirements.txt`
3. Write tests for new features
4. Update database migrations when modifying models
5. Follow PEP 8 style guide

## Common Issues

1. If you get database errors, try:
   - Delete the existing `words.db` file
   - Run `python init_db.py` again
   - Run `python seed_data.py` to reload test data

2. Virtual environment issues:
   - Make sure you've activated the virtual environment
   - Check that all dependencies are installed within the virtual environment