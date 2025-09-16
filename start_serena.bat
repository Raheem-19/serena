@echo off
echo Starting Serena...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Check if we're in a virtual environment
if defined VIRTUAL_ENV (
    echo Using virtual environment: %VIRTUAL_ENV%
) else (
    echo Warning: Not in a virtual environment
    echo Consider creating one with: python -m venv venv
    echo.
)

REM Install Serena if not already installed
python -c "import serena" >nul 2>&1
if %errorlevel% neq 0 (
    echo Serena not found, installing...
    pip install -e .
    if %errorlevel% neq 0 (
        echo Error: Failed to install Serena
        pause
        exit /b 1
    )
)

REM Start the dashboard
echo Starting Serena dashboard...
python run_dashboard.py

if %errorlevel% neq 0 (
    echo Error: Failed to start dashboard
    pause
    exit /b 1
)

echo Dashboard stopped.
pause