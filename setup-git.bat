@echo off
REM CNC Machine Monitor - GitHub Setup Script (Windows)
REM This script prepares your project for GitHub

echo ==========================================
echo CNC Machine Monitor - GitHub Setup
echo ==========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git first:
    echo   Download from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Check if this is already a git repository
if exist .git (
    echo WARNING: This is already a Git repository
    echo.
    set /p REINIT="Do you want to reinitialize? (y/N): "
    if /i "%REINIT%"=="y" (
        rmdir /s /q .git
        echo [OK] Removed existing Git repository
    ) else (
        echo Keeping existing repository
        exit /b 0
    )
)

REM Initialize git repository
echo Initializing Git repository...
git init
echo [OK] Git repository initialized
echo.

REM Set default branch to main
git branch -M main
echo [OK] Default branch set to 'main'
echo.

REM Add all files
echo Adding files to Git...
git add .
echo [OK] Files added
echo.

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: CNC Machine Monitor v1.0.0" -m "Features:" -m "- Real-time machine monitoring via WebSocket" -m "- Support for 5 machine types" -m "- SQLite database for historical data" -m "- REST API with comprehensive endpoints" -m "- Mobile-responsive dashboard" -m "- Cross-platform support (Windows/Mac/Linux)" -m "- Docker support" -m "- Comprehensive documentation"

echo [OK] Initial commit created
echo.

REM Display next steps
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo.
echo 1. Create a new repository on GitHub:
echo    - Go to https://github.com/new
echo    - Name: cnc-machine-monitor
echo    - Description: Real-time CNC machine monitoring dashboard
echo    - Keep it Public or Private
echo    - DON'T initialize with README, .gitignore, or license
echo.
echo 2. Connect to GitHub and push:
echo    git remote add origin https://github.com/YOUR-USERNAME/cnc-machine-monitor.git
echo    git push -u origin main
echo.
echo 3. Optional - Add topics to your GitHub repo:
echo    - cnc
echo    - manufacturing
echo    - iot
echo    - monitoring
echo    - fastapi
echo    - websocket
echo.
echo 4. Update README.md with your GitHub username
echo.
echo ==========================================
echo.
echo For detailed deployment instructions, see:
echo   - INSTALLATION.md
echo   - DEPLOYMENT.md
echo   - API_DOCUMENTATION.md
echo.
pause
