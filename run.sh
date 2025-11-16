#!/bin/bash
# -------------------------------------------------
# FastAPI Chat System Setup & Run Script
# -------------------------------------------------

# Exit on error
set -e

# Python environment name
ENV_NAME=".venv"

echo "-------------------------------"
echo "Setting up Python environment..."
echo "-------------------------------"

# Create virtual environment if it doesn't exist
if [ ! -d "$ENV_NAME" ]; then
    python3 -m venv $ENV_NAME
    echo "✅ Virtual environment created: $ENV_NAME"
else
    echo "⚡ Virtual environment already exists: $ENV_NAME"
fi

# Activate virtual environment
source $ENV_NAME/bin/activate

echo "-------------------------------"
echo "Installing dependencies..."
echo "-------------------------------"

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "-------------------------------"
echo "Starting FastAPI server..."
echo "-------------------------------"

# Run FastAPI with reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
