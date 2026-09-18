#!/bin/bash

echo "===================================="
echo "Starting Weather REST API Server"
echo "===================================="
echo ""

# Check if venv exists
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Please create a .env file with your WEATHER_API_KEY"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting Flask server..."
echo "Server will be available at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""

python app.py