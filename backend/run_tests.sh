#!/bin/bash

# This script sets up a Python virtual environment, installs dependencies, and runs Django tests with coverage.\

echo "Activating virtual environment..."
source venv/Scripts/activate  

echo "Installing backend dependencies..."
pip install -r requirements.txt


echo "Running Django tests with coverage..."
coverage run --source='.' manage.py test


coverage report

if [ $? -eq 0 ]; then
    echo "All tests passed."
else
    echo "Some tests failed."
    exit 1
fi
