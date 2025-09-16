@echo off
echo Serena Installation Script
echo =========================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Serena in development mode
echo Installing Serena...
pip install -e .
if %errorlevel% neq 0 (
    echo Error: Failed to install Serena
    pause
    exit /b 1
)

REM Install additional dependencies
echo Installing additional dependencies...
pip install flask requests pyright

echo.
echo Installation completed successfully!
echo.
echo To start Serena:
echo 1. Run: start_serena.bat
echo 2. Or manually: python run_dashboard.py
echo.
echo The dashboard will be available at: http://localhost:24287
echo.
pause