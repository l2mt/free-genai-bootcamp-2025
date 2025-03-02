# Writing Practice

A simple Python application to help you practice writing in different styles using AI assistance.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

Run the main script:
```
python main.py
```

## Project Structure

- `main.py`: Main application entry point
- `data/`: Contains training data and sentences
- `utils/`: Utility functions for API integration and image processing 