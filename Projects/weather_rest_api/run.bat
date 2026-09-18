@echo off
echo ====================================
echo Starting Weather REST API Server
echo ====================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found
    echo Please create a .env file with your WEATHER_API_KEY
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

python app.py

pause