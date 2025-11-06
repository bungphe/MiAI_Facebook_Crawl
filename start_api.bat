@echo off
REM Multi-Platform Social Media Posting API - Startup Script (Windows)

echo ==========================================
echo Multi-Platform Social Media Posting API
echo ==========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env file with your API credentials
    echo.
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Create necessary directories
echo Creating directories...
if not exist uploads mkdir uploads
if not exist logs mkdir logs
echo Directories created
echo.

REM Start the API server
echo Starting API server...
echo    URL: http://localhost:8000
echo    Docs: http://localhost:8000/docs
echo    Press Ctrl+C to stop
echo.
echo ==========================================
echo.

python main.py
