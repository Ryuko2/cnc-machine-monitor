@echo off
REM CNC Machine Monitor - Green Theme Edition
REM Startup Script for Windows

echo ==========================================
echo CNC Machine Monitor - Green Theme
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if backend exists
if not exist "backend\api.py" (
    echo Error: backend\api.py not found
    echo Please run this script from the complete-green-deployment folder
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install fastapi uvicorn websockets --break-system-packages >nul 2>&1

echo.
echo ==========================================
echo Starting CNC Machine Monitor...
echo ==========================================
echo.
echo Backend API: http://localhost:5000
echo Dashboard:   http://localhost:5000
echo.
echo To access from phone:
echo 1. Find your computer's IP (run 'ipconfig')
echo 2. Open browser on phone to: http://YOUR-IP:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ==========================================
echo.

REM Start the server
cd backend
python api.py
