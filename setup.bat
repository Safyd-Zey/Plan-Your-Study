@REM Plan Your Study - Quick Start Script for Windows
@REM This script sets up the entire application

@echo off
setlocal enabledelayedexpansion

cls
echo ==========================================
echo Plan Your Study - Quick Start (Windows)
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is required but not installed.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found: 
python --version

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is required but not installed.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] npm found: 
npm --version
echo.

REM Setup Backend
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)

echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo Setting up frontend...
cd ..\frontend

echo Installing npm dependencies...
call npm install --quiet

if not exist ".env.local" (
    echo Creating .env.local file from template...
    copy .env.example .env.local
)

echo [OK] Frontend setup complete
echo.

cls
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the application, open TWO command windows:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open your browser:
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo.
echo For detailed instructions, see SETUP_GUIDE.md
echo.
pause
