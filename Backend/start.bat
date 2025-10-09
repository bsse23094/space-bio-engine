@echo off
REM Space Biology Knowledge Engine - Backend Startup Script (Windows)
REM This script sets up and runs the FastAPI backend server

echo 🚀 Starting Space Biology Knowledge Engine Backend...

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found

REM Check if we're in the Backend directory
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found. Please run this script from the Backend directory.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated

REM Upgrade pip in virtual environment
echo [INFO] Upgrading pip in virtual environment...
.venv\Scripts\python.exe -m ensurepip --default-pip
.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

REM Install dependencies in virtual environment
echo [INFO] Installing dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies may have failed to install. Continuing anyway...
) else (
    echo [SUCCESS] Dependencies installed successfully
)

REM Check if data files exist
echo [INFO] Checking data files...
set MISSING_FILES=0

if not exist "..\datasets\sb_publications_clean.csv" (
    echo [WARNING] Missing: ../datasets/sb_publications_clean.csv
    set MISSING_FILES=1
)

if not exist "..\datasets\topics.csv" (
    echo [WARNING] Missing: ../datasets/topics.csv
    set MISSING_FILES=1
)

if not exist "..\datasets\embeddings.npy" (
    echo [WARNING] Missing: ../datasets/embeddings.npy
    set MISSING_FILES=1
)

if not exist "..\datasets\metadata.json" (
    echo [WARNING] Missing: ../datasets/metadata.json
    set MISSING_FILES=1
)

if %MISSING_FILES%==0 (
    echo [SUCCESS] All data files found
) else (
    echo [WARNING] Some data files are missing. The API will run with limited functionality.
)

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%
set API_HOST=0.0.0.0
set API_PORT=8000
set API_DEBUG=True

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Start the server
echo [INFO] Starting FastAPI server...
echo [INFO] Server will be available at:
echo   📖 API Documentation: http://localhost:8000/docs
echo   📚 Alternative Docs: http://localhost:8000/redoc
echo   ❤️  Health Check: http://localhost:8000/health
echo   📊 API Stats: http://localhost:8000/api/v1/stats
echo.
echo [INFO] Press Ctrl+C to stop the server
echo.

REM Start uvicorn server using virtual environment python
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info

REM If uvicorn fails, try alternative startup
if %errorlevel% neq 0 (
    echo [WARNING] Uvicorn failed, trying alternative startup method...
    .venv\Scripts\python.exe app\main.py
)

pause