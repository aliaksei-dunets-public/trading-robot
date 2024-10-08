# TradingRobot

A Python project using FastAPI and GraphQL to build a trading robot API.


# Clone the repository
git clone https://github.com/aliaksei-dunets-public/trading-robot.git
cd TradingRobot

# Create virtual environment
python -m venv env

# Activate virtual environment
# macOS/Linux
source env/bin/activate
# Windows
.\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate requirements.txt
pip freeze > requirements.txt

# Configure environment variables
# Create .env file and add:
# MONGO_URI=your_mongodb_uri
# API_KEY=your_secret_api_key

# Start FastAPI application
uvicorn app.main:app --reload

# Access GraphQL Playground
# Open browser and go to:
# http://127.0.0.1:8000/graphql

# Run tests
pytest

# Run tests with coverage details
pytest --cov=app --cov-report term-missing
pytest --cov=app --cov-report html

# Run a single file
pytest -v tests/models/test_models.py
