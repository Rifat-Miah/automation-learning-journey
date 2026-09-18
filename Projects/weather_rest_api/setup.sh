#!/bin/bash

echo "===================================="
echo "Weather REST API Setup Script"
echo "===================================="
echo ""

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/4] Upgrading pip..."
python -m pip install --upgrade pip

echo "[4/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Make run.sh executable
chmod +x run.sh

echo ""
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your WEATHER_API_KEY"
echo "2. Run: ./run.sh  (or: source venv/bin/activate && python app.py)"
echo ""