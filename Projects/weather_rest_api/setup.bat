@echo off
echo ====================================
echo Weather REST API Setup Script
echo ====================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and added to PATH
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Edit .env file and add your WEATHER_API_KEY
echo 2. Run: run.bat  (or: venv\Scripts\activate ^&^& python app.py)
echo.
pause