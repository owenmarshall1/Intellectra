@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    pause
    exit /b
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b
)

echo Starting the Travel Application...
python TravelAppGUI.py
if %errorlevel% neq 0 (
    echo Failed to start the application.
    pause
    exit /b
)

echo Application started successfully!
pause